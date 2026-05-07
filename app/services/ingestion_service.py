from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.enums import DocumentStatus, normalize_capability_status, normalize_document_status, normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.chunking_service import chunk_text
from app.services.document_extraction_service import extract_text
from app.services.hashing_service import sha256_bytes
from app.services.source_authority import get_source_authority


class IngestionError(ValueError):
    pass


def _get_existing_document_by_sha(db: Session, file_sha256: str) -> KnowledgeDocument | None:
    return db.scalar(select(KnowledgeDocument).where(KnowledgeDocument.FileSha256 == file_sha256))


def ingest_file_bytes(
    db: Session,
    content: bytes,
    original_file_name: str,
    source_type: str = "OTHER",
    capability_status: str | None = None,
    tenant_id: str | None = None,
    stored_file_path: str | None = None,
    title: str | None = None,
) -> tuple[KnowledgeDocument, bool]:
    file_sha256 = sha256_bytes(content)
    existing = _get_existing_document_by_sha(db, file_sha256)
    if existing:
        return existing, True

    try:
        normalized_source_type = normalize_source_type(source_type)
        normalized_capability_status = normalize_capability_status(capability_status)
    except ValueError as exc:
        raise IngestionError(str(exc)) from exc

    text = extract_text(content, original_file_name)
    settings = get_settings()
    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise IngestionError("The document did not produce any non-empty chunks.")

    document = KnowledgeDocument(
        TenantId=tenant_id,
        SourceType=normalized_source_type,
        SourceAuthority=get_source_authority(normalized_source_type),
        CapabilityStatus=normalized_capability_status,
        OriginalFileName=original_file_name,
        StoredFilePath=stored_file_path,
        FileExtension=Path(original_file_name).suffix.lower().lstrip("."),
        FileSha256=file_sha256,
        Title=title or Path(original_file_name).stem,
        DocumentStatus=normalize_document_status(DocumentStatus.ACTIVE.value),
        ExtractedTextLength=len(text),
        ChunkCount=len(chunks),
    )

    try:
        db.add(document)
        db.flush()

        for chunk in chunks:
            db.add(
                KnowledgeChunk(
                    KnowledgeDocumentId=document.KnowledgeDocumentId,
                    ChunkIndex=chunk.index,
                    ChunkText=chunk.text,
                    ChunkHash=sha256_bytes(chunk.text.encode("utf-8")),
                    TokenEstimate=chunk.token_estimate,
                )
            )
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = _get_existing_document_by_sha(db, file_sha256)
        if existing:
            return existing, True
        raise

    db.refresh(document)
    return document, False


def ingest_file_path(
    db: Session,
    path: Path,
    source_type: str = "OTHER",
    capability_status: str | None = None,
    tenant_id: str | None = None,
    title: str | None = None,
) -> tuple[KnowledgeDocument, bool]:
    return ingest_file_bytes(
        db=db,
        content=path.read_bytes(),
        original_file_name=path.name,
        source_type=source_type,
        capability_status=capability_status,
        tenant_id=tenant_id,
        stored_file_path=str(path),
        title=title,
    )


def ingest_folder(
    db: Session,
    folder_path: str,
    source_type: str = "OTHER",
    capability_status: str | None = None,
    tenant_id: str | None = None,
) -> dict[str, int | list[str]]:
    root = Path(folder_path)
    if not root.exists() or not root.is_dir():
        raise IngestionError("folder_path must be an existing directory.")
    try:
        normalized_source_type = normalize_source_type(source_type)
        normalized_capability_status = normalize_capability_status(capability_status)
    except ValueError as exc:
        raise IngestionError(str(exc)) from exc

    ingested = duplicates = skipped = 0
    errors: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".txt", ".docx"}:
            skipped += 1
            continue
        try:
            _, duplicate = ingest_file_path(db, path, normalized_source_type, normalized_capability_status, tenant_id)
            if duplicate:
                duplicates += 1
            else:
                ingested += 1
        except Exception as exc:  # Keep folder ingestion resilient and report per-file failures.
            errors.append(f"{path}: {exc}")
    return {"ingested": ingested, "duplicates": duplicates, "skipped": skipped, "errors": errors}

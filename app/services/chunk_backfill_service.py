from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.enums import DocumentStatus, normalize_capability_status, normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.chunking_service import chunk_text
from app.services.document_extraction_service import extract_text
from app.services.hashing_service import sha256_bytes
from app.services.manifest_ingestion_service import SUPPORTED_MANIFEST_EXTENSIONS, _load_manifest, _resolve_document_path


class ChunkBackfillError(ValueError):
    pass


@dataclass(frozen=True)
class ChunkBackfillResult:
    document_id: str | None
    title: str | None
    old_chunk_count: int
    new_chunk_count: int
    old_missing_source_section_count: int
    new_missing_source_section_count: int
    status: str
    message: str
    file_path: str | None = None

    def model_dump(self) -> dict:
        return asdict(self)


def _missing_source_section_count(db: Session, document_id: str) -> int:
    return int(
        db.scalar(
            select(func.count())
            .select_from(KnowledgeChunk)
            .where(KnowledgeChunk.KnowledgeDocumentId == document_id)
            .where(KnowledgeChunk.SourceSection.is_(None))
        )
        or 0
    )


def _chunk_count(db: Session, document_id: str) -> int:
    return int(
        db.scalar(
            select(func.count())
            .select_from(KnowledgeChunk)
            .where(KnowledgeChunk.KnowledgeDocumentId == document_id)
        )
        or 0
    )


def backfill_document_chunks(
    db: Session,
    document_id: str,
    file_path: str | Path,
    dry_run: bool = False,
    include_superseded: bool = False,
) -> ChunkBackfillResult:
    document = db.get(KnowledgeDocument, document_id)
    if document is None:
        raise ChunkBackfillError(f"KnowledgeDocument not found: {document_id}")

    path = Path(file_path)
    if document.DocumentStatus == DocumentStatus.SUPERSEDED.value and not include_superseded:
        old_missing = _missing_source_section_count(db, document.KnowledgeDocumentId)
        return ChunkBackfillResult(
            document_id=document.KnowledgeDocumentId,
            title=document.Title,
            old_chunk_count=_chunk_count(db, document.KnowledgeDocumentId),
            new_chunk_count=_chunk_count(db, document.KnowledgeDocumentId),
            old_missing_source_section_count=old_missing,
            new_missing_source_section_count=old_missing,
            status="SKIPPED",
            message="Document is SUPERSEDED. Use include_superseded to process it.",
            file_path=str(path),
        )
    if path.suffix.lower() not in SUPPORTED_MANIFEST_EXTENSIONS:
        raise ChunkBackfillError("Only TXT and DOCX files can be backfilled.")
    if not path.exists() or not path.is_file():
        raise ChunkBackfillError(f"Source file not found: {path}")

    old_chunk_count = _chunk_count(db, document.KnowledgeDocumentId)
    old_missing = _missing_source_section_count(db, document.KnowledgeDocumentId)
    content = path.read_bytes()
    text = extract_text(content, path.name)
    from app.core.config import get_settings

    settings = get_settings()
    chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        raise ChunkBackfillError("Re-extracted document did not produce any chunks.")
    new_missing = sum(1 for chunk in chunks if not chunk.source_section)

    if dry_run:
        return ChunkBackfillResult(
            document_id=document.KnowledgeDocumentId,
            title=document.Title,
            old_chunk_count=old_chunk_count,
            new_chunk_count=len(chunks),
            old_missing_source_section_count=old_missing,
            new_missing_source_section_count=new_missing,
            status="DRY_RUN",
            message="Dry run only. Existing chunks were not changed.",
            file_path=str(path),
        )

    try:
        db.execute(delete(KnowledgeChunk).where(KnowledgeChunk.KnowledgeDocumentId == document.KnowledgeDocumentId))
        for chunk in chunks:
            db.add(
                KnowledgeChunk(
                    KnowledgeDocumentId=document.KnowledgeDocumentId,
                    ChunkIndex=chunk.index,
                    ChunkText=chunk.text,
                    ChunkHash=sha256_bytes(chunk.text.encode("utf-8")),
                    SourceSection=chunk.source_section,
                    TokenEstimate=chunk.token_estimate,
                )
            )
        document.ChunkCount = len(chunks)
        document.ExtractedTextLength = len(text)
        document.UpdatedAt = datetime.now(UTC)
        db.add(document)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return ChunkBackfillResult(
        document_id=document.KnowledgeDocumentId,
        title=document.Title,
        old_chunk_count=old_chunk_count,
        new_chunk_count=len(chunks),
        old_missing_source_section_count=old_missing,
        new_missing_source_section_count=_missing_source_section_count(db, document.KnowledgeDocumentId),
        status="BACKFILLED",
        message="Chunks replaced and SourceSection recalculated.",
        file_path=str(path),
    )


def _find_manifest_document(
    db: Session,
    content: bytes,
    title: str | None,
    source_type: str,
) -> KnowledgeDocument | None:
    file_sha256 = sha256_bytes(content)
    document = db.scalar(select(KnowledgeDocument).where(KnowledgeDocument.FileSha256 == file_sha256))
    if document:
        return document
    if title:
        document = db.scalar(
            select(KnowledgeDocument)
            .where(KnowledgeDocument.Title == title)
            .where(KnowledgeDocument.SourceType == source_type)
        )
        if document:
            return document
    return None


def backfill_manifest(
    db: Session,
    manifest_path: str | Path,
    dry_run: bool = False,
    include_superseded: bool = False,
) -> dict[str, Any]:
    resolved_manifest_path = Path(manifest_path).resolve()
    manifest = _load_manifest(resolved_manifest_path)
    documents = manifest.get("documents")
    if not isinstance(documents, list):
        raise ChunkBackfillError("Manifest field 'documents' must be a list.")

    default_source_type = normalize_source_type(manifest.get("default_source_type"))
    default_capability_status = normalize_capability_status(manifest.get("default_capability_status"))

    results: list[dict[str, Any]] = []
    backfilled = dry_runs = skipped = failed = 0
    for index, entry in enumerate(documents):
        if not isinstance(entry, dict):
            failed += 1
            results.append(
                ChunkBackfillResult(
                    document_id=None,
                    title=None,
                    old_chunk_count=0,
                    new_chunk_count=0,
                    old_missing_source_section_count=0,
                    new_missing_source_section_count=0,
                    status="ERROR",
                    message=f"Document entry {index} must be an object.",
                ).model_dump()
            )
            continue

        raw_path = entry.get("path")
        if not raw_path:
            failed += 1
            results.append(
                ChunkBackfillResult(
                    document_id=None,
                    title=entry.get("title"),
                    old_chunk_count=0,
                    new_chunk_count=0,
                    old_missing_source_section_count=0,
                    new_missing_source_section_count=0,
                    status="ERROR",
                    message=f"Document entry {index} must include path.",
                ).model_dump()
            )
            continue

        path = _resolve_document_path(raw_path, resolved_manifest_path)
        try:
            source_type = normalize_source_type(entry.get("source_type", default_source_type))
            normalize_capability_status(entry.get("capability_status", default_capability_status))
            if path.suffix.lower() not in SUPPORTED_MANIFEST_EXTENSIONS:
                skipped += 1
                results.append(
                    ChunkBackfillResult(
                        document_id=None,
                        title=entry.get("title"),
                        old_chunk_count=0,
                        new_chunk_count=0,
                        old_missing_source_section_count=0,
                        new_missing_source_section_count=0,
                        status="SKIPPED",
                        message="Unsupported file type.",
                        file_path=str(path),
                    ).model_dump()
                )
                continue
            if not path.exists() or not path.is_file():
                raise ChunkBackfillError(f"Source file not found: {path}")

            content = path.read_bytes()
            document = _find_manifest_document(db, content=content, title=entry.get("title"), source_type=source_type)
            if document is None:
                raise ChunkBackfillError("No existing KnowledgeDocument matched by FileSha256 or title/source_type.")

            result = backfill_document_chunks(
                db=db,
                document_id=document.KnowledgeDocumentId,
                file_path=path,
                dry_run=dry_run,
                include_superseded=include_superseded,
            )
            if result.status == "BACKFILLED":
                backfilled += 1
            elif result.status == "DRY_RUN":
                dry_runs += 1
            elif result.status == "SKIPPED":
                skipped += 1
            results.append(result.model_dump())
        except Exception as exc:
            db.rollback()
            failed += 1
            results.append(
                ChunkBackfillResult(
                    document_id=None,
                    title=entry.get("title"),
                    old_chunk_count=0,
                    new_chunk_count=0,
                    old_missing_source_section_count=0,
                    new_missing_source_section_count=0,
                    status="ERROR",
                    message=str(exc),
                    file_path=str(path),
                ).model_dump()
            )

    return {
        "total_requested": len(documents),
        "backfilled": backfilled,
        "dry_runs": dry_runs,
        "skipped": skipped,
        "failed": failed,
        "results": results,
    }

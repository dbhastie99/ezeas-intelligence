import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.enums import normalize_capability_status, normalize_source_type
from app.services.ingestion_service import ingest_file_path

SUPPORTED_MANIFEST_EXTENSIONS = {".txt", ".docx"}


class ManifestIngestionError(ValueError):
    pass


def _load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists() or not manifest_path.is_file():
        raise ManifestIngestionError(f"Manifest file not found: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestIngestionError(f"Manifest is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestIngestionError("Manifest root must be a JSON object.")
    return data


def _resolve_document_path(raw_path: str, manifest_path: Path) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate

    manifest_relative = manifest_path.parent / candidate
    if manifest_relative.exists():
        return manifest_relative

    cwd_relative = Path.cwd() / candidate
    if cwd_relative.exists():
        return cwd_relative

    return manifest_relative


def ingest_manifest(db: Session, manifest_path: str | Path) -> dict[str, Any]:
    resolved_manifest_path = Path(manifest_path).resolve()
    manifest = _load_manifest(resolved_manifest_path)

    try:
        default_source_type = normalize_source_type(manifest.get("default_source_type"))
        default_capability_status = normalize_capability_status(manifest.get("default_capability_status"))
    except ValueError as exc:
        raise ManifestIngestionError(str(exc)) from exc
    default_tenant_id = manifest.get("default_tenant_id")
    documents = manifest.get("documents")
    if not isinstance(documents, list):
        raise ManifestIngestionError("Manifest field 'documents' must be a list.")

    results: list[dict[str, Any]] = []
    ingested = duplicates = skipped = error_count = 0

    for index, entry in enumerate(documents):
        if not isinstance(entry, dict):
            raise ManifestIngestionError(f"Document entry {index} must be an object.")

        raw_path = entry.get("path")
        if not raw_path or not isinstance(raw_path, str):
            raise ManifestIngestionError(f"Document entry {index} must include a string path.")

        try:
            source_type = normalize_source_type(entry.get("source_type", default_source_type))
            capability_status = normalize_capability_status(entry.get("capability_status", default_capability_status))
        except ValueError as exc:
            raise ManifestIngestionError(f"Document entry {index}: {exc}") from exc
        tenant_id = entry.get("tenant_id", default_tenant_id)
        title = entry.get("title")
        path = _resolve_document_path(raw_path, resolved_manifest_path)
        base_result = {
            "path": raw_path,
            "resolved_path": str(path),
            "source_type": source_type,
            "capability_status": capability_status,
            "tenant_id": tenant_id,
            "title": title,
        }

        if path.suffix.lower() not in SUPPORTED_MANIFEST_EXTENSIONS:
            skipped += 1
            results.append({**base_result, "status": "SKIPPED", "duplicate": False, "error": "Unsupported file type."})
            continue

        if not path.exists() or not path.is_file():
            error_count += 1
            results.append({**base_result, "status": "ERROR", "duplicate": False, "error": "File not found."})
            continue

        try:
            document, duplicate = ingest_file_path(
                db=db,
                path=path,
                source_type=source_type,
                capability_status=capability_status,
                tenant_id=tenant_id,
                title=title,
            )
        except Exception as exc:
            error_count += 1
            results.append({**base_result, "status": "ERROR", "duplicate": False, "error": str(exc)})
            continue

        if duplicate:
            duplicates += 1
            status = "DUPLICATE"
        else:
            ingested += 1
            status = "INGESTED"

        results.append(
            {
                **base_result,
                "status": status,
                "duplicate": duplicate,
                "document_id": document.KnowledgeDocumentId,
                "chunk_count": document.ChunkCount,
                "file_sha256": document.FileSha256,
                "title": document.Title,
                "error": None,
            }
        )

    return {
        "total_documents_listed": len(documents),
        "ingested": ingested,
        "duplicates": duplicates,
        "skipped": skipped,
        "error_count": error_count,
        "results": results,
    }

import argparse
import os
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def configured_database_url() -> str | None:
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return env_value

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return None

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "MINERVA_DATABASE_URL" and value.strip():
            return value.strip().strip('"').strip("'")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="List Minerva KnowledgeDocument rows.")
    parser.add_argument("--source-type")
    parser.add_argument("--status")
    parser.add_argument("--title-contains")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.document_admin_service import list_documents

    try:
        with SessionLocal() as db:
            documents = list_documents(
                db=db,
                source_type=args.source_type,
                status=args.status,
                title_contains=args.title_contains,
            )
    except (SQLAlchemyError, ValueError) as exc:
        print(f"Document listing failed: {exc}")
        return 1

    for document in documents:
        created = document.CreatedAt.isoformat() if document.CreatedAt else ""
        sha_prefix = document.FileSha256[:12] if document.FileSha256 else ""
        print(
            f"{document.KnowledgeDocumentId} | "
            f"title={document.Title!r} | "
            f"source_type={document.SourceType} | "
            f"capability_status={document.CapabilityStatus} | "
            f"document_status={document.DocumentStatus} | "
            f"tenant_id={document.TenantId} | "
            f"chunks={document.ChunkCount} | "
            f"created={created} | "
            f"sha={sha_prefix}"
        )
    print(f"Total documents: {len(documents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

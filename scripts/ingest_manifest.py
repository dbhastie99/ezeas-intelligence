import argparse
import os
import sys
from pathlib import Path

from sqlalchemy import text
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


def print_summary(summary: dict) -> None:
    print("Manifest ingestion summary")
    print(f"Total listed: {summary['total_documents_listed']}")
    print(f"Ingested: {summary['ingested']}")
    print(f"Duplicates: {summary['duplicates']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Errors: {summary['error_count']}")
    print()

    for result in summary["results"]:
        print(
            f"- {result['status']}: {result['path']} "
            f"duplicate={result['duplicate']} "
            f"source_type={result['source_type']} "
            f"capability_status={result['capability_status']}"
        )
        if result.get("document_id"):
            print(f"  document_id={result['document_id']} chunks={result['chunk_count']} title={result['title']}")
        if result.get("error"):
            print(f"  error={result['error']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a Minerva knowledge corpus manifest.")
    parser.add_argument("manifest_path")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.manifest_ingestion_service import ManifestIngestionError, ingest_manifest

    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
            summary = ingest_manifest(db=db, manifest_path=args.manifest_path)
    except ManifestIngestionError as exc:
        print(f"Manifest validation failed: {exc}")
        return 1
    except SQLAlchemyError as exc:
        print(f"Database connection or ingestion failed: {exc}")
        return 1

    print_summary(summary)
    return 1 if summary["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

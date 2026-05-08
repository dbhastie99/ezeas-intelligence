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
    parser = argparse.ArgumentParser(description="Report Minerva chunk quality statistics.")
    parser.add_argument("--source-type")
    parser.add_argument("--title-contains")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.chunk_quality_service import build_chunk_quality_report

    try:
        with SessionLocal() as db:
            report = build_chunk_quality_report(
                db=db,
                source_type=args.source_type,
                title_contains=args.title_contains,
            )
    except (SQLAlchemyError, ValueError) as exc:
        print(f"Chunk quality report failed: {exc}")
        return 1

    print(f"Total documents: {report.total_documents}")
    print(f"Total chunks: {report.total_chunks}")
    print(f"Average chunk length: {report.average_chunk_length:.1f}")
    print(f"Min chunk length: {report.min_chunk_length}")
    print(f"Max chunk length: {report.max_chunk_length}")
    print(
        f"Chunks missing SourceSection: {report.chunks_missing_source_section} "
        f"({report.missing_source_section_percent:.1f}%)"
    )
    print("Source types:")
    for source_type, count in sorted(report.source_types_summary.items()):
        print(f"  {source_type}: {count}")
    print("Largest documents by chunk count:")
    for document in report.largest_documents_by_chunk_count:
        print(f"  {document['chunk_count']:>4} | {document['source_type']} | {document['title']} | {document['document_id']}")
    print("Top documents by missing SourceSection:")
    for document in report.missing_source_section_by_document:
        print(
            f"  {document['missing_source_section_count']:>4} missing | "
            f"{document['chunk_count']:>4} chunks | {document['source_type']} | {document['title']} | {document['document_id']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

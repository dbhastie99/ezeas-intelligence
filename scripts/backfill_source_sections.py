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


def print_result(result: dict) -> None:
    print(
        f"{result['status']}: document_id={result['document_id']} title={result['title']!r} "
        f"old_chunks={result['old_chunk_count']} new_chunks={result['new_chunk_count']} "
        f"missing={result['old_missing_source_section_count']}->{result['new_missing_source_section_count']}"
    )
    print(f"  file={result.get('file_path')}")
    print(f"  message={result['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill KnowledgeChunk.SourceSection from original TXT/DOCX files.")
    parser.add_argument("--manifest")
    parser.add_argument("--document-id")
    parser.add_argument("--file-path")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--include-superseded", action="store_true")
    args = parser.parse_args()

    if not args.manifest and not (args.document_id and args.file_path):
        print("Provide --manifest or both --document-id and --file-path.")
        return 2
    if args.manifest and (args.document_id or args.file_path):
        print("Use either --manifest or --document-id/--file-path, not both.")
        return 2
    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.chunk_backfill_service import ChunkBackfillError, backfill_document_chunks, backfill_manifest

    try:
        with SessionLocal() as db:
            if args.manifest:
                summary = backfill_manifest(
                    db=db,
                    manifest_path=args.manifest,
                    dry_run=args.dry_run,
                    include_superseded=args.include_superseded,
                )
                print(
                    f"Requested={summary['total_requested']} Backfilled={summary['backfilled']} "
                    f"DryRuns={summary['dry_runs']} Skipped={summary['skipped']} Failed={summary['failed']}"
                )
                for result in summary["results"]:
                    print_result(result)
                if summary["backfilled"] > 0 or summary["dry_runs"] > 0:
                    return 0
                return 1 if summary["failed"] else 0

            result = backfill_document_chunks(
                db=db,
                document_id=args.document_id,
                file_path=args.file_path,
                dry_run=args.dry_run,
                include_superseded=args.include_superseded,
            )
            print_result(result.model_dump())
            return 0 if result.status in {"BACKFILLED", "DRY_RUN", "SKIPPED"} else 1
    except (SQLAlchemyError, ChunkBackfillError, ValueError) as exc:
        print(f"SourceSection backfill failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

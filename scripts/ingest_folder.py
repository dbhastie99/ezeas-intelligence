import argparse

from app.db.session import SessionLocal
from app.services.ingestion_service import ingest_folder


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest TXT/DOCX knowledge files into Minerva.")
    parser.add_argument("folder_path")
    parser.add_argument("--source-type", default="OTHER")
    parser.add_argument("--capability-status", default=None)
    parser.add_argument("--tenant-id", default=None)
    args = parser.parse_args()

    with SessionLocal() as db:
        result = ingest_folder(
            db=db,
            folder_path=args.folder_path,
            source_type=args.source_type,
            capability_status=args.capability_status,
            tenant_id=args.tenant_id,
        )
    print(result)


if __name__ == "__main__":
    main()

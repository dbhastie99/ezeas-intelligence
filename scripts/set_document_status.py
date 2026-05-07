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
    parser = argparse.ArgumentParser(description="Set a Minerva KnowledgeDocument status.")
    parser.add_argument("document_id")
    parser.add_argument("status")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.document_admin_service import set_document_status

    try:
        with SessionLocal() as db:
            document, previous_status, new_status = set_document_status(db, args.document_id, args.status)
    except (SQLAlchemyError, ValueError) as exc:
        print(f"Document status update failed: {exc}")
        return 1

    print(f"Document: {document.KnowledgeDocumentId}")
    print(f"Title: {document.Title}")
    print(f"Status: {previous_status} -> {new_status}")
    print("Chunks were not deleted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

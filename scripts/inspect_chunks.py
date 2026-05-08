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
    parser = argparse.ArgumentParser(description="Inspect Minerva knowledge chunks.")
    parser.add_argument("--document-id")
    parser.add_argument("--title-contains")
    parser.add_argument("--source-type")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.chunk_inspection_service import inspect_chunks

    try:
        with SessionLocal() as db:
            chunks = inspect_chunks(
                db=db,
                document_id=args.document_id,
                title_contains=args.title_contains,
                source_type=args.source_type,
                start_index=args.start_index,
                limit=args.limit,
            )
    except (SQLAlchemyError, ValueError) as exc:
        print(f"Chunk inspection failed: {exc}")
        return 1

    for chunk in chunks:
        document = chunk.document
        preview = " ".join((chunk.ChunkText or "").split())[:400]
        hash_prefix = chunk.ChunkHash[:12] if chunk.ChunkHash else ""
        print(f"Document: {document.Title} ({document.KnowledgeDocumentId})")
        print(
            f"  source_type={document.SourceType} capability_status={document.CapabilityStatus} "
            f"document_status={document.DocumentStatus}"
        )
        print(
            f"  chunk_index={chunk.ChunkIndex} chunk_id={chunk.KnowledgeChunkId} "
            f"token_estimate={chunk.TokenEstimate} source_section={chunk.SourceSection} hash={hash_prefix}"
        )
        print(f"  text={preview}")
        print()
    print(f"Chunks shown: {len(chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

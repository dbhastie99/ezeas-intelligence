import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EXPECTED_TABLES = [
    "KnowledgeDocument",
    "KnowledgeChunk",
    "KnowledgeChatSession",
    "KnowledgeChatMessage",
    "AIInteractionAudit",
]


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
    database_url = configured_database_url()
    if not database_url:
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            existing_tables = set(
                connection.execute(
                    text(
                        """
                        SELECT TABLE_NAME
                        FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_SCHEMA = 'dbo'
                          AND TABLE_TYPE = 'BASE TABLE'
                        """
                    )
                ).scalars()
            )

            missing = [table_name for table_name in EXPECTED_TABLES if table_name not in existing_tables]
            if missing:
                print(f"Missing expected tables: {', '.join(missing)}")
                return 1

            print("All expected Minerva tables exist.")
            for table_name in EXPECTED_TABLES:
                row_count = connection.execute(text(f"SELECT COUNT_BIG(*) FROM dbo.{table_name}")).scalar_one()
                print(f"{table_name}: {row_count}")
    except SQLAlchemyError as exc:
        print(f"SQL Server verification failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
import os
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument


READY = "READY"
MISSING_CONFIGURATION = "MISSING_CONFIGURATION"
DATABASE_CONNECTION_FAILED = "DATABASE_CONNECTION_FAILED"
REQUIRED_TABLES_MISSING = "REQUIRED_TABLES_MISSING"
UNKNOWN_ERROR = "UNKNOWN_ERROR"

REQUIRED_KNOWLEDGE_TABLES = (
    KnowledgeDocument.__tablename__,
    KnowledgeChunk.__tablename__,
)

GUARDRAILS = (
    "read-only",
    "does not mutate corpus",
    "does not create databases",
    "does not create tables",
    "does not run migrations",
    "does not ingest documents",
    "does not ingest operational JSON",
    "does not connect Code Evidence to answers",
    "does not call a live LLM",
    "does not write chat messages or audit rows",
)


@dataclass(frozen=True)
class WorkerStoryBaselineDbReadinessResult:
    status: str
    is_ready: bool
    checked_at_utc: str
    required_tables_checked: list[str]
    missing_tables: list[str]
    error_summary: str | None
    guardrails: list[str]
    recommended_next_action: str

    def to_dict(self) -> dict:
        return {
            "Status": self.status,
            "IsReady": self.is_ready,
            "CheckedAtUtc": self.checked_at_utc,
            "RequiredTablesChecked": self.required_tables_checked,
            "MissingTables": self.missing_tables,
            "ErrorSummary": self.error_summary,
            "Guardrails": self.guardrails,
            "RecommendedNextAction": self.recommended_next_action,
        }


def configured_database_url(project_root: Path | None = None) -> str | None:
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return env_value

    root = project_root or Path(__file__).resolve().parents[2]
    env_file = root / ".env"
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


def _result(
    status: str,
    missing_tables: list[str] | None = None,
    error_summary: str | None = None,
) -> WorkerStoryBaselineDbReadinessResult:
    ready = status == READY
    next_actions = {
        READY: "Run the Worker Story benchmark, corpus coverage diagnostic and answer gap report commands.",
        MISSING_CONFIGURATION: "Configure MINERVA_DATABASE_URL for the intended ezeas-intelligence knowledge database.",
        DATABASE_CONNECTION_FAILED: "Fix SQL Server connectivity or credentials before retrying Worker Story baseline capture.",
        REQUIRED_TABLES_MISSING: "Verify the configured database is the migrated Minerva knowledge store before retrying.",
        UNKNOWN_ERROR: "Inspect the readiness error and rerun the read-only readiness check.",
    }
    return WorkerStoryBaselineDbReadinessResult(
        status=status,
        is_ready=ready,
        checked_at_utc=datetime.now(UTC).isoformat(),
        required_tables_checked=list(REQUIRED_KNOWLEDGE_TABLES),
        missing_tables=missing_tables or [],
        error_summary=error_summary,
        guardrails=list(GUARDRAILS),
        recommended_next_action=next_actions[status],
    )


def check_worker_story_baseline_db_readiness(
    database_url: str | None = None,
    database_url_provider: Callable[[], str | None] = configured_database_url,
    engine_factory: Callable[..., object] = create_engine,
) -> WorkerStoryBaselineDbReadinessResult:
    resolved_database_url = database_url if database_url is not None else database_url_provider()
    if not resolved_database_url:
        return _result(
            MISSING_CONFIGURATION,
            error_summary="MINERVA_DATABASE_URL was not found in the environment or .env file.",
        )

    try:
        engine = engine_factory(resolved_database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            inspector = inspect(connection)
            missing_tables = [
                table_name for table_name in REQUIRED_KNOWLEDGE_TABLES if not inspector.has_table(table_name)
            ]
    except SQLAlchemyError as exc:
        return _result(DATABASE_CONNECTION_FAILED, error_summary=str(exc).splitlines()[0])
    except Exception as exc:
        return _result(UNKNOWN_ERROR, error_summary=str(exc).splitlines()[0])

    if missing_tables:
        return _result(REQUIRED_TABLES_MISSING, missing_tables=missing_tables)

    return _result(READY)

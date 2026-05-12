from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
import os
from pathlib import Path
import re
from urllib.parse import unquote_plus

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import make_url

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
class DatabaseConfiguration:
    url: str | None
    source: str
    checked_sources: list[str]


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
    diagnostics: dict = field(default_factory=dict)

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
            "Diagnostics": self.diagnostics,
        }


def resolve_database_configuration(project_root: Path | None = None) -> DatabaseConfiguration:
    checked_sources = ["environment:MINERVA_DATABASE_URL"]
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return DatabaseConfiguration(
            url=env_value,
            source="environment:MINERVA_DATABASE_URL",
            checked_sources=checked_sources,
        )

    root = project_root or Path(__file__).resolve().parents[2]
    env_file = root / ".env"
    checked_sources.append(".env:MINERVA_DATABASE_URL")
    if not env_file.exists():
        return DatabaseConfiguration(url=None, source="not_configured", checked_sources=checked_sources)

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "MINERVA_DATABASE_URL" and value.strip():
            return DatabaseConfiguration(
                url=value.strip().strip('"').strip("'"),
                source=".env:MINERVA_DATABASE_URL",
                checked_sources=checked_sources,
            )
    return DatabaseConfiguration(url=None, source="not_configured", checked_sources=checked_sources)


def configured_database_url(project_root: Path | None = None) -> str | None:
    return resolve_database_configuration(project_root=project_root).url


def _split_odbc_connect(odbc_connect: str) -> dict[str, str]:
    settings = {}
    for item in unquote_plus(odbc_connect).split(";"):
        if not item or "=" not in item:
            continue
        key, value = item.split("=", 1)
        settings[key.strip().lower()] = value.strip()
    return settings


def _available_odbc_drivers() -> list[str] | None:
    try:
        import pyodbc
    except Exception:
        return None

    try:
        return list(pyodbc.drivers())
    except Exception:
        return None


def _redact_identifier(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 4:
        return "***"
    return f"{value[:2]}...{value[-2:]} ({len(value)} chars)"


def _connection_target_diagnostics(database_url: str | None) -> dict:
    if not database_url:
        return {
            "Dialect": None,
            "Driver": None,
            "SelectedOdbcDriver": None,
            "SelectedOdbcDriverAvailable": None,
            "OdbcInspection": "not_available_without_configuration",
            "Server": None,
            "Database": None,
            "Dsn": None,
        }

    diagnostics = {
        "Dialect": None,
        "Driver": None,
        "SelectedOdbcDriver": None,
        "SelectedOdbcDriverAvailable": None,
        "OdbcInspection": "not_applicable",
        "Server": None,
        "Database": None,
        "Dsn": None,
    }

    try:
        url = make_url(database_url)
    except Exception:
        diagnostics["ParseWarning"] = "database URL could not be parsed for redacted diagnostics"
        return diagnostics

    diagnostics["Dialect"] = url.get_backend_name()
    diagnostics["Driver"] = url.get_driver_name()
    diagnostics["Database"] = _redact_identifier(url.database)
    diagnostics["Server"] = _redact_identifier(url.host)

    odbc_connect = url.query.get("odbc_connect")
    if odbc_connect:
        odbc_settings = _split_odbc_connect(odbc_connect)
        selected_driver = odbc_settings.get("driver")
        diagnostics["SelectedOdbcDriver"] = selected_driver.strip("{}") if selected_driver else None
        diagnostics["Server"] = _redact_identifier(odbc_settings.get("server"))
        diagnostics["Database"] = _redact_identifier(odbc_settings.get("database"))
        diagnostics["Dsn"] = _redact_identifier(odbc_settings.get("dsn"))
    elif url.query.get("driver"):
        diagnostics["SelectedOdbcDriver"] = url.query["driver"]

    if diagnostics["Driver"] == "pyodbc" or diagnostics["SelectedOdbcDriver"] or diagnostics["Dsn"]:
        available_drivers = _available_odbc_drivers()
        diagnostics["OdbcInspection"] = "pyodbc_unavailable" if available_drivers is None else "pyodbc_available"
        if available_drivers is not None:
            diagnostics["InstalledSqlServerOdbcDrivers"] = [
                driver for driver in available_drivers if "SQL Server" in driver
            ]
        if diagnostics["SelectedOdbcDriver"] and available_drivers is not None:
            diagnostics["SelectedOdbcDriverAvailable"] = diagnostics["SelectedOdbcDriver"] in available_drivers

    return diagnostics


def _diagnostics(configuration: DatabaseConfiguration, database_url: str | None) -> dict:
    return {
        "ConfigurationPresent": bool(database_url),
        "ConfigurationSource": configuration.source,
        "CheckedConfigurationSources": configuration.checked_sources,
        "ConnectionStringRedacted": "configured; value intentionally not printed" if database_url else None,
        "Target": _connection_target_diagnostics(database_url),
        "OperatorNextStep": (
            "Confirm the active MINERVA_DATABASE_URL source, SQL Server instance or DSN, database name, "
            "ODBC driver, credentials and network access, then rerun the read-only readiness check before "
            "running benchmark, corpus coverage or answer gap commands."
        ),
    }


def _safe_error_summary(exc: Exception, database_url: str | None) -> str:
    summary = str(exc).splitlines()[0]
    if database_url:
        summary = summary.replace(database_url, "[REDACTED_DATABASE_URL]")
        try:
            url = make_url(database_url)
        except Exception:
            url = None
        if url is not None:
            for value in (url.password,):
                if value:
                    summary = summary.replace(value, "[REDACTED]")
            for key, value in url.query.items():
                if any(secret_word in key.lower() for secret_word in ("password", "pwd", "secret", "token")):
                    summary = summary.replace(str(value), "[REDACTED]")

    summary = re.sub(r"(?i)(password|pwd|secret|token)=([^;&\\s]+)", r"\1=[REDACTED]", summary)
    return summary


def _result(
    status: str,
    missing_tables: list[str] | None = None,
    error_summary: str | None = None,
    diagnostics: dict | None = None,
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
        diagnostics=diagnostics or {},
    )


def check_worker_story_baseline_db_readiness(
    database_url: str | None = None,
    database_url_provider: Callable[[], str | None] = configured_database_url,
    engine_factory: Callable[..., object] = create_engine,
) -> WorkerStoryBaselineDbReadinessResult:
    if database_url is not None:
        configuration = DatabaseConfiguration(
            url=database_url,
            source="argument:database_url",
            checked_sources=["argument:database_url"],
        )
    elif database_url_provider is configured_database_url:
        configuration = resolve_database_configuration()
    else:
        configuration = DatabaseConfiguration(
            url=database_url_provider(),
            source="database_url_provider",
            checked_sources=["database_url_provider"],
        )

    resolved_database_url = configuration.url
    diagnostics = _diagnostics(configuration, resolved_database_url)
    if not resolved_database_url:
        return _result(
            MISSING_CONFIGURATION,
            error_summary="MINERVA_DATABASE_URL was not found in the environment or .env file.",
            diagnostics=diagnostics,
        )

    try:
        engine = engine_factory(resolved_database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            inspector = inspect(connection)
            missing_tables = [
                table_name for table_name in REQUIRED_KNOWLEDGE_TABLES if not inspector.has_table(table_name)
            ]
    except SQLAlchemyError as exc:
        return _result(
            DATABASE_CONNECTION_FAILED,
            error_summary=_safe_error_summary(exc, resolved_database_url),
            diagnostics=diagnostics,
        )
    except Exception as exc:
        return _result(UNKNOWN_ERROR, error_summary=_safe_error_summary(exc, resolved_database_url), diagnostics=diagnostics)

    if missing_tables:
        return _result(REQUIRED_TABLES_MISSING, missing_tables=missing_tables, diagnostics=diagnostics)

    return _result(READY, diagnostics=diagnostics)

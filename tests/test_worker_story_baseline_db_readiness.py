import json
from pathlib import Path

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.services import worker_story_baseline_db_readiness_service as readiness
from scripts import check_worker_story_baseline_db_readiness as readiness_script


class FakeConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class FakeEngine:
    def __init__(self, connect_error: Exception | None = None):
        self.connect_error = connect_error

    def connect(self):
        if self.connect_error:
            raise self.connect_error
        return FakeConnection()


class FakeInspector:
    def __init__(self, existing_tables: set[str]):
        self.existing_tables = existing_tables
        self.checked_tables = []

    def has_table(self, table_name: str) -> bool:
        self.checked_tables.append(table_name)
        return table_name in self.existing_tables


def _engine_factory(engine: FakeEngine):
    def factory(*args, **kwargs):
        return engine

    return factory


def _to_dict_status(result):
    data = result.to_dict()
    assert data["Guardrails"]
    assert data["RecommendedNextAction"]
    return data


def test_worker_story_baseline_db_readiness_missing_configuration():
    result = readiness.check_worker_story_baseline_db_readiness(database_url_provider=lambda: None)
    data = _to_dict_status(result)

    assert data["Status"] == readiness.MISSING_CONFIGURATION
    assert data["IsReady"] is False
    assert data["RequiredTablesChecked"] == ["KnowledgeDocument", "KnowledgeChunk"]
    assert "MINERVA_DATABASE_URL" in data["ErrorSummary"]
    assert data["Diagnostics"]["ConfigurationPresent"] is False
    assert data["Diagnostics"]["ConfigurationSource"] == "database_url_provider"
    assert data["Diagnostics"]["AcceptedConfigurationVariables"] == ["MINERVA_DATABASE_URL"]


def test_worker_story_baseline_db_readiness_database_connection_failed():
    result = readiness.check_worker_story_baseline_db_readiness(
        database_url="mssql+pyodbc://example",
        engine_factory=_engine_factory(FakeEngine(connect_error=SQLAlchemyError("connection failed"))),
    )
    data = _to_dict_status(result)

    assert data["Status"] == readiness.DATABASE_CONNECTION_FAILED
    assert data["IsReady"] is False
    assert "connection failed" in data["ErrorSummary"]
    assert data["Diagnostics"]["ConfigurationPresent"] is True
    assert data["Diagnostics"]["ConfigurationSource"] == "argument:database_url"
    assert data["Diagnostics"]["AcceptedConfigurationVariables"] == ["MINERVA_DATABASE_URL"]


def test_worker_story_baseline_db_readiness_diagnostics_redact_connection_secrets():
    secret_url = (
        "mssql+pyodbc://user:super-secret-password@sql.example.local/ezeas-intelligence-db"
        "?token=private-token&driver=ODBC+Driver+18+for+SQL+Server"
    )
    result = readiness.check_worker_story_baseline_db_readiness(
        database_url=secret_url,
        engine_factory=_engine_factory(
            FakeEngine(connect_error=SQLAlchemyError(f"login failed for {secret_url} token=private-token"))
        ),
    )
    data = result.to_dict()
    serialized = json.dumps(data)

    assert data["Status"] == readiness.DATABASE_CONNECTION_FAILED
    assert "super-secret-password" not in serialized
    assert "private-token" not in serialized
    assert "sql.example.local" not in serialized
    assert "ezeas-intelligence-db" not in serialized
    assert data["Diagnostics"]["ConnectionStringRedacted"] == "configured; value intentionally not printed"
    assert data["Diagnostics"]["Target"]["Server"].startswith("sq...")
    assert data["Diagnostics"]["Target"]["Database"].startswith("ez...")


def test_worker_story_baseline_db_readiness_reports_odbc_driver_availability(monkeypatch):
    monkeypatch.setattr(
        readiness,
        "_available_odbc_drivers",
        lambda: ["ODBC Driver 17 for SQL Server", "ODBC Driver 18 for SQL Server"],
    )
    result = readiness.check_worker_story_baseline_db_readiness(
        database_url=(
            "mssql+pyodbc:///?odbc_connect=Driver%3D%7BODBC+Driver+18+for+SQL+Server%7D%3B"
            "Server%3Dlocalhost%3BDatabase%3Dezeas-intelligence-db%3BTrusted_Connection%3Dyes%3B"
        ),
        engine_factory=_engine_factory(FakeEngine(connect_error=SQLAlchemyError("connection failed"))),
    )
    target = result.to_dict()["Diagnostics"]["Target"]

    assert target["OdbcInspection"] == "pyodbc_available"
    assert target["SelectedOdbcDriver"] == "ODBC Driver 18 for SQL Server"
    assert target["SelectedOdbcDriverAvailable"] is True
    assert target["InstalledSqlServerOdbcDrivers"] == [
        "ODBC Driver 17 for SQL Server",
        "ODBC Driver 18 for SQL Server",
    ]


def test_worker_story_baseline_db_readiness_required_tables_missing(monkeypatch):
    inspector = FakeInspector(existing_tables={"KnowledgeDocument"})
    monkeypatch.setattr(
        readiness,
        "inspect",
        lambda connection: inspector,
    )

    result = readiness.check_worker_story_baseline_db_readiness(
        database_url="mssql+pyodbc://example",
        engine_factory=_engine_factory(FakeEngine()),
    )
    data = _to_dict_status(result)

    assert data["Status"] == readiness.REQUIRED_TABLES_MISSING
    assert data["IsReady"] is False
    assert data["MissingTables"] == ["KnowledgeChunk"]
    assert inspector.checked_tables == ["KnowledgeDocument", "KnowledgeChunk"]


def test_worker_story_baseline_db_readiness_ready(monkeypatch):
    monkeypatch.setattr(
        readiness,
        "inspect",
        lambda connection: FakeInspector(existing_tables={"KnowledgeDocument", "KnowledgeChunk"}),
    )

    result = readiness.check_worker_story_baseline_db_readiness(
        database_url="mssql+pyodbc://example",
        engine_factory=_engine_factory(FakeEngine()),
    )
    data = _to_dict_status(result)

    assert data["Status"] == readiness.READY
    assert data["IsReady"] is True
    assert data["MissingTables"] == []
    assert "Run the Worker Story benchmark" in data["RecommendedNextAction"]


def test_worker_story_baseline_db_readiness_guardrails_are_read_only():
    result = readiness.check_worker_story_baseline_db_readiness(database_url_provider=lambda: None)
    guardrails = result.to_dict()["Guardrails"]

    for expected in (
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
    ):
        assert expected in guardrails


def test_worker_story_baseline_db_readiness_required_tables_constant_remains_knowledge_only():
    assert readiness.REQUIRED_KNOWLEDGE_TABLES == ("KnowledgeDocument", "KnowledgeChunk")


def test_worker_story_baseline_db_readiness_script_json_output(capsys):
    result = readiness.WorkerStoryBaselineDbReadinessResult(
        status=readiness.READY,
        is_ready=True,
        checked_at_utc="2026-05-12T00:00:00+00:00",
        required_tables_checked=["KnowledgeDocument", "KnowledgeChunk"],
        missing_tables=[],
        error_summary=None,
        guardrails=list(readiness.GUARDRAILS),
        recommended_next_action="Run baseline capture.",
    )

    exit_code = readiness_script.main(["--json"], readiness_checker=lambda: result)
    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert exit_code == 0
    assert data["Status"] == readiness.READY
    assert data["IsReady"] is True


def test_worker_story_baseline_db_readiness_script_non_ready_exits_nonzero(capsys):
    result = readiness.WorkerStoryBaselineDbReadinessResult(
        status=readiness.DATABASE_CONNECTION_FAILED,
        is_ready=False,
        checked_at_utc="2026-05-12T00:00:00+00:00",
        required_tables_checked=["KnowledgeDocument", "KnowledgeChunk"],
        missing_tables=[],
        error_summary="connection failed",
        guardrails=list(readiness.GUARDRAILS),
        recommended_next_action="Fix connectivity.",
        diagnostics={"AcceptedConfigurationVariables": ["MINERVA_DATABASE_URL"]},
    )

    exit_code = readiness_script.main([], readiness_checker=lambda: result)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Worker Story baseline DB readiness: DATABASE_CONNECTION_FAILED" in captured.out
    assert "Ready: no" in captured.out
    assert "Diagnostics:" in captured.out
    assert "Accepted configuration variables: MINERVA_DATABASE_URL" in captured.out
    assert "Operator next step:" in captured.out


def test_worker_story_baseline_db_readiness_documentation_and_baseline_notes():
    doc_path = Path("docs/evaluation/worker_story_baselines/WORKER_STORY_BASELINE_DB_READINESS.md")
    summary_path = Path("docs/evaluation/worker_story_baselines/worker_story/v0_1/BASELINE_SUMMARY.md")
    notes_path = Path("docs/evaluation/worker_story_baselines/worker_story/v0_1/REVIEW_NOTES.md")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert doc_path.exists()
    doc = doc_path.read_text(encoding="utf-8")
    summary = summary_path.read_text(encoding="utf-8")
    notes = notes_path.read_text(encoding="utf-8")

    assert "py scripts/check_worker_story_baseline_db_readiness.py" in doc
    assert "does not mutate corpus" in doc
    assert "does not create tables" in doc
    assert "does not run migrations" in doc
    assert "KnowledgeDocument" in doc
    assert "KnowledgeChunk" in doc
    assert "Accepted configuration variable" in doc
    assert "Troubleshooting `DATABASE_CONNECTION_FAILED`" in doc
    assert "Do not treat `DATABASE_CONNECTION_FAILED` as a corpus coverage gap" in doc
    assert "WORKER_STORY_BASELINE_DB_READINESS.md" in summary
    assert "check_worker_story_baseline_db_readiness.py" in notes
    assert "WORKER_STORY_BASELINE_DB_READINESS.md" in readme

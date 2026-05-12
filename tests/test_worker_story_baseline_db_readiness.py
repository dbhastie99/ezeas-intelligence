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

    def has_table(self, table_name: str) -> bool:
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


def test_worker_story_baseline_db_readiness_database_connection_failed():
    result = readiness.check_worker_story_baseline_db_readiness(
        database_url="mssql+pyodbc://example",
        engine_factory=_engine_factory(FakeEngine(connect_error=SQLAlchemyError("connection failed"))),
    )
    data = _to_dict_status(result)

    assert data["Status"] == readiness.DATABASE_CONNECTION_FAILED
    assert data["IsReady"] is False
    assert "connection failed" in data["ErrorSummary"]


def test_worker_story_baseline_db_readiness_required_tables_missing(monkeypatch):
    monkeypatch.setattr(
        readiness,
        "inspect",
        lambda connection: FakeInspector(existing_tables={"KnowledgeDocument"}),
    )

    result = readiness.check_worker_story_baseline_db_readiness(
        database_url="mssql+pyodbc://example",
        engine_factory=_engine_factory(FakeEngine()),
    )
    data = _to_dict_status(result)

    assert data["Status"] == readiness.REQUIRED_TABLES_MISSING
    assert data["IsReady"] is False
    assert data["MissingTables"] == ["KnowledgeChunk"]


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
    )

    exit_code = readiness_script.main([], readiness_checker=lambda: result)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Worker Story baseline DB readiness: DATABASE_CONNECTION_FAILED" in captured.out
    assert "Ready: no" in captured.out


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
    assert "WORKER_STORY_BASELINE_DB_READINESS.md" in summary
    assert "check_worker_story_baseline_db_readiness.py" in notes
    assert "WORKER_STORY_BASELINE_DB_READINESS.md" in readme

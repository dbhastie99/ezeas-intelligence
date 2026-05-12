import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.public_holidays_corpus_coverage_service import scan_public_holidays_corpus_coverage
from scripts import scan_public_holidays_corpus_coverage as scan_public_holidays_script


EXPECTED_GROUPS = {
    "public_holiday_source_and_calendar",
    "worksite_state_and_applicability_context",
    "payroll_treatment_and_decision_story",
    "leave_interaction_and_deducts_on_public_holiday",
    "worker_story_admin_queue_and_finalisation",
    "minerva_boundaries_and_non_mutation_guardrails",
}


def _ingest(db_session, text: str, title: str):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=f"{title.lower().replace(' ', '-')}.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def test_public_holidays_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar",
    )

    report = scan_public_holidays_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PUBLIC_HOLIDAYS"
    assert report["domain"] == "Public Holidays"
    assert report["total_evidence_groups"] == 6
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == EXPECTED_GROUPS
    first_group = report["groups"][0]
    assert {
        "group_key",
        "group_label",
        "search_terms_used",
        "matched_chunk_count",
        "matched_document_count",
        "matched_sources",
        "representative_matched_terms",
        "coverage_status",
        "diagnostic_notes",
    }.issubset(first_group)


def test_public_holidays_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar A",
    )
    _ingest(
        db_session,
        "Public Holiday Group, public holiday override and governed reference configuration evidence support PublicHoliday source data.",
        "Developer Log - Public Holidays Calendar B",
    )
    _ingest(
        db_session,
        "Public holiday applicability depends on Worksite and state context.",
        "Developer Log - Public Holidays Worksite",
    )
    _ingest(
        db_session,
        "Public holiday payroll treatment uses Decision Story evidence.",
        "Developer Log - Public Holidays Payroll",
    )

    report = scan_public_holidays_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["public_holiday_source_and_calendar"]["coverage_status"] == "STRONG"
    assert groups["payroll_treatment_and_decision_story"]["coverage_status"] == "WEAK"
    assert groups["leave_interaction_and_deducts_on_public_holiday"]["coverage_status"] == "MISSING"
    assert groups["public_holiday_source_and_calendar"]["matched_sources"]
    assert groups["public_holiday_source_and_calendar"]["representative_matched_terms"]
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_public_holidays_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar",
    )
    monkeypatch.setattr(sys, "argv", ["scan_public_holidays_corpus_coverage.py", "--json"])

    exit_code = scan_public_holidays_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PUBLIC_HOLIDAYS"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_public_holidays_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "public-holidays-coverage.json"
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_public_holidays_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_public_holidays_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Public Holidays corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out
    assert report["plan_id"] == "PUBLIC_HOLIDAYS"


def test_public_holidays_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar",
    )
    monkeypatch.setattr(sys, "argv", ["scan_public_holidays_corpus_coverage.py"])

    exit_code = scan_public_holidays_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out


def test_public_holidays_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "PublicHoliday and PublicHolidayGroup provide public holiday calendar and observed day evidence.",
        "Developer Log - Public Holidays Calendar",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_public_holidays_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_public_holidays_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_public_holidays_corpus_coverage.py" in readme
    assert "build_public_holidays_answer_gap_report.py" in readme
    assert "Public Holidays diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
    assert "do not prove runtime operational truth" in readme
    assert "do not calculate public holiday entitlements" in readme
    assert "do not decide payroll treatment" in readme

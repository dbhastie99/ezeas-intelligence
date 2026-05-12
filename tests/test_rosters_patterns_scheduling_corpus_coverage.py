import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.rosters_patterns_scheduling_corpus_coverage_service import (
    scan_rosters_patterns_scheduling_corpus_coverage,
)
from scripts import scan_rosters_patterns_scheduling_corpus_coverage as scan_rosters_script


EXPECTED_GROUPS = {
    "roster_pattern_source_and_configuration",
    "appointment_worksite_and_applicability_context",
    "ordinary_hours_leave_basis_and_public_holiday_context",
    "payroll_interpretation_and_worker_story_relationship",
    "admin_queue_finalisation_and_readiness_relationship",
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


def test_rosters_patterns_scheduling_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source",
    )

    report = scan_rosters_patterns_scheduling_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "ROSTERS_PATTERNS_SCHEDULING"
    assert report["domain"] == "Rosters / Patterns / Scheduling"
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


def test_rosters_patterns_scheduling_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source A",
    )
    _ingest(
        db_session,
        "Roster, Pattern Day and Employee Appointment Pattern are governed configuration evidence for expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source B",
    )
    _ingest(
        db_session,
        "Roster assignment context depends on EmployeeAppointment and Worksite.",
        "Developer Log - Rosters Patterns Scheduling Appointment",
    )
    _ingest(
        db_session,
        "Scheduling context can support payroll interpretation and Worker Story evidence.",
        "Developer Log - Rosters Patterns Scheduling Payroll",
    )

    report = scan_rosters_patterns_scheduling_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["roster_pattern_source_and_configuration"]["coverage_status"] == "STRONG"
    assert groups["payroll_interpretation_and_worker_story_relationship"]["coverage_status"] == "WEAK"
    assert groups["ordinary_hours_leave_basis_and_public_holiday_context"]["coverage_status"] == "MISSING"
    assert groups["roster_pattern_source_and_configuration"]["matched_sources"]
    assert groups["roster_pattern_source_and_configuration"]["representative_matched_terms"]
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_rosters_patterns_scheduling_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source",
    )
    monkeypatch.setattr(sys, "argv", ["scan_rosters_patterns_scheduling_corpus_coverage.py", "--json"])

    exit_code = scan_rosters_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "ROSTERS_PATTERNS_SCHEDULING"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_rosters_patterns_scheduling_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "rosters-patterns-scheduling-coverage.json"
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_rosters_patterns_scheduling_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_rosters_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Rosters / Patterns / Scheduling corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out
    assert report["plan_id"] == "ROSTERS_PATTERNS_SCHEDULING"


def test_rosters_patterns_scheduling_corpus_coverage_human_output_is_diagnostic_only(
    db_session,
    monkeypatch,
    capsys,
):
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source",
    )
    monkeypatch.setattr(sys, "argv", ["scan_rosters_patterns_scheduling_corpus_coverage.py"])

    exit_code = scan_rosters_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out


def test_rosters_patterns_scheduling_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Pattern, PatternDay and EmployeeAppointmentPattern provide roster schedule configuration and expected work context.",
        "Developer Log - Rosters Patterns Scheduling Source",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_rosters_patterns_scheduling_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_rosters_patterns_scheduling_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_rosters_patterns_scheduling_corpus_coverage.py" in readme
    assert "build_rosters_patterns_scheduling_answer_gap_report.py" in readme
    assert "Rosters / Patterns / Scheduling diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
    assert "do not prove runtime operational truth" in readme
    assert "do not create rosters" in readme
    assert "do not change worker schedules" in readme
    assert "do not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth" in readme

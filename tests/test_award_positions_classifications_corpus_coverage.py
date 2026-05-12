import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.award_positions_classifications_corpus_coverage_service import (
    scan_award_positions_classifications_corpus_coverage,
)
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_award_positions_classifications_corpus_coverage as scan_award_positions_script


EXPECTED_GROUPS = {
    "award_position_classification_source_and_build",
    "appointment_position_and_worksite_assignment",
    "payroll_interpretation_rate_and_decision_story",
    "comparison_remediation_and_classification_lenses",
    "worker_story_admin_queue_and_readiness_relationship",
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


def test_award_positions_classifications_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "AwardPosition and AwardPositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source",
    )

    report = scan_award_positions_classifications_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "AWARD_POSITIONS_CLASSIFICATIONS"
    assert report["domain"] == "Award Positions / Classifications"
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


def test_award_positions_classifications_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "AwardPosition, AwardPositionClass and PositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source A",
    )
    _ingest(
        db_session,
        "Award Position Class and Award Position evidence preserve position groups and deterministic extraction hardening.",
        "Developer Log - Award Positions Classifications Source B",
    )
    _ingest(
        db_session,
        "EmployeeAppointment connects through WorksitePosition and Worksite assignment context.",
        "Developer Log - Award Positions Classifications Assignment",
    )
    _ingest(
        db_session,
        "Classification context supports payroll interpretation and RateSource evidence.",
        "Developer Log - Award Positions Classifications Payroll",
    )

    report = scan_award_positions_classifications_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["award_position_classification_source_and_build"]["coverage_status"] == "STRONG"
    assert groups["payroll_interpretation_rate_and_decision_story"]["coverage_status"] == "WEAK"
    assert groups["comparison_remediation_and_classification_lenses"]["coverage_status"] == "MISSING"
    assert groups["award_position_classification_source_and_build"]["matched_sources"]
    assert groups["award_position_classification_source_and_build"]["representative_matched_terms"]
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_award_positions_classifications_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "AwardPosition and AwardPositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source",
    )
    monkeypatch.setattr(sys, "argv", ["scan_award_positions_classifications_corpus_coverage.py", "--json"])

    exit_code = scan_award_positions_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "AWARD_POSITIONS_CLASSIFICATIONS"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_award_positions_classifications_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "award-positions-classifications-coverage.json"
    _ingest(
        db_session,
        "AwardPosition and AwardPositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_award_positions_classifications_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_award_positions_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Award Positions / Classifications corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out
    assert report["plan_id"] == "AWARD_POSITIONS_CLASSIFICATIONS"


def test_award_positions_classifications_corpus_coverage_human_output_is_diagnostic_only(
    db_session,
    monkeypatch,
    capsys,
):
    _ingest(
        db_session,
        "AwardPosition and AwardPositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source",
    )
    monkeypatch.setattr(sys, "argv", ["scan_award_positions_classifications_corpus_coverage.py"])

    exit_code = scan_award_positions_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out


def test_award_positions_classifications_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "AwardPosition and AwardPositionClass provide classification levels, pay guide and class evidence.",
        "Developer Log - Award Positions Classifications Source",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_award_positions_classifications_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_award_positions_classifications_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_award_positions_classifications_corpus_coverage.py" in readme
    assert "build_award_positions_classifications_answer_gap_report.py" in readme
    assert "Award Positions / Classifications diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
    assert "do not prove runtime operational truth" in readme
    assert "do not classify workers" in readme
    assert "do not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records" in readme
    assert "do not select award classes at runtime" in readme
    assert "do not interpret awards at runtime" in readme
    assert "do not calculate payroll" in readme
    assert "do not decide entitlements" in readme

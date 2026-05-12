import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.imports_actuals_corpus_coverage_service import scan_imports_actuals_corpus_coverage
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_imports_actuals_corpus_coverage as scan_imports_actuals_corpus_coverage_script


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


def test_imports_actuals_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose",
    )

    report = scan_imports_actuals_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "IMPORTS_ACTUALS"
    assert report["domain"] == "Imports / Actuals"
    assert report["total_evidence_groups"] == 12
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "imported_timesheet_source_truth",
        "imported_payroll_actuals_lane",
        "source_system_mapping_and_validation",
        "pay_code_and_rate_type_mapping",
        "position_classification_mapping",
        "objecttime_and_source_truth_connection",
        "comparison_and_remediation_connection",
        "reconciliation_and_movement_review_connection",
        "worker_story_and_admin_queue_connection",
        "evidence_provenance_and_audit",
        "outstanding_hardening",
    }
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


def test_imports_actuals_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose A",
    )
    _ingest(
        db_session,
        "Imports and Actuals are not calculated interpreter truth and preserve governed imported evidence.",
        "Developer Log - Imports Actuals Purpose B",
    )
    _ingest(
        db_session,
        "Imported payroll actuals are payroll actuals in an actuals lane and external outcome lane.",
        "Developer Log - Imports Actuals Lane",
    )

    report = scan_imports_actuals_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["imported_payroll_actuals_lane"]["coverage_status"] == "WEAK"
    assert groups["position_classification_mapping"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_imports_actuals_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_imports_actuals_corpus_coverage.py", "--json"])

    exit_code = scan_imports_actuals_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "IMPORTS_ACTUALS"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_imports_actuals_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "imports-actuals-coverage.json"
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_imports_actuals_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_imports_actuals_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Imports / Actuals corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "IMPORTS_ACTUALS"


def test_imports_actuals_corpus_coverage_human_output_is_diagnostic_only(
    db_session,
    monkeypatch,
    capsys,
):
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_imports_actuals_corpus_coverage.py"])

    exit_code = scan_imports_actuals_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_imports_actuals_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Imports / Actuals are governed imported evidence and external source evidence.",
        "Developer Log - Imports Actuals Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_imports_actuals_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

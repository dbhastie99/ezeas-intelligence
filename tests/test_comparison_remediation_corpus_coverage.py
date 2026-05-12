import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.comparison_remediation_corpus_coverage_service import (
    scan_comparison_remediation_corpus_coverage,
)
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_comparison_remediation_corpus_coverage as scan_comparison_remediation_corpus_coverage_script


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


def test_comparison_remediation_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose",
    )

    report = scan_comparison_remediation_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "COMPARISON_REMEDIATION"
    assert report["domain"] == "Comparison / Remediation"
    assert report["total_evidence_groups"] == 12
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "three_lane_comparison_model",
        "primary_award_path_preservation",
        "actuals_as_external_outcome_truth",
        "comparison_policy",
        "comparison_run_and_line_evidence",
        "variance_generation_and_governance",
        "position_classification_mapping",
        "worker_story_connection",
        "admin_queue_connection",
        "movement_review_connection",
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


def test_comparison_remediation_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Comparison / Remediation is a governed comparison capability for remediation.",
        "Developer Log - Comparison Remediation Purpose A",
    )
    _ingest(
        db_session,
        "Comparison Remediation provides governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose B",
    )
    _ingest(
        db_session,
        "AwardComparisonPolicy governs comparator selection and variance treatment.",
        "Developer Log - Comparison Policy",
    )

    report = scan_comparison_remediation_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["comparison_policy"]["coverage_status"] == "WEAK"
    assert groups["actuals_as_external_outcome_truth"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_comparison_remediation_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_comparison_remediation_corpus_coverage.py", "--json"])

    exit_code = scan_comparison_remediation_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "COMPARISON_REMEDIATION"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_comparison_remediation_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "comparison-remediation-coverage.json"
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_comparison_remediation_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_comparison_remediation_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Comparison / Remediation corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "COMPARISON_REMEDIATION"


def test_comparison_remediation_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_comparison_remediation_corpus_coverage.py"])

    exit_code = scan_comparison_remediation_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_comparison_remediation_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence for operators.",
        "Developer Log - Comparison Remediation Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_comparison_remediation_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

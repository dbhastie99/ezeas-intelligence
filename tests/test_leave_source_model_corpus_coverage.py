import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.leave_source_model_corpus_coverage_service import (
    scan_leave_source_model_corpus_coverage,
)
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_leave_source_model_corpus_coverage as scan_leave_source_model_corpus_coverage_script


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


def test_leave_source_model_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for leave worker context.",
        "Developer Log - Leave Source Model Purpose",
    )

    report = scan_leave_source_model_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "LEAVE_SOURCE_MODEL"
    assert report["domain"] == "Leave Source Model"
    assert report["total_evidence_groups"] == 11
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "applicability_vs_rule_content",
        "leave_type_rule_limitations",
        "contact_vs_appointment_scope",
        "source_dimensions_and_precedence",
        "leave_accrual_connection",
        "leave_request_and_payment_effects_connection",
        "worker_story_connection",
        "command_centre_and_finalisation_connection",
        "readiness_and_missing_output_detection",
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


def test_leave_source_model_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for whether leave applies.",
        "Developer Log - Leave Source Model Purpose A",
    )
    _ingest(
        db_session,
        "Leave Source Model is not leave calculation and it decides worker context applicability.",
        "Developer Log - Leave Source Model Purpose B",
    )
    _ingest(
        db_session,
        "LeaveTypeRule is policy calculation content and not final applicability truth.",
        "Developer Log - Leave Source Model Rule",
    )

    report = scan_leave_source_model_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["leave_type_rule_limitations"]["coverage_status"] == "WEAK"
    assert groups["source_dimensions_and_precedence"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_leave_source_model_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for leave worker context.",
        "Developer Log - Leave Source Model Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_source_model_corpus_coverage.py", "--json"])

    exit_code = scan_leave_source_model_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "LEAVE_SOURCE_MODEL"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_leave_source_model_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "leave-source-model-coverage.json"
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for leave worker context.",
        "Developer Log - Leave Source Model Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_leave_source_model_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_leave_source_model_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Leave Source Model corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "LEAVE_SOURCE_MODEL"


def test_leave_source_model_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for leave worker context.",
        "Developer Log - Leave Source Model Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_source_model_corpus_coverage.py"])

    exit_code = scan_leave_source_model_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_leave_source_model_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability and source-truth layer for leave worker context.",
        "Developer Log - Leave Source Model Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_leave_source_model_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


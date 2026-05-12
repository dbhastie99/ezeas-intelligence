import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.leave_accrual_processing_corpus_coverage_service import (
    scan_leave_accrual_processing_corpus_coverage,
)
from scripts import scan_leave_accrual_processing_corpus_coverage as scan_leave_accrual_processing_corpus_coverage_script


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


def test_leave_accrual_processing_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Accrual Purpose",
    )

    report = scan_leave_accrual_processing_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "LEAVE_ACCRUAL_PROCESSING"
    assert report["domain"] == "Leave Accrual Detail / Leave Processing"
    assert report["total_evidence_groups"] == 12
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "leave_source_truth_and_applicability",
        "accrual_basis_and_quantity",
        "payroll_output_and_calc_interpreter_source",
        "leave_type_and_rule_configuration",
        "leave_ledger_and_accrual_posting",
        "leave_valuation_basis",
        "leave_request_payment_effects",
        "payrun_processing_and_finalisation",
        "worker_story_connection",
        "payroll_bases_connection",
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


def test_leave_accrual_processing_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Purpose A",
    )
    _ingest(
        db_session,
        "Leave Accrual / Processing is not Minerva calculations or generic leave policy advice.",
        "Developer Log - Leave Purpose B",
    )
    _ingest(
        db_session,
        "Leave source truth and applicability govern accrual while LeaveTypeRule is not final source truth.",
        "Developer Log - Leave Source Truth",
    )

    report = scan_leave_accrual_processing_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["leave_source_truth_and_applicability"]["coverage_status"] == "WEAK"
    assert groups["leave_request_payment_effects"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_leave_accrual_processing_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_accrual_processing_corpus_coverage.py", "--json"])

    exit_code = scan_leave_accrual_processing_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "LEAVE_ACCRUAL_PROCESSING"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_leave_accrual_processing_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "leave-accrual-processing-coverage.json"
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_leave_accrual_processing_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_leave_accrual_processing_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Leave Accrual / Processing corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "LEAVE_ACCRUAL_PROCESSING"


def test_leave_accrual_processing_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_accrual_processing_corpus_coverage.py"])

    exit_code = scan_leave_accrual_processing_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_leave_accrual_processing_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes.",
        "Developer Log - Leave Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_leave_accrual_processing_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

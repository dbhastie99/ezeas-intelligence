import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.payment_execution_remittance_corpus_coverage_service import (
    scan_payment_execution_remittance_corpus_coverage,
)
from scripts import scan_payment_execution_remittance_corpus_coverage as scan_payment_execution_remittance_corpus_coverage_script


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


def test_payment_execution_remittance_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose",
    )

    report = scan_payment_execution_remittance_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PAYMENT_EXECUTION_REMITTANCE"
    assert report["domain"] == "Payment Execution / Remittance"
    assert report["total_evidence_groups"] == 11
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "finalised_gross_to_net_source",
        "worker_net_pay_and_bank_allocation",
        "payment_destination_readiness",
        "negative_net_pay_and_obligation_interaction",
        "deduction_and_third_party_remittance",
        "payment_file_generation_and_period_close",
        "remittance_batching_and_reconciliation",
        "worker_attention_and_admin_queue_connection",
        "worker_story_and_audit_evidence",
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


def test_payment_execution_remittance_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose A",
    )
    _ingest(
        db_session,
        "Payment Execution / Remittance is not a generic file export.",
        "Developer Log - Payment Execution Purpose B",
    )
    _ingest(
        db_session,
        "Worker net pay requires payment allocation and bank allocation before complete payment execution.",
        "Developer Log - Worker Net Pay Allocation",
    )

    report = scan_payment_execution_remittance_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["worker_net_pay_and_bank_allocation"]["coverage_status"] == "WEAK"
    assert groups["remittance_batching_and_reconciliation"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_payment_execution_remittance_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payment_execution_remittance_corpus_coverage.py", "--json"])

    exit_code = scan_payment_execution_remittance_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PAYMENT_EXECUTION_REMITTANCE"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_payment_execution_remittance_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "payment-execution-remittance-coverage.json"
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_payment_execution_remittance_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_payment_execution_remittance_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Payment Execution / Remittance corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "PAYMENT_EXECUTION_REMITTANCE"


def test_payment_execution_remittance_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payment_execution_remittance_corpus_coverage.py"])

    exit_code = scan_payment_execution_remittance_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_payment_execution_remittance_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence.",
        "Developer Log - Payment Execution Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_payment_execution_remittance_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

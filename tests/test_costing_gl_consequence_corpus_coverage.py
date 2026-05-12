import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.costing_gl_consequence_corpus_coverage_service import (
    scan_costing_gl_consequence_corpus_coverage,
)
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_costing_gl_consequence_corpus_coverage as scan_costing_script


EXPECTED_GROUPS = {
    "purpose_and_operator_meaning",
    "downstream_not_payroll_calculation_truth",
    "finalised_payroll_outcome_source",
    "payment_execution_and_remittance_connection",
    "employer_liability_and_oncost_connection",
    "deduction_obligation_and_writeoff_consequences",
    "comparison_remediation_variance_connection",
    "leave_valuation_and_accrual_connection",
    "negative_net_pay_and_out_of_pay_consequences",
    "audit_story_and_financial_evidence",
    "deferred_costing_slice_boundary",
    "outstanding_hardening",
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


def test_costing_gl_consequence_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose",
    )

    report = scan_costing_gl_consequence_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "COSTING_GL_CONSEQUENCE"
    assert report["domain"] == "Costing / GL Consequence Evidence"
    assert report["total_evidence_groups"] == 12
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


def test_costing_gl_consequence_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose A",
    )
    _ingest(
        db_session,
        "Costing is a GL consequence domain and not payroll calculation truth.",
        "Developer Log - Costing Purpose B",
    )
    _ingest(
        db_session,
        "Leave valuation and leave accrual evidence may eventually flow to costing.",
        "Developer Log - Costing Leave Valuation",
    )

    report = scan_costing_gl_consequence_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["leave_valuation_and_accrual_connection"]["coverage_status"] == "WEAK"
    assert groups["negative_net_pay_and_out_of_pay_consequences"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_costing_gl_consequence_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_costing_gl_consequence_corpus_coverage.py", "--json"])

    exit_code = scan_costing_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "COSTING_GL_CONSEQUENCE"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_costing_gl_consequence_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "costing-gl-consequence-coverage.json"
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_costing_gl_consequence_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_costing_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Costing / GL Consequence Evidence corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "COSTING_GL_CONSEQUENCE"


def test_costing_gl_consequence_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_costing_gl_consequence_corpus_coverage.py"])

    exit_code = scan_costing_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_costing_gl_consequence_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence.",
        "Developer Log - Costing Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_costing_gl_consequence_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

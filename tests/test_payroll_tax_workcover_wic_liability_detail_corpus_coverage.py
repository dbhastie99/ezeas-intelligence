import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.payroll_tax_workcover_wic_liability_detail_corpus_coverage_service import (
    scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage,
)
from scripts import scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage as scan_payroll_tax_wic_script


EXPECTED_GROUPS = {
    "liability_scope_and_employer_side_boundary",
    "jurisdiction_worksite_and_state_context",
    "governed_basis_membership_and_payroll_bases",
    "rates_sources_and_liability_evidence",
    "worker_story_output_and_finalisation_relationship",
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


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope",
    )

    report = scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL"
    assert report["domain"] == "Payroll Tax / WorkCover / WIC Liability Detail"
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


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liabilities and employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope A",
    )
    _ingest(
        db_session,
        "WorkCover, WIC and Workers Compensation are employer-side liability evidence, not PAYG withholding.",
        "Developer Log - Payroll Tax WorkCover WIC Scope B",
    )
    _ingest(
        db_session,
        "Worksite.StateId and WorksitePosition provide jurisdiction context for Payroll Tax liability.",
        "Developer Log - Payroll Tax WorkCover WIC Jurisdiction",
    )
    _ingest(
        db_session,
        "RateSource provides date-effective rates for liability evidence.",
        "Developer Log - Payroll Tax WorkCover WIC Rates",
    )

    report = scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["liability_scope_and_employer_side_boundary"]["coverage_status"] == "STRONG"
    assert groups["rates_sources_and_liability_evidence"]["coverage_status"] == "WEAK"
    assert groups["worker_story_output_and_finalisation_relationship"]["coverage_status"] == "MISSING"
    assert groups["liability_scope_and_employer_side_boundary"]["matched_sources"]
    assert groups["liability_scope_and_employer_side_boundary"]["representative_matched_terms"]
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py", "--json"])

    exit_code = scan_payroll_tax_wic_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_writes_output_file(
    db_session,
    tmp_path,
    monkeypatch,
    capsys,
):
    output_path = tmp_path / "payroll-tax-workcover-wic-coverage.json"
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_payroll_tax_wic_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Payroll Tax / WorkCover / WIC Liability Detail corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out
    assert report["plan_id"] == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL"


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_human_output_is_diagnostic_only(
    db_session,
    monkeypatch,
    capsys,
):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py"])

    exit_code = scan_payroll_tax_wic_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out


def test_payroll_tax_workcover_wic_liability_detail_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liability evidence, not worker net pay.",
        "Developer Log - Payroll Tax WorkCover WIC Scope",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_payroll_tax_workcover_wic_liability_detail_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py" in readme
    assert "build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py" in readme
    assert "Payroll Tax / WorkCover / WIC Liability Detail diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
    assert "do not prove runtime operational truth" in readme
    assert "do not calculate payroll tax" in readme
    assert "do not calculate WorkCover or WIC liability" in readme
    assert "do not lodge or remit statutory returns" in readme
    assert "do not decide statutory liability" in readme
    assert "do not change employer-liability configuration" in readme
    assert "do not change Worksite, State or jurisdiction truth" in readme
    assert "do not calculate payroll" in readme
    assert "do not mutate payroll output" in readme
    assert "do not determine or finalise readiness" in readme

import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.tax_payg_corpus_coverage_service import scan_tax_payg_corpus_coverage
from scripts import scan_tax_payg_corpus_coverage as scan_tax_payg_corpus_coverage_script


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


def test_tax_payg_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence for operators.",
        "Developer Log - Tax PAYG Purpose",
    )

    report = scan_tax_payg_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "TAX_PAYG"
    assert report["domain"] == "Tax / PAYG"
    assert report["total_evidence_groups"] == 12
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "deterministic_tax_boundary",
        "tax_story_and_explainability",
        "taxable_basis_and_payroll_bases",
        "worker_tax_declaration_and_withholding_inputs",
        "payment_date_and_process_period_context",
        "pay_frequency_and_provider_support",
        "gross_to_net_and_finalised_totals",
        "supplementary_incremental_payg",
        "worker_story_and_admin_queue_connection",
        "unsupported_and_review_states",
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


def test_tax_payg_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence.",
        "Developer Log - Tax PAYG Purpose A",
    )
    _ingest(
        db_session,
        "PAYG withholding is governed withholding calculation evidence for tax evidence.",
        "Developer Log - Tax PAYG Purpose B",
    )
    _ingest(
        db_session,
        "TaxStory explains worker tax profile and rule pack selection.",
        "Developer Log - TaxStory",
    )

    report = scan_tax_payg_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["tax_story_and_explainability"]["coverage_status"] == "WEAK"
    assert groups["supplementary_incremental_payg"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_tax_payg_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence for operators.",
        "Developer Log - Tax PAYG Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_tax_payg_corpus_coverage.py", "--json"])

    exit_code = scan_tax_payg_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "TAX_PAYG"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_tax_payg_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "tax-payg-coverage.json"
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence for operators.",
        "Developer Log - Tax PAYG Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_tax_payg_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_tax_payg_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Tax / PAYG corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "TAX_PAYG"


def test_tax_payg_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence for operators.",
        "Developer Log - Tax PAYG Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_tax_payg_corpus_coverage.py"])

    exit_code = scan_tax_payg_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_tax_payg_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence for operators.",
        "Developer Log - Tax PAYG Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_tax_payg_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

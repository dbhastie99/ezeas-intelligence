import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.payroll_bases_corpus_coverage_service import scan_payroll_bases_corpus_coverage
from scripts import scan_payroll_bases_corpus_coverage as scan_payroll_bases_corpus_coverage_script


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


def test_payroll_bases_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose",
    )

    report = scan_payroll_bases_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PAYROLL_BASES_AND_TOTALS"
    assert report["domain"] == "Payroll Bases & Totals"
    assert report["total_evidence_groups"] == 9
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "bucket_definition_and_membership",
        "worked_hours_and_quantity",
        "gross_ordinary_superable_taxable_bases",
        "current_effective_truth",
        "readiness_and_rebuild",
        "worker_story_connection",
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


def test_payroll_bases_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose A",
    )
    _ingest(
        db_session,
        "Payroll Bases and Totals provide governed payroll basis evidence for operator understanding.",
        "Developer Log - Payroll Bases Purpose B",
    )
    _ingest(
        db_session,
        "Payroll Bases & Totals require current-effective truth and current-effective payroll output.",
        "Developer Log - Payroll Current Effective Truth",
    )

    report = scan_payroll_bases_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["current_effective_truth"]["coverage_status"] == "WEAK"
    assert groups["readiness_and_rebuild"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_payroll_bases_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_bases_corpus_coverage.py", "--json"])

    exit_code = scan_payroll_bases_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PAYROLL_BASES_AND_TOTALS"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_payroll_bases_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "payroll-bases-coverage.json"
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_payroll_bases_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_payroll_bases_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Payroll Bases & Totals corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "PAYROLL_BASES_AND_TOTALS"


def test_payroll_bases_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_bases_corpus_coverage.py"])

    exit_code = scan_payroll_bases_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_payroll_bases_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operators.",
        "Developer Log - Payroll Bases Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_payroll_bases_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count

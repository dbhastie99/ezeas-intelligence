import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.payroll_output_corpus_coverage_service import scan_payroll_output_corpus_coverage
from scripts import scan_payroll_output_corpus_coverage as scan_payroll_output_script


EXPECTED_GROUPS = {
    "payroll_output_purpose",
    "calculated_payroll_lines",
    "current_effective_output_truth",
    "run_output_vs_process_period_output",
    "worker_level_output",
    "payrun_totals_and_line_totals",
    "decision_story_and_rate_story_relationship",
    "gross_to_net_relationship",
    "payroll_bases_relationship",
    "finalisation_and_payment_execution_relationship",
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


def test_payroll_output_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Payroll Output explains calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose",
    )

    report = scan_payroll_output_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PAYROLL_OUTPUT"
    assert report["domain"] == "Payroll Output"
    assert report["total_evidence_groups"] == 11
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


def test_payroll_output_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Payroll Output and PayRun Output explain calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose A",
    )
    _ingest(
        db_session,
        "Payroll Output is calculated payroll result evidence for output review.",
        "Developer Log - Payroll Output Purpose B",
    )
    _ingest(
        db_session,
        "Calculated payroll lines and payroll line evidence explain output line treatment.",
        "Developer Log - Payroll Output Lines",
    )

    report = scan_payroll_output_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["payroll_output_purpose"]["coverage_status"] == "STRONG"
    assert groups["calculated_payroll_lines"]["coverage_status"] == "WEAK"
    assert groups["finalisation_and_payment_execution_relationship"]["coverage_status"] == "MISSING"
    assert groups["payroll_output_purpose"]["matched_sources"]
    assert groups["payroll_output_purpose"]["representative_matched_terms"]
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_payroll_output_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payroll Output explains calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_output_corpus_coverage.py", "--json"])

    exit_code = scan_payroll_output_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PAYROLL_OUTPUT"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_payroll_output_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "payroll-output-coverage.json"
    _ingest(
        db_session,
        "Payroll Output explains calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_output_corpus_coverage.py", "--output", str(output_path)])

    exit_code = scan_payroll_output_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Payroll Output corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert report["plan_id"] == "PAYROLL_OUTPUT"


def test_payroll_output_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Payroll Output explains calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payroll_output_corpus_coverage.py"])

    exit_code = scan_payroll_output_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out


def test_payroll_output_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Payroll Output explains calculated payroll output and payroll result evidence.",
        "Developer Log - Payroll Output Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_payroll_output_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_payroll_output_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_payroll_output_corpus_coverage.py" in readme
    assert "build_payroll_output_answer_gap_report.py" in readme
    assert "Payroll Output diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme

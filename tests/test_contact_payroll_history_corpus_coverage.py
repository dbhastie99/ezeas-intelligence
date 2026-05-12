import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.contact_payroll_history_corpus_coverage_service import (
    scan_contact_payroll_history_corpus_coverage,
)
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_contact_payroll_history_corpus_coverage as scan_contact_payroll_history_script


EXPECTED_GROUPS = {
    "contact_payroll_history_purpose",
    "contact_identity_and_payrun_participation",
    "current_and_historical_payroll_output",
    "gross_to_net_history",
    "deductions_obligations_and_negative_net_pay",
    "tax_and_payment_readiness_history",
    "leave_and_accrual_history",
    "worker_story_relationship",
    "movement_review_and_admin_queue_relationship",
    "retro_replay_and_correction_relationship",
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


def test_contact_payroll_history_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history and worker payroll history.",
        "Developer Log - Contact Payroll History Purpose",
    )

    report = scan_contact_payroll_history_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "CONTACT_PAYROLL_HISTORY"
    assert report["domain"] == "Contact Payroll History"
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


def test_contact_payroll_history_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history, worker payroll history and payroll outcome history.",
        "Developer Log - Contact Payroll History Purpose A",
    )
    _ingest(
        db_session,
        "Contact Payroll History is contact-level payroll history evidence for operators.",
        "Developer Log - Contact Payroll History Purpose B",
    )
    _ingest(
        db_session,
        "PayRun participation and worker history show where a worker appeared.",
        "Developer Log - Contact Payroll History Participation",
    )
    _ingest(
        db_session,
        "Leave history and accrual history can appear in the contact payroll history lens.",
        "Developer Log - Contact Payroll History Leave",
    )

    report = scan_contact_payroll_history_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["contact_payroll_history_purpose"]["coverage_status"] == "STRONG"
    assert groups["leave_and_accrual_history"]["coverage_status"] == "WEAK"
    assert groups["retro_replay_and_correction_relationship"]["coverage_status"] == "MISSING"
    assert groups["contact_payroll_history_purpose"]["matched_sources"]
    assert groups["contact_payroll_history_purpose"]["representative_matched_terms"]
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_contact_payroll_history_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history and worker payroll history.",
        "Developer Log - Contact Payroll History Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_contact_payroll_history_corpus_coverage.py", "--json"])

    exit_code = scan_contact_payroll_history_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "CONTACT_PAYROLL_HISTORY"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_contact_payroll_history_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "contact-payroll-history-coverage.json"
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history and worker payroll history.",
        "Developer Log - Contact Payroll History Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_contact_payroll_history_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_contact_payroll_history_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Contact Payroll History corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert report["plan_id"] == "CONTACT_PAYROLL_HISTORY"


def test_contact_payroll_history_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history and worker payroll history.",
        "Developer Log - Contact Payroll History Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_contact_payroll_history_corpus_coverage.py"])

    exit_code = scan_contact_payroll_history_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out


def test_contact_payroll_history_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Contact Payroll History explains payroll history and worker payroll history.",
        "Developer Log - Contact Payroll History Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_contact_payroll_history_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_contact_payroll_history_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_contact_payroll_history_corpus_coverage.py" in readme
    assert "build_contact_payroll_history_answer_gap_report.py" in readme
    assert "Contact Payroll History diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme

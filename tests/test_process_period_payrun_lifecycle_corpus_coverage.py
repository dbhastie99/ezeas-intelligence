import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.domain_retrieval_plan_service import detect_domain_retrieval_plan
from app.services.ingestion_service import ingest_file_bytes
from app.services.process_period_payrun_lifecycle_corpus_coverage_service import (
    scan_process_period_payrun_lifecycle_corpus_coverage,
)
from scripts import scan_process_period_payrun_lifecycle_corpus_coverage as scan_process_period_script


EXPECTED_GROUPS = {
    "purpose_and_operator_meaning",
    "process_period_and_group_context",
    "open_not_open_closed_lifecycle",
    "close_rolls_forward",
    "payment_date_and_calendar_policy",
    "payrun_creation_and_admission",
    "run_type_and_run_purpose",
    "regular_supplementary_retro_distinction",
    "payrun_contact_lifecycle",
    "current_effective_output_and_finalisation",
    "payment_execution_and_period_close",
    "worker_story_admin_queue_and_movement_review_connection",
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


def test_process_period_payrun_lifecycle_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose",
    )

    report = scan_process_period_payrun_lifecycle_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PROCESS_PERIOD_PAYRUN_LIFECYCLE"
    assert report["domain"] == "Process Periods / PayRun Lifecycle"
    assert report["total_evidence_groups"] == 13
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


def test_process_period_payrun_lifecycle_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose A",
    )
    _ingest(
        db_session,
        "ProcessPeriod is payment-event lifecycle evidence, not payroll calculation truth and not a generic date range.",
        "Developer Log - Process Period Purpose B",
    )
    _ingest(
        db_session,
        "PaymentDate and payment date matter for payment context and governed derived calendar policy.",
        "Developer Log - Process Period PaymentDate",
    )

    report = scan_process_period_payrun_lifecycle_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["payment_date_and_calendar_policy"]["coverage_status"] == "WEAK"
    assert groups["payrun_contact_lifecycle"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_process_period_payrun_lifecycle_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_process_period_payrun_lifecycle_corpus_coverage.py", "--json"])

    exit_code = scan_process_period_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PROCESS_PERIOD_PAYRUN_LIFECYCLE"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_process_period_payrun_lifecycle_corpus_coverage_writes_output_file(
    db_session, tmp_path, monkeypatch, capsys
):
    output_path = tmp_path / "process-period-payrun-lifecycle-coverage.json"
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_process_period_payrun_lifecycle_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_process_period_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Process Periods / PayRun Lifecycle corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "PROCESS_PERIOD_PAYRUN_LIFECYCLE"


def test_process_period_payrun_lifecycle_corpus_coverage_human_output_is_diagnostic_only(
    db_session, monkeypatch, capsys
):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_process_period_payrun_lifecycle_corpus_coverage.py"])

    exit_code = scan_process_period_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_process_period_payrun_lifecycle_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context.",
        "Developer Log - Process Period Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_process_period_payrun_lifecycle_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_process_period_payrun_lifecycle_detection_keeps_overlapping_domain_ownership():
    tax_plan = detect_domain_retrieval_plan("Why does ProcessPeriod PaymentDate matter for Tax / PAYG?")
    retro_plan = detect_domain_retrieval_plan("How should Retro / Replay handle attributed period and paid period truth?")
    finalisation_plan = detect_domain_retrieval_plan("Why does current-effective payroll output matter for finalisation?")

    assert tax_plan is not None
    assert tax_plan.plan_id == "TAX_PAYG"
    assert retro_plan is not None
    assert retro_plan.plan_id == "RETRO_REPLAY"
    assert finalisation_plan is not None
    assert finalisation_plan.plan_id == "FINALISATION_READINESS"

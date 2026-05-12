import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.contacts_employee_appointments_corpus_coverage_service import (
    scan_contacts_employee_appointments_corpus_coverage,
)
from app.services.domain_retrieval_plan_service import detect_domain_retrieval_plan
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_contacts_employee_appointments_corpus_coverage as scan_contacts_script


EXPECTED_GROUPS = {
    "purpose_and_operator_meaning",
    "contact_identity_and_worker_context",
    "employee_appointment_as_employment_assignment",
    "appointment_scope_and_payrun_admission",
    "award_classification_and_position_context",
    "worksite_state_and_runtime_location",
    "objecttime_and_source_truth_connection",
    "leave_source_and_accrual_connection",
    "worker_story_and_contact_history_connection",
    "worker_readiness_tax_bank_deduction_payment",
    "dirty_contact_and_reprocessing",
    "comparison_and_classification_lenses",
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


def test_contacts_employee_appointments_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose",
    )

    report = scan_contacts_employee_appointments_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "CONTACTS_EMPLOYEE_APPOINTMENTS"
    assert report["domain"] == "Contacts / Employee Appointments"
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


def test_contacts_employee_appointments_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose A",
    )
    _ingest(
        db_session,
        "Contact and EmployeeAppointment provide employment context and are not payroll calculation truth.",
        "Developer Log - Contacts Purpose B",
    )
    _ingest(
        db_session,
        "AwardPositionClass supplies award classification and classification evidence for appointment context.",
        "Developer Log - Contacts Award Classification",
    )

    report = scan_contacts_employee_appointments_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["award_classification_and_position_context"]["coverage_status"] == "WEAK"
    assert groups["leave_source_and_accrual_connection"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_contacts_employee_appointments_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_contacts_employee_appointments_corpus_coverage.py", "--json"])

    exit_code = scan_contacts_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "CONTACTS_EMPLOYEE_APPOINTMENTS"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_contacts_employee_appointments_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "contacts-employee-appointments-coverage.json"
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_contacts_employee_appointments_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_contacts_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Contacts / Employee Appointments corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "CONTACTS_EMPLOYEE_APPOINTMENTS"


def test_contacts_employee_appointments_corpus_coverage_human_output_is_diagnostic_only(
    db_session, monkeypatch, capsys
):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_contacts_employee_appointments_corpus_coverage.py"])

    exit_code = scan_contacts_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_contacts_employee_appointments_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as worker identity context.",
        "Developer Log - Contacts Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_contacts_employee_appointments_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_contacts_diagnostics_do_not_steal_ordinary_payrun_admin_queue_dirty_contact_questions():
    plan = detect_domain_retrieval_plan("How do Worker Attention and dirty contacts relate to the PayRun Admin Queue?")

    assert plan is not None
    assert plan.plan_id == "PAYRUN_ADMIN_QUEUE"

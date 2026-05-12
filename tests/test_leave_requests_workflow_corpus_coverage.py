import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.leave_requests_workflow_corpus_coverage_service import scan_leave_requests_workflow_corpus_coverage
from scripts import scan_leave_requests_workflow_corpus_coverage as scan_leave_requests_workflow_script


EXPECTED_GROUPS = {
    "request_lifecycle_and_status_transitions",
    "preview_overlap_and_shortfall_handling",
    "taken_leave_valuation_and_hard_fail",
    "leaveledger_posting_and_balance_effects",
    "leave_source_and_applicability_relationship",
    "worker_story_payrun_and_finalisation_relationship",
    "idempotency_reopen_and_approval_governance",
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


def test_leave_requests_workflow_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and approve leave.",
        "Developer Log - Leave Requests Workflow Lifecycle",
    )

    report = scan_leave_requests_workflow_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "LEAVE_REQUESTS_WORKFLOW"
    assert report["domain"] == "Leave Requests / Leave Workflow"
    assert report["total_evidence_groups"] == 8
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


def test_leave_requests_workflow_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and review leave.",
        "Developer Log - Leave Requests Workflow Lifecycle A",
    )
    _ingest(
        db_session,
        "Approve leave, reject leave and reopen leave are governed status transitions in the Leave Request workflow.",
        "Developer Log - Leave Requests Workflow Lifecycle B",
    )
    _ingest(
        db_session,
        "Leave request preview is read-only and checks leave overlap.",
        "Developer Log - Leave Requests Preview",
    )

    report = scan_leave_requests_workflow_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["request_lifecycle_and_status_transitions"]["coverage_status"] == "STRONG"
    assert groups["preview_overlap_and_shortfall_handling"]["coverage_status"] == "WEAK"
    assert groups["taken_leave_valuation_and_hard_fail"]["coverage_status"] == "MISSING"
    assert groups["request_lifecycle_and_status_transitions"]["matched_sources"]
    assert groups["request_lifecycle_and_status_transitions"]["representative_matched_terms"]
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_leave_requests_workflow_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and approve leave.",
        "Developer Log - Leave Requests Workflow Lifecycle",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_requests_workflow_corpus_coverage.py", "--json"])

    exit_code = scan_leave_requests_workflow_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "LEAVE_REQUESTS_WORKFLOW"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_leave_requests_workflow_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "leave-requests-workflow-coverage.json"
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and approve leave.",
        "Developer Log - Leave Requests Workflow Lifecycle",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_leave_requests_workflow_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_leave_requests_workflow_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Leave Requests / Leave Workflow corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out
    assert report["plan_id"] == "LEAVE_REQUESTS_WORKFLOW"


def test_leave_requests_workflow_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and approve leave.",
        "Developer Log - Leave Requests Workflow Lifecycle",
    )
    monkeypatch.setattr(sys, "argv", ["scan_leave_requests_workflow_corpus_coverage.py"])

    exit_code = scan_leave_requests_workflow_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert "Runtime operational truth proof: no" in captured.out


def test_leave_requests_workflow_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Leave Request workflow status transitions include create leave request, draft leave, submit leave and approve leave.",
        "Developer Log - Leave Requests Workflow Lifecycle",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_leave_requests_workflow_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_leave_requests_workflow_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_leave_requests_workflow_corpus_coverage.py" in readme
    assert "build_leave_requests_workflow_answer_gap_report.py" in readme
    assert "Leave Requests / Leave Workflow diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
    assert "do not prove runtime operational truth" in readme

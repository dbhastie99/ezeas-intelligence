import json
import sys
from pathlib import Path

from app.models.knowledge import KnowledgeDocument
from app.services.annual_leave_corpus_coverage_service import scan_annual_leave_corpus_coverage
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_annual_leave_corpus_coverage as scan_annual_leave_corpus_coverage_script


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


def test_annual_leave_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )

    report = scan_annual_leave_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "ANNUAL_LEAVE_MANAGEMENT"
    assert report["domain"] == "Annual Leave / Leave Management"
    assert report["total_evidence_groups"] == 7
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "configuration",
        "accrual",
        "taken",
        "valuation",
        "payrun",
        "worker_story",
        "outstanding",
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


def test_annual_leave_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration A",
    )
    _ingest(
        db_session,
        "Annual Leave configuration includes LeaveType and LeaveTypeRule governance in Rule Cockpit.",
        "Developer Log - Annual Leave Configuration B",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts minutes to LeaveLedger from interpreter truth with no fallback.",
        "Developer Log - Annual Leave Accrual",
    )

    report = scan_annual_leave_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["configuration"]["coverage_status"] == "STRONG"
    assert groups["accrual"]["coverage_status"] == "WEAK"
    assert groups["valuation"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_annual_leave_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    monkeypatch.setattr(sys, "argv", ["scan_annual_leave_corpus_coverage.py", "--json"])

    exit_code = scan_annual_leave_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "ANNUAL_LEAVE_MANAGEMENT"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_annual_leave_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "annual-leave-coverage.json"
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_annual_leave_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_annual_leave_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Annual Leave / Leave Management corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "ANNUAL_LEAVE_MANAGEMENT"


def test_annual_leave_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    monkeypatch.setattr(sys, "argv", ["scan_annual_leave_corpus_coverage.py"])

    exit_code = scan_annual_leave_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_annual_leave_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_annual_leave_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_annual_leave_corpus_coverage_does_not_treat_adjacent_domains_as_substitutes(db_session):
    _ingest(
        db_session,
        "Leave Accrual / Processing posts accrual basis and LeaveLedger minutes from interpreter truth.",
        "Developer Log - Adjacent Leave Accrual Processing",
    )
    _ingest(
        db_session,
        "Public Holidays uses calendars and DeductsOnPublicHoliday for payroll treatment.",
        "Developer Log - Adjacent Public Holidays",
    )
    _ingest(
        db_session,
        "Leave Source Model explains source truth applicability and precedence boundaries.",
        "Developer Log - Adjacent Leave Source Model",
    )

    report = scan_annual_leave_corpus_coverage(db_session).to_dict()

    assert report["coverage_counts"]["STRONG"] == 0
    assert all(group["coverage_status"] == "MISSING" for group in report["groups"])
    assert all(group["matched_chunk_count"] == 0 for group in report["groups"])


def test_annual_leave_runbook_includes_corpus_coverage_command():
    runbook = Path("docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md").read_text(encoding="utf-8")

    assert "scripts\\scan_annual_leave_corpus_coverage.py" in runbook
    assert "build_annual_leave_answer_gap_report.py" in runbook
    assert "No Annual Leave / Leave Management-specific answer gap report service or script exists" in runbook

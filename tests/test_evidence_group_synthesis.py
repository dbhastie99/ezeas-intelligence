from app.services.answer_generation_service import generate_grounded_answer
from app.services.domain_retrieval_plan_service import ANNUAL_LEAVE_MANAGEMENT_PLAN, retrieve_chunks_for_question
from app.services.evidence_group_synthesis_service import synthesize_evidence_group
from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import RetrievalResult
from app.services.golden_question_service import run_golden_questions


def _group(group_id: str):
    return next(group for group in ANNUAL_LEAVE_MANAGEMENT_PLAN.evidence_groups if group.group_id == group_id)


def _result(text: str, group_id: str, title: str = "Developer Log - Annual Leave") -> RetrievalResult:
    group = _group(group_id)
    return RetrievalResult(
        chunk_id=f"chunk-{group_id}",
        document_id=f"document-{group_id}",
        chunk_index=0,
        chunk_text=text,
        title=title,
        original_file_name=f"{group_id}.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        score=50.0,
        matched_tokens=[],
        snippet=text,
        match_ratio=1.0,
        domain_plan_id=ANNUAL_LEAVE_MANAGEMENT_PLAN.plan_id,
        evidence_group_id=group.group_id,
        evidence_group_label=group.label,
    )


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


def test_evidence_group_summary_does_not_copy_broken_snippet_fragment():
    summary = synthesize_evidence_group(
        _group("configuration"),
        [
            _result(
                "ations. Inconsistent UX behaviour appears before real evidence. "
                "Annual Leave uses LeaveType and LeaveTypeRule in Rule Cockpit configuration.",
                "configuration",
            )
        ],
    )

    assert summary.is_weak is False
    assert "ations. Inconsistent UX" not in summary.sentence
    assert "LeaveType/LeaveTypeRule" in summary.sentence


def test_configuration_summary_mentions_leave_type_terms_only_when_present():
    weak_leave_type_summary = synthesize_evidence_group(
        _group("configuration"),
        [_result("Annual Leave setup is surfaced in the Rule Cockpit.", "configuration")],
    )

    assert weak_leave_type_summary.is_weak is False
    assert "LeaveType/LeaveTypeRule" not in weak_leave_type_summary.sentence
    assert "Rule Cockpit" in weak_leave_type_summary.sentence


def test_taken_summary_includes_public_holiday_control_when_present():
    summary = synthesize_evidence_group(
        _group("taken"),
        [
            _result(
                "Annual Leave TAKEN rows use LeaveLedger minutes. Public holiday treatment is controlled by "
                "DeductsOnPublicHoliday.",
                "taken",
            )
        ],
    )

    assert summary.is_weak is False
    assert "public holiday deduction controlled by DeductsOnPublicHoliday" in summary.sentence


def test_weak_group_returns_honest_weak_evidence_statement():
    summary = synthesize_evidence_group(
        _group("valuation"),
        [_result("Annual Leave appears in this document, but no value terms are present.", "valuation")],
    )

    assert summary.is_weak is True
    assert summary.sentence == "The retrieved formal corpus has weak evidence for Valuation and ordinary rate evidence."


def test_product_domain_answer_uses_sections_and_avoids_raw_snippet_stitching(db_session):
    _ingest(
        db_session,
        "ations. Inconsistent UX behaviour. Annual Leave uses LeaveType and LeaveTypeRule in Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts LeaveLedger minutes with interpreter truth and no fallback during PayRun.",
        "Developer Log - Annual Leave Accrual",
    )

    results = retrieve_chunks_for_question(db_session, "How is Annual Leave managed in the system?")
    answer, _, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", results)

    assert "Direct summary" in answer
    assert "How the system works" in answer
    assert "Current implementation status" in answer
    assert "What remains outstanding" in answer
    assert "Source 1:" not in answer
    assert "Source 2:" not in answer
    assert "ations. Inconsistent UX" not in answer


def test_annual_leave_benchmark_style_fixture_can_pass_with_complete_evidence_groups(db_session):
    _ingest(
        db_session,
        "Annual Leave configuration uses LeaveType and LeaveTypeRule. LeaveTypeKind and Rule Cockpit organise "
        "Accrual Payment Governance settings.",
        "Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts LeaveLedger minutes using interpreter truth with no fallback during PayRun.",
        "Developer Log - Annual Leave Accrual",
    )
    _ingest(
        db_session,
        "Annual Leave TAKEN consumption posts LeaveLedger minutes. Public holiday treatment uses "
        "DeductsOnPublicHoliday with resolver skip behaviour.",
        "Developer Log - Annual Leave TAKEN",
    )
    _ingest(
        db_session,
        "Annual Leave valuation uses valuation basis, ordinary rate, PayRun snapshot and liability evidence.",
        "Developer Log - Annual Leave Valuation",
    )
    _ingest(
        db_session,
        "PayRun processing includes Generate Leave Accruals on Process, leave accruals, valuation basis and Admin Queue.",
        "Developer Log - PayRun Leave Orchestration",
    )
    _ingest(
        db_session,
        "Worker Story includes Leave and Accrual Outcome as server-owned leave output with ledger, valuation basis "
        "and evidence chain.",
        "Developer Log - Worker Story Leave Evidence",
    )
    _ingest(
        db_session,
        "Annual Leave outstanding hardening includes Leave Source Model, FIFO lot consumption, revaluation and "
        "production hardening.",
        "Developer Log - Annual Leave Outstanding",
    )

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.annual_leave.json")

    assert result["all_passed"] is True

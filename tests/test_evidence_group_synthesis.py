from app.services.answer_generation_service import generate_grounded_answer
from app.services.domain_retrieval_plan_service import (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    WORKER_STORY_PLAN,
    retrieve_chunks_for_question,
)
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
    assert "LeaveType and LeaveTypeRule" in summary.sentence


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


def test_worker_story_benchmark_style_fixture_can_pass_with_complete_evidence_groups(db_session):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence and explain payroll "
        "outcomes.",
        "Developer Log - Worker Story Purpose",
    )
    _ingest(
        db_session,
        "Worker Story uses SourceTruth and source truth inclusion to show which source truth inputs are included.",
        "Developer Log - Worker Story SourceTruth",
    )
    _ingest(
        db_session,
        "Interpreted Worked Hours are shown from the current-effective interpreter run with ObjectTime grouping.",
        "Developer Log - Worker Story Interpreted Worked Hours",
    )
    _ingest(
        db_session,
        "Calculated Payroll Outcome shows the current-effective payroll output from PayRun calculation evidence.",
        "Developer Log - Worker Story Calculated Payroll Outcome",
    )
    _ingest(
        db_session,
        "Decision Story and Rate Story include DecisionEvidenceIndex and RateSourceEvidenceIndex for rate evidence.",
        "Developer Log - Worker Story Decision Rate Evidence",
    )
    _ingest(
        db_session,
        "Worker Story includes Leave and Accrual Outcome evidence for leave and accrual outcomes.",
        "Developer Log - Worker Story Leave Accrual",
    )
    _ingest(
        db_session,
        "Worker Story includes Payroll Bases & Totals evidence with payroll bases and totals.",
        "Developer Log - Worker Story Payroll Bases Totals",
    )
    _ingest(
        db_session,
        "Movement Review and PayRun Admin Queue evidence explain review and admin queue relationship.",
        "Developer Log - Worker Story Movement Review",
    )
    _ingest(
        db_session,
        "Worker Story uses current-effective truth from current-effective payroll output and current-effective "
        "interpreter run, with Correction Audit Story where corrections exist.",
        "Developer Log - Worker Story Current Effective Truth",
    )
    _ingest(
        db_session,
        "Worker Story outstanding hardening records limitations, shared Worker Story surface/component work, explicit "
        "break-treatment proof and future reusable story surfaces for evidence explanation.",
        "Developer Log - Worker Story Outstanding Hardening",
    )

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.worker_story.json")

    assert result["all_passed"] is True


def test_worker_story_answer_uses_platform_specific_concepts_and_status_caveats(db_session):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence and explain payroll "
        "outcomes.",
        "Developer Log - Worker Story Purpose",
    )
    _ingest(
        db_session,
        "Worker Story uses SourceTruth and source truth inclusion to show which source truth inputs are included.",
        "Developer Log - Worker Story SourceTruth",
    )
    _ingest(
        db_session,
        "Interpreted Worked Hours are shown from the current-effective interpreter run with ObjectTime grouping.",
        "Developer Log - Worker Story Interpreted Worked Hours",
    )
    _ingest(
        db_session,
        "Calculated Payroll Outcome shows the current-effective payroll output from PayRun calculation evidence.",
        "Developer Log - Worker Story Calculated Payroll Outcome",
    )
    _ingest(
        db_session,
        "Decision Story and Rate Story include DecisionEvidenceIndex and RateSourceEvidenceIndex for rate evidence.",
        "Developer Log - Worker Story Decision Rate Evidence",
    )
    _ingest(
        db_session,
        "Worker Story includes Leave and Accrual Outcome evidence using server-owned leave output and ledger evidence.",
        "Developer Log - Worker Story Leave Accrual",
    )
    _ingest(
        db_session,
        "Worker Story includes Payroll Bases & Totals evidence with payroll bases and totals.",
        "Developer Log - Worker Story Payroll Bases Totals",
    )
    _ingest(
        db_session,
        "Movement Review and PayRun Admin Queue evidence explain review and admin queue relationship.",
        "Developer Log - Worker Story Movement Review",
    )
    _ingest(
        db_session,
        "Worker Story uses current-effective truth from current-effective payroll output and current-effective "
        "interpreter run, with Correction Audit Story where corrections exist.",
        "Developer Log - Worker Story Current Effective Truth",
    )
    _ingest(
        db_session,
        "Worker Story outstanding hardening records limitations, shared Worker Story surface/component work, explicit "
        "break-treatment proof and future reusable story surfaces for evidence explanation.",
        "Developer Log - Worker Story Outstanding Hardening",
    )

    results = retrieve_chunks_for_question(db_session, "What is Worker Story and what evidence does it show?")
    answer, _, _, _ = generate_grounded_answer("What is Worker Story and what evidence does it show?", results)
    normalized_answer = answer.lower()

    assert "Direct summary" in answer
    assert "How the system works" in answer
    assert "Current implementation status" in answer
    assert "What remains outstanding" in answer
    assert "Evidence basis" in answer
    assert "platform evidence surface" in normalized_answer
    assert "source truth" in normalized_answer
    assert "current-effective payroll output" in normalized_answer
    assert "calculated payroll outcome" in normalized_answer
    assert "decision story" in normalized_answer
    assert "rate story" in normalized_answer
    assert "payrun admin queue" in normalized_answer or "movement review" in normalized_answer
    assert "outstanding hardening" in normalized_answer
    assert "fully production-complete" in normalized_answer
    assert "code evidence" not in normalized_answer


def test_complete_evidence_coverage_produces_direct_platform_summary(db_session):
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

    results = retrieve_chunks_for_question(db_session, "How is Annual Leave managed in the system?")
    answer, _, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", results)

    assert answer.startswith("Direct summary\nAnnual Leave is managed")
    assert "The loaded formal corpus contains usable evidence" not in answer.split("\n\n", 1)[0]
    assert "The system separates configuration, accrual, consumption, valuation, PayRun processing" in answer


def test_partial_evidence_coverage_keeps_caveats(db_session):
    _ingest(
        db_session,
        "Annual Leave configuration uses LeaveType and LeaveTypeRule in Rule Cockpit configuration.",
        "Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts LeaveLedger minutes using interpreter truth with no fallback during PayRun.",
        "Developer Log - Annual Leave Accrual",
    )
    _ingest(
        db_session,
        "Annual Leave TAKEN consumption posts LeaveLedger minutes with public holiday DeductsOnPublicHoliday handling.",
        "Developer Log - Annual Leave TAKEN",
    )

    results = retrieve_chunks_for_question(db_session, "How is Annual Leave managed in the system?")
    answer, _, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", results)

    assert "Annual Leave is partially described by the loaded formal corpus" in answer
    assert "The loaded formal corpus does not yet contain enough retrieved evidence for" in answer


def test_weak_evidence_coverage_says_corpus_is_insufficient():
    weak_result = _result(
        "Annual Leave is mentioned, but this evidence does not describe the leave management mechanisms.",
        "configuration",
    )

    answer, _, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", [weak_result])

    assert "The retrieved formal corpus is not yet sufficient to answer this at the required rich-answer standard." in answer
    assert "Unknown from the currently retrieved formal corpus." in answer

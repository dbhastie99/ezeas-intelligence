from app.services.answer_generation_service import generate_grounded_answer
from app.services.domain_retrieval_plan_service import (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    detect_domain_retrieval_plan,
    retrieve_chunks_for_question,
    retrieve_with_domain_plan,
)
from app.services.ingestion_service import ingest_file_bytes


def _ingest(
    db_session,
    text: str,
    title: str = "Developer Log - Annual Leave",
    source_type: str = "DEVELOPER_LOG",
):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=f"{title.lower().replace(' ', '-')}.txt",
        source_type=source_type,
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def test_annual_leave_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How is Annual Leave managed in the system?")

    assert plan is not None
    assert plan.plan_id == "ANNUAL_LEAVE_MANAGEMENT"


def test_annual_leave_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in ANNUAL_LEAVE_MANAGEMENT_PLAN.evidence_groups}

    assert group_ids == {
        "configuration",
        "accrual",
        "taken",
        "valuation",
        "payrun",
        "worker_story",
        "outstanding",
    }


def test_domain_retrieval_runs_group_specific_searches_and_adds_group_metadata(db_session):
    _ingest(
        db_session,
        "Configuration and rule setup\n"
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit Accrual Payment Governance.",
        title="Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Accrual basis and ledger posting\n"
        "Annual Leave accrual posts LeaveLedger minutes using interpreter truth with no fallback during PayRun.",
        title="Developer Log - Annual Leave Accrual",
    )

    results = retrieve_chunks_for_question(db_session, "How is Annual Leave managed in the system?")

    assert {result.evidence_group_id for result in results} >= {"configuration", "accrual"}
    assert all(result.domain_plan_id == "ANNUAL_LEAVE_MANAGEMENT" for result in results)
    answer, sources, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", results)
    assert "Direct summary" in answer
    assert any(source.evidence_group_label == "Configuration and rule setup" for source in sources)
    assert any(source.evidence_group_label == "Accrual basis and ledger posting" for source in sources)


def test_domain_retrieval_de_duplicates_chunks_across_groups(db_session):
    _ingest(
        db_session,
        "Annual Leave LeaveType LeaveTypeRule LeaveTypeKind Rule Cockpit accrual LeaveLedger minutes "
        "interpreter truth no fallback TAKEN public holiday DeductsOnPublicHoliday valuation basis ordinary rate "
        "PayRun Worker Story Leave and Accrual Outcome outstanding hardening Leave Source Model FIFO revaluation.",
        title="Developer Log - Annual Leave Everything",
    )

    results = retrieve_with_domain_plan(
        db=db_session,
        query="How is Annual Leave managed in the system?",
        plan=ANNUAL_LEAVE_MANAGEMENT_PLAN,
    )

    chunk_ids = [result.chunk_id for result in results]
    assert len(chunk_ids) == len(set(chunk_ids))
    assert len(results) == 1
    assert results[0].evidence_group_id == "configuration"


def test_product_domain_answer_reports_missing_groups_honestly(db_session):
    _ingest(
        db_session,
        "Annual Leave uses LeaveType and LeaveTypeRule in Rule Cockpit configuration.",
        title="Developer Log - Annual Leave Configuration Only",
    )

    results = retrieve_chunks_for_question(db_session, "How is Annual Leave managed in the system?")
    answer, _, _, _ = generate_grounded_answer("How is Annual Leave managed in the system?", results)

    assert "The loaded formal corpus does not yet contain enough retrieved evidence for" in answer
    assert "Accrual basis and ledger posting" in answer


def test_non_domain_question_uses_normal_retrieval_without_group_metadata(db_session):
    _ingest(
        db_session,
        "LLM Boundary\nMinerva must not calculate payroll and is not payroll calculation truth.",
        title="Platform Doctrine - LLM Boundary",
        source_type="PLATFORM_DOCTRINE",
    )

    results = retrieve_chunks_for_question(db_session, "What is Minerva not allowed to do?")

    assert results
    assert all(result.domain_plan_id is None for result in results)
    assert all(result.evidence_group_id is None for result in results)

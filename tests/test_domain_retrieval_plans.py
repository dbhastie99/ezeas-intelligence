from app.services.answer_generation_service import generate_grounded_answer
from app.services.domain_retrieval_plan_service import (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    COMPARISON_REMEDIATION_PLAN,
    DEDUCTIONS_OBLIGATIONS_PLAN,
    MOVEMENT_REVIEW_PLAN,
    PAYROLL_BASES_AND_TOTALS_PLAN,
    PAYRUN_ADMIN_QUEUE_PLAN,
    RETRO_REPLAY_PLAN,
    TAX_PAYG_PLAN,
    WORKER_STORY_PLAN,
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


def test_worker_story_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Worker Story and what evidence does it show?")

    assert plan is not None
    assert plan.plan_id == "WORKER_STORY"


def test_worker_story_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in WORKER_STORY_PLAN.evidence_groups}

    assert group_ids == {
        "worker_story_purpose",
        "source_truth_and_inclusion",
        "interpreted_worked_hours",
        "calculated_payroll_outcome",
        "decision_story_and_rate_story",
        "leave_and_accrual_outcome",
        "payroll_bases_and_totals",
        "movement_review_and_admin_queue",
        "current_effective_truth",
        "outstanding_hardening",
    }


def test_payroll_bases_and_totals_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What are Payroll Bases & Totals and why do they matter?")

    assert plan is not None
    assert plan.plan_id == "PAYROLL_BASES_AND_TOTALS"


def test_payroll_bases_and_totals_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PAYROLL_BASES_AND_TOTALS_PLAN.evidence_groups}

    assert group_ids == {
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


def test_payrun_admin_queue_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is the PayRun Admin Queue and what does it show?")

    assert plan is not None
    assert plan.plan_id == "PAYRUN_ADMIN_QUEUE"


def test_payrun_admin_queue_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PAYRUN_ADMIN_QUEUE_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "blockers_warnings_and_ready_actions",
        "worker_attention_and_dirty_contacts",
        "processing_and_reprocessing_actions",
        "finalisation_readiness",
        "assurance_snapshot",
        "review_surfaces_and_navigation",
        "worker_story_connection",
        "payroll_bases_connection",
        "movement_review_connection",
        "outstanding_hardening",
    }


def test_movement_review_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Movement Review and what does it show?")

    assert plan is not None
    assert plan.plan_id == "MOVEMENT_REVIEW"


def test_movement_review_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in MOVEMENT_REVIEW_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "reasonableness_not_error",
        "worker_and_organisation_lenses",
        "variance_and_comparable_periods",
        "payroll_bases_connection",
        "worker_story_connection",
        "admin_queue_connection",
        "current_effective_truth",
        "trend_only_and_threshold_treatment",
        "filters_and_return_context",
        "outstanding_hardening",
    }


def test_comparison_remediation_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Comparison / Remediation and how should it work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "COMPARISON_REMEDIATION"


def test_comparison_remediation_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in COMPARISON_REMEDIATION_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "three_lane_comparison_model",
        "primary_award_path_preservation",
        "actuals_as_external_outcome_truth",
        "comparison_policy",
        "comparison_run_and_line_evidence",
        "variance_generation_and_governance",
        "position_classification_mapping",
        "worker_story_connection",
        "admin_queue_connection",
        "movement_review_connection",
        "outstanding_hardening",
    }


def test_tax_payg_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Tax / PAYG work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "TAX_PAYG"


def test_tax_payg_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in TAX_PAYG_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "deterministic_tax_boundary",
        "tax_story_and_explainability",
        "taxable_basis_and_payroll_bases",
        "worker_tax_declaration_and_withholding_inputs",
        "payment_date_and_process_period_context",
        "pay_frequency_and_provider_support",
        "gross_to_net_and_finalised_totals",
        "supplementary_incremental_payg",
        "worker_story_and_admin_queue_connection",
        "unsupported_and_review_states",
        "outstanding_hardening",
    }


def test_deductions_obligations_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Deductions and Obligations work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "DEDUCTIONS_OBLIGATIONS"


def test_deductions_obligations_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in DEDUCTIONS_OBLIGATIONS_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "deduction_template_chain",
        "worker_deduction_instruction",
        "payrun_deduction_application_memory",
        "supplementary_deduction_memory",
        "applicability_affordability_and_priority",
        "skipped_partial_unmet_and_carry_forward",
        "obligations_and_reducing_balance_recovery",
        "negative_net_pay_governance",
        "gross_to_net_and_payment_execution",
        "worker_story_and_admin_queue_connection",
        "outstanding_hardening",
    }


def test_retro_replay_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Retro / Replay work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "RETRO_REPLAY"


def test_retro_replay_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in RETRO_REPLAY_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "attributed_period_and_paid_period_truth",
        "finalised_outcome_memory",
        "current_effective_and_historical_truth",
        "bucket_and_basis_snapshot_dependency",
        "source_change_and_dependency_detection",
        "retro_payrun_and_supplementary_distinction",
        "comparison_and_variance_connection",
        "worker_story_connection",
        "admin_queue_and_movement_review_connection",
        "audit_replay_and_non_destructive_history",
        "outstanding_hardening",
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


def test_worker_story_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Worker Story purpose\n"
        "Worker Story and Worker Calculation Story act as a Talking Payslip that explains worker evidence.",
        title="Developer Log - Worker Story Purpose",
    )
    _ingest(
        db_session,
        "Worker Story source evidence\n"
        "Worker Story uses SourceTruth and source truth inclusion to explain which inputs were included.",
        title="Developer Log - Worker Story SourceTruth",
    )
    _ingest(
        db_session,
        "Calculated Payroll Outcome\n"
        "Worker Story shows Calculated Payroll Outcome using current-effective payroll output during PayRun.",
        title="Developer Log - Worker Story Payroll Outcome",
    )

    results = retrieve_chunks_for_question(db_session, "What is Worker Story and what evidence does it show?")

    assert {result.evidence_group_id for result in results} >= {
        "worker_story_purpose",
        "source_truth_and_inclusion",
        "calculated_payroll_outcome",
    }
    assert all(result.domain_plan_id == "WORKER_STORY" for result in results)


def test_payroll_bases_and_totals_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Payroll Bases & Totals are governed payroll basis evidence for operator understanding.",
        title="Developer Log - Payroll Bases Purpose",
    )
    _ingest(
        db_session,
        "PayrollBucketDefinition bucket definition uses period definition, calendar policy and membership evidence.",
        title="Developer Log - Payroll Bucket Definition",
    )
    _ingest(
        db_session,
        "PayrollBucketResult readiness requires rebuild before bucket result evidence is trusted.",
        title="Developer Log - Payroll Bucket Result Readiness",
    )

    results = retrieve_chunks_for_question(db_session, "What are Payroll Bases & Totals and why do they matter?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "bucket_definition_and_membership",
        "readiness_and_rebuild",
    }
    assert all(result.domain_plan_id == "PAYROLL_BASES_AND_TOTALS" for result in results)


def test_payrun_admin_queue_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now, while Command Centre is the "
        "full evidence control-room surface.",
        title="Developer Log - Admin Queue Purpose",
    )
    _ingest(
        db_session,
        "PayRun Admin Queue shows blockers, warnings and ready actions with different operational meaning.",
        title="Developer Log - Admin Queue Actions",
    )
    _ingest(
        db_session,
        "Assurance Snapshot provides reasonableness review signals and assurance signals for operators.",
        title="Developer Log - Admin Queue Assurance",
    )

    results = retrieve_chunks_for_question(db_session, "What is the PayRun Admin Queue and what does it show?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "blockers_warnings_and_ready_actions",
        "assurance_snapshot",
    }
    assert all(result.domain_plan_id == "PAYRUN_ADMIN_QUEUE" for result in results)


def test_movement_review_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Movement Review is a payroll reasonableness review surface for operators.",
        title="Developer Log - Movement Review Purpose",
    )
    _ingest(
        db_session,
        "Movement Review variance uses comparable period baseline evidence and review-worthy movement.",
        title="Developer Log - Movement Review Variance",
    )
    _ingest(
        db_session,
        "Movement Review connects to Payroll Bases & Totals payroll bases and basis evidence.",
        title="Developer Log - Movement Review Payroll Bases",
    )

    results = retrieve_chunks_for_question(db_session, "What is Movement Review and what does it show?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "variance_and_comparable_periods",
        "payroll_bases_connection",
    }
    assert all(result.domain_plan_id == "MOVEMENT_REVIEW" for result in results)


def test_comparison_remediation_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Comparison / Remediation is governed comparison evidence, not a simple top-up adjustment.",
        title="Developer Log - Comparison Purpose",
    )
    _ingest(
        db_session,
        "AwardComparisonPolicy governs comparator selection, active lanes, offset policy and variance treatment.",
        title="Developer Log - Comparison Policy",
    )
    _ingest(
        db_session,
        "PayRunComparisonRun and PayRunComparisonLine provide comparison evidence before variance generation.",
        title="Developer Log - Comparison Run Line",
    )

    results = retrieve_chunks_for_question(db_session, "What is Comparison / Remediation and how should it work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "comparison_policy",
        "comparison_run_and_line_evidence",
    }
    assert all(result.domain_plan_id == "COMPARISON_REMEDIATION" for result in results)


def test_tax_payg_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Tax / PAYG is governed withholding calculation evidence, not an LLM calculation.",
        title="Developer Log - Tax PAYG Purpose",
    )
    _ingest(
        db_session,
        "TaxStory explains worker tax profile, rule pack selection, frequency conversion and audit provenance.",
        title="Developer Log - TaxStory",
    )
    _ingest(
        db_session,
        "ProcessPeriod PaymentDate and payment date provide governed derived tax context.",
        title="Developer Log - Tax Payment Date",
    )

    results = retrieve_chunks_for_question(db_session, "How should Tax / PAYG work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "tax_story_and_explainability",
        "payment_date_and_process_period_context",
    }
    assert all(result.domain_plan_id == "TAX_PAYG" for result in results)


def test_deductions_obligations_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Deductions / Obligations are governed application outcomes, not automatic raw net-pay subtraction.",
        title="Developer Log - Deductions Obligations Purpose",
    )
    _ingest(
        db_session,
        "The deduction chain is LibraryDeductionTemplate to AccountDeductionTemplate to ContactPayrollDeduction to "
        "PayRunDeductionApplication.",
        title="Developer Log - Deduction Template Chain",
    )
    _ingest(
        db_session,
        "PayRunDeductionApplication records requested, taken, skipped and unmet amounts as outcome memory.",
        title="Developer Log - Deduction Application Memory",
    )

    results = retrieve_chunks_for_question(db_session, "How should Deductions and Obligations work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "deduction_template_chain",
        "payrun_deduction_application_memory",
    }
    assert all(result.domain_plan_id == "DEDUCTIONS_OBLIGATIONS" for result in results)


def test_retro_replay_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay, not ordinary reprocessing.",
        title="Developer Log - Retro Replay Purpose",
    )
    _ingest(
        db_session,
        "Attributed-period truth and paid-period truth must remain distinct for Retro / Replay.",
        title="Developer Log - Retro Period Truth",
    )
    _ingest(
        db_session,
        "Finalised outcome memory is historical payment truth and finalised outcomes should not be silently overwritten.",
        title="Developer Log - Retro Finalised Memory",
    )

    results = retrieve_chunks_for_question(db_session, "How should Retro / Replay work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "attributed_period_and_paid_period_truth",
        "finalised_outcome_memory",
    }
    assert all(result.domain_plan_id == "RETRO_REPLAY" for result in results)

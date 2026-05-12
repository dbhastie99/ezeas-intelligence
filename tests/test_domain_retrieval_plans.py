from app.services.answer_generation_service import generate_grounded_answer
from app.services.domain_retrieval_plan_service import (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    AWARD_BUILD_EVIDENCE_PLAN,
    AWARD_POSITIONS_CLASSIFICATIONS_PLAN,
    COMPARISON_REMEDIATION_PLAN,
    CONTACTS_EMPLOYEE_APPOINTMENTS_PLAN,
    CONTACT_PAYROLL_HISTORY_PLAN,
    COSTING_GL_CONSEQUENCE_PLAN,
    DECISION_STORY_PLAN,
    DEDUCTIONS_OBLIGATIONS_PLAN,
    FINALISATION_READINESS_PLAN,
    GROSS_TO_NET_PLAN,
    IMPORTS_ACTUALS_PLAN,
    LEAVE_ACCRUAL_PROCESSING_PLAN,
    LEAVE_REQUESTS_WORKFLOW_PLAN,
    LEAVE_SOURCE_MODEL_PLAN,
    MOVEMENT_REVIEW_PLAN,
    OBJECTTIME_SOURCE_TRUTH_PLAN,
    ONCOSTS_EMPLOYER_LIABILITIES_PLAN,
    PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN,
    PAYROLL_OUTPUT_PLAN,
    PAYROLL_BASES_AND_TOTALS_PLAN,
    PAYRUN_ADMIN_QUEUE_PLAN,
    PAYMENT_EXECUTION_REMITTANCE_PLAN,
    PROCESS_PERIOD_PAYRUN_LIFECYCLE_PLAN,
    PUBLIC_HOLIDAYS_PLAN,
    RATE_SOURCE_RATE_STORY_PLAN,
    ROSTERS_PATTERNS_SCHEDULING_PLAN,
    RETRO_REPLAY_PLAN,
    TAX_PAYG_PLAN,
    WORKER_ATTENTION_ISSUE_RESOLUTION_PLAN,
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


def test_worker_attention_issue_resolution_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Worker Attention / Issue Resolution in the platform?")

    assert plan is not None
    assert plan.plan_id == "WORKER_ATTENTION_ISSUE_RESOLUTION"


def test_worker_attention_issue_resolution_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in WORKER_ATTENTION_ISSUE_RESOLUTION_PLAN.evidence_groups}

    assert group_ids == {
        "worker_attention_purpose",
        "worker_issue_model",
        "blockers_warnings_and_readiness",
        "deterministic_fix_links",
        "dirty_contact_and_reprocessing",
        "payment_allocation_readiness",
        "tax_deduction_leave_readiness",
        "negative_net_pay_and_obligations",
        "worker_story_relationship",
        "admin_queue_relationship",
        "outstanding_hardening",
    }


def test_worker_attention_issue_resolution_focused_questions_detect_domain_plan():
    questions = [
        "How does Worker Attention model worker issues?",
        "How should Worker Attention guide users to fix an issue?",
        "How does dirty contact state relate to Worker Attention?",
        "How does Worker Attention handle payment allocation and negative net pay issues?",
        "How do Worker Attention, Admin Queue and Worker Story relate?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "WORKER_ATTENTION_ISSUE_RESOLUTION"


def test_leave_requests_workflow_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Leave Requests / Leave Workflow in the platform?")

    assert plan is not None
    assert plan.plan_id == "LEAVE_REQUESTS_WORKFLOW"


def test_leave_requests_workflow_focused_questions_detect_domain_plan():
    questions = [
        "How does the Leave Request workflow move from draft to approval?",
        "How does Leave Request preview handle overlaps and shortfalls?",
        "How does the Leave Request workflow handle TAKEN leave valuation?",
        "How do Leave Requests relate to LeaveLedger posting and leave balances?",
        "How does the Leave Request workflow relate to Leave Source and applicability?",
        "How do Leave Requests connect to Worker Story, PayRun and finalisation readiness?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "LEAVE_REQUESTS_WORKFLOW"


def test_leave_requests_workflow_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in LEAVE_REQUESTS_WORKFLOW_PLAN.evidence_groups}

    assert group_ids == {
        "leave_request_purpose",
        "request_creation_and_draft_editing",
        "status_transitions_and_idempotency",
        "submission_review_approval_reopen",
        "overlap_and_shortfall_handling",
        "taken_leave_valuation_and_hard_fail",
        "leave_ledger_posting",
        "leave_source_and_applicability_relationship",
        "worker_story_and_payrun_relationship",
        "finalisation_and_readiness_relationship",
        "outstanding_hardening",
    }


def test_leave_requests_workflow_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How does leave accrue and get processed in Ezeas?": "LEAVE_ACCRUAL_PROCESSING",
        "How should Leave Accrual / Processing handle TAKEN leave valuation?": "LEAVE_ACCRUAL_PROCESSING",
        "What is the Leave Source Model and why does it matter?": "LEAVE_SOURCE_MODEL",
        "How does Leave Source and applicability determine leave output?": "LEAVE_SOURCE_MODEL",
        "What is Payroll Output in the platform?": "PAYROLL_OUTPUT",
        "How should Payroll Output show leave payment effects?": "PAYROLL_OUTPUT",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "How should Worker Story explain worker-level leave evidence?": "WORKER_STORY",
        "What is Finalisation Readiness in the platform?": "FINALISATION_READINESS",
        "How does Finalisation Readiness handle leave readiness warnings?": "FINALISATION_READINESS",
        "How does Contact Payroll History relate to leave, accrual and Worker Story?": "CONTACT_PAYROLL_HISTORY",
        "How does Contact Payroll History show historical contact leave and payroll evidence?": "CONTACT_PAYROLL_HISTORY",
        "What are Deductions / Obligations and how should they work?": "DEDUCTIONS_OBLIGATIONS",
        "How do Deductions / Obligations affect explicit net-pay deduction context?": "DEDUCTIONS_OBLIGATIONS",
        "How does Gross-to-Net move from gross earnings to net pay?": "GROSS_TO_NET",
        "How does Gross-to-Net explain explicit net pay and deduction context?": "GROSS_TO_NET",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_public_holidays_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How are Public Holidays handled in the platform?")

    assert plan is not None
    assert plan.plan_id == "PUBLIC_HOLIDAYS"


def test_public_holidays_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PUBLIC_HOLIDAYS_PLAN.evidence_groups}

    assert group_ids == {
        "public_holiday_source_and_calendar",
        "worksite_state_and_applicability_context",
        "payroll_treatment_and_decision_story",
        "leave_interaction_and_deducts_on_public_holiday",
        "worker_story_admin_queue_and_finalisation",
    }
    groups = {group.group_id: group for group in PUBLIC_HOLIDAYS_PLAN.evidence_groups}
    assert "PublicHolidayGroup" in groups["public_holiday_source_and_calendar"].query_terms
    assert "WorksitePosition" in groups["worksite_state_and_applicability_context"].query_terms
    assert "Decision Story" in groups["payroll_treatment_and_decision_story"].query_terms
    assert "DeductsOnPublicHoliday" in groups["leave_interaction_and_deducts_on_public_holiday"].query_terms
    assert "Finalisation Readiness" in groups["worker_story_admin_queue_and_finalisation"].query_terms


def test_public_holidays_framed_questions_detect_domain_plan():
    questions = [
        "How are Public Holidays handled in the platform?",
        "How does PublicHolidayGroup affect public holiday calendars?",
        "How does DeductsOnPublicHoliday affect leave on public holidays?",
        "How does public holiday payroll treatment relate to Decision Story?",
        "How does the platform know which Public Holiday applies to a worker?",
        "How do Public Holidays affect payroll treatment?",
        "How do Public Holidays affect leave requests and LeaveLedger posting?",
        "How do Public Holidays appear in Worker Story and payroll evidence?",
        "What happens if Public Holiday configuration or location context is missing?",
        "How do Public Holidays relate to employer liabilities or on-costs?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "PUBLIC_HOLIDAYS"


def test_public_holidays_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How does the Leave Request workflow move from draft to approval?": "LEAVE_REQUESTS_WORKFLOW",
        "How does Leave Request preview handle overlaps and shortfalls?": "LEAVE_REQUESTS_WORKFLOW",
        "How do Leave Requests relate to LeaveLedger posting and leave balances?": "LEAVE_REQUESTS_WORKFLOW",
        "How does leave accrue and get processed in Ezeas?": "LEAVE_ACCRUAL_PROCESSING",
        "What is the Leave Source Model and why does it matter?": "LEAVE_SOURCE_MODEL",
        "How should Payroll Output explain payroll lines?": "PAYROLL_OUTPUT",
        "How does Decision Story explain treatment decisions?": "DECISION_STORY",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "What is Finalisation Readiness in the platform?": "FINALISATION_READINESS",
        "How does Worker Attention handle blockers, warnings and fix links?": "WORKER_ATTENTION_ISSUE_RESOLUTION",
        "How should On-costs / Employer Liabilities work?": "ONCOSTS_EMPLOYER_LIABILITIES",
        "How does Process Periods / PayRun Lifecycle handle period close?": "PROCESS_PERIOD_PAYRUN_LIFECYCLE",
        "How should Contacts / Employee Appointments work?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "How does ObjectTime / Source Truth work?": "OBJECTTIME_SOURCE_TRUTH",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_rosters_patterns_scheduling_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How do Rosters, Patterns and Scheduling work in the platform?")

    assert plan is not None
    assert plan.plan_id == "ROSTERS_PATTERNS_SCHEDULING"


def test_rosters_patterns_scheduling_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in ROSTERS_PATTERNS_SCHEDULING_PLAN.evidence_groups}

    assert group_ids == {
        "roster_pattern_source_and_configuration",
        "appointment_worksite_and_applicability_context",
        "ordinary_hours_leave_basis_and_public_holiday_context",
        "payroll_interpretation_and_worker_story_relationship",
        "admin_queue_finalisation_and_readiness_relationship",
    }
    groups = {group.group_id: group for group in ROSTERS_PATTERNS_SCHEDULING_PLAN.evidence_groups}
    assert "PatternDay" in groups["roster_pattern_source_and_configuration"].query_terms
    assert "EmployeeAppointmentPattern" in groups["roster_pattern_source_and_configuration"].query_terms
    assert "WorksitePosition" in groups["appointment_worksite_and_applicability_context"].query_terms
    assert "ordinary hours" in groups["ordinary_hours_leave_basis_and_public_holiday_context"].query_terms
    assert "ObjectTime comparison" in groups["payroll_interpretation_and_worker_story_relationship"].query_terms
    assert "Finalisation Readiness" in groups["admin_queue_finalisation_and_readiness_relationship"].query_terms


def test_rosters_patterns_scheduling_framed_questions_detect_domain_plan():
    questions = [
        "How do Rosters, Patterns and Scheduling work in the platform?",
        "How does PatternDay define expected work context?",
        "How does EmployeeAppointmentPattern connect rosters to appointments?",
        "How do roster schedules support ordinary hours and leave basis minutes?",
        "How does scheduling context compare to ObjectTime actual worked time?",
        "How can missing roster pattern configuration affect readiness evidence?",
        "How does the platform use roster or pattern configuration for expected work context?",
        "How do rosters and patterns relate to Employee Appointments and Worksites?",
        "How do rosters or patterns affect ordinary hours and leave basis?",
        "How are rosters or patterns different from ObjectTime source truth?",
        "How do rosters and scheduling appear in Worker Story or payroll evidence?",
        "What happens if roster or pattern configuration is missing?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "ROSTERS_PATTERNS_SCHEDULING"


def test_rosters_patterns_scheduling_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How does ObjectTime / Source Truth work?": "OBJECTTIME_SOURCE_TRUTH",
        "How should Contacts / Employee Appointments work?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "How are Public Holidays handled in the platform?": "PUBLIC_HOLIDAYS",
        "How does leave accrue and get processed in Ezeas?": "LEAVE_ACCRUAL_PROCESSING",
        "What is the Leave Source Model and why does it matter?": "LEAVE_SOURCE_MODEL",
        "How does the Leave Request workflow move from draft to approval?": "LEAVE_REQUESTS_WORKFLOW",
        "What is Payroll Output in the platform?": "PAYROLL_OUTPUT",
        "How does Decision Story explain treatment decisions?": "DECISION_STORY",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "What is Finalisation Readiness in the platform?": "FINALISATION_READINESS",
        "How does Worker Attention handle blockers, warnings and fix links?": "WORKER_ATTENTION_ISSUE_RESOLUTION",
        "How does Process Periods / PayRun Lifecycle handle period close?": "PROCESS_PERIOD_PAYRUN_LIFECYCLE",
        "How does DeductsOnPublicHoliday affect leave on public holidays?": "PUBLIC_HOLIDAYS",
        "How does PublicHolidayGroup affect public holiday calendars?": "PUBLIC_HOLIDAYS",
        "What are Payroll Bases & Totals in the platform?": "PAYROLL_BASES_AND_TOTALS",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_award_positions_classifications_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How do Award Positions and Classifications work in the platform?")

    assert plan is not None
    assert plan.plan_id == "AWARD_POSITIONS_CLASSIFICATIONS"


def test_award_positions_classifications_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in AWARD_POSITIONS_CLASSIFICATIONS_PLAN.evidence_groups}

    assert group_ids == {
        "award_position_classification_source_and_build",
        "appointment_position_and_worksite_assignment",
        "payroll_interpretation_rate_and_decision_story",
        "comparison_remediation_and_classification_lenses",
        "worker_story_admin_queue_and_readiness_relationship",
    }
    groups = {group.group_id: group for group in AWARD_POSITIONS_CLASSIFICATIONS_PLAN.evidence_groups}
    assert "AwardPosition" in groups["award_position_classification_source_and_build"].query_terms
    assert "AwardPositionClass" in groups["award_position_classification_source_and_build"].query_terms
    assert "PositionClass" in groups["award_position_classification_source_and_build"].query_terms
    assert "EmployeeAppointment" in groups["appointment_position_and_worksite_assignment"].query_terms
    assert "WorksitePosition" in groups["appointment_position_and_worksite_assignment"].query_terms
    assert "RateSource" in groups["payroll_interpretation_rate_and_decision_story"].query_terms
    assert "Decision Story" in groups["payroll_interpretation_rate_and_decision_story"].query_terms
    assert "classification lenses" in groups["comparison_remediation_and_classification_lenses"].query_terms
    assert "Finalisation Readiness" in groups["worker_story_admin_queue_and_readiness_relationship"].query_terms


def test_award_positions_classifications_framed_questions_detect_domain_plan():
    questions = [
        "How do Award Positions and Classifications work in the platform?",
        "How are Award Positions and Award Position Classes created from award evidence?",
        "How does an Employee Appointment connect to an Award Position Class?",
        "How do classifications affect RateSource, Rate Story and payroll output?",
        "How do classifications relate to Decision Story?",
        "How do classifications work in comparison or remediation scenarios?",
        "What happens if classification evidence is missing or unresolved?",
        "How does AwardPositionClass connect to EmployeeAppointment classification?",
        "How does Award Position Class evidence relate to Worksite Position assignment?",
        "How do classification levels and pay guide class evidence support payroll interpretation?",
        "How do Award Positions connect to RateSource and Rate Story?",
        "How do classification lenses support comparison remediation?",
        "How can missing AwardPositionClass configuration affect Worker Story and readiness evidence?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "AWARD_POSITIONS_CLASSIFICATIONS"


def test_award_positions_classifications_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How should Award Build / Award Evidence handle RateSourceEvidenceIndex?": "AWARD_BUILD_EVIDENCE",
        "How should award documents and pay guides act as source evidence?": "AWARD_BUILD_EVIDENCE",
        "How should Contacts / Employee Appointments work?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "How does an Employee Appointment carry work assignment context?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "How do Rosters, Patterns and Scheduling work in the platform?": "ROSTERS_PATTERNS_SCHEDULING",
        "How does PatternDay define expected work context?": "ROSTERS_PATTERNS_SCHEDULING",
        "How does ObjectTime / Source Truth work?": "OBJECTTIME_SOURCE_TRUTH",
        "How does ObjectTime / Source Truth preserve source rows?": "OBJECTTIME_SOURCE_TRUTH",
        "How does RateSource / Rate Story explain selected rate amount?": "RATE_SOURCE_RATE_STORY",
        "How does Decision Story explain treatment decisions?": "DECISION_STORY",
        "How does Decision Story explain entitlement and treatment selection?": "DECISION_STORY",
        "What is Payroll Output in the platform?": "PAYROLL_OUTPUT",
        "What does current-effective payroll output mean?": "PAYROLL_OUTPUT",
        "How does Comparison / Remediation compare primary and comparator lanes?": "COMPARISON_REMEDIATION",
        "How should Comparison / Remediation handle comparator assessment?": "COMPARISON_REMEDIATION",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "What is Finalisation Readiness in the platform?": "FINALISATION_READINESS",
        "How should Finalisation Readiness handle readiness gates?": "FINALISATION_READINESS",
        "How does Worker Attention handle blockers, warnings and fix links?": "WORKER_ATTENTION_ISSUE_RESOLUTION",
        "How should Imports / Actuals map imported payroll evidence?": "IMPORTS_ACTUALS",
        "How should Imports / Actuals handle imported actuals and external payroll evidence?": "IMPORTS_ACTUALS",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_award_positions_classifications_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Award Positions / Classifications are governed employment classification evidence with AwardPosition, "
        "AwardPositionClass, PositionClass, classification levels, position groups, pay guide and class evidence.",
        title="Developer Log - Award Positions Classifications Source",
    )
    _ingest(
        db_session,
        "EmployeeAppointment connects through WorksitePosition, Position and Worksite assignment context to award "
        "classification without Minerva changing appointment truth.",
        title="Developer Log - Award Classification Assignment",
    )
    _ingest(
        db_session,
        "Classification context supports payroll interpretation, RateSource, Rate Story, Decision Story, Payroll "
        "Output and calculated line evidence.",
        title="Developer Log - Award Classification Payroll Story",
    )

    results = retrieve_chunks_for_question(
        db_session,
        "How do Award Positions and Classifications work in the platform?",
    )

    assert {result.evidence_group_id for result in results} >= {
        "award_position_classification_source_and_build",
        "appointment_position_and_worksite_assignment",
        "payroll_interpretation_rate_and_decision_story",
    }
    assert all(result.domain_plan_id == "AWARD_POSITIONS_CLASSIFICATIONS" for result in results)


def test_payroll_tax_workcover_wic_liability_detail_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How do Payroll Tax, WorkCover and WIC liabilities work in the platform?")

    assert plan is not None
    assert plan.plan_id == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL"


def test_payroll_tax_workcover_wic_liability_detail_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN.evidence_groups}

    assert group_ids == {
        "liability_scope_and_employer_side_boundary",
        "jurisdiction_worksite_and_state_context",
        "governed_basis_membership_and_payroll_bases",
        "rates_sources_and_liability_evidence",
        "worker_story_output_and_finalisation_relationship",
    }
    groups = {group.group_id: group for group in PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN.evidence_groups}
    assert "Payroll Tax" in groups["liability_scope_and_employer_side_boundary"].query_terms
    assert "WorkCover" in groups["liability_scope_and_employer_side_boundary"].query_terms
    assert "WIC" in groups["liability_scope_and_employer_side_boundary"].query_terms
    assert "Worksite.StateId" in groups["jurisdiction_worksite_and_state_context"].query_terms
    assert "WorksitePosition" in groups["jurisdiction_worksite_and_state_context"].query_terms
    assert "EmployeeAppointment" in groups["jurisdiction_worksite_and_state_context"].query_terms
    assert "Payroll Bases & Totals" in groups["governed_basis_membership_and_payroll_bases"].query_terms
    assert "taxable wages" in groups["governed_basis_membership_and_payroll_bases"].query_terms
    assert "liability wages" in groups["governed_basis_membership_and_payroll_bases"].query_terms
    assert "RateSource" in groups["rates_sources_and_liability_evidence"].query_terms
    assert "demo fallback" in groups["rates_sources_and_liability_evidence"].query_terms
    assert "Worker Story" in groups["worker_story_output_and_finalisation_relationship"].query_terms
    assert "Finalisation Readiness" in groups["worker_story_output_and_finalisation_relationship"].query_terms


def test_payroll_tax_workcover_wic_liability_detail_framed_questions_detect_domain_plan():
    questions = [
        "How do Payroll Tax, WorkCover and WIC liabilities work in the platform?",
        "How does PayrollTax liability use Worksite.StateId jurisdiction context?",
        "How do WorkCover and WIC liabilities relate to governed payroll bases?",
        "How do liability RateSource and date-effective rates support payroll tax?",
        "How should Worker Story show Payroll Tax WorkCover WIC liability evidence?",
        "How do taxable wages and liability wages affect WorkCover liability evidence?",
        "How does ObjectTime location support Payroll Tax WorkCover WIC jurisdiction evidence?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL"


def test_payroll_tax_workcover_wic_liability_detail_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How should On-costs / Employer Liabilities work?": "ONCOSTS_EMPLOYER_LIABILITIES",
        "What are employer liabilities in the platform?": "ONCOSTS_EMPLOYER_LIABILITIES",
        "How should Tax / PAYG handle taxable basis and gross-to-net withholding?": "TAX_PAYG",
        "How do Payroll Bases & Totals provide basis evidence?": "PAYROLL_BASES_AND_TOTALS",
        "How does Payment Execution / Remittance generate payment files?": "PAYMENT_EXECUTION_REMITTANCE",
        "How does Gross-to-Net explain net pay from payroll output?": "GROSS_TO_NET",
        "What is Payroll Output in the platform?": "PAYROLL_OUTPUT",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "What is Finalisation Readiness in the platform?": "FINALISATION_READINESS",
        "How are Public Holidays handled in the platform?": "PUBLIC_HOLIDAYS",
        "How does ObjectTime / Source Truth work?": "OBJECTTIME_SOURCE_TRUTH",
        "How should Contacts / Employee Appointments work?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "How does RateSource / Rate Story explain selected rate amount?": "RATE_SOURCE_RATE_STORY",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_payroll_tax_workcover_wic_liability_detail_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Payroll Tax, WorkCover and WIC are employer-side liabilities and employer-side liability evidence, not "
        "worker net pay, not PAYG withholding and not payment execution.",
        title="Developer Log - Payroll Tax WorkCover WIC Liability Scope",
    )
    _ingest(
        db_session,
        "Jurisdiction depends on state, Worksite.StateId, WorksitePosition, EmployeeAppointment, ObjectTime location "
        "and runtime location for Payroll Tax WorkCover WIC liability detail.",
        title="Developer Log - Payroll Tax WorkCover WIC Jurisdiction",
    )
    _ingest(
        db_session,
        "Governed basis membership, payroll basis evidence, Payroll Bases & Totals, taxable wages, liability wages, "
        "included RateTypes, excluded RateTypes and AwardRateTypes support Payroll Tax WorkCover WIC liability detail.",
        title="Developer Log - Payroll Tax WorkCover WIC Payroll Bases",
    )

    results = retrieve_chunks_for_question(
        db_session,
        "How do Payroll Tax, WorkCover and WIC liabilities work in the platform?",
    )

    assert {result.evidence_group_id for result in results} >= {
        "liability_scope_and_employer_side_boundary",
        "jurisdiction_worksite_and_state_context",
        "governed_basis_membership_and_payroll_bases",
    }
    assert all(result.domain_plan_id == "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL" for result in results)


def test_gross_to_net_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Gross-to-Net in the platform?")

    assert plan is not None
    assert plan.plan_id == "GROSS_TO_NET"


def test_gross_to_net_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in GROSS_TO_NET_PLAN.evidence_groups}

    assert group_ids == {
        "gross_to_net_purpose",
        "gross_earnings_and_payroll_output",
        "taxable_basis_and_payg",
        "deductions_and_obligations",
        "negative_net_pay",
        "net_pay_and_payment_allocation",
        "worker_story_relationship",
        "finalisation_and_payment_execution",
        "current_effective_output_truth",
        "outstanding_hardening",
    }


def test_rate_source_rate_story_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is RateSource / Rate Story in the platform?")

    assert plan is not None
    assert plan.plan_id == "RATE_SOURCE_RATE_STORY"


def test_rate_source_rate_story_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in RATE_SOURCE_RATE_STORY_PLAN.evidence_groups}

    assert group_ids == {
        "rate_story_purpose",
        "rate_source_selection",
        "rate_amount_evidence",
        "date_effective_rates",
        "award_account_class_scope",
        "pay_guide_rate_evidence",
        "rate_source_evidence_index",
        "rate_story_vs_decision_story",
        "worker_story_relationship",
        "payroll_output_and_gross_to_net_relationship",
        "outstanding_hardening",
    }


def test_rate_source_rate_story_focused_questions_detect_domain_plan():
    questions = [
        "How does Rate Story explain RateSource selection?",
        "How does Rate Story use pay guide evidence?",
        "What is the difference between RateSource / Rate Story and Decision Story?",
        "How do date-effective and scoped rates affect Rate Story?",
        "How does Rate Story relate to Worker Story and Gross-to-Net?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "RATE_SOURCE_RATE_STORY"


def test_decision_story_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Decision Story in the platform?")

    assert plan is not None
    assert plan.plan_id == "DECISION_STORY"


def test_decision_story_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in DECISION_STORY_PLAN.evidence_groups}

    assert group_ids == {
        "decision_story_purpose",
        "treatment_and_entitlement_selection",
        "decision_evidence_index",
        "award_rule_and_runtime_fact_evidence",
        "allowance_penalty_overtime_shift_evidence",
        "break_public_holiday_and_special_condition_evidence",
        "decision_story_vs_rate_story",
        "worker_story_relationship",
        "payroll_output_and_gross_to_net_relationship",
        "outstanding_hardening",
    }


def test_decision_story_focused_questions_detect_domain_plan():
    questions = [
        "How does Decision Story explain why a payroll line exists?",
        "What is DecisionEvidenceIndex used for?",
        "What is the difference between Decision Story and Rate Story for treatment and rate evidence?",
        "How does Decision Story explain allowances, penalties, overtime and shift decisions?",
        "How does Decision Story handle breaks, public holidays and special conditions?",
        "How does Decision Story relate to Worker Story and Gross-to-Net?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "DECISION_STORY"


def test_payroll_output_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Payroll Output in the platform?")

    assert plan is not None
    assert plan.plan_id == "PAYROLL_OUTPUT"


def test_payroll_output_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PAYROLL_OUTPUT_PLAN.evidence_groups}

    assert group_ids == {
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


def test_payroll_output_focused_questions_detect_domain_plan():
    questions = [
        "What does current-effective payroll output mean?",
        "What is the difference between Run Output and Process Period Output?",
        "How should Payroll Output explain payroll lines?",
        "How does Payroll Output relate to Gross-to-Net?",
        "How does Payroll Output relate to Payroll Bases & Totals?",
        "How does Payroll Output relate to finalisation and payment execution?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "PAYROLL_OUTPUT"


def test_contact_payroll_history_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is Contact Payroll History in the platform?")

    assert plan is not None
    assert plan.plan_id == "CONTACT_PAYROLL_HISTORY"


def test_contact_payroll_history_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in CONTACT_PAYROLL_HISTORY_PLAN.evidence_groups}

    assert group_ids == {
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


def test_contact_payroll_history_focused_questions_detect_domain_plan():
    questions = [
        "How does Contact Payroll History show PayRun participation?",
        "How should Contact Payroll History distinguish current and historical payroll output?",
        "How does Contact Payroll History relate to deductions, obligations and negative net pay?",
        "How does Contact Payroll History relate to tax, payment and readiness history?",
        "How does Contact Payroll History relate to leave, accrual and Worker Story?",
        "How does Contact Payroll History support retro, replay and correction context?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "CONTACT_PAYROLL_HISTORY"


def test_contact_payroll_history_routing_overlaps_keep_existing_domain_owners():
    cases = {
        "How do Contacts / Employee Appointments explain contact identity and appointment context?": "CONTACTS_EMPLOYEE_APPOINTMENTS",
        "What is Payroll Output in the platform?": "PAYROLL_OUTPUT",
        "How does Gross-to-Net move from gross earnings to net pay?": "GROSS_TO_NET",
        "What is Worker Story and what evidence does it show?": "WORKER_STORY",
        "How do Deductions / Obligations explain obligations and reducing-balance recovery?": "DEDUCTIONS_OBLIGATIONS",
        "How should Tax / PAYG explain PAYG withholding?": "TAX_PAYG",
        "How does Payment Execution / Remittance handle payment files?": "PAYMENT_EXECUTION_REMITTANCE",
        "What is Retro / Replay and how should replay work?": "RETRO_REPLAY",
        "What is Movement Review and what does it show?": "MOVEMENT_REVIEW",
        "What is the PayRun Admin Queue and what does it show?": "PAYRUN_ADMIN_QUEUE",
    }

    for question, expected_plan_id in cases.items():
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == expected_plan_id


def test_gross_to_net_focused_questions_detect_domain_plan():
    questions = [
        "How does Gross-to-Net move from gross earnings to net pay?",
        "How does Gross-to-Net relate to taxable basis and PAYG?",
        "How do deductions and obligations affect Gross-to-Net?",
        "How should Gross-to-Net explain negative net pay?",
        "How does Gross-to-Net relate to current-effective payroll output and Worker Story?",
    ]

    for question in questions:
        plan = detect_domain_retrieval_plan(question)

        assert plan is not None
        assert plan.plan_id == "GROSS_TO_NET"


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


def test_payment_execution_remittance_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Payment Execution and Remittance work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "PAYMENT_EXECUTION_REMITTANCE"


def test_payment_execution_remittance_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PAYMENT_EXECUTION_REMITTANCE_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "finalised_gross_to_net_source",
        "worker_net_pay_and_bank_allocation",
        "payment_destination_readiness",
        "negative_net_pay_and_obligation_interaction",
        "deduction_and_third_party_remittance",
        "payment_file_generation_and_period_close",
        "remittance_batching_and_reconciliation",
        "worker_attention_and_admin_queue_connection",
        "worker_story_and_audit_evidence",
        "outstanding_hardening",
    }


def test_leave_accrual_processing_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How does leave accrue and get processed in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "LEAVE_ACCRUAL_PROCESSING"


def test_leave_accrual_processing_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in LEAVE_ACCRUAL_PROCESSING_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "leave_source_truth_and_applicability",
        "accrual_basis_and_quantity",
        "payroll_output_and_calc_interpreter_source",
        "leave_type_and_rule_configuration",
        "leave_ledger_and_accrual_posting",
        "leave_valuation_basis",
        "leave_request_payment_effects",
        "payrun_processing_and_finalisation",
        "worker_story_connection",
        "payroll_bases_connection",
        "outstanding_hardening",
    }


def test_finalisation_readiness_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Finalisation Readiness work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "FINALISATION_READINESS"


def test_finalisation_readiness_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in FINALISATION_READINESS_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "blockers_warnings_and_green_state",
        "current_effective_payroll_output",
        "worker_attention_and_admin_queue",
        "payroll_bases_readiness",
        "leave_readiness",
        "tax_deduction_and_payment_readiness",
        "payment_execution_and_bank_readiness",
        "finalised_outcome_truth",
        "warning_acknowledgement_and_audit",
        "worker_story_and_review_surfaces",
        "outstanding_hardening",
    }


def test_leave_source_model_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is the Leave Source Model and why does it matter?")

    assert plan is not None
    assert plan.plan_id == "LEAVE_SOURCE_MODEL"


def test_leave_source_model_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in LEAVE_SOURCE_MODEL_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "applicability_vs_rule_content",
        "leave_type_rule_limitations",
        "contact_vs_appointment_scope",
        "source_dimensions_and_precedence",
        "leave_accrual_connection",
        "leave_request_and_payment_effects_connection",
        "worker_story_connection",
        "command_centre_and_finalisation_connection",
        "readiness_and_missing_output_detection",
        "outstanding_hardening",
    }


def test_oncosts_employer_liabilities_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should On-costs and Employer Liabilities work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "ONCOSTS_EMPLOYER_LIABILITIES"


def test_oncosts_employer_liabilities_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in ONCOSTS_EMPLOYER_LIABILITIES_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "employer_liability_not_worker_pay",
        "rate_source_and_date_effective_rates",
        "award_rate_type_and_rate_type_settings",
        "governed_basis_membership",
        "super_payroll_tax_and_workcover_wic",
        "state_worksite_and_runtime_location_resolution",
        "payrun_output_and_worker_story_connection",
        "payroll_bases_connection",
        "finalisation_and_readiness_connection",
        "demo_fallback_vs_production_truth",
        "outstanding_hardening",
    }


def test_award_build_evidence_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Award Build and Award Evidence work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "AWARD_BUILD_EVIDENCE"


def test_award_build_evidence_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in AWARD_BUILD_EVIDENCE_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "award_document_and_pay_guide_sources",
        "rate_type_and_award_rate_type_creation",
        "rate_source_and_date_effective_rate_evidence",
        "classification_position_and_class_evidence",
        "allowances_penalties_and_conditions",
        "decision_evidence_index",
        "rate_source_evidence_index",
        "worker_story_decision_and_rate_story_connection",
        "needs_configuration_and_build_status",
        "durable_award_evidence_set",
        "outstanding_hardening",
    }


def test_imports_actuals_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Imports and Actuals work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "IMPORTS_ACTUALS"


def test_imports_actuals_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in IMPORTS_ACTUALS_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "imported_timesheet_source_truth",
        "imported_payroll_actuals_lane",
        "source_system_mapping_and_validation",
        "pay_code_and_rate_type_mapping",
        "position_classification_mapping",
        "objecttime_and_source_truth_connection",
        "comparison_and_remediation_connection",
        "reconciliation_and_movement_review_connection",
        "worker_story_and_admin_queue_connection",
        "evidence_provenance_and_audit",
        "outstanding_hardening",
    }


def test_objecttime_source_truth_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("What is ObjectTime / Source Truth and why does it matter?")

    assert plan is not None
    assert plan.plan_id == "OBJECTTIME_SOURCE_TRUTH"


def test_objecttime_source_truth_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in OBJECTTIME_SOURCE_TRUTH_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "objecttime_as_source_evidence",
        "payrun_inclusion_and_source_truth",
        "imported_and_generated_source_rows",
        "source_truth_vs_worked_hours",
        "current_effective_output_connection",
        "worker_story_connection",
        "payroll_bases_and_leave_accrual_connection",
        "comparison_movement_and_replay_connection",
        "corrections_dirty_contacts_and_reprocessing",
        "evidence_provenance_and_audit",
        "outstanding_hardening",
    }


def test_contacts_employee_appointments_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Contacts and Employee Appointments work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS"


def test_contacts_employee_appointments_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in CONTACTS_EMPLOYEE_APPOINTMENTS_PLAN.evidence_groups}

    assert group_ids == {
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


def test_process_period_payrun_lifecycle_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Process Periods and PayRun Lifecycle work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "PROCESS_PERIOD_PAYRUN_LIFECYCLE"


def test_process_period_payrun_lifecycle_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in PROCESS_PERIOD_PAYRUN_LIFECYCLE_PLAN.evidence_groups}

    assert group_ids == {
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


def test_costing_gl_consequence_question_detects_domain_plan():
    plan = detect_domain_retrieval_plan("How should Costing and GL Consequence Evidence work in Ezeas?")

    assert plan is not None
    assert plan.plan_id == "COSTING_GL_CONSEQUENCE"


def test_costing_gl_consequence_plan_contains_expected_evidence_groups():
    group_ids = {group.group_id for group in COSTING_GL_CONSEQUENCE_PLAN.evidence_groups}

    assert group_ids == {
        "purpose_and_operator_meaning",
        "downstream_not_payroll_calculation_truth",
        "finalised_payroll_outcome_source",
        "payment_execution_and_remittance_connection",
        "employer_liability_and_oncost_connection",
        "deduction_obligation_and_writeoff_consequences",
        "comparison_remediation_variance_connection",
        "leave_valuation_and_accrual_connection",
        "negative_net_pay_and_out_of_pay_consequences",
        "audit_story_and_financial_evidence",
        "deferred_costing_slice_boundary",
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


def test_payment_execution_remittance_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Payment Execution / Remittance is governed payment execution and remittance evidence, not a generic file export.",
        title="Developer Log - Payment Execution Purpose",
    )
    _ingest(
        db_session,
        "Payment execution consumes finalised gross-to-net, finalised payroll outcome and payment outcome evidence, "
        "not payroll calculation truth.",
        title="Developer Log - Payment Execution Finalised Source",
    )
    _ingest(
        db_session,
        "Worker net pay requires payment allocation, bank allocation and bank instruction readiness.",
        title="Developer Log - Payment Execution Allocation",
    )

    results = retrieve_chunks_for_question(db_session, "How should Payment Execution and Remittance work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "finalised_gross_to_net_source",
        "worker_net_pay_and_bank_allocation",
    }
    assert all(result.domain_plan_id == "PAYMENT_EXECUTION_REMITTANCE" for result in results)


def test_leave_accrual_processing_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes, "
        "not Minerva calculations or generic leave policy advice.",
        title="Developer Log - Leave Accrual Processing Purpose",
    )
    _ingest(
        db_session,
        "Leave source truth and applicability govern accrual; LeaveTypeRule alone is not final applicability truth "
        "while Leave Source Model remains hardening.",
        title="Developer Log - Leave Source Applicability",
    )
    _ingest(
        db_session,
        "CalcInterpreterLine and current-effective payroll output provide canonical processed payroll result truth "
        "for leave output quantity.",
        title="Developer Log - Leave Payroll Output Source",
    )

    results = retrieve_chunks_for_question(db_session, "How does leave accrue and get processed in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "leave_source_truth_and_applicability",
        "payroll_output_and_calc_interpreter_source",
    }
    assert all(result.domain_plan_id == "LEAVE_ACCRUAL_PROCESSING" for result in results)


def test_finalisation_readiness_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Finalisation Readiness is a governed readiness gate and assurance gate, not payroll calculation truth.",
        title="Developer Log - Finalisation Readiness Purpose",
    )
    _ingest(
        db_session,
        "Finalisation Readiness uses blockers, warnings, red blockers, amber warnings and green ready state.",
        title="Developer Log - Finalisation Readiness Status",
    )
    _ingest(
        db_session,
        "Current-effective payroll output matters because stale or superseded runs must not be finalised as current truth.",
        title="Developer Log - Finalisation Current Output",
    )

    results = retrieve_chunks_for_question(db_session, "How should Finalisation Readiness work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "blockers_warnings_and_green_state",
        "current_effective_payroll_output",
    }
    assert all(result.domain_plan_id == "FINALISATION_READINESS" for result in results)


def test_leave_source_model_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Leave Source Model is the governed applicability source-truth layer for whether leave applies in worker context.",
        title="Developer Log - Leave Source Model Purpose",
    )
    _ingest(
        db_session,
        "LeaveTypeRule is policy calculation content and must not be final applicability truth.",
        title="Developer Log - Leave Source Rule Limitation",
    )
    _ingest(
        db_session,
        "Leave readiness should distinguish leave does not apply from leave output is missing.",
        title="Developer Log - Leave Source Missing Output",
    )
    _ingest(
        db_session,
        "Contact scope and EmployeeAppointment scope require appointment-aware leave handling.",
        title="Developer Log - Leave Source Scope",
    )

    results = retrieve_chunks_for_question(db_session, "What is the Leave Source Model and why does it matter?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "applicability_vs_rule_content",
        "contact_vs_appointment_scope",
    }
    assert all(result.domain_plan_id == "LEAVE_SOURCE_MODEL" for result in results)


def test_oncosts_employer_liabilities_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "On-costs and Employer Liabilities are governed employer liability evidence with operator meaning, "
        "not a reporting add-on.",
        title="Developer Log - On-costs Employer Liabilities Purpose",
    )
    _ingest(
        db_session,
        "Employer liability evidence is not worker pay, not worker net pay and not payroll calculation truth; "
        "Minerva does not calculate on-costs.",
        title="Developer Log - On-costs Worker Pay Boundary",
    )
    _ingest(
        db_session,
        "RateSource and date-effective rates should use date-effective RateSource rule-pack configuration, not "
        "application code.",
        title="Developer Log - On-costs RateSource",
    )

    results = retrieve_chunks_for_question(db_session, "How should On-costs and Employer Liabilities work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "employer_liability_not_worker_pay",
        "rate_source_and_date_effective_rates",
    }
    assert all(result.domain_plan_id == "ONCOSTS_EMPLOYER_LIABILITIES" for result in results)


def test_award_build_evidence_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Award Build and Award Evidence are governed configuration and traceable evidence, not runtime payroll "
        "calculation.",
        title="Developer Log - Award Build Purpose",
    )
    _ingest(
        db_session,
        "Award document and pay guide evidence provide source evidence with row column page evidence.",
        title="Developer Log - Award Pay Guide Sources",
    )
    _ingest(
        db_session,
        "RateType is the stable conceptual pay type and AwardRateType is award-scoped treatment.",
        title="Developer Log - Award Rate Types",
    )

    results = retrieve_chunks_for_question(db_session, "How should Award Build and Award Evidence work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "award_document_and_pay_guide_sources",
        "rate_type_and_award_rate_type_creation",
    }
    assert all(result.domain_plan_id == "AWARD_BUILD_EVIDENCE" for result in results)


def test_imports_actuals_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Imports / Actuals and Imports and Actuals are governed imported evidence and external source evidence, "
        "not calculated interpreter truth.",
        title="Developer Log - Imports Actuals Purpose",
    )
    _ingest(
        db_session,
        "Imported timesheets can become ObjectTime work evidence and timesheet source truth only after validation "
        "and mapping.",
        title="Developer Log - Imported Timesheets",
    )
    _ingest(
        db_session,
        "Imported payroll actuals and payroll actuals live in an actuals lane and external outcome lane, separate "
        "from calculated interpreter output.",
        title="Developer Log - Imported Payroll Actuals",
    )

    results = retrieve_chunks_for_question(db_session, "How should Imports and Actuals work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "imported_timesheet_source_truth",
        "imported_payroll_actuals_lane",
    }
    assert all(result.domain_plan_id == "IMPORTS_ACTUALS" for result in results)


def test_imports_actuals_detection_does_not_steal_comparison_remediation_imported_actuals_question():
    plan = detect_domain_retrieval_plan("Why are imported actuals treated as external outcome truth?")

    assert plan is not None
    assert plan.plan_id == "COMPARISON_REMEDIATION"


def test_imports_actuals_interpreter_truth_question_routes_to_imports_actuals():
    plan = detect_domain_retrieval_plan(
        "Why are imported actuals external outcome truth rather than calculated interpreter truth?"
    )

    assert plan is not None
    assert plan.plan_id == "IMPORTS_ACTUALS"


def test_objecttime_source_truth_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "ObjectTime / Source Truth and ObjectTime Source Truth are governed source evidence, not payroll "
        "calculation truth.",
        title="Developer Log - ObjectTime Source Truth Purpose",
    )
    _ingest(
        db_session,
        "ObjectTime source evidence preserves source row and inclusion context for work time.",
        title="Developer Log - ObjectTime Source Evidence",
    )
    _ingest(
        db_session,
        "PayRun inclusion uses SourceTruth and Source Truth source inclusion to explain why a source row belongs "
        "in a PayRun.",
        title="Developer Log - ObjectTime PayRun Inclusion",
    )

    results = retrieve_chunks_for_question(db_session, "What is ObjectTime / Source Truth and why does it matter?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "objecttime_as_source_evidence",
        "payrun_inclusion_and_source_truth",
    }
    assert all(result.domain_plan_id == "OBJECTTIME_SOURCE_TRUTH" for result in results)


def test_objecttime_source_truth_detection_does_not_steal_imports_actuals_objecttime_question():
    plan = detect_domain_retrieval_plan("How do Imports / Actuals connect to ObjectTime and source truth?")

    assert plan is not None
    assert plan.plan_id == "IMPORTS_ACTUALS"


def test_objecttime_source_truth_detection_does_not_steal_leave_source_truth_question():
    plan = detect_domain_retrieval_plan("What source truth should leave accrual use?")

    assert plan is not None
    assert plan.plan_id == "LEAVE_ACCRUAL_PROCESSING"


def test_contacts_employee_appointments_detection_does_not_steal_admin_queue_dirty_contact_question():
    plan = detect_domain_retrieval_plan("How do Worker Attention and dirty contacts relate to the PayRun Admin Queue?")

    assert plan is not None
    assert plan.plan_id == "PAYRUN_ADMIN_QUEUE"


def test_worker_attention_issue_resolution_detection_keeps_overlapping_domain_ownership():
    admin_plan = detect_domain_retrieval_plan("How do Worker Attention and dirty contacts relate to the PayRun Admin Queue?")
    contacts_plan = detect_domain_retrieval_plan("How should Worker Attention use Contact and EmployeeAppointment readiness?")

    assert admin_plan is not None
    assert admin_plan.plan_id == "PAYRUN_ADMIN_QUEUE"
    assert contacts_plan is not None
    assert contacts_plan.plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS"


def test_gross_to_net_detection_keeps_overlapping_domain_ownership():
    tax_plan = detect_domain_retrieval_plan("How should Tax / PAYG handle taxable basis and gross-to-net withholding?")
    deduction_plan = detect_domain_retrieval_plan("How do Deductions / Obligations affect gross-to-net deductions?")
    payment_plan = detect_domain_retrieval_plan("How does Payment Execution / Remittance use gross-to-net net pay?")
    worker_attention_plan = detect_domain_retrieval_plan("How does Worker Attention handle gross-to-net negative net pay issues?")
    payroll_bases_plan = detect_domain_retrieval_plan("How do Payroll Bases & Totals provide gross basis evidence?")

    assert tax_plan is not None
    assert tax_plan.plan_id == "TAX_PAYG"
    assert deduction_plan is not None
    assert deduction_plan.plan_id == "DEDUCTIONS_OBLIGATIONS"
    assert payment_plan is not None
    assert payment_plan.plan_id == "PAYMENT_EXECUTION_REMITTANCE"
    assert worker_attention_plan is not None
    assert worker_attention_plan.plan_id == "WORKER_ATTENTION_ISSUE_RESOLUTION"
    assert payroll_bases_plan is not None
    assert payroll_bases_plan.plan_id == "PAYROLL_BASES_AND_TOTALS"


def test_rate_source_rate_story_detection_keeps_overlapping_domain_ownership():
    decision_plan = detect_domain_retrieval_plan("How does Decision Story explain entitlement and treatment selection?")
    award_plan = detect_domain_retrieval_plan("How should Award Build / Award Evidence handle RateSourceEvidenceIndex?")
    gross_to_net_plan = detect_domain_retrieval_plan("How does Gross-to-Net use rate amount in payroll output?")
    payroll_bases_plan = detect_domain_retrieval_plan("How do Payroll Bases & Totals use RateType basis evidence?")
    worker_story_plan = detect_domain_retrieval_plan("What is Worker Story and how does it show Rate Story?")
    tax_plan = detect_domain_retrieval_plan("How should Tax / PAYG handle RateSource withholding context?")
    oncost_plan = detect_domain_retrieval_plan("How should On-costs use RateSource and date-effective rates?")

    assert decision_plan is not None
    assert decision_plan.plan_id == "DECISION_STORY"
    assert award_plan is not None
    assert award_plan.plan_id == "AWARD_BUILD_EVIDENCE"
    assert gross_to_net_plan is not None
    assert gross_to_net_plan.plan_id == "GROSS_TO_NET"
    assert payroll_bases_plan is not None
    assert payroll_bases_plan.plan_id == "PAYROLL_BASES_AND_TOTALS"
    assert worker_story_plan is not None
    assert worker_story_plan.plan_id == "WORKER_STORY"
    assert tax_plan is not None
    assert tax_plan.plan_id == "TAX_PAYG"
    assert oncost_plan is not None
    assert oncost_plan.plan_id == "ONCOSTS_EMPLOYER_LIABILITIES"


def test_decision_story_detection_keeps_overlapping_domain_ownership():
    rate_plan = detect_domain_retrieval_plan("How does RateSource / Rate Story explain selected rate amount?")
    worker_story_plan = detect_domain_retrieval_plan("What is Worker Story and how does it show Decision Story?")
    award_plan = detect_domain_retrieval_plan("How should Award Build / Award Evidence handle DecisionEvidenceIndex?")
    gross_to_net_plan = detect_domain_retrieval_plan("How does Gross-to-Net use calculated payroll outcome lines?")
    payroll_bases_plan = detect_domain_retrieval_plan("How do Payroll Bases & Totals provide basis evidence?")
    leave_plan = detect_domain_retrieval_plan("How does Leave Accrual / Processing calculate leave processing evidence?")
    finalisation_plan = detect_domain_retrieval_plan("How should Finalisation Readiness handle readiness gates?")

    assert rate_plan is not None
    assert rate_plan.plan_id == "RATE_SOURCE_RATE_STORY"
    assert worker_story_plan is not None
    assert worker_story_plan.plan_id == "WORKER_STORY"
    assert award_plan is not None
    assert award_plan.plan_id == "AWARD_BUILD_EVIDENCE"
    assert gross_to_net_plan is not None
    assert gross_to_net_plan.plan_id == "GROSS_TO_NET"
    assert payroll_bases_plan is not None
    assert payroll_bases_plan.plan_id == "PAYROLL_BASES_AND_TOTALS"
    assert leave_plan is not None
    assert leave_plan.plan_id == "LEAVE_ACCRUAL_PROCESSING"
    assert finalisation_plan is not None
    assert finalisation_plan.plan_id == "FINALISATION_READINESS"


def test_payroll_output_detection_keeps_overlapping_domain_ownership():
    gross_to_net_plan = detect_domain_retrieval_plan("How does Gross-to-Net explain net pay from payroll output?")
    worker_story_plan = detect_domain_retrieval_plan("What is Worker Story and how does it show payroll output?")
    decision_plan = detect_domain_retrieval_plan("How does Decision Story explain why a payroll line exists?")
    rate_plan = detect_domain_retrieval_plan("How does RateSource / Rate Story explain selected rate amount?")
    payroll_bases_plan = detect_domain_retrieval_plan("How do Payroll Bases & Totals provide basis evidence?")
    finalisation_plan = detect_domain_retrieval_plan("How should Finalisation Readiness handle readiness gates?")
    payment_plan = detect_domain_retrieval_plan("How does Payment Execution / Remittance generate payment files?")
    admin_queue_plan = detect_domain_retrieval_plan("How does the PayRun Admin Queue show actions for payroll output issues?")

    assert gross_to_net_plan is not None
    assert gross_to_net_plan.plan_id == "GROSS_TO_NET"
    assert worker_story_plan is not None
    assert worker_story_plan.plan_id == "WORKER_STORY"
    assert decision_plan is not None
    assert decision_plan.plan_id == "DECISION_STORY"
    assert rate_plan is not None
    assert rate_plan.plan_id == "RATE_SOURCE_RATE_STORY"
    assert payroll_bases_plan is not None
    assert payroll_bases_plan.plan_id == "PAYROLL_BASES_AND_TOTALS"
    assert finalisation_plan is not None
    assert finalisation_plan.plan_id == "FINALISATION_READINESS"
    assert payment_plan is not None
    assert payment_plan.plan_id == "PAYMENT_EXECUTION_REMITTANCE"
    assert admin_queue_plan is not None
    assert admin_queue_plan.plan_id == "PAYRUN_ADMIN_QUEUE"


def test_contacts_employee_appointments_objecttime_question_routes_to_contacts_when_contacts_framed():
    plan = detect_domain_retrieval_plan("How do Contacts and Employee Appointments relate to ObjectTime / Source Truth?")

    assert plan is not None
    assert plan.plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS"


def test_contacts_employee_appointments_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Contacts / Employee Appointments use Contact and EmployeeAppointment as governed worker identity context "
        "and employment context, not payroll calculation truth.",
        title="Developer Log - Contacts Appointments Purpose",
    )
    _ingest(
        db_session,
        "Contact is worker identity, person payroll identity, worker context and payroll identity context.",
        title="Developer Log - Contacts Identity",
    )
    _ingest(
        db_session,
        "EmployeeAppointment and Employee Appointment are the employment assignment and work assignment, carrying "
        "position worksite classification award context.",
        title="Developer Log - Employee Appointment Assignment",
    )

    results = retrieve_chunks_for_question(db_session, "How should Contacts and Employee Appointments work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "contact_identity_and_worker_context",
        "employee_appointment_as_employment_assignment",
    }
    assert all(result.domain_plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS" for result in results)


def test_process_period_payrun_lifecycle_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context and "
        "payment-event lifecycle evidence, not payroll calculation truth or a generic date range.",
        title="Developer Log - Process Period Lifecycle Purpose",
    )
    _ingest(
        db_session,
        "ProcessPeriod and Process Period use ProcessPeriodGroup and Process Period Group for recurring calendar "
        "policy and payment policy context.",
        title="Developer Log - Process Period Group Context",
    )
    _ingest(
        db_session,
        "PayRun creation and PayRun admission happen inside process-period context, but admission is not processing.",
        title="Developer Log - PayRun Creation Admission",
    )

    results = retrieve_chunks_for_question(
        db_session,
        "How should Process Periods and PayRun Lifecycle work in Ezeas?",
    )

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "process_period_and_group_context",
        "payrun_creation_and_admission",
    }
    assert all(result.domain_plan_id == "PROCESS_PERIOD_PAYRUN_LIFECYCLE" for result in results)


def test_process_period_payrun_lifecycle_detection_does_not_steal_tax_paymentdate_question():
    plan = detect_domain_retrieval_plan("Why does ProcessPeriod PaymentDate matter for Tax / PAYG?")

    assert plan is not None
    assert plan.plan_id == "TAX_PAYG"


def test_costing_gl_consequence_domain_retrieval_uses_group_specific_evidence(db_session):
    _ingest(
        db_session,
        "Costing / GL Consequence Evidence is downstream financial consequence evidence, not payroll calculation truth.",
        title="Developer Log - Costing Purpose",
    )
    _ingest(
        db_session,
        "Finalised payroll outcome and finalised gross-to-net are source outcome evidence for costing status.",
        title="Developer Log - Costing Finalised Outcome",
    )
    _ingest(
        db_session,
        "Obligation write-off and obligation writeoff events may need GL/provision/costing treatment.",
        title="Developer Log - Costing Obligation Writeoff",
    )

    results = retrieve_chunks_for_question(db_session, "How should Costing and GL Consequence Evidence work in Ezeas?")

    assert {result.evidence_group_id for result in results} >= {
        "purpose_and_operator_meaning",
        "finalised_payroll_outcome_source",
        "deduction_obligation_and_writeoff_consequences",
    }
    assert all(result.domain_plan_id == "COSTING_GL_CONSEQUENCE" for result in results)

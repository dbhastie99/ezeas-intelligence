from dataclasses import dataclass

from app.services.domain_retrieval_plan_service import DomainRetrievalPlan, EvidenceGroup
from app.services.knowledge_retrieval_service import RetrievalResult
from app.utils.term_normalization import contains_normalized_term


@dataclass(frozen=True)
class EvidenceGroupSummary:
    group_id: str
    label: str
    sentence: str
    detected_terms: list[str]
    is_weak: bool


GROUP_KEY_TERMS = {
    "configuration": (
        "Annual Leave",
        "LeaveType",
        "LeaveTypeRule",
        "LeaveTypeKind",
        "Rule Cockpit",
        "Accrual",
        "Payment",
        "Governance",
    ),
    "accrual": (
        "Annual Leave",
        "accrual",
        "LeaveLedger",
        "minutes",
        "interpreter truth",
        "no fallback",
        "process period",
        "PayRun",
    ),
    "taken": (
        "Annual Leave",
        "TAKEN",
        "LeaveLedger",
        "minutes",
        "public holiday",
        "DeductsOnPublicHoliday",
        "skip",
        "resolver",
    ),
    "valuation": (
        "Annual Leave",
        "valuation",
        "valuation basis",
        "ordinary rate",
        "PayRun",
        "snapshot",
        "liability",
    ),
    "payrun": (
        "PayRun",
        "Generate Leave Accruals on Process",
        "leave accruals",
        "valuation basis",
        "processing",
        "Admin Queue",
    ),
    "worker_story": (
        "Worker Story",
        "Leave and Accrual Outcome",
        "server-owned leave output",
        "ledger",
        "valuation basis",
        "evidence chain",
    ),
    "outstanding": (
        "Annual Leave",
        "outstanding",
        "hardening",
        "Leave Source Model",
        "FIFO",
        "lot consumption",
        "revaluation",
        "production hardening",
    ),
    "worker_story_purpose": ("Worker Story", "Worker Calculation Story", "Talking Payslip", "worker evidence", "explain"),
    "source_truth_and_inclusion": ("Worker Story", "SourceTruth", "Source truth", "inclusion", "source truth"),
    "interpreted_worked_hours": (
        "Worker Story",
        "Interpreted Worked Hours",
        "current-effective interpreter run",
        "ObjectTime grouping",
    ),
    "calculated_payroll_outcome": (
        "Worker Story",
        "Calculated Payroll Outcome",
        "current-effective payroll output",
        "PayRun",
        "quantity",
        "rate",
        "amount",
        "line proof",
    ),
    "decision_story_and_rate_story": (
        "Decision Story",
        "Rate Story",
        "DecisionEvidenceIndex",
        "RateSourceEvidenceIndex",
        "rate evidence",
    ),
    "leave_and_accrual_outcome": ("Worker Story", "Leave and Accrual Outcome", "leave", "accrual", "evidence"),
    "payroll_bases_and_totals": ("Worker Story", "Payroll Bases & Totals", "payroll bases", "totals", "evidence"),
    "movement_review_and_admin_queue": ("Movement Review", "PayRun Admin Queue", "Admin Queue", "PayRun"),
    "purpose_and_operator_meaning": (
        "Payroll Bases & Totals",
        "Payroll Bases and Totals",
        "governed payroll basis evidence",
        "operator",
        "basis evidence",
    ),
    "bucket_definition_and_membership": (
        "PayrollBucketDefinition",
        "Payroll Bucket Definition",
        "bucket definition",
        "period definition",
        "calendar policy",
        "membership",
    ),
    "worked_hours_and_quantity": ("worked hours", "quantity", "minutes", "hours", "basis quantity"),
    "gross_ordinary_superable_taxable_bases": (
        "gross basis",
        "ordinary basis",
        "superable basis",
        "taxable basis",
        "payroll tax",
        "WIC",
        "PAYG",
    ),
    "current_effective_truth": (
        "current-effective truth",
        "current-effective payroll output",
        "current-effective interpreter run",
        "Correction Audit Story",
        "current effective",
        "stale",
        "source truth",
    ),
    "readiness_and_rebuild": ("PayrollBucketResult", "Payroll Bucket Result", "readiness", "stale rows", "rebuild"),
    "worker_story_connection": ("Payroll Bases & Totals", "Worker Story", "Worker Calculation Story", "worker evidence"),
    "movement_review_connection": ("Payroll Bases & Totals", "Movement Review", "PayRun Admin Queue", "operator review"),
    "outstanding_hardening": (
        "Worker Story",
        "Payroll Bases & Totals",
        "outstanding hardening",
        "limitations",
        "future work",
        "hardening",
        "bucket lifecycle",
        "versioning",
    ),
}

GROUP_SIGNAL_TERMS = {
    "configuration": ("LeaveType", "LeaveTypeRule", "LeaveTypeKind", "Rule Cockpit"),
    "accrual": ("accrual", "LeaveLedger", "minutes", "interpreter truth", "no fallback"),
    "taken": ("TAKEN", "DeductsOnPublicHoliday", "public holiday", "minutes"),
    "valuation": ("valuation", "valuation basis", "ordinary rate", "snapshot", "liability"),
    "payrun": ("PayRun", "Generate Leave Accruals on Process", "leave accruals", "Admin Queue"),
    "worker_story": ("Worker Story", "Leave and Accrual Outcome", "server-owned leave output", "evidence chain"),
    "outstanding": ("outstanding", "hardening", "Leave Source Model", "FIFO", "lot consumption", "revaluation"),
    "worker_story_purpose": ("Worker Story", "Worker Calculation Story", "Talking Payslip"),
    "source_truth_and_inclusion": ("SourceTruth", "Source truth", "inclusion"),
    "interpreted_worked_hours": ("Interpreted Worked Hours", "current-effective interpreter run", "ObjectTime grouping"),
    "calculated_payroll_outcome": ("Calculated Payroll Outcome", "current-effective payroll output", "line proof"),
    "decision_story_and_rate_story": ("Decision Story", "Rate Story", "DecisionEvidenceIndex", "RateSourceEvidenceIndex"),
    "leave_and_accrual_outcome": ("Leave and Accrual Outcome", "leave", "accrual"),
    "payroll_bases_and_totals": ("Payroll Bases & Totals", "payroll bases", "totals"),
    "movement_review_and_admin_queue": ("Movement Review", "PayRun Admin Queue", "Admin Queue"),
    "purpose_and_operator_meaning": ("Payroll Bases & Totals", "Payroll Bases and Totals", "governed payroll basis evidence"),
    "bucket_definition_and_membership": ("PayrollBucketDefinition", "bucket definition", "period definition", "membership"),
    "worked_hours_and_quantity": ("worked hours", "quantity", "basis quantity"),
    "gross_ordinary_superable_taxable_bases": ("gross basis", "ordinary basis", "superable basis", "taxable basis"),
    "current_effective_truth": ("current-effective truth", "current-effective payroll output", "current-effective interpreter run"),
    "readiness_and_rebuild": ("PayrollBucketResult", "readiness", "stale rows", "rebuild"),
    "worker_story_connection": ("Payroll Bases & Totals", "Worker Story", "Worker Calculation Story"),
    "movement_review_connection": ("Payroll Bases & Totals", "Movement Review", "PayRun Admin Queue"),
    "outstanding_hardening": ("outstanding hardening", "limitations", "hardening", "bucket lifecycle", "versioning"),
}

PAYRUN_ADMIN_QUEUE_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "PayRun Admin Queue",
        "Admin Queue",
        "PayRun Queue",
        "operator workbench",
        "what needs action now",
        "Command Centre",
    ),
    "blockers_warnings_and_ready_actions": (
        "blockers",
        "warnings",
        "ready actions",
        "amber warnings",
        "operational meaning",
    ),
    "worker_attention_and_dirty_contacts": (
        "Worker Attention",
        "worker attention",
        "dirty contacts",
        "contact changes",
        "action workflow",
    ),
    "processing_and_reprocessing_actions": (
        "processing actions",
        "reprocessing actions",
        "reprocess",
        "deterministic services",
        "calculation truth",
    ),
    "finalisation_readiness": ("finalisation readiness", "finalisation", "blockers", "warnings", "amber warnings"),
    "assurance_snapshot": (
        "Assurance Snapshot",
        "reasonableness",
        "review signals",
        "assurance signals",
        "thresholds",
        "calculation truth",
    ),
    "review_surfaces_and_navigation": (
        "review surfaces",
        "navigation",
        "Worker Story",
        "Payroll Bases & Totals",
        "Movement Review",
        "PayRun Output",
        "Command Centre",
    ),
    "worker_story_connection": ("PayRun Admin Queue", "Worker Story", "Worker Calculation Story", "worker evidence"),
    "payroll_bases_connection": ("PayRun Admin Queue", "Payroll Bases & Totals", "payroll bases", "basis evidence"),
    "movement_review_connection": ("PayRun Admin Queue", "Movement Review", "operator review", "movement evidence"),
    "outstanding_hardening": (
        "PayRun Admin Queue",
        "outstanding hardening",
        "server-owned operation tracker",
        "global queue resolver",
        "reusable Worker Story surface",
        "governed assurance thresholds",
        "warning acknowledgement",
    ),
}

PAYRUN_ADMIN_QUEUE_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("PayRun Admin Queue", "Admin Queue", "operator workbench", "what needs action now"),
    "blockers_warnings_and_ready_actions": ("blockers", "warnings", "ready actions"),
    "worker_attention_and_dirty_contacts": ("Worker Attention", "dirty contacts", "contact changes"),
    "processing_and_reprocessing_actions": ("processing actions", "reprocessing actions", "reprocess"),
    "finalisation_readiness": ("finalisation readiness", "finalisation", "blockers", "warnings"),
    "assurance_snapshot": ("Assurance Snapshot", "reasonableness", "review signals", "assurance signals"),
    "review_surfaces_and_navigation": ("review surfaces", "navigation", "PayRun Output", "Command Centre"),
    "worker_story_connection": ("PayRun Admin Queue", "Worker Story", "Worker Calculation Story"),
    "payroll_bases_connection": ("PayRun Admin Queue", "Payroll Bases & Totals", "payroll bases"),
    "movement_review_connection": ("PayRun Admin Queue", "Movement Review", "operator review"),
    "outstanding_hardening": ("outstanding hardening", "server-owned operation tracker", "global queue resolver"),
}

MOVEMENT_REVIEW_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Movement Review",
        "Payroll Movement Review",
        "reasonableness",
        "review surface",
        "operator",
    ),
    "reasonableness_not_error": ("reasonableness", "not automatic proof", "variance", "payroll is wrong"),
    "worker_and_organisation_lenses": ("worker lens", "organisation lens", "worker-level", "organisation-level"),
    "variance_and_comparable_periods": ("variance", "comparable period", "baseline evidence", "review-worthy"),
    "payroll_bases_connection": ("Movement Review", "Payroll Bases & Totals", "payroll bases", "basis evidence"),
    "worker_story_connection": ("Movement Review", "Worker Story", "worker-level drill-through", "worker evidence"),
    "admin_queue_connection": ("Movement Review", "PayRun Admin Queue", "Admin Queue", "review actions"),
    "current_effective_truth": (
        "current-effective payroll",
        "current-effective truth",
        "bucket source truth",
        "stale bucket",
    ),
    "trend_only_and_threshold_treatment": (
        "trend-only",
        "rolling average",
        "YTD",
        "thresholds",
        "current-period blockers",
    ),
    "filters_and_return_context": ("filters", "filtered lenses", "return context", "all-worker views", "audit"),
    "outstanding_hardening": (
        "Movement Review",
        "outstanding hardening",
        "Movement Review Policy",
        "thresholds",
        "comparable period rules",
        "historical bucket rebuild governance",
    ),
}

MOVEMENT_REVIEW_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Movement Review", "Payroll Movement Review", "reasonableness", "review surface"),
    "reasonableness_not_error": ("reasonableness", "not automatic proof", "variance"),
    "worker_and_organisation_lenses": ("worker lens", "organisation lens", "worker-level", "organisation-level"),
    "variance_and_comparable_periods": ("variance", "comparable period", "baseline evidence", "review-worthy"),
    "payroll_bases_connection": ("Movement Review", "Payroll Bases & Totals", "payroll bases"),
    "worker_story_connection": ("Movement Review", "Worker Story", "worker-level drill-through"),
    "admin_queue_connection": ("Movement Review", "PayRun Admin Queue", "Admin Queue", "review actions"),
    "current_effective_truth": ("current-effective payroll", "current-effective truth", "bucket source truth"),
    "trend_only_and_threshold_treatment": ("trend-only", "rolling average", "YTD", "thresholds"),
    "filters_and_return_context": ("filters", "filtered lenses", "return context", "all-worker views"),
    "outstanding_hardening": ("outstanding hardening", "Movement Review Policy", "comparable period rules"),
}

COMPARISON_REMEDIATION_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Comparison / Remediation",
        "Comparison Remediation",
        "governed comparison",
        "remediation",
        "top-up",
    ),
    "three_lane_comparison_model": (
        "primary calculated",
        "comparator calculated",
        "actual imported",
        "actuals lane",
        "three lane",
    ),
    "primary_award_path_preservation": (
        "ObjectTime",
        "EmployeeAppointment",
        "AwardPositionClass",
        "primary award path",
        "operational payroll truth",
    ),
    "actuals_as_external_outcome_truth": (
        "imported actuals",
        "actuals lane",
        "external outcome truth",
        "imported actual payroll truth",
    ),
    "comparison_policy": (
        "AwardComparisonPolicy",
        "Award Comparison Policy",
        "comparator selection",
        "active lanes",
        "grain",
        "offset policy",
        "review requirements",
        "variance treatment",
    ),
    "comparison_run_and_line_evidence": (
        "PayRunComparisonRun",
        "PayRun Comparison Run",
        "PayRunComparisonLine",
        "PayRun Comparison Line",
        "comparison evidence",
    ),
    "variance_generation_and_governance": (
        "PayRunVarianceLine",
        "PayRun Variance Line",
        "variance line",
        "remediation top-up",
        "typed",
        "explainable",
    ),
    "position_classification_mapping": (
        "AwardPositionClassComparisonMap",
        "EmployeeAppointmentAwardClassAssignment",
        "ObjectTimeClassificationResolution",
        "comparator classification",
        "classification lens",
    ),
    "worker_story_connection": ("Comparison / Remediation", "Worker Story", "comparison chapter", "worker evidence"),
    "admin_queue_connection": (
        "Comparison / Remediation",
        "PayRun Admin Queue",
        "missing policy",
        "unmapped actuals",
        "variance review actions",
    ),
    "movement_review_connection": (
        "Comparison / Remediation",
        "Movement Review",
        "variance",
        "comparison outcomes",
        "not automatic proof of error",
    ),
    "outstanding_hardening": (
        "Comparison / Remediation",
        "outstanding hardening",
        "design doctrine",
        "not yet implemented",
        "full runtime capability",
        "future work",
    ),
}

COMPARISON_REMEDIATION_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Comparison / Remediation", "Comparison Remediation", "governed comparison"),
    "three_lane_comparison_model": ("primary calculated", "comparator calculated", "actual imported", "actuals lane"),
    "primary_award_path_preservation": ("ObjectTime", "EmployeeAppointment", "AwardPositionClass", "primary award path"),
    "actuals_as_external_outcome_truth": ("imported actuals", "actuals lane", "external outcome truth"),
    "comparison_policy": ("AwardComparisonPolicy", "Award Comparison Policy", "comparator selection", "active lanes"),
    "comparison_run_and_line_evidence": ("PayRunComparisonRun", "PayRunComparisonLine", "comparison evidence"),
    "variance_generation_and_governance": ("PayRunVarianceLine", "variance line", "remediation top-up"),
    "position_classification_mapping": (
        "AwardPositionClassComparisonMap",
        "EmployeeAppointmentAwardClassAssignment",
        "ObjectTimeClassificationResolution",
        "comparator classification",
    ),
    "worker_story_connection": ("Comparison / Remediation", "Worker Story", "comparison chapter"),
    "admin_queue_connection": ("Comparison / Remediation", "PayRun Admin Queue", "missing policy", "unmapped actuals"),
    "movement_review_connection": ("Comparison / Remediation", "Movement Review", "comparison outcomes"),
    "outstanding_hardening": ("outstanding hardening", "design doctrine", "not yet implemented"),
}

TAX_PAYG_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Tax / PAYG",
        "PAYG withholding",
        "governed withholding calculation evidence",
        "tax evidence",
    ),
    "deterministic_tax_boundary": ("deterministic services", "tax providers", "withholding calculation", "Minerva explains"),
    "tax_story_and_explainability": (
        "TaxStory",
        "Tax Story",
        "source truth",
        "worker tax profile",
        "payroll context",
        "rule pack selection",
        "component selection",
        "frequency conversion",
        "band formula calculation",
        "rounding",
        "net-pay effect",
        "audit provenance",
    ),
    "taxable_basis_and_payroll_bases": (
        "taxable basis",
        "taxable earnings",
        "Payroll Bases & Totals",
        "governed basis membership",
        "raw flags",
    ),
    "worker_tax_declaration_and_withholding_inputs": (
        "worker tax declaration",
        "withholding instruction",
        "withholding inputs",
        "tax profile",
        "calculation readiness",
    ),
    "payment_date_and_process_period_context": (
        "ProcessPeriod PaymentDate",
        "payment date",
        "process period",
        "tax context",
        "governed derived",
    ),
    "pay_frequency_and_provider_support": (
        "pay frequency",
        "provider support",
        "daily",
        "weekly",
        "fortnightly",
        "monthly",
        "quarterly",
        "unsupported frequency",
    ),
    "gross_to_net_and_finalised_totals": (
        "gross-to-net",
        "gross to net",
        "net pay",
        "finalised totals",
        "finalised payment memory",
        "PAYG outcome",
    ),
    "supplementary_incremental_payg": (
        "supplementary incremental PAYG",
        "supplementary PAYG",
        "same-period taxable earnings",
        "prior PAYG withheld",
    ),
    "worker_story_and_admin_queue_connection": (
        "Tax / PAYG",
        "Worker Story",
        "PayRun Admin Queue",
        "tax readiness",
        "unsupported states",
        "reprocessing",
    ),
    "unsupported_and_review_states": (
        "unsupported tax scenarios",
        "unsupported frequencies",
        "explicit status",
        "configuration status",
        "review states",
    ),
    "outstanding_hardening": (
        "Tax / PAYG",
        "outstanding hardening",
        "provider support",
        "non-weekly frequencies",
        "taxable basis governance",
        "withholding instruction UI",
        "supplementary tax",
        "full TaxStory",
    ),
}

TAX_PAYG_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Tax / PAYG", "PAYG withholding", "governed withholding calculation evidence"),
    "deterministic_tax_boundary": ("deterministic services", "tax providers", "withholding calculation"),
    "tax_story_and_explainability": ("TaxStory", "Tax Story", "worker tax profile", "rule pack selection"),
    "taxable_basis_and_payroll_bases": ("taxable basis", "taxable earnings", "Payroll Bases & Totals"),
    "worker_tax_declaration_and_withholding_inputs": ("worker tax declaration", "withholding instruction", "withholding inputs"),
    "payment_date_and_process_period_context": ("ProcessPeriod PaymentDate", "payment date", "process period"),
    "pay_frequency_and_provider_support": ("pay frequency", "provider support", "unsupported frequency"),
    "gross_to_net_and_finalised_totals": ("gross-to-net", "gross to net", "net pay", "finalised totals"),
    "supplementary_incremental_payg": ("supplementary incremental PAYG", "supplementary PAYG", "prior PAYG withheld"),
    "worker_story_and_admin_queue_connection": ("Tax / PAYG", "Worker Story", "PayRun Admin Queue"),
    "unsupported_and_review_states": ("unsupported tax scenarios", "unsupported frequencies", "explicit status"),
    "outstanding_hardening": ("outstanding hardening", "taxable basis governance", "full TaxStory"),
}

DEDUCTIONS_OBLIGATIONS_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Deductions / Obligations",
        "governed application outcomes",
        "net-pay subtraction",
        "governed payroll outcome",
    ),
    "deduction_template_chain": (
        "LibraryDeductionTemplate",
        "AccountDeductionTemplate",
        "ContactPayrollDeduction",
        "PayRunDeductionApplication",
        "advisory accelerators",
        "operative configuration",
    ),
    "worker_deduction_instruction": (
        "ContactPayrollDeduction",
        "worker-specific deduction instruction",
        "operative configuration",
    ),
    "payrun_deduction_application_memory": (
        "PayRunDeductionApplication",
        "requested",
        "taken",
        "skipped",
        "unmet",
        "outcome memory",
    ),
    "supplementary_deduction_memory": (
        "supplementary deduction memory",
        "supplementary PayRuns",
        "same-period application memory",
        "recurring deductions",
        "blindly repeat",
    ),
    "applicability_affordability_and_priority": (
        "applicability",
        "affordability",
        "priority",
        "partial",
        "full-only",
        "carry-forward",
        "explainable",
    ),
    "skipped_partial_unmet_and_carry_forward": (
        "skipped",
        "partial",
        "unmet",
        "carry-forward",
        "carry forward",
        "visible",
        "must not silently disappear",
    ),
    "obligations_and_reducing_balance_recovery": (
        "ContactPayrollObligation",
        "ContactPayrollObligationLedger",
        "durable obligations",
        "balance-bearing recovery",
        "reducing-balance recovery",
        "outstanding balance",
        "ledger evidence",
    ),
    "negative_net_pay_governance": (
        "negative net pay",
        "governed outcome",
        "policy treatment",
        "silent arithmetic side effect",
    ),
    "gross_to_net_and_payment_execution": (
        "gross-to-net",
        "gross to net",
        "payment execution",
        "remittance",
        "deduction readiness",
    ),
    "worker_story_and_admin_queue_connection": (
        "Deductions / Obligations",
        "Worker Story",
        "PayRun Admin Queue",
        "Worker Attention",
        "readiness",
        "issues",
    ),
    "outstanding_hardening": (
        "Deductions / Obligations",
        "outstanding hardening",
        "full UI",
        "remittance",
        "payment execution",
        "obligation write-off",
        "costing consequences",
        "negative-net-pay policy",
        "deduction tax integration",
    ),
}

DEDUCTIONS_OBLIGATIONS_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Deductions / Obligations", "governed application outcomes", "net-pay subtraction"),
    "deduction_template_chain": ("LibraryDeductionTemplate", "AccountDeductionTemplate", "ContactPayrollDeduction"),
    "worker_deduction_instruction": ("ContactPayrollDeduction", "worker-specific deduction instruction"),
    "payrun_deduction_application_memory": ("PayRunDeductionApplication", "requested", "taken", "skipped", "unmet"),
    "supplementary_deduction_memory": ("supplementary deduction memory", "same-period application memory"),
    "applicability_affordability_and_priority": ("applicability", "affordability", "priority"),
    "skipped_partial_unmet_and_carry_forward": ("skipped", "partial", "unmet", "carry-forward"),
    "obligations_and_reducing_balance_recovery": (
        "ContactPayrollObligation",
        "ContactPayrollObligationLedger",
        "reducing-balance recovery",
    ),
    "negative_net_pay_governance": ("negative net pay", "policy treatment"),
    "gross_to_net_and_payment_execution": ("gross-to-net", "gross to net", "payment execution", "remittance"),
    "worker_story_and_admin_queue_connection": ("Worker Story", "PayRun Admin Queue", "Worker Attention"),
    "outstanding_hardening": ("outstanding hardening", "negative-net-pay policy", "deduction tax integration"),
}

RETRO_REPLAY_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Retro / Replay",
        "governed historical correction",
        "evidence replay",
        "ordinary reprocessing",
    ),
    "attributed_period_and_paid_period_truth": (
        "attributed period",
        "paid period",
        "attributed-period truth",
        "paid-period truth",
        "distinct",
    ),
    "finalised_outcome_memory": (
        "finalised outcome memory",
        "historical payment truth",
        "finalised outcomes",
        "silently overwritten",
    ),
    "current_effective_and_historical_truth": (
        "current-effective truth",
        "historical truth",
        "finalised truth",
        "current-effective payroll truth",
    ),
    "bucket_and_basis_snapshot_dependency": (
        "bucket snapshot",
        "basis snapshot",
        "calculation evidence",
        "source hashes",
        "historical bucket evidence",
    ),
    "source_change_and_dependency_detection": (
        "source change",
        "configuration change",
        "dependency detection",
        "dirty replay candidates",
        "hidden recalculation",
    ),
    "retro_payrun_and_supplementary_distinction": (
        "retro PayRun",
        "supplementary PayRun",
        "retro PayRuns",
        "supplementary PayRuns",
        "same concept",
    ),
    "comparison_and_variance_connection": (
        "Comparison / Remediation",
        "comparison",
        "variance",
        "retro/replay evidence",
        "not the same concept",
    ),
    "worker_story_connection": ("Retro / Replay", "Worker Story", "worker level", "retro impacts", "replay impacts"),
    "admin_queue_and_movement_review_connection": (
        "PayRun Admin Queue",
        "Admin Queue",
        "Movement Review",
        "retro candidates",
        "dependency issues",
        "variance",
    ),
    "audit_replay_and_non_destructive_history": (
        "audit replay",
        "non-destructive history",
        "auditable",
        "historical evidence",
        "correction/replay",
    ),
    "outstanding_hardening": (
        "Retro / Replay",
        "outstanding hardening",
        "future work",
        "full retro/replay implementation",
        "dependency detection",
    ),
}

RETRO_REPLAY_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Retro / Replay", "governed historical correction", "evidence replay"),
    "attributed_period_and_paid_period_truth": ("attributed period", "paid period", "distinct"),
    "finalised_outcome_memory": ("finalised outcome memory", "historical payment truth", "finalised outcomes"),
    "current_effective_and_historical_truth": ("current-effective truth", "historical truth", "finalised truth"),
    "bucket_and_basis_snapshot_dependency": ("bucket snapshot", "basis snapshot", "source hashes"),
    "source_change_and_dependency_detection": ("source change", "dependency detection", "dirty replay candidates"),
    "retro_payrun_and_supplementary_distinction": ("retro PayRun", "supplementary PayRun"),
    "comparison_and_variance_connection": ("Comparison / Remediation", "variance", "retro/replay evidence"),
    "worker_story_connection": ("Retro / Replay", "Worker Story"),
    "admin_queue_and_movement_review_connection": ("PayRun Admin Queue", "Movement Review", "dependency issues"),
    "audit_replay_and_non_destructive_history": ("audit replay", "non-destructive history", "auditable"),
    "outstanding_hardening": ("outstanding hardening", "future work", "full retro/replay implementation"),
}


def _evidence_text(results: list[RetrievalResult]) -> str:
    parts: list[str] = []
    for result in results[:2]:
        parts.extend(
            [
                result.title or "",
                result.chunk_text or "",
                " ".join(result.matched_tokens),
                " ".join(result.matched_phrases),
                result.snippet or "",
            ]
        )
    return "\n".join(parts)


def _detect_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if contains_normalized_term(text, term)]


def _has_any(detected_terms: list[str], *terms: str) -> bool:
    detected = {term.lower() for term in detected_terms}
    return any(term.lower() in detected for term in terms)


def _weak_summary(group: EvidenceGroup) -> EvidenceGroupSummary:
    return EvidenceGroupSummary(
        group_id=group.group_id,
        label=group.label,
        sentence=f"The retrieved formal corpus has weak evidence for {group.label}.",
        detected_terms=[],
        is_weak=True,
    )


def _configuration_sentence(terms: list[str], label: str) -> str:
    clauses = ["Annual Leave configuration is represented in the retrieved formal corpus"]
    if _has_any(terms, "LeaveType", "LeaveTypeRule"):
        clauses.append("through LeaveType and LeaveTypeRule policy")
    if _has_any(terms, "LeaveTypeKind", "Rule Cockpit"):
        clauses.append("with LeaveTypeKind and the Rule Cockpit organising leave-rule setup")
    settings = [term for term in ("Accrual", "Payment", "Governance") if _has_any(terms, term)]
    if settings:
        clauses.append(f"including {', '.join(settings)} settings")
    return f"{label}: {', '.join(clauses)}."


def _accrual_sentence(terms: list[str], label: str) -> str:
    clauses = ["Annual Leave accrual is treated as entitlement movement"]
    if _has_any(terms, "LeaveLedger"):
        clauses.append("represented through LeaveLedger-style rows")
    if _has_any(terms, "minutes"):
        clauses.append("with minute-based evidence")
    if _has_any(terms, "interpreter truth", "no fallback"):
        clauses.append("using interpreter-truth or no-fallback controls where retrieved")
    if _has_any(terms, "process period", "PayRun"):
        clauses.append("in process-period or PayRun context where available")
    return f"{label}: {', '.join(clauses)}."


def _taken_sentence(terms: list[str], label: str) -> str:
    clauses = ["TAKEN Annual Leave is treated separately from accrual"]
    if _has_any(terms, "LeaveLedger"):
        clauses.append("with consumption recorded as LeaveLedger movement")
    if _has_any(terms, "minutes"):
        clauses.append("using minutes where retrieved")
    if _has_any(terms, "public holiday", "DeductsOnPublicHoliday"):
        clauses.append("and public holiday deduction controlled by DeductsOnPublicHoliday")
    if _has_any(terms, "skip", "resolver"):
        clauses.append("with resolver or skip behaviour indicated by formal evidence")
    return f"{label}: {', '.join(clauses)}."


def _valuation_sentence(terms: list[str], label: str) -> str:
    clauses = ["Valuation is a distinct Annual Leave evidence area"]
    if _has_any(terms, "valuation basis"):
        clauses.append("connected to valuation-basis evidence")
    if _has_any(terms, "ordinary rate"):
        clauses.append("with ordinary-rate evidence where retrieved")
    if _has_any(terms, "PayRun", "snapshot"):
        clauses.append("and PayRun or snapshot context in the retrieved logs")
    if _has_any(terms, "liability"):
        clauses.append("including liability context where retrieved")
    return f"{label}: {', '.join(clauses)}."


def _payrun_sentence(terms: list[str], label: str) -> str:
    clauses = ["PayRun processing includes leave-management operating flow evidence"]
    if _has_any(terms, "Generate Leave Accruals on Process"):
        clauses.append("with Generate Leave Accruals on Process exposed as an explicit processing option")
    if _has_any(terms, "leave accruals"):
        clauses.append("including leave accrual generation")
    if _has_any(terms, "valuation basis"):
        clauses.append("and valuation basis generation where retrieved")
    if _has_any(terms, "Admin Queue"):
        clauses.append("with Admin Queue context present")
    return f"{label}: {', '.join(clauses)}."


def _worker_story_sentence(terms: list[str], label: str) -> str:
    clauses = ["Worker Story presents leave through worker-facing evidence output"]
    if _has_any(terms, "Leave and Accrual Outcome"):
        clauses.append("including a Leave and Accrual Outcome chapter")
    if _has_any(terms, "server-owned leave output"):
        clauses.append("as server-owned leave output")
    if _has_any(terms, "ledger", "valuation basis", "evidence chain"):
        details = [term for term in ("ledger", "valuation basis", "evidence chain") if _has_any(terms, term)]
        clauses.append(f"with {', '.join(details)} details")
    return f"{label}: {', '.join(clauses)}."


def _outstanding_sentence(terms: list[str], label: str) -> str:
    clauses = ["Outstanding hardening remains in the retrieved Annual Leave evidence"]
    if _has_any(terms, "Leave Source Model"):
        clauses.append("around the Leave Source Model")
    lot_terms = [term for term in ("FIFO", "lot consumption", "revaluation") if _has_any(terms, term)]
    if lot_terms:
        clauses.append(f"including {', '.join(lot_terms)} where applicable")
    if _has_any(terms, "production hardening", "hardening"):
        clauses.append("and production hardening")
    return f"{label}: {', '.join(clauses)}."


def _worker_story_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Worker Story evidence"]
    detail_terms = [
        term
        for term in (
            "Worker Story",
            "Worker Calculation Story",
            "Talking Payslip",
            "SourceTruth",
            "Source truth",
            "inclusion",
            "Interpreted Worked Hours",
            "Calculated Payroll Outcome",
            "Decision Story",
            "Rate Story",
            "DecisionEvidenceIndex",
            "RateSourceEvidenceIndex",
            "current-effective payroll output",
            "current-effective interpreter run",
            "ObjectTime grouping",
            "PayRun Admin Queue",
            "Movement Review",
            "Payroll Bases & Totals",
            "Leave and Accrual Outcome",
            "Correction Audit Story",
            "outstanding hardening",
            "limitations",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:6])}")
    return f"{', '.join(clauses)}."


def _payroll_bases_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Payroll Bases & Totals evidence"]
    detail_terms = [
        term
        for term in (
            "Payroll Bases & Totals",
            "governed payroll basis evidence",
            "PayrollBucketDefinition",
            "Payroll Bucket Definition",
            "period definition",
            "calendar policy",
            "membership",
            "worked hours",
            "quantity",
            "gross basis",
            "ordinary basis",
            "superable basis",
            "taxable basis",
            "payroll tax",
            "WIC",
            "PAYG",
            "current-effective truth",
            "stale",
            "PayrollBucketResult",
            "readiness",
            "stale rows",
            "rebuild",
            "Worker Story",
            "Movement Review",
            "PayRun Admin Queue",
            "outstanding hardening",
            "bucket lifecycle",
            "versioning",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:8])}")
    return f"{', '.join(clauses)}."


def _is_payrun_admin_queue_group(group: EvidenceGroup) -> bool:
    return "Admin Queue" in group.label or group.group_id in {
        "blockers_warnings_and_ready_actions",
        "worker_attention_and_dirty_contacts",
        "processing_and_reprocessing_actions",
        "finalisation_readiness",
        "assurance_snapshot",
        "review_surfaces_and_navigation",
        "payroll_bases_connection",
    }


def _is_movement_review_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Movement Review") or group.group_id in {
        "reasonableness_not_error",
        "worker_and_organisation_lenses",
        "variance_and_comparable_periods",
        "admin_queue_connection",
        "trend_only_and_threshold_treatment",
        "filters_and_return_context",
    }


def _is_comparison_remediation_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Comparison") or group.group_id in {
        "three_lane_comparison_model",
        "primary_award_path_preservation",
        "actuals_as_external_outcome_truth",
        "comparison_policy",
        "comparison_run_and_line_evidence",
        "variance_generation_and_governance",
        "position_classification_mapping",
    }


def _is_tax_payg_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Tax / PAYG") or group.group_id in {
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
    }


def _is_deductions_obligations_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Deductions / Obligations") or group.group_id in {
        "deduction_template_chain",
        "worker_deduction_instruction",
        "payrun_deduction_application_memory",
        "supplementary_deduction_memory",
        "applicability_affordability_and_priority",
        "skipped_partial_unmet_and_carry_forward",
        "obligations_and_reducing_balance_recovery",
        "negative_net_pay_governance",
        "gross_to_net_and_payment_execution",
    }


def _is_retro_replay_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Retro / Replay") or group.group_id in {
        "attributed_period_and_paid_period_truth",
        "finalised_outcome_memory",
        "current_effective_and_historical_truth",
        "bucket_and_basis_snapshot_dependency",
        "source_change_and_dependency_detection",
        "retro_payrun_and_supplementary_distinction",
        "comparison_and_variance_connection",
        "audit_replay_and_non_destructive_history",
    }


def _payrun_admin_queue_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved PayRun Admin Queue evidence"]
    detail_terms = [
        term
        for term in (
            "PayRun Admin Queue",
            "Admin Queue",
            "operator workbench",
            "what needs action now",
            "Command Centre",
            "blockers",
            "warnings",
            "ready actions",
            "Worker Attention",
            "dirty contacts",
            "processing actions",
            "reprocessing actions",
            "deterministic services",
            "finalisation readiness",
            "Assurance Snapshot",
            "reasonableness",
            "review signals",
            "Worker Story",
            "Payroll Bases & Totals",
            "Movement Review",
            "PayRun Output",
            "server-owned operation tracker",
            "global queue resolver",
            "governed assurance thresholds",
            "warning acknowledgement",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:8])}")
    return f"{', '.join(clauses)}."


def _comparison_remediation_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Comparison / Remediation evidence"]
    detail_terms = [
        term
        for term in (
            "Comparison / Remediation",
            "governed comparison",
            "primary calculated",
            "comparator calculated",
            "actual imported",
            "actuals lane",
            "ObjectTime",
            "EmployeeAppointment",
            "AwardPositionClass",
            "primary award path",
            "operational payroll truth",
            "imported actuals",
            "external outcome truth",
            "AwardComparisonPolicy",
            "comparator selection",
            "active lanes",
            "offset policy",
            "variance treatment",
            "PayRunComparisonRun",
            "PayRunComparisonLine",
            "comparison evidence",
            "PayRunVarianceLine",
            "variance line",
            "remediation top-up",
            "typed",
            "explainable",
            "AwardPositionClassComparisonMap",
            "EmployeeAppointmentAwardClassAssignment",
            "ObjectTimeClassificationResolution",
            "comparator classification",
            "Worker Story",
            "PayRun Admin Queue",
            "Movement Review",
            "outstanding hardening",
            "design doctrine",
            "not yet implemented",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:8])}")
    return f"{', '.join(clauses)}."


def _tax_payg_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Tax / PAYG evidence"]
    detail_terms = [
        term
        for term in (
            "Tax / PAYG",
            "PAYG withholding",
            "governed withholding calculation evidence",
            "deterministic services",
            "tax providers",
            "withholding calculation",
            "TaxStory",
            "Tax Story",
            "source truth",
            "worker tax profile",
            "payroll context",
            "rule pack selection",
            "component selection",
            "frequency conversion",
            "band formula calculation",
            "rounding",
            "net-pay effect",
            "audit provenance",
            "taxable basis",
            "taxable earnings",
            "Payroll Bases & Totals",
            "governed basis membership",
            "worker tax declaration",
            "withholding instruction",
            "ProcessPeriod PaymentDate",
            "payment date",
            "pay frequency",
            "provider support",
            "gross-to-net",
            "finalised totals",
            "supplementary incremental PAYG",
            "Worker Story",
            "PayRun Admin Queue",
            "unsupported tax scenarios",
            "explicit status",
            "outstanding hardening",
            "full TaxStory",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:8])}")
    return f"{', '.join(clauses)}."


def _deductions_obligations_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Deductions / Obligations evidence"]
    detail_terms = [
        term
        for term in (
            "Deductions / Obligations",
            "governed application outcomes",
            "governed payroll outcome",
            "net-pay subtraction",
            "LibraryDeductionTemplate",
            "AccountDeductionTemplate",
            "ContactPayrollDeduction",
            "PayRunDeductionApplication",
            "advisory accelerators",
            "operative configuration",
            "worker-specific deduction instruction",
            "requested",
            "taken",
            "skipped",
            "unmet",
            "outcome memory",
            "supplementary deduction memory",
            "same-period application memory",
            "recurring deductions",
            "applicability",
            "affordability",
            "priority",
            "partial",
            "full-only",
            "carry-forward",
            "visible",
            "ContactPayrollObligation",
            "ContactPayrollObligationLedger",
            "durable obligations",
            "balance-bearing recovery",
            "reducing-balance recovery",
            "outstanding balance",
            "ledger evidence",
            "negative net pay",
            "policy treatment",
            "gross-to-net",
            "payment execution",
            "remittance",
            "Worker Story",
            "PayRun Admin Queue",
            "Worker Attention",
            "outstanding hardening",
            "negative-net-pay policy",
            "deduction tax integration",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:9])}")
    return f"{', '.join(clauses)}."


def _retro_replay_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Retro / Replay evidence"]
    detail_terms = [
        term
        for term in (
            "Retro / Replay",
            "governed historical correction",
            "evidence replay",
            "ordinary reprocessing",
            "attributed period",
            "paid period",
            "attributed-period truth",
            "paid-period truth",
            "finalised outcome memory",
            "historical payment truth",
            "finalised outcomes",
            "current-effective truth",
            "historical truth",
            "finalised truth",
            "bucket snapshot",
            "basis snapshot",
            "calculation evidence",
            "source hashes",
            "historical bucket evidence",
            "source change",
            "configuration change",
            "dependency detection",
            "dirty replay candidates",
            "hidden recalculation",
            "retro PayRun",
            "supplementary PayRun",
            "Comparison / Remediation",
            "variance",
            "Worker Story",
            "PayRun Admin Queue",
            "Movement Review",
            "audit replay",
            "non-destructive history",
            "auditable",
            "outstanding hardening",
            "future work",
            "full retro/replay implementation",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:9])}")
    return f"{', '.join(clauses)}."


def _movement_review_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Movement Review evidence"]
    detail_terms = [
        term
        for term in (
            "Movement Review",
            "Payroll Movement Review",
            "reasonableness",
            "review surface",
            "variance",
            "review-worthy",
            "worker lens",
            "organisation lens",
            "comparable period",
            "baseline evidence",
            "Payroll Bases & Totals",
            "basis evidence",
            "Worker Story",
            "worker-level drill-through",
            "PayRun Admin Queue",
            "Admin Queue",
            "current-effective payroll",
            "bucket source truth",
            "trend-only",
            "rolling average",
            "YTD",
            "thresholds",
            "filters",
            "return context",
            "Movement Review Policy",
            "historical bucket rebuild governance",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:8])}")
    return f"{', '.join(clauses)}."


def _sentence_for_group(group: EvidenceGroup, terms: list[str]) -> str:
    if _is_retro_replay_group(group):
        return _retro_replay_domain_sentence(terms, group.label)
    if _is_deductions_obligations_group(group):
        return _deductions_obligations_domain_sentence(terms, group.label)
    if _is_tax_payg_group(group):
        return _tax_payg_domain_sentence(terms, group.label)
    if _is_comparison_remediation_group(group):
        return _comparison_remediation_domain_sentence(terms, group.label)
    if _is_movement_review_group(group):
        return _movement_review_domain_sentence(terms, group.label)
    if _is_payrun_admin_queue_group(group):
        return _payrun_admin_queue_domain_sentence(terms, group.label)
    if group.group_id == "configuration":
        return _configuration_sentence(terms, group.label)
    if group.group_id == "accrual":
        return _accrual_sentence(terms, group.label)
    if group.group_id == "taken":
        return _taken_sentence(terms, group.label)
    if group.group_id == "valuation":
        return _valuation_sentence(terms, group.label)
    if group.group_id == "payrun":
        return _payrun_sentence(terms, group.label)
    if group.group_id == "worker_story":
        return _worker_story_sentence(terms, group.label)
    if group.group_id == "outstanding":
        return _outstanding_sentence(terms, group.label)
    if group.group_id in {
        "purpose_and_operator_meaning",
        "bucket_definition_and_membership",
        "worked_hours_and_quantity",
        "gross_ordinary_superable_taxable_bases",
        "readiness_and_rebuild",
        "worker_story_connection",
        "movement_review_connection",
    }:
        return _payroll_bases_domain_sentence(terms, group.label)
    if group.group_id == "current_effective_truth" and _has_any(terms, "stale", "source truth"):
        return _payroll_bases_domain_sentence(terms, group.label)
    if group.group_id == "outstanding_hardening" and _has_any(terms, "Payroll Bases & Totals", "bucket lifecycle", "versioning"):
        return _payroll_bases_domain_sentence(terms, group.label)
    if group.group_id in {
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
    }:
        return _worker_story_domain_sentence(terms, group.label)
    return f"{group.label}: Retrieved evidence indicates {', '.join(terms)}."


def synthesize_evidence_group(group: EvidenceGroup, results: list[RetrievalResult]) -> EvidenceGroupSummary:
    if not results:
        return _weak_summary(group)
    evidence_text = _evidence_text(results)
    key_terms = (
        RETRO_REPLAY_GROUP_KEY_TERMS.get(group.group_id)
        if _is_retro_replay_group(group)
        else
        DEDUCTIONS_OBLIGATIONS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_deductions_obligations_group(group)
        else
        TAX_PAYG_GROUP_KEY_TERMS.get(group.group_id)
        if _is_tax_payg_group(group)
        else
        COMPARISON_REMEDIATION_GROUP_KEY_TERMS.get(group.group_id)
        if _is_comparison_remediation_group(group)
        else
        MOVEMENT_REVIEW_GROUP_KEY_TERMS.get(group.group_id)
        if _is_movement_review_group(group)
        else
        PAYRUN_ADMIN_QUEUE_GROUP_KEY_TERMS.get(group.group_id)
        if _is_payrun_admin_queue_group(group)
        else GROUP_KEY_TERMS.get(group.group_id)
    )
    signal_key_terms = (
        RETRO_REPLAY_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_retro_replay_group(group)
        else
        DEDUCTIONS_OBLIGATIONS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_deductions_obligations_group(group)
        else
        TAX_PAYG_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_tax_payg_group(group)
        else
        COMPARISON_REMEDIATION_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_comparison_remediation_group(group)
        else
        MOVEMENT_REVIEW_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_movement_review_group(group)
        else
        PAYRUN_ADMIN_QUEUE_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_payrun_admin_queue_group(group)
        else GROUP_SIGNAL_TERMS.get(group.group_id)
    )
    terms = _detect_terms(evidence_text, key_terms or group.required_terms_any)
    signal_terms = _detect_terms(evidence_text, signal_key_terms or group.required_terms_any)
    if not signal_terms:
        return _weak_summary(group)
    return EvidenceGroupSummary(
        group_id=group.group_id,
        label=group.label,
        sentence=_sentence_for_group(group, terms),
        detected_terms=terms,
        is_weak=False,
    )


def synthesize_domain_plan_evidence(
    plan: DomainRetrievalPlan,
    retrieved_chunks: list[RetrievalResult],
) -> list[EvidenceGroupSummary]:
    chunks_by_group: dict[str, list[RetrievalResult]] = {}
    for result in retrieved_chunks:
        if result.evidence_group_id:
            chunks_by_group.setdefault(result.evidence_group_id, []).append(result)
    return [
        synthesize_evidence_group(group, chunks_by_group.get(group.group_id, retrieved_chunks))
        for group in plan.evidence_groups
    ]

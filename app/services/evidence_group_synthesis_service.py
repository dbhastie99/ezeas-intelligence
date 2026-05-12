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

WORKER_ATTENTION_ISSUE_RESOLUTION_GROUP_KEY_TERMS = {
    "worker_attention_purpose": (
        "Worker Attention",
        "WorkerAttention",
        "Worker Attention Centre",
        "Issue Resolution",
        "worker-level issue surface",
    ),
    "worker_issue_model": ("Worker issue", "WorkerIssue", "issue scope", "issue class", "issue type", "issue severity"),
    "blockers_warnings_and_readiness": (
        "blockers",
        "warnings",
        "readiness gaps",
        "worker-level blockers",
        "worker-level warnings",
        "ready actions",
    ),
    "deterministic_fix_links": (
        "deterministic fix link",
        "deterministic fix links",
        "resolution surfaces",
        "fix action",
        "server-owned fix target",
    ),
    "dirty_contact_and_reprocessing": (
        "dirty contact",
        "dirty contacts",
        "PayRunContact dirty",
        "reprocessing",
        "reprocess",
        "contact changes",
    ),
    "payment_allocation_readiness": (
        "payment allocation",
        "payment allocation readiness",
        "payment destination",
        "bank allocation",
        "payment readiness",
    ),
    "tax_deduction_leave_readiness": (
        "tax readiness",
        "deduction readiness",
        "leave readiness",
        "tax/deduction/leave readiness",
        "readiness evidence",
    ),
    "negative_net_pay_and_obligations": (
        "negative net pay",
        "obligations",
        "out-of-pay",
        "recoveries",
        "worker obligation",
        "obligation issue",
    ),
    "worker_story_relationship": (
        "Worker Attention",
        "Worker Story",
        "worker issue evidence",
        "worker evidence",
        "explanation surface",
    ),
    "admin_queue_relationship": (
        "Worker Attention",
        "PayRun Admin Queue",
        "Admin Queue",
        "operator workbench",
        "not the same surface",
    ),
    "outstanding_hardening": (
        "Worker Attention",
        "outstanding hardening",
        "WorkerIssue",
        "issue taxonomy",
        "resolution workflow",
        "contract tests",
    ),
}

WORKER_ATTENTION_ISSUE_RESOLUTION_GROUP_SIGNAL_TERMS = {
    "worker_attention_purpose": ("Worker Attention", "Issue Resolution", "worker-level issue surface"),
    "worker_issue_model": ("WorkerIssue", "Worker issue", "issue scope", "issue severity"),
    "blockers_warnings_and_readiness": ("blockers", "warnings", "readiness gaps"),
    "deterministic_fix_links": ("deterministic fix link", "resolution surfaces", "fix action"),
    "dirty_contact_and_reprocessing": ("dirty contact", "PayRunContact dirty", "reprocessing"),
    "payment_allocation_readiness": ("payment allocation", "payment destination", "payment readiness"),
    "tax_deduction_leave_readiness": ("tax readiness", "deduction readiness", "leave readiness"),
    "negative_net_pay_and_obligations": ("negative net pay", "obligations", "out-of-pay"),
    "worker_story_relationship": ("Worker Attention", "Worker Story", "worker issue evidence"),
    "admin_queue_relationship": ("Worker Attention", "PayRun Admin Queue", "not the same surface"),
    "outstanding_hardening": ("Worker Attention", "outstanding hardening", "contract tests"),
}

GROSS_TO_NET_GROUP_KEY_TERMS = {
    "gross_to_net_purpose": (
        "Gross-to-Net",
        "Gross to Net",
        "GrossToNet",
        "payroll outcome calculation",
        "payroll outcome explanation surface",
    ),
    "gross_earnings_and_payroll_output": ("gross earnings", "gross pay", "payroll output", "earnings lines", "payroll outcome"),
    "taxable_basis_and_payg": ("taxable basis", "taxable earnings", "PAYG", "withholding", "tax withholding", "final withholding"),
    "deductions_and_obligations": (
        "deductions",
        "obligations",
        "deduction applications",
        "obligation recovery",
        "post-tax deductions",
    ),
    "negative_net_pay": (
        "negative net pay",
        "governed treatment",
        "carry-forward",
        "recovery",
        "write-off",
        "not silently converted to zero",
    ),
    "net_pay_and_payment_allocation": (
        "net pay",
        "payment allocation",
        "payment execution readiness",
        "payment destination",
        "worker net pay",
    ),
    "worker_story_relationship": (
        "Gross-to-Net",
        "Worker Story",
        "gross-to-net evidence",
        "worker evidence",
        "payroll outcome explanation",
    ),
    "finalisation_and_payment_execution": (
        "finalisation",
        "finalised outcome truth",
        "payment execution",
        "payment execution readiness",
        "not payment execution",
    ),
    "current_effective_output_truth": (
        "current-effective payroll output",
        "current effective payroll output",
        "current truth",
        "stale",
        "superseded",
    ),
    "outstanding_hardening": (
        "Gross-to-Net",
        "outstanding hardening",
        "negative net pay",
        "taxable basis",
        "payment allocation",
        "contract tests",
    ),
}

GROSS_TO_NET_GROUP_SIGNAL_TERMS = {
    "gross_to_net_purpose": ("Gross-to-Net", "payroll outcome calculation", "payroll outcome explanation surface"),
    "gross_earnings_and_payroll_output": ("gross earnings", "payroll output", "payroll outcome"),
    "taxable_basis_and_payg": ("taxable basis", "PAYG", "withholding"),
    "deductions_and_obligations": ("deductions", "obligations", "deduction applications"),
    "negative_net_pay": ("negative net pay", "governed treatment", "not silently converted to zero"),
    "net_pay_and_payment_allocation": ("net pay", "payment allocation", "payment execution readiness"),
    "worker_story_relationship": ("Gross-to-Net", "Worker Story", "gross-to-net evidence"),
    "finalisation_and_payment_execution": ("finalised outcome truth", "payment execution", "not payment execution"),
    "current_effective_output_truth": ("current-effective payroll output", "current truth", "stale"),
    "outstanding_hardening": ("Gross-to-Net", "outstanding hardening", "contract tests"),
}

RATE_SOURCE_RATE_STORY_GROUP_KEY_TERMS = {
    "rate_story_purpose": ("RateSource / Rate Story", "Rate Story", "RateStory", "selected rate", "rate explanation"),
    "rate_source_selection": ("RateSource", "Rate Source", "selected rate", "rate selection", "rate source selection"),
    "rate_amount_evidence": ("rate amount", "amount came from", "rate evidence", "selected amount", "rate value"),
    "date_effective_rates": ("date-effective rate", "date-effective rates", "effective date", "date effective rates", "RateSource"),
    "award_account_class_scope": ("award rate", "account rate", "class rate", "award scope", "account scope", "class scope", "AwardRateType", "RateType"),
    "pay_guide_rate_evidence": ("pay guide rate evidence", "pay guide evidence", "RateSourceEvidenceIndex", "Rate Source Evidence Index", "source row"),
    "rate_source_evidence_index": (
        "RateSourceEvidenceIndex",
        "Rate Source Evidence Index",
        "rate source evidence index",
        "why a rate",
        "rate evidence index",
    ),
    "rate_story_vs_decision_story": ("Rate Story", "Decision Story", "rate amount", "treatment selection", "entitlement", "not the same"),
    "worker_story_relationship": ("Rate Story", "Worker Story", "Worker Calculation Story", "worker evidence", "rate explanation"),
    "payroll_output_and_gross_to_net_relationship": ("Rate Story", "payroll output", "gross-to-net", "Gross-to-Net", "calculated payroll outcome", "line proof"),
    "outstanding_hardening": ("RateSource", "Rate Story", "outstanding hardening", "RateSourceEvidenceIndex", "contract tests", "pay guide evidence"),
}

RATE_SOURCE_RATE_STORY_GROUP_SIGNAL_TERMS = {
    "rate_story_purpose": ("RateSource / Rate Story", "Rate Story", "selected rate"),
    "rate_source_selection": ("RateSource", "selected rate", "rate selection"),
    "rate_amount_evidence": ("rate amount", "rate evidence", "amount came from"),
    "date_effective_rates": ("date-effective rate", "date-effective rates", "effective date"),
    "award_account_class_scope": ("award rate", "account rate", "class rate", "AwardRateType", "RateType"),
    "pay_guide_rate_evidence": ("pay guide rate evidence", "RateSourceEvidenceIndex", "pay guide evidence"),
    "rate_source_evidence_index": ("RateSourceEvidenceIndex", "Rate Source Evidence Index", "why a rate"),
    "rate_story_vs_decision_story": ("Rate Story", "Decision Story", "not the same"),
    "worker_story_relationship": ("Rate Story", "Worker Story", "worker evidence"),
    "payroll_output_and_gross_to_net_relationship": ("Rate Story", "payroll output", "Gross-to-Net"),
    "outstanding_hardening": ("RateSource", "Rate Story", "outstanding hardening"),
}

DECISION_STORY_GROUP_KEY_TERMS = {
    "decision_story_purpose": ("Decision Story", "DecisionStory", "payroll decision", "why a treatment", "why a line exists"),
    "treatment_and_entitlement_selection": ("treatment selection", "entitlement decision", "why a treatment was selected", "why the line exists", "payroll decision"),
    "decision_evidence_index": ("DecisionEvidenceIndex", "Decision Evidence Index", "decision evidence", "why a treatment", "why a line exists"),
    "award_rule_and_runtime_fact_evidence": ("award rule", "configured rules", "runtime facts", "source evidence", "rule outcome"),
    "allowance_penalty_overtime_shift_evidence": ("allowance decision", "penalty decision", "overtime decision", "shift decision", "allowance", "penalty", "overtime", "shift"),
    "break_public_holiday_and_special_condition_evidence": ("break treatment", "missed break", "public holiday decision", "minimum engagement", "special condition"),
    "decision_story_vs_rate_story": ("Decision Story", "Rate Story", "treatment or line exists", "rate amount", "not the same"),
    "worker_story_relationship": ("Decision Story", "Worker Story", "payroll line explanation", "worker evidence", "DecisionEvidenceIndex"),
    "payroll_output_and_gross_to_net_relationship": ("Decision Story", "payroll output", "Gross-to-Net", "calculated payroll outcome", "line proof"),
    "outstanding_hardening": ("Decision Story", "DecisionEvidenceIndex", "outstanding hardening", "contract tests", "evidence limitation"),
}

DECISION_STORY_GROUP_SIGNAL_TERMS = {
    "decision_story_purpose": ("Decision Story", "payroll decision", "why a treatment"),
    "treatment_and_entitlement_selection": ("treatment selection", "entitlement decision", "why the line exists"),
    "decision_evidence_index": ("DecisionEvidenceIndex", "Decision Evidence Index", "decision evidence"),
    "award_rule_and_runtime_fact_evidence": ("award rule", "runtime facts", "rule outcome"),
    "allowance_penalty_overtime_shift_evidence": ("allowance", "penalty", "overtime", "shift"),
    "break_public_holiday_and_special_condition_evidence": ("break treatment", "public holiday decision", "minimum engagement"),
    "decision_story_vs_rate_story": ("Decision Story", "Rate Story", "not the same"),
    "worker_story_relationship": ("Decision Story", "Worker Story", "payroll line explanation"),
    "payroll_output_and_gross_to_net_relationship": ("Decision Story", "payroll output", "Gross-to-Net"),
    "outstanding_hardening": ("Decision Story", "DecisionEvidenceIndex", "outstanding hardening"),
}

PAYROLL_OUTPUT_GROUP_KEY_TERMS = {
    "payroll_output_purpose": ("Payroll Output", "PayRun Output", "calculated payroll output", "payroll result", "calculated payroll result"),
    "calculated_payroll_lines": ("calculated payroll lines", "payroll line", "output line", "line-level payroll outcome", "CalcInterpreterLine"),
    "current_effective_output_truth": ("current-effective output", "current effective payroll output", "current-effective payroll output truth", "current truth", "superseded output"),
    "run_output_vs_process_period_output": ("Run Output", "Process Period Output", "PayRun Output", "run output", "process-period output"),
    "worker_level_output": ("worker-level output", "worker output", "worker payroll output", "Worker Story", "worker evidence"),
    "payrun_totals_and_line_totals": ("PayRun totals", "line totals", "payroll totals", "output totals", "CalcInterpreterRun"),
    "decision_story_and_rate_story_relationship": ("Decision Story", "Rate Story", "why line exists", "selected rate", "rate amount"),
    "gross_to_net_relationship": ("Gross-to-Net", "gross to net", "gross earnings", "net pay", "payroll outcome"),
    "payroll_bases_relationship": ("Payroll Bases & Totals", "Payroll Bases", "basis evidence", "bucket evidence", "basis totals"),
    "finalisation_and_payment_execution_relationship": ("Finalisation Readiness", "Payment Execution", "finalised outcome truth", "payment execution boundary", "payment file"),
    "outstanding_hardening": ("Payroll Output", "outstanding hardening", "current-effective output", "contract tests", "status honesty"),
}

PAYROLL_OUTPUT_GROUP_SIGNAL_TERMS = {
    "payroll_output_purpose": ("Payroll Output", "calculated payroll output", "payroll result"),
    "calculated_payroll_lines": ("payroll line", "output line", "CalcInterpreterLine"),
    "current_effective_output_truth": ("current-effective output", "current truth", "superseded output"),
    "run_output_vs_process_period_output": ("Run Output", "Process Period Output", "PayRun Output"),
    "worker_level_output": ("worker-level output", "worker output", "Worker Story"),
    "payrun_totals_and_line_totals": ("PayRun totals", "line totals", "CalcInterpreterRun"),
    "decision_story_and_rate_story_relationship": ("Decision Story", "Rate Story", "selected rate"),
    "gross_to_net_relationship": ("Gross-to-Net", "gross earnings", "net pay"),
    "payroll_bases_relationship": ("Payroll Bases & Totals", "basis evidence", "basis totals"),
    "finalisation_and_payment_execution_relationship": ("Finalisation Readiness", "Payment Execution", "finalised outcome truth"),
    "outstanding_hardening": ("Payroll Output", "outstanding hardening", "status honesty"),
}

CONTACT_PAYROLL_HISTORY_GROUP_KEY_TERMS = {
    "contact_payroll_history_purpose": ("Contact Payroll History", "payroll history", "worker payroll history", "contact-level payroll history", "payroll outcome history"),
    "contact_identity_and_payrun_participation": ("Contact", "worker", "contact identity", "PayRun participation", "PayRunContact", "worker history"),
    "current_and_historical_payroll_output": ("current payroll output", "historical payroll output", "current-effective payroll output", "payroll output history", "historical evidence"),
    "gross_to_net_history": ("Gross-to-Net history", "gross to net history", "gross earnings history", "net pay history", "payroll outcome history"),
    "deductions_obligations_and_negative_net_pay": ("contact deductions", "contact obligations", "deductions", "obligations", "negative net pay", "out-of-pay"),
    "tax_and_payment_readiness_history": ("contact tax", "contact payment", "tax history", "payment readiness history", "payment allocation", "PAYG"),
    "leave_and_accrual_history": ("leave history", "accrual history", "leave/accrual evidence", "leave accrual", "leave evidence"),
    "worker_story_relationship": ("Worker Story", "worker evidence", "worker-level story", "payroll explanation", "contact history"),
    "movement_review_and_admin_queue_relationship": ("Movement Review", "Admin Queue", "PayRun Admin Queue", "review context", "action workbench", "reasonableness"),
    "retro_replay_and_correction_relationship": ("retro history", "correction history", "retro/replay/correction context", "retro replay", "correction implications"),
    "outstanding_hardening": ("Contact Payroll History", "outstanding hardening", "status honesty", "historical payroll records", "finalised truth"),
}

CONTACT_PAYROLL_HISTORY_GROUP_SIGNAL_TERMS = {
    "contact_payroll_history_purpose": ("Contact Payroll History", "payroll history", "worker payroll history"),
    "contact_identity_and_payrun_participation": ("Contact", "PayRun participation", "worker history"),
    "current_and_historical_payroll_output": ("historical payroll output", "current-effective payroll output", "historical evidence"),
    "gross_to_net_history": ("Gross-to-Net history", "net pay history", "payroll outcome history"),
    "deductions_obligations_and_negative_net_pay": ("contact deductions", "contact obligations", "negative net pay"),
    "tax_and_payment_readiness_history": ("contact tax", "contact payment", "payment readiness history"),
    "leave_and_accrual_history": ("leave history", "accrual history", "leave/accrual evidence"),
    "worker_story_relationship": ("Worker Story", "worker evidence", "contact history"),
    "movement_review_and_admin_queue_relationship": ("Movement Review", "Admin Queue", "review context"),
    "retro_replay_and_correction_relationship": ("retro history", "correction history", "retro/replay/correction context"),
    "outstanding_hardening": ("Contact Payroll History", "outstanding hardening", "status honesty"),
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

PAYMENT_EXECUTION_REMITTANCE_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Payment Execution / Remittance",
        "governed payment execution",
        "remittance evidence",
        "generic file export",
    ),
    "finalised_gross_to_net_source": (
        "finalised gross-to-net",
        "finalised payroll outcome",
        "payment outcome",
        "payroll calculation truth",
    ),
    "worker_net_pay_and_bank_allocation": (
        "worker net pay",
        "bank allocation",
        "payment allocation",
        "bank instruction readiness",
    ),
    "payment_destination_readiness": (
        "payment destination",
        "missing payment destination",
        "partial payment destinations",
        "payment execution readiness",
    ),
    "negative_net_pay_and_obligation_interaction": (
        "negative net pay",
        "obligations",
        "carry-forward",
        "recovery",
        "write-off",
        "out-of-pay treatment",
    ),
    "deduction_and_third_party_remittance": (
        "deduction remittance",
        "third-party remittance",
        "third-party payments",
        "remittance files",
        "payment destinations",
    ),
    "payment_file_generation_and_period_close": (
        "Generate Bank File",
        "Bank File",
        "payment file",
        "Period Close",
        "payment-file execution",
    ),
    "remittance_batching_and_reconciliation": (
        "remittance batching",
        "remittance reconciliation",
        "reconciliation",
        "batching",
        "remittance batch",
    ),
    "worker_attention_and_admin_queue_connection": (
        "Payment Execution / Remittance",
        "Worker Attention",
        "PayRun Admin Queue",
        "blockers",
        "warnings",
        "actions",
    ),
    "worker_story_and_audit_evidence": (
        "Payment Execution / Remittance",
        "Worker Story",
        "audit evidence",
        "payment allocation",
        "remittance",
        "skipped",
        "unpaid",
        "unmet",
    ),
    "outstanding_hardening": (
        "Payment Execution / Remittance",
        "outstanding hardening",
        "bank file generation",
        "remittance execution",
        "reconciliation",
        "payment close",
        "obligation write-off",
        "financial consequences",
        "UI surfaces",
    ),
}

PAYMENT_EXECUTION_REMITTANCE_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Payment Execution / Remittance", "governed payment execution", "remittance evidence"),
    "finalised_gross_to_net_source": ("finalised gross-to-net", "finalised payroll outcome", "payment outcome"),
    "worker_net_pay_and_bank_allocation": ("worker net pay", "bank allocation", "payment allocation"),
    "payment_destination_readiness": ("payment destination", "payment execution readiness"),
    "negative_net_pay_and_obligation_interaction": ("negative net pay", "obligations", "write-off"),
    "deduction_and_third_party_remittance": ("deduction remittance", "third-party remittance", "third-party payments"),
    "payment_file_generation_and_period_close": ("Generate Bank File", "Bank File", "payment file", "Period Close"),
    "remittance_batching_and_reconciliation": ("remittance batching", "remittance reconciliation", "reconciliation"),
    "worker_attention_and_admin_queue_connection": ("Worker Attention", "PayRun Admin Queue", "blockers"),
    "worker_story_and_audit_evidence": ("Worker Story", "audit evidence", "payment allocation"),
    "outstanding_hardening": ("outstanding hardening", "bank file generation", "remittance execution"),
}

LEAVE_ACCRUAL_PROCESSING_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Leave Accrual",
        "Leave Processing",
        "deterministic platform outcomes",
        "Minerva calculations",
        "generic leave policy advice",
    ),
    "leave_source_truth_and_applicability": (
        "leave source truth",
        "applicability",
        "LeaveTypeRule",
        "Leave Source Model",
        "source truth",
    ),
    "accrual_basis_and_quantity": ("accrual basis", "PER_HOUR", "minute", "hour", "accrual quantity"),
    "payroll_output_and_calc_interpreter_source": (
        "CalcInterpreterLine",
        "current-effective payroll output",
        "canonical processed payroll result truth",
        "payroll result truth",
    ),
    "leave_type_and_rule_configuration": ("LeaveType", "LeaveTypeRule", "AwardRateType", "RateType", "accrualability"),
    "leave_ledger_and_accrual_posting": (
        "LeaveLedger",
        "Leave Ledger",
        "accrual",
        "payment",
        "balance movements",
        "story evidence",
    ),
    "leave_valuation_basis": ("leave valuation basis", "TAKEN leave", "valuation", "mandatory", "hard failure", "silent fallback"),
    "leave_request_payment_effects": (
        "leave request",
        "payment effects",
        "before payroll interpretation",
        "within payroll interpretation",
        "after payroll interpretation",
    ),
    "payrun_processing_and_finalisation": (
        "LeaveProcessRun",
        "PayRun",
        "finalisation readiness",
        "missing leave output",
        "leave readiness",
    ),
    "worker_story_connection": (
        "Worker Story",
        "Leave and Accrual Outcome",
        "server-owned leave output",
        "ledger",
        "valuation evidence",
    ),
    "payroll_bases_connection": (
        "Payroll Bases & Totals",
        "worked hours",
        "basis quantity",
        "governed basis evidence",
        "leave basis quantities",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "Leave Source Model",
        "leave-processing UI",
        "leave request ownership",
        "contact-vs-appointment",
        "leave story polish",
        "finalisation warning acknowledgement",
    ),
}

LEAVE_ACCRUAL_PROCESSING_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Leave Accrual", "Leave Processing", "deterministic platform outcomes"),
    "leave_source_truth_and_applicability": ("leave source truth", "applicability", "LeaveTypeRule"),
    "accrual_basis_and_quantity": ("accrual basis", "PER_HOUR", "accrual quantity"),
    "payroll_output_and_calc_interpreter_source": ("CalcInterpreterLine", "current-effective payroll output", "canonical processed payroll result truth"),
    "leave_type_and_rule_configuration": ("LeaveType", "LeaveTypeRule", "accrualability"),
    "leave_ledger_and_accrual_posting": ("LeaveLedger", "accrual", "balance movements"),
    "leave_valuation_basis": ("leave valuation basis", "TAKEN leave", "valuation"),
    "leave_request_payment_effects": ("leave request", "payment effects", "payroll interpretation"),
    "payrun_processing_and_finalisation": ("LeaveProcessRun", "PayRun", "finalisation readiness"),
    "worker_story_connection": ("Worker Story", "Leave and Accrual Outcome", "server-owned leave output"),
    "payroll_bases_connection": ("Payroll Bases & Totals", "worked hours", "basis quantity"),
    "outstanding_hardening": ("outstanding hardening", "Leave Source Model", "leave-processing UI"),
}

LEAVE_REQUESTS_WORKFLOW_GROUP_KEY_TERMS = {
    "leave_request_purpose": ("Leave Requests / Leave Workflow", "Leave Request", "LeaveRequest", "leave workflow", "governed leave request workflow"),
    "request_creation_and_draft_editing": ("Leave Request", "create leave request", "draft leave", "draft editing", "leave request preview"),
    "status_transitions_and_idempotency": ("leave status", "status transitions", "IdempotencyKey", "idempotency", "idempotent leave"),
    "submission_review_approval_reopen": ("leave submission", "submit leave", "approve leave", "reject leave", "reopen leave", "review leave"),
    "overlap_and_shortfall_handling": ("leave overlap", "overlap handling", "shortfall substitution", "shortfall", "substitution"),
    "taken_leave_valuation_and_hard_fail": ("TAKEN leave", "leave valuation", "hard fail", "hard-fail", "leave valuation basis"),
    "leave_ledger_posting": ("LeaveLedger", "leave posting", "LeaveLedger posting", "leave balance", "leave ledger rows"),
    "leave_source_and_applicability_relationship": ("Leave Source Model", "leave applicability", "LeaveTypeRule", "source applicability", "leave source"),
    "worker_story_and_payrun_relationship": ("Worker Story", "PayRun", "leave request payment", "Leave and Accrual Outcome", "worker leave evidence"),
    "finalisation_and_readiness_relationship": ("finalisation readiness", "leave readiness", "missing leave output", "PayRun finalisation", "readiness"),
    "outstanding_hardening": ("Leave Requests / Leave Workflow", "outstanding hardening", "leave workflow", "request ownership", "leave hardening"),
}

LEAVE_REQUESTS_WORKFLOW_GROUP_SIGNAL_TERMS = {
    "leave_request_purpose": ("Leave Requests / Leave Workflow", "Leave Request", "leave workflow"),
    "request_creation_and_draft_editing": ("create leave request", "draft leave", "leave request preview"),
    "status_transitions_and_idempotency": ("leave status", "status transitions", "IdempotencyKey"),
    "submission_review_approval_reopen": ("submit leave", "approve leave", "reject leave", "reopen leave"),
    "overlap_and_shortfall_handling": ("leave overlap", "shortfall substitution", "substitution"),
    "taken_leave_valuation_and_hard_fail": ("TAKEN leave", "leave valuation", "hard fail"),
    "leave_ledger_posting": ("LeaveLedger", "leave posting", "leave balance"),
    "leave_source_and_applicability_relationship": ("Leave Source Model", "leave applicability", "LeaveTypeRule"),
    "worker_story_and_payrun_relationship": ("Worker Story", "PayRun", "Leave and Accrual Outcome"),
    "finalisation_and_readiness_relationship": ("finalisation readiness", "leave readiness", "missing leave output"),
    "outstanding_hardening": ("Leave Requests / Leave Workflow", "outstanding hardening", "leave workflow"),
}

PUBLIC_HOLIDAYS_GROUP_KEY_TERMS = {
    "public_holiday_source_and_calendar": (
        "PublicHoliday",
        "Public Holiday",
        "PublicHolidayGroup",
        "Public Holiday Group",
        "public holiday calendar",
        "observed day",
        "public holiday override",
        "governed reference configuration",
    ),
    "worksite_state_and_applicability_context": (
        "public holiday",
        "PublicHolidayGroup",
        "Worksite",
        "WorksitePosition",
        "EmployeeAppointment",
        "worker",
        "applies to a worker",
        "state",
        "jurisdiction",
        "location context",
        "applicability context",
        "employer liabilities",
        "on-costs",
    ),
    "payroll_treatment_and_decision_story": (
        "public holiday payroll treatment",
        "deterministic payroll interpretation",
        "public holiday treatment decisions",
        "public holiday decision",
        "entitlement decision",
        "treatment decision",
        "Decision Story",
        "Payroll Output",
        "deterministic payroll services",
    ),
    "leave_interaction_and_deducts_on_public_holiday": (
        "DeductsOnPublicHoliday",
        "Deducts On Public Holiday",
        "public holiday leave treatment",
        "leave request",
        "leave preview",
        "LeaveLedger",
        "leave posting",
    ),
    "worker_story_admin_queue_and_finalisation": (
        "public holiday",
        "Worker Story",
        "Decision Story",
        "Payroll Output",
        "payroll evidence",
        "source/context visibility",
        "PayRun Admin Queue",
        "Worker Attention",
        "Finalisation Readiness",
        "public holiday configuration",
        "NEEDS_CONFIGURATION",
        "source context missing",
        "operator evidence",
    ),
}

PUBLIC_HOLIDAYS_GROUP_SIGNAL_TERMS = {
    "public_holiday_source_and_calendar": ("PublicHoliday", "PublicHolidayGroup", "public holiday calendar"),
    "worksite_state_and_applicability_context": ("public holiday", "Worksite", "state", "location context", "applies to a worker"),
    "payroll_treatment_and_decision_story": ("public holiday payroll treatment", "Decision Story", "Payroll Output", "deterministic payroll interpretation"),
    "leave_interaction_and_deducts_on_public_holiday": ("DeductsOnPublicHoliday", "public holiday leave treatment", "LeaveLedger"),
    "worker_story_admin_queue_and_finalisation": ("public holiday", "Worker Story", "Finalisation Readiness", "NEEDS_CONFIGURATION"),
}

ROSTERS_PATTERNS_SCHEDULING_GROUP_KEY_TERMS = {
    "roster_pattern_source_and_configuration": (
        "Roster",
        "Rosters",
        "Pattern",
        "PatternDay",
        "Pattern Day",
        "EmployeeAppointmentPattern",
        "Employee Appointment Pattern",
        "roster schedule configuration",
        "expected work context",
        "governed configuration evidence",
    ),
    "appointment_worksite_and_applicability_context": (
        "Roster",
        "Pattern",
        "EmployeeAppointment",
        "WorksitePosition",
        "Worksite",
        "state",
        "public holiday context",
        "assignment context",
        "applicability context",
    ),
    "ordinary_hours_leave_basis_and_public_holiday_context": (
        "ordinary hours",
        "ordinary-hours",
        "leave basis minutes",
        "schedule pattern relationship",
        "public holiday",
        "leave interaction",
        "roster-based basis",
        "deferred roster-based basis hardening",
    ),
    "payroll_interpretation_and_worker_story_relationship": (
        "scheduling context",
        "payroll interpretation",
        "ObjectTime comparison",
        "expected schedule",
        "actual worked time",
        "Worker Story",
        "Decision Story",
        "Payroll Output",
        "source truth",
    ),
    "admin_queue_finalisation_and_readiness_relationship": (
        "missing schedule",
        "missing pattern",
        "configuration gaps",
        "Worker Attention",
        "PayRun Admin Queue",
        "Admin Queue",
        "Finalisation Readiness",
        "readiness evidence",
        "NEEDS_CONFIGURATION",
    ),
}

ROSTERS_PATTERNS_SCHEDULING_GROUP_SIGNAL_TERMS = {
    "roster_pattern_source_and_configuration": ("Roster", "Pattern", "PatternDay", "EmployeeAppointmentPattern"),
    "appointment_worksite_and_applicability_context": ("EmployeeAppointment", "WorksitePosition", "Worksite", "assignment context"),
    "ordinary_hours_leave_basis_and_public_holiday_context": ("ordinary hours", "leave basis minutes", "public holiday"),
    "payroll_interpretation_and_worker_story_relationship": ("payroll interpretation", "ObjectTime", "Worker Story", "Payroll Output"),
    "admin_queue_finalisation_and_readiness_relationship": ("Worker Attention", "Admin Queue", "Finalisation Readiness", "NEEDS_CONFIGURATION"),
}

AWARD_POSITIONS_CLASSIFICATIONS_GROUP_KEY_TERMS = {
    "award_position_classification_source_and_build": (
        "AwardPosition",
        "Award Position",
        "AwardPositionClass",
        "Award Position Class",
        "PositionClass",
        "Position Class",
        "classification levels",
        "position groups",
        "pay guide",
        "class evidence",
        "award build extraction",
        "deterministic extraction hardening",
    ),
    "appointment_position_and_worksite_assignment": (
        "EmployeeAppointment",
        "Employee Appointment",
        "WorksitePosition",
        "Worksite Position",
        "Position",
        "Worksite",
        "worker assignment",
        "assignment context",
        "employment classification",
    ),
    "payroll_interpretation_rate_and_decision_story": (
        "classification context",
        "payroll interpretation",
        "RateSource",
        "Rate Story",
        "Decision Story",
        "Payroll Output",
        "calculated line evidence",
    ),
    "comparison_remediation_and_classification_lenses": (
        "comparator classification",
        "award comparison",
        "comparison remediation",
        "imported classification mapping",
        "classification lenses",
        "comparison classes",
        "primary appointment class",
    ),
    "worker_story_admin_queue_and_readiness_relationship": (
        "Worker Story",
        "Admin Queue",
        "Worker Attention",
        "Finalisation Readiness",
        "configuration gaps",
        "NEEDS_CONFIGURATION",
        "evidence visibility",
    ),
}

AWARD_POSITIONS_CLASSIFICATIONS_GROUP_SIGNAL_TERMS = {
    "award_position_classification_source_and_build": ("AwardPosition", "AwardPositionClass", "classification levels", "pay guide"),
    "appointment_position_and_worksite_assignment": ("EmployeeAppointment", "WorksitePosition", "Position", "Worksite"),
    "payroll_interpretation_rate_and_decision_story": ("classification context", "RateSource", "Rate Story", "Decision Story"),
    "comparison_remediation_and_classification_lenses": ("comparator classification", "classification lenses", "primary appointment class"),
    "worker_story_admin_queue_and_readiness_relationship": ("Worker Story", "Worker Attention", "Finalisation Readiness", "NEEDS_CONFIGURATION"),
}

FINALISATION_READINESS_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Finalisation Readiness",
        "governed readiness gate",
        "assurance gate",
        "not payroll calculation truth",
        "green means done",
    ),
    "blockers_warnings_and_green_state": (
        "blockers",
        "warnings",
        "red blockers",
        "amber warnings",
        "green",
        "ready",
        "cleared",
    ),
    "current_effective_payroll_output": (
        "current-effective payroll output",
        "stale",
        "superseded",
        "current truth",
        "finalised as current truth",
    ),
    "worker_attention_and_admin_queue": (
        "Worker Attention",
        "Admin Queue",
        "worker-level blockers",
        "worker-level warnings",
        "ready actions",
    ),
    "payroll_bases_readiness": (
        "Payroll Bases readiness",
        "Payroll Bases & Totals",
        "unresolved basis evidence",
        "stale basis evidence",
        "finalisation",
    ),
    "leave_readiness": (
        "leave readiness",
        "missing leave output",
        "leave valuation basis",
        "LeaveLedger",
        "TAKEN leave",
    ),
    "tax_deduction_and_payment_readiness": (
        "tax readiness",
        "deduction readiness",
        "negative net pay",
        "payment destination readiness",
        "gross-to-net",
    ),
    "payment_execution_and_bank_readiness": (
        "payment execution readiness",
        "payment readiness",
        "bank readiness",
        "gross-to-net readiness",
        "payment destination",
    ),
    "finalised_outcome_truth": (
        "finalised outcome truth",
        "finalised outcome",
        "finalised totals",
        "durable payment outcome memory",
        "finalised payroll truth",
    ),
    "warning_acknowledgement_and_audit": (
        "warning acknowledgement",
        "warning acknowledgment",
        "finalisation audit",
        "reviewed",
        "accepted",
        "unresolved",
    ),
    "worker_story_and_review_surfaces": (
        "Worker Story",
        "review surfaces",
        "readiness evidence",
        "worker-specific issues",
        "Movement Review",
        "Admin Queue",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "warning acknowledgement",
        "WorkerAttention schemas",
        "finalisation policy",
        "server-owned operation",
        "readiness evidence",
        "payment execution readiness",
        "contract tests",
    ),
}

FINALISATION_READINESS_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Finalisation Readiness", "governed readiness gate", "assurance gate"),
    "blockers_warnings_and_green_state": ("blockers", "warnings", "green"),
    "current_effective_payroll_output": ("current-effective payroll output", "stale", "current truth"),
    "worker_attention_and_admin_queue": ("Worker Attention", "Admin Queue", "ready actions"),
    "payroll_bases_readiness": ("Payroll Bases readiness", "Payroll Bases & Totals", "stale basis evidence"),
    "leave_readiness": ("leave readiness", "missing leave output", "leave valuation basis"),
    "tax_deduction_and_payment_readiness": ("tax readiness", "deduction readiness", "negative net pay"),
    "payment_execution_and_bank_readiness": ("payment execution readiness", "payment readiness", "bank readiness"),
    "finalised_outcome_truth": ("finalised outcome", "finalised totals", "durable payment outcome memory"),
    "warning_acknowledgement_and_audit": ("warning acknowledgement", "finalisation audit", "reviewed"),
    "worker_story_and_review_surfaces": ("Worker Story", "review surfaces", "readiness evidence"),
    "outstanding_hardening": ("outstanding hardening", "finalisation policy", "payment execution readiness"),
}

LEAVE_SOURCE_MODEL_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Leave Source Model",
        "governed applicability",
        "source-truth layer",
        "leave applies",
        "worker context",
    ),
    "applicability_vs_rule_content": (
        "applicability",
        "rule content",
        "LeaveTypeRule",
        "policy calculation content",
        "source truth",
    ),
    "leave_type_rule_limitations": (
        "LeaveTypeRule",
        "final applicability truth",
        "active LeaveTypeRule",
        "every worker",
        "leave output",
    ),
    "contact_vs_appointment_scope": (
        "Contact scope",
        "EmployeeAppointment scope",
        "appointment-aware leave",
        "contact-level",
        "appointment-level",
    ),
    "source_dimensions_and_precedence": (
        "Account",
        "EmploymentType",
        "WorksitePosition",
        "Worksite",
        "EmployeeAppointment",
        "Contact",
        "AwardPositionClass",
        "AwardPosition",
        "Position",
        "Award",
        "State",
        "precedence",
    ),
    "leave_accrual_connection": (
        "leave accrual",
        "source applicability decisions",
        "accrual",
        "consume source",
        "infer ad hoc",
    ),
    "leave_request_and_payment_effects_connection": (
        "leave request",
        "payment effects",
        "source applicability decisions",
        "leave ownership",
        "request ownership",
    ),
    "worker_story_connection": (
        "Worker Story",
        "leave chapters",
        "source applicability decisions",
        "leave output",
        "warnings",
    ),
    "command_centre_and_finalisation_connection": (
        "Command Centre",
        "Finalisation Readiness",
        "PayRun finalisation warnings",
        "leave readiness",
        "honestly",
    ),
    "readiness_and_missing_output_detection": (
        "leave readiness",
        "missing leave output",
        "leave does not apply",
        "leave output is missing",
        "source truth",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "planned model",
        "required model",
        "not complete",
        "runtime capability",
    ),
}

LEAVE_SOURCE_MODEL_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Leave Source Model", "governed applicability", "source-truth layer"),
    "applicability_vs_rule_content": ("applicability", "LeaveTypeRule", "source truth"),
    "leave_type_rule_limitations": ("LeaveTypeRule", "final applicability truth", "active LeaveTypeRule"),
    "contact_vs_appointment_scope": ("Contact scope", "EmployeeAppointment scope", "appointment-aware leave"),
    "source_dimensions_and_precedence": ("EmploymentType", "EmployeeAppointment", "State"),
    "leave_accrual_connection": ("leave accrual", "source applicability decisions", "consume source"),
    "leave_request_and_payment_effects_connection": ("leave request", "payment effects", "source applicability decisions"),
    "worker_story_connection": ("Worker Story", "leave chapters", "source applicability decisions"),
    "command_centre_and_finalisation_connection": ("Command Centre", "Finalisation Readiness", "leave readiness"),
    "readiness_and_missing_output_detection": ("leave readiness", "missing leave output", "leave does not apply"),
    "outstanding_hardening": ("outstanding hardening", "planned model", "not complete"),
}

ONCOSTS_EMPLOYER_LIABILITIES_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "On-costs",
        "Employer Liabilities",
        "governed employer liability evidence",
        "operator meaning",
        "not reporting add-on",
    ),
    "employer_liability_not_worker_pay": (
        "employer liability",
        "not worker pay",
        "not worker net pay",
        "not payroll calculation truth",
        "Minerva does not calculate",
    ),
    "rate_source_and_date_effective_rates": (
        "RateSource",
        "date-effective rates",
        "date-effective RateSource",
        "rule-pack configuration",
        "application code",
    ),
    "award_rate_type_and_rate_type_settings": (
        "AwardRateType",
        "RateType",
        "SUPER_ONCOST",
        "PAYROLLTAX_ONCOST",
        "WORKCOVER_ONCOST",
        "award defaults",
    ),
    "governed_basis_membership": (
        "governed basis membership",
        "bucket membership",
        "basis membership",
        "raw flags",
        "runtime basis decisions",
    ),
    "super_payroll_tax_and_workcover_wic": (
        "superannuation on-cost",
        "payroll tax on-cost",
        "WorkCover",
        "WIC",
        "jurisdiction",
    ),
    "state_worksite_and_runtime_location_resolution": (
        "state",
        "worksite",
        "runtime location",
        "state-scoped RateSource",
        "state-scoped employer liabilities",
    ),
    "payrun_output_and_worker_story_connection": (
        "PayRun output",
        "Worker Story",
        "worker-payable lines",
        "employer liability lines",
        "on-cost evidence",
    ),
    "payroll_bases_connection": (
        "Payroll Bases & Totals",
        "governed basis evidence",
        "liability calculations",
        "basis evidence",
        "basis totals",
    ),
    "finalisation_and_readiness_connection": (
        "Finalisation Readiness",
        "unresolved basis",
        "liability configuration",
        "policy requires",
        "readiness",
    ),
    "demo_fallback_vs_production_truth": (
        "demo fallback",
        "account-wide fallback",
        "RateSource rows",
        "production truth",
        "unblock demos",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "runtime state",
        "worksite resolution",
        "award creation seeding",
        "production replacement",
    ),
}

ONCOSTS_EMPLOYER_LIABILITIES_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("On-costs", "Employer Liabilities", "governed employer liability evidence"),
    "employer_liability_not_worker_pay": ("employer liability", "not worker pay", "Minerva does not calculate"),
    "rate_source_and_date_effective_rates": ("RateSource", "date-effective rates", "rule-pack configuration"),
    "award_rate_type_and_rate_type_settings": ("AwardRateType", "RateType", "SUPER_ONCOST"),
    "governed_basis_membership": ("governed basis membership", "bucket membership", "runtime basis decisions"),
    "super_payroll_tax_and_workcover_wic": ("superannuation on-cost", "payroll tax on-cost", "WorkCover"),
    "state_worksite_and_runtime_location_resolution": ("state", "worksite", "runtime location"),
    "payrun_output_and_worker_story_connection": ("PayRun output", "Worker Story", "worker-payable lines"),
    "payroll_bases_connection": ("Payroll Bases & Totals", "governed basis evidence", "basis totals"),
    "finalisation_and_readiness_connection": ("Finalisation Readiness", "unresolved basis", "liability configuration"),
    "demo_fallback_vs_production_truth": ("demo fallback", "account-wide fallback", "production truth"),
    "outstanding_hardening": ("outstanding hardening", "runtime state", "production replacement"),
}

AWARD_BUILD_EVIDENCE_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Award Build",
        "Award Evidence",
        "governed configuration",
        "traceable evidence",
        "not runtime payroll calculation",
    ),
    "award_document_and_pay_guide_sources": (
        "award document",
        "pay guide",
        "pay guide evidence",
        "source evidence",
        "row column page evidence",
    ),
    "rate_type_and_award_rate_type_creation": (
        "RateType",
        "Rate Type",
        "AwardRateType",
        "Award Rate Type",
        "stable conceptual pay type",
        "award-scoped treatment",
    ),
    "rate_source_and_date_effective_rate_evidence": (
        "RateSource",
        "date-effective",
        "rate amounts",
        "rate evidence",
        "hardcoded rates",
    ),
    "classification_position_and_class_evidence": (
        "classification",
        "position",
        "class evidence",
        "deterministically derived",
        "reviewed",
        "not guessed",
    ),
    "allowances_penalties_and_conditions": (
        "allowances",
        "penalties",
        "conditions",
        "shift",
        "overtime",
        "source evidence",
    ),
    "decision_evidence_index": (
        "DecisionEvidenceIndex",
        "Decision Evidence Index",
        "why a treatment",
        "why a line exists",
        "decision evidence",
    ),
    "rate_source_evidence_index": (
        "RateSourceEvidenceIndex",
        "Rate Source Evidence Index",
        "why a rate",
        "why an amount",
        "rate source evidence",
    ),
    "worker_story_decision_and_rate_story_connection": (
        "Worker Story",
        "Decision Story",
        "Rate Story",
        "award build",
        "runtime artifacts",
        "PayRun interpretation evidence",
    ),
    "needs_configuration_and_build_status": (
        "NEEDS_CONFIGURATION",
        "award build status",
        "missing evidence",
        "missing configuration",
        "valid build outcome",
    ),
    "durable_award_evidence_set": (
        "AwardEvidenceSet",
        "Durable AwardEvidenceSet",
        "durable evidence",
        "artifact based",
        "file based",
        "future hardening",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "semantic table classification",
        "durable evidence sets",
        "parser routing",
        "conditional award regimes",
        "source evidence coverage",
    ),
}

AWARD_BUILD_EVIDENCE_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Award Build", "Award Evidence", "governed configuration"),
    "award_document_and_pay_guide_sources": ("award document", "pay guide", "source evidence"),
    "rate_type_and_award_rate_type_creation": ("RateType", "AwardRateType", "stable conceptual pay type"),
    "rate_source_and_date_effective_rate_evidence": ("RateSource", "date-effective", "rate evidence"),
    "classification_position_and_class_evidence": ("classification", "position", "not guessed"),
    "allowances_penalties_and_conditions": ("allowances", "penalties", "conditions"),
    "decision_evidence_index": ("DecisionEvidenceIndex", "Decision Evidence Index", "why a treatment"),
    "rate_source_evidence_index": ("RateSourceEvidenceIndex", "Rate Source Evidence Index", "why a rate"),
    "worker_story_decision_and_rate_story_connection": ("Worker Story", "Decision Story", "Rate Story"),
    "needs_configuration_and_build_status": ("NEEDS_CONFIGURATION", "missing configuration", "valid build outcome"),
    "durable_award_evidence_set": ("AwardEvidenceSet", "Durable AwardEvidenceSet", "durable evidence"),
    "outstanding_hardening": ("outstanding hardening", "semantic table classification", "parser routing"),
}

IMPORTS_ACTUALS_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Imports / Actuals",
        "Imports and Actuals",
        "governed imported evidence",
        "external source evidence",
        "not calculated interpreter truth",
    ),
    "imported_timesheet_source_truth": (
        "imported timesheets",
        "timesheet source truth",
        "ObjectTime",
        "work evidence",
        "validation and mapping",
    ),
    "imported_payroll_actuals_lane": (
        "imported payroll actuals",
        "payroll actuals",
        "actuals lane",
        "external outcome lane",
        "calculated interpreter output",
    ),
    "source_system_mapping_and_validation": (
        "source-system mapping",
        "source system mapping",
        "validation",
        "workers",
        "dates",
        "source rows",
    ),
    "pay_code_and_rate_type_mapping": (
        "pay code mapping",
        "source-system pay code",
        "RateType mapping",
        "platform concepts",
        "unmapped actuals",
    ),
    "position_classification_mapping": (
        "ImportedPositionClassificationMap",
        "position mapping",
        "classification mapping",
        "source-system classification",
        "source-system position",
    ),
    "objecttime_and_source_truth_connection": (
        "ObjectTime source truth",
        "ObjectTime",
        "source truth",
        "source row",
        "import provenance",
    ),
    "comparison_and_remediation_connection": (
        "Comparison / Remediation",
        "primary calculated",
        "comparator calculated",
        "imported actual lanes",
        "variance",
    ),
    "reconciliation_and_movement_review_connection": (
        "reconciliation",
        "Movement Review",
        "imported actuals",
        "source evidence",
        "review outcomes",
    ),
    "worker_story_and_admin_queue_connection": (
        "Worker Story",
        "Admin Queue",
        "import provenance",
        "mapping issues",
        "unmapped actuals",
        "missing classifications",
    ),
    "evidence_provenance_and_audit": (
        "evidence provenance",
        "audit",
        "source file",
        "source row",
        "import run",
        "mapping decision",
        "validation status",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "actuals lane model",
        "import mapping UI",
        "comparison-line models",
        "source-system classification mapping",
        "source-row evidence",
        "validation workflows",
    ),
}

IMPORTS_ACTUALS_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Imports / Actuals", "governed imported evidence", "external source evidence"),
    "imported_timesheet_source_truth": ("imported timesheets", "ObjectTime", "validation and mapping"),
    "imported_payroll_actuals_lane": ("imported payroll actuals", "actuals lane", "external outcome lane"),
    "source_system_mapping_and_validation": ("source-system mapping", "validation", "source rows"),
    "pay_code_and_rate_type_mapping": ("pay code mapping", "RateType mapping", "unmapped actuals"),
    "position_classification_mapping": ("ImportedPositionClassificationMap", "position mapping", "classification mapping"),
    "objecttime_and_source_truth_connection": ("ObjectTime source truth", "source row", "import provenance"),
    "comparison_and_remediation_connection": ("Comparison / Remediation", "primary calculated", "imported actual lanes"),
    "reconciliation_and_movement_review_connection": ("reconciliation", "Movement Review", "review outcomes"),
    "worker_story_and_admin_queue_connection": ("Worker Story", "Admin Queue", "mapping issues"),
    "evidence_provenance_and_audit": ("evidence provenance", "source file", "import run"),
    "outstanding_hardening": ("outstanding hardening", "actuals lane model", "import mapping UI"),
}

OBJECTTIME_SOURCE_TRUTH_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "ObjectTime / Source Truth",
        "ObjectTime",
        "Source Truth",
        "governed source evidence",
        "not payroll calculation truth",
    ),
    "objecttime_as_source_evidence": (
        "ObjectTime",
        "source evidence",
        "work time",
        "source row",
        "inclusion context",
    ),
    "payrun_inclusion_and_source_truth": (
        "PayRun inclusion",
        "SourceTruth",
        "Source Truth",
        "source inclusion",
        "belongs in a PayRun",
    ),
    "imported_and_generated_source_rows": (
        "imported source rows",
        "generated source rows",
        "source row",
        "provenance",
        "validation mapping status",
    ),
    "source_truth_vs_worked_hours": (
        "SourceTruth",
        "WorkedHours",
        "worked hours",
        "raw span hours",
        "span hours",
        "interpreted payable hours",
    ),
    "current_effective_output_connection": (
        "current-effective output",
        "current-effective payroll output",
        "processed source truth",
        "payroll outcome",
        "current-effective truth",
    ),
    "worker_story_connection": (
        "Worker Story",
        "Source Truth",
        "source inclusion",
        "calculated payroll outcome",
        "Decision Story",
    ),
    "payroll_bases_and_leave_accrual_connection": (
        "Payroll Bases & Totals",
        "leave accrual",
        "processed payroll",
        "bucket evidence",
        "raw source span duration",
    ),
    "comparison_movement_and_replay_connection": (
        "Comparison / Remediation",
        "Movement Review",
        "Retro / Replay",
        "source truth",
        "historical current-effective distinctions",
    ),
    "corrections_dirty_contacts_and_reprocessing": (
        "correction audit",
        "dirty contact",
        "dirty PayRunContact",
        "reprocessing",
        "source truth correction",
    ),
    "evidence_provenance_and_audit": (
        "evidence provenance",
        "audit",
        "source file",
        "source row",
        "ObjectTime",
        "correction history",
        "evidence story",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "command-centre source hours cleanup",
        "schema contracts",
        "dependency detection",
        "source-truth provenance coverage",
    ),
}

OBJECTTIME_SOURCE_TRUTH_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("ObjectTime / Source Truth", "governed source evidence", "not payroll calculation truth"),
    "objecttime_as_source_evidence": ("ObjectTime", "source evidence", "source row"),
    "payrun_inclusion_and_source_truth": ("PayRun inclusion", "SourceTruth", "source inclusion"),
    "imported_and_generated_source_rows": ("imported source rows", "generated source rows", "provenance"),
    "source_truth_vs_worked_hours": ("SourceTruth", "WorkedHours", "raw span hours"),
    "current_effective_output_connection": ("current-effective output", "processed source truth", "payroll outcome"),
    "worker_story_connection": ("Worker Story", "Source Truth", "calculated payroll outcome"),
    "payroll_bases_and_leave_accrual_connection": ("Payroll Bases & Totals", "leave accrual", "bucket evidence"),
    "comparison_movement_and_replay_connection": ("Comparison / Remediation", "Movement Review", "Retro / Replay"),
    "corrections_dirty_contacts_and_reprocessing": ("correction audit", "dirty contact", "reprocessing"),
    "evidence_provenance_and_audit": ("evidence provenance", "source file", "correction history"),
    "outstanding_hardening": ("outstanding hardening", "schema contracts", "dependency detection"),
}

CONTACTS_EMPLOYEE_APPOINTMENTS_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Contacts / Employee Appointments",
        "Contact",
        "EmployeeAppointment",
        "worker identity context",
        "employment context",
        "not payroll calculation truth",
    ),
    "contact_identity_and_worker_context": (
        "Contact",
        "worker identity",
        "person payroll identity",
        "worker context",
        "payroll identity context",
    ),
    "employee_appointment_as_employment_assignment": (
        "EmployeeAppointment",
        "Employee Appointment",
        "employment assignment",
        "work assignment",
        "position worksite classification award",
    ),
    "appointment_scope_and_payrun_admission": (
        "appointment scope",
        "PayRun admission",
        "source truth",
        "appointment context",
        "worker inclusion",
    ),
    "award_classification_and_position_context": (
        "award classification",
        "AwardPositionClass",
        "WorksitePosition",
        "Position",
        "classification evidence",
        "appointment",
    ),
    "worksite_state_and_runtime_location": (
        "worksite",
        "state",
        "runtime location",
        "worksite state",
        "state evidence",
        "appointment",
    ),
    "objecttime_and_source_truth_connection": (
        "ObjectTime",
        "source truth",
        "source rows",
        "appointments",
        "contacts",
        "worker inclusion",
    ),
    "leave_source_and_accrual_connection": (
        "leave source",
        "leave applicability",
        "leave accrual",
        "contact scope",
        "appointment scope",
    ),
    "worker_story_and_contact_history_connection": (
        "Worker Story",
        "Contact history",
        "finalised payroll outcome memory",
        "cumulative movement",
        "source truth context",
    ),
    "worker_readiness_tax_bank_deduction_payment": (
        "worker readiness",
        "tax declarations",
        "bank",
        "payment allocation",
        "deductions",
        "obligations",
    ),
    "dirty_contact_and_reprocessing": (
        "dirty contact",
        "dirty contacts",
        "reprocessing",
        "PayRun output unsafe",
        "payroll-affecting changes",
    ),
    "comparison_and_classification_lenses": (
        "comparison",
        "classification lens",
        "classification lenses",
        "appointment",
        "duplicate full appointments",
        "remediation",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "GUID boundary",
        "schema contracts",
        "contact-level history",
        "WorkerAttention schemas",
        "classification lenses",
        "dirty-contact propagation",
    ),
}

CONTACTS_EMPLOYEE_APPOINTMENTS_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Contacts / Employee Appointments", "Contact", "EmployeeAppointment"),
    "contact_identity_and_worker_context": ("Contact", "worker identity", "payroll identity context"),
    "employee_appointment_as_employment_assignment": ("EmployeeAppointment", "employment assignment", "work assignment"),
    "appointment_scope_and_payrun_admission": ("appointment scope", "PayRun admission", "worker inclusion"),
    "award_classification_and_position_context": ("AwardPositionClass", "WorksitePosition", "classification evidence"),
    "worksite_state_and_runtime_location": ("worksite", "state", "runtime location"),
    "objecttime_and_source_truth_connection": ("ObjectTime", "source truth", "worker inclusion"),
    "leave_source_and_accrual_connection": ("leave source", "leave applicability", "appointment scope"),
    "worker_story_and_contact_history_connection": ("Worker Story", "Contact history", "finalised payroll outcome memory"),
    "worker_readiness_tax_bank_deduction_payment": ("worker readiness", "tax declarations", "payment allocation"),
    "dirty_contact_and_reprocessing": ("dirty contact", "reprocessing", "PayRun output unsafe"),
    "comparison_and_classification_lenses": ("comparison", "classification lens", "duplicate full appointments"),
    "outstanding_hardening": ("outstanding hardening", "GUID boundary", "WorkerAttention schemas"),
}

PROCESS_PERIOD_PAYRUN_LIFECYCLE_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Process Periods / PayRun Lifecycle",
        "ProcessPeriod",
        "governed payroll-period context",
        "payment-event lifecycle evidence",
        "not payroll calculation truth",
        "not a generic date range",
    ),
    "process_period_and_group_context": (
        "ProcessPeriod",
        "Process Period",
        "ProcessPeriodGroup",
        "Process Period Group",
        "recurring calendar policy",
        "payment policy context",
    ),
    "open_not_open_closed_lifecycle": (
        "open",
        "not-open",
        "not open",
        "closed",
        "closed dominates open",
        "period lifecycle",
    ),
    "close_rolls_forward": (
        "close rolls forward",
        "roll forward",
        "close period",
        "open next period",
        "create next period",
        "period close",
        "implemented",
    ),
    "payment_date_and_calendar_policy": (
        "PaymentDate",
        "payment date",
        "calendar policy",
        "tax/PAYG",
        "payment context",
        "governed derived",
        "not hardcoded",
    ),
    "payrun_creation_and_admission": (
        "PayRun creation",
        "PayRun admission",
        "process-period context",
        "worker inclusion",
        "admission is not processing",
        "payment event",
    ),
    "run_type_and_run_purpose": (
        "RunType",
        "RunPurpose",
        "separate",
        "run type",
        "run purpose",
        "payment/processing event",
    ),
    "regular_supplementary_retro_distinction": (
        "regular PayRun",
        "supplementary PayRun",
        "retro PayRun",
        "termination PayRun",
        "reversal PayRun",
        "adjustment PayRun",
        "different lifecycle concepts",
    ),
    "payrun_contact_lifecycle": (
        "PayRunContact",
        "worker participation",
        "admission",
        "processing state",
        "operational state layer",
        "dirty PayRunContact",
    ),
    "current_effective_output_and_finalisation": (
        "current-effective output",
        "current-effective payroll output",
        "stale",
        "superseded",
        "current truth",
        "finalisation readiness",
    ),
    "payment_execution_and_period_close": (
        "payment execution",
        "period close",
        "downstream governed outcome",
        "payment outcome",
        "not payroll calculation",
        "closed period",
    ),
    "worker_story_admin_queue_and_movement_review_connection": (
        "Worker Story",
        "PayRun Admin Queue",
        "Admin Queue",
        "Movement Review",
        "worker participation",
        "readiness",
        "review implications",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "operation trackers",
        "lifecycle contracts",
        "supplementary/retro policies",
        "payment execution",
        "finalisation warning acknowledgement",
        "broader contract tests",
    ),
}

PROCESS_PERIOD_PAYRUN_LIFECYCLE_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Process Periods / PayRun Lifecycle", "ProcessPeriod", "not payroll calculation truth"),
    "process_period_and_group_context": ("ProcessPeriod", "ProcessPeriodGroup", "calendar policy"),
    "open_not_open_closed_lifecycle": ("open", "not-open", "closed"),
    "close_rolls_forward": ("close rolls forward", "roll forward", "open next period"),
    "payment_date_and_calendar_policy": ("PaymentDate", "payment date", "governed derived"),
    "payrun_creation_and_admission": ("PayRun creation", "PayRun admission", "admission is not processing"),
    "run_type_and_run_purpose": ("RunType", "RunPurpose", "separate"),
    "regular_supplementary_retro_distinction": ("regular PayRun", "supplementary PayRun", "retro PayRun"),
    "payrun_contact_lifecycle": ("PayRunContact", "worker participation", "operational state layer"),
    "current_effective_output_and_finalisation": ("current-effective output", "stale", "finalisation readiness"),
    "payment_execution_and_period_close": ("payment execution", "period close", "downstream governed outcome"),
    "worker_story_admin_queue_and_movement_review_connection": ("Worker Story", "PayRun Admin Queue", "Movement Review"),
    "outstanding_hardening": ("outstanding hardening", "operation trackers", "lifecycle contracts"),
}

COSTING_GL_CONSEQUENCE_GROUP_KEY_TERMS = {
    "purpose_and_operator_meaning": (
        "Costing / GL Consequence Evidence",
        "Costing",
        "GL consequence",
        "financial consequence evidence",
        "downstream financial consequence evidence",
        "not payroll calculation truth",
    ),
    "downstream_not_payroll_calculation_truth": (
        "downstream financial consequence",
        "not payroll calculation truth",
        "not payment execution",
        "Minerva does not post GL",
        "does not calculate costing",
    ),
    "finalised_payroll_outcome_source": (
        "finalised payroll outcome",
        "finalised payroll outcomes",
        "finalised gross-to-net",
        "payment outcome",
        "source outcome",
        "finalised truth",
    ),
    "payment_execution_and_remittance_connection": (
        "payment execution",
        "remittance",
        "payment outcome",
        "downstream payment",
        "payment execution performance",
        "period close",
    ),
    "employer_liability_and_oncost_connection": (
        "employer liabilities",
        "employer liability",
        "on-costs",
        "on costs",
        "super",
        "payroll tax",
        "WorkCover",
        "WIC",
    ),
    "deduction_obligation_and_writeoff_consequences": (
        "deductions",
        "obligations",
        "obligation write-off",
        "obligation writeoff",
        "forgiveness",
        "balance reduction",
        "material adjustment",
        "GL/provision/costing treatment",
    ),
    "comparison_remediation_variance_connection": (
        "Comparison / Remediation",
        "remediation variance",
        "variance line",
        "remediation top-up",
        "downstream tax",
        "super",
        "payroll tax",
        "WIC",
        "costing treatment",
    ),
    "leave_valuation_and_accrual_connection": (
        "leave valuation",
        "leave accrual",
        "leave valuation basis",
        "LeaveLedger",
        "accrual evidence",
        "costing flow",
    ),
    "negative_net_pay_and_out_of_pay_consequences": (
        "negative net pay",
        "recoveries",
        "obligations",
        "write-offs",
        "out-of-pay",
        "out of pay",
        "financial consequences",
    ),
    "audit_story_and_financial_evidence": (
        "audit story",
        "financial evidence",
        "source outcome",
        "reason",
        "treatment",
        "amount",
        "ledger status",
        "costing status",
        "deferred accounting design status",
    ),
    "deferred_costing_slice_boundary": (
        "deferred costing slice",
        "future costing slice",
        "later/final slice",
        "not completed costing engine",
        "status-honest",
        "deferred accounting",
    ),
    "outstanding_hardening": (
        "outstanding hardening",
        "costing engine",
        "GL posting",
        "remediation downstream treatment",
        "negative net pay financial treatment",
        "obligation write-off",
        "contract tests",
    ),
}

COSTING_GL_CONSEQUENCE_GROUP_SIGNAL_TERMS = {
    "purpose_and_operator_meaning": ("Costing / GL Consequence Evidence", "GL consequence", "financial consequence evidence"),
    "downstream_not_payroll_calculation_truth": ("downstream financial consequence", "not payroll calculation truth", "Minerva does not post GL"),
    "finalised_payroll_outcome_source": ("finalised payroll outcome", "finalised gross-to-net", "source outcome"),
    "payment_execution_and_remittance_connection": ("payment execution", "remittance", "payment outcome"),
    "employer_liability_and_oncost_connection": ("employer liabilities", "on-costs", "payroll tax"),
    "deduction_obligation_and_writeoff_consequences": ("obligation write-off", "obligations", "GL/provision/costing treatment"),
    "comparison_remediation_variance_connection": ("remediation variance", "variance line", "costing treatment"),
    "leave_valuation_and_accrual_connection": ("leave valuation", "leave accrual", "LeaveLedger"),
    "negative_net_pay_and_out_of_pay_consequences": ("negative net pay", "out-of-pay", "financial consequences"),
    "audit_story_and_financial_evidence": ("audit story", "financial evidence", "costing status"),
    "deferred_costing_slice_boundary": ("deferred costing slice", "future costing slice", "not completed costing engine"),
    "outstanding_hardening": ("outstanding hardening", "costing engine", "GL posting"),
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


def _is_worker_attention_issue_resolution_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Worker Attention")


def _is_gross_to_net_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Gross-to-Net")


def _is_rate_source_rate_story_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("RateSource / Rate Story")


def _is_decision_story_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Decision Story")


def _is_payroll_output_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Payroll Output")


def _is_contact_payroll_history_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Contact Payroll History")


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


def _is_payment_execution_remittance_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Payment Execution / Remittance") or group.group_id in {
        "finalised_gross_to_net_source",
        "worker_net_pay_and_bank_allocation",
        "payment_destination_readiness",
        "negative_net_pay_and_obligation_interaction",
        "deduction_and_third_party_remittance",
        "payment_file_generation_and_period_close",
        "remittance_batching_and_reconciliation",
        "worker_attention_and_admin_queue_connection",
        "worker_story_and_audit_evidence",
    }


def _is_leave_accrual_processing_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Leave Accrual / Processing")


def _is_leave_requests_workflow_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Leave Requests / Leave Workflow")


def _is_public_holidays_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Public Holidays")


def _is_rosters_patterns_scheduling_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Rosters / Patterns / Scheduling")


def _is_award_positions_classifications_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Award Positions / Classifications")


def _is_finalisation_readiness_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Finalisation Readiness")


def _is_leave_source_model_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Leave Source Model")


def _is_oncosts_employer_liabilities_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("On-costs / Employer Liabilities")


def _is_award_build_evidence_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Award Build / Award Evidence")


def _is_imports_actuals_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Imports / Actuals")


def _is_objecttime_source_truth_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("ObjectTime / Source Truth")


def _is_contacts_employee_appointments_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Contacts / Employee Appointments")


def _is_process_period_payrun_lifecycle_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Process Periods / PayRun Lifecycle")


def _is_costing_gl_consequence_group(group: EvidenceGroup) -> bool:
    return group.label.startswith("Costing / GL Consequence Evidence")


def _costing_gl_consequence_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Costing / GL Consequence Evidence evidence"]
    detail_terms = [
        term
        for term in (
            "Costing / GL Consequence Evidence",
            "Costing",
            "GL consequence",
            "financial consequence evidence",
            "downstream financial consequence evidence",
            "not payroll calculation truth",
            "not payment execution",
            "Minerva does not post GL",
            "does not calculate costing",
            "finalised payroll outcome",
            "finalised payroll outcomes",
            "finalised gross-to-net",
            "payment outcome",
            "source outcome",
            "finalised truth",
            "payment execution",
            "remittance",
            "downstream payment",
            "payment execution performance",
            "period close",
            "employer liabilities",
            "employer liability",
            "on-costs",
            "on costs",
            "super",
            "payroll tax",
            "WorkCover",
            "WIC",
            "deductions",
            "obligations",
            "obligation write-off",
            "obligation writeoff",
            "forgiveness",
            "balance reduction",
            "material adjustment",
            "GL/provision/costing treatment",
            "Comparison / Remediation",
            "remediation variance",
            "variance line",
            "remediation top-up",
            "downstream tax",
            "costing treatment",
            "leave valuation",
            "leave accrual",
            "leave valuation basis",
            "LeaveLedger",
            "accrual evidence",
            "costing flow",
            "negative net pay",
            "recoveries",
            "write-offs",
            "out-of-pay",
            "out of pay",
            "financial consequences",
            "audit story",
            "financial evidence",
            "reason",
            "treatment",
            "amount",
            "ledger status",
            "costing status",
            "deferred accounting design status",
            "deferred costing slice",
            "future costing slice",
            "later/final slice",
            "not completed costing engine",
            "status-honest",
            "deferred accounting",
            "outstanding hardening",
            "costing engine",
            "GL posting",
            "remediation downstream treatment",
            "negative net pay financial treatment",
            "contract tests",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _process_period_payrun_lifecycle_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Process Periods / PayRun Lifecycle evidence"]
    detail_terms = [
        term
        for term in (
            "Process Periods / PayRun Lifecycle",
            "ProcessPeriod",
            "Process Period",
            "ProcessPeriodGroup",
            "Process Period Group",
            "governed payroll-period context",
            "payment-event lifecycle evidence",
            "not payroll calculation truth",
            "not a generic date range",
            "recurring calendar policy",
            "payment policy context",
            "open",
            "not-open",
            "not open",
            "closed",
            "closed dominates open",
            "period lifecycle",
            "close rolls forward",
            "roll forward",
            "open next period",
            "create next period",
            "implemented",
            "PaymentDate",
            "payment date",
            "calendar policy",
            "tax/PAYG",
            "payment context",
            "governed derived",
            "not hardcoded",
            "PayRun creation",
            "PayRun admission",
            "worker inclusion",
            "admission is not processing",
            "RunType",
            "RunPurpose",
            "run type",
            "run purpose",
            "regular PayRun",
            "supplementary PayRun",
            "retro PayRun",
            "termination PayRun",
            "reversal PayRun",
            "adjustment PayRun",
            "PayRunContact",
            "worker participation",
            "processing state",
            "operational state layer",
            "current-effective output",
            "current-effective payroll output",
            "stale",
            "superseded",
            "current truth",
            "finalisation readiness",
            "payment execution",
            "period close",
            "downstream governed outcome",
            "payment outcome",
            "Worker Story",
            "PayRun Admin Queue",
            "Admin Queue",
            "Movement Review",
            "readiness",
            "review implications",
            "outstanding hardening",
            "operation trackers",
            "lifecycle contracts",
            "supplementary/retro policies",
            "finalisation warning acknowledgement",
            "broader contract tests",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _contacts_employee_appointments_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Contacts / Employee Appointments evidence"]
    detail_terms = [
        term
        for term in (
            "Contacts / Employee Appointments",
            "Contact",
            "EmployeeAppointment",
            "Employee Appointment",
            "worker identity context",
            "employment context",
            "not payroll calculation truth",
            "worker identity",
            "person payroll identity",
            "worker context",
            "payroll identity context",
            "employment assignment",
            "work assignment",
            "position worksite classification award",
            "appointment scope",
            "PayRun admission",
            "source truth",
            "appointment context",
            "worker inclusion",
            "award classification",
            "AwardPositionClass",
            "WorksitePosition",
            "Position",
            "classification evidence",
            "worksite",
            "state",
            "runtime location",
            "worksite state",
            "state evidence",
            "ObjectTime",
            "source rows",
            "appointments",
            "contacts",
            "leave source",
            "leave applicability",
            "leave accrual",
            "contact scope",
            "Worker Story",
            "Contact history",
            "finalised payroll outcome memory",
            "cumulative movement",
            "source truth context",
            "worker readiness",
            "tax declarations",
            "bank",
            "payment allocation",
            "deductions",
            "obligations",
            "dirty contact",
            "dirty contacts",
            "reprocessing",
            "PayRun output unsafe",
            "payroll-affecting changes",
            "comparison",
            "classification lens",
            "classification lenses",
            "duplicate full appointments",
            "remediation",
            "outstanding hardening",
            "GUID boundary",
            "schema contracts",
            "contact-level history",
            "WorkerAttention schemas",
            "dirty-contact propagation",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _objecttime_source_truth_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved ObjectTime / Source Truth evidence"]
    detail_terms = [
        term
        for term in (
            "ObjectTime / Source Truth",
            "ObjectTime",
            "SourceTruth",
            "Source Truth",
            "governed source evidence",
            "not payroll calculation truth",
            "source evidence",
            "work time",
            "source row",
            "inclusion context",
            "PayRun inclusion",
            "source inclusion",
            "belongs in a PayRun",
            "imported source rows",
            "generated source rows",
            "provenance",
            "validation mapping status",
            "WorkedHours",
            "worked hours",
            "raw span hours",
            "span hours",
            "interpreted payable hours",
            "current-effective output",
            "current-effective payroll output",
            "processed source truth",
            "payroll outcome",
            "current-effective truth",
            "Worker Story",
            "calculated payroll outcome",
            "Decision Story",
            "Payroll Bases & Totals",
            "leave accrual",
            "processed payroll",
            "bucket evidence",
            "raw source span duration",
            "Comparison / Remediation",
            "Movement Review",
            "Retro / Replay",
            "historical current-effective distinctions",
            "correction audit",
            "dirty contact",
            "dirty PayRunContact",
            "reprocessing",
            "source truth correction",
            "evidence provenance",
            "audit",
            "source file",
            "correction history",
            "evidence story",
            "outstanding hardening",
            "command-centre source hours cleanup",
            "schema contracts",
            "dependency detection",
            "source-truth provenance coverage",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _imports_actuals_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Imports / Actuals evidence"]
    detail_terms = [
        term
        for term in (
            "Imports / Actuals",
            "Imports and Actuals",
            "governed imported evidence",
            "external source evidence",
            "not calculated interpreter truth",
            "imported timesheets",
            "timesheet source truth",
            "ObjectTime",
            "work evidence",
            "validation and mapping",
            "imported payroll actuals",
            "payroll actuals",
            "actuals lane",
            "external outcome lane",
            "calculated interpreter output",
            "source-system mapping",
            "source system mapping",
            "validation",
            "workers",
            "dates",
            "source rows",
            "pay code mapping",
            "source-system pay code",
            "RateType mapping",
            "platform concepts",
            "unmapped actuals",
            "ImportedPositionClassificationMap",
            "position mapping",
            "classification mapping",
            "source-system classification",
            "source-system position",
            "ObjectTime source truth",
            "source truth",
            "source row",
            "import provenance",
            "Comparison / Remediation",
            "primary calculated",
            "comparator calculated",
            "imported actual lanes",
            "variance",
            "reconciliation",
            "Movement Review",
            "source evidence",
            "review outcomes",
            "Worker Story",
            "Admin Queue",
            "mapping issues",
            "missing classifications",
            "evidence provenance",
            "audit",
            "source file",
            "import run",
            "mapping decision",
            "validation status",
            "outstanding hardening",
            "actuals lane model",
            "import mapping UI",
            "comparison-line models",
            "source-system classification mapping",
            "source-row evidence",
            "validation workflows",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _award_build_evidence_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Award Build / Award Evidence evidence"]
    detail_terms = [
        term
        for term in (
            "Award Build",
            "Award Evidence",
            "governed configuration",
            "traceable evidence",
            "not runtime payroll calculation",
            "award document",
            "pay guide",
            "pay guide evidence",
            "source evidence",
            "row column page evidence",
            "RateType",
            "AwardRateType",
            "stable conceptual pay type",
            "award-scoped treatment",
            "RateSource",
            "date-effective",
            "rate amounts",
            "rate evidence",
            "hardcoded rates",
            "classification",
            "position",
            "class evidence",
            "deterministically derived",
            "reviewed",
            "not guessed",
            "allowances",
            "penalties",
            "conditions",
            "shift",
            "overtime",
            "DecisionEvidenceIndex",
            "Decision Evidence Index",
            "why a treatment",
            "why a line exists",
            "RateSourceEvidenceIndex",
            "Rate Source Evidence Index",
            "why a rate",
            "why an amount",
            "Worker Story",
            "Decision Story",
            "Rate Story",
            "runtime artifacts",
            "PayRun interpretation evidence",
            "NEEDS_CONFIGURATION",
            "award build status",
            "missing evidence",
            "missing configuration",
            "valid build outcome",
            "AwardEvidenceSet",
            "Durable AwardEvidenceSet",
            "durable evidence",
            "artifact based",
            "file based",
            "future hardening",
            "outstanding hardening",
            "semantic table classification",
            "durable evidence sets",
            "parser routing",
            "conditional award regimes",
            "source evidence coverage",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _oncosts_employer_liabilities_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved On-costs / Employer Liabilities evidence"]
    detail_terms = [
        term
        for term in (
            "On-costs",
            "Employer Liabilities",
            "governed employer liability evidence",
            "operator meaning",
            "not reporting add-on",
            "employer liability",
            "not worker pay",
            "not worker net pay",
            "not payroll calculation truth",
            "Minerva does not calculate",
            "RateSource",
            "date-effective rates",
            "date-effective RateSource",
            "rule-pack configuration",
            "application code",
            "AwardRateType",
            "RateType",
            "SUPER_ONCOST",
            "PAYROLLTAX_ONCOST",
            "WORKCOVER_ONCOST",
            "award defaults",
            "governed basis membership",
            "bucket membership",
            "basis membership",
            "raw flags",
            "runtime basis decisions",
            "superannuation on-cost",
            "payroll tax on-cost",
            "WorkCover",
            "WIC",
            "jurisdiction",
            "state",
            "worksite",
            "runtime location",
            "state-scoped RateSource",
            "state-scoped employer liabilities",
            "PayRun output",
            "Worker Story",
            "worker-payable lines",
            "employer liability lines",
            "on-cost evidence",
            "Payroll Bases & Totals",
            "governed basis evidence",
            "liability calculations",
            "basis evidence",
            "basis totals",
            "Finalisation Readiness",
            "unresolved basis",
            "liability configuration",
            "policy requires",
            "readiness",
            "demo fallback",
            "account-wide fallback",
            "RateSource rows",
            "production truth",
            "unblock demos",
            "outstanding hardening",
            "runtime state",
            "worksite resolution",
            "award creation seeding",
            "production replacement",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


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


def _worker_attention_issue_resolution_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Worker Attention / Issue Resolution evidence"]
    detail_terms = [
        term
        for term in (
            "Worker Attention",
            "WorkerAttention",
            "Worker Attention Centre",
            "Issue Resolution",
            "worker-level issue surface",
            "WorkerIssue",
            "Worker issue",
            "issue scope",
            "issue class",
            "issue type",
            "issue severity",
            "blockers",
            "warnings",
            "readiness gaps",
            "deterministic fix links",
            "resolution surfaces",
            "dirty contact",
            "PayRunContact dirty",
            "reprocessing",
            "payment allocation readiness",
            "tax readiness",
            "deduction readiness",
            "leave readiness",
            "negative net pay",
            "obligations",
            "Worker Story",
            "PayRun Admin Queue",
            "not the same surface",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _gross_to_net_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Gross-to-Net evidence"]
    detail_terms = [
        term
        for term in (
            "Gross-to-Net",
            "Gross to Net",
            "GrossToNet",
            "payroll outcome calculation",
            "payroll outcome explanation surface",
            "gross earnings",
            "payroll output",
            "taxable basis",
            "taxable earnings",
            "PAYG",
            "withholding",
            "tax withholding",
            "deductions",
            "obligations",
            "negative net pay",
            "governed treatment",
            "net pay",
            "payment allocation",
            "payment execution readiness",
            "Worker Story",
            "finalised outcome truth",
            "current-effective payroll output",
            "current truth",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _rate_source_rate_story_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved RateSource / Rate Story evidence"]
    detail_terms = [
        term
        for term in (
            "RateSource",
            "Rate Source",
            "Rate Story",
            "RateStory",
            "selected rate",
            "rate amount",
            "date-effective rate",
            "date-effective rates",
            "award rate",
            "account rate",
            "class rate",
            "pay guide rate evidence",
            "RateSourceEvidenceIndex",
            "Decision Story",
            "Worker Story",
            "payroll output",
            "Gross-to-Net",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _decision_story_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Decision Story evidence"]
    detail_terms = [
        term
        for term in (
            "Decision Story",
            "DecisionStory",
            "treatment selection",
            "entitlement decision",
            "payroll decision",
            "why a treatment",
            "why a line exists",
            "DecisionEvidenceIndex",
            "Decision Evidence Index",
            "award rule",
            "configured rules",
            "runtime facts",
            "allowance",
            "penalty",
            "overtime",
            "shift",
            "break treatment",
            "public holiday decision",
            "minimum engagement",
            "Rate Story",
            "Worker Story",
            "payroll output",
            "Gross-to-Net",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _payroll_output_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Payroll Output evidence"]
    detail_terms = [
        term
        for term in (
            "Payroll Output",
            "PayRun Output",
            "Process Period Output",
            "Run Output",
            "calculated payroll output",
            "payroll result",
            "payroll line",
            "output line",
            "CalcInterpreterLine",
            "current-effective output",
            "current-effective payroll output truth",
            "worker-level output",
            "PayRun totals",
            "CalcInterpreterRun",
            "Decision Story",
            "Rate Story",
            "Gross-to-Net",
            "Payroll Bases & Totals",
            "Finalisation Readiness",
            "Payment Execution",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _contact_payroll_history_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Contact Payroll History evidence"]
    detail_terms = [
        term
        for term in (
            "Contact Payroll History",
            "payroll history",
            "worker payroll history",
            "contact-level payroll history",
            "PayRun participation",
            "current payroll output",
            "historical payroll output",
            "current-effective payroll output",
            "Gross-to-Net history",
            "deductions",
            "obligations",
            "negative net pay",
            "tax history",
            "payment readiness history",
            "leave history",
            "accrual history",
            "Worker Story",
            "Movement Review",
            "Admin Queue",
            "retro/replay/correction context",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
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


def _payment_execution_remittance_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Payment Execution / Remittance evidence"]
    detail_terms = [
        term
        for term in (
            "Payment Execution / Remittance",
            "governed payment execution",
            "remittance evidence",
            "generic file export",
            "finalised gross-to-net",
            "finalised payroll outcome",
            "payment outcome",
            "payroll calculation truth",
            "worker net pay",
            "bank allocation",
            "payment allocation",
            "bank instruction readiness",
            "payment destination",
            "missing payment destination",
            "partial payment destinations",
            "payment execution readiness",
            "negative net pay",
            "obligations",
            "carry-forward",
            "recovery",
            "write-off",
            "out-of-pay treatment",
            "deduction remittance",
            "third-party remittance",
            "third-party payments",
            "remittance files",
            "Generate Bank File",
            "Bank File",
            "payment file",
            "Period Close",
            "payment-file execution",
            "remittance batching",
            "remittance reconciliation",
            "reconciliation",
            "Worker Attention",
            "PayRun Admin Queue",
            "Worker Story",
            "audit evidence",
            "skipped",
            "unpaid",
            "unmet",
            "outstanding hardening",
            "bank file generation",
            "remittance execution",
            "payment close",
            "financial consequences",
            "UI surfaces",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:9])}")
    return f"{', '.join(clauses)}."


def _leave_accrual_processing_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Leave Accrual / Processing evidence"]
    detail_terms = [
        term
        for term in (
            "Leave Accrual",
            "Leave Processing",
            "deterministic platform outcomes",
            "Minerva calculations",
            "generic leave policy advice",
            "leave source truth",
            "applicability",
            "LeaveTypeRule",
            "Leave Source Model",
            "source truth",
            "accrual basis",
            "PER_HOUR",
            "minute",
            "hour",
            "accrual quantity",
            "CalcInterpreterLine",
            "current-effective payroll output",
            "canonical processed payroll result truth",
            "AwardRateType",
            "RateType",
            "accrualability",
            "LeaveLedger",
            "balance movements",
            "story evidence",
            "leave valuation basis",
            "TAKEN leave",
            "mandatory",
            "hard failure",
            "silent fallback",
            "leave request",
            "payment effects",
            "before payroll interpretation",
            "within payroll interpretation",
            "after payroll interpretation",
            "LeaveProcessRun",
            "PayRun",
            "finalisation readiness",
            "missing leave output",
            "Worker Story",
            "Leave and Accrual Outcome",
            "server-owned leave output",
            "Payroll Bases & Totals",
            "worked hours",
            "basis quantity",
            "outstanding hardening",
            "leave-processing UI",
            "contact-vs-appointment",
            "leave story polish",
            "finalisation warning acknowledgement",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:9])}")
    return f"{', '.join(clauses)}."


def _finalisation_readiness_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Finalisation Readiness evidence"]
    detail_terms = [
        term
        for term in (
            "Finalisation Readiness",
            "governed readiness gate",
            "assurance gate",
            "not payroll calculation truth",
            "green means done",
            "blockers",
            "warnings",
            "red blockers",
            "amber warnings",
            "green",
            "ready",
            "cleared",
            "current-effective payroll output",
            "stale",
            "superseded",
            "current truth",
            "Worker Attention",
            "Admin Queue",
            "worker-level blockers",
            "ready actions",
            "Payroll Bases readiness",
            "Payroll Bases & Totals",
            "stale basis evidence",
            "leave readiness",
            "missing leave output",
            "leave valuation basis",
            "tax readiness",
            "deduction readiness",
            "negative net pay",
            "payment destination readiness",
            "payment execution readiness",
            "payment readiness",
            "bank readiness",
            "gross-to-net readiness",
            "finalised outcome truth",
            "finalised outcome",
            "finalised totals",
            "durable payment outcome memory",
            "warning acknowledgement",
            "warning acknowledgment",
            "finalisation audit",
            "reviewed",
            "accepted",
            "unresolved",
            "Worker Story",
            "review surfaces",
            "readiness evidence",
            "worker-specific issues",
            "Movement Review",
            "outstanding hardening",
            "WorkerAttention schemas",
            "finalisation policy",
            "server-owned operation",
            "contract tests",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:9])}")
    return f"{', '.join(clauses)}."


def _leave_requests_workflow_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Leave Requests / Leave Workflow evidence"]
    detail_terms = [
        term
        for term in (
            "Leave Requests / Leave Workflow",
            "Leave Request",
            "LeaveRequest",
            "leave workflow",
            "governed leave request workflow",
            "create leave request",
            "draft leave",
            "leave request preview",
            "leave status",
            "status transitions",
            "IdempotencyKey",
            "leave submission",
            "submit leave",
            "approve leave",
            "reject leave",
            "reopen leave",
            "leave overlap",
            "shortfall substitution",
            "TAKEN leave",
            "leave valuation",
            "hard fail",
            "LeaveLedger",
            "leave posting",
            "leave balance",
            "Leave Source Model",
            "leave applicability",
            "LeaveTypeRule",
            "Worker Story",
            "PayRun",
            "finalisation readiness",
            "leave readiness",
            "outstanding hardening",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _public_holidays_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Public Holidays evidence"]
    detail_terms = [
        term
        for term in (
            "PublicHoliday",
            "Public Holiday",
            "PublicHolidayGroup",
            "Public Holiday Group",
            "public holiday calendar",
            "observed day",
            "public holiday override",
            "governed reference configuration",
            "Worksite",
            "WorksitePosition",
            "EmployeeAppointment",
            "state",
            "jurisdiction",
            "location context",
            "public holiday payroll treatment",
            "public holiday decision",
            "Decision Story",
            "Payroll Output",
            "deterministic payroll services",
            "DeductsOnPublicHoliday",
            "public holiday leave treatment",
            "leave request",
            "LeaveLedger",
            "Worker Story",
            "PayRun Admin Queue",
            "Worker Attention",
            "Finalisation Readiness",
            "operator evidence",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _rosters_patterns_scheduling_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Rosters / Patterns / Scheduling evidence"]
    detail_terms = [
        term
        for term in (
            "Roster",
            "Pattern",
            "PatternDay",
            "EmployeeAppointmentPattern",
            "expected work context",
            "EmployeeAppointment",
            "WorksitePosition",
            "Worksite",
            "ordinary hours",
            "leave basis minutes",
            "public holiday",
            "ObjectTime",
            "expected schedule",
            "actual worked time",
            "Worker Story",
            "Decision Story",
            "Payroll Output",
            "Worker Attention",
            "Admin Queue",
            "Finalisation Readiness",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _award_positions_classifications_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Award Positions / Classifications evidence"]
    detail_terms = [
        term
        for term in (
            "AwardPosition",
            "AwardPositionClass",
            "PositionClass",
            "classification levels",
            "pay guide",
            "EmployeeAppointment",
            "WorksitePosition",
            "Position",
            "Worksite",
            "classification context",
            "RateSource",
            "Rate Story",
            "Decision Story",
            "Payroll Output",
            "comparator classification",
            "classification lenses",
            "primary appointment class",
            "Worker Story",
            "Worker Attention",
            "Finalisation Readiness",
            "NEEDS_CONFIGURATION",
        )
        if _has_any(terms, term)
    ]
    if detail_terms:
        clauses.append(f"covering {', '.join(detail_terms[:10])}")
    return f"{', '.join(clauses)}."


def _leave_source_model_domain_sentence(terms: list[str], label: str) -> str:
    clauses = [f"{label} is described in the retrieved Leave Source Model evidence"]
    detail_terms = [
        term
        for term in (
            "Leave Source Model",
            "governed applicability",
            "source-truth layer",
            "leave applies",
            "worker context",
            "applicability",
            "rule content",
            "LeaveTypeRule",
            "policy calculation content",
            "source truth",
            "final applicability truth",
            "active LeaveTypeRule",
            "every worker",
            "leave output",
            "Contact scope",
            "EmployeeAppointment scope",
            "appointment-aware leave",
            "contact-level",
            "appointment-level",
            "Account",
            "EmploymentType",
            "WorksitePosition",
            "Worksite",
            "EmployeeAppointment",
            "Contact",
            "AwardPositionClass",
            "AwardPosition",
            "Position",
            "Award",
            "State",
            "precedence",
            "leave accrual",
            "source applicability decisions",
            "consume source",
            "infer ad hoc",
            "leave request",
            "payment effects",
            "leave ownership",
            "request ownership",
            "Worker Story",
            "leave chapters",
            "warnings",
            "Command Centre",
            "Finalisation Readiness",
            "PayRun finalisation warnings",
            "leave readiness",
            "honestly",
            "missing leave output",
            "leave does not apply",
            "leave output is missing",
            "outstanding hardening",
            "planned model",
            "required model",
            "not complete",
            "runtime capability",
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
    if _is_rate_source_rate_story_group(group):
        return _rate_source_rate_story_domain_sentence(terms, group.label)
    if _is_decision_story_group(group):
        return _decision_story_domain_sentence(terms, group.label)
    if _is_payroll_output_group(group):
        return _payroll_output_domain_sentence(terms, group.label)
    if _is_gross_to_net_group(group):
        return _gross_to_net_domain_sentence(terms, group.label)
    if _is_worker_attention_issue_resolution_group(group):
        return _worker_attention_issue_resolution_domain_sentence(terms, group.label)
    if _is_costing_gl_consequence_group(group):
        return _costing_gl_consequence_domain_sentence(terms, group.label)
    if _is_process_period_payrun_lifecycle_group(group):
        return _process_period_payrun_lifecycle_domain_sentence(terms, group.label)
    if _is_contact_payroll_history_group(group):
        return _contact_payroll_history_domain_sentence(terms, group.label)
    if _is_contacts_employee_appointments_group(group):
        return _contacts_employee_appointments_domain_sentence(terms, group.label)
    if _is_objecttime_source_truth_group(group):
        return _objecttime_source_truth_domain_sentence(terms, group.label)
    if _is_imports_actuals_group(group):
        return _imports_actuals_domain_sentence(terms, group.label)
    if _is_award_build_evidence_group(group):
        return _award_build_evidence_domain_sentence(terms, group.label)
    if _is_oncosts_employer_liabilities_group(group):
        return _oncosts_employer_liabilities_domain_sentence(terms, group.label)
    if _is_leave_source_model_group(group):
        return _leave_source_model_domain_sentence(terms, group.label)
    if _is_finalisation_readiness_group(group):
        return _finalisation_readiness_domain_sentence(terms, group.label)
    if _is_leave_accrual_processing_group(group):
        return _leave_accrual_processing_domain_sentence(terms, group.label)
    if _is_leave_requests_workflow_group(group):
        return _leave_requests_workflow_domain_sentence(terms, group.label)
    if _is_public_holidays_group(group):
        return _public_holidays_domain_sentence(terms, group.label)
    if _is_rosters_patterns_scheduling_group(group):
        return _rosters_patterns_scheduling_domain_sentence(terms, group.label)
    if _is_award_positions_classifications_group(group):
        return _award_positions_classifications_domain_sentence(terms, group.label)
    if _is_payment_execution_remittance_group(group):
        return _payment_execution_remittance_domain_sentence(terms, group.label)
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
        RATE_SOURCE_RATE_STORY_GROUP_KEY_TERMS.get(group.group_id)
        if _is_rate_source_rate_story_group(group)
        else
        DECISION_STORY_GROUP_KEY_TERMS.get(group.group_id)
        if _is_decision_story_group(group)
        else
        PAYROLL_OUTPUT_GROUP_KEY_TERMS.get(group.group_id)
        if _is_payroll_output_group(group)
        else
        CONTACT_PAYROLL_HISTORY_GROUP_KEY_TERMS.get(group.group_id)
        if _is_contact_payroll_history_group(group)
        else
        GROSS_TO_NET_GROUP_KEY_TERMS.get(group.group_id)
        if _is_gross_to_net_group(group)
        else
        WORKER_ATTENTION_ISSUE_RESOLUTION_GROUP_KEY_TERMS.get(group.group_id)
        if _is_worker_attention_issue_resolution_group(group)
        else
        COSTING_GL_CONSEQUENCE_GROUP_KEY_TERMS.get(group.group_id)
        if _is_costing_gl_consequence_group(group)
        else
        PROCESS_PERIOD_PAYRUN_LIFECYCLE_GROUP_KEY_TERMS.get(group.group_id)
        if _is_process_period_payrun_lifecycle_group(group)
        else
        CONTACTS_EMPLOYEE_APPOINTMENTS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_contacts_employee_appointments_group(group)
        else
        OBJECTTIME_SOURCE_TRUTH_GROUP_KEY_TERMS.get(group.group_id)
        if _is_objecttime_source_truth_group(group)
        else
        IMPORTS_ACTUALS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_imports_actuals_group(group)
        else
        AWARD_BUILD_EVIDENCE_GROUP_KEY_TERMS.get(group.group_id)
        if _is_award_build_evidence_group(group)
        else
        ONCOSTS_EMPLOYER_LIABILITIES_GROUP_KEY_TERMS.get(group.group_id)
        if _is_oncosts_employer_liabilities_group(group)
        else
        LEAVE_SOURCE_MODEL_GROUP_KEY_TERMS.get(group.group_id)
        if _is_leave_source_model_group(group)
        else
        FINALISATION_READINESS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_finalisation_readiness_group(group)
        else
        LEAVE_ACCRUAL_PROCESSING_GROUP_KEY_TERMS.get(group.group_id)
        if _is_leave_accrual_processing_group(group)
        else
        LEAVE_REQUESTS_WORKFLOW_GROUP_KEY_TERMS.get(group.group_id)
        if _is_leave_requests_workflow_group(group)
        else
        PUBLIC_HOLIDAYS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_public_holidays_group(group)
        else
        ROSTERS_PATTERNS_SCHEDULING_GROUP_KEY_TERMS.get(group.group_id)
        if _is_rosters_patterns_scheduling_group(group)
        else
        AWARD_POSITIONS_CLASSIFICATIONS_GROUP_KEY_TERMS.get(group.group_id)
        if _is_award_positions_classifications_group(group)
        else
        PAYMENT_EXECUTION_REMITTANCE_GROUP_KEY_TERMS.get(group.group_id)
        if _is_payment_execution_remittance_group(group)
        else
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
        RATE_SOURCE_RATE_STORY_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_rate_source_rate_story_group(group)
        else
        DECISION_STORY_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_decision_story_group(group)
        else
        PAYROLL_OUTPUT_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_payroll_output_group(group)
        else
        CONTACT_PAYROLL_HISTORY_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_contact_payroll_history_group(group)
        else
        GROSS_TO_NET_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_gross_to_net_group(group)
        else
        WORKER_ATTENTION_ISSUE_RESOLUTION_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_worker_attention_issue_resolution_group(group)
        else
        COSTING_GL_CONSEQUENCE_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_costing_gl_consequence_group(group)
        else
        PROCESS_PERIOD_PAYRUN_LIFECYCLE_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_process_period_payrun_lifecycle_group(group)
        else
        CONTACTS_EMPLOYEE_APPOINTMENTS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_contacts_employee_appointments_group(group)
        else
        OBJECTTIME_SOURCE_TRUTH_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_objecttime_source_truth_group(group)
        else
        IMPORTS_ACTUALS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_imports_actuals_group(group)
        else
        AWARD_BUILD_EVIDENCE_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_award_build_evidence_group(group)
        else
        ONCOSTS_EMPLOYER_LIABILITIES_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_oncosts_employer_liabilities_group(group)
        else
        LEAVE_SOURCE_MODEL_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_leave_source_model_group(group)
        else
        FINALISATION_READINESS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_finalisation_readiness_group(group)
        else
        LEAVE_ACCRUAL_PROCESSING_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_leave_accrual_processing_group(group)
        else
        LEAVE_REQUESTS_WORKFLOW_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_leave_requests_workflow_group(group)
        else
        PUBLIC_HOLIDAYS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_public_holidays_group(group)
        else
        ROSTERS_PATTERNS_SCHEDULING_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_rosters_patterns_scheduling_group(group)
        else
        AWARD_POSITIONS_CLASSIFICATIONS_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_award_positions_classifications_group(group)
        else
        PAYMENT_EXECUTION_REMITTANCE_GROUP_SIGNAL_TERMS.get(group.group_id)
        if _is_payment_execution_remittance_group(group)
        else
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

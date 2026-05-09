from dataclasses import dataclass, replace

from sqlalchemy.orm import Session

from app.core.enums import normalize_source_type
from app.services.answer_mode_service import AnswerMode, classify_answer_mode
from app.services.knowledge_retrieval_service import RetrievalResult, retrieve_relevant_chunks


@dataclass(frozen=True)
class EvidenceGroup:
    group_id: str
    label: str
    query_terms: tuple[str, ...]
    required_terms_any: tuple[str, ...]
    preferred_source_types: tuple[str, ...]
    max_chunks: int = 1


@dataclass(frozen=True)
class DomainRetrievalPlan:
    plan_id: str
    domain: str
    trigger_phrases: tuple[str, ...]
    evidence_groups: tuple[EvidenceGroup, ...]


ANNUAL_LEAVE_MANAGEMENT_PLAN = DomainRetrievalPlan(
    plan_id="ANNUAL_LEAVE_MANAGEMENT",
    domain="Annual Leave / Leave Management",
    trigger_phrases=(
        "how is annual leave managed in the system",
        "how does annual leave work",
        "how is annual leave handled",
        "how is annual leave accrual and taken leave managed",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="configuration",
            label="Configuration and rule setup",
            query_terms=(
                "Annual Leave",
                "LeaveType",
                "LeaveTypeRule",
                "LeaveTypeKind",
                "Rule Cockpit",
                "Accrual",
                "Payment",
                "Governance",
            ),
            required_terms_any=("Annual Leave", "LeaveType", "LeaveTypeRule", "LeaveTypeKind", "Rule Cockpit"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="accrual",
            label="Accrual basis and ledger posting",
            query_terms=(
                "Annual Leave",
                "accrual",
                "LeaveLedger",
                "minutes",
                "interpreter truth",
                "no fallback",
                "process period",
                "PayRun",
            ),
            required_terms_any=("Annual Leave", "accrual", "LeaveLedger", "interpreter truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="taken",
            label="TAKEN leave and deduction rules",
            query_terms=(
                "Annual Leave",
                "TAKEN",
                "LeaveLedger",
                "minutes",
                "public holiday",
                "DeductsOnPublicHoliday",
                "skip",
                "resolver",
            ),
            required_terms_any=("Annual Leave", "TAKEN", "LeaveLedger", "DeductsOnPublicHoliday", "public holiday"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="valuation",
            label="Valuation and ordinary rate evidence",
            query_terms=(
                "Annual Leave",
                "valuation",
                "valuation basis",
                "ordinary rate",
                "PayRun",
                "snapshot",
                "liability",
            ),
            required_terms_any=("Annual Leave", "valuation", "valuation basis", "ordinary rate", "liability"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun",
            label="PayRun leave orchestration",
            query_terms=(
                "PayRun",
                "Generate Leave Accruals on Process",
                "leave accruals",
                "valuation basis",
                "processing",
                "Admin Queue",
            ),
            required_terms_any=("PayRun", "Generate Leave Accruals on Process", "leave accruals", "Admin Queue"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story",
            label="Worker Story leave evidence",
            query_terms=(
                "Worker Story",
                "Leave and Accrual Outcome",
                "server-owned leave output",
                "ledger",
                "valuation basis",
                "evidence chain",
            ),
            required_terms_any=("Worker Story", "Leave and Accrual Outcome", "server-owned leave output", "evidence chain"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding",
            label="Outstanding hardening and future work",
            query_terms=(
                "Annual Leave",
                "outstanding",
                "hardening",
                "Leave Source Model",
                "FIFO",
                "lot consumption",
                "revaluation",
                "production hardening",
            ),
            required_terms_any=("Annual Leave", "outstanding", "hardening", "Leave Source Model", "FIFO", "revaluation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

WORKER_STORY_PLAN = DomainRetrievalPlan(
    plan_id="WORKER_STORY",
    domain="Worker Story / Worker Calculation Story",
    trigger_phrases=(
        "what is worker story",
        "what evidence does worker story show",
        "how does worker story explain payroll outcomes",
        "how does worker story explain calculated payroll outcome",
        "how does worker story use source truth",
        "how does worker story explain rate and decision evidence",
        "how does worker story relate to payrun",
        "what is worker calculation story",
        "what is talking payslip",
        "how does source truth work",
        "how does calculated payroll outcome work",
        "what is the difference between decision story and rate story",
        "how does movement review relate to payrun admin queue",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="worker_story_purpose",
            label="Worker Story purpose",
            query_terms=("Worker Story", "Worker Calculation Story", "Talking Payslip", "worker evidence", "explain"),
            required_terms_any=("Worker Story", "Worker Calculation Story", "Talking Payslip"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="source_truth_and_inclusion",
            label="Source truth and inclusion evidence",
            query_terms=("Worker Story", "SourceTruth", "Source truth", "inclusion", "source truth"),
            required_terms_any=("SourceTruth", "Source truth", "inclusion"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="interpreted_worked_hours",
            label="Interpreted Worked Hours",
            query_terms=("Worker Story", "Interpreted Worked Hours", "current-effective interpreter run", "ObjectTime grouping"),
            required_terms_any=("Interpreted Worked Hours", "current-effective interpreter run", "ObjectTime grouping"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="calculated_payroll_outcome",
            label="Calculated Payroll Outcome",
            query_terms=(
                "Worker Story",
                "Calculated Payroll Outcome",
                "current-effective payroll output",
                "PayRun",
                "quantity",
                "rate",
                "amount",
                "line proof",
            ),
            required_terms_any=(
                "Calculated Payroll Outcome",
                "current-effective payroll output",
                "PayRun",
                "line proof",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="decision_story_and_rate_story",
            label="Decision Story and Rate Story",
            query_terms=(
                "Decision Story",
                "Rate Story",
                "DecisionEvidenceIndex",
                "RateSourceEvidenceIndex",
                "rate evidence",
            ),
            required_terms_any=("Decision Story", "Rate Story", "DecisionEvidenceIndex", "RateSourceEvidenceIndex"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_and_accrual_outcome",
            label="Leave and Accrual Outcome",
            query_terms=("Worker Story", "Leave and Accrual Outcome", "leave", "accrual", "evidence"),
            required_terms_any=("Leave and Accrual Outcome", "leave", "accrual"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_and_totals",
            label="Payroll Bases & Totals",
            query_terms=("Worker Story", "Payroll Bases & Totals", "payroll bases", "totals", "evidence"),
            required_terms_any=("Payroll Bases & Totals", "payroll bases", "totals"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="movement_review_and_admin_queue",
            label="Movement Review and Admin Queue",
            query_terms=("Movement Review", "PayRun Admin Queue", "Admin Queue", "PayRun", "worker evidence"),
            required_terms_any=("Movement Review", "PayRun Admin Queue", "Admin Queue"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_truth",
            label="Current-effective truth",
            query_terms=(
                "current-effective truth",
                "current-effective payroll output",
                "current-effective interpreter run",
                "Correction Audit Story",
            ),
            required_terms_any=(
                "current-effective truth",
                "current-effective payroll output",
                "current-effective interpreter run",
                "Correction Audit Story",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Outstanding hardening",
            query_terms=("Worker Story", "outstanding hardening", "limitations", "future work", "hardening"),
            required_terms_any=("outstanding hardening", "limitations", "hardening"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PAYROLL_BASES_AND_TOTALS_PLAN = DomainRetrievalPlan(
    plan_id="PAYROLL_BASES_AND_TOTALS",
    domain="Payroll Bases & Totals",
    trigger_phrases=(
        "what are payroll bases and totals",
        "what are payroll bases & totals",
        "why do payroll bases and totals matter",
        "why do payroll bases & totals matter",
        "how do payroll bases and totals work",
        "how do payroll bases & totals work",
        "what is payroll bucket result",
        "what is payrollbucketresult",
        "what is payroll bucket definition",
        "what is payrollbucketdefinition",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Purpose and operator meaning",
            query_terms=("Payroll Bases & Totals", "Payroll Bases and Totals", "governed payroll basis evidence", "operator"),
            required_terms_any=("Payroll Bases & Totals", "Payroll Bases and Totals", "governed payroll basis evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="bucket_definition_and_membership",
            label="Bucket definition and membership",
            query_terms=(
                "PayrollBucketDefinition",
                "Payroll Bucket Definition",
                "bucket definition",
                "period definition",
                "calendar policy",
                "membership",
            ),
            required_terms_any=(
                "PayrollBucketDefinition",
                "Payroll Bucket Definition",
                "bucket definition",
                "period definition",
                "calendar policy",
                "membership",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worked_hours_and_quantity",
            label="Worked hours and quantity",
            query_terms=("Payroll Bases & Totals", "worked hours", "quantity", "minutes", "hours", "basis quantity"),
            required_terms_any=("worked hours", "quantity", "minutes", "hours", "basis quantity"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_ordinary_superable_taxable_bases",
            label="Gross, ordinary, superable and taxable bases",
            query_terms=(
                "gross basis",
                "ordinary basis",
                "superable basis",
                "taxable basis",
                "payroll tax",
                "WIC",
                "PAYG",
            ),
            required_terms_any=("gross basis", "ordinary basis", "superable basis", "taxable basis", "payroll tax", "WIC", "PAYG"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_truth",
            label="Current-effective truth",
            query_terms=("current-effective truth", "current effective", "current-effective payroll output", "stale", "source truth"),
            required_terms_any=("current-effective truth", "current effective", "current-effective payroll output", "stale", "source truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="readiness_and_rebuild",
            label="Readiness and rebuild",
            query_terms=("PayrollBucketResult", "Payroll Bucket Result", "readiness", "stale rows", "rebuild", "recalculate"),
            required_terms_any=("PayrollBucketResult", "Payroll Bucket Result", "readiness", "stale rows", "rebuild"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Worker Story connection",
            query_terms=("Payroll Bases & Totals", "Worker Story", "Worker Calculation Story", "evidence surface", "worker evidence"),
            required_terms_any=("Payroll Bases & Totals", "Worker Story", "Worker Calculation Story", "worker evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="movement_review_connection",
            label="Movement Review connection",
            query_terms=("Payroll Bases & Totals", "Movement Review", "PayRun Admin Queue", "operator review", "basis movement"),
            required_terms_any=("Payroll Bases & Totals", "Movement Review", "PayRun Admin Queue", "operator review"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Outstanding hardening",
            query_terms=("Payroll Bases & Totals", "outstanding hardening", "limitations", "bucket lifecycle", "versioning", "future work"),
            required_terms_any=("outstanding hardening", "limitations", "bucket lifecycle", "versioning", "future work"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PAYRUN_ADMIN_QUEUE_PLAN = DomainRetrievalPlan(
    plan_id="PAYRUN_ADMIN_QUEUE",
    domain="PayRun Admin Queue",
    trigger_phrases=(
        "what is the payrun admin queue",
        "what does the payrun admin queue show",
        "what is payrun admin queue",
        "what does payrun admin queue show",
        "what is the admin queue",
        "what is the payrun queue",
        "what does the payrun queue show",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Admin Queue purpose and operator meaning",
            query_terms=("PayRun Admin Queue", "Admin Queue", "operator workbench", "what needs action now", "Command Centre"),
            required_terms_any=("PayRun Admin Queue", "Admin Queue", "operator workbench", "what needs action now"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="blockers_warnings_and_ready_actions",
            label="Blockers, warnings and ready actions",
            query_terms=("PayRun Admin Queue", "blockers", "warnings", "ready actions", "amber warnings"),
            required_terms_any=("blockers", "warnings", "ready actions", "amber warnings"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_attention_and_dirty_contacts",
            label="Worker attention and dirty contacts",
            query_terms=("PayRun Admin Queue", "Worker Attention", "worker attention", "dirty contacts", "contact changes"),
            required_terms_any=("Worker Attention", "worker attention", "dirty contacts", "contact changes"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="processing_and_reprocessing_actions",
            label="Processing and reprocessing actions",
            query_terms=("PayRun Admin Queue", "processing actions", "reprocessing actions", "reprocess", "deterministic services"),
            required_terms_any=("processing actions", "reprocessing actions", "reprocess", "deterministic services"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalisation_readiness",
            label="Finalisation readiness",
            query_terms=("PayRun Admin Queue", "finalisation readiness", "finalisation", "blockers", "warnings"),
            required_terms_any=("finalisation readiness", "finalisation", "blockers", "warnings"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="assurance_snapshot",
            label="Assurance Snapshot",
            query_terms=("Assurance Snapshot", "reasonableness", "review signals", "assurance signals", "thresholds"),
            required_terms_any=("Assurance Snapshot", "reasonableness", "review signals", "assurance signals", "thresholds"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="review_surfaces_and_navigation",
            label="Review surfaces and navigation",
            query_terms=("PayRun Admin Queue", "review surfaces", "navigation", "PayRun Output", "Command Centre"),
            required_terms_any=("review surfaces", "navigation", "PayRun Output", "Command Centre"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Admin Queue Worker Story connection",
            query_terms=("PayRun Admin Queue", "Worker Story", "Worker Calculation Story", "worker evidence"),
            required_terms_any=("PayRun Admin Queue", "Worker Story", "Worker Calculation Story", "worker evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_connection",
            label="Payroll Bases & Totals connection",
            query_terms=("PayRun Admin Queue", "Payroll Bases & Totals", "payroll bases", "basis evidence"),
            required_terms_any=("PayRun Admin Queue", "Payroll Bases & Totals", "payroll bases", "basis evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="movement_review_connection",
            label="Admin Queue Movement Review connection",
            query_terms=("PayRun Admin Queue", "Movement Review", "operator review", "movement evidence"),
            required_terms_any=("PayRun Admin Queue", "Movement Review", "operator review", "movement evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Admin Queue outstanding hardening",
            query_terms=(
                "PayRun Admin Queue",
                "outstanding hardening",
                "server-owned operation tracker",
                "global queue resolver",
                "governed assurance thresholds",
                "warning acknowledgement",
            ),
            required_terms_any=(
                "outstanding hardening",
                "server-owned operation tracker",
                "global queue resolver",
                "governed assurance thresholds",
                "warning acknowledgement",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

MOVEMENT_REVIEW_PLAN = DomainRetrievalPlan(
    plan_id="MOVEMENT_REVIEW",
    domain="Movement Review",
    trigger_phrases=(
        "what is movement review",
        "what does movement review show",
        "what is payroll movement review",
        "what does payroll movement review show",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Movement Review purpose and operator meaning",
            query_terms=("Movement Review", "Payroll Movement Review", "reasonableness", "review surface", "operator"),
            required_terms_any=("Movement Review", "Payroll Movement Review", "reasonableness", "review surface"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="reasonableness_not_error",
            label="Reasonableness not automatic error",
            query_terms=("Movement Review", "reasonableness", "not automatic proof", "variance", "payroll is wrong"),
            required_terms_any=("reasonableness", "not automatic proof", "variance", "payroll is wrong"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_and_organisation_lenses",
            label="Worker and organisation lenses",
            query_terms=("Movement Review", "worker lens", "organisation lens", "worker-level", "organisation-level"),
            required_terms_any=("worker lens", "organisation lens", "worker-level", "organisation-level"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="variance_and_comparable_periods",
            label="Variance and comparable periods",
            query_terms=("Movement Review", "variance", "comparable period", "baseline evidence", "review-worthy"),
            required_terms_any=("variance", "comparable period", "baseline evidence", "review-worthy"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_connection",
            label="Movement Review Payroll Bases & Totals connection",
            query_terms=("Movement Review", "Payroll Bases & Totals", "payroll bases", "basis evidence", "bucket source truth"),
            required_terms_any=("Movement Review", "Payroll Bases & Totals", "payroll bases", "basis evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Movement Review Worker Story connection",
            query_terms=("Movement Review", "Worker Story", "worker-level drill-through", "worker evidence", "explanation"),
            required_terms_any=("Movement Review", "Worker Story", "worker-level drill-through", "worker evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="admin_queue_connection",
            label="Movement Review Admin Queue connection",
            query_terms=("Movement Review", "PayRun Admin Queue", "Admin Queue", "movement review actions", "assurance review actions"),
            required_terms_any=("Movement Review", "PayRun Admin Queue", "Admin Queue", "review actions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_truth",
            label="Movement Review current-effective truth",
            query_terms=("Movement Review", "current-effective payroll", "current-effective truth", "bucket source truth", "stale bucket"),
            required_terms_any=("current-effective payroll", "current-effective truth", "bucket source truth", "stale bucket"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="trend_only_and_threshold_treatment",
            label="Trend-only and threshold treatment",
            query_terms=("Movement Review", "trend-only", "rolling average", "YTD", "thresholds", "current-period blockers"),
            required_terms_any=("trend-only", "rolling average", "YTD", "thresholds", "current-period blockers"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="filters_and_return_context",
            label="Filters and return context",
            query_terms=("Movement Review", "filters", "filtered lenses", "return context", "all-worker views", "audit"),
            required_terms_any=("filters", "filtered lenses", "return context", "all-worker views", "audit"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Movement Review outstanding hardening",
            query_terms=(
                "Movement Review",
                "outstanding hardening",
                "Movement Review Policy",
                "thresholds",
                "comparable period rules",
                "historical bucket rebuild governance",
            ),
            required_terms_any=(
                "outstanding hardening",
                "Movement Review Policy",
                "thresholds",
                "comparable period rules",
                "historical bucket rebuild governance",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

COMPARISON_REMEDIATION_PLAN = DomainRetrievalPlan(
    plan_id="COMPARISON_REMEDIATION",
    domain="Comparison / Remediation",
    trigger_phrases=(
        "what is comparison remediation",
        "what is comparison / remediation",
        "how should comparison remediation work",
        "how should comparison / remediation work",
        "what is award comparison",
        "what is remediation top-up",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Comparison / Remediation purpose and operator meaning",
            query_terms=("Comparison / Remediation", "Comparison Remediation", "governed comparison", "remediation", "top-up"),
            required_terms_any=("Comparison / Remediation", "Comparison Remediation", "governed comparison", "remediation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="three_lane_comparison_model",
            label="Three-lane comparison model",
            query_terms=("primary calculated", "comparator calculated", "actual imported", "actuals lane", "three lane"),
            required_terms_any=("primary calculated", "comparator calculated", "actual imported", "actuals lane", "three lane"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="primary_award_path_preservation",
            label="Primary award path preservation",
            query_terms=("ObjectTime", "EmployeeAppointment", "AwardPositionClass", "primary award path", "operational payroll truth"),
            required_terms_any=("ObjectTime", "EmployeeAppointment", "AwardPositionClass", "primary award path", "operational payroll truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="actuals_as_external_outcome_truth",
            label="Actuals as external outcome truth",
            query_terms=("imported actuals", "actuals lane", "external outcome truth", "imported actual payroll truth"),
            required_terms_any=("imported actuals", "actuals lane", "external outcome truth", "imported actual payroll truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_policy",
            label="Comparison policy",
            query_terms=(
                "AwardComparisonPolicy",
                "Award Comparison Policy",
                "comparator selection",
                "active lanes",
                "offset policy",
                "variance treatment",
            ),
            required_terms_any=(
                "AwardComparisonPolicy",
                "Award Comparison Policy",
                "comparator selection",
                "active lanes",
                "offset policy",
                "variance treatment",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_run_and_line_evidence",
            label="Comparison run and line evidence",
            query_terms=("PayRunComparisonRun", "PayRun Comparison Run", "PayRunComparisonLine", "PayRun Comparison Line", "comparison evidence"),
            required_terms_any=("PayRunComparisonRun", "PayRun Comparison Run", "PayRunComparisonLine", "PayRun Comparison Line", "comparison evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="variance_generation_and_governance",
            label="Variance generation and governance",
            query_terms=("PayRunVarianceLine", "PayRun Variance Line", "variance line", "remediation top-up", "typed explainable"),
            required_terms_any=("PayRunVarianceLine", "PayRun Variance Line", "variance line", "remediation top-up", "typed explainable"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="position_classification_mapping",
            label="Position and classification mapping",
            query_terms=(
                "AwardPositionClassComparisonMap",
                "EmployeeAppointmentAwardClassAssignment",
                "ObjectTimeClassificationResolution",
                "comparator classification",
                "classification lens",
            ),
            required_terms_any=(
                "AwardPositionClassComparisonMap",
                "EmployeeAppointmentAwardClassAssignment",
                "ObjectTimeClassificationResolution",
                "comparator classification",
                "classification lens",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Comparison Worker Story connection",
            query_terms=("Comparison / Remediation", "Worker Story", "comparison chapter", "worker evidence", "remediation evidence"),
            required_terms_any=("Comparison / Remediation", "Worker Story", "comparison chapter", "worker evidence", "remediation evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="admin_queue_connection",
            label="Comparison Admin Queue connection",
            query_terms=("Comparison / Remediation", "PayRun Admin Queue", "missing policy", "unmapped actuals", "variance review actions"),
            required_terms_any=("Comparison / Remediation", "PayRun Admin Queue", "missing policy", "unmapped actuals", "variance review actions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="movement_review_connection",
            label="Comparison Movement Review connection",
            query_terms=("Comparison / Remediation", "Movement Review", "variance", "comparison outcomes", "not automatic proof of error"),
            required_terms_any=("Comparison / Remediation", "Movement Review", "variance", "comparison outcomes", "not automatic proof of error"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Comparison / Remediation outstanding hardening",
            query_terms=(
                "Comparison / Remediation",
                "outstanding hardening",
                "design doctrine",
                "not yet implemented",
                "full runtime capability",
                "future work",
            ),
            required_terms_any=("outstanding hardening", "design doctrine", "not yet implemented", "full runtime capability", "future work"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

TAX_PAYG_PLAN = DomainRetrievalPlan(
    plan_id="TAX_PAYG",
    domain="Tax / PAYG",
    trigger_phrases=(
        "how should tax payg work",
        "how should tax / payg work",
        "what is tax payg",
        "what is tax / payg",
        "how should payg work",
        "how does payg withholding work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Tax / PAYG purpose and operator meaning",
            query_terms=("Tax / PAYG", "PAYG withholding", "governed withholding calculation evidence", "tax evidence"),
            required_terms_any=("Tax / PAYG", "PAYG withholding", "governed withholding calculation evidence", "tax evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deterministic_tax_boundary",
            label="Deterministic tax boundary",
            query_terms=("Tax / PAYG", "deterministic services", "tax providers", "withholding calculation", "Minerva explains"),
            required_terms_any=("deterministic services", "tax providers", "withholding calculation", "Minerva explains"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="tax_story_and_explainability",
            label="TaxStory and explainability",
            query_terms=(
                "TaxStory",
                "Tax Story",
                "source truth",
                "worker tax profile",
                "rule pack selection",
                "frequency conversion",
                "band formula calculation",
                "audit provenance",
            ),
            required_terms_any=(
                "TaxStory",
                "Tax Story",
                "worker tax profile",
                "rule pack selection",
                "frequency conversion",
                "audit provenance",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="taxable_basis_and_payroll_bases",
            label="Taxable basis and Payroll Bases",
            query_terms=("taxable basis", "taxable earnings", "Payroll Bases & Totals", "governed basis membership", "raw flags"),
            required_terms_any=("taxable basis", "taxable earnings", "Payroll Bases & Totals", "governed basis membership", "raw flags"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_tax_declaration_and_withholding_inputs",
            label="Worker tax declaration and withholding inputs",
            query_terms=("worker tax declaration", "withholding instruction", "withholding inputs", "tax profile", "calculation readiness"),
            required_terms_any=("worker tax declaration", "withholding instruction", "withholding inputs", "tax profile", "calculation readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_date_and_process_period_context",
            label="Payment date and process period context",
            query_terms=("ProcessPeriod PaymentDate", "payment date", "process period", "tax context", "governed derived"),
            required_terms_any=("ProcessPeriod PaymentDate", "payment date", "process period", "tax context", "governed derived"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="pay_frequency_and_provider_support",
            label="Pay frequency and provider support",
            query_terms=("pay frequency", "provider support", "daily", "weekly", "fortnightly", "monthly", "quarterly", "unsupported frequency"),
            required_terms_any=("pay frequency", "provider support", "weekly", "fortnightly", "monthly", "quarterly", "unsupported frequency"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_to_net_and_finalised_totals",
            label="Gross-to-net and finalised totals",
            query_terms=("gross-to-net", "gross to net", "net pay", "finalised totals", "finalised payment memory", "PAYG outcome"),
            required_terms_any=("gross-to-net", "gross to net", "net pay", "finalised totals", "finalised payment memory", "PAYG outcome"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="supplementary_incremental_payg",
            label="Supplementary incremental PAYG",
            query_terms=("supplementary incremental PAYG", "supplementary PAYG", "same-period taxable earnings", "prior PAYG withheld"),
            required_terms_any=("supplementary incremental PAYG", "supplementary PAYG", "same-period taxable earnings", "prior PAYG withheld"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_admin_queue_connection",
            label="Worker Story and Admin Queue connection",
            query_terms=("Tax / PAYG", "Worker Story", "PayRun Admin Queue", "tax readiness", "unsupported states", "reprocessing"),
            required_terms_any=("Tax / PAYG", "Worker Story", "PayRun Admin Queue", "tax readiness", "unsupported states", "reprocessing"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="unsupported_and_review_states",
            label="Unsupported and review states",
            query_terms=("unsupported tax scenarios", "unsupported frequencies", "explicit status", "configuration status", "review states"),
            required_terms_any=("unsupported tax scenarios", "unsupported frequencies", "explicit status", "configuration status", "review states"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Tax / PAYG outstanding hardening",
            query_terms=(
                "Tax / PAYG",
                "outstanding hardening",
                "provider support",
                "non-weekly frequencies",
                "taxable basis governance",
                "withholding instruction UI",
                "supplementary tax",
                "full TaxStory",
            ),
            required_terms_any=(
                "outstanding hardening",
                "provider support",
                "non-weekly frequencies",
                "taxable basis governance",
                "withholding instruction UI",
                "supplementary tax",
                "full TaxStory",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

DEDUCTIONS_OBLIGATIONS_PLAN = DomainRetrievalPlan(
    plan_id="DEDUCTIONS_OBLIGATIONS",
    domain="Deductions / Obligations",
    trigger_phrases=(
        "how should deductions and obligations work",
        "how should deductions / obligations work",
        "what are deductions and obligations",
        "what are deductions / obligations",
        "how do deductions and obligations work",
        "how do deductions / obligations work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Deductions / Obligations purpose and operator meaning",
            query_terms=("Deductions / Obligations", "governed application outcomes", "net-pay subtraction", "operator"),
            required_terms_any=("Deductions / Obligations", "governed application outcomes", "net-pay subtraction"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deduction_template_chain",
            label="Deductions / Obligations deduction template chain",
            query_terms=(
                "LibraryDeductionTemplate",
                "AccountDeductionTemplate",
                "ContactPayrollDeduction",
                "PayRunDeductionApplication",
                "deduction chain",
            ),
            required_terms_any=(
                "LibraryDeductionTemplate",
                "AccountDeductionTemplate",
                "ContactPayrollDeduction",
                "PayRunDeductionApplication",
                "deduction chain",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_deduction_instruction",
            label="Deductions / Obligations worker deduction instruction",
            query_terms=("ContactPayrollDeduction", "worker-specific deduction instruction", "operative configuration"),
            required_terms_any=("ContactPayrollDeduction", "worker-specific deduction instruction", "operative configuration"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_deduction_application_memory",
            label="Deductions / Obligations PayRun deduction application memory",
            query_terms=("PayRunDeductionApplication", "requested", "taken", "skipped", "unmet", "outcome memory"),
            required_terms_any=("PayRunDeductionApplication", "requested", "taken", "skipped", "unmet", "outcome memory"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="supplementary_deduction_memory",
            label="Deductions / Obligations supplementary deduction memory",
            query_terms=("supplementary deduction memory", "supplementary PayRuns", "same-period application memory", "recurring deductions"),
            required_terms_any=("supplementary deduction memory", "supplementary PayRuns", "same-period application memory", "recurring deductions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="applicability_affordability_and_priority",
            label="Deductions / Obligations applicability affordability and priority",
            query_terms=("applicability", "affordability", "priority", "partial", "full-only", "explainable"),
            required_terms_any=("applicability", "affordability", "priority", "partial", "full-only", "explainable"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="skipped_partial_unmet_and_carry_forward",
            label="Deductions / Obligations skipped partial unmet and carry-forward",
            query_terms=("skipped", "partial", "unmet", "carry-forward", "carry forward", "visible", "must not silently disappear"),
            required_terms_any=("skipped", "partial", "unmet", "carry-forward", "carry forward", "must not silently disappear"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="obligations_and_reducing_balance_recovery",
            label="Deductions / Obligations reducing-balance recovery",
            query_terms=(
                "ContactPayrollObligation",
                "ContactPayrollObligationLedger",
                "durable obligations",
                "balance-bearing recovery",
                "reducing-balance recovery",
                "outstanding balance",
                "ledger evidence",
            ),
            required_terms_any=(
                "ContactPayrollObligation",
                "ContactPayrollObligationLedger",
                "durable obligations",
                "reducing-balance recovery",
                "outstanding balance",
                "ledger evidence",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="negative_net_pay_governance",
            label="Deductions / Obligations negative net pay governance",
            query_terms=("negative net pay", "governed outcome", "policy treatment", "silent arithmetic side effect"),
            required_terms_any=("negative net pay", "governed outcome", "policy treatment", "silent arithmetic side effect"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_to_net_and_payment_execution",
            label="Deductions / Obligations gross-to-net and payment execution",
            query_terms=("gross-to-net", "gross to net", "payment execution", "remittance", "deduction readiness"),
            required_terms_any=("gross-to-net", "gross to net", "payment execution", "remittance", "deduction readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_admin_queue_connection",
            label="Deductions / Obligations Worker Story and Admin Queue connection",
            query_terms=("Deductions / Obligations", "Worker Story", "PayRun Admin Queue", "Worker Attention", "readiness", "issues"),
            required_terms_any=("Deductions / Obligations", "Worker Story", "PayRun Admin Queue", "Worker Attention", "readiness", "issues"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Deductions / Obligations outstanding hardening",
            query_terms=(
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
            required_terms_any=(
                "outstanding hardening",
                "full UI",
                "remittance",
                "payment execution",
                "obligation write-off",
                "costing consequences",
                "negative-net-pay policy",
                "deduction tax integration",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

RETRO_REPLAY_PLAN = DomainRetrievalPlan(
    plan_id="RETRO_REPLAY",
    domain="Retro / Replay",
    trigger_phrases=(
        "how should retro replay work",
        "how should retro / replay work",
        "what is retro replay",
        "what is retro / replay",
        "how does retro replay work",
        "how does retro / replay work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Retro / Replay purpose and operator meaning",
            query_terms=("Retro / Replay", "governed historical correction", "evidence replay", "ordinary reprocessing"),
            required_terms_any=("Retro / Replay", "governed historical correction", "evidence replay", "ordinary reprocessing"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="attributed_period_and_paid_period_truth",
            label="Retro / Replay attributed-period and paid-period truth",
            query_terms=("attributed period", "paid period", "attributed-period truth", "paid-period truth", "distinct"),
            required_terms_any=("attributed period", "paid period", "attributed-period truth", "paid-period truth", "distinct"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalised_outcome_memory",
            label="Retro / Replay finalised outcome memory",
            query_terms=("finalised outcome memory", "historical payment truth", "finalised outcomes", "silently overwritten"),
            required_terms_any=("finalised outcome memory", "historical payment truth", "finalised outcomes", "silently overwritten"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_and_historical_truth",
            label="Retro / Replay current-effective and historical truth",
            query_terms=("current-effective truth", "historical truth", "finalised truth", "current-effective payroll truth"),
            required_terms_any=("current-effective truth", "historical truth", "finalised truth", "current-effective payroll truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="bucket_and_basis_snapshot_dependency",
            label="Retro / Replay bucket and basis snapshot dependency",
            query_terms=("bucket snapshot", "basis snapshot", "calculation evidence", "source hashes", "historical bucket evidence"),
            required_terms_any=("bucket snapshot", "basis snapshot", "calculation evidence", "source hashes", "historical bucket evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="source_change_and_dependency_detection",
            label="Retro / Replay source change and dependency detection",
            query_terms=("source change", "configuration change", "dependency detection", "dirty replay candidates", "hidden recalculation"),
            required_terms_any=("source change", "configuration change", "dependency detection", "dirty replay candidates", "hidden recalculation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="retro_payrun_and_supplementary_distinction",
            label="Retro / Replay retro PayRun and supplementary distinction",
            query_terms=("retro PayRun", "supplementary PayRun", "retro PayRuns", "supplementary PayRuns", "same concept"),
            required_terms_any=("retro PayRun", "supplementary PayRun", "retro PayRuns", "supplementary PayRuns", "same concept"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_and_variance_connection",
            label="Retro / Replay comparison and variance connection",
            query_terms=("Comparison / Remediation", "comparison", "variance", "retro/replay evidence", "not the same concept"),
            required_terms_any=("Comparison / Remediation", "comparison", "variance", "retro/replay evidence", "not the same concept"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Retro / Replay Worker Story connection",
            query_terms=("Retro / Replay", "Worker Story", "worker level", "retro impacts", "replay impacts"),
            required_terms_any=("Retro / Replay", "Worker Story", "worker level", "retro impacts", "replay impacts"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="admin_queue_and_movement_review_connection",
            label="Retro / Replay Admin Queue and Movement Review connection",
            query_terms=("PayRun Admin Queue", "Admin Queue", "Movement Review", "retro candidates", "dependency issues", "variance"),
            required_terms_any=("PayRun Admin Queue", "Admin Queue", "Movement Review", "retro candidates", "dependency issues", "variance"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="audit_replay_and_non_destructive_history",
            label="Retro / Replay audit replay and non-destructive history",
            query_terms=("audit replay", "non-destructive history", "auditable", "historical evidence", "correction/replay"),
            required_terms_any=("audit replay", "non-destructive history", "auditable", "historical evidence", "correction/replay"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Retro / Replay outstanding hardening",
            query_terms=("Retro / Replay", "outstanding hardening", "future work", "full retro/replay implementation", "dependency detection"),
            required_terms_any=("outstanding hardening", "future work", "full retro/replay implementation", "dependency detection"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

DOMAIN_RETRIEVAL_PLANS = (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    WORKER_STORY_PLAN,
    PAYROLL_BASES_AND_TOTALS_PLAN,
    PAYRUN_ADMIN_QUEUE_PLAN,
    MOVEMENT_REVIEW_PLAN,
    COMPARISON_REMEDIATION_PLAN,
    TAX_PAYG_PLAN,
    DEDUCTIONS_OBLIGATIONS_PLAN,
    RETRO_REPLAY_PLAN,
)


def _normalize_question(text: str) -> str:
    return " ".join(text.lower().replace("-", " ").split()).rstrip("?")


def detect_domain_retrieval_plan(question: str) -> DomainRetrievalPlan | None:
    normalized = _normalize_question(question)
    if (
        "retro replay" in normalized
        or "retro payrun" in normalized
        or "retro pay run" in normalized
        or "attributed period" in normalized
        or "paid period" in normalized
        or "finalised outcome memory" in normalized
        or "finalized outcome memory" in normalized
        or ("current effective truth" in normalized and ("historical" in normalized or "finalised" in normalized or "finalized" in normalized))
        or "historical bucket evidence" in normalized
        or "dependency detection" in normalized
        or ("bucket rebuild" in normalized and ("finalised" in normalized or "finalized" in normalized or "history" in normalized))
        or "correction replay" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return RETRO_REPLAY_PLAN
    if (
        "deductions obligations" in normalized
        or "deductions and obligations" in normalized
        or "deduction and obligation" in normalized
        or ("deduction" in normalized and "obligation" in normalized)
        or "deduction obligation" in normalized
        or "deduction template chain" in normalized
        or "librarydeductiontemplate" in normalized
        or "library deduction template" in normalized
        or "accountdeductiontemplate" in normalized
        or "account deduction template" in normalized
        or "contactpayrolldeduction" in normalized
        or "contact payroll deduction" in normalized
        or "payrundeductionapplication" in normalized
        or "payrun deduction application" in normalized
        or "contactpayrollobligation" in normalized
        or "contact payroll obligation" in normalized
        or "contactpayrollobligationledger" in normalized
        or "contact payroll obligation ledger" in normalized
        or "supplementary deduction memory" in normalized
        or ("supplementary payruns" in normalized and "deduction memory" in normalized)
        or "applicability before affordability" in normalized
        or "reducing balance recovery" in normalized
        or ("carry forward" in normalized and "deduction" in normalized)
        or "negative net pay" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return DEDUCTIONS_OBLIGATIONS_PLAN
    if (
        "tax / payg" in normalized
        or "tax payg" in normalized
        or "payg withholding" in normalized
        or "taxstory" in normalized
        or "tax story" in normalized
        or "worker tax declaration" in normalized
        or "withholding instruction" in normalized
        or "processperiod paymentdate" in normalized
        or ("payment date" in normalized and ("tax" in normalized or "payg" in normalized))
        or ("taxable basis" in normalized and ("payroll bases" in normalized or "payg" in normalized or "tax" in normalized))
        or ("pay frequency" in normalized and ("tax" in normalized or "payg" in normalized))
        or "gross to net" in normalized
        or "gross-to-net" in normalized
        or "supplementary incremental payg" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return TAX_PAYG_PLAN
    if (
        "comparison lane" in normalized
        or "three comparison lanes" in normalized
        or "primary award path" in normalized
        or "imported actuals" in normalized
        or "actuals" in normalized and "external outcome truth" in normalized
        or "awardcomparisonpolicy" in normalized
        or "award comparison policy" in normalized
        or "comparison evidence" in normalized
        or "variance generation" in normalized
        or "top up variance" in normalized
        or "top-up variance" in normalized
        or ("ordinary manual adjustment" in normalized and ("remediation" in normalized or "top up" in normalized or "top-up" in normalized))
        or "comparator classification" in normalized
    ) and (
        "what" in normalized
        or "why" in normalized
        or "how" in normalized
        or "should" in normalized
        or "govern" in normalized
    ):
        return COMPARISON_REMEDIATION_PLAN
    if normalized.startswith("how does movement review") or normalized.startswith("why does movement review"):
        return MOVEMENT_REVIEW_PLAN
    if (
        ("rolling" in normalized or "ytd" in normalized or "trend only" in normalized or "trend-only" in normalized)
        and "current period blockers" in normalized
    ):
        return MOVEMENT_REVIEW_PLAN
    for plan in DOMAIN_RETRIEVAL_PLANS:
        if any(trigger in normalized for trigger in plan.trigger_phrases):
            return plan
    if "annual leave" in normalized and (
        "managed" in normalized
        or "management" in normalized
        or "handled" in normalized
        or "work" in normalized
        or ("accrual" in normalized and "taken" in normalized)
    ):
        return ANNUAL_LEAVE_MANAGEMENT_PLAN
    if normalized.startswith("how does payrun admin queue") or normalized.startswith("how does the payrun admin queue"):
        return PAYRUN_ADMIN_QUEUE_PLAN
    if (
        "comparison remediation" in normalized
        or "comparison / remediation" in normalized
        or "award comparison" in normalized
        or "payruncomparisonrun" in normalized
        or "payrun comparison run" in normalized
        or "payruncomparisonline" in normalized
        or "payrun comparison line" in normalized
        or "payrunvarianceline" in normalized
        or "payrun variance line" in normalized
        or "awardcomparisonpolicy" in normalized
        or "award comparison policy" in normalized
        or "remediation top up" in normalized
        or "remediation top-up" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return COMPARISON_REMEDIATION_PLAN
    if (
        "movement review" in normalized
        or "payroll movement review" in normalized
    ) and (
        "worker story" not in normalized
        and "payrun admin queue" not in normalized
        and "admin queue" not in normalized
        and "payroll bases" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "show" in normalized
        or "evidence" in normalized
        or "explain" in normalized
    ):
        return MOVEMENT_REVIEW_PLAN
    if (
        "payrun admin queue" in normalized
        or "admin queue" in normalized
        or "payrun queue" in normalized
        or "assurance snapshot" in normalized
        or "command centre" in normalized
        or ("queue cleanliness" in normalized and "payrun" in normalized)
    ) and (
        "worker story" not in normalized
        and "workerstory" not in normalized
        and "payroll bases" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "show" in normalized
        or "evidence" in normalized
        or "explain" in normalized
    ):
        return PAYRUN_ADMIN_QUEUE_PLAN
    if (
        "payroll bases" in normalized
        or "payroll bases and totals" in normalized
        or "payroll bases totals" in normalized
        or "payrollbucketresult" in normalized
        or "payroll bucket result" in normalized
        or "payrollbucketdefinition" in normalized
        or "payroll bucket definition" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "matter" in normalized
        or "evidence" in normalized
        or "explain" in normalized
    ):
        return PAYROLL_BASES_AND_TOTALS_PLAN
    if (
        "worker story" in normalized
        or "workerstory" in normalized
        or "worker calculation story" in normalized
        or "talking payslip" in normalized
        or "source truth" in normalized
        or "sourcetruth" in normalized
        or "calculated payroll outcome" in normalized
        or "decision story" in normalized
        or "rate story" in normalized
        or ("movement review" in normalized and "admin queue" in normalized)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "relate" in normalized
    ):
        return WORKER_STORY_PLAN
    return None


def _contains_required_term(result: RetrievalResult, group: EvidenceGroup) -> bool:
    haystack = f"{result.title or ''}\n{result.chunk_text}".lower()
    return any(term.lower() in haystack for term in group.required_terms_any)


def _required_term_count(result: RetrievalResult, group: EvidenceGroup) -> int:
    haystack = f"{result.title or ''}\n{result.chunk_text}".lower()
    return sum(1 for term in group.required_terms_any if term.lower() in haystack)


def _source_type_filter(
    requested_source_types: list[str] | None,
    preferred_source_types: tuple[str, ...],
) -> list[str] | None:
    if requested_source_types is None:
        return list(preferred_source_types)
    requested = {normalize_source_type(source_type) for source_type in requested_source_types}
    allowed = [source_type for source_type in preferred_source_types if source_type in requested]
    return allowed or []


def retrieve_with_domain_plan(
    db: Session,
    query: str,
    plan: DomainRetrievalPlan,
    tenant_id: str | None = None,
    source_types: list[str] | None = None,
    include_samples: bool = False,
) -> list[RetrievalResult]:
    seen_chunk_ids: set[str] = set()
    planned_results: list[RetrievalResult] = []

    for group in plan.evidence_groups:
        group_source_types = _source_type_filter(source_types, group.preferred_source_types)
        if group_source_types == []:
            continue
        group_query = " ".join(group.query_terms)
        results = retrieve_relevant_chunks(
            db=db,
            query=group_query,
            tenant_id=tenant_id,
            top_k=max(group.max_chunks * 3, group.max_chunks),
            source_types=group_source_types,
            include_samples=include_samples,
        )
        qualifying_results = sorted(
            [result for result in results if _contains_required_term(result, group)],
            key=lambda result: (_required_term_count(result, group), result.score),
            reverse=True,
        )
        for result in qualifying_results[: group.max_chunks]:
            if result.chunk_id in seen_chunk_ids:
                continue
            seen_chunk_ids.add(result.chunk_id)
            planned_results.append(
                replace(
                    result,
                    domain_plan_id=plan.plan_id,
                    evidence_group_id=group.group_id,
                    evidence_group_label=group.label,
                )
            )

    return planned_results


def retrieve_chunks_for_question(
    db: Session,
    query: str,
    tenant_id: str | None = None,
    top_k: int = 5,
    source_types: list[str] | None = None,
    include_samples: bool = False,
) -> list[RetrievalResult]:
    answer_mode = classify_answer_mode(query)
    plan = detect_domain_retrieval_plan(query) if answer_mode == AnswerMode.PRODUCT_DOMAIN.value else None
    if plan:
        planned_results = retrieve_with_domain_plan(
            db=db,
            query=query,
            plan=plan,
            tenant_id=tenant_id,
            source_types=source_types,
            include_samples=include_samples,
        )
        if planned_results:
            return planned_results

    return retrieve_relevant_chunks(
        db=db,
        query=query,
        tenant_id=tenant_id,
        top_k=top_k,
        source_types=source_types,
        include_samples=include_samples,
    )

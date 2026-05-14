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

WORKER_ATTENTION_ISSUE_RESOLUTION_PLAN = DomainRetrievalPlan(
    plan_id="WORKER_ATTENTION_ISSUE_RESOLUTION",
    domain="Worker Attention / Issue Resolution",
    trigger_phrases=(
        "what is worker attention / issue resolution",
        "what is worker attention issue resolution",
        "what is worker attention in the platform",
        "what is issue resolution in the platform",
        "how should worker attention issue resolution work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="worker_attention_purpose",
            label="Worker Attention / Issue Resolution purpose",
            query_terms=("Worker Attention", "WorkerAttention", "Worker Attention Centre", "Issue Resolution", "worker-level issue surface"),
            required_terms_any=("Worker Attention", "WorkerAttention", "Worker Attention Centre", "Issue Resolution", "worker-level issue surface"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_issue_model",
            label="Worker Attention worker issue model",
            query_terms=("Worker issue", "WorkerIssue", "issue scope", "issue class", "issue type", "issue severity"),
            required_terms_any=("Worker issue", "WorkerIssue", "issue scope", "issue class", "issue type", "issue severity"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="blockers_warnings_and_readiness",
            label="Worker Attention blockers warnings and readiness",
            query_terms=("blockers", "warnings", "readiness gaps", "worker-level blockers", "worker-level warnings", "ready actions"),
            required_terms_any=("blockers", "warnings", "readiness gaps", "worker-level blockers", "worker-level warnings", "ready actions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deterministic_fix_links",
            label="Worker Attention deterministic fix links",
            query_terms=("deterministic fix link", "deterministic fix links", "resolution surfaces", "fix action", "server-owned fix target"),
            required_terms_any=("deterministic fix link", "deterministic fix links", "resolution surfaces", "fix action", "server-owned fix target"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="dirty_contact_and_reprocessing",
            label="Worker Attention dirty contact and reprocessing",
            query_terms=("dirty contact", "dirty contacts", "PayRunContact dirty", "reprocessing", "reprocess", "contact changes"),
            required_terms_any=("dirty contact", "dirty contacts", "PayRunContact dirty", "reprocessing", "reprocess", "contact changes"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_allocation_readiness",
            label="Worker Attention payment allocation readiness",
            query_terms=("payment allocation", "payment allocation readiness", "payment destination", "bank allocation", "payment readiness"),
            required_terms_any=("payment allocation", "payment allocation readiness", "payment destination", "bank allocation", "payment readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="tax_deduction_leave_readiness",
            label="Worker Attention tax deduction leave readiness",
            query_terms=("tax readiness", "deduction readiness", "leave readiness", "tax/deduction/leave readiness", "readiness evidence"),
            required_terms_any=("tax readiness", "deduction readiness", "leave readiness", "tax/deduction/leave readiness", "readiness evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="negative_net_pay_and_obligations",
            label="Worker Attention negative net pay and obligations",
            query_terms=("negative net pay", "obligations", "out-of-pay", "recoveries", "worker obligation", "obligation issue"),
            required_terms_any=("negative net pay", "obligations", "out-of-pay", "recoveries", "worker obligation", "obligation issue"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_relationship",
            label="Worker Attention Worker Story relationship",
            query_terms=("Worker Attention", "Worker Story", "worker issue evidence", "worker evidence", "explanation surface"),
            required_terms_any=("Worker Attention", "Worker Story", "worker issue evidence", "worker evidence", "explanation surface"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="admin_queue_relationship",
            label="Worker Attention PayRun Admin Queue relationship",
            query_terms=("Worker Attention", "PayRun Admin Queue", "Admin Queue", "operator workbench", "not the same surface"),
            required_terms_any=("Worker Attention", "PayRun Admin Queue", "Admin Queue", "operator workbench", "not the same surface"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Worker Attention outstanding hardening",
            query_terms=("Worker Attention", "outstanding hardening", "WorkerIssue", "issue taxonomy", "resolution workflow", "contract tests"),
            required_terms_any=("Worker Attention", "outstanding hardening", "WorkerIssue", "issue taxonomy", "resolution workflow", "contract tests"),
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

PAYMENT_EXECUTION_REMITTANCE_PLAN = DomainRetrievalPlan(
    plan_id="PAYMENT_EXECUTION_REMITTANCE",
    domain="Payment Execution / Remittance",
    trigger_phrases=(
        "how should payment execution and remittance work",
        "how should payment execution / remittance work",
        "what is payment execution and remittance",
        "what is payment execution / remittance",
        "how does payment execution and remittance work",
        "how does payment execution / remittance work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Payment Execution / Remittance purpose and operator meaning",
            query_terms=("Payment Execution / Remittance", "governed payment execution", "remittance evidence", "generic file export"),
            required_terms_any=("Payment Execution / Remittance", "governed payment execution", "remittance evidence", "generic file export"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalised_gross_to_net_source",
            label="Payment Execution / Remittance finalised gross-to-net source",
            query_terms=("finalised gross-to-net", "finalised payroll outcome", "payment outcome", "payroll calculation truth"),
            required_terms_any=("finalised gross-to-net", "finalised payroll outcome", "payment outcome", "payroll calculation truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_net_pay_and_bank_allocation",
            label="Payment Execution / Remittance worker net pay and bank allocation",
            query_terms=("worker net pay", "bank allocation", "payment allocation", "bank instruction readiness"),
            required_terms_any=("worker net pay", "bank allocation", "payment allocation", "bank instruction readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_destination_readiness",
            label="Payment Execution / Remittance payment destination readiness",
            query_terms=("payment destination", "missing payment destination", "partial payment destinations", "payment execution readiness"),
            required_terms_any=("payment destination", "missing payment destination", "partial payment destinations", "payment execution readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="negative_net_pay_and_obligation_interaction",
            label="Payment Execution / Remittance negative net pay and obligation interaction",
            query_terms=("negative net pay", "obligations", "carry-forward", "recovery", "write-off", "out-of-pay treatment"),
            required_terms_any=("negative net pay", "obligations", "carry-forward", "recovery", "write-off", "out-of-pay treatment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deduction_and_third_party_remittance",
            label="Payment Execution / Remittance deduction and third-party remittance",
            query_terms=("deduction remittance", "third-party remittance", "third-party payments", "remittance files", "payment destinations"),
            required_terms_any=("deduction remittance", "third-party remittance", "third-party payments", "remittance files", "payment destinations"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_file_generation_and_period_close",
            label="Payment Execution / Remittance payment file generation and period close",
            query_terms=("Generate Bank File", "Bank File", "payment file", "Period Close", "payment-file execution"),
            required_terms_any=("Generate Bank File", "Bank File", "payment file", "Period Close", "payment-file execution"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="remittance_batching_and_reconciliation",
            label="Payment Execution / Remittance batching and reconciliation",
            query_terms=("remittance batching", "remittance reconciliation", "reconciliation", "batching", "remittance batch"),
            required_terms_any=("remittance batching", "remittance reconciliation", "reconciliation", "batching", "remittance batch"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_attention_and_admin_queue_connection",
            label="Payment Execution / Remittance Worker Attention and Admin Queue connection",
            query_terms=("Payment Execution / Remittance", "Worker Attention", "PayRun Admin Queue", "blockers", "warnings", "actions"),
            required_terms_any=("Payment Execution / Remittance", "Worker Attention", "PayRun Admin Queue", "blockers", "warnings", "actions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_audit_evidence",
            label="Payment Execution / Remittance Worker Story and audit evidence",
            query_terms=("Payment Execution / Remittance", "Worker Story", "audit evidence", "payment allocation", "remittance", "skipped", "unpaid", "unmet"),
            required_terms_any=("Payment Execution / Remittance", "Worker Story", "audit evidence", "payment allocation", "remittance", "skipped", "unpaid", "unmet"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Payment Execution / Remittance outstanding hardening",
            query_terms=(
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
            required_terms_any=(
                "outstanding hardening",
                "bank file generation",
                "remittance execution",
                "reconciliation",
                "payment close",
                "obligation write-off",
                "financial consequences",
                "UI surfaces",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

LEAVE_ACCRUAL_PROCESSING_PLAN = DomainRetrievalPlan(
    plan_id="LEAVE_ACCRUAL_PROCESSING",
    domain="Leave Accrual Detail / Leave Processing",
    trigger_phrases=(
        "how does leave accrue and get processed",
        "how does leave accrue and get processed in ezeas",
        "how does leave accrual processing work",
        "what is leave accrual processing",
        "how does leave processing work",
        "leave accrual detail",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Leave Accrual / Processing purpose and operator meaning",
            query_terms=("Leave Accrual", "Leave Processing", "deterministic platform outcomes", "Minerva calculations", "generic leave policy advice"),
            required_terms_any=("Leave Accrual", "Leave Processing", "deterministic platform outcomes", "Minerva calculations", "generic leave policy advice"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_source_truth_and_applicability",
            label="Leave Accrual / Processing source truth and applicability",
            query_terms=("leave source truth", "applicability", "LeaveTypeRule", "Leave Source Model", "source truth"),
            required_terms_any=("leave source truth", "applicability", "LeaveTypeRule", "Leave Source Model", "source truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="accrual_basis_and_quantity",
            label="Leave Accrual / Processing accrual basis and quantity",
            query_terms=("accrual basis", "PER_HOUR", "minute", "hour", "accrual quantity"),
            required_terms_any=("accrual basis", "PER_HOUR", "minute", "hour", "accrual quantity"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_output_and_calc_interpreter_source",
            label="Leave Accrual / Processing payroll output and CalcInterpreter source",
            query_terms=("CalcInterpreterLine", "current-effective payroll output", "canonical processed payroll result truth", "payroll result truth"),
            required_terms_any=("CalcInterpreterLine", "current-effective payroll output", "canonical processed payroll result truth", "payroll result truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_type_and_rule_configuration",
            label="Leave Accrual / Processing leave type and rule configuration",
            query_terms=("LeaveType", "LeaveTypeRule", "AwardRateType", "RateType", "accrualability"),
            required_terms_any=("LeaveType", "LeaveTypeRule", "AwardRateType", "RateType", "accrualability"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_ledger_and_accrual_posting",
            label="Leave Accrual / Processing LeaveLedger and accrual posting",
            query_terms=("LeaveLedger", "Leave Ledger", "accrual", "payment", "balance movements", "story evidence"),
            required_terms_any=("LeaveLedger", "Leave Ledger", "accrual", "payment", "balance movements", "story evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_valuation_basis",
            label="Leave Accrual / Processing leave valuation basis",
            query_terms=("leave valuation basis", "TAKEN leave", "valuation", "mandatory", "hard failure", "silent fallback"),
            required_terms_any=("leave valuation basis", "TAKEN leave", "valuation", "mandatory", "hard failure", "silent fallback"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_request_payment_effects",
            label="Leave Accrual / Processing leave request payment effects",
            query_terms=("leave request", "payment effects", "before payroll interpretation", "within payroll interpretation", "after payroll interpretation"),
            required_terms_any=("leave request", "payment effects", "before payroll interpretation", "within payroll interpretation", "after payroll interpretation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_processing_and_finalisation",
            label="Leave Accrual / Processing PayRun processing and finalisation",
            query_terms=("LeaveProcessRun", "PayRun", "finalisation readiness", "missing leave output", "leave readiness"),
            required_terms_any=("LeaveProcessRun", "PayRun", "finalisation readiness", "missing leave output", "leave readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Leave Accrual / Processing Worker Story connection",
            query_terms=("Worker Story", "Leave and Accrual Outcome", "server-owned leave output", "ledger", "valuation evidence"),
            required_terms_any=("Worker Story", "Leave and Accrual Outcome", "server-owned leave output", "ledger", "valuation evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_connection",
            label="Leave Accrual / Processing Payroll Bases connection",
            query_terms=("Payroll Bases & Totals", "worked hours", "basis quantity", "governed basis evidence", "leave basis quantities"),
            required_terms_any=("Payroll Bases & Totals", "worked hours", "basis quantity", "governed basis evidence", "leave basis quantities"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Leave Accrual / Processing outstanding hardening",
            query_terms=(
                "outstanding hardening",
                "Leave Source Model",
                "leave-processing UI",
                "leave request ownership",
                "contact-vs-appointment",
                "leave story polish",
                "finalisation warning acknowledgement",
            ),
            required_terms_any=(
                "outstanding hardening",
                "Leave Source Model",
                "leave-processing UI",
                "leave request ownership",
                "contact-vs-appointment",
                "leave story polish",
                "finalisation warning acknowledgement",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

LEAVE_SOURCE_MODEL_PLAN = DomainRetrievalPlan(
    plan_id="LEAVE_SOURCE_MODEL",
    domain="Leave Source Model",
    trigger_phrases=(
        "what is the leave source model",
        "why does the leave source model matter",
        "what is the leave source model and why does it matter",
        "how should the leave source model work",
        "leave source model",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Leave Source Model purpose and operator meaning",
            query_terms=("Leave Source Model", "governed applicability", "source-truth layer", "leave applies", "worker context"),
            required_terms_any=("Leave Source Model", "governed applicability", "source-truth layer", "leave applies", "worker context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="applicability_vs_rule_content",
            label="Leave Source Model applicability versus rule content",
            query_terms=("applicability", "rule content", "LeaveTypeRule", "policy calculation content", "source truth"),
            required_terms_any=("applicability", "rule content", "LeaveTypeRule", "policy calculation content", "source truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_type_rule_limitations",
            label="Leave Source Model LeaveTypeRule limitations",
            query_terms=("LeaveTypeRule", "final applicability truth", "active LeaveTypeRule", "every worker", "leave output"),
            required_terms_any=("LeaveTypeRule", "final applicability truth", "active LeaveTypeRule", "every worker", "leave output"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="contact_vs_appointment_scope",
            label="Leave Source Model contact versus appointment scope",
            query_terms=("Contact scope", "EmployeeAppointment scope", "appointment-aware leave", "contact-level", "appointment-level"),
            required_terms_any=("Contact scope", "EmployeeAppointment scope", "appointment-aware leave", "contact-level", "appointment-level"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="source_dimensions_and_precedence",
            label="Leave Source Model source dimensions and precedence",
            query_terms=("Account", "EmploymentType", "WorksitePosition", "Worksite", "EmployeeAppointment", "Contact", "AwardPositionClass", "AwardPosition", "Position", "Award", "State", "precedence"),
            required_terms_any=("Account", "EmploymentType", "WorksitePosition", "Worksite", "EmployeeAppointment", "Contact", "AwardPositionClass", "AwardPosition", "Position", "Award", "State", "precedence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_accrual_connection",
            label="Leave Source Model leave accrual connection",
            query_terms=("leave accrual", "source applicability decisions", "accrual", "consume source", "infer ad hoc"),
            required_terms_any=("leave accrual", "source applicability decisions", "accrual", "consume source", "infer ad hoc"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_request_and_payment_effects_connection",
            label="Leave Source Model leave request and payment effects connection",
            query_terms=("leave request", "payment effects", "source applicability decisions", "leave ownership", "request ownership"),
            required_terms_any=("leave request", "payment effects", "source applicability decisions", "leave ownership", "request ownership"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="Leave Source Model Worker Story connection",
            query_terms=("Worker Story", "leave chapters", "source applicability decisions", "leave output", "warnings"),
            required_terms_any=("Worker Story", "leave chapters", "source applicability decisions", "leave output", "warnings"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="command_centre_and_finalisation_connection",
            label="Leave Source Model Command Centre and finalisation connection",
            query_terms=("Command Centre", "Finalisation Readiness", "PayRun finalisation warnings", "leave readiness", "honestly"),
            required_terms_any=("Command Centre", "Finalisation Readiness", "PayRun finalisation warnings", "leave readiness", "honestly"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="readiness_and_missing_output_detection",
            label="Leave Source Model readiness and missing output detection",
            query_terms=("leave readiness", "missing leave output", "leave does not apply", "leave output is missing", "source truth"),
            required_terms_any=("leave readiness", "missing leave output", "leave does not apply", "leave output is missing", "source truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Leave Source Model outstanding hardening",
            query_terms=("outstanding hardening", "planned model", "required model", "not complete", "runtime capability"),
            required_terms_any=("outstanding hardening", "planned model", "required model", "not complete", "runtime capability"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

ONCOSTS_EMPLOYER_LIABILITIES_PLAN = DomainRetrievalPlan(
    plan_id="ONCOSTS_EMPLOYER_LIABILITIES",
    domain="On-costs / Employer Liabilities",
    trigger_phrases=(
        "how should on-costs and employer liabilities work",
        "how should oncosts and employer liabilities work",
        "what are on-costs and employer liabilities",
        "what are employer liabilities",
        "how should employer liability work",
        "how should employer liabilities work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="On-costs / Employer Liabilities purpose and operator meaning",
            query_terms=("On-costs", "Employer Liabilities", "governed employer liability evidence", "operator meaning", "not reporting add-on"),
            required_terms_any=("On-costs", "Employer Liabilities", "governed employer liability evidence", "operator meaning", "not reporting add-on"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="employer_liability_not_worker_pay",
            label="On-costs / Employer Liabilities not worker pay",
            query_terms=("employer liability", "not worker pay", "not worker net pay", "not payroll calculation truth", "Minerva does not calculate"),
            required_terms_any=("employer liability", "not worker pay", "not worker net pay", "not payroll calculation truth", "Minerva does not calculate"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_source_and_date_effective_rates",
            label="On-costs / Employer Liabilities RateSource and date-effective rates",
            query_terms=("RateSource", "date-effective rates", "date-effective RateSource", "rule-pack configuration", "application code"),
            required_terms_any=("RateSource", "date-effective rates", "date-effective RateSource", "rule-pack configuration", "application code"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="award_rate_type_and_rate_type_settings",
            label="On-costs / Employer Liabilities AwardRateType and RateType settings",
            query_terms=("AwardRateType", "RateType", "SUPER_ONCOST", "PAYROLLTAX_ONCOST", "WORKCOVER_ONCOST", "award defaults"),
            required_terms_any=("AwardRateType", "RateType", "SUPER_ONCOST", "PAYROLLTAX_ONCOST", "WORKCOVER_ONCOST", "award defaults"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="governed_basis_membership",
            label="On-costs / Employer Liabilities governed basis membership",
            query_terms=("governed basis membership", "bucket membership", "basis membership", "raw flags", "runtime basis decisions"),
            required_terms_any=("governed basis membership", "bucket membership", "basis membership", "raw flags", "runtime basis decisions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="super_payroll_tax_and_workcover_wic",
            label="On-costs / Employer Liabilities super payroll tax and WorkCover WIC",
            query_terms=("superannuation on-cost", "payroll tax on-cost", "WorkCover", "WIC", "jurisdiction"),
            required_terms_any=("superannuation on-cost", "payroll tax on-cost", "WorkCover", "WIC", "jurisdiction"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="state_worksite_and_runtime_location_resolution",
            label="On-costs / Employer Liabilities state worksite and runtime location resolution",
            query_terms=("state", "worksite", "runtime location", "state-scoped RateSource", "state-scoped employer liabilities"),
            required_terms_any=("state", "worksite", "runtime location", "state-scoped RateSource", "state-scoped employer liabilities"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_output_and_worker_story_connection",
            label="On-costs / Employer Liabilities PayRun output and Worker Story connection",
            query_terms=("PayRun output", "Worker Story", "worker-payable lines", "employer liability lines", "on-cost evidence"),
            required_terms_any=("PayRun output", "Worker Story", "worker-payable lines", "employer liability lines", "on-cost evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_connection",
            label="On-costs / Employer Liabilities Payroll Bases connection",
            query_terms=("Payroll Bases & Totals", "governed basis evidence", "liability calculations", "basis evidence", "basis totals"),
            required_terms_any=("Payroll Bases & Totals", "governed basis evidence", "liability calculations", "basis evidence", "basis totals"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalisation_and_readiness_connection",
            label="On-costs / Employer Liabilities finalisation and readiness connection",
            query_terms=("Finalisation Readiness", "unresolved basis", "liability configuration", "policy requires", "readiness"),
            required_terms_any=("Finalisation Readiness", "unresolved basis", "liability configuration", "policy requires", "readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="demo_fallback_vs_production_truth",
            label="On-costs / Employer Liabilities demo fallback versus production truth",
            query_terms=("demo fallback", "account-wide fallback", "RateSource rows", "production truth", "unblock demos"),
            required_terms_any=("demo fallback", "account-wide fallback", "RateSource rows", "production truth", "unblock demos"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="On-costs / Employer Liabilities outstanding hardening",
            query_terms=("outstanding hardening", "runtime state", "worksite resolution", "award creation seeding", "production replacement"),
            required_terms_any=("outstanding hardening", "runtime state", "worksite resolution", "award creation seeding", "production replacement"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

AWARD_BUILD_EVIDENCE_PLAN = DomainRetrievalPlan(
    plan_id="AWARD_BUILD_EVIDENCE",
    domain="Award Build / Award Evidence",
    trigger_phrases=(
        "how should award build and award evidence work",
        "what is award build and award evidence",
        "how does award build evidence work",
        "how should award evidence work",
        "how should award build work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Award Build / Award Evidence purpose and operator meaning",
            query_terms=("Award Build", "Award Evidence", "governed configuration", "traceable evidence", "not runtime payroll calculation"),
            required_terms_any=("Award Build", "Award Evidence", "governed configuration", "traceable evidence", "not runtime payroll calculation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="award_document_and_pay_guide_sources",
            label="Award Build / Award Evidence award document and pay guide sources",
            query_terms=("award document", "pay guide", "pay guide evidence", "source evidence", "row column page evidence"),
            required_terms_any=("award document", "pay guide", "pay guide evidence", "source evidence", "row column page evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_type_and_award_rate_type_creation",
            label="Award Build / Award Evidence RateType and AwardRateType creation",
            query_terms=("RateType", "Rate Type", "AwardRateType", "Award Rate Type", "stable conceptual pay type", "award-scoped treatment"),
            required_terms_any=("RateType", "Rate Type", "AwardRateType", "Award Rate Type", "stable conceptual pay type", "award-scoped treatment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_source_and_date_effective_rate_evidence",
            label="Award Build / Award Evidence RateSource and date-effective rate evidence",
            query_terms=("RateSource", "date-effective", "rate amounts", "rate evidence", "hardcoded rates"),
            required_terms_any=("RateSource", "date-effective", "rate amounts", "rate evidence", "hardcoded rates"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="classification_position_and_class_evidence",
            label="Award Build / Award Evidence classification position and class evidence",
            query_terms=("classification", "position", "class evidence", "deterministically derived", "reviewed", "not guessed"),
            required_terms_any=("classification", "position", "class evidence", "deterministically derived", "reviewed", "not guessed"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="allowances_penalties_and_conditions",
            label="Award Build / Award Evidence allowances penalties and conditions",
            query_terms=("allowances", "penalties", "conditions", "shift", "overtime", "source evidence"),
            required_terms_any=("allowances", "penalties", "conditions", "shift", "overtime", "source evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="decision_evidence_index",
            label="Award Build / Award Evidence DecisionEvidenceIndex",
            query_terms=("DecisionEvidenceIndex", "Decision Evidence Index", "why a treatment", "why a line exists", "decision evidence"),
            required_terms_any=("DecisionEvidenceIndex", "Decision Evidence Index", "why a treatment", "why a line exists", "decision evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_source_evidence_index",
            label="Award Build / Award Evidence RateSourceEvidenceIndex",
            query_terms=("RateSourceEvidenceIndex", "Rate Source Evidence Index", "why a rate", "why an amount", "rate source evidence"),
            required_terms_any=("RateSourceEvidenceIndex", "Rate Source Evidence Index", "why a rate", "why an amount", "rate source evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_decision_and_rate_story_connection",
            label="Award Build / Award Evidence Worker Story Decision Story and Rate Story connection",
            query_terms=("Worker Story", "Decision Story", "Rate Story", "award build", "runtime artifacts", "PayRun interpretation evidence"),
            required_terms_any=("Worker Story", "Decision Story", "Rate Story", "award build", "runtime artifacts", "PayRun interpretation evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="needs_configuration_and_build_status",
            label="Award Build / Award Evidence NEEDS_CONFIGURATION and build status",
            query_terms=("NEEDS_CONFIGURATION", "award build status", "missing evidence", "missing configuration", "valid build outcome"),
            required_terms_any=("NEEDS_CONFIGURATION", "award build status", "missing evidence", "missing configuration", "valid build outcome"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="durable_award_evidence_set",
            label="Award Build / Award Evidence durable AwardEvidenceSet",
            query_terms=("AwardEvidenceSet", "Durable AwardEvidenceSet", "durable evidence", "artifact based", "file based", "future hardening"),
            required_terms_any=("AwardEvidenceSet", "Durable AwardEvidenceSet", "durable evidence", "artifact based", "file based", "future hardening"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Award Build / Award Evidence outstanding hardening",
            query_terms=("outstanding hardening", "semantic table classification", "durable evidence sets", "parser routing", "conditional award regimes", "source evidence coverage"),
            required_terms_any=("outstanding hardening", "semantic table classification", "durable evidence sets", "parser routing", "conditional award regimes", "source evidence coverage"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

IMPORTS_ACTUALS_PLAN = DomainRetrievalPlan(
    plan_id="IMPORTS_ACTUALS",
    domain="Imports / Actuals",
    trigger_phrases=(
        "how should imports and actuals work",
        "how should imports / actuals work",
        "what are imports and actuals",
        "how should imported timesheets work",
        "how should imported payroll actuals work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Imports / Actuals purpose and operator meaning",
            query_terms=("Imports / Actuals", "Imports and Actuals", "governed imported evidence", "external source evidence", "not calculated interpreter truth"),
            required_terms_any=("Imports / Actuals", "Imports and Actuals", "governed imported evidence", "external source evidence", "not calculated interpreter truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="imported_timesheet_source_truth",
            label="Imports / Actuals imported timesheet source truth",
            query_terms=("imported timesheets", "timesheet source truth", "ObjectTime", "work evidence", "validation and mapping"),
            required_terms_any=("imported timesheets", "timesheet source truth", "ObjectTime", "work evidence", "validation and mapping"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="imported_payroll_actuals_lane",
            label="Imports / Actuals imported payroll actuals lane",
            query_terms=("imported payroll actuals", "payroll actuals", "actuals lane", "external outcome lane", "calculated interpreter output"),
            required_terms_any=("imported payroll actuals", "payroll actuals", "actuals lane", "external outcome lane", "calculated interpreter output"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="source_system_mapping_and_validation",
            label="Imports / Actuals source-system mapping and validation",
            query_terms=("source-system mapping", "source system mapping", "validation", "workers", "dates", "source rows"),
            required_terms_any=("source-system mapping", "source system mapping", "validation", "workers", "dates", "source rows"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="pay_code_and_rate_type_mapping",
            label="Imports / Actuals pay code and RateType mapping",
            query_terms=("pay code mapping", "source-system pay code", "RateType mapping", "platform concepts", "unmapped actuals"),
            required_terms_any=("pay code mapping", "source-system pay code", "RateType mapping", "platform concepts", "unmapped actuals"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="position_classification_mapping",
            label="Imports / Actuals position and classification mapping",
            query_terms=("ImportedPositionClassificationMap", "position mapping", "classification mapping", "source-system classification", "source-system position"),
            required_terms_any=("ImportedPositionClassificationMap", "position mapping", "classification mapping", "source-system classification", "source-system position"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="objecttime_and_source_truth_connection",
            label="Imports / Actuals ObjectTime and source truth connection",
            query_terms=("ObjectTime source truth", "ObjectTime", "source truth", "source row", "import provenance"),
            required_terms_any=("ObjectTime source truth", "ObjectTime", "source truth", "source row", "import provenance"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_and_remediation_connection",
            label="Imports / Actuals Comparison / Remediation connection",
            query_terms=("Comparison / Remediation", "primary calculated", "comparator calculated", "imported actual lanes", "variance"),
            required_terms_any=("Comparison / Remediation", "primary calculated", "comparator calculated", "imported actual lanes", "variance"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="reconciliation_and_movement_review_connection",
            label="Imports / Actuals reconciliation and Movement Review connection",
            query_terms=("reconciliation", "Movement Review", "imported actuals", "source evidence", "review outcomes"),
            required_terms_any=("reconciliation", "Movement Review", "imported actuals", "source evidence", "review outcomes"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_admin_queue_connection",
            label="Imports / Actuals Worker Story and Admin Queue connection",
            query_terms=("Worker Story", "Admin Queue", "import provenance", "mapping issues", "unmapped actuals", "missing classifications"),
            required_terms_any=("Worker Story", "Admin Queue", "import provenance", "mapping issues", "unmapped actuals", "missing classifications"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="evidence_provenance_and_audit",
            label="Imports / Actuals evidence provenance and audit",
            query_terms=("evidence provenance", "audit", "source file", "source row", "import run", "mapping decision", "validation status"),
            required_terms_any=("evidence provenance", "audit", "source file", "source row", "import run", "mapping decision", "validation status"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Imports / Actuals outstanding hardening",
            query_terms=("outstanding hardening", "actuals lane model", "import mapping UI", "comparison-line models", "source-system classification mapping", "source-row evidence", "validation workflows"),
            required_terms_any=("outstanding hardening", "actuals lane model", "import mapping UI", "comparison-line models", "source-system classification mapping", "source-row evidence", "validation workflows"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

OBJECTTIME_SOURCE_TRUTH_PLAN = DomainRetrievalPlan(
    plan_id="OBJECTTIME_SOURCE_TRUTH",
    domain="ObjectTime / Source Truth",
    trigger_phrases=(
        "what is objecttime source truth",
        "what is objecttime / source truth",
        "why does objecttime source truth matter",
        "why does objecttime / source truth matter",
        "how should objecttime source truth work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="ObjectTime / Source Truth purpose and operator meaning",
            query_terms=("ObjectTime / Source Truth", "ObjectTime", "Source Truth", "governed source evidence", "not payroll calculation truth"),
            required_terms_any=("ObjectTime / Source Truth", "ObjectTime", "Source Truth", "governed source evidence", "not payroll calculation truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="objecttime_as_source_evidence",
            label="ObjectTime / Source Truth ObjectTime as source evidence",
            query_terms=("ObjectTime", "source evidence", "work time", "source row", "inclusion context"),
            required_terms_any=("ObjectTime", "source evidence", "work time", "source row", "inclusion context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_inclusion_and_source_truth",
            label="ObjectTime / Source Truth PayRun inclusion and SourceTruth",
            query_terms=("PayRun inclusion", "SourceTruth", "Source Truth", "source inclusion", "belongs in a PayRun"),
            required_terms_any=("PayRun inclusion", "SourceTruth", "Source Truth", "source inclusion", "belongs in a PayRun"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="imported_and_generated_source_rows",
            label="ObjectTime / Source Truth imported and generated source rows",
            query_terms=("imported source rows", "generated source rows", "source row", "provenance", "validation mapping status"),
            required_terms_any=("imported source rows", "generated source rows", "source row", "provenance", "validation mapping status"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="source_truth_vs_worked_hours",
            label="ObjectTime / Source Truth SourceTruth versus WorkedHours",
            query_terms=("SourceTruth", "WorkedHours", "worked hours", "raw span hours", "span hours", "interpreted payable hours"),
            required_terms_any=("SourceTruth", "WorkedHours", "worked hours", "raw span hours", "span hours", "interpreted payable hours"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_output_connection",
            label="ObjectTime / Source Truth current-effective output connection",
            query_terms=("current-effective output", "current-effective payroll output", "processed source truth", "payroll outcome", "current-effective truth"),
            required_terms_any=("current-effective output", "current-effective payroll output", "processed source truth", "payroll outcome", "current-effective truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_connection",
            label="ObjectTime / Source Truth Worker Story connection",
            query_terms=("Worker Story", "Source Truth", "source inclusion", "calculated payroll outcome", "Decision Story"),
            required_terms_any=("Worker Story", "Source Truth", "source inclusion", "calculated payroll outcome", "Decision Story"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_and_leave_accrual_connection",
            label="ObjectTime / Source Truth Payroll Bases and leave accrual connection",
            query_terms=("Payroll Bases & Totals", "leave accrual", "processed payroll", "bucket evidence", "raw source span duration"),
            required_terms_any=("Payroll Bases & Totals", "leave accrual", "processed payroll", "bucket evidence", "raw source span duration"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_movement_and_replay_connection",
            label="ObjectTime / Source Truth comparison movement and replay connection",
            query_terms=("Comparison / Remediation", "Movement Review", "Retro / Replay", "source truth", "historical current-effective distinctions"),
            required_terms_any=("Comparison / Remediation", "Movement Review", "Retro / Replay", "source truth", "historical current-effective distinctions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="corrections_dirty_contacts_and_reprocessing",
            label="ObjectTime / Source Truth corrections dirty contacts and reprocessing",
            query_terms=("correction audit", "dirty contact", "dirty PayRunContact", "reprocessing", "source truth correction"),
            required_terms_any=("correction audit", "dirty contact", "dirty PayRunContact", "reprocessing", "source truth correction"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="evidence_provenance_and_audit",
            label="ObjectTime / Source Truth evidence provenance and audit",
            query_terms=("evidence provenance", "audit", "source file", "source row", "ObjectTime", "correction history", "evidence story"),
            required_terms_any=("evidence provenance", "audit", "source file", "source row", "ObjectTime", "correction history", "evidence story"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="ObjectTime / Source Truth outstanding hardening",
            query_terms=(
                "outstanding hardening",
                "guarded dry-run",
                "readiness contract",
                "source-change runtime intake readiness",
                "runtime source-change hook",
                "not implemented",
                "not production enabled",
                "finalised correction intake",
                "review request creation",
                "no correction execution",
                "production enablement",
                "guardrails",
                "non-goals",
                "command-centre source hours cleanup",
                "dependency detection",
            ),
            required_terms_any=(
                "outstanding hardening",
                "guarded dry-run",
                "readiness contract",
                "source-change runtime intake readiness",
                "runtime source-change hook",
                "not implemented",
                "not production enabled",
                "finalised correction intake",
                "review request creation",
                "no correction execution",
                "production enablement",
                "guardrails",
                "non-goals",
                "command-centre source hours cleanup",
                "dependency detection",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

LEAVE_REQUESTS_WORKFLOW_PLAN = DomainRetrievalPlan(
    plan_id="LEAVE_REQUESTS_WORKFLOW",
    domain="Leave Requests / Leave Workflow",
    trigger_phrases=(
        "what is leave requests / leave workflow",
        "what is leave requests leave workflow",
        "what is leave workflow",
        "how should leave requests work",
        "how should leave workflow work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="leave_request_purpose",
            label="Leave Requests / Leave Workflow purpose",
            query_terms=("Leave Requests / Leave Workflow", "Leave Request", "LeaveRequest", "leave workflow", "governed leave request workflow"),
            required_terms_any=("Leave Requests / Leave Workflow", "Leave Request", "LeaveRequest", "leave workflow", "governed leave request workflow"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="request_creation_and_draft_editing",
            label="Leave Requests / Leave Workflow request creation and draft editing",
            query_terms=("Leave Request", "create leave request", "draft leave", "draft editing", "leave request preview"),
            required_terms_any=("Leave Request", "create leave request", "draft leave", "draft editing", "leave request preview"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="status_transitions_and_idempotency",
            label="Leave Requests / Leave Workflow status transitions and idempotency",
            query_terms=("leave status", "status transitions", "IdempotencyKey", "idempotency", "idempotent leave"),
            required_terms_any=("leave status", "status transitions", "IdempotencyKey", "idempotency", "idempotent leave"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="submission_review_approval_reopen",
            label="Leave Requests / Leave Workflow submission review approval reopen",
            query_terms=("leave submission", "submit leave", "approve leave", "reject leave", "reopen leave", "review leave"),
            required_terms_any=("leave submission", "submit leave", "approve leave", "reject leave", "reopen leave", "review leave"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="overlap_and_shortfall_handling",
            label="Leave Requests / Leave Workflow overlap and shortfall handling",
            query_terms=("leave overlap", "overlap handling", "shortfall substitution", "shortfall", "substitution"),
            required_terms_any=("leave overlap", "overlap handling", "shortfall substitution", "shortfall", "substitution"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="taken_leave_valuation_and_hard_fail",
            label="Leave Requests / Leave Workflow TAKEN leave valuation and hard fail",
            query_terms=("TAKEN leave", "leave valuation", "hard fail", "hard-fail", "leave valuation basis"),
            required_terms_any=("TAKEN leave", "leave valuation", "hard fail", "hard-fail", "leave valuation basis"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_ledger_posting",
            label="Leave Requests / Leave Workflow LeaveLedger posting",
            query_terms=("LeaveLedger", "leave posting", "LeaveLedger posting", "leave balance", "leave ledger rows"),
            required_terms_any=("LeaveLedger", "leave posting", "LeaveLedger posting", "leave balance", "leave ledger rows"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_source_and_applicability_relationship",
            label="Leave Requests / Leave Workflow Leave Source and applicability relationship",
            query_terms=("Leave Source Model", "leave applicability", "LeaveTypeRule", "source applicability", "leave source"),
            required_terms_any=("Leave Source Model", "leave applicability", "LeaveTypeRule", "source applicability", "leave source"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_payrun_relationship",
            label="Leave Requests / Leave Workflow Worker Story and PayRun relationship",
            query_terms=("Worker Story", "PayRun", "leave request payment", "Leave and Accrual Outcome", "worker leave evidence"),
            required_terms_any=("Worker Story", "PayRun", "leave request payment", "Leave and Accrual Outcome", "worker leave evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalisation_and_readiness_relationship",
            label="Leave Requests / Leave Workflow finalisation and readiness relationship",
            query_terms=("finalisation readiness", "leave readiness", "missing leave output", "PayRun finalisation", "readiness"),
            required_terms_any=("finalisation readiness", "leave readiness", "missing leave output", "PayRun finalisation", "readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Leave Requests / Leave Workflow outstanding hardening",
            query_terms=("Leave Requests / Leave Workflow", "outstanding hardening", "leave workflow", "request ownership", "leave hardening"),
            required_terms_any=("Leave Requests / Leave Workflow", "outstanding hardening", "leave workflow", "request ownership", "leave hardening"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PUBLIC_HOLIDAYS_PLAN = DomainRetrievalPlan(
    plan_id="PUBLIC_HOLIDAYS",
    domain="Public Holidays",
    trigger_phrases=(
        "how are public holidays handled",
        "how are public holidays handled in the platform",
        "what is public holidays in the platform",
        "how should public holiday handling work",
        "public holiday handling",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="public_holiday_source_and_calendar",
            label="Public Holidays source and calendar",
            query_terms=("PublicHoliday", "Public Holiday", "PublicHolidayGroup", "Public Holiday Group", "public holiday calendar", "observed day", "public holiday override", "governed reference configuration"),
            required_terms_any=("PublicHoliday", "Public Holiday", "PublicHolidayGroup", "Public Holiday Group", "public holiday calendar", "observed day"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worksite_state_and_applicability_context",
            label="Public Holidays worksite state and applicability context",
            query_terms=("public holiday", "PublicHolidayGroup", "Worksite", "WorksitePosition", "EmployeeAppointment", "worker", "applies to a worker", "state", "jurisdiction", "location context", "applicability context", "employer liabilities", "on-costs"),
            required_terms_any=("public holiday", "Worksite", "WorksitePosition", "EmployeeAppointment", "state", "jurisdiction", "location context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_treatment_and_decision_story",
            label="Public Holidays payroll treatment and Decision Story",
            query_terms=("public holiday payroll treatment", "deterministic payroll interpretation", "public holiday treatment decisions", "public holiday decision", "entitlement decision", "treatment decision", "Decision Story", "Payroll Output", "deterministic payroll services"),
            required_terms_any=("public holiday payroll treatment", "public holiday decision", "Decision Story", "Payroll Output", "deterministic payroll services"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_interaction_and_deducts_on_public_holiday",
            label="Public Holidays leave interaction and DeductsOnPublicHoliday",
            query_terms=("DeductsOnPublicHoliday", "Deducts On Public Holiday", "public holiday leave treatment", "leave request", "leave preview", "LeaveLedger", "leave posting"),
            required_terms_any=("DeductsOnPublicHoliday", "Deducts On Public Holiday", "public holiday leave treatment", "leave request", "LeaveLedger"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_admin_queue_and_finalisation",
            label="Public Holidays Worker Story Admin Queue and finalisation",
            query_terms=("public holiday", "Worker Story", "Decision Story", "Payroll Output", "payroll evidence", "source/context visibility", "PayRun Admin Queue", "Worker Attention", "Finalisation Readiness", "public holiday configuration", "NEEDS_CONFIGURATION", "source context missing", "operator evidence"),
            required_terms_any=("public holiday", "Worker Story", "Admin Queue", "Worker Attention", "Finalisation Readiness", "operator evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

ROSTERS_PATTERNS_SCHEDULING_PLAN = DomainRetrievalPlan(
    plan_id="ROSTERS_PATTERNS_SCHEDULING",
    domain="Rosters / Patterns / Scheduling",
    trigger_phrases=(
        "how do rosters patterns and scheduling work",
        "how do rosters, patterns and scheduling work",
        "what are rosters patterns and scheduling",
        "rosters patterns scheduling",
        "roster pattern scheduling",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="roster_pattern_source_and_configuration",
            label="Rosters / Patterns / Scheduling source and configuration",
            query_terms=("Roster", "Rosters", "Pattern", "PatternDay", "Pattern Day", "EmployeeAppointmentPattern", "Employee Appointment Pattern", "roster schedule configuration", "expected work context", "governed configuration evidence"),
            required_terms_any=("Roster", "Pattern", "PatternDay", "EmployeeAppointmentPattern", "roster schedule configuration", "expected work context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="appointment_worksite_and_applicability_context",
            label="Rosters / Patterns / Scheduling appointment worksite and applicability context",
            query_terms=("Roster", "Pattern", "EmployeeAppointment", "WorksitePosition", "Worksite", "state", "public holiday context", "assignment context", "applicability context"),
            required_terms_any=("Roster", "Pattern", "EmployeeAppointment", "WorksitePosition", "Worksite", "assignment context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="ordinary_hours_leave_basis_and_public_holiday_context",
            label="Rosters / Patterns / Scheduling ordinary hours leave basis and public holiday context",
            query_terms=("ordinary hours", "ordinary-hours", "leave basis minutes", "schedule pattern relationship", "public holiday", "leave interaction", "roster-based basis", "deferred roster-based basis hardening"),
            required_terms_any=("ordinary hours", "leave basis minutes", "public holiday", "leave interaction", "roster-based basis"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_interpretation_and_worker_story_relationship",
            label="Rosters / Patterns / Scheduling payroll interpretation and Worker Story relationship",
            query_terms=("scheduling context", "payroll interpretation", "ObjectTime comparison", "expected schedule", "actual worked time", "Worker Story", "Decision Story", "Payroll Output", "source truth"),
            required_terms_any=("scheduling context", "payroll interpretation", "ObjectTime", "Worker Story", "Decision Story", "Payroll Output"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="admin_queue_finalisation_and_readiness_relationship",
            label="Rosters / Patterns / Scheduling Admin Queue finalisation and readiness relationship",
            query_terms=("missing schedule", "missing pattern", "configuration gaps", "Worker Attention", "PayRun Admin Queue", "Admin Queue", "Finalisation Readiness", "readiness evidence", "NEEDS_CONFIGURATION"),
            required_terms_any=("missing schedule", "missing pattern", "configuration gaps", "Worker Attention", "Admin Queue", "Finalisation Readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

AWARD_POSITIONS_CLASSIFICATIONS_PLAN = DomainRetrievalPlan(
    plan_id="AWARD_POSITIONS_CLASSIFICATIONS",
    domain="Award Positions / Classifications",
    trigger_phrases=(
        "how do award positions and classifications work",
        "how do award positions classifications work",
        "what are award positions and classifications",
        "award positions classifications",
        "award position classification",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="award_position_classification_source_and_build",
            label="Award Positions / Classifications source and build",
            query_terms=("AwardPosition", "Award Position", "AwardPositionClass", "Award Position Class", "PositionClass", "Position Class", "classification levels", "position groups", "pay guide", "class evidence", "award build extraction", "deterministic extraction hardening"),
            required_terms_any=("AwardPosition", "Award Position", "AwardPositionClass", "Award Position Class", "PositionClass", "classification", "pay guide", "class evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="appointment_position_and_worksite_assignment",
            label="Award Positions / Classifications appointment position and worksite assignment",
            query_terms=("EmployeeAppointment", "Employee Appointment", "WorksitePosition", "Worksite Position", "Position", "Worksite", "worker assignment", "assignment context", "award classification", "employment classification"),
            required_terms_any=("EmployeeAppointment", "Employee Appointment", "WorksitePosition", "Worksite Position", "Position", "Worksite", "assignment context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_interpretation_rate_and_decision_story",
            label="Award Positions / Classifications payroll interpretation rate and Decision Story",
            query_terms=("classification context", "payroll interpretation", "RateSource", "Rate Story", "Decision Story", "Payroll Output", "calculated line evidence", "rate selection", "classification facts", "treatment", "entitlement", "classification evidence", "not Decision Story itself"),
            required_terms_any=("classification context", "payroll interpretation", "RateSource", "Rate Story", "Decision Story", "Payroll Output", "classification facts", "classification evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_remediation_and_classification_lenses",
            label="Award Positions / Classifications comparison remediation and classification lenses",
            query_terms=("comparator classification", "award comparison", "comparison remediation", "imported classification mapping", "classification lenses", "comparison classes", "primary appointment class", "classification lens"),
            required_terms_any=("comparator classification", "award comparison", "comparison remediation", "imported classification mapping", "classification lenses", "primary appointment class"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_admin_queue_and_readiness_relationship",
            label="Award Positions / Classifications Worker Story Admin Queue and readiness relationship",
            query_terms=("Worker Story", "PayRun Admin Queue", "Admin Queue", "Worker Attention", "Finalisation Readiness", "readiness", "configuration gaps", "NEEDS_CONFIGURATION", "evidence visibility"),
            required_terms_any=("Worker Story", "Admin Queue", "Worker Attention", "Finalisation Readiness", "configuration gaps", "NEEDS_CONFIGURATION", "evidence visibility"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN = DomainRetrievalPlan(
    plan_id="PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL",
    domain="Payroll Tax / WorkCover / WIC Liability Detail",
    trigger_phrases=(
        "how do payroll tax workcover and wic liabilities work",
        "how do payroll tax, workcover and wic liabilities work",
        "payroll tax workcover wic liability detail",
        "payroll tax workcover wic liabilities",
        "workcover wic liability detail",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="liability_scope_and_employer_side_boundary",
            label="Payroll Tax / WorkCover / WIC liability scope and employer-side boundary",
            query_terms=("Payroll Tax", "PayrollTax", "WorkCover", "Work Cover", "WIC", "Workers Insurance", "Workers Compensation", "employer-side liabilities", "employer-side liability evidence", "not worker net pay", "PAYG withholding", "payment execution"),
            required_terms_any=("Payroll Tax", "PayrollTax", "WorkCover", "WIC", "employer-side liabilities", "employer-side liability evidence", "not worker net pay", "PAYG withholding"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="jurisdiction_worksite_and_state_context",
            label="Payroll Tax / WorkCover / WIC jurisdiction worksite and state context",
            query_terms=("state", "jurisdiction", "Worksite.StateId", "WorksiteState", "Worksite State", "WorksitePosition", "EmployeeAppointment", "ObjectTime location", "runtime location", "public holiday worksite context", "state/worksite context"),
            required_terms_any=("state", "jurisdiction", "Worksite.StateId", "WorksitePosition", "EmployeeAppointment", "ObjectTime location", "runtime location"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="governed_basis_membership_and_payroll_bases",
            label="Payroll Tax / WorkCover / WIC governed basis membership and Payroll Bases",
            query_terms=("governed basis membership", "payroll bucket", "payroll basis evidence", "Payroll Bases & Totals", "taxable wages", "liability wages", "included RateTypes", "excluded RateTypes", "AwardRateTypes", "basis totals"),
            required_terms_any=("governed basis membership", "payroll basis evidence", "Payroll Bases & Totals", "taxable wages", "liability wages", "RateTypes", "AwardRateTypes"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rates_sources_and_liability_evidence",
            label="Payroll Tax / WorkCover / WIC rates sources and liability evidence",
            query_terms=("RateSource", "liability RateSource", "date-effective rates", "date-effective liability rates", "liability rate evidence", "account scoping", "state scoping", "award scoping", "demo fallback", "production truth", "configuration evidence"),
            required_terms_any=("RateSource", "date-effective rates", "liability rate evidence", "demo fallback", "production truth", "configuration evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_output_and_finalisation_relationship",
            label="Payroll Tax / WorkCover / WIC Worker Story output and finalisation relationship",
            query_terms=("Worker Story", "Payroll Output", "Gross-to-Net", "employer liability lines", "worker net pay boundary", "Finalisation Readiness", "PayRun Admin Queue", "Admin Queue", "Worker Attention", "missing liability configuration", "audit evidence", "explanation relationship"),
            required_terms_any=("Worker Story", "Payroll Output", "Gross-to-Net", "Finalisation Readiness", "Admin Queue", "Worker Attention", "employer liability lines"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

CONTACTS_EMPLOYEE_APPOINTMENTS_PLAN = DomainRetrievalPlan(
    plan_id="CONTACTS_EMPLOYEE_APPOINTMENTS",
    domain="Contacts / Employee Appointments",
    trigger_phrases=(
        "how should contacts and employee appointments work",
        "how should contacts / employee appointments work",
        "what are contacts and employee appointments",
        "how should employee appointments work",
        "how should contact appointments work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Contacts / Employee Appointments purpose and operator meaning",
            query_terms=("Contacts / Employee Appointments", "Contact", "EmployeeAppointment", "worker identity context", "employment context", "not payroll calculation truth"),
            required_terms_any=("Contacts / Employee Appointments", "Contact", "EmployeeAppointment", "worker identity context", "employment context", "not payroll calculation truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="contact_identity_and_worker_context",
            label="Contacts / Employee Appointments contact identity and worker context",
            query_terms=("Contact", "worker identity", "person payroll identity", "worker context", "payroll identity context"),
            required_terms_any=("Contact", "worker identity", "person payroll identity", "worker context", "payroll identity context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="employee_appointment_as_employment_assignment",
            label="Contacts / Employee Appointments EmployeeAppointment as employment assignment",
            query_terms=("EmployeeAppointment", "Employee Appointment", "employment assignment", "work assignment", "position worksite classification award"),
            required_terms_any=("EmployeeAppointment", "Employee Appointment", "employment assignment", "work assignment", "position worksite classification award"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="appointment_scope_and_payrun_admission",
            label="Contacts / Employee Appointments appointment scope and PayRun admission",
            query_terms=("appointment scope", "PayRun admission", "source truth", "appointment context", "worker inclusion"),
            required_terms_any=("appointment scope", "PayRun admission", "source truth", "appointment context", "worker inclusion"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="award_classification_and_position_context",
            label="Contacts / Employee Appointments award classification and position context",
            query_terms=("award classification", "AwardPositionClass", "WorksitePosition", "Position", "classification evidence", "appointment"),
            required_terms_any=("award classification", "AwardPositionClass", "WorksitePosition", "Position", "classification evidence", "appointment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worksite_state_and_runtime_location",
            label="Contacts / Employee Appointments worksite state and runtime location",
            query_terms=("worksite", "state", "runtime location", "worksite state", "state evidence", "appointment"),
            required_terms_any=("worksite", "state", "runtime location", "worksite state", "state evidence", "appointment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="objecttime_and_source_truth_connection",
            label="Contacts / Employee Appointments ObjectTime and source truth connection",
            query_terms=("ObjectTime", "source truth", "source rows", "appointments", "contacts", "worker inclusion"),
            required_terms_any=("ObjectTime", "source truth", "source rows", "appointments", "contacts", "worker inclusion"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_source_and_accrual_connection",
            label="Contacts / Employee Appointments leave source and accrual connection",
            query_terms=("leave source", "leave applicability", "leave accrual", "contact scope", "appointment scope"),
            required_terms_any=("leave source", "leave applicability", "leave accrual", "contact scope", "appointment scope"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_contact_history_connection",
            label="Contacts / Employee Appointments Worker Story and contact history connection",
            query_terms=("Worker Story", "Contact history", "finalised payroll outcome memory", "cumulative movement", "source truth context"),
            required_terms_any=("Worker Story", "Contact history", "finalised payroll outcome memory", "cumulative movement", "source truth context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_readiness_tax_bank_deduction_payment",
            label="Contacts / Employee Appointments worker readiness tax bank deduction payment",
            query_terms=("worker readiness", "tax declarations", "bank", "payment allocation", "deductions", "obligations"),
            required_terms_any=("worker readiness", "tax declarations", "bank", "payment allocation", "deductions", "obligations"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="dirty_contact_and_reprocessing",
            label="Contacts / Employee Appointments dirty contact and reprocessing",
            query_terms=("dirty contact", "dirty contacts", "reprocessing", "PayRun output unsafe", "payroll-affecting changes"),
            required_terms_any=("dirty contact", "dirty contacts", "reprocessing", "PayRun output unsafe", "payroll-affecting changes"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_and_classification_lenses",
            label="Contacts / Employee Appointments comparison and classification lenses",
            query_terms=("comparison", "classification lens", "classification lenses", "appointment", "duplicate full appointments", "remediation"),
            required_terms_any=("comparison", "classification lens", "classification lenses", "appointment", "duplicate full appointments", "remediation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Contacts / Employee Appointments outstanding hardening",
            query_terms=("outstanding hardening", "GUID boundary", "schema contracts", "contact-level history", "WorkerAttention schemas", "classification lenses", "dirty-contact propagation"),
            required_terms_any=("outstanding hardening", "GUID boundary", "schema contracts", "contact-level history", "WorkerAttention schemas", "classification lenses", "dirty-contact propagation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PROCESS_PERIOD_PAYRUN_LIFECYCLE_PLAN = DomainRetrievalPlan(
    plan_id="PROCESS_PERIOD_PAYRUN_LIFECYCLE",
    domain="Process Periods / PayRun Lifecycle",
    trigger_phrases=(
        "how should process periods and payrun lifecycle work",
        "how should process periods / payrun lifecycle work",
        "what are process periods and payrun lifecycle",
        "how should processperiod work",
        "how should payrun lifecycle work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Process Periods / PayRun Lifecycle purpose and operator meaning",
            query_terms=("Process Periods / PayRun Lifecycle", "ProcessPeriod", "governed payroll-period context", "payment-event lifecycle evidence", "not payroll calculation truth", "not a generic date range"),
            required_terms_any=("Process Periods / PayRun Lifecycle", "ProcessPeriod", "governed payroll-period context", "payment-event lifecycle evidence", "not payroll calculation truth", "not a generic date range"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="process_period_and_group_context",
            label="Process Periods / PayRun Lifecycle ProcessPeriod and ProcessPeriodGroup context",
            query_terms=("ProcessPeriod", "Process Period", "ProcessPeriodGroup", "Process Period Group", "recurring calendar policy", "payment policy context"),
            required_terms_any=("ProcessPeriod", "Process Period", "ProcessPeriodGroup", "Process Period Group", "recurring calendar policy", "payment policy context"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="open_not_open_closed_lifecycle",
            label="Process Periods / PayRun Lifecycle open not-open closed lifecycle",
            query_terms=("open", "not-open", "not open", "closed", "closed dominates open", "period lifecycle"),
            required_terms_any=("open", "not-open", "not open", "closed", "closed dominates open", "period lifecycle"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="close_rolls_forward",
            label="Process Periods / PayRun Lifecycle close rolls forward",
            query_terms=("close rolls forward", "roll forward", "close period", "open next period", "create next period", "period close"),
            required_terms_any=("close rolls forward", "roll forward", "close period", "open next period", "create next period", "period close"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_date_and_calendar_policy",
            label="Process Periods / PayRun Lifecycle PaymentDate and calendar policy",
            query_terms=("PaymentDate", "payment date", "calendar policy", "tax/PAYG", "payment context", "governed derived", "not hardcoded"),
            required_terms_any=("PaymentDate", "payment date", "calendar policy", "tax/PAYG", "payment context", "governed derived", "not hardcoded"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_creation_and_admission",
            label="Process Periods / PayRun Lifecycle PayRun creation and admission",
            query_terms=("PayRun creation", "PayRun admission", "process-period context", "worker inclusion", "admission is not processing", "payment event"),
            required_terms_any=("PayRun creation", "PayRun admission", "process-period context", "worker inclusion", "admission is not processing", "payment event"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="run_type_and_run_purpose",
            label="Process Periods / PayRun Lifecycle RunType and RunPurpose",
            query_terms=("RunType", "RunPurpose", "separate", "run type", "run purpose", "payment/processing event"),
            required_terms_any=("RunType", "RunPurpose", "separate", "run type", "run purpose", "payment/processing event"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="regular_supplementary_retro_distinction",
            label="Process Periods / PayRun Lifecycle regular supplementary retro distinction",
            query_terms=("regular PayRun", "supplementary PayRun", "retro PayRun", "termination PayRun", "reversal PayRun", "adjustment PayRun", "different lifecycle concepts"),
            required_terms_any=("regular PayRun", "supplementary PayRun", "retro PayRun", "termination PayRun", "reversal PayRun", "adjustment PayRun", "different lifecycle concepts"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_contact_lifecycle",
            label="Process Periods / PayRun Lifecycle PayRunContact lifecycle",
            query_terms=("PayRunContact", "worker participation", "admission", "processing state", "operational state layer", "dirty PayRunContact"),
            required_terms_any=("PayRunContact", "worker participation", "admission", "processing state", "operational state layer", "dirty PayRunContact"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_output_and_finalisation",
            label="Process Periods / PayRun Lifecycle current-effective output and finalisation",
            query_terms=("current-effective output", "current-effective payroll output", "stale", "superseded", "current truth", "finalisation readiness"),
            required_terms_any=("current-effective output", "current-effective payroll output", "stale", "superseded", "current truth", "finalisation readiness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_execution_and_period_close",
            label="Process Periods / PayRun Lifecycle payment execution and period close",
            query_terms=("payment execution", "period close", "downstream governed outcome", "payment outcome", "not payroll calculation", "closed period"),
            required_terms_any=("payment execution", "period close", "downstream governed outcome", "payment outcome", "not payroll calculation", "closed period"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_admin_queue_and_movement_review_connection",
            label="Process Periods / PayRun Lifecycle Worker Story Admin Queue and Movement Review connection",
            query_terms=("Worker Story", "PayRun Admin Queue", "Admin Queue", "Movement Review", "worker participation", "readiness", "review implications"),
            required_terms_any=("Worker Story", "PayRun Admin Queue", "Admin Queue", "Movement Review", "worker participation", "readiness", "review implications"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Process Periods / PayRun Lifecycle outstanding hardening",
            query_terms=("outstanding hardening", "operation trackers", "lifecycle contracts", "supplementary/retro policies", "payment execution", "finalisation warning acknowledgement", "broader contract tests"),
            required_terms_any=("outstanding hardening", "operation trackers", "lifecycle contracts", "supplementary/retro policies", "payment execution", "finalisation warning acknowledgement", "broader contract tests"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

COSTING_GL_CONSEQUENCE_PLAN = DomainRetrievalPlan(
    plan_id="COSTING_GL_CONSEQUENCE",
    domain="Costing / GL Consequence Evidence",
    trigger_phrases=(
        "how should costing and gl consequence evidence work",
        "how should costing / gl consequence evidence work",
        "what is costing and gl consequence evidence",
        "what is costing / gl consequence evidence",
        "how should costing work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Costing / GL Consequence Evidence purpose and operator meaning",
            query_terms=("Costing / GL Consequence Evidence", "Costing", "GL consequence", "financial consequence evidence", "downstream financial consequence evidence", "not payroll calculation truth"),
            required_terms_any=("Costing / GL Consequence Evidence", "Costing", "GL consequence", "financial consequence evidence", "downstream financial consequence evidence", "not payroll calculation truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="downstream_not_payroll_calculation_truth",
            label="Costing / GL Consequence Evidence downstream not payroll calculation truth",
            query_terms=("downstream financial consequence", "not payroll calculation truth", "not payment execution", "Minerva does not post GL", "does not calculate costing"),
            required_terms_any=("downstream financial consequence", "not payroll calculation truth", "not payment execution", "Minerva does not post GL", "does not calculate costing"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalised_payroll_outcome_source",
            label="Costing / GL Consequence Evidence finalised payroll outcome source",
            query_terms=("finalised payroll outcome", "finalised payroll outcomes", "finalised gross-to-net", "payment outcome", "source outcome", "finalised truth"),
            required_terms_any=("finalised payroll outcome", "finalised payroll outcomes", "finalised gross-to-net", "payment outcome", "source outcome", "finalised truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_execution_and_remittance_connection",
            label="Costing / GL Consequence Evidence payment execution and remittance connection",
            query_terms=("payment execution", "remittance", "payment outcome", "downstream payment", "payment execution performance", "period close"),
            required_terms_any=("payment execution", "remittance", "payment outcome", "downstream payment", "payment execution performance", "period close"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="employer_liability_and_oncost_connection",
            label="Costing / GL Consequence Evidence employer liability and on-cost connection",
            query_terms=("employer liabilities", "employer liability", "on-costs", "on costs", "super", "payroll tax", "WorkCover", "WIC"),
            required_terms_any=("employer liabilities", "employer liability", "on-costs", "on costs", "super", "payroll tax", "WorkCover", "WIC"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deduction_obligation_and_writeoff_consequences",
            label="Costing / GL Consequence Evidence deduction obligation and write-off consequences",
            query_terms=("deductions", "obligations", "obligation write-off", "obligation writeoff", "forgiveness", "balance reduction", "material adjustment", "GL/provision/costing treatment"),
            required_terms_any=("deductions", "obligations", "obligation write-off", "obligation writeoff", "forgiveness", "balance reduction", "material adjustment", "GL/provision/costing treatment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="comparison_remediation_variance_connection",
            label="Costing / GL Consequence Evidence comparison remediation variance connection",
            query_terms=("Comparison / Remediation", "remediation variance", "variance line", "remediation top-up", "downstream tax", "super", "payroll tax", "WIC", "costing treatment"),
            required_terms_any=("Comparison / Remediation", "remediation variance", "variance line", "remediation top-up", "downstream tax", "super", "payroll tax", "WIC", "costing treatment"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_valuation_and_accrual_connection",
            label="Costing / GL Consequence Evidence leave valuation and accrual connection",
            query_terms=("leave valuation", "leave accrual", "leave valuation basis", "LeaveLedger", "accrual evidence", "costing flow"),
            required_terms_any=("leave valuation", "leave accrual", "leave valuation basis", "LeaveLedger", "accrual evidence", "costing flow"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="negative_net_pay_and_out_of_pay_consequences",
            label="Costing / GL Consequence Evidence negative net pay and out-of-pay consequences",
            query_terms=("negative net pay", "recoveries", "obligations", "write-offs", "out-of-pay", "out of pay", "financial consequences"),
            required_terms_any=("negative net pay", "recoveries", "obligations", "write-offs", "out-of-pay", "out of pay", "financial consequences"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="audit_story_and_financial_evidence",
            label="Costing / GL Consequence Evidence audit story and financial evidence",
            query_terms=("audit story", "financial evidence", "source outcome", "reason", "treatment", "amount", "ledger status", "costing status", "deferred accounting design status"),
            required_terms_any=("audit story", "financial evidence", "source outcome", "reason", "treatment", "amount", "ledger status", "costing status", "deferred accounting design status"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deferred_costing_slice_boundary",
            label="Costing / GL Consequence Evidence deferred costing slice boundary",
            query_terms=("deferred costing slice", "future costing slice", "later/final slice", "not completed costing engine", "status-honest", "deferred accounting"),
            required_terms_any=("deferred costing slice", "future costing slice", "later/final slice", "not completed costing engine", "status-honest", "deferred accounting"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Costing / GL Consequence Evidence outstanding hardening",
            query_terms=("outstanding hardening", "costing engine", "GL posting", "remediation downstream treatment", "negative net pay financial treatment", "obligation write-off", "contract tests"),
            required_terms_any=("outstanding hardening", "costing engine", "GL posting", "remediation downstream treatment", "negative net pay financial treatment", "obligation write-off", "contract tests"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

RATE_SOURCE_RATE_STORY_PLAN = DomainRetrievalPlan(
    plan_id="RATE_SOURCE_RATE_STORY",
    domain="RateSource / Rate Story",
    trigger_phrases=(
        "what is ratesource / rate story",
        "what is ratesource rate story",
        "what is rate source / rate story",
        "what is rate source rate story",
        "what is rate story",
        "what is ratesource",
        "how should rate story work",
        "how should ratesource work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="rate_story_purpose",
            label="RateSource / Rate Story purpose",
            query_terms=("RateSource / Rate Story", "Rate Story", "RateStory", "selected rate", "rate explanation"),
            required_terms_any=("RateSource / Rate Story", "Rate Story", "RateStory", "selected rate", "rate explanation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_source_selection",
            label="RateSource / Rate Story RateSource selection",
            query_terms=("RateSource", "Rate Source", "selected rate", "rate selection", "rate source selection"),
            required_terms_any=("RateSource", "Rate Source", "selected rate", "rate selection", "rate source selection"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_amount_evidence",
            label="RateSource / Rate Story rate amount evidence",
            query_terms=("rate amount", "amount came from", "rate evidence", "selected amount", "rate value"),
            required_terms_any=("rate amount", "amount came from", "rate evidence", "selected amount", "rate value"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="date_effective_rates",
            label="RateSource / Rate Story date-effective rates",
            query_terms=("date-effective rate", "date-effective rates", "effective date", "date effective rates", "RateSource"),
            required_terms_any=("date-effective rate", "date-effective rates", "effective date", "date effective rates", "RateSource"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="award_account_class_scope",
            label="RateSource / Rate Story award account class scope",
            query_terms=("award rate", "account rate", "class rate", "award scope", "account scope", "class scope", "AwardRateType", "RateType"),
            required_terms_any=("award rate", "account rate", "class rate", "award scope", "account scope", "class scope", "AwardRateType", "RateType"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="pay_guide_rate_evidence",
            label="RateSource / Rate Story pay guide rate evidence",
            query_terms=("pay guide rate evidence", "pay guide evidence", "RateSourceEvidenceIndex", "Rate Source Evidence Index", "source row"),
            required_terms_any=("pay guide rate evidence", "pay guide evidence", "RateSourceEvidenceIndex", "Rate Source Evidence Index", "source row"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_source_evidence_index",
            label="RateSource / Rate Story RateSourceEvidenceIndex",
            query_terms=("RateSourceEvidenceIndex", "Rate Source Evidence Index", "rate source evidence index", "why a rate", "rate evidence index"),
            required_terms_any=("RateSourceEvidenceIndex", "Rate Source Evidence Index", "rate source evidence index", "why a rate", "rate evidence index"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="rate_story_vs_decision_story",
            label="RateSource / Rate Story versus Decision Story",
            query_terms=("Rate Story", "Decision Story", "rate amount", "treatment selection", "entitlement", "not the same"),
            required_terms_any=("Rate Story", "Decision Story", "rate amount", "treatment selection", "entitlement", "not the same"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_relationship",
            label="RateSource / Rate Story Worker Story relationship",
            query_terms=("Rate Story", "Worker Story", "Worker Calculation Story", "worker evidence", "rate explanation"),
            required_terms_any=("Rate Story", "Worker Story", "Worker Calculation Story", "worker evidence", "rate explanation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_output_and_gross_to_net_relationship",
            label="RateSource / Rate Story payroll output and Gross-to-Net relationship",
            query_terms=("Rate Story", "payroll output", "gross-to-net", "Gross-to-Net", "calculated payroll outcome", "line proof"),
            required_terms_any=("Rate Story", "payroll output", "gross-to-net", "Gross-to-Net", "calculated payroll outcome", "line proof"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="RateSource / Rate Story outstanding hardening",
            query_terms=("RateSource", "Rate Story", "outstanding hardening", "RateSourceEvidenceIndex", "contract tests", "pay guide evidence"),
            required_terms_any=("RateSource", "Rate Story", "outstanding hardening", "RateSourceEvidenceIndex", "contract tests", "pay guide evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

DECISION_STORY_PLAN = DomainRetrievalPlan(
    plan_id="DECISION_STORY",
    domain="Decision Story",
    trigger_phrases=(
        "what is decision story",
        "what is decisionstory",
        "how should decision story work",
        "how does decision story explain",
        "what is decision evidence index",
        "what is decisionevidenceindex",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="decision_story_purpose",
            label="Decision Story purpose",
            query_terms=("Decision Story", "DecisionStory", "payroll decision", "why a treatment", "why a line exists"),
            required_terms_any=("Decision Story", "DecisionStory", "payroll decision", "why a treatment", "why a line exists"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="treatment_and_entitlement_selection",
            label="Decision Story treatment and entitlement selection",
            query_terms=("treatment selection", "entitlement decision", "why a treatment was selected", "why the line exists", "payroll decision"),
            required_terms_any=("treatment selection", "entitlement decision", "why a treatment was selected", "why the line exists", "payroll decision"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="decision_evidence_index",
            label="Decision Story DecisionEvidenceIndex",
            query_terms=("DecisionEvidenceIndex", "Decision Evidence Index", "decision evidence", "why a treatment", "why a line exists"),
            required_terms_any=("DecisionEvidenceIndex", "Decision Evidence Index", "decision evidence", "why a treatment", "why a line exists"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="award_rule_and_runtime_fact_evidence",
            label="Decision Story award rule and runtime fact evidence",
            query_terms=("award rule", "configured rules", "runtime facts", "source evidence", "rule outcome"),
            required_terms_any=("award rule", "configured rules", "runtime facts", "source evidence", "rule outcome"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="allowance_penalty_overtime_shift_evidence",
            label="Decision Story allowance penalty overtime shift evidence",
            query_terms=("allowance decision", "penalty decision", "overtime decision", "shift decision", "allowance", "penalty", "overtime", "shift"),
            required_terms_any=("allowance decision", "penalty decision", "overtime decision", "shift decision", "allowance", "penalty", "overtime", "shift"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="break_public_holiday_and_special_condition_evidence",
            label="Decision Story break public holiday and special condition evidence",
            query_terms=("break treatment", "missed break", "public holiday decision", "minimum engagement", "special condition"),
            required_terms_any=("break treatment", "missed break", "public holiday decision", "minimum engagement", "special condition"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="decision_story_vs_rate_story",
            label="Decision Story versus Rate Story",
            query_terms=("Decision Story", "Rate Story", "treatment or line exists", "rate amount", "not the same"),
            required_terms_any=("Decision Story", "Rate Story", "treatment or line exists", "rate amount", "not the same"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_relationship",
            label="Decision Story Worker Story relationship",
            query_terms=("Decision Story", "Worker Story", "payroll line explanation", "worker evidence", "DecisionEvidenceIndex"),
            required_terms_any=("Decision Story", "Worker Story", "payroll line explanation", "worker evidence", "DecisionEvidenceIndex"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_output_and_gross_to_net_relationship",
            label="Decision Story payroll output and Gross-to-Net relationship",
            query_terms=("Decision Story", "payroll output", "Gross-to-Net", "calculated payroll outcome", "line proof"),
            required_terms_any=("Decision Story", "payroll output", "Gross-to-Net", "calculated payroll outcome", "line proof"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Decision Story outstanding hardening",
            query_terms=("Decision Story", "DecisionEvidenceIndex", "outstanding hardening", "contract tests", "evidence limitation"),
            required_terms_any=("Decision Story", "DecisionEvidenceIndex", "outstanding hardening", "contract tests", "evidence limitation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

PAYROLL_OUTPUT_PLAN = DomainRetrievalPlan(
    plan_id="PAYROLL_OUTPUT",
    domain="Payroll Output",
    trigger_phrases=(
        "what is payroll output",
        "what is payrun output",
        "what is process period output",
        "what is run output",
        "how should payroll output work",
        "how should payrun output work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="payroll_output_purpose",
            label="Payroll Output purpose",
            query_terms=("Payroll Output", "PayRun Output", "calculated payroll output", "payroll result", "calculated payroll result"),
            required_terms_any=("Payroll Output", "PayRun Output", "calculated payroll output", "payroll result", "calculated payroll result"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="calculated_payroll_lines",
            label="Payroll Output calculated payroll lines",
            query_terms=("calculated payroll lines", "payroll line", "output line", "line-level payroll outcome", "CalcInterpreterLine"),
            required_terms_any=("calculated payroll lines", "payroll line", "output line", "line-level payroll outcome", "CalcInterpreterLine"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_output_truth",
            label="Payroll Output current-effective output truth",
            query_terms=("current-effective output", "current effective payroll output", "current-effective payroll output truth", "current truth", "superseded output"),
            required_terms_any=("current-effective output", "current effective payroll output", "current-effective payroll output truth", "current truth", "superseded output"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="run_output_vs_process_period_output",
            label="Payroll Output run output versus process-period output",
            query_terms=("Run Output", "Process Period Output", "PayRun Output", "run output", "process-period output"),
            required_terms_any=("Run Output", "Process Period Output", "PayRun Output", "run output", "process-period output"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_level_output",
            label="Payroll Output worker-level output",
            query_terms=("worker-level output", "worker output", "worker payroll output", "Worker Story", "worker evidence"),
            required_terms_any=("worker-level output", "worker output", "worker payroll output", "Worker Story", "worker evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payrun_totals_and_line_totals",
            label="Payroll Output PayRun totals and line totals",
            query_terms=("PayRun totals", "line totals", "payroll totals", "output totals", "CalcInterpreterRun"),
            required_terms_any=("PayRun totals", "line totals", "payroll totals", "output totals", "CalcInterpreterRun"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="decision_story_and_rate_story_relationship",
            label="Payroll Output Decision Story and Rate Story relationship",
            query_terms=("Decision Story", "Rate Story", "why line exists", "selected rate", "rate amount"),
            required_terms_any=("Decision Story", "Rate Story", "why line exists", "selected rate", "rate amount"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_to_net_relationship",
            label="Payroll Output Gross-to-Net relationship",
            query_terms=("Gross-to-Net", "gross to net", "gross earnings", "net pay", "payroll outcome"),
            required_terms_any=("Gross-to-Net", "gross to net", "gross earnings", "net pay", "payroll outcome"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_relationship",
            label="Payroll Output Payroll Bases & Totals relationship",
            query_terms=("Payroll Bases & Totals", "Payroll Bases", "basis evidence", "bucket evidence", "basis totals"),
            required_terms_any=("Payroll Bases & Totals", "Payroll Bases", "basis evidence", "bucket evidence", "basis totals"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalisation_and_payment_execution_relationship",
            label="Payroll Output finalisation and payment execution relationship",
            query_terms=("Finalisation Readiness", "Payment Execution", "finalised outcome truth", "payment execution boundary", "payment file"),
            required_terms_any=("Finalisation Readiness", "Payment Execution", "finalised outcome truth", "payment execution boundary", "payment file"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Payroll Output outstanding hardening",
            query_terms=("Payroll Output", "outstanding hardening", "current-effective output", "contract tests", "status honesty"),
            required_terms_any=("Payroll Output", "outstanding hardening", "current-effective output", "contract tests", "status honesty"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

CONTACT_PAYROLL_HISTORY_PLAN = DomainRetrievalPlan(
    plan_id="CONTACT_PAYROLL_HISTORY",
    domain="Contact Payroll History",
    trigger_phrases=(
        "what is contact payroll history",
        "what is payroll history",
        "what is worker payroll history",
        "how should contact payroll history work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="contact_payroll_history_purpose",
            label="Contact Payroll History purpose",
            query_terms=("Contact Payroll History", "payroll history", "worker payroll history", "contact-level payroll history", "payroll outcome history"),
            required_terms_any=("Contact Payroll History", "payroll history", "worker payroll history", "contact-level payroll history", "payroll outcome history"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="contact_identity_and_payrun_participation",
            label="Contact Payroll History contact identity and PayRun participation",
            query_terms=("Contact", "worker", "contact identity", "PayRun participation", "PayRunContact", "worker history"),
            required_terms_any=("Contact", "worker", "contact identity", "PayRun participation", "PayRunContact", "worker history"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_and_historical_payroll_output",
            label="Contact Payroll History current and historical payroll output",
            query_terms=("current payroll output", "historical payroll output", "current-effective payroll output", "payroll output history", "historical evidence"),
            required_terms_any=("current payroll output", "historical payroll output", "current-effective payroll output", "payroll output history", "historical evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_to_net_history",
            label="Contact Payroll History Gross-to-Net history",
            query_terms=("Gross-to-Net history", "gross to net history", "gross earnings history", "net pay history", "payroll outcome history"),
            required_terms_any=("Gross-to-Net history", "gross to net history", "gross earnings history", "net pay history", "payroll outcome history"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deductions_obligations_and_negative_net_pay",
            label="Contact Payroll History deductions obligations and negative net pay",
            query_terms=("contact deductions", "contact obligations", "deductions", "obligations", "negative net pay", "out-of-pay"),
            required_terms_any=("contact deductions", "contact obligations", "deductions", "obligations", "negative net pay", "out-of-pay"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="tax_and_payment_readiness_history",
            label="Contact Payroll History tax and payment readiness history",
            query_terms=("contact tax", "contact payment", "tax history", "payment readiness history", "payment allocation", "PAYG"),
            required_terms_any=("contact tax", "contact payment", "tax history", "payment readiness history", "payment allocation", "PAYG"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_and_accrual_history",
            label="Contact Payroll History leave and accrual history",
            query_terms=("leave history", "accrual history", "leave/accrual evidence", "leave accrual", "leave evidence"),
            required_terms_any=("leave history", "accrual history", "leave/accrual evidence", "leave accrual", "leave evidence"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_relationship",
            label="Contact Payroll History Worker Story relationship",
            query_terms=("Worker Story", "worker evidence", "worker-level story", "payroll explanation", "contact history"),
            required_terms_any=("Worker Story", "worker evidence", "worker-level story", "payroll explanation", "contact history"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="movement_review_and_admin_queue_relationship",
            label="Contact Payroll History Movement Review and Admin Queue relationship",
            query_terms=("Movement Review", "Admin Queue", "PayRun Admin Queue", "review context", "action workbench", "reasonableness"),
            required_terms_any=("Movement Review", "Admin Queue", "PayRun Admin Queue", "review context", "action workbench", "reasonableness"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="retro_replay_and_correction_relationship",
            label="Contact Payroll History retro replay and correction relationship",
            query_terms=("retro history", "correction history", "retro/replay/correction context", "retro replay", "correction implications"),
            required_terms_any=("retro history", "correction history", "retro/replay/correction context", "retro replay", "correction implications"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Contact Payroll History outstanding hardening",
            query_terms=("Contact Payroll History", "outstanding hardening", "status honesty", "historical payroll records", "finalised truth"),
            required_terms_any=("Contact Payroll History", "outstanding hardening", "status honesty", "historical payroll records", "finalised truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

GROSS_TO_NET_PLAN = DomainRetrievalPlan(
    plan_id="GROSS_TO_NET",
    domain="Gross-to-Net",
    trigger_phrases=(
        "what is gross-to-net",
        "what is gross to net",
        "what is grosstonet",
        "how should gross-to-net work",
        "how should gross to net work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="gross_to_net_purpose",
            label="Gross-to-Net purpose and operator meaning",
            query_terms=("Gross-to-Net", "Gross to Net", "GrossToNet", "payroll outcome calculation", "payroll outcome explanation surface"),
            required_terms_any=("Gross-to-Net", "Gross to Net", "GrossToNet", "payroll outcome calculation", "payroll outcome explanation surface"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="gross_earnings_and_payroll_output",
            label="Gross-to-Net gross earnings and payroll output",
            query_terms=("gross earnings", "gross pay", "payroll output", "earnings lines", "payroll outcome"),
            required_terms_any=("gross earnings", "gross pay", "payroll output", "earnings lines", "payroll outcome"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="taxable_basis_and_payg",
            label="Gross-to-Net taxable basis and PAYG",
            query_terms=("taxable basis", "taxable earnings", "PAYG", "withholding", "tax withholding", "final withholding"),
            required_terms_any=("taxable basis", "taxable earnings", "PAYG", "withholding", "tax withholding", "final withholding"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="deductions_and_obligations",
            label="Gross-to-Net deductions and obligations",
            query_terms=("deductions", "obligations", "deduction applications", "obligation recovery", "post-tax deductions"),
            required_terms_any=("deductions", "obligations", "deduction applications", "obligation recovery", "post-tax deductions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="negative_net_pay",
            label="Gross-to-Net negative net pay",
            query_terms=("negative net pay", "governed treatment", "carry-forward", "recovery", "write-off", "not silently converted to zero"),
            required_terms_any=("negative net pay", "governed treatment", "carry-forward", "recovery", "write-off", "not silently converted to zero"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="net_pay_and_payment_allocation",
            label="Gross-to-Net net pay and payment allocation",
            query_terms=("net pay", "payment allocation", "payment execution readiness", "payment destination", "worker net pay"),
            required_terms_any=("net pay", "payment allocation", "payment execution readiness", "payment destination", "worker net pay"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_relationship",
            label="Gross-to-Net Worker Story relationship",
            query_terms=("Gross-to-Net", "Worker Story", "gross-to-net evidence", "worker evidence", "payroll outcome explanation"),
            required_terms_any=("Gross-to-Net", "Worker Story", "gross-to-net evidence", "worker evidence", "payroll outcome explanation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalisation_and_payment_execution",
            label="Gross-to-Net finalisation and payment execution",
            query_terms=("finalisation", "finalised outcome truth", "payment execution", "payment execution readiness", "not payment execution"),
            required_terms_any=("finalisation", "finalised outcome truth", "payment execution", "payment execution readiness", "not payment execution"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_output_truth",
            label="Gross-to-Net current-effective output truth",
            query_terms=("current-effective payroll output", "current effective payroll output", "current truth", "stale", "superseded"),
            required_terms_any=("current-effective payroll output", "current effective payroll output", "current truth", "stale", "superseded"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Gross-to-Net outstanding hardening",
            query_terms=("Gross-to-Net", "outstanding hardening", "negative net pay", "taxable basis", "payment allocation", "contract tests"),
            required_terms_any=("Gross-to-Net", "outstanding hardening", "negative net pay", "taxable basis", "payment allocation", "contract tests"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

FINALISATION_READINESS_PLAN = DomainRetrievalPlan(
    plan_id="FINALISATION_READINESS",
    domain="Finalisation Readiness",
    trigger_phrases=(
        "how should finalisation readiness work",
        "how should finalization readiness work",
        "what is finalisation readiness",
        "what is finalization readiness",
        "how does finalisation readiness work",
        "how does finalization readiness work",
    ),
    evidence_groups=(
        EvidenceGroup(
            group_id="purpose_and_operator_meaning",
            label="Finalisation Readiness purpose and operator meaning",
            query_terms=("Finalisation Readiness", "governed readiness gate", "assurance gate", "not payroll calculation truth", "green means done"),
            required_terms_any=("Finalisation Readiness", "governed readiness gate", "assurance gate", "not payroll calculation truth", "green means done"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="blockers_warnings_and_green_state",
            label="Finalisation Readiness blockers warnings and green state",
            query_terms=("blockers", "warnings", "red blockers", "amber warnings", "green", "ready", "cleared"),
            required_terms_any=("blockers", "warnings", "red blockers", "amber warnings", "green", "ready", "cleared"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="current_effective_payroll_output",
            label="Finalisation Readiness current-effective payroll output",
            query_terms=("current-effective payroll output", "stale", "superseded", "current truth", "finalised as current truth"),
            required_terms_any=("current-effective payroll output", "stale", "superseded", "current truth", "finalised as current truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_attention_and_admin_queue",
            label="Finalisation Readiness Worker Attention and Admin Queue",
            query_terms=("Worker Attention", "Admin Queue", "worker-level blockers", "worker-level warnings", "ready actions"),
            required_terms_any=("Worker Attention", "Admin Queue", "worker-level blockers", "worker-level warnings", "ready actions"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payroll_bases_readiness",
            label="Finalisation Readiness Payroll Bases readiness",
            query_terms=("Payroll Bases readiness", "Payroll Bases & Totals", "unresolved basis evidence", "stale basis evidence", "finalisation"),
            required_terms_any=("Payroll Bases readiness", "Payroll Bases & Totals", "unresolved basis evidence", "stale basis evidence", "finalisation"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="leave_readiness",
            label="Finalisation Readiness leave readiness",
            query_terms=("leave readiness", "missing leave output", "leave valuation basis", "LeaveLedger", "TAKEN leave"),
            required_terms_any=("leave readiness", "missing leave output", "leave valuation basis", "LeaveLedger", "TAKEN leave"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="tax_deduction_and_payment_readiness",
            label="Finalisation Readiness tax deduction and payment readiness",
            query_terms=("tax readiness", "deduction readiness", "negative net pay", "payment destination readiness", "gross-to-net"),
            required_terms_any=("tax readiness", "deduction readiness", "negative net pay", "payment destination readiness", "gross-to-net"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="payment_execution_and_bank_readiness",
            label="Finalisation Readiness payment execution and bank readiness",
            query_terms=("payment execution readiness", "payment readiness", "bank readiness", "gross-to-net readiness", "payment destination"),
            required_terms_any=("payment execution readiness", "payment readiness", "bank readiness", "gross-to-net readiness", "payment destination"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="finalised_outcome_truth",
            label="Finalisation Readiness finalised outcome truth",
            query_terms=("finalised outcome truth", "finalised outcome", "finalised totals", "durable payment outcome memory", "finalised payroll truth"),
            required_terms_any=("finalised outcome truth", "finalised outcome", "finalised totals", "durable payment outcome memory", "finalised payroll truth"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="warning_acknowledgement_and_audit",
            label="Finalisation Readiness warning acknowledgement and audit",
            query_terms=("warning acknowledgement", "warning acknowledgment", "finalisation audit", "reviewed", "accepted", "unresolved"),
            required_terms_any=("warning acknowledgement", "warning acknowledgment", "finalisation audit", "reviewed", "accepted", "unresolved"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="worker_story_and_review_surfaces",
            label="Finalisation Readiness Worker Story and review surfaces",
            query_terms=("Worker Story", "review surfaces", "readiness evidence", "worker-specific issues", "Movement Review", "Admin Queue"),
            required_terms_any=("Worker Story", "review surfaces", "readiness evidence", "worker-specific issues", "Movement Review", "Admin Queue"),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
        EvidenceGroup(
            group_id="outstanding_hardening",
            label="Finalisation Readiness outstanding hardening",
            query_terms=(
                "outstanding hardening",
                "warning acknowledgement",
                "WorkerAttention schemas",
                "finalisation policy",
                "server-owned operation",
                "readiness evidence",
                "payment execution readiness",
                "contract tests",
            ),
            required_terms_any=(
                "outstanding hardening",
                "warning acknowledgement",
                "WorkerAttention schemas",
                "finalisation policy",
                "server-owned operation",
                "readiness evidence",
                "payment execution readiness",
                "contract tests",
            ),
            preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
        ),
    ),
)

DOMAIN_RETRIEVAL_PLANS = (
    ANNUAL_LEAVE_MANAGEMENT_PLAN,
    WORKER_STORY_PLAN,
    PAYROLL_BASES_AND_TOTALS_PLAN,
    WORKER_ATTENTION_ISSUE_RESOLUTION_PLAN,
    PAYRUN_ADMIN_QUEUE_PLAN,
    MOVEMENT_REVIEW_PLAN,
    COMPARISON_REMEDIATION_PLAN,
    TAX_PAYG_PLAN,
    DEDUCTIONS_OBLIGATIONS_PLAN,
    RETRO_REPLAY_PLAN,
    PAYMENT_EXECUTION_REMITTANCE_PLAN,
    LEAVE_ACCRUAL_PROCESSING_PLAN,
    LEAVE_SOURCE_MODEL_PLAN,
    LEAVE_REQUESTS_WORKFLOW_PLAN,
    PUBLIC_HOLIDAYS_PLAN,
    ROSTERS_PATTERNS_SCHEDULING_PLAN,
    AWARD_POSITIONS_CLASSIFICATIONS_PLAN,
    PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN,
    ONCOSTS_EMPLOYER_LIABILITIES_PLAN,
    AWARD_BUILD_EVIDENCE_PLAN,
    IMPORTS_ACTUALS_PLAN,
    OBJECTTIME_SOURCE_TRUTH_PLAN,
    CONTACTS_EMPLOYEE_APPOINTMENTS_PLAN,
    PROCESS_PERIOD_PAYRUN_LIFECYCLE_PLAN,
    COSTING_GL_CONSEQUENCE_PLAN,
    RATE_SOURCE_RATE_STORY_PLAN,
    DECISION_STORY_PLAN,
    PAYROLL_OUTPUT_PLAN,
    CONTACT_PAYROLL_HISTORY_PLAN,
    GROSS_TO_NET_PLAN,
    FINALISATION_READINESS_PLAN,
)


def _normalize_question(text: str) -> str:
    return " ".join(text.lower().replace("-", " ").split()).rstrip("?")


def detect_domain_retrieval_plan(question: str) -> DomainRetrievalPlan | None:
    normalized = _normalize_question(question)
    payroll_output_framed = (
        normalized.startswith("how does payroll output")
        or normalized.startswith("how should payroll output")
        or normalized.startswith("what does current effective payroll output")
        or normalized.startswith("what is the difference between run output and process period output")
        or "payroll output relate" in normalized
        or "payroll output explain" in normalized
    )
    contact_payroll_history_framed = (
        "contact payroll history" in normalized
        or "contact level payroll history" in normalized
        or "worker payroll history" in normalized
        or "payroll outcome history" in normalized
        or ("payroll history" in normalized and ("contact" in normalized or "worker" in normalized or "platform" in normalized))
        or ("historical payroll output" in normalized and ("contact" in normalized or "worker" in normalized or "history" in normalized))
        or ("payrun participation" in normalized and ("history" in normalized or "contact" in normalized or "worker" in normalized))
        or ("contact history" in normalized and "payroll" in normalized)
    )
    if (
        "worker attention / issue resolution" in normalized
        or "worker attention issue resolution" in normalized
        or "issue resolution" in normalized and "worker" in normalized
        or "worker attention centre" in normalized
        or "workerattention" in normalized and ("issue" in normalized or "resolution" in normalized)
        or "worker issue" in normalized and ("resolution" in normalized or "surface" in normalized or "platform" in normalized)
        or "worker attention" in normalized and (
            "model worker issue" in normalized
            or "worker issues" in normalized
            or "blockers" in normalized
            or "warnings" in normalized
            or "fix links" in normalized
            or "fix link" in normalized
            or "fix an issue" in normalized
            or "guide users" in normalized
            or "dirty contact state" in normalized
            or "payment allocation" in normalized
            or "negative net pay" in normalized
            or ("admin queue" in normalized and "worker story" in normalized and "relate" in normalized)
        )
    ) and not (
        "payrun admin queue" in normalized
        or "contacts / employee appointments" in normalized
        or "contacts and employee appointments" in normalized
        or "employee appointment" in normalized
        or "employeeappointment" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return WORKER_ATTENTION_ISSUE_RESOLUTION_PLAN
    costing_focused_anchor = (
        "finalised payroll outcome" in normalized
        or "finalized payroll outcome" in normalized
        or "payment execution" in normalized
        or "remittance" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
        or "on costs" in normalized
        or "oncosts" in normalized
        or "deduction obligations" in normalized
        or "deduction obligation" in normalized
        or "write offs" in normalized
        or "write off" in normalized
        or "comparison / remediation" in normalized
        or "comparison remediation" in normalized
        or "remediation variance" in normalized
        or "variance line" in normalized
        or "leave valuation" in normalized
        or "leave accrual" in normalized
        or "negative net pay" in normalized
        or "out of pay" in normalized
        or "audit story" in normalized
        or "financial evidence" in normalized
        or "deferred/final slice" in normalized
        or "deferred final slice" in normalized
        or "payroll processing blocker" in normalized
        or "final slice" in normalized
    )
    if (
        "costing / gl consequence" in normalized
        or "costing and gl consequence" in normalized
        or "costing gl consequence" in normalized
        or ("costing" in normalized and ("gl" in normalized or "financial consequence" in normalized or "financial consequences" in normalized))
        or ("costing" in normalized and costing_focused_anchor)
        or ("gl consequence" in normalized and ("costing" in normalized or "financial" in normalized))
        or ("gl consequences" in normalized and ("costing" in normalized or "financial" in normalized))
        or ("financial consequence" in normalized and ("costing" in normalized or "gl" in normalized))
        or ("financial consequences" in normalized and ("costing" in normalized or "gl" in normalized))
        or ("financial consequence" in normalized and costing_focused_anchor)
        or ("financial consequences" in normalized and costing_focused_anchor)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "matter" in normalized
        or "work" in normalized
    ):
        return COSTING_GL_CONSEQUENCE_PLAN
    award_positions_classifications_framed = (
        "award positions / classifications" in normalized
        or "award positions and classifications" in normalized
        or "award positions classifications" in normalized
        or "award position classification" in normalized
        or "awardposition" in normalized
        or "award position" in normalized
        or "awardpositionclass" in normalized
        or "award position class" in normalized
        or "positionclass" in normalized
        or "position class" in normalized
        or ("classification" in normalized and ("award position" in normalized or "award class" in normalized or "employee appointment" in normalized or "worksiteposition" in normalized or "worksite position" in normalized))
        or ("classification" in normalized and "pay guide" in normalized and ("payroll interpretation" in normalized or "class evidence" in normalized))
        or ("classification" in normalized and ("ratesource" in normalized or "rate story" in normalized or "payroll output" in normalized))
        or ("classifications" in normalized and ("ratesource" in normalized or "rate story" in normalized or "payroll output" in normalized))
        or ("classification" in normalized and "decision story" in normalized and ("relate" in normalized or "support" in normalized))
        or ("classifications" in normalized and "decision story" in normalized and ("relate" in normalized or "support" in normalized))
        or ("classification evidence" in normalized and ("missing" in normalized or "unresolved" in normalized or "readiness" in normalized))
        or ("classifications" in normalized and ("award position" in normalized or "award class" in normalized or "employee appointment" in normalized or "worksiteposition" in normalized or "worksite position" in normalized))
        or ("classifications" in normalized and ("comparison" in normalized or "remediation" in normalized))
        or ("class" in normalized and ("award position" in normalized or "worksite position" in normalized or "employee appointment" in normalized))
        or ("classification lenses" in normalized and ("comparison remediation" in normalized or "comparison / remediation" in normalized))
        or ("classification lens" in normalized and ("comparison remediation" in normalized or "comparison / remediation" in normalized))
    )
    if award_positions_classifications_framed and not (
        normalized.startswith("how should award build")
        or normalized.startswith("how should award evidence")
        or normalized.startswith("what is award build")
        or normalized.startswith("what is award evidence")
        or ("award build" in normalized and "classification" not in normalized and "class" not in normalized and "position" not in normalized)
        or ("award evidence" in normalized and "classification" not in normalized and "class" not in normalized and "position" not in normalized)
        or normalized.startswith("how should contacts")
        or normalized.startswith("what are contacts")
        or normalized.startswith("how should employee appointments")
        or normalized.startswith("how do rosters")
        or normalized.startswith("how does objecttime")
        or normalized.startswith("what is objecttime")
        or normalized.startswith("how does ratesource / rate story")
        or normalized.startswith("how does rate source / rate story")
        or normalized.startswith("how does decision story")
        or normalized.startswith("what is decision story")
        or normalized.startswith("what is payroll output")
        or normalized.startswith("how does comparison / remediation")
        or normalized.startswith("what is worker story")
        or normalized.startswith("what is finalisation readiness")
        or normalized.startswith("how does worker attention")
        or normalized.startswith("how should imports / actuals")
        or ("depend on employeeappointment" in normalized and "awardpositionclass" not in normalized and "award position class" not in normalized)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return AWARD_POSITIONS_CLASSIFICATIONS_PLAN
    payroll_tax_workcover_wic_liability_detail_framed = (
        "payroll tax / workcover / wic liability detail" in normalized
        or "payroll tax workcover wic liability detail" in normalized
        or "payroll tax workcover wic liabilities" in normalized
        or "payroll tax, workcover and wic liabilities" in normalized
        or "payroll tax workcover and wic liabilities" in normalized
        or "payrolltax" in normalized
        or "payroll tax" in normalized and ("workcover" in normalized or "wic" in normalized or "liability" in normalized)
        or "workcover" in normalized and ("wic" in normalized or "liability" in normalized or "payroll tax" in normalized or "ratesource" in normalized)
        or "work cover" in normalized and ("wic" in normalized or "liability" in normalized or "payroll tax" in normalized or "rate source" in normalized)
        or "wic" in normalized and ("workcover" in normalized or "work cover" in normalized or "payroll tax" in normalized or "liability" in normalized or "rate" in normalized)
        or "workers insurance" in normalized and ("liability" in normalized or "workcover" in normalized or "payroll tax" in normalized)
        or "workers compensation" in normalized and ("liability" in normalized or "workcover" in normalized or "payroll tax" in normalized)
        or "liability wages" in normalized and ("payroll tax" in normalized or "workcover" in normalized or "wic" in normalized)
        or "taxable wages" in normalized and ("payroll tax" in normalized or "workcover" in normalized or "wic" in normalized)
        or "objecttime location" in normalized and ("payroll tax" in normalized or "workcover" in normalized or "wic" in normalized or "liability" in normalized)
        or "worksite.stateid" in normalized and ("payroll tax" in normalized or "workcover" in normalized or "wic" in normalized or "liability" in normalized)
        or "worksite state" in normalized and ("payroll tax" in normalized or "workcover" in normalized or "wic" in normalized or "liability" in normalized)
        or "state or worksite context applies to employer liabilities" in normalized
        or "worksite context applies to employer liabilities" in normalized
        or "liability ratesource" in normalized
        or "liability rate source" in normalized
        or "date effective liability rate" in normalized
        or "date effective liability rates" in normalized
    )
    if payroll_tax_workcover_wic_liability_detail_framed and not (
        normalized.startswith("what are on costs")
        or normalized.startswith("what are oncosts")
        or normalized.startswith("how should on costs")
        or normalized.startswith("how should oncosts")
        or normalized.startswith("what are employer liabilities")
        or normalized.startswith("how should employer liability work")
        or normalized.startswith("how should employer liabilities work")
        or "superannuation" in normalized
        or "super" in normalized
        or "super oncost" in normalized
        or "super on cost" in normalized
        or normalized.startswith("how should tax / payg")
        or normalized.startswith("how should tax payg")
        or normalized.startswith("what is tax / payg")
        or normalized.startswith("what is tax payg")
        or ("payg" in normalized and "payroll tax" not in normalized and "payrolltax" not in normalized)
        or ("withholding" in normalized and "payroll tax" not in normalized and "payrolltax" not in normalized)
        or (normalized.startswith("how do payroll bases") and "payroll tax" not in normalized and "workcover" not in normalized and "wic" not in normalized)
        or (normalized.startswith("what is payroll bases") and "payroll tax" not in normalized and "workcover" not in normalized and "wic" not in normalized)
        or normalized.startswith("how does payment execution")
        or normalized.startswith("what is payment execution")
        or normalized.startswith("what is gross to net")
        or normalized.startswith("how does gross to net")
        or normalized.startswith("what is payroll output")
        or normalized.startswith("what is worker story")
        or normalized.startswith("what is finalisation readiness")
        or normalized.startswith("how are public holidays")
        or normalized.startswith("how do public holidays")
        or (normalized.startswith("how does objecttime") and "payroll tax" not in normalized and "workcover" not in normalized and "wic" not in normalized and "liability" not in normalized)
        or (normalized.startswith("what is objecttime") and "payroll tax" not in normalized and "workcover" not in normalized and "wic" not in normalized and "liability" not in normalized)
        or normalized.startswith("how should contacts")
        or normalized.startswith("how should employee appointments")
        or normalized.startswith("how does ratesource / rate story")
        or normalized.startswith("how does rate source / rate story")
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_PLAN
    if (
        "ratesource / rate story" in normalized
        or "ratesource rate story" in normalized
        or "rate source / rate story" in normalized
        or "rate source rate story" in normalized
        or ("rate story" in normalized and ("ratesource" in normalized or "rate source" in normalized))
        or ("rate story" in normalized and ("selected rate" in normalized or "rate amount" in normalized or "platform" in normalized))
        or ("rate story" in normalized and "pay guide" in normalized)
        or ("rate story" in normalized and ("date effective" in normalized or "scoped rates" in normalized or "effective date" in normalized))
        or ("rate story" in normalized and ("worker story" in normalized or "gross to net" in normalized or "payroll output" in normalized))
        or ("ratesource" in normalized and ("rate story" in normalized or "selected rate" in normalized or "rate amount" in normalized or "evidence layer" in normalized))
        or ("rate source" in normalized and ("rate story" in normalized or "selected rate" in normalized or "rate amount" in normalized or "evidence layer" in normalized))
    ) and not (
        "tax / payg" in normalized
        or "tax payg" in normalized
        or "on costs" in normalized
        or "oncosts" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
        or "award build" in normalized
        or "award evidence" in normalized
        or "payroll bases" in normalized
        or ("gross to net" in normalized and "rate story" not in normalized)
        or normalized.startswith("what is worker story")
        or "worker story" in normalized and "rate story" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return RATE_SOURCE_RATE_STORY_PLAN
    roster_pattern_scheduling_framed = (
        "rosters / patterns / scheduling" in normalized
        or "rosters patterns scheduling" in normalized
        or "rosters, patterns and scheduling" in normalized
        or "rosters patterns and scheduling" in normalized
        or "roster pattern scheduling" in normalized
        or "employeeappointmentpattern" in normalized
        or "employee appointment pattern" in normalized
        or "patternday" in normalized
        or "pattern day" in normalized
        or ("roster" in normalized and ("pattern" in normalized or "schedule" in normalized or "scheduling" in normalized or "ordinary hours" in normalized or "worksite" in normalized or "worker story" in normalized or "public holiday" in normalized or "readiness" in normalized))
        or ("rosters" in normalized and ("pattern" in normalized or "schedule" in normalized or "scheduling" in normalized or "ordinary hours" in normalized or "worksite" in normalized or "worker story" in normalized or "public holiday" in normalized or "readiness" in normalized))
        or ("pattern" in normalized and ("schedule" in normalized or "scheduling" in normalized or "ordinary hours" in normalized or "employee appointment" in normalized or "worksite" in normalized or "worker story" in normalized))
        or ("patterns" in normalized and ("schedule" in normalized or "scheduling" in normalized or "ordinary hours" in normalized or "employee appointment" in normalized or "worksite" in normalized or "worker story" in normalized))
        or ("work schedule" in normalized and ("roster" in normalized or "pattern" in normalized or "ordinary hours" in normalized or "employee appointment" in normalized))
        or ("scheduling" in normalized and ("roster" in normalized or "pattern" in normalized or "ordinary hours" in normalized or "expected time" in normalized or "expected work" in normalized))
        or ("scheduling context" in normalized and ("objecttime" in normalized or "actual worked time" in normalized or "source truth" in normalized))
    )
    if roster_pattern_scheduling_framed and not (
        normalized.startswith("what is objecttime")
        or normalized.startswith("how does objecttime")
        or normalized.startswith("what is source truth")
        or normalized.startswith("how does source truth")
        or normalized.startswith("how should contacts")
        or normalized.startswith("what are contacts")
        or normalized.startswith("how should employee appointments")
        or normalized.startswith("how are public holidays")
        or normalized.startswith("how do public holidays")
        or normalized.startswith("what is finalisation readiness")
        or normalized.startswith("how does finalisation readiness")
        or normalized.startswith("what is worker story")
        or normalized.startswith("how should worker story")
        or normalized.startswith("how does worker attention")
        or normalized.startswith("what is payroll output")
        or normalized.startswith("how should payroll output")
        or normalized.startswith("how does decision story")
        or normalized.startswith("what is decision story")
        or normalized.startswith("how does process periods")
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return ROSTERS_PATTERNS_SCHEDULING_PLAN
    if (
        "public holidays" in normalized
        or "public holiday" in normalized
        or "publicholiday" in normalized
        or "publicholidaygroup" in normalized
        or "public holiday group" in normalized
        or "deductsonpublicholiday" in normalized
        or "deducts on public holiday" in normalized
    ) and not (
        normalized.startswith("how does decision story")
        or normalized.startswith("what is decision story")
        or normalized.startswith("what is decisionstory")
        or normalized.startswith("what is the difference between decision story")
        or normalized.startswith("what is decisionevidenceindex")
        or normalized.startswith("what is decision evidence index")
    ) and not (
        ("leave request" in normalized or "leave workflow" in normalized or "leaveledger" in normalized or "leave ledger" in normalized)
        and ("approval" in normalized or "preview" in normalized or "shortfall" in normalized or "posting" in normalized)
        and "public holiday" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "handled" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return PUBLIC_HOLIDAYS_PLAN
    if (
        "what is decision story" in normalized
        or "what is decisionstory" in normalized
        or ("decision story" in normalized and ("platform" in normalized or "evidence layer" in normalized))
        or ("decisionstory" in normalized and ("platform" in normalized or "evidence layer" in normalized))
        or ("decision story" in normalized and ("treatment" in normalized or "entitlement" in normalized or "line exists" in normalized or "payroll decision" in normalized))
        or ("decisionstory" in normalized and ("treatment" in normalized or "entitlement" in normalized or "line exists" in normalized or "payroll decision" in normalized))
        or ("decision story" in normalized and "rate story" in normalized and ("treatment" in normalized or "entitlement" in normalized or "decision evidence" in normalized))
        or ("decision story" in normalized and ("worker story" in normalized or "gross to net" in normalized or "payroll output" in normalized))
        or ("decisionevidenceindex" in normalized and ("decision story" in normalized or "why a treatment" in normalized or "why a line" in normalized))
        or ("decision evidence index" in normalized and ("decision story" in normalized or "why a treatment" in normalized or "why a line" in normalized))
        or ("decisionevidenceindex" in normalized and ("what" in normalized or "used for" in normalized or "explain" in normalized))
        or ("decision evidence index" in normalized and ("what" in normalized or "used for" in normalized or "explain" in normalized))
        or "treatment selection" in normalized
        or "entitlement decision" in normalized
        or "why the line exists" in normalized
        or "why a treatment was selected" in normalized
        or "payroll decision" in normalized and ("why" in normalized or "explain" in normalized)
        or ("allowance decision" in normalized or "penalty decision" in normalized or "overtime decision" in normalized or "shift decision" in normalized)
        or ("public holiday decision" in normalized or "public holidays" in normalized or "break treatment" in normalized or "breaks" in normalized or "missed break" in normalized or "minimum engagement" in normalized)
    ) and not (
        "ratesource / rate story" in normalized
        or "rate source / rate story" in normalized
        or "ratesource rate story" in normalized
        or "rate source rate story" in normalized
        or ("rate story" in normalized and ("selected rate" in normalized or "rate amount" in normalized or "ratesource" in normalized or "rate source" in normalized))
        or normalized.startswith("what is worker story")
        or ("worker story" in normalized and "decision story" not in normalized)
        or "award build" in normalized
        or "award evidence" in normalized
        or "pay guide" in normalized and "award" in normalized
        or ("decisionevidenceindex" in normalized and "why does it matter" in normalized)
        or ("decision evidence index" in normalized and "why does it matter" in normalized)
        or "gross to net" in normalized and "decision story" not in normalized
        or "gross-to-net" in normalized and "decision story" not in normalized
        or "net pay" in normalized and "decision story" not in normalized
        or "payroll bases" in normalized
        or "payroll bases & totals" in normalized
        or ("leave accrual" in normalized or "leave processing" in normalized or "leave calculation" in normalized)
        or "finalisation readiness" in normalized
        or "finalization readiness" in normalized
        or ("readiness" in normalized and ("finalisation" in normalized or "finalization" in normalized))
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return DECISION_STORY_PLAN
    if (
        payroll_output_framed
        or "what is payroll output" in normalized
        or "what is payrun output" in normalized
        or "what is process period output" in normalized
        or "what is run output" in normalized
        or ("payroll output" in normalized and ("platform" in normalized or "evidence surface" in normalized or "calculated" in normalized))
        or ("payrun output" in normalized and ("platform" in normalized or "evidence" in normalized or "calculated" in normalized))
        or ("process period output" in normalized and ("payroll" in normalized or "payrun" in normalized or "run output" in normalized))
        or ("run output" in normalized and ("process period output" in normalized or "payroll output" in normalized or "platform" in normalized))
        or ("current effective payroll output" in normalized and "payroll output" in normalized)
        or ("current effective output" in normalized and "payroll output" in normalized)
        or ("calculated payroll output" in normalized and ("what" in normalized or "how" in normalized or "explain" in normalized))
    ) and not (
        ("gross to net" in normalized and not payroll_output_framed)
        or ("gross-to-net" in normalized and not payroll_output_framed)
        or ("net pay" in normalized and "payroll output" not in normalized)
        or "decision story" in normalized and "payroll output" not in normalized
        or "rate story" in normalized and "payroll output" not in normalized
        or "ratesource" in normalized and "payroll output" not in normalized
        or "rate source" in normalized and "payroll output" not in normalized
        or normalized.startswith("what is worker story")
        or ("worker story" in normalized and "payroll output" not in normalized)
        or ("payroll bases" in normalized and not payroll_output_framed)
        or ("payroll bases & totals" in normalized and not payroll_output_framed)
        or "leave accrual" in normalized
        or "leave processing" in normalized
        or "objecttime" in normalized
        or "objecttime / source truth" in normalized
        or "source truth" in normalized
        or ("finalisation readiness" in normalized and not payroll_output_framed)
        or ("finalization readiness" in normalized and not payroll_output_framed)
        or ("finalisation" in normalized and not payroll_output_framed)
        or ("finalization" in normalized and not payroll_output_framed)
        or ("payment execution / remittance" in normalized and not payroll_output_framed)
        or ("payment execution and remittance" in normalized and not payroll_output_framed)
        or ("payment execution remittance" in normalized and not payroll_output_framed)
        or ("payment file" in normalized and "payroll output" not in normalized)
        or "payrun admin queue" in normalized
        or "admin queue" in normalized and ("action" in normalized or "workbench" in normalized)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return PAYROLL_OUTPUT_PLAN
    if (
        contact_payroll_history_framed
    ) and not (
        "contacts / employee appointments" in normalized
        or "contacts and employee appointments" in normalized
        or "employee appointment" in normalized
        or "employeeappointment" in normalized
        or ("appointment" in normalized and "history" not in normalized)
        or "payroll output" in normalized and "history" not in normalized
        or "gross to net" in normalized and "history" not in normalized
        or "gross-to-net" in normalized and "history" not in normalized
        or "deductions / obligations" in normalized
        or "tax / payg" in normalized
        or "payment execution / remittance" in normalized
        or "retro / replay" in normalized and "history" not in normalized
        or "movement review" in normalized and "history" not in normalized
        or "payrun admin queue" in normalized and "history" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return CONTACT_PAYROLL_HISTORY_PLAN
    if (
        "gross to net" in normalized
        or "gross-to-net" in normalized
        or "grosstonet" in normalized
        or ("gross earnings" in normalized and "net pay" in normalized)
        or ("gross" in normalized and "taxable" in normalized and "net pay" in normalized)
    ) and not (
        "tax / payg" in normalized
        or "tax payg" in normalized
        or ("payg" in normalized and "gross to net" not in normalized and "gross-to-net" not in normalized)
        or "deductions / obligations" in normalized
        or ("deductions and obligations" in normalized and "gross to net" not in normalized)
        or "payment execution / remittance" in normalized
        or "payment execution and remittance" in normalized
        or "payment execution remittance" in normalized
        or "payment execution" in normalized
        or "payment destination" in normalized
        or "payment execution readiness" in normalized
        or "gross to net readiness" in normalized
        or "worker attention" in normalized
        or "issue resolution" in normalized
        or "payroll bases" in normalized
        or "payroll bases & totals" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return GROSS_TO_NET_PLAN
    if (
        "process periods / payrun lifecycle" in normalized
        or "process periods and payrun lifecycle" in normalized
        or (
            "processperiod" in normalized
            and (
                "payrun" in normalized
                or "lifecycle" in normalized
                or "period" in normalized
                or "processperiodgroup" in normalized
                or "open" in normalized
                or "closed" in normalized
                or "state" in normalized
                or "governance" in normalized
            )
        )
        or ("process period" in normalized and ("payrun" in normalized or "lifecycle" in normalized or "period" in normalized))
        or ("processperiodgroup" in normalized and ("payrun" in normalized or "calendar" in normalized or "payment" in normalized))
        or ("process period group" in normalized and ("payrun" in normalized or "calendar" in normalized or "payment" in normalized))
        or "payrun lifecycle" in normalized
        or ("paymentdate" in normalized and ("process period" in normalized or "payrun lifecycle" in normalized))
        or ("payment date" in normalized and ("process period" in normalized or "payrun lifecycle" in normalized))
        or ("payruncontact" in normalized and ("process period" in normalized or "lifecycle" in normalized or "admission" in normalized))
        or ("runpurpose" in normalized and ("runtype" in normalized or "payrun" in normalized))
        or ("run purpose" in normalized and ("run type" in normalized or "payrun" in normalized))
        or "close rolls forward" in normalized
        or ("admission" in normalized and "processing" in normalized)
        or ("regular" in normalized and "supplementary" in normalized and "retro" in normalized and "payrun" in normalized)
    ) and not (
        "tax / payg" in normalized
        or "tax payg" in normalized
        or "payg" in normalized
        or "payment execution / remittance" in normalized
        or "payment execution and remittance" in normalized
        or "payment execution remittance" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "matter" in normalized
        or "work" in normalized
    ):
        return PROCESS_PERIOD_PAYRUN_LIFECYCLE_PLAN
    if (
        "contacts and employee appointments" in normalized
        or "contacts / employee appointments" in normalized
        or "contact and employee appointment" in normalized
        or "contact / employee appointment" in normalized
        or ("employeeappointment" in normalized and ("contact" in normalized or "worker" in normalized or "appointment" in normalized))
        or ("employee appointment" in normalized and ("contact" in normalized or "worker" in normalized or "appointment" in normalized))
        or ("contact" in normalized and "appointment" in normalized and ("payrun admission" in normalized or "worker context" in normalized or "employment" in normalized))
        or ("contact history" in normalized and ("worker" in normalized or "payroll" in normalized or "finalised" in normalized))
        or ("worksiteposition" in normalized and ("appointment" in normalized or "contact" in normalized))
        or ("awardpositionclass" in normalized and ("appointment" in normalized or "contact" in normalized))
        or ("classification lens" in normalized and ("appointment" in normalized or "contact" in normalized))
        or ("worker readiness" in normalized and ("contact" in normalized or "appointment" in normalized))
        or ("contact" in normalized and ("tax" in normalized or "bank" in normalized or "deduction" in normalized or "payment readiness" in normalized))
        or ("worker attention" in normalized and "appointment" in normalized)
        or ("dirty contact" in normalized and ("appointment" in normalized or "employee" in normalized or "payroll affecting" in normalized))
    ) and not (
        "imports / actuals" in normalized
        or "imports and actuals" in normalized
        or "leave source model" in normalized
        or "leave accrual processing" in normalized
        or "comparison / remediation" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "matter" in normalized
        or "work" in normalized
    ):
        return CONTACTS_EMPLOYEE_APPOINTMENTS_PLAN
    if (
        "objecttime source truth" in normalized
        or "objecttime / source truth" in normalized
        or ("objecttime" in normalized and "source truth" in normalized)
        or ("objecttime" in normalized and ("source evidence" in normalized or "payroll calculation truth" in normalized))
        or ("objecttime" in normalized and ("source rows" in normalized or "source row" in normalized or "imported" in normalized or "generated" in normalized))
        or ("objecttime" in normalized and "payrun inclusion" in normalized)
        or ("sourcetruth" in normalized and ("workedhours" in normalized or "worked hours" in normalized))
        or ("source truth" in normalized and "worked hours" in normalized and "objecttime" in normalized)
        or ("source truth" in normalized and ("worker story" in normalized or "payroll bases" in normalized or "leave accrual" in normalized))
        or ("source truth" in normalized and ("comparison" in normalized or "movement review" in normalized or "retro" in normalized or "replay" in normalized))
        or ("source truth" in normalized and ("correction" in normalized or "dirty contact" in normalized or "reprocessing" in normalized))
        or ("raw span hours" in normalized and ("worked hours" in normalized or "objecttime" in normalized))
        or ("span hours" in normalized and ("worked hours" in normalized or "objecttime" in normalized))
        or ("dirty contact" in normalized and ("source truth" in normalized or "objecttime" in normalized))
        or ("reprocessing" in normalized and ("source truth" in normalized or "objecttime" in normalized))
        or ("correction audit" in normalized and ("source truth" in normalized or "objecttime" in normalized))
    ) and not (
        "imports / actuals" in normalized
        or "imports and actuals" in normalized
        or "imports actuals" in normalized
        or "imported timesheets" in normalized
        or "imported actuals" in normalized
        or "leave source truth" in normalized
        or "leave source model" in normalized
        or ("leave accrual" in normalized and "source truth" in normalized and "objecttime" not in normalized)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "matter" in normalized
        or "work" in normalized
    ):
        return OBJECTTIME_SOURCE_TRUTH_PLAN
    if (
        "imports and actuals" in normalized
        or "imports / actuals" in normalized
        or "imports actuals" in normalized
        or "imported timesheets" in normalized
        or "imported payroll actuals" in normalized
        or "imported actuals" in normalized and ("calculated interpreter truth" in normalized or "interpreter truth" in normalized or "calculated interpreter output" in normalized)
        or "payroll actuals" in normalized and ("import" in normalized or "source system" in normalized)
        or "actuals lane" in normalized and ("import" in normalized or "source system" in normalized)
        or "source system mapping" in normalized and ("import" in normalized or "actuals" in normalized)
        or "source-system mapping" in normalized and ("import" in normalized or "actuals" in normalized)
        or "pay code mapping" in normalized and ("import" in normalized or "actuals" in normalized)
        or "ratetype mapping" in normalized and ("import" in normalized or "actuals" in normalized)
        or "importedpositionclassificationmap" in normalized
        or "objecttime source truth" in normalized
        or "source row" in normalized and ("import" in normalized or "actuals" in normalized)
        or "import provenance" in normalized
        or "import run" in normalized
        or "import" in normalized and "actuals" in normalized and ("worker story" in normalized or "admin queue" in normalized)
        or "unmapped actuals" in normalized and ("import" in normalized or "admin queue" in normalized or "mapping" in normalized)
    ) and not (
        "comparison / remediation" in normalized
        or "comparison remediation" in normalized
        or "comparison lane" in normalized
        or "three comparison lanes" in normalized
        or "primary award path" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return IMPORTS_ACTUALS_PLAN
    if (
        "award build" in normalized
        or "award evidence" in normalized
        or "awardevidenceset" in normalized
        or "durable award evidence set" in normalized
        or ("pay guide" in normalized and "evidence" in normalized)
        or ("award document" in normalized and ("evidence" in normalized or "build" in normalized))
        or ("needs configuration" in normalized and "award" in normalized)
        or ("needs_configuration" in normalized and "award" in normalized)
        or "decisionevidenceindex" in normalized
        or "decision evidence index" in normalized
        or "ratesourceevidenceindex" in normalized
        or "rate source evidence index" in normalized
        or ("ratetype" in normalized and "awardratetype" in normalized)
        or ("rate type" in normalized and "award rate type" in normalized)
        or ("ratesource" in normalized and "date effective" in normalized and "rate evidence" in normalized)
        or ("rate source" in normalized and "date effective" in normalized and "rate evidence" in normalized)
        or ("classification" in normalized and "position" in normalized and "class evidence" in normalized)
    ) and not (
        "on costs" in normalized
        or "oncosts" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return AWARD_BUILD_EVIDENCE_PLAN
    if (
        "on costs" in normalized
        or "oncosts" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
        or "super oncost" in normalized
        or "superannuation on cost" in normalized
        or "superannuation oncost" in normalized
        or "payrolltax oncost" in normalized
        or "payroll tax on cost" in normalized
        or "workcover oncost" in normalized
        or "workcover" in normalized
        or ("wic" in normalized and ("on cost" in normalized or "liability" in normalized or "rate" in normalized))
        or ("ratesource" in normalized and ("employer" in normalized or "liability" in normalized or "state scoped" in normalized))
        or ("date effective rates" in normalized and ("employer" in normalized or "liability" in normalized))
        or ("runtime location" in normalized and ("employer" in normalized or "liability" in normalized))
        or ("account wide fallback" in normalized and "ratesource" in normalized)
        or ("account wide fallback" in normalized and ("demo" in normalized or "production truth" in normalized))
        or ("demo fallback" in normalized and ("employer" in normalized or "liability" in normalized or "production truth" in normalized))
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return ONCOSTS_EMPLOYER_LIABILITIES_PLAN
    if (
        "leave source model" in normalized
        or "leave source truth" in normalized
        or ("leave source" in normalized and "applicability" in normalized)
        or ("leave applicability" in normalized and "leave rule content" in normalized)
        or ("leave applicability" in normalized and ("source" in normalized or "model" in normalized or "leavetyperule" in normalized))
        or ("leave type rule" in normalized and "final applicability truth" in normalized)
        or ("leavetyperule" in normalized and "final applicability truth" in normalized)
        or ("missing leave output" in normalized and ("applicability" in normalized or "source truth" in normalized))
        or ("contact scope" in normalized and "leave" in normalized)
        or ("contact versus appointment" in normalized and "leave" in normalized)
        or ("contact vs appointment" in normalized and "leave" in normalized)
        or ("employeeappointment scope" in normalized and "leave" in normalized)
        or ("employee appointment scope" in normalized and "leave" in normalized)
        or ("appointment aware leave" in normalized)
        or ("source dimensions" in normalized and "leave" in normalized)
    ) and not (
        ("leave request" in normalized or "leaverequest" in normalized) and "workflow" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "matter" in normalized
    ):
        return LEAVE_SOURCE_MODEL_PLAN
    if (
        "leave requests / leave workflow" in normalized
        or "leave requests leave workflow" in normalized
        or ("leave workflow" in normalized and ("what" in normalized or "how" in normalized or "platform" in normalized))
        or ("leave requests" in normalized and ("workflow" in normalized or "status" in normalized or "draft" in normalized or "submit" in normalized or "approve" in normalized or "reject" in normalized or "reopen" in normalized or "leaveledger" in normalized or "posting" in normalized or "balance" in normalized or "worker story" in normalized or "payrun" in normalized or "finalisation readiness" in normalized or "finalization readiness" in normalized))
        or ("leave request" in normalized and ("workflow" in normalized or "status" in normalized or "draft" in normalized or "submit" in normalized or "approve" in normalized or "reject" in normalized or "reopen" in normalized))
        or ("leaverequest" in normalized and ("workflow" in normalized or "status" in normalized or "draft" in normalized or "submit" in normalized or "approve" in normalized or "reject" in normalized or "reopen" in normalized))
        or ("leave submission" in normalized and ("workflow" in normalized or "review" in normalized or "approval" in normalized))
        or ("submit leave" in normalized and ("workflow" in normalized or "request" in normalized))
        or ("approve leave" in normalized and ("workflow" in normalized or "request" in normalized))
        or ("reject leave" in normalized and ("workflow" in normalized or "request" in normalized))
        or ("reopen leave" in normalized and ("workflow" in normalized or "request" in normalized))
        or ("idempotencykey" in normalized and "leave" in normalized)
        or ("leave overlap" in normalized and ("workflow" in normalized or "request" in normalized))
        or ("shortfall substitution" in normalized and ("leave" in normalized or "request" in normalized))
        or ("leave request preview" in normalized)
    ) and not (
        "leave source model" in normalized
        or "leave source truth" in normalized
        or ("leave source" in normalized and "applicability" in normalized and "workflow" not in normalized)
        or ("leave accrual processing" in normalized)
        or ("leave accrual" in normalized and "workflow" not in normalized and "request" not in normalized)
        or ("leave processing" in normalized and "workflow" not in normalized and "request" not in normalized)
        or ("payroll output" in normalized and "workflow" not in normalized)
        or ("worker story" in normalized and "workflow" not in normalized and "leave request" not in normalized)
        or ("finalisation readiness" in normalized and "workflow" not in normalized and "leave request" not in normalized)
        or ("contact payroll history" in normalized)
        or ("deductions / obligations" in normalized)
        or ("gross to net" in normalized and "workflow" not in normalized and "leave request" not in normalized)
        or ("gross-to-net" in normalized and "workflow" not in normalized and "leave request" not in normalized)
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
        or "platform" in normalized
    ):
        return LEAVE_REQUESTS_WORKFLOW_PLAN
    if (
        "finalisation readiness" in normalized
        or "finalization readiness" in normalized
        or ("finalisation" in normalized and ("readiness" in normalized or "ready" in normalized or "warning" in normalized or "blocker" in normalized or "current effective" in normalized or "payroll output" in normalized or "worker story" in normalized or "review surface" in normalized))
        or ("finalization" in normalized and ("readiness" in normalized or "ready" in normalized or "warning" in normalized or "blocker" in normalized or "current effective" in normalized or "payroll output" in normalized or "worker story" in normalized or "review surface" in normalized))
        or ("payment execution readiness" in normalized and "gross to net readiness" in normalized)
        or ("payment execution readiness" in normalized and "gross-to-net readiness" in normalized)
        or "finalised outcome truth" in normalized
        or "finalized outcome truth" in normalized
        or "finalisation audit" in normalized
        or "finalization audit" in normalized
        or ("warning acknowledgement" in normalized and ("finalisation" in normalized or "payrun" in normalized))
        or ("warning acknowledgment" in normalized and ("finalization" in normalized or "payrun" in normalized))
        or ("green" in normalized and "readiness" in normalized)
        or ("finalised outcome" in normalized and ("readiness" in normalized or "finalisation" in normalized))
        or ("finalized outcome" in normalized and ("readiness" in normalized or "finalization" in normalized))
    ) and (
        not normalized.startswith("how does the payrun admin queue")
        and not normalized.startswith("how does payrun admin queue")
        and not ("payrun processing" in normalized and "leave readiness" in normalized)
        and "missing leave output" not in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return FINALISATION_READINESS_PLAN
    if (
        "leave accrual processing" in normalized
        or "leave accrual detail" in normalized
        or ("leave accrual" in normalized and ("minerva" in normalized or "source truth" in normalized or "applicability" in normalized))
        or ("leave accrual" in normalized and ("calcinterpreterline" in normalized or "current effective payroll output" in normalized))
        or ("leave accrual" in normalized and ("worker story" in normalized or "payroll bases" in normalized or "finalisation" in normalized))
        or ("leave accrue" in normalized and ("processed" in normalized or "processing" in normalized or "ezeas" in normalized))
        or ("leave processing" in normalized and ("how" in normalized or "what" in normalized or "ezeas" in normalized))
        or ("leavetyperule" in normalized and ("leave" in normalized or "applicability" in normalized or "processing" in normalized))
        or ("leave type rule" in normalized and ("leave" in normalized or "applicability" in normalized or "processing" in normalized))
        or ("leavetype" in normalized and "leave processing" in normalized)
        or ("leave type" in normalized and "leave processing" in normalized)
        or ("leaveledger" in normalized and ("what" in normalized or "explain" in normalized or "leave" in normalized))
        or ("leave ledger" in normalized and ("what" in normalized or "explain" in normalized or "leave" in normalized))
        or ("leave request" in normalized and ("payment effects" in normalized or "sequencing" in normalized))
        or ("leave readiness" in normalized and ("payrun" in normalized or "finalisation" in normalized))
        or ("missing leave output" in normalized and ("payrun" in normalized or "finalisation" in normalized))
        or ("leave source model" in normalized and "leave" in normalized)
        or ("leave valuation basis" in normalized and "leave" in normalized)
        or ("accrual basis" in normalized and "leave" in normalized)
        or ("accrualability" in normalized and ("leave" in normalized or "awardratetype" in normalized or "rate type" in normalized))
        or ("calcinterpreterline" in normalized and ("leave" in normalized or "accrual" in normalized))
        or ("calc interpreter line" in normalized and ("leave" in normalized or "accrual" in normalized))
        or ("current effective payroll output" in normalized and ("leave" in normalized or "accrual" in normalized))
        or ("leaveprocessrun" in normalized or "leave process run" in normalized)
        or ("taken leave" in normalized and "valuation" in normalized)
        or ("per hour" in normalized and ("leave" in normalized or "accrual" in normalized))
        or ("per_hour" in normalized and ("leave" in normalized or "accrual" in normalized))
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return LEAVE_ACCRUAL_PROCESSING_PLAN
    if (
        "payment execution remittance" in normalized
        or "payment execution and remittance" in normalized
        or "payment execution" in normalized
        or ("remittance" in normalized and ("payment" in normalized or "deduction" in normalized or "third party" in normalized))
        or "generate bank file" in normalized
        or "bank file" in normalized
        or "period close" in normalized
        or "payment allocation" in normalized
        or "payment destination" in normalized
        or "bank allocation" in normalized
        or "worker net pay" in normalized
        or "third party remittance" in normalized
        or "remittance batching" in normalized
        or "remittance reconciliation" in normalized
        or "payment file" in normalized
        or "obligation write off" in normalized
    ) and (
        "what" in normalized
        or "how" in normalized
        or "why" in normalized
        or "should" in normalized
        or "evidence" in normalized
        or "explain" in normalized
        or "work" in normalized
    ):
        return PAYMENT_EXECUTION_REMITTANCE_PLAN
    if (
        "retro replay" in normalized
        or "retro / replay" in normalized
        or "retro payrun" in normalized
        or "retro pay run" in normalized
        or "attributed period" in normalized
        or "paid period" in normalized
        or "finalised outcome memory" in normalized
        or "finalized outcome memory" in normalized
        or "finalised payroll truth" in normalized
        or "finalized payroll truth" in normalized
        or ("current effective truth" in normalized and ("historical" in normalized or "finalised" in normalized or "finalized" in normalized))
        or ("current-effective truth" in normalized and ("historical" in normalized or "finalised" in normalized or "finalized" in normalized))
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

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.domain_retrieval_plan_service import LEAVE_REQUESTS_WORKFLOW_PLAN, EvidenceGroup
from app.services.knowledge_retrieval_service import RetrievalResult, retrieve_relevant_chunks


LEAVE_REQUESTS_WORKFLOW_DIAGNOSTIC_GROUPS: tuple[EvidenceGroup, ...] = (
    EvidenceGroup(
        group_id="request_lifecycle_and_status_transitions",
        label="Leave Requests / Leave Workflow request lifecycle and status transitions",
        query_terms=(
            "Leave Request workflow",
            "create leave request",
            "draft leave",
            "submit leave",
            "review leave",
            "approve leave",
            "reject leave",
            "reopen leave",
            "status transitions",
        ),
        required_terms_any=("Leave Request", "draft", "submit leave", "review leave", "approve leave", "status transitions"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="preview_overlap_and_shortfall_handling",
        label="Leave Requests / Leave Workflow preview overlap and shortfall handling",
        query_terms=(
            "leave request preview",
            "leave overlap",
            "overlap handling",
            "same-type overlap",
            "cross-type overlap",
            "shortfall substitution",
            "apply-plan",
            "child request linkage",
        ),
        required_terms_any=("leave request preview", "leave overlap", "shortfall substitution", "same-type overlap", "cross-type overlap"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="taken_leave_valuation_and_hard_fail",
        label="Leave Requests / Leave Workflow TAKEN leave valuation and hard fail",
        query_terms=(
            "TAKEN leave",
            "leave valuation",
            "leave valuation basis",
            "ordinary rate",
            "hard fail",
            "no silent minutes-only fallback",
            "structured processing error",
            "needs configuration",
        ),
        required_terms_any=("TAKEN leave", "leave valuation", "leave valuation basis", "hard fail", "ordinary rate"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="leaveledger_posting_and_balance_effects",
        label="Leave Requests / Leave Workflow LeaveLedger posting and balance effects",
        query_terms=(
            "LeaveLedger posting",
            "leave posting",
            "leave balance",
            "accrual",
            "taken",
            "balance movement",
            "parent/child request lineage",
            "posting evidence",
            "audit/story",
        ),
        required_terms_any=("LeaveLedger", "LeaveLedger posting", "leave balance", "balance movement", "posting evidence"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="leave_source_and_applicability_relationship",
        label="Leave Requests / Leave Workflow Leave Source and applicability relationship",
        query_terms=(
            "Leave Source Model",
            "leave applicability",
            "LeaveTypeRule",
            "policy calculation content",
            "Contact",
            "EmployeeAppointment",
            "employment/worksite/state dimensions",
            "no entitlement",
            "missing output",
        ),
        required_terms_any=("Leave Source Model", "leave applicability", "LeaveTypeRule", "Contact", "EmployeeAppointment"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="worker_story_payrun_and_finalisation_relationship",
        label="Leave Requests / Leave Workflow Worker Story PayRun and finalisation relationship",
        query_terms=(
            "Worker Story",
            "Leave and Accrual Outcome",
            "PayRun processing",
            "leave payment effects",
            "leave output",
            "valuation",
            "ledger evidence",
            "finalisation readiness",
            "warnings",
            "blockers",
        ),
        required_terms_any=("Worker Story", "PayRun", "PayRun processing", "finalisation readiness", "Leave and Accrual Outcome"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="idempotency_reopen_and_approval_governance",
        label="Leave Requests / Leave Workflow idempotency reopen and approval governance",
        query_terms=(
            "IdempotencyKey",
            "idempotency",
            "idempotent leave",
            "approve leave",
            "reject leave",
            "reopen leave",
            "operator/user action",
            "governed workflow transitions",
        ),
        required_terms_any=("IdempotencyKey", "idempotency", "approve leave", "reject leave", "reopen leave"),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    EvidenceGroup(
        group_id="minerva_boundaries_and_non_mutation_guardrails",
        label="Leave Requests / Leave Workflow Minerva boundaries and non-mutation guardrails",
        query_terms=(
            "Minerva does not approve leave",
            "calculate leave",
            "post LeaveLedger rows",
            "change leave balances",
            "reopen leave requests",
            "resolve shortfalls",
            "finalise PayRuns",
            "mutate operational leave or payroll truth",
        ),
        required_terms_any=(
            "Minerva does not approve leave",
            "calculate leave",
            "post LeaveLedger rows",
            "change leave balances",
            "mutate operational leave or payroll truth",
        ),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
)


@dataclass(frozen=True)
class LeaveRequestsWorkflowGroupCoverage:
    group_key: str
    group_label: str
    search_terms_used: list[str]
    matched_chunk_count: int
    matched_document_count: int
    matched_sources: list[dict]
    representative_matched_terms: list[str]
    coverage_status: str
    diagnostic_notes: list[str]

    def to_dict(self) -> dict:
        return {
            "group_key": self.group_key,
            "group_label": self.group_label,
            "search_terms_used": self.search_terms_used,
            "matched_chunk_count": self.matched_chunk_count,
            "matched_document_count": self.matched_document_count,
            "matched_sources": self.matched_sources,
            "representative_matched_terms": self.representative_matched_terms,
            "coverage_status": self.coverage_status,
            "diagnostic_notes": self.diagnostic_notes,
        }


@dataclass(frozen=True)
class LeaveRequestsWorkflowCoverageReport:
    plan_id: str
    domain: str
    generated_at_utc: str
    total_evidence_groups: int
    coverage_counts: dict[str, int]
    corpus_document_count: int
    corpus_chunk_count: int
    groups: list[LeaveRequestsWorkflowGroupCoverage]
    mutation_performed: bool = False
    live_llm_call_performed: bool = False
    operational_json_ingestion_performed: bool = False

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "domain": self.domain,
            "generated_at_utc": self.generated_at_utc,
            "total_evidence_groups": self.total_evidence_groups,
            "coverage_counts": self.coverage_counts,
            "corpus_document_count": self.corpus_document_count,
            "corpus_chunk_count": self.corpus_chunk_count,
            "mutation_performed": self.mutation_performed,
            "live_llm_call_performed": self.live_llm_call_performed,
            "operational_json_ingestion_performed": self.operational_json_ingestion_performed,
            "groups": [group.to_dict() for group in self.groups],
        }


def _term_in_text(term: str, text: str) -> bool:
    return term.lower() in text.lower()


def _matched_terms(group: EvidenceGroup, results: list[RetrievalResult]) -> list[str]:
    terms = list(dict.fromkeys([*group.query_terms, *group.required_terms_any]))
    matched: list[str] = []
    for term in terms:
        if any(_term_in_text(term, f"{result.title or ''}\n{result.chunk_text}") for result in results):
            matched.append(term)
    return matched


def _matched_sources(results: list[RetrievalResult]) -> list[dict]:
    sources: dict[str, dict] = {}
    for result in results:
        key = result.document_id
        if key not in sources:
            sources[key] = {
                "title": result.title,
                "source_type": result.source_type,
                "original_file_name": result.original_file_name,
                "matched_chunk_count": 0,
            }
        sources[key]["matched_chunk_count"] += 1
    return sorted(
        sources.values(),
        key=lambda item: (str(item["title"] or "").lower(), str(item["source_type"]).lower()),
    )


def _coverage_status(matched_chunk_count: int, matched_document_count: int, matched_term_count: int) -> str:
    if matched_chunk_count == 0 or matched_term_count == 0:
        return "MISSING"
    if matched_document_count >= 2 and matched_term_count >= 2:
        return "STRONG"
    if matched_chunk_count >= 2 and matched_term_count >= 3:
        return "STRONG"
    return "WEAK"


def _diagnostic_notes(status: str, matched_term_count: int, matched_document_count: int) -> list[str]:
    if status == "STRONG":
        return [
            f"Found support across {matched_document_count} document(s).",
            f"Matched {matched_term_count} planned term(s) for this evidence group.",
        ]
    if status == "WEAK":
        return [
            "Some formal-corpus support was found, but breadth is limited.",
            "Refine retrieval or synthesis before widening Leave Requests / Leave Workflow claims.",
        ]
    return [
        "No useful formal-corpus support was found for this evidence group.",
        "Answers should state that the loaded formal corpus is insufficient for this group.",
    ]


def _count_active_documents(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(KnowledgeDocument).where(KnowledgeDocument.DocumentStatus == "ACTIVE")) or 0


def _count_active_chunks(db: Session) -> int:
    stmt = (
        select(func.count())
        .select_from(KnowledgeChunk)
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.DocumentStatus == "ACTIVE")
    )
    return db.scalar(stmt) or 0


def scan_leave_requests_workflow_corpus_coverage(
    db: Session,
    top_k_per_group: int = 10,
    tenant_id: str | None = None,
) -> LeaveRequestsWorkflowCoverageReport:
    group_reports: list[LeaveRequestsWorkflowGroupCoverage] = []
    coverage_counts = {"STRONG": 0, "WEAK": 0, "MISSING": 0}

    for group in LEAVE_REQUESTS_WORKFLOW_DIAGNOSTIC_GROUPS:
        results = retrieve_relevant_chunks(
            db=db,
            query=" ".join(group.query_terms),
            tenant_id=tenant_id,
            top_k=top_k_per_group,
            source_types=list(group.preferred_source_types),
            include_samples=False,
        )
        useful_results = [
            result
            for result in results
            if any(_term_in_text(term, f"{result.title or ''}\n{result.chunk_text}") for term in group.required_terms_any)
        ]
        matched_terms = _matched_terms(group, useful_results)
        sources = _matched_sources(useful_results)
        status = _coverage_status(len(useful_results), len(sources), len(matched_terms))
        coverage_counts[status] += 1
        group_reports.append(
            LeaveRequestsWorkflowGroupCoverage(
                group_key=group.group_id,
                group_label=group.label,
                search_terms_used=list(group.query_terms),
                matched_chunk_count=len(useful_results),
                matched_document_count=len(sources),
                matched_sources=sources,
                representative_matched_terms=matched_terms[:12],
                coverage_status=status,
                diagnostic_notes=_diagnostic_notes(status, len(matched_terms), len(sources)),
            )
        )

    return LeaveRequestsWorkflowCoverageReport(
        plan_id=LEAVE_REQUESTS_WORKFLOW_PLAN.plan_id,
        domain=LEAVE_REQUESTS_WORKFLOW_PLAN.domain,
        generated_at_utc=datetime.now(UTC).isoformat(),
        total_evidence_groups=len(LEAVE_REQUESTS_WORKFLOW_DIAGNOSTIC_GROUPS),
        coverage_counts=coverage_counts,
        corpus_document_count=_count_active_documents(db),
        corpus_chunk_count=_count_active_chunks(db),
        groups=group_reports,
    )

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

DOMAIN_RETRIEVAL_PLANS = (ANNUAL_LEAVE_MANAGEMENT_PLAN,)


def _normalize_question(text: str) -> str:
    return " ".join(text.lower().replace("-", " ").split()).rstrip("?")


def detect_domain_retrieval_plan(question: str) -> DomainRetrievalPlan | None:
    normalized = _normalize_question(question)
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

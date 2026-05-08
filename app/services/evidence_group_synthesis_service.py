from dataclasses import dataclass

from app.services.domain_retrieval_plan_service import DomainRetrievalPlan, EvidenceGroup
from app.services.knowledge_retrieval_service import RetrievalResult


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
}

GROUP_SIGNAL_TERMS = {
    "configuration": ("LeaveType", "LeaveTypeRule", "LeaveTypeKind", "Rule Cockpit"),
    "accrual": ("accrual", "LeaveLedger", "minutes", "interpreter truth", "no fallback"),
    "taken": ("TAKEN", "DeductsOnPublicHoliday", "public holiday", "minutes"),
    "valuation": ("valuation", "valuation basis", "ordinary rate", "snapshot", "liability"),
    "payrun": ("PayRun", "Generate Leave Accruals on Process", "leave accruals", "Admin Queue"),
    "worker_story": ("Worker Story", "Leave and Accrual Outcome", "server-owned leave output", "evidence chain"),
    "outstanding": ("outstanding", "hardening", "Leave Source Model", "FIFO", "lot consumption", "revaluation"),
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
    lower_text = text.lower()
    return [term for term in terms if term.lower() in lower_text]


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
    clauses = ["Configuration evidence indicates Annual Leave rule setup is represented in the formal corpus"]
    if _has_any(terms, "LeaveType", "LeaveTypeRule"):
        clauses.append("through LeaveType/LeaveTypeRule configuration")
    if _has_any(terms, "LeaveTypeKind", "Rule Cockpit"):
        clauses.append("with LeaveTypeKind and Rule Cockpit surfaces organising leave-rule setup")
    settings = [term for term in ("Accrual", "Payment", "Governance") if _has_any(terms, term)]
    if settings:
        clauses.append(f"including {', '.join(settings)} settings")
    return f"{label}: {', '.join(clauses)}."


def _accrual_sentence(terms: list[str], label: str) -> str:
    clauses = ["Accrual evidence indicates Annual Leave accrual is represented separately from consumption"]
    if _has_any(terms, "LeaveLedger"):
        clauses.append("through LeaveLedger-style entitlement movement")
    if _has_any(terms, "minutes"):
        clauses.append("with minutes present in the retrieved evidence")
    if _has_any(terms, "interpreter truth", "no fallback"):
        clauses.append("and with interpreter-truth/no-fallback controls indicated where retrieved")
    if _has_any(terms, "process period", "PayRun"):
        clauses.append("in the process-period or PayRun flow where available")
    return f"{label}: {', '.join(clauses)}."


def _taken_sentence(terms: list[str], label: str) -> str:
    clauses = ["TAKEN leave evidence indicates Annual Leave consumption is represented separately from accrual"]
    if _has_any(terms, "LeaveLedger"):
        clauses.append("with LeaveLedger posting evidence")
    if _has_any(terms, "minutes"):
        clauses.append("using minutes where retrieved")
    if _has_any(terms, "public holiday", "DeductsOnPublicHoliday"):
        clauses.append("and public holiday deduction controlled by DeductsOnPublicHoliday")
    if _has_any(terms, "skip", "resolver"):
        clauses.append("with resolver or skip behaviour indicated by the retrieved corpus")
    return f"{label}: {', '.join(clauses)}."


def _valuation_sentence(terms: list[str], label: str) -> str:
    clauses = ["Valuation evidence indicates Annual Leave value is treated as a distinct evidence area"]
    if _has_any(terms, "valuation basis"):
        clauses.append("connected to valuation-basis evidence")
    if _has_any(terms, "ordinary rate"):
        clauses.append("with ordinary-rate evidence where retrieved")
    if _has_any(terms, "PayRun", "snapshot"):
        clauses.append("and PayRun or snapshot context present in the corpus")
    if _has_any(terms, "liability"):
        clauses.append("including liability context where retrieved")
    return f"{label}: {', '.join(clauses)}."


def _payrun_sentence(terms: list[str], label: str) -> str:
    clauses = ["PayRun evidence indicates leave processing is part of the PayRun operating flow"]
    if _has_any(terms, "Generate Leave Accruals on Process"):
        clauses.append("with Generate Leave Accruals on Process exposed as an explicit processing option")
    if _has_any(terms, "leave accruals"):
        clauses.append("including leave-accrual generation")
    if _has_any(terms, "valuation basis"):
        clauses.append("and valuation-basis generation where retrieved")
    if _has_any(terms, "Admin Queue"):
        clauses.append("with Admin Queue context present")
    return f"{label}: {', '.join(clauses)}."


def _worker_story_sentence(terms: list[str], label: str) -> str:
    clauses = ["Worker Story evidence indicates leave outcomes are explained through worker-facing evidence output"]
    if _has_any(terms, "Leave and Accrual Outcome"):
        clauses.append("including a Leave and Accrual Outcome chapter")
    if _has_any(terms, "server-owned leave output"):
        clauses.append("as server-owned leave output")
    if _has_any(terms, "ledger", "valuation basis", "evidence chain"):
        details = [term for term in ("ledger", "valuation basis", "evidence chain") if _has_any(terms, term)]
        clauses.append(f"with {', '.join(details)} details")
    return f"{label}: {', '.join(clauses)}."


def _outstanding_sentence(terms: list[str], label: str) -> str:
    clauses = ["Outstanding-hardening evidence indicates Annual Leave still has future work or hardening context"]
    if _has_any(terms, "Leave Source Model"):
        clauses.append("around the Leave Source Model")
    lot_terms = [term for term in ("FIFO", "lot consumption", "revaluation") if _has_any(terms, term)]
    if lot_terms:
        clauses.append(f"including {', '.join(lot_terms)} where applicable")
    if _has_any(terms, "production hardening", "hardening"):
        clauses.append("and production hardening")
    return f"{label}: {', '.join(clauses)}."


def _sentence_for_group(group: EvidenceGroup, terms: list[str]) -> str:
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
    return f"{group.label}: Retrieved evidence indicates {', '.join(terms)}."


def synthesize_evidence_group(group: EvidenceGroup, results: list[RetrievalResult]) -> EvidenceGroupSummary:
    if not results:
        return _weak_summary(group)
    evidence_text = _evidence_text(results)
    terms = _detect_terms(evidence_text, GROUP_KEY_TERMS.get(group.group_id, group.required_terms_any))
    signal_terms = _detect_terms(evidence_text, GROUP_SIGNAL_TERMS.get(group.group_id, group.required_terms_any))
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

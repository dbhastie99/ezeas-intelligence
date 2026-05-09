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
    "current_effective_truth": (
        "current-effective truth",
        "current-effective payroll output",
        "current-effective interpreter run",
        "Correction Audit Story",
    ),
    "outstanding_hardening": ("Worker Story", "outstanding hardening", "limitations", "future work", "hardening"),
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
    "calculated_payroll_outcome": ("Calculated Payroll Outcome", "current-effective payroll output"),
    "decision_story_and_rate_story": ("Decision Story", "Rate Story", "DecisionEvidenceIndex", "RateSourceEvidenceIndex"),
    "leave_and_accrual_outcome": ("Leave and Accrual Outcome", "leave", "accrual"),
    "payroll_bases_and_totals": ("Payroll Bases & Totals", "payroll bases", "totals"),
    "movement_review_and_admin_queue": ("Movement Review", "PayRun Admin Queue", "Admin Queue"),
    "current_effective_truth": ("current-effective truth", "current-effective payroll output", "current-effective interpreter run"),
    "outstanding_hardening": ("outstanding hardening", "limitations", "hardening"),
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

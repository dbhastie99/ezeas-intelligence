import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from app.services.controlled_citation_provenance_packet_service import (
    BLOCKED_PROHIBITED_CLAIMS,
    OPERATOR_SCENARIO_REASONING,
    PAYROLL_CORRECTION_WORKFLOW_REASONING,
    PROHIBITED,
    PROVENANCE_READY,
    PROVENANCE_READY_WITH_CAVEATS,
    SUPPORTED,
    SUPPORTED_WITH_CAVEAT,
    build_controlled_citation_provenance_packet,
)
from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)


REHEARSAL_UNIVERSE = "CONTROLLED_CITATION_PROVENANCE_PACKET_V0_1"
REHEARSAL_LABEL = "CONTROLLED_REHEARSAL_ONLY"

WHY_EXPLANATION = "WHY_EXPLANATION"
TREATMENT_EXPLANATION = "TREATMENT_EXPLANATION"
STATUS_EXPLANATION = "STATUS_EXPLANATION"
EVIDENCE_GAP_EXPLANATION = "EVIDENCE_GAP_EXPLANATION"
GENERAL_CONTROLLED_REHEARSAL = "GENERAL_CONTROLLED_REHEARSAL"

PAYROLL_OPERATOR = "PAYROLL_OPERATOR"

CONTROLLED_REHEARSAL_READY = "CONTROLLED_REHEARSAL_READY"
CONTROLLED_REHEARSAL_READY_WITH_CAVEATS = "CONTROLLED_REHEARSAL_READY_WITH_CAVEATS"
INSUFFICIENT_EVIDENCE_FOR_REHEARSAL = "INSUFFICIENT_EVIDENCE_FOR_REHEARSAL"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

SUPPORTED_STATUSES = {SUPPORTED, SUPPORTED_WITH_CAVEAT}
UNSUPPORTED_STATUSES = {
    "UNSUPPORTED",
    "REQUIRES_CURRENT_RUNTIME_EVIDENCE",
    "REQUIRES_CODE_EVIDENCE",
    "REQUIRES_DB_EVIDENCE",
    "REQUIRES_DEPLOYMENT_EVIDENCE",
    "REQUIRES_PRODUCTION_EVIDENCE",
}

NEXT_STEP = (
    "Use this controlled rehearsal only as input to a later answer gate. Do not "
    "expose it as chat, a final answer, runtime output, DB truth, deployment "
    "truth, or production readiness."
)

BASE_CAVEATS = (
    "This is CONTROLLED_REHEARSAL_ONLY, not FINAL_ANSWER, LIVE_CHAT_RESPONSE, or RUNTIME_ANSWER.",
    "Final answer generation remains disabled.",
    "No live LLM, chat endpoint, DB read/write, live corpus mutation, runtime integration, or production-readiness claim is performed.",
    "Payroll reasoning evidence is curated scenario reasoning, not Workforce runtime proof.",
    "Object-specific answers require authorised object story, runtime, and DB evidence.",
)

OBJECT_EVIDENCE_GAPS = (
    ("CorrectionReviewId / object story", "Required to identify the specific correction review being explained."),
    ("SourceChangeSummary", "Required to prove what changed in source truth."),
    ("ProcessPeriodLifecycleStatus", "Required to decide open, locked, finalised, or payment-state treatment."),
    ("PaymentWindowStatus", "Required to distinguish banking netting, payment execution, and recovery paths."),
    ("PayRun / PayRunContact state", "Required to distinguish dirty reprocessing from supplementary or retro treatment."),
    ("Payment execution state", "Required to distinguish payment-layer netting from overpayment/recovery review."),
    ("DB/runtime evidence", "Required before making worker-specific or current-state claims."),
)


@dataclass(frozen=True)
class ControlledAnswerRehearsalEnvelope:
    QueryText: str
    RehearsalMode: str
    Audience: str
    RehearsalStatus: str
    ControlledAnswerDraft: dict[str, Any]
    AnswerSections: tuple[dict[str, Any], ...]
    ClaimsIncluded: tuple[dict[str, Any], ...]
    ClaimsExcluded: tuple[dict[str, Any], ...]
    CitationPlan: tuple[dict[str, Any], ...]
    RequiredCaveats: tuple[str, ...]
    EvidenceGaps: tuple[dict[str, Any], ...]
    ProhibitedClaimsExcluded: tuple[dict[str, Any], ...]
    UnsupportedClaimsExcluded: tuple[dict[str, Any], ...]
    BoundaryFlags: dict[str, bool]
    FinalAnswerPermitted: bool
    NextStep: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_answer_rehearsal(
    query_text: str,
    citation_provenance_packet: dict[str, Any] | None = None,
    rehearsal_mode: str = GENERAL_CONTROLLED_REHEARSAL,
    audience: str = PAYROLL_OPERATOR,
) -> dict[str, Any]:
    return rehearse_controlled_answer(
        query_text=query_text,
        citation_provenance_packet=citation_provenance_packet,
        rehearsal_mode=rehearsal_mode,
        audience=audience,
    )


def rehearse_controlled_answer(
    query_text: str,
    citation_provenance_packet: dict[str, Any] | None = None,
    rehearsal_mode: str = GENERAL_CONTROLLED_REHEARSAL,
    audience: str = PAYROLL_OPERATOR,
) -> dict[str, Any]:
    """Build a deterministic non-final answer rehearsal over provenance claims."""

    query = str(query_text or "")
    packet = citation_provenance_packet or build_controlled_citation_provenance_packet(query)
    scenario = _scenario(query)
    mode = _normalize_rehearsal_mode(rehearsal_mode, query, scenario)

    prohibited = _prohibited_claims(packet, query)
    unsupported = _unsupported_claims(packet)
    included = _included_claims(packet)
    if scenario != "general":
        included = _ensure_scenario_claim(packet, included, scenario)

    evidence_gaps = _evidence_gaps(query, scenario, packet)
    status = _rehearsal_status(
        packet=packet,
        prohibited=prohibited,
        unsupported=unsupported,
        included=included,
        evidence_gaps=evidence_gaps,
        query=query,
        scenario=scenario,
    )
    sections = _answer_sections(
        query=query,
        scenario=scenario,
        status=status,
        included=included,
        evidence_gaps=evidence_gaps,
    )
    citation_plan = _citation_plan(included)
    caveats = _required_caveats(packet, scenario, evidence_gaps)

    draft = {
        "Label": REHEARSAL_LABEL,
        "DraftStatus": "NOT_FINAL_ANSWER",
        "FinalAnswerPermitted": False,
        "Audience": _normalize_audience(audience),
        "Sections": sections,
        "DisallowedUses": (
            "FINAL_ANSWER",
            "LIVE_CHAT_RESPONSE",
            "RUNTIME_ANSWER",
        ),
    }

    return ControlledAnswerRehearsalEnvelope(
        QueryText=query,
        RehearsalMode=mode,
        Audience=_normalize_audience(audience),
        RehearsalStatus=status,
        ControlledAnswerDraft=draft,
        AnswerSections=sections,
        ClaimsIncluded=included,
        ClaimsExcluded=(*unsupported, *prohibited),
        CitationPlan=citation_plan,
        RequiredCaveats=caveats,
        EvidenceGaps=evidence_gaps,
        ProhibitedClaimsExcluded=prohibited,
        UnsupportedClaimsExcluded=unsupported,
        BoundaryFlags=_boundary_flags(),
        FinalAnswerPermitted=False,
        NextStep=NEXT_STEP,
    ).to_dict()


def _scenario(query: str) -> str:
    normalized = _normalize(query)
    if "supplementary" in normalized and ("dirty" in normalized or "reprocess" in normalized):
        return "supplementary_vs_dirty"
    if "negative" in normalized and ("net" in normalized or "bank" in normalized or "recover" in normalized):
        return "negative_delta_payment"
    if "payment date" in normalized or ("year end" in normalized and "payment" in normalized):
        return "payment_date_year_end"
    if "retro" in normalized and ("current pay" in normalized or "adjustment" in normalized):
        return "retro_vs_current_adjustment"
    if _object_specific_query(query):
        return "object_specific_missing"
    return "general"


def _answer_sections(
    *,
    query: str,
    scenario: str,
    status: str,
    included: tuple[dict[str, Any], ...],
    evidence_gaps: tuple[dict[str, Any], ...],
) -> tuple[dict[str, Any], ...]:
    if status == INSUFFICIENT_EVIDENCE_FOR_REHEARSAL:
        return _insufficient_evidence_sections(query, included, evidence_gaps)

    notes = {
        "retro_vs_current_adjustment": (
            (
                "Short explanation",
                "CONTROLLED_REHEARSAL_ONLY: after a ProcessPeriod finalisation lock, late source changes are not admitted back into finalisation-locked PayRuns. The controlled treatment rehearsal routes the correction to retro/off-cycle review rather than a current-period adjustment when historical attribution and audit lineage must be preserved.",
            ),
            (
                "Evidence basis",
                "The rehearsal relies on payroll correction workflow reasoning and its finalisation-lock, admission-boundary, finalised-payroll-immutability, and attribution-period distinction doctrines.",
            ),
            (
                "Why this treatment applies",
                "Retro/off-cycle treatment preserves the historical attribution period, the original relied-upon payroll truth, the corrected due truth, and the explicit delta treatment.",
            ),
            (
                "Why alternatives are not appropriate",
                "A current-period adjustment could obscure that the correction belongs to an earlier attribution period and could hide the source-change lineage that the correction review must preserve.",
            ),
        ),
        "supplementary_vs_dirty": (
            (
                "Short explanation",
                "CONTROLLED_REHEARSAL_ONLY: dirty reprocessing is appropriate only while the PayRunContact or calculation remains open and unrelied upon. Once the original PayRun or PayRunContact is finalised or relied upon, the rehearsal routes the change to supplementary review instead of overwriting the original outcome.",
            ),
            (
                "Evidence basis",
                "The rehearsal relies on payroll correction workflow reasoning for open calculation rebuild, finalised payroll immutability, and supplementary treatment boundaries.",
            ),
            (
                "Why this treatment applies",
                "Supplementary review can preserve the original finalised calculation identity while recording the delta created by the later source-truth change.",
            ),
            (
                "Why alternatives are not appropriate",
                "Dirty reprocessing would be inappropriate if it overwrites or silently rebuilds a finalised or relied-upon PayRunContact outcome.",
            ),
        ),
        "negative_delta_payment": (
            (
                "Short explanation",
                "CONTROLLED_REHEARSAL_ONLY: before banking or payment execution, a negative delta may be netted at the payment layer; after payment execution, the already-paid amount becomes historical paid truth and the negative delta routes to overpayment/recovery review.",
            ),
            (
                "Evidence basis",
                "The rehearsal relies on banking-netting, payment-batch lifecycle separation, and calculation-identity versus payment-aggregation reasoning.",
            ),
            (
                "Why this treatment applies",
                "Payment-layer netting can alter the money movement before execution without mutating calculation truth. After execution, recovery review is required because the original bank payment cannot be merged or rewritten.",
            ),
            (
                "Why alternatives are not appropriate",
                "Treating an executed bank payment as still nettable would collapse calculation identity, payment aggregation, and paid historical truth into one unsafe step.",
            ),
        ),
        "payment_date_year_end": (
            (
                "Short explanation",
                "CONTROLLED_REHEARSAL_ONLY: payment date matters at year end because work attribution and payment reporting period are distinct. Payment date controls reporting or tax-year timing unless a specific statutory rule says otherwise.",
            ),
            (
                "Evidence basis",
                "The rehearsal relies on payment-date reporting period reasoning and attribution-period-is-not-payment-period doctrine.",
            ),
            (
                "Why this treatment applies",
                "The work can belong to an earlier attribution period while the payment enters the bank in a later reporting or tax year.",
            ),
            (
                "Why alternatives are not appropriate",
                "Using work attribution alone as reporting timing would ignore the separate payment date evidence required for year-end treatment.",
            ),
        ),
        "general": (
            (
                "Short explanation",
                "CONTROLLED_REHEARSAL_ONLY: the provenance packet can be rehearsed only where supported claims and citation requirements exist.",
            ),
            (
                "Evidence basis",
                "The rehearsal relies only on claim-level provenance and controlled local evidence artefacts.",
            ),
            (
                "Why this treatment applies",
                "Supported claims can be previewed with caveats; unsupported and prohibited claims remain excluded.",
            ),
            (
                "Why alternatives are not appropriate",
                "The rehearsal cannot become a live chat response, final answer, runtime answer, or production-readiness claim.",
            ),
        ),
    }[scenario if scenario != "object_specific_missing" else "general"]

    common = (
        (
            "What has not happened",
            "No live runtime action, DB read/write, payment action, PAYG/STP/tax calculation, chat exposure, live LLM call, corpus mutation, Workforce integration, Analytics integration, deployment check, or production-readiness assertion has occurred.",
        ),
        (
            "Evidence gaps / next safe step",
            _gap_summary(evidence_gaps)
            or "Keep the rehearsal behind a later answer gate and preserve citation requirements.",
        ),
    )
    return tuple(
        _section(title, note, included)
        for title, note in (*notes, *common)
    )


def _insufficient_evidence_sections(
    query: str,
    included: tuple[dict[str, Any], ...],
    evidence_gaps: tuple[dict[str, Any], ...],
) -> tuple[dict[str, Any], ...]:
    sections = (
        (
            "What can be answered",
            "CONTROLLED_REHEARSAL_ONLY: the system can identify the evidence categories needed before a worker-specific or runtime-specific answer is safe.",
        ),
        (
            "What cannot be answered",
            "The rehearsal cannot say what happened to a specific worker's pay, what runtime object state exists, what DB records show, or what payment action occurred without object story/runtime evidence.",
        ),
        (
            "Additional evidence required",
            _gap_summary(evidence_gaps),
        ),
        (
            "Next safe step",
            "Provide authorised CorrectionReview object story, source-change, lifecycle, PayRun/PayRunContact, payment-window, payment-execution, and DB/runtime evidence before rehearsing object-specific explanation.",
        ),
    )
    return tuple(_section(title, note, included) for title, note in sections)


def _section(
    title: str,
    note: str,
    included: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    return {
        "SectionTitle": title,
        "Label": REHEARSAL_LABEL,
        "RehearsalNotes": note,
        "SupportedClaimIds": tuple(claim["ClaimId"] for claim in included),
        "FinalAnswerPermitted": False,
    }


def _included_claims(packet: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    return tuple(
        _claim_for_output(claim)
        for claim in packet.get("Claims", ()) or ()
        if claim.get("ClaimStatus") in SUPPORTED_STATUSES
    )


def _unsupported_claims(packet: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    unsupported = [
        _claim_for_output(claim)
        for claim in packet.get("Claims", ()) or ()
        if claim.get("ClaimStatus") in UNSUPPORTED_STATUSES
    ]
    unsupported.extend(_claim_for_output(claim) for claim in packet.get("UnsupportedClaims", ()) or ())
    unsupported.extend(
        _additional_evidence_claim(claim)
        for claim in packet.get("ClaimsRequiringAdditionalEvidence", ()) or ()
    )
    return tuple(_dedupe_claims(unsupported))


def _prohibited_claims(packet: dict[str, Any], query: str) -> tuple[dict[str, Any], ...]:
    prohibited = [
        _claim_for_output(claim)
        for claim in packet.get("Claims", ()) or ()
        if claim.get("ClaimStatus") == PROHIBITED
    ]
    prohibited.extend(_claim_for_output(claim) for claim in packet.get("ProhibitedClaims", ()) or ())
    if _asks_for_prohibited_overclaim(query):
        prohibited.append(
            {
                "ClaimId": "prohibited-live-or-production-overclaim",
                "ClaimText": "Live LLM, live chat, runtime answer, final answer, or production readiness can be claimed now.",
                "ClaimType": "PRODUCTION_OR_RUNTIME_OVERCLAIM",
                "ClaimStatus": PROHIBITED,
                "ProhibitedReason": "This slice prohibits live/runtime/final-answer/production-readiness claims.",
                "FinalAnswerEligible": False,
            }
        )
    return tuple(_dedupe_claims(prohibited))


def _ensure_scenario_claim(
    packet: dict[str, Any],
    included: tuple[dict[str, Any], ...],
    scenario: str,
) -> tuple[dict[str, Any], ...]:
    if scenario in {"general", "object_specific_missing"}:
        return included
    if any(claim.get("ClaimType") == OPERATOR_SCENARIO_REASONING for claim in included):
        return included

    payroll_evidence = tuple(
        item
        for item in packet.get("EvidenceInventory", ()) or ()
        if item.get("EvidenceType") == PAYROLL_CORRECTION_WORKFLOW_REASONING
    )
    if not payroll_evidence:
        return included

    scenario_text = {
        "retro_vs_current_adjustment": "Finalisation lock and attribution lineage can support retro/off-cycle review rather than current-period adjustment.",
        "supplementary_vs_dirty": "Finalised or relied-upon PayRunContact outcomes support supplementary review rather than dirty reprocessing.",
        "negative_delta_payment": "Payment execution state separates pre-banking netting from post-payment recovery review.",
        "payment_date_year_end": "Payment date can control reporting/tax-year timing separately from work attribution period.",
    }[scenario]
    claim = {
        "ClaimId": f"rehearsal-derived-{scenario.replace('_', '-')}",
        "ClaimText": scenario_text,
        "ClaimType": OPERATOR_SCENARIO_REASONING,
        "ClaimStatus": SUPPORTED_WITH_CAVEAT,
        "EvidenceRequired": (PAYROLL_CORRECTION_WORKFLOW_REASONING,),
        "EvidenceUsed": payroll_evidence,
        "EvidenceMissing": (),
        "SourceAuthoritySatisfied": True,
        "CitationRequirement": "Future answer must cite the payroll correction workflow reasoning artefact and/or Platform Doctrine evidence.",
        "CaveatRequirement": "Payroll reasoning evidence is curated scenario reasoning, not Workforce runtime proof.",
        "FinalAnswerEligible": False,
        "AdditionalEvidenceRequired": (),
    }
    return (*included, claim)


def _citation_plan(included: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "CitationPlanId": f"citation-plan-{claim['ClaimId']}",
            "ClaimId": claim["ClaimId"],
            "ClaimText": claim["ClaimText"],
            "ClaimType": claim.get("ClaimType", ""),
            "CitationRequirement": claim.get("CitationRequirement", ""),
            "EvidenceRequired": tuple(claim.get("EvidenceRequired", ()) or ()),
            "EvidenceToCite": tuple(claim.get("EvidenceUsed", ()) or ()),
            "FinalAnswerEligible": False,
        }
        for claim in included
    )


def _required_caveats(
    packet: dict[str, Any],
    scenario: str,
    evidence_gaps: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    caveats = [*BASE_CAVEATS]
    caveats.extend(str(item) for item in packet.get("CaveatRequirements", ()) or () if str(item))
    if scenario == "negative_delta_payment":
        caveats.append("Object-specific negative-delta treatment requires payment window and payment execution state.")
    if scenario == "payment_date_year_end":
        caveats.append("No PAYG/STP/tax calculation is performed in this rehearsal.")
    if evidence_gaps:
        caveats.append("Evidence gaps must be resolved before object-specific answer use.")
    return tuple(dict.fromkeys(caveats))


def _evidence_gaps(
    query: str,
    scenario: str,
    packet: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    gaps: list[dict[str, Any]] = []
    needs_object_evidence = scenario in {
        "retro_vs_current_adjustment",
        "supplementary_vs_dirty",
        "negative_delta_payment",
        "payment_date_year_end",
        "object_specific_missing",
    } or _object_specific_query(query)
    if needs_object_evidence and not _has_runtime_or_object_story_evidence(packet):
        gaps.extend(
            {
                "EvidenceGapId": _gap_id(name),
                "RequiredEvidence": name,
                "Reason": reason,
                "SupportedNow": False,
            }
            for name, reason in OBJECT_EVIDENCE_GAPS
        )
    if _asks_for_prohibited_overclaim(query):
        gaps.append(
            {
                "EvidenceGapId": "deployment-production-authorisation",
                "RequiredEvidence": "deployment/production evidence and explicit authorisation",
                "Reason": "Production readiness and live runtime claims are prohibited without separate authorised evidence.",
                "SupportedNow": False,
            }
        )
    return tuple(_dedupe_dicts(gaps))


def _rehearsal_status(
    *,
    packet: dict[str, Any],
    prohibited: tuple[dict[str, Any], ...],
    unsupported: tuple[dict[str, Any], ...],
    included: tuple[dict[str, Any], ...],
    evidence_gaps: tuple[dict[str, Any], ...],
    query: str,
    scenario: str,
) -> str:
    if prohibited or packet.get("PacketStatus") == BLOCKED_PROHIBITED_CLAIMS:
        return BLOCKED_PROHIBITED_CLAIMS
    if scenario == "object_specific_missing" or _object_specific_query(query):
        return INSUFFICIENT_EVIDENCE_FOR_REHEARSAL
    if not included:
        return INSUFFICIENT_EVIDENCE_FOR_REHEARSAL if unsupported else OUT_OF_SCOPE
    if evidence_gaps or unsupported or packet.get("PacketStatus") == PROVENANCE_READY_WITH_CAVEATS:
        return CONTROLLED_REHEARSAL_READY_WITH_CAVEATS
    if packet.get("PacketStatus") == PROVENANCE_READY:
        return CONTROLLED_REHEARSAL_READY
    return CONTROLLED_REHEARSAL_READY_WITH_CAVEATS


def _claim_for_output(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "ClaimId": str(claim.get("ClaimId") or _gap_id(str(claim.get("ClaimText") or "claim"))),
        "ClaimText": str(claim.get("ClaimText") or claim.get("RequiredEvidence") or ""),
        "ClaimType": str(claim.get("ClaimType") or ""),
        "ClaimStatus": str(claim.get("ClaimStatus") or ""),
        "EvidenceRequired": tuple(claim.get("EvidenceRequired", ()) or ()),
        "EvidenceUsed": tuple(claim.get("EvidenceUsed", ()) or ()),
        "EvidenceMissing": tuple(claim.get("EvidenceMissing", ()) or ()),
        "CitationRequirement": str(claim.get("CitationRequirement") or ""),
        "CaveatRequirement": str(claim.get("CaveatRequirement") or ""),
        "UnsupportedReason": str(claim.get("UnsupportedReason") or claim.get("Reason") or ""),
        "ProhibitedReason": str(claim.get("ProhibitedReason") or ""),
        "FinalAnswerEligible": False,
    }


def _additional_evidence_claim(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "ClaimId": str(claim.get("ClaimId") or _gap_id(str(claim.get("ClaimText") or "additional-evidence"))),
        "ClaimText": str(claim.get("ClaimText") or ""),
        "ClaimType": str(claim.get("ClaimType") or "ADDITIONAL_EVIDENCE_REQUIRED"),
        "ClaimStatus": str(claim.get("ClaimStatus") or "UNSUPPORTED"),
        "RequiredEvidence": tuple(claim.get("RequiredEvidence", ()) or ()),
        "MissingEvidence": tuple(claim.get("MissingEvidence", ()) or ()),
        "FinalAnswerEligible": False,
    }


def _normalize_rehearsal_mode(rehearsal_mode: str, query: str, scenario: str) -> str:
    requested = str(rehearsal_mode or "").strip().upper()
    valid = {
        WHY_EXPLANATION,
        TREATMENT_EXPLANATION,
        STATUS_EXPLANATION,
        EVIDENCE_GAP_EXPLANATION,
        GENERAL_CONTROLLED_REHEARSAL,
    }
    if requested in valid and requested != GENERAL_CONTROLLED_REHEARSAL:
        return requested
    if scenario == "object_specific_missing":
        return EVIDENCE_GAP_EXPLANATION
    if scenario in {
        "retro_vs_current_adjustment",
        "supplementary_vs_dirty",
        "negative_delta_payment",
        "payment_date_year_end",
    }:
        return WHY_EXPLANATION if query.strip().lower().startswith("why") else TREATMENT_EXPLANATION
    return GENERAL_CONTROLLED_REHEARSAL


def _normalize_audience(audience: str) -> str:
    requested = str(audience or "").strip().upper().replace("-", "_").replace(" ", "_")
    return requested or PAYROLL_OPERATOR


def _object_specific_query(query: str) -> bool:
    normalized = _normalize(query)
    return any(
        marker in normalized
        for marker in (
            "this worker",
            "worker's pay",
            "workers pay",
            "this pay",
            "what happened to",
            "correctionreviewid",
            "correction review id",
        )
    )


def _asks_for_prohibited_overclaim(query: str) -> bool:
    normalized = _normalize(query)
    return any(
        marker in normalized
        for marker in (
            "production-ready",
            "production ready",
            "production readiness",
            "live chat",
            "live llm",
            "runtime answer",
            "runtime integration is active",
            "final answer",
        )
    ) and any(verb in normalized for verb in ("say", "claim", "state", "assert", "prove", "ready", "live"))


def _has_runtime_or_object_story_evidence(packet: dict[str, Any]) -> bool:
    haystack = " ".join(
        " ".join(str(value) for value in item.values())
        for item in packet.get("EvidenceInventory", ()) or ()
        if isinstance(item, dict)
    ).lower()
    return any(
        marker in haystack
        for marker in (
            "runtime_evidence",
            "db_evidence",
            "correctionreview",
            "object story",
            "payruncontact state",
            "payment execution state",
        )
    )


def _gap_summary(evidence_gaps: tuple[dict[str, Any], ...]) -> str:
    if not evidence_gaps:
        return ""
    return "Required before object-specific use: " + ", ".join(
        gap["RequiredEvidence"] for gap in evidence_gaps
    ) + "."


def _boundary_flags() -> dict[str, bool]:
    flags = dict(BOUNDARY_FLAGS)
    flags["ControlledRehearsalOnly"] = True
    flags["FinalAnswerGenerated"] = False
    return flags


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").lower().replace("-", " ")).strip()


def _gap_id(value: str) -> str:
    normalized = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    return normalized[:80] or "unknown"


def _dedupe_claims(items: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    return tuple(_dedupe_dicts(items))


def _dedupe_dicts(items: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = tuple(sorted((str(key), str(value)) for key, value in item.items()))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return tuple(unique)

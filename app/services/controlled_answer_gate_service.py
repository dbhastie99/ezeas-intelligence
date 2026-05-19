import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from app.services.controlled_answer_rehearsal_service import (
    BLOCKED_PROHIBITED_CLAIMS as REHEARSAL_BLOCKED_PROHIBITED_CLAIMS,
    OUT_OF_SCOPE as REHEARSAL_OUT_OF_SCOPE,
    build_controlled_answer_rehearsal,
)
from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)


CONTROLLED_TEST_ONLY = "CONTROLLED_TEST_ONLY"
INTERNAL_PREVIEW = "INTERNAL_PREVIEW"
ADMIN_QUEUE_ASSISTANT_DRAFT = "ADMIN_QUEUE_ASSISTANT_DRAFT"
LIVE_OPERATOR_RESPONSE = "LIVE_OPERATOR_RESPONSE"

EXPOSURE_MODES = {
    CONTROLLED_TEST_ONLY,
    INTERNAL_PREVIEW,
    ADMIN_QUEUE_ASSISTANT_DRAFT,
    LIVE_OPERATOR_RESPONSE,
}

SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL = "SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL"
SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW = "SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW"
BLOCKED_PROHIBITED_CLAIMS = "BLOCKED_PROHIBITED_CLAIMS"
BLOCKED_INSUFFICIENT_EVIDENCE = "BLOCKED_INSUFFICIENT_EVIDENCE"
BLOCKED_OBJECT_EVIDENCE_REQUIRED = "BLOCKED_OBJECT_EVIDENCE_REQUIRED"
BLOCKED_RUNTIME_EVIDENCE_REQUIRED = "BLOCKED_RUNTIME_EVIDENCE_REQUIRED"
BLOCKED_DB_EVIDENCE_REQUIRED = "BLOCKED_DB_EVIDENCE_REQUIRED"
BLOCKED_DEPLOYMENT_EVIDENCE_REQUIRED = "BLOCKED_DEPLOYMENT_EVIDENCE_REQUIRED"
BLOCKED_PRODUCTION_CLAIM = "BLOCKED_PRODUCTION_CLAIM"
BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED = "BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

GREEN = "GREEN"
AMBER = "AMBER"
RED = "RED"

FINAL_ANSWER_DISABLED_REASON = (
    "Final answer generation remains disabled in this slice. The gate records "
    "controlled exposure eligibility only and does not display an answer."
)

CONTROLLED_REASONING_CAVEAT = (
    "This is a controlled reasoning explanation, not a live operational determination."
)
OBJECT_EVIDENCE_CAVEAT = (
    "Specific treatment requires object-level CorrectionReview and payment-window evidence."
)

BOUNDARY_TRUE_FLAGS = (
    "LiveLLMCalled",
    "FinalAnswerGenerated",
    "ChatExposureEnabled",
    "DatabaseReadPerformed",
    "DatabaseWritePerformed",
    "RuntimeIntegrationPerformed",
    "ProductionReadinessClaimed",
)

FALSE_BOUNDARY_FLAGS = (
    "LiveLLMCalled",
    "FinalAnswerGenerated",
    "ChatExposureEnabled",
    "DatabaseReadPerformed",
    "DatabaseWritePerformed",
    "LiveCorpusMutationPerformed",
    "CodeEvidenceIngestionPerformed",
    "RuntimeIntegrationPerformed",
    "ProductionReadinessClaimed",
    "AnswerDisplayed",
    "PersistedToDb",
)

NEXT_STEP_BY_STATUS = {
    SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL: (
        "Keep this result in controlled test-only rehearsal. Do not expose it as "
        "an internal preview, Admin Queue draft, live response, or final answer."
    ),
    SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW: (
        "Internal preview may inspect the caveated rehearsal, but object-specific "
        "and live answer use still require authorised object story/runtime evidence."
    ),
    BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED: (
        "Do not display or route this answer. Live operator response is not "
        "authorised in this slice."
    ),
}


@dataclass(frozen=True)
class ControlledAnswerGateDecision:
    QueryText: str
    RequestedExposureMode: str
    GateStatus: str
    GateSeverity: str
    AllowedExposureMode: str | None
    BlockedExposureModes: tuple[str, ...]
    RequiredCaveats: tuple[str, ...]
    MissingEvidence: tuple[dict[str, Any], ...]
    BlockedClaims: tuple[dict[str, Any], ...]
    AllowedClaims: tuple[dict[str, Any], ...]
    Warnings: tuple[str, ...]
    GateReasons: tuple[str, ...]
    FinalAnswerPermitted: bool
    ControlledRehearsalOnly: bool
    PersistableAuditPacket: dict[str, Any]
    BoundaryFlags: dict[str, bool]
    NextStep: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ControlledAnswerGateService:
    """Deterministic safety gate for controlled answer rehearsals."""

    def evaluate_gate(
        self,
        query_text: str,
        controlled_answer_rehearsal_envelope: dict[str, Any] | None = None,
        requested_exposure_mode: str = CONTROLLED_TEST_ONLY,
        object_evidence_available: bool = False,
        runtime_evidence_available: bool = False,
        db_evidence_available: bool = False,
        deployment_evidence_available: bool = False,
        production_evidence_available: bool = False,
    ) -> dict[str, Any]:
        return evaluate_controlled_answer_gate(
            query_text=query_text,
            controlled_answer_rehearsal_envelope=controlled_answer_rehearsal_envelope,
            requested_exposure_mode=requested_exposure_mode,
            object_evidence_available=object_evidence_available,
            runtime_evidence_available=runtime_evidence_available,
            db_evidence_available=db_evidence_available,
            deployment_evidence_available=deployment_evidence_available,
            production_evidence_available=production_evidence_available,
        )


def evaluate_controlled_answer_gate(
    query_text: str,
    controlled_answer_rehearsal_envelope: dict[str, Any] | None = None,
    requested_exposure_mode: str = CONTROLLED_TEST_ONLY,
    object_evidence_available: bool = False,
    runtime_evidence_available: bool = False,
    db_evidence_available: bool = False,
    deployment_evidence_available: bool = False,
    production_evidence_available: bool = False,
) -> dict[str, Any]:
    """Evaluate controlled rehearsal exposure without producing or displaying an answer."""

    query = str(query_text or "")
    requested = _normalize_exposure_mode(requested_exposure_mode)
    rehearsal = controlled_answer_rehearsal_envelope or build_controlled_answer_rehearsal(query)
    text = _combined_text(query, rehearsal)
    claim_text = _claim_detection_text(query, rehearsal)

    explicit_object_evidence = object_evidence_available or _has_object_evidence(rehearsal)
    explicit_runtime_evidence = runtime_evidence_available or _has_evidence_type(rehearsal, "RUNTIME_EVIDENCE")
    explicit_db_evidence = db_evidence_available or _has_evidence_type(rehearsal, "DB_EVIDENCE")
    explicit_deployment_evidence = deployment_evidence_available or _has_evidence_type(
        rehearsal, "DEPLOYMENT_EVIDENCE"
    )
    explicit_production_evidence = production_evidence_available or _has_evidence_type(
        rehearsal, "PRODUCTION_EVIDENCE"
    )

    required_caveats = _required_caveats(rehearsal, text, explicit_object_evidence)
    missing_evidence = list(_missing_evidence_from_rehearsal(rehearsal))
    blocked_claims = list(_blocked_claims_from_rehearsal(rehearsal))
    allowed_claims = _allowed_claims_from_rehearsal(rehearsal)
    warnings = list(_warnings(rehearsal, text))
    reasons: list[str] = []

    if requested not in EXPOSURE_MODES:
        status = OUT_OF_SCOPE
        reasons.append(f"Requested exposure mode is out of scope: {requested}.")
    elif requested == LIVE_OPERATOR_RESPONSE:
        status = BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED
        reasons.append("Live operator response is not authorised for this slice.")
    else:
        status = _blocking_status(
            requested=requested,
            rehearsal=rehearsal,
            text=claim_text,
            caveat_text=text,
            object_evidence_available=explicit_object_evidence,
            runtime_evidence_available=explicit_runtime_evidence,
            db_evidence_available=explicit_db_evidence,
            deployment_evidence_available=explicit_deployment_evidence,
            production_evidence_available=explicit_production_evidence,
            required_caveats=required_caveats,
            missing_evidence=missing_evidence,
            blocked_claims=blocked_claims,
            reasons=reasons,
        )

    if status in {SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL, SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW}:
        reasons.extend(_safe_reasons(status, requested, rehearsal))

    if _has_boundary_violations(rehearsal):
        blocked_claims.extend(_boundary_violation_claims(rehearsal))
        warnings.append("One or more rehearsal boundary flags were dirty.")
        if status in {SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL, SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW}:
            status = BLOCKED_PROHIBITED_CLAIMS
            reasons.append("Dirty rehearsal boundary flags block exposure.")

    blocked_claims_tuple = tuple(_dedupe_dicts(blocked_claims))
    missing_evidence_tuple = tuple(_dedupe_dicts(missing_evidence))
    reasons_tuple = tuple(dict.fromkeys(reason for reason in reasons if reason))
    caveats_tuple = tuple(dict.fromkeys(required_caveats))
    warnings_tuple = tuple(dict.fromkeys(warning for warning in warnings if warning))

    boundary_flags = _boundary_flags()
    audit_packet = _audit_packet(
        query=query,
        status=status,
        reasons=reasons_tuple,
        rehearsal=rehearsal,
        missing_evidence=missing_evidence_tuple,
        blocked_claims=blocked_claims_tuple,
        required_caveats=caveats_tuple,
    )

    return ControlledAnswerGateDecision(
        QueryText=query,
        RequestedExposureMode=requested,
        GateStatus=status,
        GateSeverity=_severity(status),
        AllowedExposureMode=_allowed_exposure_mode(status, requested),
        BlockedExposureModes=_blocked_exposure_modes(status, requested),
        RequiredCaveats=caveats_tuple,
        MissingEvidence=missing_evidence_tuple,
        BlockedClaims=blocked_claims_tuple,
        AllowedClaims=allowed_claims,
        Warnings=warnings_tuple,
        GateReasons=reasons_tuple,
        FinalAnswerPermitted=False,
        ControlledRehearsalOnly=True,
        PersistableAuditPacket=audit_packet,
        BoundaryFlags=boundary_flags,
        NextStep=_next_step(status),
    ).to_dict()


def _blocking_status(
    *,
    requested: str,
    rehearsal: dict[str, Any],
    text: str,
    caveat_text: str,
    object_evidence_available: bool,
    runtime_evidence_available: bool,
    db_evidence_available: bool,
    deployment_evidence_available: bool,
    production_evidence_available: bool,
    required_caveats: tuple[str, ...],
    missing_evidence: list[dict[str, Any]],
    blocked_claims: list[dict[str, Any]],
    reasons: list[str],
) -> str:
    if _has_boundary_violations(rehearsal):
        reasons.append("Rehearsal boundary flags must be clean before any exposure.")
        return BLOCKED_PROHIBITED_CLAIMS

    if _has_production_claim(text) and not production_evidence_available:
        missing_evidence.append(_missing("ProductionEvidence", "Production-readiness claim requires authorised production evidence."))
        reasons.append("Production-readiness claims are blocked without explicit evidence and authorisation.")
        return BLOCKED_PRODUCTION_CLAIM

    if _has_db_claim(text, rehearsal) and not db_evidence_available:
        missing_evidence.append(_missing("DbEvidence", "DB state claim requires authorised DB evidence."))
        reasons.append("DB state claims are blocked without authorised DB evidence.")
        return BLOCKED_DB_EVIDENCE_REQUIRED

    if _has_runtime_claim(text, rehearsal) and not runtime_evidence_available:
        missing_evidence.append(_missing("RuntimeEvidence", "Runtime state claim requires authorised runtime evidence."))
        reasons.append("Runtime state claims are blocked without authorised runtime evidence.")
        return BLOCKED_RUNTIME_EVIDENCE_REQUIRED

    if _has_deployment_claim(text, rehearsal) and not deployment_evidence_available:
        missing_evidence.append(_missing("DeploymentEvidence", "Deployment claim requires authorised deployment evidence."))
        reasons.append("Deployment claims are blocked without authorised deployment evidence.")
        return BLOCKED_DEPLOYMENT_EVIDENCE_REQUIRED

    if _has_prohibited_claims(rehearsal, text):
        if not blocked_claims:
            blocked_claims.append(
                {
                    "ClaimId": "blocked-prohibited-overclaim",
                    "ClaimText": "Live/runtime/final-answer/payment/production overclaim detected.",
                    "ClaimType": "PROHIBITED_OVERCLAIM",
                    "ClaimStatus": "PROHIBITED",
                    "FinalAnswerEligible": False,
                }
            )
        reasons.append("Prohibited claims block exposure.")
        return BLOCKED_PROHIBITED_CLAIMS

    if requested == ADMIN_QUEUE_ASSISTANT_DRAFT:
        reasons.append("Admin Queue assistant draft exposure is a future slice and is blocked here.")
        return BLOCKED_INSUFFICIENT_EVIDENCE

    if _specific_object_question(text) and not object_evidence_available:
        missing_evidence.extend(_object_missing_evidence())
        reasons.append("Object-specific answer requires object-level CorrectionReview/payment evidence.")
        return BLOCKED_OBJECT_EVIDENCE_REQUIRED

    supplied_caveats = tuple(str(item) for item in _as_tuple(rehearsal.get("RequiredCaveats")) if str(item))
    if _requires_caveats(caveat_text, rehearsal, object_evidence_available) and not _has_required_caveat_text(supplied_caveats):
        missing_evidence.append(
            _missing(
                "RequiredCaveats",
                "Controlled reasoning and object-evidence caveats are required before preview.",
            )
        )
        reasons.append("Required caveats are missing for controlled reasoning preview.")
        return BLOCKED_INSUFFICIENT_EVIDENCE

    if rehearsal.get("RehearsalStatus") == REHEARSAL_OUT_OF_SCOPE:
        reasons.append("The rehearsal is out of scope.")
        return OUT_OF_SCOPE

    if requested == INTERNAL_PREVIEW:
        reasons.append("Internal preview is allowed only with caveats and no final answer permission.")
        return SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW

    if _requires_caveats(caveat_text, rehearsal, object_evidence_available):
        reasons.append("Controlled test-only rehearsal is safe only with preserved caveats.")
        return SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW

    return SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL


def _normalize_exposure_mode(value: str) -> str:
    return str(value or "").strip().upper().replace("-", "_").replace(" ", "_")


def _required_caveats(
    rehearsal: dict[str, Any],
    text: str,
    object_evidence_available: bool,
) -> tuple[str, ...]:
    caveats = [str(item) for item in _as_tuple(rehearsal.get("RequiredCaveats")) if str(item)]
    if _requires_caveats(text, rehearsal, object_evidence_available):
        caveats.extend((CONTROLLED_REASONING_CAVEAT, OBJECT_EVIDENCE_CAVEAT))
    return tuple(dict.fromkeys(caveats))


def _requires_caveats(text: str, rehearsal: dict[str, Any], object_evidence_available: bool) -> bool:
    if object_evidence_available:
        return False
    if rehearsal.get("EvidenceGaps"):
        return True
    if "OPERATOR_SCENARIO_REASONING" in _claim_types(rehearsal):
        return True
    return any(
        marker in _normalize(text)
        for marker in (
            "retro",
            "off cycle",
            "off-cycle",
            "supplementary",
            "dirty reprocessing",
            "negative delta",
            "payment window",
            "correctionreview",
        )
    )


def _has_required_caveat_text(caveats: tuple[str, ...]) -> bool:
    text = _normalize(" ".join(caveats))
    has_controlled_boundary = "controlled" in text and (
        "not final" in text
        or "not live" in text
        or "not runtime" in text
        or "not workforce runtime proof" in text
        or "not a live operational determination" in text
    )
    has_object_boundary = (
        "object specific" in text
        or "object level" in text
        or "object story" in text
        or "correctionreview" in text
    ) and ("payment window" in text or "runtime" in text or "object story" in text)
    return has_controlled_boundary and has_object_boundary


def _has_boundary_violations(rehearsal: dict[str, Any]) -> bool:
    flags = rehearsal.get("BoundaryFlags", {}) or {}
    return any(bool(flags.get(flag)) for flag in BOUNDARY_TRUE_FLAGS)


def _boundary_violation_claims(rehearsal: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    flags = rehearsal.get("BoundaryFlags", {}) or {}
    return tuple(
        {
            "ClaimId": f"boundary-flag-{_slug(flag)}",
            "ClaimText": f"Boundary flag {flag} was true in the rehearsal envelope.",
            "ClaimType": "BOUNDARY_FLAG_VIOLATION",
            "ClaimStatus": "PROHIBITED",
            "FinalAnswerEligible": False,
        }
        for flag in BOUNDARY_TRUE_FLAGS
        if bool(flags.get(flag))
    )


def _has_prohibited_claims(rehearsal: dict[str, Any], text: str) -> bool:
    if rehearsal.get("RehearsalStatus") == REHEARSAL_BLOCKED_PROHIBITED_CLAIMS:
        return True
    if _has_prohibited_text(text):
        return True
    return any(
        str(claim.get("ClaimStatus", "")).upper() == "PROHIBITED"
        for claim in _all_claims(rehearsal)
    )


def _has_prohibited_text(text: str) -> bool:
    normalized = _normalize(text)
    prohibited_markers = (
        "live chat is enabled",
        "live chat uses",
        "live llm was called",
        "live llm",
        "payment was executed",
        "payment executed",
        "final answer generated",
        "final answer can be displayed",
        "database read was performed",
        "db state was checked",
        "production deployment is active",
        "production ready",
        "production-ready",
    )
    return any(marker in normalized for marker in prohibited_markers)


def _has_db_claim(text: str, rehearsal: dict[str, Any]) -> bool:
    normalized = _normalize(text)
    return "DB_STATE" in _claim_types(rehearsal) or any(
        marker in normalized
        for marker in (
            "current live db state",
            "database state",
            "db state",
            "db records show",
            "database records show",
            "database read",
        )
    )


def _has_runtime_claim(text: str, rehearsal: dict[str, Any]) -> bool:
    normalized = _normalize(text)
    return "RUNTIME_STATE" in _claim_types(rehearsal) or any(
        marker in normalized
        for marker in (
            "runtime state",
            "current runtime",
            "runtime integration is active",
            "runtime object state",
            "workforce runtime",
        )
    )


def _has_deployment_claim(text: str, rehearsal: dict[str, Any]) -> bool:
    normalized = _normalize(text)
    return "DEPLOYMENT_STATE" in _claim_types(rehearsal) or any(
        marker in normalized for marker in ("deployment state", "deployment is active", "deployed")
    )


def _has_production_claim(text: str) -> bool:
    normalized = _normalize(text)
    return any(
        marker in normalized
        for marker in (
            "production readiness",
            "production ready",
            "production-ready",
            "production deployment",
        )
    )


def _specific_object_question(text: str) -> bool:
    normalized = _normalize(text)
    return any(
        marker in normalized
        for marker in (
            "what happened to this worker",
            "this worker's pay",
            "this workers pay",
            "what happened to this pay",
            "what happened to this payruncontact",
            "what changed on this objecttime",
            "is this worker ready to be paid",
            "this specific worker",
            "specific worker's review item",
            "specific workers review item",
            "correctionreviewid",
            "correction review id",
        )
    )


def _missing_evidence_from_rehearsal(rehearsal: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    gaps: list[dict[str, Any]] = []
    for gap in _as_tuple(rehearsal.get("EvidenceGaps")):
        if not isinstance(gap, dict):
            continue
        gaps.append(
            {
                "EvidenceType": str(gap.get("RequiredEvidence") or gap.get("EvidenceType") or "UnknownEvidence"),
                "Reason": str(gap.get("Reason") or "Required by controlled answer rehearsal."),
                "SupportedNow": bool(gap.get("SupportedNow", False)),
            }
        )
    return tuple(_dedupe_dicts(gaps))


def _object_missing_evidence() -> tuple[dict[str, Any], ...]:
    return (
        _missing("CorrectionReviewObjectStory", "Object-level CorrectionReview story is required."),
        _missing("SourceChangeSummary", "Source change summary is required."),
        _missing("PayrollImpactSummary", "Payroll impact summary is required."),
        _missing("ProcessPeriodLifecycleStatus", "Process period lifecycle status is required."),
        _missing("PaymentWindowStatus", "Payment window status is required."),
        _missing("ActionsTakenActionsNotTaken", "Actions taken/not taken evidence is required."),
    )


def _missing(evidence_type: str, reason: str) -> dict[str, Any]:
    return {
        "EvidenceType": evidence_type,
        "Reason": reason,
        "SupportedNow": False,
    }


def _blocked_claims_from_rehearsal(rehearsal: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    claims = []
    for claim in _all_claims(rehearsal):
        status = str(claim.get("ClaimStatus", "")).upper()
        if status in {
            "PROHIBITED",
            "REQUIRES_CURRENT_RUNTIME_EVIDENCE",
            "REQUIRES_DB_EVIDENCE",
            "REQUIRES_DEPLOYMENT_EVIDENCE",
            "REQUIRES_PRODUCTION_EVIDENCE",
            "UNSUPPORTED",
        }:
            claims.append(_claim_output(claim))
    return tuple(_dedupe_dicts(claims))


def _allowed_claims_from_rehearsal(rehearsal: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    claims = []
    for claim in _as_tuple(rehearsal.get("ClaimsIncluded")):
        if isinstance(claim, dict):
            claims.append(_claim_output(claim))
    return tuple(_dedupe_dicts(claims))


def _claim_output(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "ClaimId": str(claim.get("ClaimId") or _slug(str(claim.get("ClaimText") or "claim"))),
        "ClaimText": str(claim.get("ClaimText") or ""),
        "ClaimType": str(claim.get("ClaimType") or ""),
        "ClaimStatus": str(claim.get("ClaimStatus") or ""),
        "FinalAnswerEligible": False,
    }


def _all_claims(rehearsal: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    claims: list[dict[str, Any]] = []
    for key in (
        "ClaimsIncluded",
        "ClaimsExcluded",
        "ProhibitedClaimsExcluded",
        "UnsupportedClaimsExcluded",
    ):
        for claim in _as_tuple(rehearsal.get(key)):
            if isinstance(claim, dict):
                claims.append(claim)
    return tuple(claims)


def _claim_types(rehearsal: dict[str, Any]) -> set[str]:
    return {str(claim.get("ClaimType", "")).upper() for claim in _all_claims(rehearsal)}


def _warnings(rehearsal: dict[str, Any], text: str) -> tuple[str, ...]:
    warnings = [FINAL_ANSWER_DISABLED_REASON]
    if rehearsal.get("EvidenceGaps"):
        warnings.append("The rehearsal includes evidence gaps that must be resolved before object-specific use.")
    if _has_prohibited_text(text):
        warnings.append("The rehearsal text or query includes live/runtime/production overclaim markers.")
    return tuple(warnings)


def _safe_reasons(status: str, requested: str, rehearsal: dict[str, Any]) -> tuple[str, ...]:
    if status == SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL:
        return (
            "Requested exposure is controlled test-only.",
            "No prohibited claim or dirty boundary flag was detected.",
            "Final answer remains disabled.",
        )
    reasons = [
        "Requested exposure is internal preview only.",
        "Required caveats are preserved.",
        "Final answer remains disabled.",
    ]
    if rehearsal.get("EvidenceGaps"):
        reasons.append("Evidence gaps are carried forward as caveats and missing evidence.")
    return tuple(reasons)


def _severity(status: str) -> str:
    if status == SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL:
        return GREEN
    if status == SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW:
        return AMBER
    return RED


def _allowed_exposure_mode(status: str, requested: str) -> str | None:
    if status == SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL:
        return CONTROLLED_TEST_ONLY
    if status == SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW:
        return INTERNAL_PREVIEW if requested == INTERNAL_PREVIEW else CONTROLLED_TEST_ONLY
    return None


def _blocked_exposure_modes(status: str, requested: str) -> tuple[str, ...]:
    if status == SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL:
        return (INTERNAL_PREVIEW, ADMIN_QUEUE_ASSISTANT_DRAFT, LIVE_OPERATOR_RESPONSE)
    if status == SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW:
        return (ADMIN_QUEUE_ASSISTANT_DRAFT, LIVE_OPERATOR_RESPONSE)
    blocked = [mode for mode in EXPOSURE_MODES if mode != CONTROLLED_TEST_ONLY]
    if requested == CONTROLLED_TEST_ONLY:
        blocked.append(CONTROLLED_TEST_ONLY)
    return tuple(dict.fromkeys(blocked))


def _next_step(status: str) -> str:
    return NEXT_STEP_BY_STATUS.get(
        status,
        "Do not expose this answer. Resolve the gate reasons and rerun a later authorised gate slice.",
    )


def _boundary_flags() -> dict[str, bool]:
    flags = dict(BOUNDARY_FLAGS)
    for flag in FALSE_BOUNDARY_FLAGS:
        flags[flag] = False
    flags["ControlledRehearsalOnly"] = True
    return flags


def _audit_packet(
    *,
    query: str,
    status: str,
    reasons: tuple[str, ...],
    rehearsal: dict[str, Any],
    missing_evidence: tuple[dict[str, Any], ...],
    blocked_claims: tuple[dict[str, Any], ...],
    required_caveats: tuple[str, ...],
) -> dict[str, Any]:
    question_hash = hashlib.sha256(query.encode("utf-8")).hexdigest()
    return {
        "AnswerAttemptId": f"preview-{question_hash[:12]}",
        "QuestionHash": question_hash,
        "QueryText": query,
        "GateDecisionCode": status,
        "GateReasons": reasons,
        "EvidenceReferenceIds": _evidence_reference_ids(rehearsal),
        "MissingEvidence": missing_evidence,
        "BlockedClaims": blocked_claims,
        "RequiredCaveats": required_caveats,
        "FinalAnswerPermitted": False,
        "AnswerDisplayed": False,
        "PersistableAuditPacketReady": True,
    }


def _evidence_reference_ids(rehearsal: dict[str, Any]) -> tuple[str, ...]:
    ids: list[str] = []
    for item in _iter_evidence_items(rehearsal):
        if not isinstance(item, dict):
            continue
        reference = (
            item.get("EvidenceReferenceId")
            or item.get("ReferenceId")
            or item.get("RecordId")
            or item.get("EvidenceId")
            or item.get("SourceId")
            or item.get("SourceTitle")
            or item.get("EvidenceType")
        )
        if reference:
            ids.append(str(reference))
    return tuple(dict.fromkeys(ids))


def _iter_evidence_items(rehearsal: dict[str, Any]) -> Iterable[Any]:
    for key in ("EvidenceInventory", "EvidenceUsed"):
        for item in _as_tuple(rehearsal.get(key)):
            yield item
    for claim in _all_claims(rehearsal):
        for key in ("EvidenceUsed", "EvidenceReferences", "EvidenceToCite"):
            for item in _as_tuple(claim.get(key)):
                yield item
    for plan in _as_tuple(rehearsal.get("CitationPlan")):
        if not isinstance(plan, dict):
            continue
        for item in _as_tuple(plan.get("EvidenceToCite")):
            yield item


def _has_evidence_type(rehearsal: dict[str, Any], evidence_type: str) -> bool:
    expected = evidence_type.upper()
    return any(
        isinstance(item, dict) and str(item.get("EvidenceType", "")).upper() == expected
        for item in _iter_evidence_items(rehearsal)
    )


def _has_object_evidence(rehearsal: dict[str, Any]) -> bool:
    haystack = _normalize(
        " ".join(str(item) for item in _iter_evidence_items(rehearsal))
    )
    return any(
        marker in haystack
        for marker in (
            "correctionreview",
            "object story",
            "sourcechangesummary",
            "payrollimpactsummary",
            "processperiodlifecyclestatus",
            "paymentwindowstatus",
            "actionstaken",
        )
    )


def _combined_text(query: str, rehearsal: dict[str, Any]) -> str:
    parts = [query]
    for key in (
        "RehearsalStatus",
        "ControlledAnswerDraft",
        "AnswerSections",
        "ClaimsIncluded",
        "ClaimsExcluded",
        "RequiredCaveats",
        "EvidenceGaps",
        "ProhibitedClaimsExcluded",
        "UnsupportedClaimsExcluded",
        "BoundaryFlags",
    ):
        parts.append(str(rehearsal.get(key, "")))
    return " ".join(parts)


def _claim_detection_text(query: str, rehearsal: dict[str, Any]) -> str:
    parts = [query, str(rehearsal.get("RehearsalStatus", ""))]
    for claim in _all_claims(rehearsal):
        parts.append(str(claim.get("ClaimText", "")))
        parts.append(str(claim.get("ClaimType", "")))
        parts.append(str(claim.get("ClaimStatus", "")))
        parts.append(str(claim.get("ProhibitedReason", "")))
        parts.append(str(claim.get("UnsupportedReason", "")))
    flags = rehearsal.get("BoundaryFlags", {}) or {}
    for flag in BOUNDARY_TRUE_FLAGS:
        if bool(flags.get(flag)):
            parts.append(flag)
    return " ".join(parts)


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    return (value,)


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").lower().replace("-", " ")).strip()


def _slug(value: str) -> str:
    normalized = "".join(char.lower() if char.isalnum() else "-" for char in value).strip("-")
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    return normalized[:80] or "unknown"


def _dedupe_dicts(items: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = tuple(sorted((str(key), str(value)) for key, value in item.items()))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return tuple(unique)


def build_controlled_answer_gate_decision(
    query_text: str,
    controlled_answer_rehearsal_envelope: dict[str, Any] | None = None,
    requested_exposure_mode: str = CONTROLLED_TEST_ONLY,
    object_evidence_available: bool = False,
    runtime_evidence_available: bool = False,
    db_evidence_available: bool = False,
    deployment_evidence_available: bool = False,
    production_evidence_available: bool = False,
) -> dict[str, Any]:
    return evaluate_controlled_answer_gate(
        query_text=query_text,
        controlled_answer_rehearsal_envelope=controlled_answer_rehearsal_envelope,
        requested_exposure_mode=requested_exposure_mode,
        object_evidence_available=object_evidence_available,
        runtime_evidence_available=runtime_evidence_available,
        db_evidence_available=db_evidence_available,
        deployment_evidence_available=deployment_evidence_available,
        production_evidence_available=production_evidence_available,
    )

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)
from app.services.controlled_multi_source_answer_preparation_service import (
    build_controlled_multi_source_answer_preparation,
)
from app.services.controlled_multi_source_evidence_retrieval_service import (
    DEVELOPER_LOG,
    HARDENING_LOG,
    PLATFORM_DOCTRINE,
)


PROVENANCE_MODE = "DETERMINISTIC_CITATION_PROVENANCE_PACKET_V0_1"
PROVENANCE_UNIVERSE = "CONTROLLED_MULTI_SOURCE_ANSWER_PREPARATION_OUTPUT_V0_1"

PROVENANCE_READY = "PROVENANCE_READY"
PROVENANCE_READY_WITH_CAVEATS = "PROVENANCE_READY_WITH_CAVEATS"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
BLOCKED_PROHIBITED_CLAIMS = "BLOCKED_PROHIBITED_CLAIMS"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

SUPPORTED = "SUPPORTED"
SUPPORTED_WITH_CAVEAT = "SUPPORTED_WITH_CAVEAT"
UNSUPPORTED = "UNSUPPORTED"
PROHIBITED = "PROHIBITED"
REQUIRES_CURRENT_RUNTIME_EVIDENCE = "REQUIRES_CURRENT_RUNTIME_EVIDENCE"
REQUIRES_CODE_EVIDENCE = "REQUIRES_CODE_EVIDENCE"
REQUIRES_DB_EVIDENCE = "REQUIRES_DB_EVIDENCE"
REQUIRES_DEPLOYMENT_EVIDENCE = "REQUIRES_DEPLOYMENT_EVIDENCE"
REQUIRES_PRODUCTION_EVIDENCE = "REQUIRES_PRODUCTION_EVIDENCE"

DOCTRINE = "DOCTRINE"
HARDENING_BOUNDARY = "HARDENING_BOUNDARY"
IMPLEMENTATION_STATUS = "IMPLEMENTATION_STATUS"
TEST_EVIDENCE = "TEST_EVIDENCE"
OPERATOR_SCENARIO_REASONING = "OPERATOR_SCENARIO_REASONING"
RUNTIME_STATE = "RUNTIME_STATE"
DB_STATE = "DB_STATE"
DEPLOYMENT_STATE = "DEPLOYMENT_STATE"
PRODUCTION_READINESS = "PRODUCTION_READINESS"
UNKNOWN = "UNKNOWN"

PAYROLL_CORRECTION_WORKFLOW_REASONING = "PAYROLL_CORRECTION_WORKFLOW_REASONING"
RUNTIME_EVIDENCE = "RUNTIME_EVIDENCE"
DB_EVIDENCE = "DB_EVIDENCE"
DEPLOYMENT_EVIDENCE = "DEPLOYMENT_EVIDENCE"
PRODUCTION_EVIDENCE = "PRODUCTION_EVIDENCE"
CODE_EVIDENCE = "CODE_EVIDENCE"

PAYROLL_REASONING_ARTIFACT = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "knowledge"
    / "payroll_correction_workflow_reasoning_v0_1.md"
)

FINAL_ANSWER_ELIGIBILITY = {
    "Eligible": False,
    "EligibilityStatus": "PREPARATION_ONLY",
    "Reason": (
        "This packet records claim-level provenance requirements only. It does "
        "not generate final prose, expose chat, call a live LLM, perform DB or "
        "runtime checks, or establish production readiness."
    ),
}

NEXT_STEP = (
    "Use this provenance packet as controlled input to a later answer rehearsal "
    "or final-answer gate. Do not convert it directly into a user-facing answer."
)

SOURCE_AUTHORITY_RULES = {
    DOCTRINE: {
        "Required": (PLATFORM_DOCTRINE,),
        "CitationRequirement": "Future answer must cite Platform Doctrine evidence.",
        "CaveatRequirement": "Doctrine evidence is governance context, not execution or implementation proof.",
        "Missing": "Platform Doctrine evidence is required for doctrine claims.",
        "AdditionalEvidence": ("Platform Doctrine evidence for the doctrine claim.",),
    },
    HARDENING_BOUNDARY: {
        "Required": (HARDENING_LOG, PLATFORM_DOCTRINE),
        "CitationRequirement": "Future answer must cite Hardening Log and/or Platform Doctrine evidence.",
        "CaveatRequirement": "Hardening/prohibition evidence establishes boundaries, not completed implementation.",
        "Missing": "Hardening Log or Platform Doctrine evidence is required for boundary claims.",
        "AdditionalEvidence": ("Hardening Log or Platform Doctrine evidence for the boundary claim.",),
    },
    IMPLEMENTATION_STATUS: {
        "Required": (DEVELOPER_LOG,),
        "CitationRequirement": "Future answer must cite Developer Log, slice knowledge, or implementation evidence.",
        "CaveatRequirement": "Developer Log evidence does not prove runtime, deployment, or production readiness.",
        "Missing": "Developer Log or implementation evidence is required for work-completed claims.",
        "AdditionalEvidence": ("Developer Log or implementation evidence for the implementation-status claim.",),
    },
    TEST_EVIDENCE: {
        "Required": (DEVELOPER_LOG,),
        "CitationRequirement": "Future answer must cite Developer Log, test output, or slice knowledge evidence.",
        "CaveatRequirement": "Test evidence from this slice does not prove production readiness.",
        "Missing": "Developer Log or explicit test evidence is required for test-evidence claims.",
        "AdditionalEvidence": ("Developer Log or explicit test evidence for the test claim.",),
    },
    OPERATOR_SCENARIO_REASONING: {
        "Required": (PAYROLL_CORRECTION_WORKFLOW_REASONING, PLATFORM_DOCTRINE),
        "CitationRequirement": "Future answer must cite the payroll correction workflow reasoning artefact and/or Platform Doctrine evidence.",
        "CaveatRequirement": "Payroll reasoning evidence is curated scenario reasoning, not Workforce runtime proof.",
        "Missing": "Payroll correction workflow reasoning evidence is required for operator scenario claims.",
        "AdditionalEvidence": ("Payroll correction workflow reasoning evidence for the operator scenario claim.",),
    },
    RUNTIME_STATE: {
        "Required": (RUNTIME_EVIDENCE,),
        "CitationRequirement": "Future answer must cite authorised runtime evidence.",
        "CaveatRequirement": "Controlled fixture evidence is insufficient for current runtime state.",
        "Missing": "Authorised runtime evidence is required.",
        "AdditionalEvidence": ("Authorised current runtime evidence.",),
    },
    DB_STATE: {
        "Required": (DB_EVIDENCE,),
        "CitationRequirement": "Future answer must cite authorised DB evidence.",
        "CaveatRequirement": "Controlled fixture evidence is insufficient for current live DB state.",
        "Missing": "Authorised DB evidence is required.",
        "AdditionalEvidence": ("Authorised DB evidence from a later slice.",),
    },
    DEPLOYMENT_STATE: {
        "Required": (DEPLOYMENT_EVIDENCE,),
        "CitationRequirement": "Future answer must cite authorised deployment evidence.",
        "CaveatRequirement": "Controlled fixture evidence is insufficient for deployment state.",
        "Missing": "Authorised deployment evidence is required.",
        "AdditionalEvidence": ("Authorised deployment evidence.",),
    },
    PRODUCTION_READINESS: {
        "Required": (PRODUCTION_EVIDENCE,),
        "CitationRequirement": "Future answer must cite authorised production-readiness evidence.",
        "CaveatRequirement": "Production readiness is prohibited without production evidence and explicit authorisation.",
        "Missing": "Production-readiness evidence is required and is not present in this slice.",
        "AdditionalEvidence": ("Authorised production-readiness evidence.",),
    },
    UNKNOWN: {
        "Required": (),
        "CitationRequirement": "Future answer must classify this claim before citation can be assigned.",
        "CaveatRequirement": "Unknown claim authority cannot support final answer use.",
        "Missing": "A known claim type and matching source authority are required.",
        "AdditionalEvidence": ("Claim classification evidence.",),
    },
}


@dataclass(frozen=True)
class CitationProvenancePacket:
    QueryText: str
    ProvenanceMode: str
    EvidenceUniverse: str
    PacketStatus: str
    Claims: tuple[dict[str, Any], ...]
    EvidenceInventory: tuple[dict[str, Any], ...]
    SourceAuthoritySummary: tuple[dict[str, Any], ...]
    CitationRequirements: tuple[dict[str, Any], ...]
    CaveatRequirements: tuple[str, ...]
    UnsupportedClaims: tuple[dict[str, Any], ...]
    ProhibitedClaims: tuple[dict[str, Any], ...]
    ClaimsRequiringAdditionalEvidence: tuple[dict[str, Any], ...]
    FinalAnswerEligibility: dict[str, Any]
    BoundaryFlags: dict[str, bool]
    NextStep: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_citation_provenance_packet(
    query_text: str,
    answer_preparation_envelope: dict[str, Any] | None = None,
    provenance_mode: str = PROVENANCE_MODE,
    required_claim_type_filter: str | Iterable[str] | None = None,
) -> dict[str, Any]:
    return build_citation_provenance_packet(
        query_text=query_text,
        answer_preparation_envelope=answer_preparation_envelope,
        provenance_mode=provenance_mode,
        required_claim_type_filter=required_claim_type_filter,
    )


def build_citation_provenance_packet(
    query_text: str,
    answer_preparation_envelope: dict[str, Any] | None = None,
    provenance_mode: str = PROVENANCE_MODE,
    required_claim_type_filter: str | Iterable[str] | None = None,
) -> dict[str, Any]:
    """Map prepared claims to deterministic source-aware provenance rules."""

    query = str(query_text or "")
    preparation = answer_preparation_envelope or build_controlled_multi_source_answer_preparation(query)
    requested_types = _claim_type_filter(required_claim_type_filter)
    inventory = _evidence_inventory(preparation)
    claims = tuple(
        claim
        for claim in (
            _provenance_claim(prepared_claim, inventory)
            for prepared_claim in _prepared_claims(preparation)
        )
        if not requested_types or claim["ClaimType"] in requested_types
    )

    unsupported = tuple(
        claim for claim in claims if claim["ClaimStatus"] in _unsupported_statuses()
    )
    prohibited = tuple(claim for claim in claims if claim["ClaimStatus"] == PROHIBITED)
    additional_evidence = tuple(
        _additional_evidence_requirement(claim)
        for claim in claims
        if claim["AdditionalEvidenceRequired"]
    )

    return CitationProvenancePacket(
        QueryText=query,
        ProvenanceMode=str(provenance_mode or PROVENANCE_MODE),
        EvidenceUniverse=PROVENANCE_UNIVERSE,
        PacketStatus=_packet_status(claims),
        Claims=claims,
        EvidenceInventory=inventory,
        SourceAuthoritySummary=_source_authority_summary(),
        CitationRequirements=_citation_requirements(),
        CaveatRequirements=_caveat_requirements(preparation, claims),
        UnsupportedClaims=unsupported,
        ProhibitedClaims=prohibited,
        ClaimsRequiringAdditionalEvidence=additional_evidence,
        FinalAnswerEligibility=dict(FINAL_ANSWER_ELIGIBILITY),
        BoundaryFlags=dict(BOUNDARY_FLAGS),
        NextStep=NEXT_STEP,
    ).to_dict()


def _prepared_claims(preparation: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    claims: list[dict[str, Any]] = []
    for key in ("SupportedClaims", "UnsupportedClaims", "ProhibitedClaims", "ClaimsRequiringAdditionalEvidence"):
        for claim in preparation.get(key, ()) or ():
            claims.append(dict(claim))
    return tuple(claims)


def _provenance_claim(
    prepared_claim: dict[str, Any],
    inventory: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    claim_type = _claim_type(prepared_claim)
    rule = SOURCE_AUTHORITY_RULES[claim_type]
    evidence_used = _evidence_used_for_claim(prepared_claim, inventory, claim_type)
    required = tuple(rule["Required"])
    source_authority_satisfied = _source_authority_satisfied(claim_type, required, evidence_used)
    status = _claim_status(prepared_claim, claim_type, source_authority_satisfied, evidence_used)
    evidence_missing = _evidence_missing(claim_type, required, evidence_used)
    additional_required = _additional_required(claim_type, evidence_missing, status)

    return {
        "ClaimId": _claim_id(prepared_claim),
        "ClaimText": _claim_text(prepared_claim),
        "ClaimType": claim_type,
        "ClaimStatus": status,
        "EvidenceRequired": required,
        "EvidenceUsed": evidence_used,
        "EvidenceMissing": evidence_missing,
        "SourceAuthorityRequired": required,
        "SourceAuthoritySatisfied": source_authority_satisfied,
        "CitationRequirement": rule["CitationRequirement"],
        "CaveatRequirement": rule["CaveatRequirement"],
        "UnsupportedReason": _unsupported_reason(prepared_claim, claim_type, status, rule),
        "ProhibitedReason": _prohibited_reason(prepared_claim, claim_type, status),
        "FinalAnswerEligible": False,
        "AdditionalEvidenceRequired": additional_required,
    }


def _evidence_inventory(preparation: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    evidence: list[dict[str, Any]] = []
    for item in preparation.get("EvidenceUsed", ()) or ():
        evidence.append(_evidence_reference(item))
    for claim in _prepared_claims(preparation):
        for item in claim.get("EvidenceReferences", ()) or ():
            evidence.append(_evidence_reference(item))
    if PAYROLL_REASONING_ARTIFACT.exists():
        evidence.append(_payroll_reasoning_reference())
    return tuple(_dedupe_dicts(evidence))


def _evidence_used_for_claim(
    prepared_claim: dict[str, Any],
    inventory: tuple[dict[str, Any], ...],
    claim_type: str,
) -> tuple[dict[str, Any], ...]:
    claim_refs = tuple(_evidence_reference(item) for item in prepared_claim.get("EvidenceReferences", ()) or ())
    if claim_type == OPERATOR_SCENARIO_REASONING and PAYROLL_REASONING_ARTIFACT.exists():
        return tuple(_dedupe_dicts((*claim_refs, _payroll_reasoning_reference())))

    if claim_refs:
        return claim_refs

    required = SOURCE_AUTHORITY_RULES[claim_type]["Required"]
    return tuple(item for item in inventory if item["EvidenceType"] in required)


def _claim_status(
    prepared_claim: dict[str, Any],
    claim_type: str,
    source_authority_satisfied: bool,
    evidence_used: tuple[dict[str, Any], ...],
) -> str:
    if _is_prohibited_overclaim(prepared_claim, claim_type):
        return PROHIBITED
    if claim_type == RUNTIME_STATE:
        return REQUIRES_CURRENT_RUNTIME_EVIDENCE
    if claim_type == DB_STATE:
        return REQUIRES_DB_EVIDENCE
    if claim_type == DEPLOYMENT_STATE:
        return REQUIRES_DEPLOYMENT_EVIDENCE
    if claim_type == PRODUCTION_READINESS:
        return PROHIBITED
    if _requires_code_evidence(prepared_claim):
        return REQUIRES_CODE_EVIDENCE
    if not source_authority_satisfied:
        if claim_type == DOCTRINE and any(item["EvidenceType"] == DEVELOPER_LOG for item in evidence_used):
            return SUPPORTED_WITH_CAVEAT
        return UNSUPPORTED
    if _has_caveat(prepared_claim, claim_type):
        return SUPPORTED_WITH_CAVEAT
    return SUPPORTED


def _claim_type(prepared_claim: dict[str, Any]) -> str:
    raw = _normalize_type(prepared_claim.get("ClaimType"))
    text = _claim_text(prepared_claim).lower()
    combined = f"{raw} {text}"

    if "PRODUCTION" in raw or "production-ready" in text or "production ready" in text:
        return PRODUCTION_READINESS
    if "DB" in raw or "DATABASE" in raw or "live db" in text or "database state" in text:
        return DB_STATE
    if "DEPLOYMENT" in raw or "deployment" in text:
        return DEPLOYMENT_STATE
    if "RUNTIME" in raw or "runtime state" in text or "runtime integration is active" in text:
        return RUNTIME_STATE
    if "OPERATOR_SCENARIO_REASONING" in raw or _is_payroll_operator_claim(text):
        return OPERATOR_SCENARIO_REASONING
    if "TEST" in raw:
        return TEST_EVIDENCE
    if "IMPLEMENTATION" in raw or "WORK_COMPLETED" in raw or "controlled multi-source" in combined.lower():
        return IMPLEMENTATION_STATUS
    if "HARDENING" in raw or "PROHIBITION" in raw or "PROHIBITED" in raw or "llm" in text or "chat exposure" in text:
        return HARDENING_BOUNDARY
    if "CODE_EVIDENCE" in raw or "code evidence" in text:
        return TEST_EVIDENCE
    if "DOCTRINE" in raw or "source/status" in text or "boundary" in text:
        return DOCTRINE
    return UNKNOWN


def _is_payroll_operator_claim(text: str) -> bool:
    markers = (
        "processperiod",
        "objecttime",
        "retro",
        "off-cycle",
        "off cycle",
        "current pay adjustment",
        "current-period adjustment",
        "finalisation lock",
        "payrun",
        "timesheet",
    )
    return any(marker in text for marker in markers)


def _source_authority_satisfied(
    claim_type: str,
    required: tuple[str, ...],
    evidence_used: tuple[dict[str, Any], ...],
) -> bool:
    evidence_types = {item["EvidenceType"] for item in evidence_used}
    if claim_type == OPERATOR_SCENARIO_REASONING:
        return PAYROLL_CORRECTION_WORKFLOW_REASONING in evidence_types
    if claim_type == HARDENING_BOUNDARY:
        return bool(evidence_types & {HARDENING_LOG, PLATFORM_DOCTRINE})
    if not required:
        return False
    return bool(evidence_types & set(required))


def _evidence_missing(
    claim_type: str,
    required: tuple[str, ...],
    evidence_used: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    evidence_types = {item["EvidenceType"] for item in evidence_used}
    if claim_type in {HARDENING_BOUNDARY, OPERATOR_SCENARIO_REASONING}:
        if _source_authority_satisfied(claim_type, required, evidence_used):
            return ()
        return required
    return tuple(item for item in required if item not in evidence_types)


def _additional_required(
    claim_type: str,
    evidence_missing: tuple[str, ...],
    status: str,
) -> tuple[str, ...]:
    if status in {SUPPORTED, SUPPORTED_WITH_CAVEAT} and not evidence_missing:
        return ()
    if status == PROHIBITED and claim_type == PRODUCTION_READINESS:
        return (
            "Explicit production-readiness authorisation.",
            "Deployment evidence.",
            "Production evidence.",
        )
    if status == PROHIBITED:
        return ("Explicit evidence and authorisation overriding the prohibited overclaim.",)
    if claim_type == RUNTIME_STATE:
        return ("Authorised current runtime evidence.",)
    if claim_type == DB_STATE:
        return ("Authorised DB evidence from a later slice.",)
    if claim_type == DEPLOYMENT_STATE:
        return ("Authorised deployment evidence.",)
    if status == REQUIRES_CODE_EVIDENCE:
        return ("Authorised Code Evidence ingestion from a later slice.",)
    return tuple(SOURCE_AUTHORITY_RULES[claim_type]["AdditionalEvidence"])


def _unsupported_reason(
    prepared_claim: dict[str, Any],
    claim_type: str,
    status: str,
    rule: dict[str, Any],
) -> str:
    if status in {SUPPORTED, SUPPORTED_WITH_CAVEAT, PROHIBITED}:
        return ""
    if prepared_claim.get("Reason"):
        return str(prepared_claim["Reason"])
    return str(rule["Missing"])


def _prohibited_reason(prepared_claim: dict[str, Any], claim_type: str, status: str) -> str:
    if status != PROHIBITED:
        return ""
    if prepared_claim.get("Reason"):
        return str(prepared_claim["Reason"])
    if claim_type == PRODUCTION_READINESS:
        return "Production readiness cannot be claimed without deployment and production evidence."
    return "The claim is a live/runtime/chat/production overclaim for this slice."


def _packet_status(claims: tuple[dict[str, Any], ...]) -> str:
    if not claims:
        return OUT_OF_SCOPE
    if any(claim["ClaimStatus"] == PROHIBITED for claim in claims):
        return BLOCKED_PROHIBITED_CLAIMS
    if all(claim["ClaimStatus"] in _unsupported_statuses() for claim in claims):
        return INSUFFICIENT_EVIDENCE
    if any(claim["ClaimStatus"] in _unsupported_statuses() for claim in claims):
        return PROVENANCE_READY_WITH_CAVEATS
    if any(claim["ClaimStatus"] == SUPPORTED_WITH_CAVEAT for claim in claims):
        return PROVENANCE_READY_WITH_CAVEATS
    return PROVENANCE_READY


def _citation_requirements() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "ClaimType": claim_type,
            "RequiredSourceAuthority": tuple(rule["Required"]),
            "CitationRequirement": rule["CitationRequirement"],
        }
        for claim_type, rule in SOURCE_AUTHORITY_RULES.items()
    )


def _source_authority_summary() -> tuple[dict[str, Any], ...]:
    return (
        {
            "SourceAuthority": PLATFORM_DOCTRINE,
            "AppliesToClaimTypes": (DOCTRINE, HARDENING_BOUNDARY, OPERATOR_SCENARIO_REASONING),
            "CannotEstablish": (
                "implementation completed",
                "current runtime state",
                "DB state",
                "deployment readiness",
                "production readiness",
            ),
        },
        {
            "SourceAuthority": HARDENING_LOG,
            "AppliesToClaimTypes": (HARDENING_BOUNDARY,),
            "CannotEstablish": (
                "implementation completed",
                "repair completed",
                "current runtime state",
                "production readiness",
            ),
        },
        {
            "SourceAuthority": DEVELOPER_LOG,
            "AppliesToClaimTypes": (IMPLEMENTATION_STATUS, TEST_EVIDENCE),
            "CannotEstablish": (
                "Platform Doctrine",
                "current runtime state",
                "DB state",
                "deployment readiness",
                "production readiness",
            ),
        },
        {
            "SourceAuthority": PAYROLL_CORRECTION_WORKFLOW_REASONING,
            "AppliesToClaimTypes": (OPERATOR_SCENARIO_REASONING,),
            "CannotEstablish": (
                "Workforce runtime implementation",
                "Analytics runtime implementation",
                "current DB state",
                "production readiness",
            ),
        },
        {
            "SourceAuthority": (RUNTIME_EVIDENCE, DB_EVIDENCE, DEPLOYMENT_EVIDENCE, PRODUCTION_EVIDENCE),
            "AppliesToClaimTypes": (
                RUNTIME_STATE,
                DB_STATE,
                DEPLOYMENT_STATE,
                PRODUCTION_READINESS,
            ),
            "CannotEstablish": ("Not present in this controlled local fixture slice.",),
        },
    )


def _caveat_requirements(
    preparation: dict[str, Any],
    claims: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    caveats = [
        "Final answer generation remains out of scope.",
        "Citation/provenance requirements are not final prose answers.",
        "Historical evidence is not current truth by default.",
        "Controlled fixture evidence is not runtime, DB, deployment, or production evidence.",
    ]
    caveats.extend(str(item) for item in preparation.get("RequiredCaveats", ()) or () if str(item))
    caveats.extend(claim["CaveatRequirement"] for claim in claims if claim.get("CaveatRequirement"))
    return tuple(dict.fromkeys(caveats))


def _additional_evidence_requirement(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "ClaimId": claim["ClaimId"],
        "ClaimText": claim["ClaimText"],
        "ClaimType": claim["ClaimType"],
        "ClaimStatus": claim["ClaimStatus"],
        "RequiredEvidence": claim["AdditionalEvidenceRequired"],
        "MissingEvidence": claim["EvidenceMissing"],
    }


def _evidence_reference(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "RecordId": str(item.get("RecordId") or ""),
        "EvidenceType": str(item.get("EvidenceType") or item.get("SourceType") or ""),
        "SourceType": str(item.get("SourceType") or item.get("EvidenceType") or ""),
        "SourceTitle": str(item.get("SourceTitle") or ""),
        "AuthorityLevel": str(item.get("AuthorityLevel") or ""),
        "SourceStatus": str(item.get("SourceStatus") or ""),
        "ImplementationStatus": str(item.get("ImplementationStatus") or ""),
        "CurrentTruthStatus": str(item.get("CurrentTruthStatus") or ""),
        "AnswerUseStatus": str(item.get("AnswerUseStatus") or ""),
    }


def _payroll_reasoning_reference() -> dict[str, Any]:
    return {
        "RecordId": "payroll-correction-workflow-reasoning-v0-1",
        "EvidenceType": PAYROLL_CORRECTION_WORKFLOW_REASONING,
        "SourceType": PAYROLL_CORRECTION_WORKFLOW_REASONING,
        "SourceTitle": "Payroll Correction Workflow Reasoning v0.1",
        "AuthorityLevel": "AUTHORITY_3_CURATED_OPERATOR_REASONING",
        "SourceStatus": "CURATED_REASONING_EVIDENCE",
        "ImplementationStatus": "WORKFORCE_RUNTIME_IMPLEMENTATION_NOT_PROVEN",
        "CurrentTruthStatus": "CURATED_REASONING_NOT_CURRENT_RUNTIME_TRUTH",
        "AnswerUseStatus": "FINAL_ANSWER_NOT_PERMITTED_PROVENANCE_ONLY",
    }


def _claim_id(prepared_claim: dict[str, Any]) -> str:
    if prepared_claim.get("ClaimId"):
        return str(prepared_claim["ClaimId"])
    text = _claim_text(prepared_claim)
    normalized = "".join(char.lower() if char.isalnum() else "-" for char in text).strip("-")
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    return f"claim-{normalized[:72] or 'unknown'}"


def _claim_text(prepared_claim: dict[str, Any]) -> str:
    return str(
        prepared_claim.get("ClaimText")
        or prepared_claim.get("ClaimSummary")
        or prepared_claim.get("RequiredEvidence")
        or ""
    )


def _has_caveat(prepared_claim: dict[str, Any], claim_type: str) -> bool:
    if prepared_claim.get("RequiredCaveats"):
        return True
    return claim_type in {
        DOCTRINE,
        HARDENING_BOUNDARY,
        IMPLEMENTATION_STATUS,
        TEST_EVIDENCE,
        OPERATOR_SCENARIO_REASONING,
    }


def _is_prohibited_overclaim(prepared_claim: dict[str, Any], claim_type: str) -> bool:
    text = _claim_text(prepared_claim).lower()
    raw_status = _normalize_type(prepared_claim.get("ClaimStatus"))
    if raw_status == PROHIBITED:
        return True
    prohibited_markers = (
        "minerva chat is live",
        "live llm is enabled",
        "production-ready",
        "production ready",
        "runtime integration is active",
    )
    return claim_type == PRODUCTION_READINESS or any(marker in text for marker in prohibited_markers)


def _requires_code_evidence(prepared_claim: dict[str, Any]) -> bool:
    raw_status = _normalize_type(prepared_claim.get("ClaimStatus"))
    return raw_status == REQUIRES_CODE_EVIDENCE


def _unsupported_statuses() -> set[str]:
    return {
        UNSUPPORTED,
        REQUIRES_CURRENT_RUNTIME_EVIDENCE,
        REQUIRES_CODE_EVIDENCE,
        REQUIRES_DB_EVIDENCE,
        REQUIRES_DEPLOYMENT_EVIDENCE,
        REQUIRES_PRODUCTION_EVIDENCE,
    }


def _claim_type_filter(value: str | Iterable[str] | None) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {_claim_type({"ClaimType": value})}
    return {_claim_type({"ClaimType": item}) for item in value}


def _normalize_type(value: Any) -> str:
    return str(value or "").strip().upper().replace("-", "_").replace(" ", "_")


def _dedupe_dicts(items: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = tuple(sorted((str(key), str(value)) for key, value in item.items()))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return tuple(unique)

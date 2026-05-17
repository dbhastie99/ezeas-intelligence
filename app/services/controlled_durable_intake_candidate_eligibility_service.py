import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE = (
    "DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE"
)
NEEDS_SOURCE_REFERENCE = "NEEDS_SOURCE_REFERENCE"
NEEDS_SOURCE_STATUS_BOUNDARY = "NEEDS_SOURCE_STATUS_BOUNDARY"
NEEDS_EVIDENCE_ENVELOPE = "NEEDS_EVIDENCE_ENVELOPE"
NEEDS_AUDIT_ENVELOPE = "NEEDS_AUDIT_ENVELOPE"
NEEDS_REVIEWER_CONFIRMATION = "NEEDS_REVIEWER_CONFIRMATION"
NEEDS_ROLLBACK_POLICY = "NEEDS_ROLLBACK_POLICY"
NEEDS_SENSITIVE_DATA_REVIEW = "NEEDS_SENSITIVE_DATA_REVIEW"
BLOCKED_PROHIBITED_CLAIMS = "BLOCKED_PROHIBITED_CLAIMS"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

CANDIDATE_TYPES = (
    "DEVELOPER_LOG",
    "HARDENING_LOG",
    "PLATFORM_DOCTRINE",
    "ANALYTICS_READINESS_SUMMARY",
    "AWARD_RECOVERY_ANALYSIS",
    "CONTROLLED_EVALUATION_SUMMARY",
    "CODE_EVIDENCE_PLANNING_OUTPUT",
    UNKNOWN_REQUIRES_REVIEW,
)

PREREQUISITE_STATUS_BY_KEY = {
    "source_reference": NEEDS_SOURCE_REFERENCE,
    "source_status_boundary": NEEDS_SOURCE_STATUS_BOUNDARY,
    "evidence_envelope": NEEDS_EVIDENCE_ENVELOPE,
    "audit_envelope": NEEDS_AUDIT_ENVELOPE,
    "reviewer_confirmation": NEEDS_REVIEWER_CONFIRMATION,
    "rollback_policy": NEEDS_ROLLBACK_POLICY,
    "sensitive_data_review": NEEDS_SENSITIVE_DATA_REVIEW,
}

PROHIBITED_CLAIM_KEYS = (
    "durable_intake_authorised_now",
    "durable_intake_performed",
    "durable_ingestion_performed",
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
    "db_write_authorised",
    "db_write_authorised_now",
    "db_write_performed",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_performed",
    "live_retrieval_authorised",
    "live_retrieval_performed",
    "live_llm_authorised",
    "live_llm_performed",
    "final_answer_generation_authorised",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "runtime_integration_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)

REQUIRED_CAVEATS = (
    "Eligibility is only for a future durable-intake authorisation gate.",
    "No durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM, final answer generation, chat exposure, runtime integration, deployment readiness, or production readiness is authorised.",
)


@dataclass(frozen=True)
class ControlledDurableIntakeCandidateEligibilityResult:
    eligibility_id: str
    candidate_id: str
    candidate_type: str
    eligibility_status: str
    eligible_for_authorisation_gate: bool
    source_reference_present: bool
    source_status_boundary_present: bool
    evidence_envelope_present: bool
    audit_envelope_present: bool
    reviewer_confirmation_present: bool
    rollback_policy_present: bool
    sensitive_data_review_present: bool
    prohibited_claims_present: bool
    missing_prerequisites: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_durable_intake_candidate_eligibility(
    candidate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Evaluate durable-intake candidate eligibility without taking action."""

    metadata = candidate_metadata or {}
    candidate_id = str(metadata.get("candidate_id") or "")
    candidate_type = str(metadata.get("candidate_type") or UNKNOWN_REQUIRES_REVIEW)
    presence = _prerequisite_presence(metadata)
    missing = tuple(key for key, present in presence.items() if not present)
    blocked = _blocked_reasons(metadata)
    status = _eligibility_status(candidate_type, missing, blocked)
    eligible = status == DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE

    material = {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "missing": missing,
        "blocked": blocked,
        "status": status,
    }

    return ControlledDurableIntakeCandidateEligibilityResult(
        eligibility_id=str(metadata.get("eligibility_id") or _stable_id(material)),
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        eligibility_status=status,
        eligible_for_authorisation_gate=eligible,
        source_reference_present=presence["source_reference"],
        source_status_boundary_present=presence["source_status_boundary"],
        evidence_envelope_present=presence["evidence_envelope"],
        audit_envelope_present=presence["audit_envelope"],
        reviewer_confirmation_present=presence["reviewer_confirmation"],
        rollback_policy_present=presence["rollback_policy"],
        sensitive_data_review_present=presence["sensitive_data_review"],
        prohibited_claims_present=bool(blocked),
        missing_prerequisites=missing,
        blocked_reasons=blocked,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def build_controlled_durable_intake_candidate_eligibility(
    candidate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_controlled_durable_intake_candidate_eligibility(candidate_metadata)


def _prerequisite_presence(metadata: dict[str, Any]) -> dict[str, bool]:
    return {
        "source_reference": bool(metadata.get("source_reference")),
        "source_status_boundary": bool(metadata.get("source_status_boundary")),
        "evidence_envelope": metadata.get("evidence_envelope") is True,
        "audit_envelope": metadata.get("audit_envelope") is True,
        "reviewer_confirmation": metadata.get("reviewer_confirmation") is True,
        "rollback_policy": bool(metadata.get("rollback_policy")),
        "sensitive_data_review": metadata.get("sensitive_data_review") is True,
    }


def _blocked_reasons(metadata: dict[str, Any]) -> tuple[str, ...]:
    if any(bool(metadata.get(key)) for key in PROHIBITED_CLAIM_KEYS):
        return ("prohibited_runtime_production_mutation_or_ingestion_claim",)
    return ()


def _eligibility_status(
    candidate_type: str,
    missing: tuple[str, ...],
    blocked: tuple[str, ...],
) -> str:
    if blocked:
        return BLOCKED_PROHIBITED_CLAIMS
    if candidate_type not in CANDIDATE_TYPES or candidate_type == UNKNOWN_REQUIRES_REVIEW:
        return UNKNOWN_REQUIRES_REVIEW
    for prerequisite, status in PREREQUISITE_STATUS_BY_KEY.items():
        if prerequisite in missing:
            return status
    return DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE:
        return (
            "Candidate metadata is complete for a future durable-intake "
            "authorisation gate only; no durable intake or mutation was performed."
        )
    if status == BLOCKED_PROHIBITED_CLAIMS:
        return (
            "Candidate metadata includes a prohibited runtime, production, "
            "mutation, ingestion, DB, retrieval, LLM, final-answer, or chat claim."
        )
    if status == UNKNOWN_REQUIRES_REVIEW:
        return "Candidate type is unknown or requires controlled review."
    return "Candidate metadata is missing a required durable-intake prerequisite."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-candidate-eligibility-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

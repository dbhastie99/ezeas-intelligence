import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION = (
    "AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION"
)
NEEDS_SOURCE_REFERENCE = "NEEDS_SOURCE_REFERENCE"
NEEDS_SOURCE_STATUS_BOUNDARY = "NEEDS_SOURCE_STATUS_BOUNDARY"
NEEDS_EVIDENCE_ENVELOPE = "NEEDS_EVIDENCE_ENVELOPE"
NEEDS_AUDIT_ENVELOPE = "NEEDS_AUDIT_ENVELOPE"
NEEDS_REVIEWER_CONFIRMATION = "NEEDS_REVIEWER_CONFIRMATION"
NEEDS_ROLLBACK_POLICY = "NEEDS_ROLLBACK_POLICY"
NEEDS_SENSITIVE_DATA_REVIEW = "NEEDS_SENSITIVE_DATA_REVIEW"
BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM = (
    "BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM"
)
BLOCKED_MUTATION_OR_DB_WRITE_CLAIM = "BLOCKED_MUTATION_OR_DB_WRITE_CLAIM"
BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM = "BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM"
BLOCKED_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

PREREQUISITE_STATUS_BY_KEY = {
    "source_reference": NEEDS_SOURCE_REFERENCE,
    "source_status_boundary": NEEDS_SOURCE_STATUS_BOUNDARY,
    "evidence_envelope": NEEDS_EVIDENCE_ENVELOPE,
    "audit_envelope": NEEDS_AUDIT_ENVELOPE,
    "reviewer_confirmation": NEEDS_REVIEWER_CONFIRMATION,
    "rollback_policy": NEEDS_ROLLBACK_POLICY,
    "sensitive_data_review": NEEDS_SENSITIVE_DATA_REVIEW,
}

DURABLE_INTAKE_PERFORMED_CLAIM_KEYS = (
    "durable_intake_performed",
    "durable_ingestion_performed",
    "durable_evidence_ingestion_performed",
    "already_durably_ingested",
)

MUTATION_OR_DB_WRITE_CLAIM_KEYS = (
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
    "db_write_authorised",
    "db_write_authorised_now",
    "db_write_performed",
    "db_access_authorised",
    "db_read_performed",
)

CODE_EVIDENCE_INGESTION_CLAIM_KEYS = (
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_performed",
)

LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM_KEYS = (
    "live_retrieval_authorised",
    "live_retrieval_performed",
    "live_llm_authorised",
    "live_llm_performed",
    "final_answer_generation_authorised",
    "final_answer_generation_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "chat_exposure_authorised",
    "internal_chat_exposure_authorised",
    "public_chat_exposure_authorised",
    "tenant_chat_exposure_authorised",
    "customer_chat_exposure_authorised",
    "runtime_integration_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)

REQUIRED_CAVEATS = (
    "Future durable intake execution eligibility is not durable intake authorisation now.",
    "No durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM, final answer generation, chat exposure, runtime integration, deployment readiness, or production readiness is authorised.",
)


@dataclass(frozen=True)
class ControlledDurableEvidenceIntakeAuthorisationGateResult:
    authorisation_id: str
    candidate_id: str
    authorisation_status: str
    eligible_for_future_durable_intake_execution: bool
    durable_intake_authorised_now: bool
    durable_intake_performed: bool
    corpus_mutation_performed: bool
    db_write_performed: bool
    code_evidence_ingestion_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    chat_exposure_authorised: bool
    runtime_integration_authorised: bool
    missing_prerequisites: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_durable_evidence_intake_authorisation_gate(
    candidate_metadata: dict[str, Any] | None,
    prerequisite_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Authorise only future durable-intake execution candidacy."""

    candidate = candidate_metadata or {}
    prerequisites = prerequisite_metadata or {}
    combined = {**candidate, **prerequisites}
    candidate_id = str(candidate.get("candidate_id") or prerequisites.get("candidate_id") or "")
    presence = _prerequisite_presence(combined)
    missing = tuple(key for key, present in presence.items() if not present)
    blocked = _blocked_reasons(combined)
    status = _authorisation_status(combined, missing, blocked)
    eligible = status == AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION

    material = {
        "candidate_id": candidate_id,
        "candidate_type": candidate.get("candidate_type") or prerequisites.get("candidate_type") or "",
        "missing": missing,
        "blocked": blocked,
        "status": status,
    }

    return ControlledDurableEvidenceIntakeAuthorisationGateResult(
        authorisation_id=str(combined.get("authorisation_id") or _stable_id(material)),
        candidate_id=candidate_id,
        authorisation_status=status,
        eligible_for_future_durable_intake_execution=eligible,
        durable_intake_authorised_now=False,
        durable_intake_performed=False,
        corpus_mutation_performed=False,
        db_write_performed=False,
        code_evidence_ingestion_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        chat_exposure_authorised=False,
        runtime_integration_authorised=False,
        missing_prerequisites=missing,
        blocked_reasons=blocked,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def build_controlled_durable_evidence_intake_authorisation_gate(
    candidate_metadata: dict[str, Any] | None,
    prerequisite_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return evaluate_controlled_durable_evidence_intake_authorisation_gate(
        candidate_metadata,
        prerequisite_metadata,
    )


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
    blocked: list[str] = []
    if any(bool(metadata.get(key)) for key in DURABLE_INTAKE_PERFORMED_CLAIM_KEYS):
        blocked.append("durable_intake_already_performed_claim")
    if any(bool(metadata.get(key)) for key in MUTATION_OR_DB_WRITE_CLAIM_KEYS):
        blocked.append("mutation_or_db_write_claim")
    if any(bool(metadata.get(key)) for key in CODE_EVIDENCE_INGESTION_CLAIM_KEYS):
        blocked.append("code_evidence_ingestion_claim")
    if any(bool(metadata.get(key)) for key in LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM_KEYS):
        blocked.append("live_retrieval_llm_or_final_answer_claim")
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        blocked.append("runtime_or_production_overstatement")
    return tuple(blocked)


def _authorisation_status(
    metadata: dict[str, Any],
    missing: tuple[str, ...],
    blocked: tuple[str, ...],
) -> str:
    if "durable_intake_already_performed_claim" in blocked:
        return BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    if "mutation_or_db_write_claim" in blocked:
        return BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
    if "code_evidence_ingestion_claim" in blocked:
        return BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM
    if "live_retrieval_llm_or_final_answer_claim" in blocked:
        return BLOCKED_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM
    if "runtime_or_production_overstatement" in blocked:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    for prerequisite, status in PREREQUISITE_STATUS_BY_KEY.items():
        if prerequisite in missing:
            return status
    return AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION


def _explanation(status: str) -> str:
    if status == AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION:
        return (
            "Candidate metadata is eligible for a separately authorised future "
            "durable-intake execution slice. Durable intake is not authorised "
            "now and no action was performed."
        )
    if status.startswith("BLOCKED"):
        return (
            "Candidate metadata includes a prohibited claim for this controlled "
            "authorisation gate. No durable intake, mutation, runtime action, "
            "or exposure was performed."
        )
    if status == UNKNOWN_REQUIRES_REVIEW:
        return "Authorisation metadata is missing or requires controlled review."
    return "Authorisation metadata is missing a required prerequisite."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-evidence-intake-authorisation-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

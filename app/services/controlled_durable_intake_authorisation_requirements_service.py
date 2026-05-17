import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY = (
    "DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY"
)
MISSING_REQUIRED_PREREQUISITES = "MISSING_REQUIRED_PREREQUISITES"
BLOCKED_AUTHORISATION_OVERSTATEMENT = "BLOCKED_AUTHORISATION_OVERSTATEMENT"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_PREREQUISITES = (
    "reviewer_confirmation",
    "source_status_boundary",
    "evidence_envelope",
    "no_overstatement_check",
    "rollback_policy",
    "audit_metadata",
    "dry_run_review",
)

AUTHORISATION_OVERSTATEMENT_KEYS = (
    "durable_intake_authorised_now",
    "durable_intake_authorised",
    "durable_ingestion_authorised",
    "durable_ingestion_performed",
    "corpus_mutation_authorised_now",
    "corpus_mutation_authorised",
    "corpus_mutation_performed",
    "db_write_authorised_now",
    "db_write_authorised",
    "db_write_performed",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_performed",
    "production_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "runtime_readiness_claim_permitted",
)


@dataclass(frozen=True)
class ControlledDurableIntakeAuthorisationRequirementsResult:
    requirements_id: str
    requirements_status: str
    required_prerequisites: tuple[str, ...]
    missing_prerequisites: tuple[str, ...]
    reviewer_confirmation_required: bool
    source_status_boundary_required: bool
    evidence_envelope_required: bool
    no_overstatement_check_required: bool
    rollback_policy_required: bool
    audit_metadata_required: bool
    dry_run_review_required: bool
    durable_intake_authorised_now: bool
    corpus_mutation_authorised_now: bool
    db_write_authorised_now: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_intake_authorisation_requirements(
    prerequisite_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return deterministic prerequisites for a future durable-intake gate."""

    metadata = prerequisite_metadata or {}
    missing = _missing_prerequisites(metadata)
    status = _requirements_status(metadata, missing)
    material = {"status": status, "missing": missing}

    return ControlledDurableIntakeAuthorisationRequirementsResult(
        requirements_id=_stable_id(material),
        requirements_status=status,
        required_prerequisites=REQUIRED_PREREQUISITES,
        missing_prerequisites=missing,
        reviewer_confirmation_required=True,
        source_status_boundary_required=True,
        evidence_envelope_required=True,
        no_overstatement_check_required=True,
        rollback_policy_required=True,
        audit_metadata_required=True,
        dry_run_review_required=True,
        durable_intake_authorised_now=False,
        corpus_mutation_authorised_now=False,
        db_write_authorised_now=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _requirements_status(metadata: dict[str, Any], missing: tuple[str, ...]) -> str:
    if _has_authorisation_overstatement(metadata) or _status_claims_authorisation(metadata):
        return BLOCKED_AUTHORISATION_OVERSTATEMENT
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    if missing:
        return MISSING_REQUIRED_PREREQUISITES
    return DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY


def _missing_prerequisites(metadata: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        prerequisite
        for prerequisite in REQUIRED_PREREQUISITES
        if metadata.get(prerequisite) is not True
    )


def _has_authorisation_overstatement(metadata: dict[str, Any]) -> bool:
    return any(bool(metadata.get(key)) for key in AUTHORISATION_OVERSTATEMENT_KEYS)


def _status_claims_authorisation(metadata: dict[str, Any]) -> bool:
    status = " ".join(
        str(metadata.get(key) or "")
        for key in ("requirements_status", "authorisation_status", "claim_status")
    )
    return "AUTHORISED" in status or "PRODUCTION_READY" in status


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY:
        return (
            "Future durable intake prerequisites are defined and complete for "
            "review. This does not authorise durable intake, corpus mutation, "
            "or DB writes now."
        )
    if status == BLOCKED_AUTHORISATION_OVERSTATEMENT:
        return (
            "The prerequisite metadata includes an authorisation, mutation, DB "
            "write, deployment, runtime, or production overstatement."
        )
    if status == MISSING_REQUIRED_PREREQUISITES:
        return "One or more future durable-intake prerequisites are missing."
    return "The future durable-intake prerequisite metadata is missing or requires review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-authorisation-requirements-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

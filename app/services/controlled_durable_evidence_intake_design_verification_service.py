import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_durable_evidence_intake_design_service import (
    BLOCKED_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_READY,
)
from app.services.controlled_durable_intake_audit_envelope_service import (
    DURABLE_INTAKE_AUDIT_ENVELOPE_READY,
)
from app.services.controlled_durable_intake_authorisation_requirements_service import (
    DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED = (
    "DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED"
)
NEEDS_DESIGN_REVIEW = "NEEDS_DESIGN_REVIEW"
NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW = (
    "NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW"
)
NEEDS_AUDIT_ENVELOPE_REVIEW = "NEEDS_AUDIT_ENVELOPE_REVIEW"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_CAVEATS = (
    "Durable intake design verification is deterministic verification metadata only.",
    "Durable evidence intake is not authorised yet.",
    "Corpus mutation, DB writes, and Code Evidence ingestion are not authorised yet.",
    "Runtime, deployment, and production readiness claims remain blocked.",
)

VERIFICATION_FINDINGS = (
    "Durable intake design components are present for design-phase review.",
    "Authorisation prerequisites are present for a future explicit decision.",
    "Audit envelope requirements are present for a future explicit decision.",
    "Storage, mutation, review, rollback, sensitive-data, no-overstatement, and dry-run boundaries are required.",
)

BLOCKED_REASONS = (
    "Durable ingestion is not authorised by design verification.",
    "Corpus mutation is not authorised by design verification.",
    "DB writes are not authorised by design verification.",
    "Code Evidence ingestion is not authorised by design verification.",
    "Runtime, deployment, and production readiness claims are not permitted.",
)


@dataclass(frozen=True)
class ControlledDurableEvidenceIntakeDesignVerificationResult:
    verification_id: str
    verification_status: str
    design_verified: bool
    authorisation_requirements_verified: bool
    audit_envelope_verified: bool
    storage_boundary_verified: bool
    mutation_boundary_verified: bool
    review_boundary_verified: bool
    rollback_policy_required: bool
    sensitive_data_review_required: bool
    no_overstatement_check_required: bool
    dry_run_review_required: bool
    durable_intake_authorised_now: bool
    corpus_mutation_authorised_now: bool
    db_write_authorised_now: bool
    code_evidence_ingestion_authorised_now: bool
    required_caveats: tuple[str, ...]
    verification_findings: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def verify_controlled_durable_evidence_intake_design(
    design_metadata: dict[str, Any] | None,
    authorisation_requirements_metadata: dict[str, Any] | None,
    audit_envelope_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return deterministic verification metadata without authorising intake."""

    design = design_metadata or {}
    requirements = authorisation_requirements_metadata or {}
    audit = audit_envelope_metadata or {}

    design_verified = _design_verified(design)
    requirements_verified = _requirements_verified(requirements)
    audit_verified = _audit_verified(audit)
    storage_boundary_verified = bool(design.get("storage_boundary_model"))
    mutation_boundary_verified = bool(design.get("mutation_boundary_model"))
    review_boundary_verified = bool(design.get("review_boundary_model"))
    status = _verification_status(
        design,
        requirements,
        audit,
        design_verified,
        requirements_verified,
        audit_verified,
        storage_boundary_verified,
        mutation_boundary_verified,
        review_boundary_verified,
    )
    material = {
        "status": status,
        "design_verified": design_verified,
        "requirements_verified": requirements_verified,
        "audit_verified": audit_verified,
        "storage_boundary_verified": storage_boundary_verified,
        "mutation_boundary_verified": mutation_boundary_verified,
        "review_boundary_verified": review_boundary_verified,
    }

    return ControlledDurableEvidenceIntakeDesignVerificationResult(
        verification_id=_stable_id(material),
        verification_status=status,
        design_verified=design_verified,
        authorisation_requirements_verified=requirements_verified,
        audit_envelope_verified=audit_verified,
        storage_boundary_verified=storage_boundary_verified,
        mutation_boundary_verified=mutation_boundary_verified,
        review_boundary_verified=review_boundary_verified,
        rollback_policy_required=True,
        sensitive_data_review_required=True,
        no_overstatement_check_required=True,
        dry_run_review_required=True,
        durable_intake_authorised_now=False,
        corpus_mutation_authorised_now=False,
        db_write_authorised_now=False,
        code_evidence_ingestion_authorised_now=False,
        required_caveats=REQUIRED_CAVEATS,
        verification_findings=_verification_findings(status),
        blocked_reasons=BLOCKED_REASONS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _verification_status(
    design: dict[str, Any],
    requirements: dict[str, Any],
    audit: dict[str, Any],
    design_verified: bool,
    requirements_verified: bool,
    audit_verified: bool,
    storage_boundary_verified: bool,
    mutation_boundary_verified: bool,
    review_boundary_verified: bool,
) -> str:
    if _claims_runtime_or_production(design, requirements, audit):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if _claims_durable_ingestion(design, requirements, audit):
        return BLOCKED_DURABLE_INGESTION_CLAIM
    if not design:
        return NEEDS_DESIGN_REVIEW
    if not requirements:
        return NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW
    if not audit:
        return NEEDS_AUDIT_ENVELOPE_REVIEW
    if not design_verified or not (
        storage_boundary_verified
        and mutation_boundary_verified
        and review_boundary_verified
    ):
        return NEEDS_DESIGN_REVIEW
    if not requirements_verified:
        return NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW
    if not audit_verified:
        return NEEDS_AUDIT_ENVELOPE_REVIEW
    return DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED


def _design_verified(metadata: dict[str, Any]) -> bool:
    return metadata.get("design_status") == DURABLE_EVIDENCE_INTAKE_DESIGN_READY or all(
        bool(metadata.get(key))
        for key in (
            "storage_boundary_model",
            "mutation_boundary_model",
            "review_boundary_model",
        )
    ) and (
        bool(metadata.get("rollback_or_removal_policy"))
        or metadata.get("rollback_or_removal_policy_required") is True
        or metadata.get("rollback_policy_required") is True
    )


def _requirements_verified(metadata: dict[str, Any]) -> bool:
    return (
        metadata.get("requirements_status")
        == DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY
    ) or all(
        metadata.get(key) is True
        for key in (
            "reviewer_confirmation",
            "source_status_boundary",
            "evidence_envelope",
            "no_overstatement_check",
            "rollback_policy",
            "audit_metadata",
            "dry_run_review",
        )
    )


def _audit_verified(metadata: dict[str, Any]) -> bool:
    return metadata.get("audit_status") == DURABLE_INTAKE_AUDIT_ENVELOPE_READY or all(
        (
            bool(metadata.get("source_reference")),
            bool(metadata.get("source_status")),
            bool(metadata.get("reviewer")),
            bool(metadata.get("decision_timestamp")),
            bool(metadata.get("no_mutation_history")),
            bool(metadata.get("rollback_policy")),
            metadata.get("prohibited_claims_checked") is True,
            metadata.get("sensitive_data_review") is True,
        )
    )


def _claims_durable_ingestion(*metadata_sets: dict[str, Any]) -> bool:
    claim_keys = (
        "durable_intake_authorised_now",
        "durable_intake_authorised",
        "durable_ingestion_authorised",
        "durable_evidence_ingestion_authorised",
        "durable_intake_performed",
        "durable_ingestion_performed",
        "corpus_mutation_authorised_now",
        "corpus_mutation_authorised",
        "corpus_mutation_performed",
        "db_write_authorised_now",
        "db_write_authorised",
        "db_write_performed",
        "code_evidence_ingestion_authorised_now",
        "code_evidence_ingestion_authorised",
        "code_evidence_ingestion_performed",
    )
    return any(bool(metadata.get(key)) for metadata in metadata_sets for key in claim_keys)


def _claims_runtime_or_production(*metadata_sets: dict[str, Any]) -> bool:
    claim_keys = (
        "db_access_authorised",
        "db_access_performed",
        "db_read_authorised",
        "db_read_performed",
        "live_retrieval_authorised_now",
        "live_retrieval_authorised",
        "live_llm_authorised_now",
        "live_llm_authorised",
        "final_answer_generation_authorised_now",
        "final_answer_generation_authorised",
        "chat_exposure_authorised",
        "endpoint_exposure_authorised",
        "route_registration_authorised",
        "runtime_integration_authorised",
        "runtime_readiness_claim_permitted",
        "deployment_readiness_claim_permitted",
        "production_readiness_claim_permitted",
    )
    return any(bool(metadata.get(key)) for metadata in metadata_sets for key in claim_keys)


def _verification_findings(status: str) -> tuple[str, ...]:
    if status == DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED:
        return VERIFICATION_FINDINGS
    return ("Verification requires review before design-phase closeout.",)


def _explanation(status: str) -> str:
    if status == DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED:
        return (
            "Durable intake design, authorisation requirements, and audit "
            "envelope metadata are verified for design-phase closeout only."
        )
    if status == BLOCKED_DURABLE_INGESTION_CLAIM:
        return "Verification blocked an unauthorised durable ingestion or mutation claim."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Verification blocked a runtime, deployment, or production overstatement."
    return "Verification cannot complete until missing or incomplete metadata is reviewed."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-evidence-intake-design-verification-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

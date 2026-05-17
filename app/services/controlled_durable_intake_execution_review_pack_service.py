import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_durable_intake_first_candidate_execution_design_service import (
    BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM,
    BLOCKED_MUTATION_OR_DB_WRITE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_INTAKE_EXECUTION_DESIGN_READY,
    UNKNOWN_REQUIRES_REVIEW,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY = (
    "DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY"
)
NEEDS_EXECUTION_DESIGN = "NEEDS_EXECUTION_DESIGN"

REQUIRED_REVIEW_ITEMS = (
    "source_evidence",
    "candidate_eligibility",
    "authorisation_gate",
    "audit_envelope",
    "rollback_removal_policy",
    "sensitive_data_review",
    "reviewer_confirmation",
)

REQUIRED_EVIDENCE_ITEMS = (
    "source_reference_record",
    "source_status_boundary_record",
    "candidate_eligibility_record",
    "authorisation_gate_record",
    "evidence_envelope_record",
    "audit_envelope_record",
    "rollback_or_removal_policy_record",
    "sensitive_data_review_record",
    "no_overstatement_attestation",
    "explicit_execution_authorisation_record",
)

PROHIBITED_EXECUTION_CLAIMS = (
    "already_ingested",
    "corpus_mutated",
    "db_written",
    "code_evidence_ingested",
    "live_retrieval_used",
    "llm_used",
    "final_answer_generated",
    "chat_exposed",
    "runtime_integrated",
    "production_ready",
)

STOP_CONDITIONS = (
    "missing_execution_design",
    "missing_source_evidence",
    "missing_candidate_eligibility",
    "missing_authorisation_gate",
    "missing_audit_envelope",
    "missing_rollback_or_removal_policy",
    "missing_sensitive_data_review",
    "missing_reviewer_confirmation",
    "durable_intake_already_performed_claim",
    "corpus_mutation_or_db_write_claim",
    "runtime_deployment_or_production_overstatement",
)

RECOMMENDED_NEXT_SLICE = (
    "Controlled Durable Intake First Candidate Execution Authorisation v0.1"
)

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


@dataclass(frozen=True)
class ControlledDurableIntakeExecutionReviewPackResult:
    review_pack_id: str
    source_design_id: str
    review_pack_status: str
    execution_design_ready: bool
    durable_intake_execution_authorised_now: bool
    durable_intake_performed: bool
    corpus_mutation_performed: bool
    db_write_performed: bool
    code_evidence_ingestion_performed: bool
    required_review_items: tuple[str, ...]
    required_evidence_items: tuple[str, ...]
    prohibited_execution_claims: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    recommended_next_slice: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_intake_execution_review_pack(
    execution_design_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_controlled_durable_intake_execution_review_pack(
        execution_design_metadata
    )


def evaluate_controlled_durable_intake_execution_review_pack(
    execution_design_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a deterministic review pack for a later execution slice."""

    design = execution_design_metadata or {}
    status = _blocked_status(design) or _review_pack_status(design)
    source_design_id = str(design.get("design_id") or "")
    ready = status == DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY
    material = {
        "source_design_id": source_design_id,
        "design_status": design.get("design_status"),
        "status": status,
    }

    return ControlledDurableIntakeExecutionReviewPackResult(
        review_pack_id=str(design.get("review_pack_id") or _stable_id(material)),
        source_design_id=source_design_id,
        review_pack_status=status,
        execution_design_ready=ready,
        durable_intake_execution_authorised_now=False,
        durable_intake_performed=False,
        corpus_mutation_performed=False,
        db_write_performed=False,
        code_evidence_ingestion_performed=False,
        required_review_items=REQUIRED_REVIEW_ITEMS,
        required_evidence_items=REQUIRED_EVIDENCE_ITEMS,
        prohibited_execution_claims=PROHIBITED_EXECUTION_CLAIMS,
        stop_conditions=STOP_CONDITIONS,
        recommended_next_slice=RECOMMENDED_NEXT_SLICE,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _review_pack_status(design: dict[str, Any]) -> str:
    if not design:
        return NEEDS_EXECUTION_DESIGN
    if design.get("design_status") != DURABLE_INTAKE_EXECUTION_DESIGN_READY:
        return NEEDS_EXECUTION_DESIGN
    return DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY


def _blocked_status(metadata: dict[str, Any]) -> str | None:
    if any(bool(metadata.get(key)) for key in DURABLE_INTAKE_PERFORMED_CLAIM_KEYS):
        return BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    if any(bool(metadata.get(key)) for key in MUTATION_OR_DB_WRITE_CLAIM_KEYS):
        return BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    return None


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY:
        return (
            "Execution review pack is ready for reviewer assessment only. "
            "Durable intake is not authorised now and no action was performed."
        )
    if status == NEEDS_EXECUTION_DESIGN:
        return "A ready first-candidate execution design is required."
    if status.startswith("BLOCKED"):
        return (
            "Review pack metadata includes a prohibited ingestion, mutation, DB, "
            "runtime, deployment, or production claim. No action was performed."
        )
    if status == UNKNOWN_REQUIRES_REVIEW:
        return "Review pack metadata is unknown or requires controlled review."
    return "Review pack metadata requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-execution-review-pack-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

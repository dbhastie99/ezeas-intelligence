import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_durable_evidence_intake_authorisation_gate_service import (
    AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION,
)
from app.services.controlled_durable_intake_candidate_eligibility_service import (
    DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_EXECUTION_DESIGN_READY = (
    "DURABLE_INTAKE_EXECUTION_DESIGN_READY"
)
NEEDS_AUTHORISATION_GATE = "NEEDS_AUTHORISATION_GATE"
NEEDS_CANDIDATE_ELIGIBILITY = "NEEDS_CANDIDATE_ELIGIBILITY"
NEEDS_REVIEWER_CONFIRMATION = "NEEDS_REVIEWER_CONFIRMATION"
BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM = (
    "BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM"
)
BLOCKED_MUTATION_OR_DB_WRITE_CLAIM = "BLOCKED_MUTATION_OR_DB_WRITE_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_EXECUTION_STEPS = (
    "confirm_explicit_execution_authorisation",
    "lock_first_candidate_source_reference",
    "verify_source_status_boundary",
    "prepare_evidence_record_envelope",
    "prepare_audit_envelope",
    "confirm_sensitive_data_review",
    "execute_single_candidate_durable_intake_only_in_later_slice",
    "record_rollback_or_removal_evidence",
    "complete_reviewer_closeout",
)

REQUIRED_PRE_EXECUTION_CHECKS = (
    "reviewer_approval",
    "source_reference",
    "source_status_boundary",
    "evidence_envelope",
    "audit_envelope",
    "rollback_removal_policy",
    "sensitive_data_review",
    "no_overstatement_check",
    "explicit_execution_authorisation",
)

REQUIRED_POST_EXECUTION_CHECKS = (
    "evidence_record_verification",
    "corpus_mutation_verification",
    "rollback_removal_evidence",
    "sensitive_data_confirmation",
    "reviewer_closeout",
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
class ControlledDurableIntakeFirstCandidateExecutionDesignResult:
    design_id: str
    candidate_id: str
    candidate_type: str
    design_status: str
    candidate_authorised_for_future_execution: bool
    durable_intake_execution_authorised_now: bool
    durable_intake_performed: bool
    corpus_mutation_performed: bool
    db_write_performed: bool
    code_evidence_ingestion_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    required_execution_steps: tuple[str, ...]
    required_pre_execution_checks: tuple[str, ...]
    required_post_execution_checks: tuple[str, ...]
    rollback_or_removal_plan_required: bool
    reviewer_confirmation_required: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_intake_first_candidate_execution_design(
    authorisation_gate_metadata: dict[str, Any] | None,
    candidate_eligibility_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_controlled_durable_intake_first_candidate_execution_design(
        authorisation_gate_metadata,
        candidate_eligibility_metadata,
    )


def evaluate_controlled_durable_intake_first_candidate_execution_design(
    authorisation_gate_metadata: dict[str, Any] | None,
    candidate_eligibility_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Design a later first-candidate durable intake execution without action."""

    gate = authorisation_gate_metadata or {}
    eligibility = candidate_eligibility_metadata or {}
    combined = {**eligibility, **gate}
    blocked = _blocked_status(combined)
    status = blocked or _design_status(gate, eligibility)
    candidate_id = str(
        gate.get("candidate_id") or eligibility.get("candidate_id") or ""
    )
    candidate_type = str(
        gate.get("candidate_type")
        or eligibility.get("candidate_type")
        or UNKNOWN_REQUIRES_REVIEW
    )
    future_authorised = status == DURABLE_INTAKE_EXECUTION_DESIGN_READY

    material = {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "status": status,
        "gate_status": gate.get("authorisation_status"),
        "eligibility_status": eligibility.get("eligibility_status"),
    }

    return ControlledDurableIntakeFirstCandidateExecutionDesignResult(
        design_id=str(combined.get("design_id") or _stable_id(material)),
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        design_status=status,
        candidate_authorised_for_future_execution=future_authorised,
        durable_intake_execution_authorised_now=False,
        durable_intake_performed=False,
        corpus_mutation_performed=False,
        db_write_performed=False,
        code_evidence_ingestion_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        required_execution_steps=REQUIRED_EXECUTION_STEPS,
        required_pre_execution_checks=REQUIRED_PRE_EXECUTION_CHECKS,
        required_post_execution_checks=REQUIRED_POST_EXECUTION_CHECKS,
        rollback_or_removal_plan_required=True,
        reviewer_confirmation_required=True,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _design_status(gate: dict[str, Any], eligibility: dict[str, Any]) -> str:
    if not gate:
        return NEEDS_AUTHORISATION_GATE
    if not eligibility:
        return NEEDS_CANDIDATE_ELIGIBILITY
    if gate.get("authorisation_status") != AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION:
        return NEEDS_AUTHORISATION_GATE
    if eligibility.get("eligibility_status") != DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE:
        return NEEDS_CANDIDATE_ELIGIBILITY
    if gate.get("eligible_for_future_durable_intake_execution") is not True:
        return NEEDS_AUTHORISATION_GATE
    if eligibility.get("eligible_for_authorisation_gate") is not True:
        return NEEDS_CANDIDATE_ELIGIBILITY
    if gate.get("reviewer_confirmation_present") is False:
        return NEEDS_REVIEWER_CONFIRMATION
    if eligibility.get("reviewer_confirmation_present") is False:
        return NEEDS_REVIEWER_CONFIRMATION
    return DURABLE_INTAKE_EXECUTION_DESIGN_READY


def _blocked_status(metadata: dict[str, Any]) -> str | None:
    upstream_statuses = (
        str(metadata.get("authorisation_status") or ""),
        str(metadata.get("eligibility_status") or ""),
        str(metadata.get("design_status") or ""),
    )
    if BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM in upstream_statuses:
        return BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    if BLOCKED_MUTATION_OR_DB_WRITE_CLAIM in upstream_statuses:
        return BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
    if BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT in upstream_statuses:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if any(bool(metadata.get(key)) for key in DURABLE_INTAKE_PERFORMED_CLAIM_KEYS):
        return BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    if any(bool(metadata.get(key)) for key in MUTATION_OR_DB_WRITE_CLAIM_KEYS):
        return BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    return None


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_EXECUTION_DESIGN_READY:
        return (
            "First-candidate durable-intake execution design metadata is ready "
            "for review only. Durable intake is not authorised now and no action "
            "was performed."
        )
    if status.startswith("BLOCKED"):
        return (
            "Execution design metadata includes a prohibited ingestion, mutation, "
            "DB, runtime, deployment, or production claim. No action was performed."
        )
    if status == NEEDS_AUTHORISATION_GATE:
        return "A complete future-execution authorisation gate is required."
    if status == NEEDS_CANDIDATE_ELIGIBILITY:
        return "Complete durable-intake candidate eligibility metadata is required."
    if status == NEEDS_REVIEWER_CONFIRMATION:
        return "Reviewer confirmation is required before execution design can proceed."
    return "Execution design metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-first-candidate-execution-design-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_durable_evidence_intake_design_verification_service import (
    BLOCKED_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY = (
    "DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY"
)
NEEDS_VERIFICATION = "NEEDS_VERIFICATION"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

RECOMMENDED_NEXT_SLICE = (
    "Controlled Durable Evidence Intake Authorisation Decision / Keep Minerva "
    "Paused v0.1"
)

REMAINING_WORK = (
    "Make an explicit future durable-intake authorisation decision.",
    "Keep Minerva paused if durable intake is not explicitly authorised.",
)

REQUIRED_CAVEATS = (
    "Closeout readiness applies to the durable intake design phase only.",
    "Durable evidence intake is not authorised now.",
    "Corpus mutation, DB writes, Code Evidence ingestion, live retrieval, live LLM use, and final answer generation remain unauthorised.",
    "Runtime, deployment, and production readiness claims are not permitted.",
)


@dataclass(frozen=True)
class ControlledDurableEvidenceIntakeCloseoutReadinessResult:
    readiness_id: str
    readiness_status: str
    ready_for_design_phase_closeout: bool
    durable_design_verified: bool
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_slice: str
    durable_intake_authorised_now: bool
    corpus_mutation_authorised_now: bool
    db_write_authorised_now: bool
    code_evidence_ingestion_authorised_now: bool
    live_retrieval_authorised_now: bool
    live_llm_authorised_now: bool
    final_answer_generation_authorised_now: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_evidence_intake_closeout_readiness(
    verification_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return deterministic design closeout readiness without runtime action."""

    metadata = verification_metadata or {}
    durable_design_verified = (
        metadata.get("verification_status")
        == DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED
        and metadata.get("design_verified") is True
        and metadata.get("authorisation_requirements_verified") is True
        and metadata.get("audit_envelope_verified") is True
    )
    status = _readiness_status(metadata, durable_design_verified)
    ready = status == DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY
    material = {
        "status": status,
        "durable_design_verified": durable_design_verified,
        "ready": ready,
    }

    return ControlledDurableEvidenceIntakeCloseoutReadinessResult(
        readiness_id=_stable_id(material),
        readiness_status=status,
        ready_for_design_phase_closeout=ready,
        durable_design_verified=durable_design_verified,
        remaining_work=REMAINING_WORK,
        next_decision_point="Explicitly authorise future durable intake or keep Minerva paused.",
        recommended_next_slice=RECOMMENDED_NEXT_SLICE,
        durable_intake_authorised_now=False,
        corpus_mutation_authorised_now=False,
        db_write_authorised_now=False,
        code_evidence_ingestion_authorised_now=False,
        live_retrieval_authorised_now=False,
        live_llm_authorised_now=False,
        final_answer_generation_authorised_now=False,
        production_readiness_claim_permitted=False,
        deployment_readiness_claim_permitted=False,
        runtime_readiness_claim_permitted=False,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _readiness_status(metadata: dict[str, Any], durable_design_verified: bool) -> str:
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    if _claims_runtime_or_production(metadata):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if _claims_durable_ingestion(metadata):
        return BLOCKED_DURABLE_INGESTION_CLAIM
    if durable_design_verified:
        return DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY
    return NEEDS_VERIFICATION


def _claims_durable_ingestion(metadata: dict[str, Any]) -> bool:
    claim_keys = (
        "durable_intake_authorised_now",
        "corpus_mutation_authorised_now",
        "db_write_authorised_now",
        "code_evidence_ingestion_authorised_now",
    )
    return any(bool(metadata.get(key)) for key in claim_keys)


def _claims_runtime_or_production(metadata: dict[str, Any]) -> bool:
    claim_keys = (
        "live_retrieval_authorised_now",
        "live_llm_authorised_now",
        "final_answer_generation_authorised_now",
        "production_readiness_claim_permitted",
        "deployment_readiness_claim_permitted",
        "runtime_readiness_claim_permitted",
    )
    return any(bool(metadata.get(key)) for key in claim_keys)


def _explanation(status: str) -> str:
    if status == DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY:
        return (
            "The durable intake design is verified and ready for design-phase "
            "closeout only. No durable intake or runtime action is authorised."
        )
    if status == BLOCKED_DURABLE_INGESTION_CLAIM:
        return "Closeout readiness blocked an unauthorised durable ingestion or mutation claim."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Closeout readiness blocked a runtime, deployment, or production overstatement."
    return "Closeout readiness requires verified durable intake design metadata."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-evidence-intake-closeout-readiness-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

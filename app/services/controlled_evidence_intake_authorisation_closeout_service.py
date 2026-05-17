import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    FIRST_CANDIDATE_REVIEW_READY,
)


CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY = (
    "CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_INGESTION_CLAIM = "BLOCKED_MUTATION_OR_INGESTION_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"

PHASE_NAME = "Controlled Evidence Intake Authorisation / First Candidate Review Closeout v0.1"
PROGRESS_BEFORE_SLICE = "Approximately 55-65% complete"
PROGRESS_AFTER_SLICE = "Approximately 90-100% complete"

COMPLETED_COMPONENTS = (
    "Controlled evidence intake authorisation gate service",
    "Controlled evidence intake first-candidate service",
    "Controlled evidence intake first-candidate review service",
    "Controlled evidence intake authorisation closeout service",
)

REMAINING_WORK = (
    "Choose whether to execute a future no-mutation intake attempt for the reviewed candidate.",
    "Or keep Minerva paused while award recovery continues.",
)

NEXT_PHASE_OPTIONS = (
    "Option A: First no-mutation intake execution with explicit authorisation.",
    "Option B: Additional candidate review before any intake execution.",
    "Option C: External evidence summary catalogue without ingestion or corpus mutation.",
    "Option D: Keep Minerva paused while award recovery continues.",
)

INGESTION_OR_MUTATION_CLAIM_KEYS = (
    "intake_authorised_now",
    "candidate_authorised_for_intake_now",
    "evidence_ingestion_performed",
    "corpus_mutation_performed",
    "code_evidence_ingestion_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "db_write_performed",
    "db_access_or_write_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "runtime_integration_authorised",
    "production_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "runtime_readiness_claim_permitted",
)

EXPOSURE_OR_FINAL_ANSWER_CLAIM_KEYS = (
    "final_answer_generation_performed",
    "chat_or_endpoint_exposure_authorised",
    "chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeAuthorisationCloseoutResult:
    closeout_id: str
    phase_name: str
    phase_status: str
    progress_before_slice: str
    progress_after_slice: str
    first_candidate_review_complete: bool
    first_candidate_ready_for_future_no_mutation_intake: bool
    intake_authorised_now: bool
    evidence_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_access_or_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    chat_or_endpoint_exposure_authorised: bool
    runtime_integration_authorised: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def closeout_controlled_evidence_intake_authorisation_phase(
    first_candidate_review_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Close out the authorisation phase without enabling intake or runtime paths."""

    review = first_candidate_review_metadata or {}
    blocked = _blocked_status(review)
    ready = (
        not blocked
        and review.get("review_status") == FIRST_CANDIDATE_REVIEW_READY
        and review.get("candidate_eligible_for_future_no_mutation_intake") is True
    )
    status = _phase_status(review, blocked, ready)
    material = {
        "phase_name": PHASE_NAME,
        "phase_status": status,
        "review_id": review.get("review_id") or "",
        "candidate_id": review.get("candidate_id") or "",
    }

    return ControlledEvidenceIntakeAuthorisationCloseoutResult(
        closeout_id=_stable_id(material),
        phase_name=PHASE_NAME,
        phase_status=status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        first_candidate_review_complete=ready,
        first_candidate_ready_for_future_no_mutation_intake=ready,
        intake_authorised_now=False,
        evidence_ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_access_or_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        chat_or_endpoint_exposure_authorised=False,
        runtime_integration_authorised=False,
        production_readiness_claim_permitted=False,
        deployment_readiness_claim_permitted=False,
        runtime_readiness_claim_permitted=False,
        completed_components=COMPLETED_COMPONENTS,
        remaining_work=REMAINING_WORK,
        next_decision_point=(
            "Decide whether to authorise a future first no-mutation intake "
            "execution or keep Minerva paused."
        ),
        recommended_next_phase_options=NEXT_PHASE_OPTIONS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def build_controlled_evidence_intake_authorisation_closeout(
    first_candidate_review_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return closeout_controlled_evidence_intake_authorisation_phase(
        first_candidate_review_metadata
    )


def _blocked_status(review: dict[str, Any]) -> str:
    if _has_claim(review, INGESTION_OR_MUTATION_CLAIM_KEYS):
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if _has_claim(review, EXPOSURE_OR_FINAL_ANSWER_CLAIM_KEYS):
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if _has_claim(review, RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    review_status = str(review.get("review_status") or "")
    if "MUTATION_OR_INGESTION" in review_status:
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if "RUNTIME_OR_PRODUCTION" in review_status:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    return ""


def _phase_status(review: dict[str, Any], blocked: str, ready: bool) -> str:
    if blocked:
        return blocked
    if not review or not ready:
        return NEEDS_REVIEW
    return CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY


def _explanation(status: str) -> str:
    if status == CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY:
        return (
            "The first-candidate review is complete for future no-mutation intake "
            "eligibility only. Intake, ingestion, corpus mutation, Code Evidence "
            "ingestion, DB work, live retrieval, live LLM use, final answers, "
            "exposure, runtime integration, deployment, and production remain "
            "unauthorised."
        )
    if status.startswith("BLOCKED"):
        return (
            "The closeout detected a blocked ingestion, mutation, exposure, "
            "runtime, deployment, or production claim; no action was performed."
        )
    return (
        "The first-candidate review is incomplete or not ready and requires "
        "controlled review before a closeout-ready status can be recorded."
    )


def _has_claim(metadata: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-authorisation-closeout-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

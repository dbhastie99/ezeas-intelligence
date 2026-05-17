import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_first_no_mutation_intake_execution_review_service import (
    NO_MUTATION_EXECUTION_REVIEW_READY,
)


NO_MUTATION_VERIFICATION_PACK_READY = "NO_MUTATION_VERIFICATION_PACK_READY"
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_INGESTION_CLAIM = "BLOCKED_MUTATION_OR_INGESTION_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

MUTATION_REVIEW_FLAGS = (
    "durable_ingestion_performed",
    "corpus_mutation_performed",
    "code_evidence_ingestion_performed",
)

RUNTIME_OR_PRODUCTION_REVIEW_FLAGS = (
    "db_access_performed",
    "db_write_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "runtime_integration_authorised",
    "production_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "runtime_readiness_claim_permitted",
)

EXPOSURE_OR_FINAL_ANSWER_REVIEW_FLAGS = (
    "final_answer_generation_performed",
    "chat_or_endpoint_exposure_authorised",
)

REQUIRED_CAVEATS = (
    "Verification pack is deterministic closeout metadata only.",
    "Ready for phase closeout does not authorise durable ingestion.",
    "Durable ingestion, corpus mutation, Code Evidence ingestion, DB access, DB write, live retrieval, live LLM use, final answer generation, chat exposure, endpoint exposure, runtime integration, deployment, and production readiness remain unauthorised.",
)

NEXT_DECISION_POINT = (
    "Close out the first no-mutation intake execution review, or deliberately "
    "authorise a separate future durable-ingestion decision gate."
)

RECOMMENDED_NEXT_SLICE = (
    "Controlled First No-Mutation Intake Execution Review Closeout / Future "
    "Durable-Ingestion Decision Gate v0.1"
)


@dataclass(frozen=True)
class ControlledNoMutationIntakeVerificationPackResult:
    verification_pack_id: str
    source_review_id: str
    verification_status: str
    no_mutation_verified: bool
    review_complete: bool
    safety_failures: tuple[str, ...]
    mutation_failures: tuple[str, ...]
    runtime_or_production_failures: tuple[str, ...]
    exposure_or_final_answer_failures: tuple[str, ...]
    ready_for_phase_closeout: bool
    ready_for_durable_ingestion: bool
    required_caveats: tuple[str, ...]
    next_decision_point: str
    recommended_next_slice: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_no_mutation_intake_verification_pack(
    execution_review_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build deterministic closeout verification metadata from execution review output."""

    review = execution_review_metadata or {}
    mutation_failures = _mutation_failures(review)
    runtime_failures = _runtime_or_production_failures(review)
    exposure_failures = _exposure_or_final_answer_failures(review)
    safety_failures = _safety_failures(
        review,
        mutation_failures,
        runtime_failures,
        exposure_failures,
    )
    status = _verification_status(
        review,
        mutation_failures,
        runtime_failures,
        exposure_failures,
        safety_failures,
    )
    review_complete = (
        status == NO_MUTATION_VERIFICATION_PACK_READY
        and review.get("review_status") == NO_MUTATION_EXECUTION_REVIEW_READY
        and review.get("execution_review_complete") is True
        and review.get("evidence_envelope_review_complete") is True
    )
    no_mutation_verified = (
        review_complete
        and review.get("no_mutation_verified") is True
        and not mutation_failures
        and not runtime_failures
        and not exposure_failures
    )
    material = {
        "source_review_id": str(review.get("review_id") or ""),
        "status": status,
        "mutation_failures": mutation_failures,
        "runtime_failures": runtime_failures,
        "exposure_failures": exposure_failures,
        "safety_failures": safety_failures,
    }

    return ControlledNoMutationIntakeVerificationPackResult(
        verification_pack_id=_stable_id(material),
        source_review_id=str(review.get("review_id") or ""),
        verification_status=status,
        no_mutation_verified=no_mutation_verified,
        review_complete=review_complete,
        safety_failures=safety_failures,
        mutation_failures=mutation_failures,
        runtime_or_production_failures=runtime_failures,
        exposure_or_final_answer_failures=exposure_failures,
        ready_for_phase_closeout=status == NO_MUTATION_VERIFICATION_PACK_READY,
        ready_for_durable_ingestion=False,
        required_caveats=_required_caveats(review),
        next_decision_point=NEXT_DECISION_POINT,
        recommended_next_slice=RECOMMENDED_NEXT_SLICE,
        no_action_attestation=str(review.get("no_action_attestation") or NO_ACTION_ATTESTATION),
        explanation=_explanation(status),
    ).to_dict()


def _mutation_failures(review: dict[str, Any]) -> tuple[str, ...]:
    return tuple(key for key in MUTATION_REVIEW_FLAGS if bool(review.get(key)))


def _runtime_or_production_failures(review: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        key for key in RUNTIME_OR_PRODUCTION_REVIEW_FLAGS if bool(review.get(key))
    )


def _exposure_or_final_answer_failures(review: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        key for key in EXPOSURE_OR_FINAL_ANSWER_REVIEW_FLAGS if bool(review.get(key))
    )


def _safety_failures(
    review: dict[str, Any],
    mutation_failures: tuple[str, ...],
    runtime_failures: tuple[str, ...],
    exposure_failures: tuple[str, ...],
) -> tuple[str, ...]:
    failures: list[str] = []
    if not review:
        failures.append("missing_review_metadata")
    if review and not review.get("review_id"):
        failures.append("missing_review_id")
    if review and review.get("review_status") != NO_MUTATION_EXECUTION_REVIEW_READY:
        failures.append("source_review_not_ready")
    if review and review.get("execution_review_complete") is not True:
        failures.append("execution_review_incomplete")
    if review and review.get("evidence_envelope_review_complete") is not True:
        failures.append("evidence_envelope_review_incomplete")
    if review and review.get("no_mutation_verified") is not True:
        failures.append("no_mutation_not_verified")
    if mutation_failures:
        failures.append("mutation_or_ingestion_failure")
    if runtime_failures:
        failures.append("runtime_or_production_failure")
    if exposure_failures:
        failures.append("exposure_or_final_answer_failure")
    return tuple(dict.fromkeys(failures))


def _verification_status(
    review: dict[str, Any],
    mutation_failures: tuple[str, ...],
    runtime_failures: tuple[str, ...],
    exposure_failures: tuple[str, ...],
    safety_failures: tuple[str, ...],
) -> str:
    if mutation_failures:
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if exposure_failures:
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if runtime_failures:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if _review_status_claims_mutation_or_ingestion(review):
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if _review_status_claims_exposure_or_final_answer(review):
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if _review_status_claims_runtime_or_production(review):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not review:
        return UNKNOWN_REQUIRES_REVIEW
    if safety_failures:
        return NEEDS_REVIEW
    return NO_MUTATION_VERIFICATION_PACK_READY


def _required_caveats(review: dict[str, Any]) -> tuple[str, ...]:
    caveats = [
        *[str(item) for item in _as_tuple(review.get("required_caveats"))],
        *REQUIRED_CAVEATS,
    ]
    return tuple(dict.fromkeys(item for item in caveats if item))


def _explanation(status: str) -> str:
    if status == NO_MUTATION_VERIFICATION_PACK_READY:
        return (
            "The execution review is complete and verifies the first no-mutation "
            "intake execution and evidence envelope as review-only metadata. "
            "The pack is ready for phase closeout, not durable ingestion."
        )
    if status == BLOCKED_MUTATION_OR_INGESTION_CLAIM:
        return (
            "The review metadata contains durable ingestion, corpus mutation, "
            "or Code Evidence ingestion failure signals."
        )
    if status == BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM:
        return (
            "The review metadata contains final answer generation or chat, "
            "endpoint, or route exposure failure signals."
        )
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return (
            "The review metadata contains DB, live retrieval, live LLM, runtime, "
            "deployment, or production overstatement failure signals."
        )
    return "The review metadata is missing, incomplete, or requires review."


def _review_status_claims_mutation_or_ingestion(review: dict[str, Any]) -> bool:
    return "MUTATION_OR" in str(review.get("review_status") or "")


def _review_status_claims_runtime_or_production(review: dict[str, Any]) -> bool:
    return "RUNTIME_OR_PRODUCTION" in str(review.get("review_status") or "")


def _review_status_claims_exposure_or_final_answer(review: dict[str, Any]) -> bool:
    status = str(review.get("review_status") or "")
    return "EXPOSURE_OR_FINAL_ANSWER" in status


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    return (value,)


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-no-mutation-intake-verification-pack-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

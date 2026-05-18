import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_answer_synthesis_rehearsal_service import (
    CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


CONTROLLED_ANSWER_REVIEW_READY = "CONTROLLED_ANSWER_REVIEW_READY"
NEEDS_REHEARSAL = "NEEDS_REHEARSAL"
NEEDS_REVIEW_CHECKS = "NEEDS_REVIEW_CHECKS"
BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM = (
    "BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_REVIEW_CHECKS = (
    "source references",
    "caveats",
    "prohibited claim scan",
    "evidence/implementation boundary",
    "no-runtime claim",
    "still-to-do clarity",
)
FINAL_ANSWER_OR_CHAT_EXPOSURE_KEYS = (
    "final_answer_generated",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "user_facing_answer_generated",
)
RUNTIME_OR_PRODUCTION_KEYS = (
    "runtime_ready",
    "runtime_authorised",
    "deployment_ready",
    "deployment_authorised",
    "production_ready",
    "production_authorised",
)


@dataclass(frozen=True)
class ControlledAnswerReviewMetadataResult:
    review_id: str
    source_rehearsal_id: str
    review_status: str
    answer_skeleton_ready_for_human_review: bool
    final_answer_generated: bool
    live_llm_performed: bool
    chat_exposure_authorised: bool
    required_review_checks: tuple[str, ...]
    missing_review_checks: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    reviewer_confirmation_required: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_answer_review_metadata(
    rehearsal_output: dict[str, Any] | None,
) -> dict[str, Any]:
    return prepare_controlled_answer_review_metadata(rehearsal_output)


def prepare_controlled_answer_review_metadata(
    rehearsal_output: dict[str, Any] | None,
) -> dict[str, Any]:
    rehearsal = rehearsal_output or {}
    missing_checks = _missing_review_checks(rehearsal)
    status = _review_status(rehearsal, missing_checks)
    ready = status == CONTROLLED_ANSWER_REVIEW_READY
    material = {
        "source_rehearsal_id": rehearsal.get("rehearsal_id"),
        "rehearsal_status": rehearsal.get("rehearsal_status"),
        "missing_checks": missing_checks,
        "status": status,
    }

    return ControlledAnswerReviewMetadataResult(
        review_id=str(rehearsal.get("review_id") or _stable_id(material)),
        source_rehearsal_id=str(rehearsal.get("rehearsal_id") or ""),
        review_status=status,
        answer_skeleton_ready_for_human_review=ready,
        final_answer_generated=False,
        live_llm_performed=False,
        chat_exposure_authorised=False,
        required_review_checks=REQUIRED_REVIEW_CHECKS,
        missing_review_checks=missing_checks,
        blocked_reasons=_blocked_reasons(status),
        reviewer_confirmation_required=True,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _review_status(
    rehearsal: dict[str, Any],
    missing_checks: tuple[str, ...],
) -> str:
    if any(bool(rehearsal.get(key)) for key in FINAL_ANSWER_OR_CHAT_EXPOSURE_KEYS):
        return BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM
    if bool(rehearsal.get("live_llm_performed")):
        return BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM
    if any(bool(rehearsal.get(key)) for key in RUNTIME_OR_PRODUCTION_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if rehearsal.get("rehearsal_status") != CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY:
        return NEEDS_REHEARSAL
    if missing_checks:
        return NEEDS_REVIEW_CHECKS
    return CONTROLLED_ANSWER_REVIEW_READY


def _missing_review_checks(rehearsal: dict[str, Any]) -> tuple[str, ...]:
    missing = []
    if not rehearsal.get("evidence_references_used"):
        missing.append("source references")
    if not rehearsal.get("required_caveats_included"):
        missing.append("caveats")
    if rehearsal.get("prohibited_claims_detected"):
        missing.append("prohibited claim scan")
    sections = tuple(rehearsal.get("safe_answer_sections") or tuple())
    if "evidence boundaries" not in sections:
        missing.append("evidence/implementation boundary")
    caveats = tuple(rehearsal.get("required_caveats_included") or tuple())
    if "no-runtime-claim" not in caveats:
        missing.append("no-runtime claim")
    if "still-to-do" not in sections:
        missing.append("still-to-do clarity")
    return tuple(missing)


def _blocked_reasons(status: str) -> tuple[str, ...]:
    if status == CONTROLLED_ANSWER_REVIEW_READY:
        return tuple()
    return (status,)


def _explanation(status: str) -> str:
    if status == CONTROLLED_ANSWER_REVIEW_READY:
        return "Controlled answer review metadata is ready for human review of the skeleton only; reviewer confirmation is required and no final answer, live LLM, chat, DB, runtime, or production action is authorised."
    if status == BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM:
        return "Controlled answer review metadata blocks final answer, live LLM, or chat exposure claims."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Controlled answer review metadata blocks runtime, deployment, or production overstatement."
    if status == NEEDS_REHEARSAL:
        return "Controlled answer review metadata requires a ready synthesis rehearsal."
    if status == NEEDS_REVIEW_CHECKS:
        return "Controlled answer review metadata requires all review checks to be present before human review."
    return "Controlled answer review metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-answer-review-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

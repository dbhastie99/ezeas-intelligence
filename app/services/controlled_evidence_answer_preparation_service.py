import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.developer_log_evidence_retrieval_metadata_service import (
    DEVELOPER_LOG_RETRIEVAL_METADATA_READY,
)


CONTROLLED_ANSWER_PREPARATION_READY = "CONTROLLED_ANSWER_PREPARATION_READY"
NEEDS_RETRIEVAL_METADATA = "NEEDS_RETRIEVAL_METADATA"
NEEDS_SOURCE_REFERENCES = "NEEDS_SOURCE_REFERENCES"
NEEDS_CAVEATS = "NEEDS_CAVEATS"
BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM = (
    "BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_ANSWER_CAVEATS = (
    "evidence-boundary",
    "implementation-status-boundary",
    "no-runtime-claim",
    "source-reference requirement",
)
SAFE_ANSWER_MODES = (
    "status-summary",
    "decision-summary",
    "risk-summary",
    "still-to-do-summary",
)
PROHIBITED_CLAIMS = (
    "final natural-language answer generated",
    "live LLM performed",
    "chat exposure authorised",
    "runtime readiness",
    "deployment readiness",
    "production readiness",
    "DB read or write performed",
    "live corpus mutation performed",
)
FINAL_ANSWER_OR_LIVE_LLM_KEYS = (
    "final_answer_generated",
    "final_answer_generation_performed",
    "live_llm_performed",
)
RUNTIME_OR_PRODUCTION_KEYS = (
    "chat_exposure_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_ready",
    "deployment_ready",
    "production_ready",
)


@dataclass(frozen=True)
class ControlledEvidenceAnswerPreparationResult:
    preparation_id: str
    source_metadata_id: str
    preparation_status: str
    answer_ready_for_controlled_synthesis: bool
    final_answer_generated: bool
    live_llm_performed: bool
    chat_exposure_authorised: bool
    required_answer_caveats: tuple[str, ...]
    required_source_references: tuple[str, ...]
    prohibited_claims: tuple[str, ...]
    safe_answer_modes: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_evidence_answer_preparation(
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return prepare_controlled_evidence_answer_preparation(retrieval_metadata)


def prepare_controlled_evidence_answer_preparation(
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = retrieval_metadata or {}
    required_source_references = _required_source_references(metadata)
    status = _preparation_status(metadata, required_source_references)
    ready = status == CONTROLLED_ANSWER_PREPARATION_READY
    blocked_reasons = _blocked_reasons(status)
    material = {
        "source_metadata_id": metadata.get("metadata_id"),
        "metadata_status": metadata.get("metadata_status"),
        "required_source_references": required_source_references,
        "status": status,
    }

    return ControlledEvidenceAnswerPreparationResult(
        preparation_id=str(metadata.get("preparation_id") or _stable_id(material)),
        source_metadata_id=str(metadata.get("metadata_id") or ""),
        preparation_status=status,
        answer_ready_for_controlled_synthesis=ready,
        final_answer_generated=False,
        live_llm_performed=False,
        chat_exposure_authorised=False,
        required_answer_caveats=REQUIRED_ANSWER_CAVEATS,
        required_source_references=required_source_references,
        prohibited_claims=PROHIBITED_CLAIMS,
        safe_answer_modes=SAFE_ANSWER_MODES,
        blocked_reasons=blocked_reasons,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _preparation_status(
    metadata: dict[str, Any],
    required_source_references: tuple[str, ...],
) -> str:
    if any(bool(metadata.get(key)) for key in FINAL_ANSWER_OR_LIVE_LLM_KEYS):
        return BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if metadata.get("metadata_status") != DEVELOPER_LOG_RETRIEVAL_METADATA_READY:
        return NEEDS_RETRIEVAL_METADATA
    if not required_source_references:
        return NEEDS_SOURCE_REFERENCES
    if not metadata.get("answer_boundaries"):
        return NEEDS_CAVEATS
    return CONTROLLED_ANSWER_PREPARATION_READY


def _required_source_references(metadata: dict[str, Any]) -> tuple[str, ...]:
    source_reference = str(metadata.get("source_reference") or "")
    return (source_reference,) if source_reference else tuple()


def _blocked_reasons(status: str) -> tuple[str, ...]:
    if status == CONTROLLED_ANSWER_PREPARATION_READY:
        return tuple()
    return (status,)


def _explanation(status: str) -> str:
    if status == CONTROLLED_ANSWER_PREPARATION_READY:
        return "Controlled answer preparation metadata is ready for bounded synthesis only; no final answer, live LLM, chat, DB, runtime, or production action is authorised."
    if status == BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM:
        return "Answer preparation metadata contains a prohibited final-answer or live LLM claim."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Answer preparation metadata contains a prohibited runtime, deployment, production, or chat exposure claim."
    if status == NEEDS_RETRIEVAL_METADATA:
        return "Controlled answer preparation requires ready retrieval metadata."
    if status == NEEDS_SOURCE_REFERENCES:
        return "Controlled answer preparation requires source references."
    if status == NEEDS_CAVEATS:
        return "Controlled answer preparation requires answer caveats and boundaries."
    return "Controlled answer preparation metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-answer-preparation-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

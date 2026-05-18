import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_answer_preparation_service import (
    CONTROLLED_ANSWER_PREPARATION_READY,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.developer_log_evidence_retrieval_metadata_service import (
    DEVELOPER_LOG_RETRIEVAL_METADATA_READY,
)


CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY = (
    "CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY"
)
NEEDS_ANSWER_PREPARATION = "NEEDS_ANSWER_PREPARATION"
NEEDS_RETRIEVAL_METADATA = "NEEDS_RETRIEVAL_METADATA"
NEEDS_SOURCE_REFERENCES = "NEEDS_SOURCE_REFERENCES"
BLOCKED_PROHIBITED_CLAIMS = "BLOCKED_PROHIBITED_CLAIMS"
BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM = (
    "BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

SAFE_ANSWER_SECTIONS = (
    "status summary",
    "decisions captured",
    "risks",
    "still-to-do",
    "evidence boundaries",
)
ANSWER_MODES_SUPPORTED = (
    "status-summary",
    "decision-summary",
    "risk-summary",
    "still-to-do-summary",
)
REQUIRED_CAVEATS = (
    "evidence-boundary",
    "implementation-status-boundary",
    "no-runtime-claim",
    "source-reference requirement",
)
PROHIBITED_CLAIM_KEYS = (
    "runtime_ready",
    "deployment_ready",
    "production_ready",
    "db_mutation_performed",
    "corpus_mutation_performed",
    "implementation_complete",
    "user_facing_enabled",
)
FINAL_ANSWER_OR_LIVE_LLM_KEYS = (
    "final_answer_generated",
    "final_answer_generation_performed",
    "live_llm_performed",
    "chat_exposure_authorised",
)


@dataclass(frozen=True)
class ControlledAnswerSynthesisRehearsalResult:
    rehearsal_id: str
    source_preparation_id: str
    source_metadata_id: str
    rehearsal_status: str
    answer_skeleton_prepared: bool
    final_answer_generated: bool
    live_llm_performed: bool
    chat_exposure_authorised: bool
    evidence_references_used: tuple[str, ...]
    required_caveats_included: tuple[str, ...]
    prohibited_claims_detected: tuple[str, ...]
    safe_answer_sections: tuple[str, ...]
    answer_modes_supported: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_answer_synthesis_rehearsal(
    answer_preparation_metadata: dict[str, Any] | None,
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return rehearse_controlled_answer_synthesis(
        answer_preparation_metadata,
        retrieval_metadata,
    )


def rehearse_controlled_answer_synthesis(
    answer_preparation_metadata: dict[str, Any] | None,
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    preparation = answer_preparation_metadata or {}
    metadata = retrieval_metadata or {}
    evidence_references = _evidence_references(preparation, metadata)
    prohibited_claims = _prohibited_claims_detected(preparation, metadata)
    status = _rehearsal_status(
        preparation,
        metadata,
        evidence_references,
        prohibited_claims,
    )
    ready = status == CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY
    material = {
        "source_preparation_id": preparation.get("preparation_id"),
        "source_metadata_id": metadata.get("metadata_id"),
        "evidence_references": evidence_references,
        "status": status,
    }

    return ControlledAnswerSynthesisRehearsalResult(
        rehearsal_id=str(preparation.get("rehearsal_id") or _stable_id(material)),
        source_preparation_id=str(preparation.get("preparation_id") or ""),
        source_metadata_id=str(metadata.get("metadata_id") or ""),
        rehearsal_status=status,
        answer_skeleton_prepared=ready,
        final_answer_generated=False,
        live_llm_performed=False,
        chat_exposure_authorised=False,
        evidence_references_used=evidence_references if ready else tuple(),
        required_caveats_included=REQUIRED_CAVEATS if ready else tuple(),
        prohibited_claims_detected=prohibited_claims,
        safe_answer_sections=SAFE_ANSWER_SECTIONS if ready else tuple(),
        answer_modes_supported=ANSWER_MODES_SUPPORTED if ready else tuple(),
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _rehearsal_status(
    preparation: dict[str, Any],
    metadata: dict[str, Any],
    evidence_references: tuple[str, ...],
    prohibited_claims: tuple[str, ...],
) -> str:
    if any(
        bool(source.get(key))
        for source in (preparation, metadata)
        for key in FINAL_ANSWER_OR_LIVE_LLM_KEYS
    ):
        return BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM
    if prohibited_claims:
        return BLOCKED_PROHIBITED_CLAIMS
    if preparation.get("preparation_status") != CONTROLLED_ANSWER_PREPARATION_READY:
        return NEEDS_ANSWER_PREPARATION
    if metadata.get("metadata_status") != DEVELOPER_LOG_RETRIEVAL_METADATA_READY:
        return NEEDS_RETRIEVAL_METADATA
    if not evidence_references:
        return NEEDS_SOURCE_REFERENCES
    return CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY


def _evidence_references(
    preparation: dict[str, Any],
    metadata: dict[str, Any],
) -> tuple[str, ...]:
    references = tuple(
        ref
        for ref in preparation.get("required_source_references", tuple())
        if ref
    )
    if references:
        return references
    source_reference = str(metadata.get("source_reference") or "")
    return (source_reference,) if source_reference else tuple()


def _prohibited_claims_detected(
    preparation: dict[str, Any],
    metadata: dict[str, Any],
) -> tuple[str, ...]:
    claims = [
        key
        for source in (preparation, metadata)
        for key in PROHIBITED_CLAIM_KEYS
        if bool(source.get(key))
    ]
    return tuple(sorted(set(claims)))


def _explanation(status: str) -> str:
    if status == CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY:
        return "Controlled answer synthesis rehearsal prepared an evidence-grounded answer skeleton only; no final answer, live LLM, chat, DB, runtime, or production action is authorised."
    if status == BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM:
        return "Controlled answer synthesis rehearsal blocks final-answer, live LLM, or chat exposure claims."
    if status == BLOCKED_PROHIBITED_CLAIMS:
        return "Controlled answer synthesis rehearsal detected prohibited evidence, implementation, runtime, production, mutation, or user-facing claims."
    if status == NEEDS_ANSWER_PREPARATION:
        return "Controlled answer synthesis rehearsal requires ready answer-preparation metadata."
    if status == NEEDS_RETRIEVAL_METADATA:
        return "Controlled answer synthesis rehearsal requires ready retrieval metadata."
    if status == NEEDS_SOURCE_REFERENCES:
        return "Controlled answer synthesis rehearsal requires source references."
    return "Controlled answer synthesis rehearsal is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-answer-synthesis-rehearsal-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

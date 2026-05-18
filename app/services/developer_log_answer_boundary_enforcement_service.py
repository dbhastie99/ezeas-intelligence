import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.developer_log_evidence_retrieval_metadata_service import (
    DEVELOPER_LOG_RETRIEVAL_METADATA_READY,
)


DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED = (
    "DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED"
)
NEEDS_RETRIEVAL_METADATA = "NEEDS_RETRIEVAL_METADATA"
BLOCKED_IMPLEMENTATION_OVERSTATEMENT = "BLOCKED_IMPLEMENTATION_OVERSTATEMENT"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_PHRASING_RULES = (
    "Use 'evidence says' only for claims directly supported by cited Developer Log evidence.",
    "Use 'project decided' only for decisions recorded by cited Developer Log evidence.",
    "Use 'implemented' only when implementation evidence is directly cited.",
    "Use 'verified' only when verification evidence is directly cited.",
    "Use 'still to do' for work not directly evidenced as implemented and verified.",
)
PROHIBITED_INFERENCES = (
    "implementation complete unless directly evidenced",
    "runtime enabled unless directly evidenced",
    "production-ready unless directly evidenced",
    "DB or corpus mutated unless directly evidenced",
    "user-facing unless directly evidenced",
)
IMPLEMENTATION_OVERSTATEMENT_KEYS = (
    "implementation_complete",
    "implemented_without_evidence",
)
RUNTIME_OR_PRODUCTION_OVERSTATEMENT_KEYS = (
    "runtime_enabled",
    "runtime_ready",
    "deployment_ready",
    "production_ready",
    "db_mutation_performed",
    "corpus_mutation_performed",
    "user_facing_enabled",
)


@dataclass(frozen=True)
class DeveloperLogAnswerBoundaryEnforcementResult:
    boundary_id: str
    source_metadata_id: str
    boundary_status: str
    evidence_boundary_enforced: bool
    implementation_status_boundary_enforced: bool
    runtime_status_boundary_enforced: bool
    production_status_boundary_enforced: bool
    required_phrasing_rules: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_developer_log_answer_boundary_enforcement(
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return enforce_developer_log_answer_boundaries(retrieval_metadata)


def enforce_developer_log_answer_boundaries(
    retrieval_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = retrieval_metadata or {}
    status = _boundary_status(metadata)
    enforced = status == DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED
    material = {
        "source_metadata_id": metadata.get("metadata_id"),
        "metadata_status": metadata.get("metadata_status"),
        "status": status,
    }

    return DeveloperLogAnswerBoundaryEnforcementResult(
        boundary_id=str(metadata.get("boundary_id") or _stable_id(material)),
        source_metadata_id=str(metadata.get("metadata_id") or ""),
        boundary_status=status,
        evidence_boundary_enforced=enforced,
        implementation_status_boundary_enforced=enforced,
        runtime_status_boundary_enforced=enforced,
        production_status_boundary_enforced=enforced,
        required_phrasing_rules=REQUIRED_PHRASING_RULES,
        prohibited_inferences=PROHIBITED_INFERENCES,
        blocked_reasons=_blocked_reasons(status),
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _boundary_status(metadata: dict[str, Any]) -> str:
    if any(bool(metadata.get(key)) for key in IMPLEMENTATION_OVERSTATEMENT_KEYS):
        return BLOCKED_IMPLEMENTATION_OVERSTATEMENT
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_OVERSTATEMENT_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if metadata.get("metadata_status") != DEVELOPER_LOG_RETRIEVAL_METADATA_READY:
        return NEEDS_RETRIEVAL_METADATA
    if metadata.get("evidence_type") != "DEVELOPER_LOG":
        return UNKNOWN_REQUIRES_REVIEW
    return DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED


def _blocked_reasons(status: str) -> tuple[str, ...]:
    if status == DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED:
        return tuple()
    return (status,)


def _explanation(status: str) -> str:
    if status == DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED:
        return "Developer Log answer boundaries are enforced for evidence, implementation, runtime, and production claims; no final answer, live LLM, chat, DB, runtime, or production action is authorised."
    if status == BLOCKED_IMPLEMENTATION_OVERSTATEMENT:
        return "Developer Log answer boundaries block implementation completion claims that are not directly evidenced."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Developer Log answer boundaries block runtime, production, DB, corpus, or user-facing overstatement."
    if status == NEEDS_RETRIEVAL_METADATA:
        return "Developer Log answer boundary enforcement requires ready retrieval metadata."
    return "Developer Log answer boundary enforcement is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "developer-log-answer-boundary-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

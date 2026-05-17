import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


READY_FOR_INTAKE_PLANNING = "READY_FOR_INTAKE_PLANNING"
NEEDS_SOURCE_CONTEXT = "NEEDS_SOURCE_CONTEXT"
NEEDS_STATUS_BOUNDARY = "NEEDS_STATUS_BOUNDARY"
NEEDS_TRUST_REVIEW = "NEEDS_TRUST_REVIEW"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
BLOCKED_UNAUTHORISED_INGESTION_CLAIM = "BLOCKED_UNAUTHORISED_INGESTION_CLAIM"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

UNKNOWN_VALUES = {"", "UNKNOWN", "UNKNOWN_REQUIRES_REVIEW", "UNTRUSTED", "REQUIRES_REVIEW"}

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "runtime_claim_permitted",
    "production_claim_permitted",
    "deployment_claim_permitted",
    "runtime_authorised",
    "production_authorised",
    "deployment_authorised",
)

NO_ACTION_ATTESTATION = (
    "No evidence ingestion, corpus mutation, runtime enablement, deployment, "
    "production use, DB access, live LLM use, endpoint exposure, final answer "
    "generation, or cross-repo runtime integration is authorised by this planning gate."
)


@dataclass(frozen=True)
class ControlledEvidenceIntakePlanningGateResult:
    gate_id: str
    gate_decision: str
    ready_for_future_intake_planning: bool
    ingestion_authorised_now: bool
    corpus_mutation_authorised_now: bool
    missing_prerequisites: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_evidence_intake_planning_gate(
    evidence_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Gate future evidence intake planning without authorising ingestion or mutation."""

    metadata = evidence_metadata or {}
    missing = _missing_prerequisites(metadata)
    blocked = _blocked_reasons(metadata)
    decision = _gate_decision(metadata, missing, blocked)
    ready = decision == READY_FOR_INTAKE_PLANNING
    caveats = _as_tuple(metadata.get("required_caveats"))

    material = {
        "category": metadata.get("evidence_category") or metadata.get("category") or "",
        "source_repo": metadata.get("source_repo") or "",
        "source_phase": metadata.get("source_phase") or "",
        "source_status": metadata.get("source_status") or metadata.get("status_boundary") or "",
        "trust_level": metadata.get("trust_level") or "",
        "missing": missing,
        "blocked": blocked,
        "caveats": caveats,
    }

    return ControlledEvidenceIntakePlanningGateResult(
        gate_id=str(metadata.get("gate_id") or _stable_id(material)),
        gate_decision=decision,
        ready_for_future_intake_planning=ready,
        ingestion_authorised_now=False,
        corpus_mutation_authorised_now=False,
        missing_prerequisites=missing,
        blocked_reasons=blocked,
        required_caveats=caveats,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(decision),
    ).to_dict()


def build_controlled_evidence_intake_planning_gate(
    evidence_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_controlled_evidence_intake_planning_gate(evidence_metadata)


def _missing_prerequisites(metadata: dict[str, Any]) -> tuple[str, ...]:
    missing: list[str] = []
    if _unknown(metadata.get("evidence_category") or metadata.get("category")):
        missing.append("evidence_category")
    if _unknown(metadata.get("source_repo")) or _unknown(metadata.get("source_phase")):
        missing.append("source_context")
    if _unknown(metadata.get("source_status") or metadata.get("status_boundary")):
        missing.append("status_boundary")
    if _unknown(metadata.get("trust_level")):
        missing.append("trust_level")
    if not _as_tuple(metadata.get("required_caveats")):
        missing.append("required_caveats")
    return tuple(missing)


def _blocked_reasons(metadata: dict[str, Any]) -> tuple[str, ...]:
    blocked: list[str] = []
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        blocked.append("runtime_or_production_overstatement")
    if bool(metadata.get("ingestion_authorised")) or bool(metadata.get("ingestion_authorised_now")):
        blocked.append("unauthorised_ingestion_claim")
    if bool(metadata.get("corpus_mutation_authorised")) or bool(metadata.get("corpus_mutation_authorised_now")):
        blocked.append("unauthorised_corpus_mutation_claim")
    return tuple(blocked)


def _gate_decision(
    metadata: dict[str, Any],
    missing: tuple[str, ...],
    blocked: tuple[str, ...],
) -> str:
    if "runtime_or_production_overstatement" in blocked:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if "unauthorised_ingestion_claim" in blocked or "unauthorised_corpus_mutation_claim" in blocked:
        return BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    if _unknown(metadata.get("evidence_category") or metadata.get("category")):
        return UNKNOWN_REQUIRES_REVIEW
    if "source_context" in missing:
        return NEEDS_SOURCE_CONTEXT
    if "status_boundary" in missing:
        return NEEDS_STATUS_BOUNDARY
    if "trust_level" in missing:
        return NEEDS_TRUST_REVIEW
    if missing:
        return UNKNOWN_REQUIRES_REVIEW
    return READY_FOR_INTAKE_PLANNING


def _explanation(decision: str) -> str:
    if decision == READY_FOR_INTAKE_PLANNING:
        return "Evidence metadata is ready for future intake planning only; ingestion and corpus mutation remain unauthorised now."
    if decision.startswith("BLOCKED"):
        return "Evidence metadata contains a blocked claim for this planning-only slice."
    return "Evidence metadata is incomplete or unknown and requires controlled review before future intake planning."


def _unknown(value: Any) -> bool:
    return str(value or "").strip().upper() in UNKNOWN_VALUES


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value else ()
    return tuple(str(item) for item in value)


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, default=str).encode("utf-8")
    return "evidence-intake-gate-" + hashlib.sha256(encoded).hexdigest()[:16]

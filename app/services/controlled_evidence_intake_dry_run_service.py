import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_planning_gate_service import (
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    NEEDS_SOURCE_CONTEXT,
    NEEDS_STATUS_BOUNDARY,
    NEEDS_TRUST_REVIEW,
    READY_FOR_INTAKE_PLANNING,
    UNKNOWN_REQUIRES_REVIEW,
    build_controlled_evidence_intake_planning_gate,
)
from app.services.controlled_evidence_intake_taxonomy_service import (
    build_controlled_evidence_intake_taxonomy,
)
from app.services.evidence_source_status_boundary_service import (
    build_evidence_source_status_boundary,
)


DRY_RUN_READY_FOR_FUTURE_INTAKE = "DRY_RUN_READY_FOR_FUTURE_INTAKE"
DRY_RUN_NEEDS_SOURCE_CONTEXT = "DRY_RUN_NEEDS_SOURCE_CONTEXT"
DRY_RUN_NEEDS_STATUS_BOUNDARY = "DRY_RUN_NEEDS_STATUS_BOUNDARY"
DRY_RUN_NEEDS_TRUST_REVIEW = "DRY_RUN_NEEDS_TRUST_REVIEW"
DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM = (
    "DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM"
)
DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM = (
    "DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
)
DRY_RUN_UNKNOWN_REQUIRES_REVIEW = "DRY_RUN_UNKNOWN_REQUIRES_REVIEW"

NO_ACTION_ATTESTATION = (
    "No evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, "
    "live retrieval, live LLM use, final natural-language answer generation, "
    "chat exposure, endpoint exposure, route registration, runtime integration, "
    "deployment, or production action was performed or authorised by this dry-run."
)

CORPUS_OR_CODE_EVIDENCE_CLAIM_KEYS = (
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "runtime_claim_permitted",
    "production_claim_permitted",
    "deployment_claim_permitted",
    "runtime_authorised",
    "production_authorised",
    "deployment_authorised",
    "runtime_readiness_claim_permitted",
    "production_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "db_write_performed",
    "db_write_authorised",
    "db_access_authorised",
    "db_read_performed",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_llm_performed",
    "live_llm_authorised",
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeDryRunResult:
    dry_run_id: str
    evidence_id: str
    evidence_category: str
    gate_decision: str
    source_status: str
    dry_run_decision: str
    would_ingest_in_future_if_authorised: bool
    ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    required_caveats: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_controlled_evidence_intake_dry_run(
    evidence_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    """Evaluate controlled evidence metadata without ingestion, mutation, or runtime calls."""

    metadata = _metadata_from_payload(evidence_payload)
    taxonomy = build_controlled_evidence_intake_taxonomy(metadata)
    enriched_metadata = _enriched_metadata(metadata, taxonomy)
    gate = build_controlled_evidence_intake_planning_gate(enriched_metadata)
    boundary = build_evidence_source_status_boundary(enriched_metadata)
    blocked_reasons = _blocked_reasons(enriched_metadata, gate)
    dry_run_decision = _dry_run_decision(gate, boundary, blocked_reasons)
    required_caveats = _dedupe(
        (
            *_as_tuple(taxonomy.get("required_caveats")),
            *_as_tuple(gate.get("required_caveats")),
            *_as_tuple(boundary.get("required_caveats")),
        )
    )
    prohibited_inferences = _dedupe(boundary.get("prohibited_inferences"))

    material = {
        "evidence_id": taxonomy["evidence_id"],
        "evidence_category": taxonomy["evidence_category"],
        "gate_decision": gate["gate_decision"],
        "source_status": boundary["source_status"],
        "dry_run_decision": dry_run_decision,
        "blocked_reasons": blocked_reasons,
        "required_caveats": required_caveats,
        "prohibited_inferences": prohibited_inferences,
    }

    return ControlledEvidenceIntakeDryRunResult(
        dry_run_id=str(metadata.get("dry_run_id") or _stable_id(material)),
        evidence_id=str(taxonomy["evidence_id"]),
        evidence_category=str(taxonomy["evidence_category"]),
        gate_decision=str(gate["gate_decision"]),
        source_status=str(boundary["source_status"]),
        dry_run_decision=dry_run_decision,
        would_ingest_in_future_if_authorised=dry_run_decision
        == DRY_RUN_READY_FOR_FUTURE_INTAKE,
        ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        required_caveats=required_caveats,
        blocked_reasons=blocked_reasons,
        prohibited_inferences=prohibited_inferences,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(dry_run_decision),
    ).to_dict()


def build_controlled_evidence_intake_dry_run(
    evidence_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    return run_controlled_evidence_intake_dry_run(evidence_payload)


def _metadata_from_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    if isinstance(payload.get("input_metadata"), dict):
        return dict(payload["input_metadata"])
    return dict(payload)


def _enriched_metadata(
    metadata: dict[str, Any],
    taxonomy: dict[str, Any],
) -> dict[str, Any]:
    enriched = dict(metadata)
    enriched.setdefault("evidence_id", taxonomy.get("evidence_id"))
    enriched.setdefault("evidence_category", taxonomy.get("evidence_category"))
    enriched.setdefault("trust_level", taxonomy.get("trust_level"))
    enriched.setdefault("required_caveats", taxonomy.get("required_caveats"))
    return enriched


def _blocked_reasons(
    metadata: dict[str, Any],
    gate: dict[str, Any],
) -> tuple[str, ...]:
    reasons = list(_as_tuple(gate.get("blocked_reasons")))
    if any(bool(metadata.get(key)) for key in CORPUS_OR_CODE_EVIDENCE_CLAIM_KEYS):
        reasons.append("corpus_or_code_evidence_claim")
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        reasons.append("runtime_or_production_overstatement")
    if bool(metadata.get("ingestion_performed")):
        reasons.append("unauthorised_ingestion_claim")
    return _dedupe(reasons)


def _dry_run_decision(
    gate: dict[str, Any],
    boundary: dict[str, Any],
    blocked_reasons: tuple[str, ...],
) -> str:
    if "corpus_or_code_evidence_claim" in blocked_reasons:
        return DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM
    if "unauthorised_corpus_mutation_claim" in blocked_reasons:
        return DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM
    if gate["gate_decision"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if "runtime_or_production_overstatement" in blocked_reasons:
        return DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if gate["gate_decision"] == BLOCKED_UNAUTHORISED_INGESTION_CLAIM:
        return DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    if "unauthorised_ingestion_claim" in blocked_reasons:
        return DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    if gate["gate_decision"] == NEEDS_SOURCE_CONTEXT:
        return DRY_RUN_NEEDS_SOURCE_CONTEXT
    if gate["gate_decision"] == NEEDS_STATUS_BOUNDARY:
        return DRY_RUN_NEEDS_STATUS_BOUNDARY
    if gate["gate_decision"] == NEEDS_TRUST_REVIEW:
        return DRY_RUN_NEEDS_TRUST_REVIEW
    if gate["gate_decision"] == READY_FOR_INTAKE_PLANNING and bool(boundary.get("evidence_exists")):
        return DRY_RUN_READY_FOR_FUTURE_INTAKE
    if gate["gate_decision"] == UNKNOWN_REQUIRES_REVIEW:
        return DRY_RUN_UNKNOWN_REQUIRES_REVIEW
    return DRY_RUN_UNKNOWN_REQUIRES_REVIEW


def _explanation(decision: str) -> str:
    if decision == DRY_RUN_READY_FOR_FUTURE_INTAKE:
        return (
            "Evidence metadata is ready for future intake if a later authorised "
            "slice permits ingestion; no ingestion or corpus mutation occurred now."
        )
    if decision.startswith("DRY_RUN_BLOCKED"):
        return (
            "The dry-run detected a claim that is blocked in this no-corpus-mutation "
            "slice; no action was performed."
        )
    return (
        "The dry-run requires additional controlled review before any future intake "
        "decision; no action was performed."
    )


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


def _dedupe(value: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(item) for item in _as_tuple(value) if str(item)))


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-dry-run-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

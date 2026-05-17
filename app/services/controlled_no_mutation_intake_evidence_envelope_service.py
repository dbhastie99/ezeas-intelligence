import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_first_no_mutation_intake_execution_service import (
    NO_MUTATION_INTAKE_EXECUTION_COMPLETED,
)


NO_MUTATION_EVIDENCE_ENVELOPE_READY = "NO_MUTATION_EVIDENCE_ENVELOPE_READY"
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_INGESTION_CLAIM = "BLOCKED_MUTATION_OR_INGESTION_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

INGESTION_OR_MUTATION_CLAIM_KEYS = (
    "durable_ingestion_performed",
    "durable_ingestion_authorised",
    "evidence_ingestion_performed",
    "evidence_ingestion_authorised",
    "corpus_mutation_performed",
    "corpus_mutation_authorised",
    "code_evidence_ingestion_performed",
    "code_evidence_ingestion_authorised",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "db_access_performed",
    "db_access_authorised",
    "db_write_performed",
    "db_write_authorised",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_llm_performed",
    "live_llm_authorised",
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "chat_or_endpoint_exposure_authorised",
    "runtime_integration_authorised",
    "runtime_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_authorised",
    "deployment_readiness_claim_permitted",
    "production_authorised",
    "production_readiness_claim_permitted",
)

REQUIRED_CAVEATS = (
    "Evidence envelope is review-only metadata.",
    "Future ingestion candidate status does not authorise durable ingestion.",
    "No durable ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, or final answer generation is authorised.",
)

REVIEW_NOTES = (
    "Source execution completed in memory only.",
    "Evidence summary is prepared for review and future decisioning only.",
    "Durable ingestion requires a later explicit authorisation gate.",
)

NEXT_DECISION_POINT = (
    "Decide whether to authorise a separate durable ingestion planning gate or "
    "keep the prepared evidence envelope review-only."
)


@dataclass(frozen=True)
class ControlledNoMutationIntakeEvidenceEnvelopeResult:
    envelope_id: str
    source_execution_id: str
    envelope_status: str
    candidate_id: str
    candidate_type: str
    evidence_summary: tuple[str, ...]
    evidence_category: str
    source_status: str
    future_ingestion_candidate: bool
    durable_ingestion_authorised: bool
    corpus_mutation_authorised: bool
    code_evidence_ingestion_authorised: bool
    db_write_authorised: bool
    live_retrieval_authorised: bool
    live_llm_authorised: bool
    final_answer_generation_authorised: bool
    required_caveats: tuple[str, ...]
    review_notes: tuple[str, ...]
    next_decision_point: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_no_mutation_intake_evidence_envelope(
    no_mutation_execution_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Prepare a review-only evidence envelope from no-mutation execution metadata."""

    execution = no_mutation_execution_metadata or {}
    blocked = _blocked_status(execution)
    status = _envelope_status(execution, blocked)
    ready = status == NO_MUTATION_EVIDENCE_ENVELOPE_READY
    source_execution_id = str(execution.get("execution_id") or "")
    candidate_id = str(execution.get("candidate_id") or "")
    candidate_type = str(execution.get("candidate_type") or "")
    source_status = str(execution.get("execution_status") or "")
    evidence_summary = _evidence_summary(execution, ready)
    material = {
        "source_execution_id": source_execution_id,
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "status": status,
        "source_status": source_status,
        "evidence_summary": evidence_summary,
    }

    return ControlledNoMutationIntakeEvidenceEnvelopeResult(
        envelope_id=_stable_id(material),
        source_execution_id=source_execution_id,
        envelope_status=status,
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        evidence_summary=evidence_summary,
        evidence_category="CONTROLLED_NO_MUTATION_INTAKE_REVIEW_ONLY",
        source_status=source_status,
        future_ingestion_candidate=ready,
        durable_ingestion_authorised=False,
        corpus_mutation_authorised=False,
        code_evidence_ingestion_authorised=False,
        db_write_authorised=False,
        live_retrieval_authorised=False,
        live_llm_authorised=False,
        final_answer_generation_authorised=False,
        required_caveats=_required_caveats(execution),
        review_notes=REVIEW_NOTES if ready else (),
        next_decision_point=NEXT_DECISION_POINT,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _blocked_status(execution: dict[str, Any]) -> str:
    if _has_claim(execution, INGESTION_OR_MUTATION_CLAIM_KEYS):
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if _status_claims_mutation_or_ingestion(execution):
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if _has_claim(execution, RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if _status_claims_runtime_or_production(execution):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    return ""


def _envelope_status(execution: dict[str, Any], blocked: str) -> str:
    if blocked:
        return blocked
    if not execution:
        return UNKNOWN_REQUIRES_REVIEW
    if execution.get("execution_status") != NO_MUTATION_INTAKE_EXECUTION_COMPLETED:
        return NEEDS_REVIEW
    if not execution.get("execution_id"):
        return NEEDS_REVIEW
    if execution.get("candidate_accepted_for_no_mutation_execution") is not True:
        return NEEDS_REVIEW
    if execution.get("in_memory_execution_completed") is not True:
        return NEEDS_REVIEW
    if not execution.get("candidate_id") or not execution.get("candidate_type"):
        return NEEDS_REVIEW
    return NO_MUTATION_EVIDENCE_ENVELOPE_READY


def _evidence_summary(
    execution: dict[str, Any],
    ready: bool,
) -> tuple[str, ...]:
    if not ready:
        return ()
    summary = _as_tuple(execution.get("prepared_evidence_summary"))
    if summary:
        return tuple(str(item) for item in summary)
    return (
        "No-mutation execution metadata is available for review.",
        "No durable ingestion or corpus mutation has been authorised.",
    )


def _required_caveats(execution: dict[str, Any]) -> tuple[str, ...]:
    caveats = [
        *[str(item) for item in _as_tuple(execution.get("required_caveats"))],
        *REQUIRED_CAVEATS,
    ]
    return tuple(dict.fromkeys(item for item in caveats if item))


def _explanation(status: str) -> str:
    if status == NO_MUTATION_EVIDENCE_ENVELOPE_READY:
        return (
            "A review-only evidence envelope was prepared from clean "
            "no-mutation execution metadata. It is a future ingestion candidate "
            "only and authorises no durable ingestion or corpus mutation."
        )
    if status.startswith("BLOCKED"):
        return (
            "The source execution metadata included a blocked ingestion, "
            "mutation, runtime, deployment, or production claim; no envelope "
            "action was authorised."
        )
    return (
        "The source no-mutation execution metadata is missing, incomplete, or "
        "not completed and requires review before envelope readiness."
    )


def _has_claim(metadata: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _status_claims_mutation_or_ingestion(metadata: dict[str, Any]) -> bool:
    status = str(metadata.get("execution_status") or "")
    return "MUTATION_OR_DURABLE_INGESTION" in status or "MUTATION_OR_INGESTION" in status


def _status_claims_runtime_or_production(metadata: dict[str, Any]) -> bool:
    status = str(metadata.get("execution_status") or "")
    return "RUNTIME_OR_PRODUCTION" in status


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
    return "controlled-no-mutation-intake-evidence-envelope-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_EVIDENCE_RETRIEVAL_READY = "DURABLE_EVIDENCE_RETRIEVAL_READY"
NEEDS_SOURCE_REFERENCE = "NEEDS_SOURCE_REFERENCE"
NEEDS_SOURCE_STATUS = "NEEDS_SOURCE_STATUS"
NEEDS_EVIDENCE_CATEGORY = "NEEDS_EVIDENCE_CATEGORY"
NEEDS_RECORD_STATUS = "NEEDS_RECORD_STATUS"
NEEDS_ROLLBACK_METADATA = "NEEDS_ROLLBACK_METADATA"
NEEDS_CAVEATS = "NEEDS_CAVEATS"
BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM = "BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_CAVEATS = (
    "Evidence remains bound to the cited local durable record envelope.",
    "Source status must be preserved in retrieval and answer preparation.",
    "No live retrieval, live LLM, DB read, DB write, chat exposure, runtime, deployment, or production readiness is authorised.",
)

LIVE_RETRIEVAL_OR_LLM_CLAIM_KEYS = (
    "live_retrieval_performed",
    "live_llm_performed",
    "final_answer_generated",
    "final_answer_generation_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "chat_exposure_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)

RUNTIME_OR_PRODUCTION_TERMS = (
    "runtime ready",
    "deployment ready",
    "production ready",
    "live chat enabled",
    "chat exposure authorised",
)


@dataclass(frozen=True)
class DurableEvidenceRetrievalReadinessResult:
    readiness_id: str
    source_record_id: str
    readiness_status: str
    retrieval_ready: bool
    source_reference_present: bool
    source_status_present: bool
    evidence_category_present: bool
    record_status_present: bool
    rollback_metadata_present: bool
    caveats_present: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    db_read_performed: bool
    db_write_performed: bool
    chat_exposure_authorised: bool
    missing_prerequisites: tuple[str, ...]
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_durable_evidence_retrieval_readiness(
    durable_record_metadata: dict[str, Any] | None,
    rollback_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return evaluate_durable_evidence_retrieval_readiness(
        durable_record_metadata,
        rollback_metadata,
    )


def evaluate_durable_evidence_retrieval_readiness(
    durable_record_metadata: dict[str, Any] | None,
    rollback_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = durable_record_metadata or {}
    rollback = rollback_metadata or {}
    source_record_id = str(record.get("record_id") or record.get("source_record_id") or "")
    missing_prerequisites = _missing_prerequisites(record, rollback)
    status = _readiness_status(record, rollback, missing_prerequisites)
    retrieval_ready = status == DURABLE_EVIDENCE_RETRIEVAL_READY
    material = {
        "source_record_id": source_record_id,
        "source_reference": record.get("source_reference"),
        "source_status": record.get("source_status"),
        "evidence_category": record.get("evidence_category"),
        "record_status": record.get("record_status"),
        "rollback_status": rollback.get("rollback_status"),
        "missing_prerequisites": missing_prerequisites,
        "status": status,
    }

    return DurableEvidenceRetrievalReadinessResult(
        readiness_id=str(record.get("readiness_id") or _stable_id(material)),
        source_record_id=source_record_id,
        readiness_status=status,
        retrieval_ready=retrieval_ready,
        source_reference_present=bool(record.get("source_reference")),
        source_status_present=bool(record.get("source_status")),
        evidence_category_present=bool(record.get("evidence_category")),
        record_status_present=bool(record.get("record_status")),
        rollback_metadata_present=_rollback_metadata_present(record, rollback),
        caveats_present=bool(record.get("required_caveats")),
        live_retrieval_performed=False,
        live_llm_performed=False,
        db_read_performed=False,
        db_write_performed=False,
        chat_exposure_authorised=False,
        missing_prerequisites=missing_prerequisites,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _missing_prerequisites(
    record: dict[str, Any],
    rollback: dict[str, Any],
) -> tuple[str, ...]:
    missing = []
    if not record.get("source_reference"):
        missing.append("source_reference")
    if not record.get("source_status"):
        missing.append("source_status")
    if not record.get("evidence_category"):
        missing.append("evidence_category")
    if not record.get("record_status"):
        missing.append("record_status")
    if not _rollback_metadata_present(record, rollback):
        missing.append("rollback_metadata")
    if not record.get("required_caveats"):
        missing.append("required_caveats")
    return tuple(missing)


def _readiness_status(
    record: dict[str, Any],
    rollback: dict[str, Any],
    missing_prerequisites: tuple[str, ...],
) -> str:
    combined = {**record, **rollback}
    if any(bool(combined.get(key)) for key in LIVE_RETRIEVAL_OR_LLM_CLAIM_KEYS):
        return BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM
    if any(bool(combined.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if _contains_runtime_or_production_text(record):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if "source_reference" in missing_prerequisites:
        return NEEDS_SOURCE_REFERENCE
    if "source_status" in missing_prerequisites:
        return NEEDS_SOURCE_STATUS
    if "evidence_category" in missing_prerequisites:
        return NEEDS_EVIDENCE_CATEGORY
    if "record_status" in missing_prerequisites:
        return NEEDS_RECORD_STATUS
    if "rollback_metadata" in missing_prerequisites:
        return NEEDS_ROLLBACK_METADATA
    if "required_caveats" in missing_prerequisites:
        return NEEDS_CAVEATS
    if record.get("record_storage_mode") != "LOCAL_CHECKED_IN_FIXTURE_ONLY":
        return UNKNOWN_REQUIRES_REVIEW
    return DURABLE_EVIDENCE_RETRIEVAL_READY


def _rollback_metadata_present(
    record: dict[str, Any],
    rollback: dict[str, Any],
) -> bool:
    if rollback.get("rollback_status") == "ROLLBACK_METADATA_READY":
        return True
    return bool(record.get("rollback_metadata_present"))


def _contains_runtime_or_production_text(record: dict[str, Any]) -> bool:
    text = " ".join(
        str(record.get(key) or "")
        for key in ("summary", "claims_text", "explanation", "phase_context")
    ).lower()
    return any(term in text for term in RUNTIME_OR_PRODUCTION_TERMS)


def _explanation(status: str) -> str:
    if status == DURABLE_EVIDENCE_RETRIEVAL_READY:
        return "The local durable evidence record has the source, status, category, rollback, and caveat metadata needed for controlled retrieval readiness only."
    if status == BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM:
        return "Readiness metadata contains a prohibited live retrieval, live LLM, or final-answer claim."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Readiness metadata contains a prohibited runtime, deployment, production, or chat exposure claim."
    if status == NEEDS_SOURCE_REFERENCE:
        return "Retrieval readiness requires a source reference."
    if status == NEEDS_SOURCE_STATUS:
        return "Retrieval readiness requires explicit source status."
    if status == NEEDS_EVIDENCE_CATEGORY:
        return "Retrieval readiness requires an evidence category."
    if status == NEEDS_RECORD_STATUS:
        return "Retrieval readiness requires local durable record status."
    if status == NEEDS_ROLLBACK_METADATA:
        return "Retrieval readiness requires rollback/removal metadata."
    if status == NEEDS_CAVEATS:
        return "Retrieval readiness requires caveats that preserve evidence and runtime boundaries."
    return "Retrieval readiness metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "durable-evidence-retrieval-readiness-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

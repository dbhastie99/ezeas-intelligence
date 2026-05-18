import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.developer_log_durable_evidence_candidate_service import (
    REQUIRED_DEVELOPER_LOG_SECTIONS,
)
from app.services.durable_evidence_retrieval_readiness_service import (
    DURABLE_EVIDENCE_RETRIEVAL_READY,
)


DEVELOPER_LOG_RETRIEVAL_METADATA_READY = (
    "DEVELOPER_LOG_RETRIEVAL_METADATA_READY"
)
NEEDS_RETRIEVAL_READY_RECORD = "NEEDS_RETRIEVAL_READY_RECORD"
NEEDS_RETRIEVABLE_SECTIONS = "NEEDS_RETRIEVABLE_SECTIONS"
NEEDS_ANSWER_BOUNDARIES = "NEEDS_ANSWER_BOUNDARIES"
BLOCKED_PROHIBITED_INFERENCE_CLAIM = "BLOCKED_PROHIBITED_INFERENCE_CLAIM"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

EVIDENCE_TYPE = "DEVELOPER_LOG"
STANDARD_RETRIEVABLE_SECTIONS = REQUIRED_DEVELOPER_LOG_SECTIONS
ANSWER_BOUNDARIES = (
    "Evidence says only what the cited Developer Log record supports.",
    "Project decisions may be summarised only when the Developer Log records them as decisions.",
    "Implementation status remains unknown unless separately evidenced.",
)
PROHIBITED_INFERENCES = (
    "production readiness",
    "runtime deployment",
    "DB mutation",
    "corpus mutation",
    "implementation completion unless directly evidenced",
)
IMPLEMENTATION_CLAIM_POLICY = (
    "Implementation completion must not be inferred from Developer Log retrieval metadata."
)
RUNTIME_CLAIM_POLICY = (
    "Runtime, deployment, production, DB, corpus, live retrieval, live LLM, and chat claims are prohibited."
)
PROHIBITED_INFERENCE_KEYS = (
    "production_ready",
    "deployment_ready",
    "runtime_ready",
    "db_mutation_performed",
    "corpus_mutation_performed",
    "implementation_complete",
)


@dataclass(frozen=True)
class DeveloperLogEvidenceRetrievalMetadataResult:
    metadata_id: str
    source_record_id: str
    metadata_status: str
    evidence_type: str
    retrieval_key: str
    retrievable_sections: tuple[str, ...]
    source_reference: str
    source_status: str
    answer_boundaries: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]
    citation_required: bool
    implementation_claim_policy: str
    runtime_claim_policy: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_developer_log_evidence_retrieval_metadata(
    durable_record_metadata: dict[str, Any] | None,
    readiness_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return prepare_developer_log_evidence_retrieval_metadata(
        durable_record_metadata,
        readiness_metadata,
    )


def prepare_developer_log_evidence_retrieval_metadata(
    durable_record_metadata: dict[str, Any] | None,
    readiness_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    record = durable_record_metadata or {}
    readiness = readiness_metadata or {}
    source_record_id = str(record.get("record_id") or readiness.get("source_record_id") or "")
    retrievable_sections = tuple(
        record.get("retrievable_sections")
        or record.get("sections_present")
        or STANDARD_RETRIEVABLE_SECTIONS
    )
    answer_boundaries = tuple(record.get("answer_boundaries") or ANSWER_BOUNDARIES)
    status = _metadata_status(record, readiness, retrievable_sections, answer_boundaries)
    ready = status == DEVELOPER_LOG_RETRIEVAL_METADATA_READY
    material = {
        "source_record_id": source_record_id,
        "readiness_status": readiness.get("readiness_status"),
        "source_reference": record.get("source_reference"),
        "source_status": record.get("source_status"),
        "retrievable_sections": retrievable_sections,
        "answer_boundaries": answer_boundaries,
        "status": status,
    }

    return DeveloperLogEvidenceRetrievalMetadataResult(
        metadata_id=str(record.get("metadata_id") or _stable_id(material)),
        source_record_id=source_record_id,
        metadata_status=status,
        evidence_type=EVIDENCE_TYPE,
        retrieval_key=f"developer-log:{source_record_id}" if ready else "",
        retrievable_sections=retrievable_sections if ready else tuple(),
        source_reference=str(record.get("source_reference") or ""),
        source_status=str(record.get("source_status") or ""),
        answer_boundaries=answer_boundaries if ready else tuple(),
        prohibited_inferences=PROHIBITED_INFERENCES,
        citation_required=True,
        implementation_claim_policy=IMPLEMENTATION_CLAIM_POLICY,
        runtime_claim_policy=RUNTIME_CLAIM_POLICY,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _metadata_status(
    record: dict[str, Any],
    readiness: dict[str, Any],
    retrievable_sections: tuple[str, ...],
    answer_boundaries: tuple[str, ...],
) -> str:
    if _prohibited_inference_claim_present(record):
        return BLOCKED_PROHIBITED_INFERENCE_CLAIM
    if readiness.get("readiness_status") != DURABLE_EVIDENCE_RETRIEVAL_READY:
        return NEEDS_RETRIEVAL_READY_RECORD
    if record.get("evidence_category") != "DEVELOPER_LOG_DURABLE_EVIDENCE_CANDIDATE":
        return UNKNOWN_REQUIRES_REVIEW
    if not retrievable_sections:
        return NEEDS_RETRIEVABLE_SECTIONS
    if not answer_boundaries:
        return NEEDS_ANSWER_BOUNDARIES
    return DEVELOPER_LOG_RETRIEVAL_METADATA_READY


def _prohibited_inference_claim_present(record: dict[str, Any]) -> bool:
    if any(bool(record.get(key)) for key in PROHIBITED_INFERENCE_KEYS):
        return True
    text = " ".join(
        str(record.get(key) or "")
        for key in ("claims_text", "summary", "explanation")
    ).lower()
    return any(inference in text for inference in PROHIBITED_INFERENCES)


def _explanation(status: str) -> str:
    if status == DEVELOPER_LOG_RETRIEVAL_METADATA_READY:
        return "Developer Log retrieval metadata is ready for controlled metadata-only answer preparation with preserved source and status boundaries."
    if status == NEEDS_RETRIEVAL_READY_RECORD:
        return "Developer Log retrieval metadata requires a retrieval-ready durable evidence record."
    if status == NEEDS_RETRIEVABLE_SECTIONS:
        return "Developer Log retrieval metadata requires retrievable sections."
    if status == NEEDS_ANSWER_BOUNDARIES:
        return "Developer Log retrieval metadata requires answer boundaries."
    if status == BLOCKED_PROHIBITED_INFERENCE_CLAIM:
        return "Developer Log retrieval metadata contains a prohibited production, runtime, mutation, or completion inference."
    return "Developer Log retrieval metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "developer-log-evidence-retrieval-metadata-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

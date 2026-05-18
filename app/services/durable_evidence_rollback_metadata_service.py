import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


ROLLBACK_METADATA_READY = "ROLLBACK_METADATA_READY"
NEEDS_SOURCE_RECORD = "NEEDS_SOURCE_RECORD"
NEEDS_REVIEWER_CONFIRMATION = "NEEDS_REVIEWER_CONFIRMATION"
BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM = (
    "BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_CAVEATS = (
    "Rollback/removal applies only to the controlled local fixture/artifact record.",
    "Reviewer confirmation and audit trail are required before removal.",
    "No live corpus mutation or DB write is authorised or performed.",
)


@dataclass(frozen=True)
class DurableEvidenceRollbackMetadataResult:
    rollback_id: str
    source_record_id: str
    rollback_status: str
    removal_supported: bool
    removal_scope: str
    removal_reason_required: bool
    reviewer_confirmation_required: bool
    audit_trail_required: bool
    live_corpus_mutation_performed: bool
    db_write_performed: bool
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_durable_evidence_rollback_metadata(
    durable_record_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return prepare_durable_evidence_rollback_metadata(durable_record_metadata)


def prepare_durable_evidence_rollback_metadata(
    durable_record_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = durable_record_metadata or {}
    source_record_id = str(metadata.get("record_id") or metadata.get("source_record_id") or "")
    status = _rollback_status(metadata, source_record_id)
    ready = status == ROLLBACK_METADATA_READY
    material = {
        "source_record_id": source_record_id,
        "record_status": metadata.get("record_status"),
        "record_storage_mode": metadata.get("record_storage_mode"),
        "reviewer_confirmation_available": metadata.get(
            "reviewer_confirmation_available"
        ),
        "status": status,
    }

    return DurableEvidenceRollbackMetadataResult(
        rollback_id=str(metadata.get("rollback_id") or _stable_id(material)),
        source_record_id=source_record_id,
        rollback_status=status,
        removal_supported=ready,
        removal_scope="LOCAL_CONTROLLED_FIXTURE_RECORD_ONLY" if ready else "",
        removal_reason_required=True,
        reviewer_confirmation_required=True,
        audit_trail_required=True,
        live_corpus_mutation_performed=False,
        db_write_performed=False,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _rollback_status(metadata: dict[str, Any], source_record_id: str) -> str:
    if metadata.get("live_corpus_mutation_performed") or metadata.get("db_write_performed"):
        return BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM
    if not source_record_id:
        return NEEDS_SOURCE_RECORD
    if metadata.get("record_storage_mode") not in (
        "LOCAL_CHECKED_IN_FIXTURE_ONLY",
        "LOCAL_CONTROLLED_FIXTURE_RECORD_ONLY",
    ):
        return UNKNOWN_REQUIRES_REVIEW
    if metadata.get("reviewer_confirmation_available") is not True:
        return NEEDS_REVIEWER_CONFIRMATION
    return ROLLBACK_METADATA_READY


def _explanation(status: str) -> str:
    if status == ROLLBACK_METADATA_READY:
        return "Rollback/removal metadata is ready for the local controlled fixture record only."
    if status == NEEDS_SOURCE_RECORD:
        return "Rollback/removal metadata requires a source local durable record."
    if status == NEEDS_REVIEWER_CONFIRMATION:
        return "Reviewer confirmation is required for local fixture record removal."
    if status == BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM:
        return "Rollback/removal metadata contains a prohibited live corpus or DB mutation claim."
    return "Rollback/removal metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "durable-evidence-rollback-metadata-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

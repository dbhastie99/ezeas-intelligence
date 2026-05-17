import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_AUDIT_ENVELOPE_READY = "DURABLE_INTAKE_AUDIT_ENVELOPE_READY"
AUDIT_ENVELOPE_INCOMPLETE = "AUDIT_ENVELOPE_INCOMPLETE"
BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM = (
    "BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_AUDIT_FIELDS = (
    "source_reference",
    "source_status",
    "reviewer",
    "decision_timestamp",
    "no_mutation_history",
    "rollback_policy",
    "prohibited_claims_checked",
    "sensitive_data_review",
)

PERFORMED_CLAIM_KEYS = (
    "durable_intake_performed",
    "durable_ingestion_performed",
    "corpus_mutation_performed",
    "db_write_performed",
    "code_evidence_ingestion_performed",
)


@dataclass(frozen=True)
class ControlledDurableIntakeAuditEnvelopeResult:
    audit_envelope_id: str
    audit_status: str
    required_audit_fields: tuple[str, ...]
    missing_audit_fields: tuple[str, ...]
    source_reference_present: bool
    source_status_present: bool
    reviewer_present: bool
    decision_timestamp_present: bool
    no_mutation_history_present: bool
    rollback_policy_present: bool
    prohibited_claims_checked: bool
    sensitive_data_review_required: bool
    durable_intake_performed: bool
    corpus_mutation_performed: bool
    db_write_performed: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_intake_audit_envelope(
    audit_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return deterministic audit-envelope metadata for future durable intake."""

    metadata = audit_metadata or {}
    present = _field_presence(metadata)
    missing = tuple(key for key, is_present in present.items() if not is_present)
    status = _audit_status(metadata, missing)
    material = {"status": status, "missing": missing, "present": present}

    return ControlledDurableIntakeAuditEnvelopeResult(
        audit_envelope_id=_stable_id(material),
        audit_status=status,
        required_audit_fields=REQUIRED_AUDIT_FIELDS,
        missing_audit_fields=missing,
        source_reference_present=present["source_reference"],
        source_status_present=present["source_status"],
        reviewer_present=present["reviewer"],
        decision_timestamp_present=present["decision_timestamp"],
        no_mutation_history_present=present["no_mutation_history"],
        rollback_policy_present=present["rollback_policy"],
        prohibited_claims_checked=present["prohibited_claims_checked"],
        sensitive_data_review_required=True,
        durable_intake_performed=False,
        corpus_mutation_performed=False,
        db_write_performed=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _audit_status(metadata: dict[str, Any], missing: tuple[str, ...]) -> str:
    if _has_performed_claim(metadata) or _status_claims_performed(metadata):
        return BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    if missing:
        return AUDIT_ENVELOPE_INCOMPLETE
    return DURABLE_INTAKE_AUDIT_ENVELOPE_READY


def _field_presence(metadata: dict[str, Any]) -> dict[str, bool]:
    return {
        "source_reference": bool(metadata.get("source_reference")),
        "source_status": bool(metadata.get("source_status")),
        "reviewer": bool(metadata.get("reviewer")),
        "decision_timestamp": bool(metadata.get("decision_timestamp")),
        "no_mutation_history": bool(metadata.get("no_mutation_history")),
        "rollback_policy": bool(metadata.get("rollback_policy")),
        "prohibited_claims_checked": metadata.get("prohibited_claims_checked") is True,
        "sensitive_data_review": metadata.get("sensitive_data_review") is True,
    }


def _has_performed_claim(metadata: dict[str, Any]) -> bool:
    return any(bool(metadata.get(key)) for key in PERFORMED_CLAIM_KEYS)


def _status_claims_performed(metadata: dict[str, Any]) -> bool:
    status = " ".join(
        str(metadata.get(key) or "")
        for key in ("audit_status", "intake_status", "claim_status")
    )
    return "PERFORMED" in status or "ALREADY_INGESTED" in status


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_AUDIT_ENVELOPE_READY:
        return (
            "The audit envelope metadata is complete for review before a "
            "future durable-intake authorisation. No durable intake, corpus "
            "mutation, or DB write has been performed."
        )
    if status == BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM:
        return (
            "The audit metadata claims durable intake, corpus mutation, DB "
            "write, or Code Evidence ingestion was already performed."
        )
    if status == AUDIT_ENVELOPE_INCOMPLETE:
        return "One or more required audit-envelope fields are missing."
    return "The audit-envelope metadata is missing or requires review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-audit-envelope-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

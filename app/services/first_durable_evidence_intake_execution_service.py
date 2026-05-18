import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.developer_log_durable_evidence_candidate_service import (
    DEVELOPER_LOG_CANDIDATE_READY,
)


FIRST_DURABLE_EVIDENCE_INTAKE_EXECUTION_READY = (
    "FIRST_DURABLE_EVIDENCE_INTAKE_EXECUTION_READY"
)
FIRST_DURABLE_EVIDENCE_RECORD_PREPARED = (
    "FIRST_DURABLE_EVIDENCE_RECORD_PREPARED"
)
NEEDS_READY_CANDIDATE = "NEEDS_READY_CANDIDATE"
NEEDS_ROLLBACK_METADATA = "NEEDS_ROLLBACK_METADATA"
BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM = (
    "BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

LOCAL_RECORD_STORAGE_MODE = "LOCAL_CHECKED_IN_FIXTURE_ONLY"
LOCAL_DURABLE_RECORD_STATUS = "LOCAL_DURABLE_RECORD_PREPARED"

LIVE_CORPUS_OR_DB_MUTATION_CLAIM_KEYS = (
    "live_corpus_mutation_performed",
    "corpus_mutation_performed",
    "db_write_performed",
    "db_read_performed",
    "db_connection_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "code_evidence_ingestion_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)


@dataclass(frozen=True)
class FirstDurableEvidenceIntakeExecutionResult:
    execution_id: str
    source_candidate_id: str
    execution_status: str
    durable_record_prepared: bool
    durable_record_written_to_local_fixture: bool
    live_corpus_mutation_performed: bool
    db_write_performed: bool
    code_evidence_ingestion_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    chat_exposure_authorised: bool
    record_id: str
    record_status: str
    record_storage_mode: str
    source_reference: str
    source_status: str
    required_caveats: tuple[str, ...]
    audit_metadata: dict[str, Any]
    rollback_metadata_required: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_first_durable_evidence_intake_execution(
    candidate_metadata: dict[str, Any] | None,
    rollback_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return execute_first_durable_evidence_intake(candidate_metadata, rollback_metadata)


def execute_first_durable_evidence_intake(
    candidate_metadata: dict[str, Any] | None,
    rollback_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate = candidate_metadata or {}
    rollback = rollback_metadata or {}
    source_candidate_id = str(candidate.get("candidate_id") or "")
    blocked = _blocked_status({**candidate, **rollback})
    status = blocked or _execution_status(candidate, rollback)
    prepared = status == FIRST_DURABLE_EVIDENCE_RECORD_PREPARED
    material = {
        "source_candidate_id": source_candidate_id,
        "candidate_status": candidate.get("candidate_status"),
        "source_reference": candidate.get("source_reference"),
        "source_status": candidate.get("source_status"),
        "rollback_status": rollback.get("rollback_status"),
        "status": status,
    }
    record_id = str(
        candidate.get("record_id")
        or ("durable-evidence-record-" + hashlib.sha256(
            json.dumps(
                material,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
        ).hexdigest()[:16])
    )
    audit_metadata = {
        "execution_scope": "FIRST_LOCAL_DURABLE_EVIDENCE_RECORD_ONLY",
        "source_candidate_id": source_candidate_id,
        "source_candidate_status": candidate.get("candidate_status"),
        "record_storage_mode": LOCAL_RECORD_STORAGE_MODE if prepared else "",
        "rollback_metadata_required": True,
        "live_corpus_mutation_performed": False,
        "db_write_performed": False,
    }

    return FirstDurableEvidenceIntakeExecutionResult(
        execution_id=str(candidate.get("execution_id") or _stable_id(material)),
        source_candidate_id=source_candidate_id,
        execution_status=status,
        durable_record_prepared=prepared,
        durable_record_written_to_local_fixture=prepared,
        live_corpus_mutation_performed=False,
        db_write_performed=False,
        code_evidence_ingestion_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        chat_exposure_authorised=False,
        record_id=record_id if prepared else "",
        record_status=LOCAL_DURABLE_RECORD_STATUS if prepared else "",
        record_storage_mode=LOCAL_RECORD_STORAGE_MODE if prepared else "",
        source_reference=str(candidate.get("source_reference") or ""),
        source_status=str(candidate.get("source_status") or ""),
        required_caveats=tuple(candidate.get("required_caveats") or ()),
        audit_metadata=audit_metadata,
        rollback_metadata_required=True,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _execution_status(
    candidate: dict[str, Any],
    rollback: dict[str, Any],
) -> str:
    if not candidate:
        return NEEDS_READY_CANDIDATE
    if candidate.get("candidate_status") != DEVELOPER_LOG_CANDIDATE_READY:
        return NEEDS_READY_CANDIDATE
    if candidate.get("eligible_for_durable_intake") is not True:
        return NEEDS_READY_CANDIDATE
    if not rollback or rollback.get("rollback_status") != "ROLLBACK_METADATA_READY":
        return NEEDS_ROLLBACK_METADATA
    if rollback.get("source_record_id") and not str(rollback["source_record_id"]).startswith(
        "durable-evidence-record-"
    ):
        return UNKNOWN_REQUIRES_REVIEW
    return FIRST_DURABLE_EVIDENCE_RECORD_PREPARED


def _blocked_status(metadata: dict[str, Any]) -> str | None:
    if any(bool(metadata.get(key)) for key in LIVE_CORPUS_OR_DB_MUTATION_CLAIM_KEYS):
        return BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    return None


def _explanation(status: str) -> str:
    if status == FIRST_DURABLE_EVIDENCE_RECORD_PREPARED:
        return (
            "A first local durable evidence record envelope was prepared for a "
            "ready Developer Log candidate only as a controlled checked-in "
            "fixture/artifact model."
        )
    if status == NEEDS_READY_CANDIDATE:
        return "A ready Developer Log durable evidence candidate is required."
    if status == NEEDS_ROLLBACK_METADATA:
        return "Rollback/removal metadata is required before local record preparation."
    if status == BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM:
        return "Execution metadata contains a prohibited live corpus or DB mutation claim."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Execution metadata contains a prohibited runtime, production, retrieval, LLM, final-answer, Code Evidence, or chat claim."
    return "Execution metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "first-durable-evidence-intake-execution-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

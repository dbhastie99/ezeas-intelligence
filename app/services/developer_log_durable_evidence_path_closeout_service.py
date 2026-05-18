import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE = (
    "DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE"
)
NEEDS_RETRIEVAL_READINESS = "NEEDS_RETRIEVAL_READINESS"
NEEDS_CONTROLLED_ANSWER_REHEARSAL = "NEEDS_CONTROLLED_ANSWER_REHEARSAL"
BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM"
)
BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM = (
    "BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

PATH_NAME = "Minerva Developer Log Durable Evidence Controlled Answer Path"
PROGRESS_BEFORE_SLICE = "approximately 85-90%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "Developer Log evidence candidate prepared",
    "Local durable record envelope prepared",
    "Rollback/removal metadata prepared",
    "Retrieval readiness determined",
    "Developer Log retrieval metadata created",
    "Controlled answer preparation created",
    "Controlled answer synthesis rehearsal created",
    "Answer review metadata created",
    "Developer Log answer boundaries enforced",
)
REMAINING_WORK = (
    "Choose the next practical Minerva value path.",
)
RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Add Hardening Log as second durable evidence type.",
    "Option B: Add Platform Doctrine as second durable evidence type.",
    "Option C: Build a controlled retrieval harness over durable evidence fixtures.",
    "Option D: Pause Minerva while analytics schema work continues.",
)
LIVE_LLM_OR_FINAL_ANSWER_KEYS = (
    "live_llm_performed",
    "final_answer_generated",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "live_llm_claimed",
    "final_answer_claimed",
    "chat_exposure_claimed",
)
DB_OR_LIVE_CORPUS_KEYS = (
    "db_read_performed",
    "db_write_performed",
    "db_connection_performed",
    "live_corpus_mutation_performed",
    "corpus_mutation_performed",
    "code_evidence_ingestion_performed",
)
RUNTIME_OR_PRODUCTION_KEYS = (
    "runtime_integration_authorised",
    "runtime_authorised",
    "runtime_ready",
    "deployment_authorised",
    "deployment_ready",
    "production_authorised",
    "production_ready",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)


@dataclass(frozen=True)
class DeveloperLogDurableEvidencePathCloseoutResult:
    closeout_id: str
    path_name: str
    path_status: str
    progress_before_slice: str
    progress_after_slice: str
    developer_log_candidate_ready: bool
    durable_record_envelope_ready: bool
    rollback_metadata_ready: bool
    retrieval_readiness_ready: bool
    retrieval_metadata_ready: bool
    answer_preparation_ready: bool
    synthesis_rehearsal_ready: bool
    answer_review_metadata_ready: bool
    answer_boundary_enforcement_ready: bool
    live_llm_performed: bool
    final_answer_generated: bool
    chat_exposure_authorised: bool
    db_read_performed: bool
    db_write_performed: bool
    live_corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    runtime_integration_authorised: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_developer_log_durable_evidence_path_closeout(
    path_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return close_out_developer_log_durable_evidence_path(path_metadata)


def close_out_developer_log_durable_evidence_path(
    path_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    metadata = path_metadata or {}
    component_flags = _component_flags(metadata)
    status = _path_status(metadata, component_flags)
    complete = (
        status == DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE
    )
    material = {
        "path_name": PATH_NAME,
        "component_flags": component_flags,
        "status": status,
    }

    return DeveloperLogDurableEvidencePathCloseoutResult(
        closeout_id=str(metadata.get("closeout_id") or _stable_id(material)),
        path_name=PATH_NAME,
        path_status=status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE if complete else "",
        developer_log_candidate_ready=component_flags["developer_log_candidate_ready"],
        durable_record_envelope_ready=component_flags["durable_record_envelope_ready"],
        rollback_metadata_ready=component_flags["rollback_metadata_ready"],
        retrieval_readiness_ready=component_flags["retrieval_readiness_ready"],
        retrieval_metadata_ready=component_flags["retrieval_metadata_ready"],
        answer_preparation_ready=component_flags["answer_preparation_ready"],
        synthesis_rehearsal_ready=component_flags["synthesis_rehearsal_ready"],
        answer_review_metadata_ready=component_flags["answer_review_metadata_ready"],
        answer_boundary_enforcement_ready=component_flags[
            "answer_boundary_enforcement_ready"
        ],
        live_llm_performed=False,
        final_answer_generated=False,
        chat_exposure_authorised=False,
        db_read_performed=False,
        db_write_performed=False,
        live_corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        runtime_integration_authorised=False,
        completed_components=COMPLETED_COMPONENTS if complete else tuple(),
        remaining_work=REMAINING_WORK if complete else _remaining_work(status),
        next_decision_point="Select the next practical Minerva value path.",
        recommended_next_phase_options=RECOMMENDED_NEXT_PHASE_OPTIONS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _component_flags(metadata: dict[str, Any]) -> dict[str, bool]:
    return {
        "developer_log_candidate_ready": _flag(
            metadata, "developer_log_candidate_ready", True
        ),
        "durable_record_envelope_ready": _flag(
            metadata, "durable_record_envelope_ready", True
        ),
        "rollback_metadata_ready": _flag(metadata, "rollback_metadata_ready", True),
        "retrieval_readiness_ready": _flag(
            metadata, "retrieval_readiness_ready", True
        ),
        "retrieval_metadata_ready": _flag(metadata, "retrieval_metadata_ready", True),
        "answer_preparation_ready": _flag(metadata, "answer_preparation_ready", True),
        "synthesis_rehearsal_ready": _flag(metadata, "synthesis_rehearsal_ready", True),
        "answer_review_metadata_ready": _flag(
            metadata, "answer_review_metadata_ready", True
        ),
        "answer_boundary_enforcement_ready": _flag(
            metadata, "answer_boundary_enforcement_ready", True
        ),
    }


def _flag(metadata: dict[str, Any], key: str, default: bool) -> bool:
    return bool(metadata[key]) if key in metadata else default


def _path_status(metadata: dict[str, Any], component_flags: dict[str, bool]) -> str:
    if any(bool(metadata.get(key)) for key in LIVE_LLM_OR_FINAL_ANSWER_KEYS):
        return BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM
    if any(bool(metadata.get(key)) for key in DB_OR_LIVE_CORPUS_KEYS):
        return BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_KEYS):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not component_flags["retrieval_readiness_ready"]:
        return NEEDS_RETRIEVAL_READINESS
    if not (
        component_flags["answer_preparation_ready"]
        and component_flags["synthesis_rehearsal_ready"]
        and component_flags["answer_review_metadata_ready"]
        and component_flags["answer_boundary_enforcement_ready"]
    ):
        return NEEDS_CONTROLLED_ANSWER_REHEARSAL
    if all(component_flags.values()):
        return DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE
    return UNKNOWN_REQUIRES_REVIEW


def _remaining_work(status: str) -> tuple[str, ...]:
    if status == NEEDS_RETRIEVAL_READINESS:
        return ("Complete retrieval-readiness metadata before closeout.",)
    if status == NEEDS_CONTROLLED_ANSWER_REHEARSAL:
        return ("Complete controlled answer preparation, rehearsal, review, and boundary metadata.",)
    return ("Resolve blocked or unknown closeout claims under controlled review.",)


def _explanation(status: str) -> str:
    if status == DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE:
        return (
            "The practical Developer Log durable-evidence controlled-answer path is "
            "closed out as local deterministic metadata only; no live LLM, final "
            "answer, chat exposure, DB activity, live corpus mutation, Code Evidence "
            "ingestion, runtime integration, deployment, or production readiness is "
            "authorised or performed."
        )
    if status == BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM:
        return "Closeout blocks live LLM, final answer, or chat exposure claims."
    if status == BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM:
        return "Closeout blocks DB, live corpus mutation, or Code Evidence ingestion claims."
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return "Closeout blocks runtime, deployment, or production overstatement."
    if status == NEEDS_RETRIEVAL_READINESS:
        return "Closeout requires retrieval readiness before the practical path can be complete."
    if status == NEEDS_CONTROLLED_ANSWER_REHEARSAL:
        return "Closeout requires controlled answer preparation, rehearsal, review, and boundary enforcement."
    return "Closeout metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "developer-log-durable-evidence-path-closeout-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

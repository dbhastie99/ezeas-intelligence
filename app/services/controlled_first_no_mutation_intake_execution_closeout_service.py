import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_no_mutation_intake_verification_pack_service import (
    NO_MUTATION_VERIFICATION_PACK_READY,
)


FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE = (
    "FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM = (
    "BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

PHASE_NAME = "Controlled First No-Mutation Intake Execution Phase Closeout v0.1"
PROGRESS_BEFORE_SLICE = "approximately 90%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "controlled_first_no_mutation_intake_execution_service",
    "controlled_no_mutation_intake_evidence_envelope_service",
    "controlled_first_no_mutation_intake_execution_review_service",
    "controlled_no_mutation_intake_verification_pack_service",
)

REMAINING_WORK = ("choose_next_phase",)

NEXT_DECISION_POINT = (
    "Explicitly choose the next Minerva evidence-intake phase before any "
    "durable ingestion, corpus mutation, runtime integration, endpoint "
    "exposure, or production-readiness work begins."
)

RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Controlled Durable Evidence Intake Design",
    "Option B: External Evidence Summary Catalogue",
    "Option C: Code Evidence Readiness Planning",
    "Option D: Pause Minerva While Award Recovery Continues",
)

NO_MUTATION_ATTESTATION = (
    "First no-mutation intake execution phase is complete at controlled-"
    "readiness/no-mutation level only; no durable ingestion, corpus mutation, "
    "Code Evidence ingestion, DB access, live retrieval, live LLM use, final "
    "answer generation, exposure, runtime integration, deployment, or "
    "production readiness has been authorised."
)

MUTATION_OR_INGESTION_FLAGS = (
    "durable_ingestion_performed",
    "durable_ingestion_authorised",
    "ready_for_durable_ingestion",
)

CORPUS_MUTATION_FLAGS = (
    "corpus_mutation_performed",
    "corpus_mutation_authorised",
)

CODE_EVIDENCE_INGESTION_FLAGS = (
    "code_evidence_ingestion_performed",
    "code_evidence_ingestion_authorised",
)

RUNTIME_OR_PRODUCTION_FLAGS = (
    "db_access_performed",
    "db_access_authorised",
    "db_read_performed",
    "db_read_authorised",
    "db_write_performed",
    "db_write_authorised",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_llm_performed",
    "live_llm_authorised",
    "runtime_integration_authorised",
    "runtime_authorised",
    "workforce_runtime_integration_authorised",
    "analytics_runtime_integration_authorised",
    "production_readiness_claim_permitted",
    "production_authorised",
    "deployment_readiness_claim_permitted",
    "deployment_authorised",
    "runtime_readiness_claim_permitted",
)

EXPOSURE_OR_FINAL_ANSWER_FLAGS = (
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "chat_exposure_authorised",
    "chat_or_endpoint_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
)


@dataclass(frozen=True)
class ControlledFirstNoMutationIntakeExecutionCloseoutResult:
    closeout_id: str
    phase_name: str
    phase_status: str
    progress_before_slice: str
    progress_after_slice: str
    first_no_mutation_intake_execution_phase_complete: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    durable_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_access_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    chat_exposure_authorised: bool
    endpoint_exposure_authorised: bool
    workforce_runtime_integration_authorised: bool
    analytics_runtime_integration_authorised: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    no_mutation_attestation: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_first_no_mutation_intake_execution_closeout(
    verification_pack_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Close out the first no-mutation intake execution phase without side effects."""

    pack = verification_pack_metadata or {}
    flags = _prohibited_flag_summary(pack)
    status = _phase_status(pack, flags)
    complete = status == FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE
    material = {
        "source_verification_pack_id": str(pack.get("verification_pack_id") or ""),
        "status": status,
        "flags": flags,
        "phase_name": PHASE_NAME,
        "completed_components": COMPLETED_COMPONENTS,
        "remaining_work": REMAINING_WORK,
    }

    return ControlledFirstNoMutationIntakeExecutionCloseoutResult(
        closeout_id=_stable_id(material),
        phase_name=PHASE_NAME,
        phase_status=status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        first_no_mutation_intake_execution_phase_complete=complete,
        completed_components=COMPLETED_COMPONENTS,
        remaining_work=REMAINING_WORK,
        next_decision_point=NEXT_DECISION_POINT,
        recommended_next_phase_options=RECOMMENDED_NEXT_PHASE_OPTIONS,
        durable_ingestion_performed=flags["durable_ingestion_performed"],
        corpus_mutation_performed=flags["corpus_mutation_performed"],
        code_evidence_ingestion_performed=flags["code_evidence_ingestion_performed"],
        db_access_performed=flags["db_access_performed"],
        db_write_performed=flags["db_write_performed"],
        live_retrieval_performed=flags["live_retrieval_performed"],
        live_llm_performed=flags["live_llm_performed"],
        final_answer_generation_performed=flags["final_answer_generation_performed"],
        chat_exposure_authorised=flags["chat_exposure_authorised"],
        endpoint_exposure_authorised=flags["endpoint_exposure_authorised"],
        workforce_runtime_integration_authorised=flags[
            "workforce_runtime_integration_authorised"
        ],
        analytics_runtime_integration_authorised=flags[
            "analytics_runtime_integration_authorised"
        ],
        production_readiness_claim_permitted=flags[
            "production_readiness_claim_permitted"
        ],
        deployment_readiness_claim_permitted=flags[
            "deployment_readiness_claim_permitted"
        ],
        runtime_readiness_claim_permitted=flags["runtime_readiness_claim_permitted"],
        no_mutation_attestation=_no_mutation_attestation(pack),
        no_action_attestation=str(pack.get("no_action_attestation") or NO_ACTION_ATTESTATION),
        explanation=_explanation(status),
    ).to_dict()


def _phase_status(pack: dict[str, Any], flags: dict[str, bool]) -> str:
    if _has_any(flags, _canonical_mutation_flag_names()) or _status_claims_mutation(pack):
        return BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    if _has_any(flags, _canonical_exposure_flag_names()) or _status_claims_exposure(pack):
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if _has_any(flags, _canonical_runtime_flag_names()) or _status_claims_runtime(pack):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not pack:
        return UNKNOWN_REQUIRES_REVIEW
    if pack.get("verification_status") != NO_MUTATION_VERIFICATION_PACK_READY:
        return NEEDS_REVIEW
    if pack.get("ready_for_phase_closeout") is not True:
        return NEEDS_REVIEW
    if pack.get("no_mutation_verified") is not True:
        return NEEDS_REVIEW
    if pack.get("review_complete") is not True:
        return NEEDS_REVIEW
    if pack.get("ready_for_durable_ingestion") is True:
        return BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    return FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE


def _prohibited_flag_summary(pack: dict[str, Any]) -> dict[str, bool]:
    return {
        "durable_ingestion_performed": _any_claim(pack, *MUTATION_OR_INGESTION_FLAGS),
        "corpus_mutation_performed": _any_claim(pack, *CORPUS_MUTATION_FLAGS),
        "code_evidence_ingestion_performed": _any_claim(
            pack,
            *CODE_EVIDENCE_INGESTION_FLAGS,
        ),
        "db_access_performed": _any_claim(
            pack,
            "db_access_performed",
            "db_access_authorised",
            "db_read_performed",
            "db_read_authorised",
        ),
        "db_write_performed": _any_claim(
            pack,
            "db_write_performed",
            "db_write_authorised",
        ),
        "live_retrieval_performed": _any_claim(
            pack,
            "live_retrieval_performed",
            "live_retrieval_authorised",
        ),
        "live_llm_performed": _any_claim(
            pack,
            "live_llm_performed",
            "live_llm_authorised",
        ),
        "final_answer_generation_performed": _any_claim(
            pack,
            "final_answer_generation_performed",
            "final_answer_generation_authorised",
        ),
        "chat_exposure_authorised": _any_claim(
            pack,
            "chat_exposure_authorised",
            "chat_or_endpoint_exposure_authorised",
        ),
        "endpoint_exposure_authorised": _any_claim(
            pack,
            "endpoint_exposure_authorised",
            "chat_or_endpoint_exposure_authorised",
            "route_registration_authorised",
        ),
        "workforce_runtime_integration_authorised": _any_claim(
            pack,
            "workforce_runtime_integration_authorised",
            "runtime_integration_authorised",
            "runtime_authorised",
        ),
        "analytics_runtime_integration_authorised": _any_claim(
            pack,
            "analytics_runtime_integration_authorised",
            "runtime_integration_authorised",
            "runtime_authorised",
        ),
        "production_readiness_claim_permitted": _any_claim(
            pack,
            "production_readiness_claim_permitted",
            "production_authorised",
        ),
        "deployment_readiness_claim_permitted": _any_claim(
            pack,
            "deployment_readiness_claim_permitted",
            "deployment_authorised",
        ),
        "runtime_readiness_claim_permitted": _any_claim(
            pack,
            "runtime_readiness_claim_permitted",
        ),
    }


def _canonical_mutation_flag_names() -> tuple[str, ...]:
    return (
        "durable_ingestion_performed",
        "corpus_mutation_performed",
        "code_evidence_ingestion_performed",
    )


def _canonical_runtime_flag_names() -> tuple[str, ...]:
    return (
        "db_access_performed",
        "db_write_performed",
        "live_retrieval_performed",
        "live_llm_performed",
        "workforce_runtime_integration_authorised",
        "analytics_runtime_integration_authorised",
        "production_readiness_claim_permitted",
        "deployment_readiness_claim_permitted",
        "runtime_readiness_claim_permitted",
    )


def _canonical_exposure_flag_names() -> tuple[str, ...]:
    return (
        "final_answer_generation_performed",
        "chat_exposure_authorised",
        "endpoint_exposure_authorised",
    )


def _has_any(flags: dict[str, bool], keys: tuple[str, ...]) -> bool:
    return any(flags[key] for key in keys)


def _any_claim(pack: dict[str, Any], *keys: str) -> bool:
    return any(bool(pack.get(key)) for key in keys)


def _status_claims_mutation(pack: dict[str, Any]) -> bool:
    status = _status_text(pack)
    return "MUTATION_OR_INGESTION" in status or "DURABLE_INGESTION" in status


def _status_claims_runtime(pack: dict[str, Any]) -> bool:
    return "RUNTIME_OR_PRODUCTION" in _status_text(pack)


def _status_claims_exposure(pack: dict[str, Any]) -> bool:
    return "EXPOSURE_OR_FINAL_ANSWER" in _status_text(pack)


def _status_text(pack: dict[str, Any]) -> str:
    return " ".join(
        str(pack.get(key) or "")
        for key in ("phase_status", "verification_status", "review_status")
    )


def _no_mutation_attestation(pack: dict[str, Any]) -> str:
    return str(pack.get("no_mutation_attestation") or NO_MUTATION_ATTESTATION)


def _explanation(status: str) -> str:
    if status == FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE:
        return (
            "The first no-mutation intake execution phase is closed at "
            "controlled-readiness/no-mutation level only. The next phase must "
            "be explicitly chosen before any durable ingestion, mutation, "
            "runtime, exposure, deployment, or production work."
        )
    if status == BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM:
        return (
            "The verification metadata includes durable ingestion, corpus "
            "mutation, or Code Evidence ingestion claims, so phase closeout is "
            "blocked."
        )
    if status == BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM:
        return (
            "The verification metadata includes final answer generation or "
            "chat, endpoint, or route exposure claims, so phase closeout is "
            "blocked."
        )
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return (
            "The verification metadata includes DB, live retrieval, live LLM, "
            "runtime, deployment, or production overstatement claims, so phase "
            "closeout is blocked."
        )
    return "The verification metadata is missing, incomplete, or requires review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-first-no-mutation-intake-execution-closeout-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

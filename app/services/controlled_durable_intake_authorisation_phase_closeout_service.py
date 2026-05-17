import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_durable_intake_execution_review_pack_service import (
    DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE = (
    "DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM = (
    "BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

PHASE_NAME = "Controlled Durable Intake Authorisation Phase Closeout v0.1"
PROGRESS_BEFORE_SLICE = "approximately 85-90%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "durable evidence intake authorisation gate",
    "durable intake candidate eligibility",
    "first-candidate execution design",
    "execution review pack",
)

REMAINING_WORK = ("choose_next_phase",)

NEXT_DECISION_POINT = (
    "Explicitly choose the next Minerva durable-intake phase before any "
    "durable ingestion, corpus mutation, Code Evidence ingestion, DB work, "
    "live retrieval, live LLM, final answer generation, exposure, runtime "
    "integration, deployment, or production-readiness work begins."
)

RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Controlled Durable Intake Execution / Review-Only First Candidate",
    "Option B: External Evidence Summary Catalogue",
    "Option C: Code Evidence Readiness Planning",
    "Option D: Pause Minerva While Demo Stabilisation Continues",
)

NO_INGESTION_ATTESTATION = (
    "Controlled durable intake authorisation phase is complete at "
    "readiness/design level only; no durable evidence ingestion has been "
    "performed or authorised."
)

NO_MUTATION_ATTESTATION = (
    "Controlled durable intake authorisation phase is complete at "
    "readiness/design level only; no corpus mutation, Code Evidence ingestion, "
    "DB write, runtime integration, deployment, or production readiness has "
    "been performed or authorised."
)

MUTATION_OR_INGESTION_FLAGS = (
    "durable_ingestion_performed",
    "durable_ingestion_authorised",
    "durable_intake_performed",
    "durable_intake_authorised",
    "durable_intake_authorised_now",
    "durable_intake_execution_authorised_now",
    "durable_evidence_ingestion_performed",
    "durable_evidence_ingestion_authorised",
    "corpus_mutation_performed",
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "code_evidence_ingestion_performed",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_authorised_now",
    "ready_for_durable_ingestion",
)

RUNTIME_OR_PRODUCTION_FLAGS = (
    "db_access_performed",
    "db_access_authorised",
    "db_read_performed",
    "db_read_authorised",
    "db_write_performed",
    "db_write_authorised",
    "db_write_authorised_now",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_retrieval_authorised_now",
    "live_llm_performed",
    "live_llm_authorised",
    "live_llm_authorised_now",
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
    "final_answer_generation_authorised_now",
    "chat_exposure_authorised",
    "chat_or_endpoint_exposure_authorised",
    "internal_chat_exposure_authorised",
    "public_chat_exposure_authorised",
    "tenant_chat_exposure_authorised",
    "customer_chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
)


@dataclass(frozen=True)
class ControlledDurableIntakeAuthorisationPhaseCloseoutResult:
    closeout_id: str
    phase_name: str
    phase_status: str
    progress_before_slice: str
    progress_after_slice: str
    durable_intake_authorisation_phase_complete: bool
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
    no_ingestion_attestation: str
    no_mutation_attestation: str
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_intake_authorisation_phase_closeout(
    execution_review_pack_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Close out durable intake authorisation phase without runtime action."""

    metadata = execution_review_pack_metadata or {}
    flags = _prohibited_flag_summary(metadata)
    status = _phase_status(metadata, flags)
    complete = status == DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE
    material = {
        "source_review_pack_id": str(metadata.get("review_pack_id") or ""),
        "status": status,
        "flags": flags,
        "phase_name": PHASE_NAME,
        "completed_components": COMPLETED_COMPONENTS,
        "remaining_work": REMAINING_WORK,
    }

    return ControlledDurableIntakeAuthorisationPhaseCloseoutResult(
        closeout_id=_stable_id(material),
        phase_name=PHASE_NAME,
        phase_status=status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        durable_intake_authorisation_phase_complete=complete,
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
        no_ingestion_attestation=_no_ingestion_attestation(metadata),
        no_mutation_attestation=_no_mutation_attestation(metadata),
        no_action_attestation=str(
            metadata.get("no_action_attestation") or NO_ACTION_ATTESTATION
        ),
        explanation=_explanation(status),
    ).to_dict()


def closeout_controlled_durable_intake_authorisation_phase(
    execution_review_pack_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return build_controlled_durable_intake_authorisation_phase_closeout(
        execution_review_pack_metadata
    )


def _phase_status(metadata: dict[str, Any], flags: dict[str, bool]) -> str:
    if _has_any(flags, _canonical_mutation_flag_names()) or _status_claims_mutation(
        metadata
    ):
        return BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM
    if _has_any(flags, _canonical_exposure_flag_names()) or _status_claims_exposure(
        metadata
    ):
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if _has_any(flags, _canonical_runtime_flag_names()) or _status_claims_runtime(
        metadata
    ):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    if metadata.get("review_pack_status") != DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY:
        return NEEDS_REVIEW
    if metadata.get("execution_design_ready") is not True:
        return NEEDS_REVIEW
    return DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE


def _prohibited_flag_summary(metadata: dict[str, Any]) -> dict[str, bool]:
    return {
        "durable_ingestion_performed": _any_claim(
            metadata,
            "durable_ingestion_performed",
            "durable_ingestion_authorised",
            "durable_intake_performed",
            "durable_intake_authorised",
            "durable_intake_authorised_now",
            "durable_intake_execution_authorised_now",
            "durable_evidence_ingestion_performed",
            "durable_evidence_ingestion_authorised",
            "ready_for_durable_ingestion",
        ),
        "corpus_mutation_performed": _any_claim(
            metadata,
            "corpus_mutation_performed",
            "corpus_mutation_authorised",
            "corpus_mutation_authorised_now",
        ),
        "code_evidence_ingestion_performed": _any_claim(
            metadata,
            "code_evidence_ingestion_performed",
            "code_evidence_ingestion_authorised",
            "code_evidence_ingestion_authorised_now",
        ),
        "db_access_performed": _any_claim(
            metadata,
            "db_access_performed",
            "db_access_authorised",
            "db_read_performed",
            "db_read_authorised",
        ),
        "db_write_performed": _any_claim(
            metadata,
            "db_write_performed",
            "db_write_authorised",
            "db_write_authorised_now",
        ),
        "live_retrieval_performed": _any_claim(
            metadata,
            "live_retrieval_performed",
            "live_retrieval_authorised",
            "live_retrieval_authorised_now",
        ),
        "live_llm_performed": _any_claim(
            metadata,
            "live_llm_performed",
            "live_llm_authorised",
            "live_llm_authorised_now",
        ),
        "final_answer_generation_performed": _any_claim(
            metadata,
            "final_answer_generation_performed",
            "final_answer_generation_authorised",
            "final_answer_generation_authorised_now",
        ),
        "chat_exposure_authorised": _any_claim(
            metadata,
            "chat_exposure_authorised",
            "chat_or_endpoint_exposure_authorised",
            "internal_chat_exposure_authorised",
            "public_chat_exposure_authorised",
            "tenant_chat_exposure_authorised",
            "customer_chat_exposure_authorised",
        ),
        "endpoint_exposure_authorised": _any_claim(
            metadata,
            "endpoint_exposure_authorised",
            "chat_or_endpoint_exposure_authorised",
            "route_registration_authorised",
        ),
        "workforce_runtime_integration_authorised": _any_claim(
            metadata,
            "workforce_runtime_integration_authorised",
            "runtime_integration_authorised",
            "runtime_authorised",
        ),
        "analytics_runtime_integration_authorised": _any_claim(
            metadata,
            "analytics_runtime_integration_authorised",
            "runtime_integration_authorised",
            "runtime_authorised",
        ),
        "production_readiness_claim_permitted": _any_claim(
            metadata,
            "production_readiness_claim_permitted",
            "production_authorised",
        ),
        "deployment_readiness_claim_permitted": _any_claim(
            metadata,
            "deployment_readiness_claim_permitted",
            "deployment_authorised",
        ),
        "runtime_readiness_claim_permitted": _any_claim(
            metadata,
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


def _any_claim(metadata: dict[str, Any], *keys: str) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _status_claims_mutation(metadata: dict[str, Any]) -> bool:
    status = _status_text(metadata)
    return (
        "DURABLE_INGESTION" in status
        or "DURABLE_INTAKE_AUTHORISED" in status
        or "DURABLE_INTAKE_ALREADY_PERFORMED" in status
        or "MUTATION_OR_INGESTION" in status
        or "CODE_EVIDENCE_INGESTION" in status
    )


def _status_claims_runtime(metadata: dict[str, Any]) -> bool:
    status = _status_text(metadata)
    return (
        "RUNTIME_OR_PRODUCTION" in status
        or "PRODUCTION_READY" in status
        or "LIVE_RETRIEVAL_LLM" in status
    )


def _status_claims_exposure(metadata: dict[str, Any]) -> bool:
    return "EXPOSURE_OR_FINAL_ANSWER" in _status_text(metadata)


def _status_text(metadata: dict[str, Any]) -> str:
    return " ".join(
        str(metadata.get(key) or "")
        for key in (
            "phase_status",
            "review_pack_status",
            "design_status",
            "authorisation_status",
            "eligibility_status",
        )
    )


def _no_ingestion_attestation(metadata: dict[str, Any]) -> str:
    return str(metadata.get("no_ingestion_attestation") or NO_INGESTION_ATTESTATION)


def _no_mutation_attestation(metadata: dict[str, Any]) -> str:
    return str(metadata.get("no_mutation_attestation") or NO_MUTATION_ATTESTATION)


def _explanation(status: str) -> str:
    if status == DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE:
        return (
            "The controlled durable intake authorisation phase is complete at "
            "readiness/design level only. The next phase must be explicitly "
            "chosen before any durable ingestion, mutation, runtime, exposure, "
            "deployment, or production work."
        )
    if status == BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM:
        return (
            "The closeout metadata includes durable ingestion, corpus mutation, "
            "or Code Evidence ingestion claims, so phase closeout is blocked."
        )
    if status == BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM:
        return (
            "The closeout metadata includes final answer generation or chat, "
            "endpoint, or route exposure claims, so phase closeout is blocked."
        )
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return (
            "The closeout metadata includes DB, live retrieval, live LLM, "
            "runtime, deployment, or production overstatement claims, so phase "
            "closeout is blocked."
        )
    if status == UNKNOWN_REQUIRES_REVIEW:
        return "The closeout metadata is missing and requires controlled review."
    return "The closeout metadata is incomplete or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-intake-authorisation-phase-closeout-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_first_no_mutation_intake_execution_service import (
    NO_MUTATION_INTAKE_EXECUTION_COMPLETED,
)
from app.services.controlled_no_mutation_intake_evidence_envelope_service import (
    NO_MUTATION_EVIDENCE_ENVELOPE_READY,
)


NO_MUTATION_EXECUTION_REVIEW_READY = "NO_MUTATION_EXECUTION_REVIEW_READY"
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

MUTATION_OR_INGESTION_FLAGS = (
    "durable_ingestion_performed",
    "durable_ingestion_authorised",
    "evidence_ingestion_performed",
    "evidence_ingestion_authorised",
    "corpus_mutation_performed",
    "corpus_mutation_authorised",
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
    "runtime_readiness_claim_permitted",
    "deployment_authorised",
    "deployment_readiness_claim_permitted",
    "production_authorised",
    "production_readiness_claim_permitted",
)

EXPOSURE_OR_FINAL_ANSWER_FLAGS = (
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "chat_or_endpoint_exposure_authorised",
    "chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
)

PROHIBITED_FLAGS = (
    *MUTATION_OR_INGESTION_FLAGS,
    *RUNTIME_OR_PRODUCTION_FLAGS,
    *EXPOSURE_OR_FINAL_ANSWER_FLAGS,
)

REQUIRED_CAVEATS = (
    "Execution review is deterministic metadata only.",
    "Evidence envelope review is review-only metadata.",
    "No durable ingestion, corpus mutation, Code Evidence ingestion, DB access, DB write, live retrieval, live LLM use, final answer generation, chat exposure, endpoint exposure, runtime integration, deployment, or production readiness has been authorised.",
    "Next action must be a deliberate closeout or separately authorised durable-ingestion decision.",
)


@dataclass(frozen=True)
class ControlledFirstNoMutationIntakeExecutionReviewResult:
    review_id: str
    source_execution_id: str
    source_envelope_id: str
    review_status: str
    execution_review_complete: bool
    evidence_envelope_review_complete: bool
    no_mutation_verified: bool
    durable_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_access_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    chat_or_endpoint_exposure_authorised: bool
    runtime_integration_authorised: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    required_caveats: tuple[str, ...]
    review_findings: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_first_no_mutation_intake_execution_review(
    no_mutation_execution_metadata: dict[str, Any] | None,
    evidence_envelope_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Review no-mutation execution and evidence envelope metadata without side effects."""

    execution = no_mutation_execution_metadata or {}
    envelope = evidence_envelope_metadata or {}
    flags = _prohibited_flag_summary(execution, envelope)
    findings = _review_findings(execution, envelope)
    blocked_reasons = _blocked_reasons(execution, envelope, flags)
    status = _review_status(execution, envelope, findings, blocked_reasons)
    execution_complete = (
        status == NO_MUTATION_EXECUTION_REVIEW_READY
        and execution.get("execution_status") == NO_MUTATION_INTAKE_EXECUTION_COMPLETED
    )
    envelope_complete = (
        status == NO_MUTATION_EXECUTION_REVIEW_READY
        and envelope.get("envelope_status") == NO_MUTATION_EVIDENCE_ENVELOPE_READY
    )
    no_mutation_verified = (
        execution_complete
        and envelope_complete
        and not any(flags.values())
    )
    material = {
        "source_execution_id": str(execution.get("execution_id") or ""),
        "source_envelope_id": str(envelope.get("envelope_id") or ""),
        "status": status,
        "findings": findings,
        "blocked_reasons": blocked_reasons,
        "flags": flags,
    }

    return ControlledFirstNoMutationIntakeExecutionReviewResult(
        review_id=_stable_id(material),
        source_execution_id=str(execution.get("execution_id") or ""),
        source_envelope_id=str(envelope.get("envelope_id") or ""),
        review_status=status,
        execution_review_complete=execution_complete,
        evidence_envelope_review_complete=envelope_complete,
        no_mutation_verified=no_mutation_verified,
        durable_ingestion_performed=flags["durable_ingestion_performed"],
        corpus_mutation_performed=flags["corpus_mutation_performed"],
        code_evidence_ingestion_performed=flags["code_evidence_ingestion_performed"],
        db_access_performed=flags["db_access_performed"],
        db_write_performed=flags["db_write_performed"],
        live_retrieval_performed=flags["live_retrieval_performed"],
        live_llm_performed=flags["live_llm_performed"],
        final_answer_generation_performed=flags["final_answer_generation_performed"],
        chat_or_endpoint_exposure_authorised=flags[
            "chat_or_endpoint_exposure_authorised"
        ],
        runtime_integration_authorised=flags["runtime_integration_authorised"],
        production_readiness_claim_permitted=flags[
            "production_readiness_claim_permitted"
        ],
        deployment_readiness_claim_permitted=flags[
            "deployment_readiness_claim_permitted"
        ],
        runtime_readiness_claim_permitted=flags["runtime_readiness_claim_permitted"],
        required_caveats=_required_caveats(execution, envelope),
        review_findings=findings,
        blocked_reasons=blocked_reasons,
        no_action_attestation=_no_action_attestation(execution, envelope),
        explanation=_explanation(status),
    ).to_dict()


def _review_findings(
    execution: dict[str, Any],
    envelope: dict[str, Any],
) -> tuple[str, ...]:
    findings: list[str] = []
    if not execution:
        findings.append("missing_execution_metadata")
    if not envelope:
        findings.append("missing_evidence_envelope_metadata")
    if execution and execution.get("execution_status") != NO_MUTATION_INTAKE_EXECUTION_COMPLETED:
        findings.append("execution_not_completed")
    if envelope and envelope.get("envelope_status") != NO_MUTATION_EVIDENCE_ENVELOPE_READY:
        findings.append("evidence_envelope_not_ready")
    if execution and not execution.get("execution_id"):
        findings.append("missing_execution_id")
    if envelope and not envelope.get("envelope_id"):
        findings.append("missing_envelope_id")
    if execution and envelope:
        if envelope.get("source_execution_id") != execution.get("execution_id"):
            findings.append("envelope_source_execution_mismatch")
    if not findings:
        findings.append("execution_and_evidence_envelope_ready_for_review_closeout")
    return tuple(findings)


def _blocked_reasons(
    execution: dict[str, Any],
    envelope: dict[str, Any],
    flags: dict[str, bool],
) -> tuple[str, ...]:
    blocked: list[str] = []
    if any(flags[key] for key in _canonical_mutation_flag_names()):
        blocked.append("mutation_or_durable_ingestion_claim")
    if _status_claims_mutation_or_ingestion(execution) or _status_claims_mutation_or_ingestion(
        envelope
    ):
        blocked.append("mutation_or_durable_ingestion_claim")
    if any(flags[key] for key in _canonical_runtime_flag_names()):
        blocked.append("runtime_or_production_overstatement")
    if _status_claims_runtime_or_production(execution) or _status_claims_runtime_or_production(
        envelope
    ):
        blocked.append("runtime_or_production_overstatement")
    if any(flags[key] for key in _canonical_exposure_flag_names()):
        blocked.append("exposure_or_final_answer_claim")
    return tuple(dict.fromkeys(blocked))


def _review_status(
    execution: dict[str, Any],
    envelope: dict[str, Any],
    findings: tuple[str, ...],
    blocked_reasons: tuple[str, ...],
) -> str:
    if "mutation_or_durable_ingestion_claim" in blocked_reasons:
        return BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    if "exposure_or_final_answer_claim" in blocked_reasons:
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if "runtime_or_production_overstatement" in blocked_reasons:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not execution or not envelope:
        return UNKNOWN_REQUIRES_REVIEW
    if findings != ("execution_and_evidence_envelope_ready_for_review_closeout",):
        return NEEDS_REVIEW
    return NO_MUTATION_EXECUTION_REVIEW_READY


def _prohibited_flag_summary(
    execution: dict[str, Any],
    envelope: dict[str, Any],
) -> dict[str, bool]:
    metadata = (execution, envelope)
    return {
        "durable_ingestion_performed": _any_claim(
            metadata,
            "durable_ingestion_performed",
            "durable_ingestion_authorised",
            "evidence_ingestion_performed",
            "evidence_ingestion_authorised",
        ),
        "corpus_mutation_performed": _any_claim(
            metadata,
            "corpus_mutation_performed",
            "corpus_mutation_authorised",
        ),
        "code_evidence_ingestion_performed": _any_claim(
            metadata,
            "code_evidence_ingestion_performed",
            "code_evidence_ingestion_authorised",
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
        ),
        "live_retrieval_performed": _any_claim(
            metadata,
            "live_retrieval_performed",
            "live_retrieval_authorised",
        ),
        "live_llm_performed": _any_claim(
            metadata,
            "live_llm_performed",
            "live_llm_authorised",
        ),
        "final_answer_generation_performed": _any_claim(
            metadata,
            "final_answer_generation_performed",
            "final_answer_generation_authorised",
        ),
        "chat_or_endpoint_exposure_authorised": _any_claim(
            metadata,
            "chat_or_endpoint_exposure_authorised",
            "chat_exposure_authorised",
            "endpoint_exposure_authorised",
            "route_registration_authorised",
        ),
        "runtime_integration_authorised": _any_claim(
            metadata,
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
        "runtime_integration_authorised",
        "production_readiness_claim_permitted",
        "deployment_readiness_claim_permitted",
        "runtime_readiness_claim_permitted",
    )


def _canonical_exposure_flag_names() -> tuple[str, ...]:
    return (
        "final_answer_generation_performed",
        "chat_or_endpoint_exposure_authorised",
    )


def _required_caveats(
    execution: dict[str, Any],
    envelope: dict[str, Any],
) -> tuple[str, ...]:
    caveats = [
        *[str(item) for item in _as_tuple(execution.get("required_caveats"))],
        *[str(item) for item in _as_tuple(envelope.get("required_caveats"))],
        *REQUIRED_CAVEATS,
    ]
    return tuple(dict.fromkeys(item for item in caveats if item))


def _no_action_attestation(
    execution: dict[str, Any],
    envelope: dict[str, Any],
) -> str:
    return (
        str(execution.get("no_action_attestation"))
        or str(envelope.get("no_action_attestation"))
        or NO_ACTION_ATTESTATION
    )


def _explanation(status: str) -> str:
    if status == NO_MUTATION_EXECUTION_REVIEW_READY:
        return (
            "The no-mutation execution and review-only evidence envelope were "
            "reviewed as deterministic metadata. No prohibited mutation, "
            "ingestion, DB, live retrieval, live LLM, final answer, exposure, "
            "runtime, deployment, or production claim was present."
        )
    if status == BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM:
        return (
            "The supplied metadata includes a mutation, durable ingestion, or "
            "Code Evidence claim, so review closeout is blocked."
        )
    if status == BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM:
        return (
            "The supplied metadata includes final answer generation or chat, "
            "endpoint, or route exposure, so review closeout is blocked."
        )
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return (
            "The supplied metadata includes DB, live retrieval, live LLM, "
            "runtime, deployment, or production overstatement, so review "
            "closeout is blocked."
        )
    return (
        "The execution or evidence envelope metadata is missing, incomplete, "
        "or mismatched and requires review."
    )


def _any_claim(metadata_items: tuple[dict[str, Any], ...], *keys: str) -> bool:
    return any(bool(metadata.get(key)) for metadata in metadata_items for key in keys)


def _status_claims_mutation_or_ingestion(metadata: dict[str, Any]) -> bool:
    status = _status_text(metadata)
    return "MUTATION_OR_DURABLE_INGESTION" in status or "MUTATION_OR_INGESTION" in status


def _status_claims_runtime_or_production(metadata: dict[str, Any]) -> bool:
    return "RUNTIME_OR_PRODUCTION" in _status_text(metadata)


def _status_text(metadata: dict[str, Any]) -> str:
    return " ".join(
        str(metadata.get(key) or "")
        for key in ("review_status", "execution_status", "envelope_status")
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


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-first-no-mutation-intake-execution-review-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

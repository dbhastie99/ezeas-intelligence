import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    FIRST_CANDIDATE_REVIEW_READY,
)


NO_MUTATION_INTAKE_EXECUTION_READY = "NO_MUTATION_INTAKE_EXECUTION_READY"
NO_MUTATION_INTAKE_EXECUTION_COMPLETED = "NO_MUTATION_INTAKE_EXECUTION_COMPLETED"
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM = (
    "BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

INGESTION_OR_MUTATION_CLAIM_KEYS = (
    "intake_authorised_now",
    "candidate_authorised_for_intake_now",
    "durable_ingestion_authorised",
    "durable_ingestion_performed",
    "evidence_ingestion_authorised_now",
    "evidence_ingestion_performed",
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "db_access_performed",
    "db_access_authorised",
    "db_read_performed",
    "db_write_performed",
    "db_write_authorised",
    "db_write_authorised_now",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_llm_performed",
    "live_llm_authorised",
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "chat_or_endpoint_exposure_authorised",
    "chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
    "runtime_integration_authorised",
    "runtime_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_authorised",
    "deployment_readiness_claim_permitted",
    "production_authorised",
    "production_readiness_claim_permitted",
)

REQUIRED_CAVEATS = (
    "Candidate accepted only for controlled no-mutation intake execution.",
    "Execution is in-memory metadata preparation only.",
    "No durable ingestion, corpus mutation, Code Evidence ingestion, DB access, DB write, live retrieval, live LLM use, or final answer generation has been performed.",
    "Future durable ingestion still requires explicit authorisation.",
)

PREPARED_EVIDENCE_SUMMARY = (
    "Reviewed candidate identity retained for future evidence-envelope review.",
    "No-mutation execution metadata prepared in memory.",
    "Durable ingestion and corpus mutation remain deferred.",
)


@dataclass(frozen=True)
class ControlledFirstNoMutationIntakeExecutionResult:
    execution_id: str
    candidate_id: str
    candidate_type: str
    execution_status: str
    candidate_accepted_for_no_mutation_execution: bool
    in_memory_execution_completed: bool
    durable_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_access_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    prepared_evidence_summary: tuple[str, ...]
    required_caveats: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def execute_controlled_first_no_mutation_intake(
    first_candidate_review_metadata: dict[str, Any] | None,
    authorisation_closeout_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Prepare first no-mutation intake execution metadata without side effects."""

    review = first_candidate_review_metadata or {}
    closeout = authorisation_closeout_metadata or {}
    candidate_id = str(review.get("candidate_id") or "")
    candidate_type = str(review.get("candidate_type") or "")
    blocked = _blocked_reasons(review, closeout)
    findings = _review_findings(review, closeout)
    status = _execution_status(review, blocked, findings)
    completed = status == NO_MUTATION_INTAKE_EXECUTION_COMPLETED
    material = {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "status": status,
        "findings": findings,
        "blocked": blocked,
    }

    return ControlledFirstNoMutationIntakeExecutionResult(
        execution_id=_stable_id(material),
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        execution_status=status,
        candidate_accepted_for_no_mutation_execution=completed,
        in_memory_execution_completed=completed,
        durable_ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_access_performed=False,
        db_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        prepared_evidence_summary=_prepared_evidence_summary(completed),
        required_caveats=_required_caveats(review, closeout),
        blocked_reasons=blocked,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def build_controlled_first_no_mutation_intake_execution(
    first_candidate_review_metadata: dict[str, Any] | None,
    authorisation_closeout_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return execute_controlled_first_no_mutation_intake(
        first_candidate_review_metadata,
        authorisation_closeout_metadata,
    )


def _blocked_reasons(
    review: dict[str, Any],
    closeout: dict[str, Any],
) -> tuple[str, ...]:
    blocked: list[str] = []
    if _has_claim(review, INGESTION_OR_MUTATION_CLAIM_KEYS) or _has_claim(
        closeout, INGESTION_OR_MUTATION_CLAIM_KEYS
    ):
        blocked.append("mutation_or_durable_ingestion_claim")
    if _status_claims_mutation_or_ingestion(review) or _status_claims_mutation_or_ingestion(
        closeout
    ):
        blocked.append("mutation_or_durable_ingestion_claim")
    if _has_claim(review, RUNTIME_OR_PRODUCTION_CLAIM_KEYS) or _has_claim(
        closeout, RUNTIME_OR_PRODUCTION_CLAIM_KEYS
    ):
        blocked.append("runtime_or_production_overstatement")
    if _status_claims_runtime_or_production(review) or _status_claims_runtime_or_production(
        closeout
    ):
        blocked.append("runtime_or_production_overstatement")
    return tuple(dict.fromkeys(blocked))


def _review_findings(
    review: dict[str, Any],
    closeout: dict[str, Any],
) -> tuple[str, ...]:
    findings: list[str] = []
    if not review:
        findings.append("missing_candidate_review_metadata")
    if not str(review.get("candidate_id") or ""):
        findings.append("missing_candidate_id")
    if not str(review.get("candidate_type") or ""):
        findings.append("missing_candidate_type")
    if review.get("review_status") != FIRST_CANDIDATE_REVIEW_READY:
        findings.append("candidate_review_not_ready")
    if review.get("candidate_eligible_for_future_no_mutation_intake") is not True:
        findings.append("future_no_mutation_eligibility_missing")
    if closeout and closeout.get("first_candidate_ready_for_future_no_mutation_intake") is not True:
        findings.append("authorisation_closeout_not_ready_for_future_no_mutation_intake")
    if closeout and closeout.get("first_candidate_review_complete") is not True:
        findings.append("authorisation_closeout_review_not_complete")
    if not findings:
        findings.append("first_candidate_review_ready_for_no_mutation_execution")
    return tuple(findings)


def _execution_status(
    review: dict[str, Any],
    blocked: tuple[str, ...],
    findings: tuple[str, ...],
) -> str:
    if "mutation_or_durable_ingestion_claim" in blocked:
        return BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    if "runtime_or_production_overstatement" in blocked:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not review:
        return UNKNOWN_REQUIRES_REVIEW
    if findings != ("first_candidate_review_ready_for_no_mutation_execution",):
        return NEEDS_REVIEW
    if review.get("no_mutation_execution_requested") is False:
        return NO_MUTATION_INTAKE_EXECUTION_READY
    return NO_MUTATION_INTAKE_EXECUTION_COMPLETED


def _prepared_evidence_summary(completed: bool) -> tuple[str, ...]:
    if not completed:
        return ()
    return PREPARED_EVIDENCE_SUMMARY


def _required_caveats(
    review: dict[str, Any],
    closeout: dict[str, Any],
) -> tuple[str, ...]:
    caveats = [
        *[str(item) for item in _as_tuple(review.get("required_caveats"))],
        *[str(item) for item in _as_tuple(closeout.get("required_caveats"))],
        *REQUIRED_CAVEATS,
    ]
    return tuple(dict.fromkeys(item for item in caveats if item))


def _explanation(status: str) -> str:
    if status == NO_MUTATION_INTAKE_EXECUTION_COMPLETED:
        return (
            "The reviewed first candidate was accepted only for controlled "
            "no-mutation execution. Execution completed in memory and prepared "
            "review metadata only; durable ingestion and corpus mutation remain "
            "unauthorised."
        )
    if status == NO_MUTATION_INTAKE_EXECUTION_READY:
        return (
            "The reviewed first candidate is ready for no-mutation execution, "
            "but execution was not requested in the supplied metadata."
        )
    if status.startswith("BLOCKED"):
        return (
            "The execution metadata included a blocked ingestion, mutation, "
            "runtime, deployment, or production claim; no action was performed."
        )
    return (
        "The candidate review or authorisation metadata is missing, unknown, "
        "or mismatched and requires review before no-mutation execution."
    )


def _has_claim(metadata: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _status_claims_mutation_or_ingestion(metadata: dict[str, Any]) -> bool:
    status = " ".join(
        str(metadata.get(key) or "")
        for key in ("review_status", "phase_status", "execution_status")
    )
    return "MUTATION_OR_INGESTION" in status or "DURABLE_INGESTION" in status


def _status_claims_runtime_or_production(metadata: dict[str, Any]) -> bool:
    status = " ".join(
        str(metadata.get(key) or "")
        for key in ("review_status", "phase_status", "execution_status")
    )
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
    return "controlled-first-no-mutation-intake-execution-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]

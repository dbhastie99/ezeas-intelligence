import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evaluation_batch_summary_service import (
    PROHIBITED_POSITIVE_PATTERNS,
    _has_positive_claim,
    _normalize_text,
)


CONTROLLED_REGRESSION_EXECUTION_COMPLETE = (
    "CONTROLLED_REGRESSION_EXECUTION_COMPLETE"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_OVERSTATED_RUNTIME = "BLOCKED_OVERSTATED_RUNTIME"
BLOCKED_OVERSTATED_PRODUCTION = "BLOCKED_OVERSTATED_PRODUCTION"
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"
)

PHASE_NAME = "Minerva Controlled Regression Execution Phase Closeout Ledger v0.1"
PROGRESS_BEFORE_SLICE = "95%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1",
    "Candidate Answer Readiness Classifier v0.1",
    "Evaluation Output Publication Gate v0.1",
    "Controlled Evaluation Report Assembler v0.1",
    "Controlled Evaluation Report Fixture Pack / Golden Report Baselines v0.1",
    "Controlled Evaluation Batch Harness v0.1",
    "Controlled Evaluation Batch Summary Model v0.1",
    "Controlled Evaluation Summary Export Model v0.1",
    "Controlled Evaluation CI Command Pack v0.1",
)

REMAINING_WORK = (
    "Choose the next Minerva phase deliberately before authorising further work.",
)

RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Controlled Evaluation Report Export File Writer.",
    "Option B: Controlled Corpus / Evidence Intake Planning.",
    "Option C: Code Evidence Readiness Planning.",
    "Option D: Keep Minerva paused while award recovery continues.",
)

NO_ACTION_ATTESTATION = (
    "No runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, final "
    "answer generation, UI, deployment, production, migration, credential, "
    "live retrieval backend, workforce-platform, ezeas-analytics, or cross-repo "
    "runtime action was performed or authorised by this closeout ledger."
)

EXPOSURE_OR_FINAL_ANSWER_PATTERNS = (
    "chat exposure enabled",
    "chat exposure authorised",
    "internal chat enabled",
    "internal chat authorised",
    "public chat enabled",
    "public chat authorised",
    "tenant chat enabled",
    "tenant chat authorised",
    "customer chat enabled",
    "customer chat authorised",
    "endpoint exposed",
    "endpoint exposure authorised",
    "api endpoint enabled",
    "api endpoint authorised",
    "route registered",
    "final answer generation enabled",
    "final answer generation authorised",
    "final natural-language answer generation enabled",
    "final natural-language answer generation authorised",
)

RUNTIME_PATTERNS = (
    "runtime-ready",
    "runtime ready",
    "runtime enabled",
    "runtime authorised",
    "live llm enabled",
    "live llm authorised",
    "calls the live llm",
    "live retrieval backend enabled",
    "live retrieval backend authorised",
    "db access occurred",
    "db access authorised",
    "database access occurred",
    "database access authorised",
    "read from the database",
    "database reads authorised",
    "write to the database",
    "wrote to the database",
    "database writes authorised",
    "migrations authorised",
    "corpus mutation occurred",
    "corpus mutation authorised",
    "mutated the corpus",
    "code evidence ingestion occurred",
    "code evidence ingestion authorised",
    "ingested code evidence",
    "workforce-platform runtime integration enabled",
    "workforce-platform runtime integration authorised",
    "analytics runtime integration enabled",
    "analytics runtime integration authorised",
    "ezeas-analytics runtime integration enabled",
    "ezeas-analytics runtime integration authorised",
)

PRODUCTION_PATTERNS = (
    "production-ready",
    "production ready",
    "ready for production",
    "production readiness authorised",
    "production readiness permitted",
    "deployment-ready",
    "deployment ready",
    "ready for deployment",
    "deployment readiness authorised",
    "deployment readiness permitted",
)


@dataclass(frozen=True)
class ControlledRegressionExecutionCloseoutResult:
    closeout_id: str
    phase_name: str
    closeout_status: str
    progress_before_slice: str
    progress_after_slice: str
    controlled_regression_execution_complete: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    final_answer_generation_authorised: bool
    live_llm_authorised: bool
    chat_exposure_authorised: bool
    endpoint_exposure_authorised: bool
    db_access_authorised: bool
    corpus_mutation_authorised: bool
    code_evidence_ingestion_authorised: bool
    workforce_runtime_integration_authorised: bool
    analytics_runtime_integration_authorised: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    no_action_attestation: str
    explanation: str
    review_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_regression_execution_closeout(
    *,
    completed_components: Any = COMPLETED_COMPONENTS,
    remaining_work: Any = REMAINING_WORK,
    next_decision_point: str = (
        "Choose the next Minerva phase deliberately before authorising any "
        "runtime, exposure, data, evidence, or cross-repo behaviour."
    ),
    recommended_next_phase_options: Any = RECOMMENDED_NEXT_PHASE_OPTIONS,
    no_action_attestation: str = NO_ACTION_ATTESTATION,
    notes: Any = (),
    claims: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return deterministic closeout metadata for controlled regression execution."""

    components = _as_tuple(completed_components)
    remaining = _as_tuple(remaining_work)
    options = _as_tuple(recommended_next_phase_options)
    review_flags = _review_flags(
        components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        no_action_attestation=no_action_attestation,
        notes=_as_tuple(notes),
        claims=claims or {},
    )
    closeout_status = _closeout_status(review_flags)
    complete = (
        closeout_status == CONTROLLED_REGRESSION_EXECUTION_COMPLETE
        and set(COMPLETED_COMPONENTS).issubset(set(components))
        and remaining == REMAINING_WORK
    )

    material = {
        "phase_name": PHASE_NAME,
        "closeout_status": closeout_status,
        "progress_before_slice": PROGRESS_BEFORE_SLICE,
        "progress_after_slice": PROGRESS_AFTER_SLICE,
        "completed_components": components,
        "remaining_work": remaining,
        "next_decision_point": next_decision_point,
        "recommended_next_phase_options": options,
        "no_action_attestation": no_action_attestation,
        "review_flags": review_flags,
    }

    return ControlledRegressionExecutionCloseoutResult(
        closeout_id=_closeout_id(material),
        phase_name=PHASE_NAME,
        closeout_status=closeout_status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        controlled_regression_execution_complete=complete,
        completed_components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        final_answer_generation_authorised=False,
        live_llm_authorised=False,
        chat_exposure_authorised=False,
        endpoint_exposure_authorised=False,
        db_access_authorised=False,
        corpus_mutation_authorised=False,
        code_evidence_ingestion_authorised=False,
        workforce_runtime_integration_authorised=False,
        analytics_runtime_integration_authorised=False,
        production_readiness_claim_permitted=False,
        deployment_readiness_claim_permitted=False,
        runtime_readiness_claim_permitted=False,
        no_action_attestation=no_action_attestation,
        explanation=_explanation(closeout_status, review_flags),
        review_flags=review_flags,
    ).to_dict()


def _review_flags(
    *,
    components: tuple[Any, ...],
    remaining_work: tuple[Any, ...],
    next_decision_point: str,
    recommended_next_phase_options: tuple[Any, ...],
    no_action_attestation: str,
    notes: tuple[Any, ...],
    claims: dict[str, Any],
) -> tuple[str, ...]:
    flags: list[str] = []
    text = _metadata_text(
        components=components,
        remaining_work=remaining_work,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=recommended_next_phase_options,
        no_action_attestation=no_action_attestation,
        notes=notes,
        claims=claims,
    )
    claim_text = _normalize_text(json.dumps(claims, sort_keys=True, default=str))

    if not set(COMPLETED_COMPONENTS).issubset(set(str(item) for item in components)):
        flags.append("MISSING_COMPLETED_COMPONENT")
    if remaining_work != REMAINING_WORK:
        flags.append("REMAINING_WORK_NOT_LIMITED_TO_NEXT_PHASE_DECISION")
    if not recommended_next_phase_options:
        flags.append("NEXT_PHASE_OPTIONS_MISSING")
    if not no_action_attestation:
        flags.append("NO_ACTION_ATTESTATION_MISSING")
    if _contains_positive_claim(text, EXPOSURE_OR_FINAL_ANSWER_PATTERNS):
        flags.append(BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM)
    if _contains_positive_claim(text, PRODUCTION_PATTERNS):
        flags.append(BLOCKED_OVERSTATED_PRODUCTION)
    if _contains_positive_claim(text, RUNTIME_PATTERNS):
        flags.append(BLOCKED_OVERSTATED_RUNTIME)
    if _contains_positive_claim(text, PROHIBITED_POSITIVE_PATTERNS):
        flags.append("PROHIBITED_CLOSEOUT_METADATA_CLAIM")
    if any(bool(value) for value in claims.values()):
        if _contains_positive_claim(claim_text, EXPOSURE_OR_FINAL_ANSWER_PATTERNS):
            flags.append(BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM)
        elif _contains_positive_claim(claim_text, PRODUCTION_PATTERNS):
            flags.append(BLOCKED_OVERSTATED_PRODUCTION)
        elif _contains_positive_claim(claim_text, RUNTIME_PATTERNS):
            flags.append(BLOCKED_OVERSTATED_RUNTIME)
        else:
            flags.append("CLAIM_REQUIRES_REVIEW")

    return tuple(dict.fromkeys(flags))


def _closeout_status(review_flags: tuple[str, ...]) -> str:
    if BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM in review_flags:
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if BLOCKED_OVERSTATED_PRODUCTION in review_flags:
        return BLOCKED_OVERSTATED_PRODUCTION
    if BLOCKED_OVERSTATED_RUNTIME in review_flags:
        return BLOCKED_OVERSTATED_RUNTIME
    if review_flags:
        return NEEDS_REVIEW
    return CONTROLLED_REGRESSION_EXECUTION_COMPLETE


def _metadata_text(
    *,
    components: tuple[Any, ...],
    remaining_work: tuple[Any, ...],
    next_decision_point: str,
    recommended_next_phase_options: tuple[Any, ...],
    no_action_attestation: str,
    notes: tuple[Any, ...],
    claims: dict[str, Any],
) -> str:
    return _normalize_text(
        "\n".join(
            str(item)
            for item in (
                *components,
                *remaining_work,
                next_decision_point,
                *recommended_next_phase_options,
                no_action_attestation,
                *notes,
                json.dumps(claims, sort_keys=True, default=str),
            )
        )
    )


def _contains_positive_claim(
    normalized_text: str,
    patterns: tuple[str, ...],
) -> bool:
    return any(_has_positive_claim(normalized_text, pattern) for pattern in patterns)


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


def _closeout_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"controlled-regression-execution-closeout-{digest}"


def _explanation(closeout_status: str, review_flags: tuple[str, ...]) -> str:
    if closeout_status == CONTROLLED_REGRESSION_EXECUTION_COMPLETE:
        return (
            "Controlled regression execution is complete at controlled-readiness "
            "level only; the next phase must be chosen deliberately."
        )
    return (
        "Controlled regression execution closeout requires review because blocked "
        "or overstated metadata was detected: "
        + ", ".join(review_flags)
        + "."
    )

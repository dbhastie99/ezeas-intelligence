import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evaluation_batch_summary_service import (
    _has_positive_claim,
    _normalize_text,
)


GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE = (
    "GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_UNAUTHORISED_INGESTION_CLAIM = (
    "BLOCKED_UNAUTHORISED_INGESTION_CLAIM"
)
BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM = (
    "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
)
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)

PHASE_NAME = "Minerva Governed Evidence Intake Phase Closeout / Intake Runbook v0.1"
PROGRESS_BEFORE_SLICE = "approximately 85%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "Evidence intake taxonomy v0.1",
    "Evidence intake planning gate v0.1",
    "Evidence source-status boundary v0.1",
    "Golden intake fixture baselines v0.1",
)

REMAINING_WORK = (
    "Choose the next Minerva evidence phase deliberately before authorising further work.",
)

NEXT_DECISION_POINT = (
    "Choose one explicit next phase before authorising any ingestion, corpus "
    "mutation, Code Evidence ingestion, DB access, live retrieval, live LLM, "
    "answer generation, endpoint exposure, runtime integration, deployment, "
    "or production claim."
)

RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Controlled Evidence Intake Dry-Run / No-Corpus-Mutation.",
    "Option B: Controlled External Evidence Summary Catalogue.",
    "Option C: Code Evidence Readiness Planning.",
    "Option D: Keep Minerva paused while award recovery continues.",
)

NO_ACTION_ATTESTATION = (
    "No evidence ingestion, corpus mutation, Code Evidence ingestion, DB "
    "connection, DB read, DB write, migration, live retrieval backend change, "
    "live LLM call, final natural-language answer generation, chat exposure, "
    "endpoint exposure, route registration, UI change, workforce-platform "
    "runtime integration, ezeas-analytics runtime integration, deployment, "
    "production, or runtime action was performed or authorised by this closeout."
)

RUNBOOK_STEPS = (
    "Confirm a separate explicit future-ingestion slice has been authorised before any evidence movement.",
    "Classify candidate evidence with the controlled evidence taxonomy.",
    "Evaluate candidate evidence through the intake planning gate.",
    "Apply the source-status boundary and preserve required caveats.",
    "Run golden intake fixture/baseline regression before any later dry-run output is trusted.",
    "Stop if any step implies ingestion, corpus mutation, Code Evidence ingestion, DB access, live retrieval, live LLM use, answer generation, chat exposure, endpoint exposure, runtime integration, deployment, production, or runtime readiness.",
)

STOP_CONDITIONS = (
    "unauthorised evidence ingestion claim",
    "unauthorised corpus mutation claim",
    "unauthorised Code Evidence ingestion claim",
    "unauthorised DB access or DB write claim",
    "unauthorised live retrieval claim",
    "unauthorised live LLM claim",
    "unauthorised final answer generation claim",
    "unauthorised chat or endpoint exposure claim",
    "unauthorised workforce-platform runtime integration claim",
    "unauthorised analytics runtime integration claim",
    "production, deployment, or runtime readiness overstatement",
)

INGESTION_PATTERNS = (
    "evidence ingestion authorised",
    "evidence ingestion enabled",
    "evidence ingestion occurred",
    "ingestion authorised",
    "ingestion enabled",
    "ingested evidence",
)

CORPUS_OR_CODE_EVIDENCE_PATTERNS = (
    "corpus mutation authorised",
    "corpus mutation enabled",
    "corpus mutation occurred",
    "mutated the corpus",
    "code evidence ingestion authorised",
    "code evidence ingestion enabled",
    "code evidence ingestion occurred",
    "ingested code evidence",
)

RUNTIME_OR_PRODUCTION_PATTERNS = (
    "db access authorised",
    "db access occurred",
    "database access authorised",
    "database access occurred",
    "db reads authorised",
    "database reads authorised",
    "db writes authorised",
    "database writes authorised",
    "read from the database",
    "write to the database",
    "wrote to the database",
    "migration authorised",
    "migrations authorised",
    "live retrieval authorised",
    "live retrieval enabled",
    "live retrieval backend authorised",
    "live retrieval backend enabled",
    "live llm authorised",
    "live llm enabled",
    "calls the live llm",
    "final answer generation authorised",
    "final answer generation enabled",
    "final natural-language answer generation authorised",
    "final natural-language answer generation enabled",
    "chat exposure authorised",
    "chat exposure enabled",
    "internal chat authorised",
    "public chat authorised",
    "tenant chat authorised",
    "customer chat authorised",
    "endpoint exposure authorised",
    "endpoint exposed",
    "api endpoint authorised",
    "route registered",
    "workforce-platform runtime integration authorised",
    "workforce-platform runtime integration enabled",
    "analytics runtime integration authorised",
    "analytics runtime integration enabled",
    "ezeas-analytics runtime integration authorised",
    "ezeas-analytics runtime integration enabled",
    "runtime-ready",
    "runtime ready",
    "runtime readiness authorised",
    "runtime readiness permitted",
    "deployment-ready",
    "deployment ready",
    "deployment readiness authorised",
    "deployment readiness permitted",
    "production-ready",
    "production ready",
    "production readiness authorised",
    "production readiness permitted",
    "ready for production",
    "ready for deployment",
)


@dataclass(frozen=True)
class GovernedEvidenceIntakeCloseoutResult:
    closeout_id: str
    phase_name: str
    phase_status: str
    progress_before_slice: str
    progress_after_slice: str
    governed_evidence_intake_phase_complete: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    evidence_ingestion_authorised: bool
    corpus_mutation_authorised: bool
    code_evidence_ingestion_authorised: bool
    db_access_authorised: bool
    db_writes_authorised: bool
    live_retrieval_authorised: bool
    live_llm_authorised: bool
    final_answer_generation_authorised: bool
    chat_exposure_authorised: bool
    endpoint_exposure_authorised: bool
    workforce_runtime_integration_authorised: bool
    analytics_runtime_integration_authorised: bool
    production_readiness_claim_permitted: bool
    deployment_readiness_claim_permitted: bool
    runtime_readiness_claim_permitted: bool
    no_action_attestation: str
    runbook_steps: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    explanation: str
    review_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_governed_evidence_intake_closeout(
    *,
    completed_components: Any = COMPLETED_COMPONENTS,
    remaining_work: Any = REMAINING_WORK,
    next_decision_point: str = NEXT_DECISION_POINT,
    recommended_next_phase_options: Any = RECOMMENDED_NEXT_PHASE_OPTIONS,
    no_action_attestation: str = NO_ACTION_ATTESTATION,
    runbook_steps: Any = RUNBOOK_STEPS,
    stop_conditions: Any = STOP_CONDITIONS,
    notes: Any = (),
    claims: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return deterministic planning-only closeout metadata for governed evidence intake."""

    components = _as_tuple(completed_components)
    remaining = _as_tuple(remaining_work)
    options = _as_tuple(recommended_next_phase_options)
    steps = _as_tuple(runbook_steps)
    stops = _as_tuple(stop_conditions)
    review_flags = _review_flags(
        components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        no_action_attestation=no_action_attestation,
        runbook_steps=steps,
        stop_conditions=stops,
        notes=_as_tuple(notes),
        claims=claims or {},
    )
    phase_status = _phase_status(review_flags)
    complete = (
        phase_status == GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE
        and set(COMPLETED_COMPONENTS).issubset(set(components))
        and remaining == REMAINING_WORK
    )

    material = {
        "phase_name": PHASE_NAME,
        "phase_status": phase_status,
        "progress_before_slice": PROGRESS_BEFORE_SLICE,
        "progress_after_slice": PROGRESS_AFTER_SLICE,
        "completed_components": components,
        "remaining_work": remaining,
        "next_decision_point": next_decision_point,
        "recommended_next_phase_options": options,
        "no_action_attestation": no_action_attestation,
        "runbook_steps": steps,
        "stop_conditions": stops,
        "review_flags": review_flags,
    }

    return GovernedEvidenceIntakeCloseoutResult(
        closeout_id=_closeout_id(material),
        phase_name=PHASE_NAME,
        phase_status=phase_status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        governed_evidence_intake_phase_complete=complete,
        completed_components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        evidence_ingestion_authorised=False,
        corpus_mutation_authorised=False,
        code_evidence_ingestion_authorised=False,
        db_access_authorised=False,
        db_writes_authorised=False,
        live_retrieval_authorised=False,
        live_llm_authorised=False,
        final_answer_generation_authorised=False,
        chat_exposure_authorised=False,
        endpoint_exposure_authorised=False,
        workforce_runtime_integration_authorised=False,
        analytics_runtime_integration_authorised=False,
        production_readiness_claim_permitted=False,
        deployment_readiness_claim_permitted=False,
        runtime_readiness_claim_permitted=False,
        no_action_attestation=no_action_attestation,
        runbook_steps=steps,
        stop_conditions=stops,
        explanation=_explanation(phase_status, review_flags),
        review_flags=review_flags,
    ).to_dict()


def build_minerva_governed_evidence_intake_closeout(**kwargs: Any) -> dict[str, Any]:
    return build_governed_evidence_intake_closeout(**kwargs)


def _review_flags(
    *,
    components: tuple[Any, ...],
    remaining_work: tuple[Any, ...],
    next_decision_point: str,
    recommended_next_phase_options: tuple[Any, ...],
    no_action_attestation: str,
    runbook_steps: tuple[Any, ...],
    stop_conditions: tuple[Any, ...],
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
        runbook_steps=runbook_steps,
        stop_conditions=stop_conditions,
        notes=notes,
        claims=claims,
    )

    if not set(COMPLETED_COMPONENTS).issubset(set(str(item) for item in components)):
        flags.append("MISSING_COMPLETED_COMPONENT")
    if remaining_work != REMAINING_WORK:
        flags.append("REMAINING_WORK_NOT_LIMITED_TO_NEXT_PHASE_DECISION")
    if recommended_next_phase_options != RECOMMENDED_NEXT_PHASE_OPTIONS:
        flags.append("NEXT_PHASE_OPTIONS_NOT_EXPLICIT")
    if not no_action_attestation:
        flags.append("NO_ACTION_ATTESTATION_MISSING")
    if runbook_steps != RUNBOOK_STEPS:
        flags.append("RUNBOOK_STEPS_NOT_CANONICAL")
    if stop_conditions != STOP_CONDITIONS:
        flags.append("STOP_CONDITIONS_NOT_CANONICAL")
    if _contains_positive_claim(text, INGESTION_PATTERNS):
        flags.append(BLOCKED_UNAUTHORISED_INGESTION_CLAIM)
    if _contains_positive_claim(text, CORPUS_OR_CODE_EVIDENCE_PATTERNS):
        flags.append(BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM)
    if _contains_positive_claim(text, RUNTIME_OR_PRODUCTION_PATTERNS):
        flags.append(BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT)
    if any(bool(value) for value in claims.values()):
        flags.extend(_claim_flags(claims))

    return tuple(dict.fromkeys(flags))


def _claim_flags(claims: dict[str, Any]) -> tuple[str, ...]:
    flags: list[str] = []
    for key, value in claims.items():
        if not value:
            continue
        normalized_key = _normalize_text(str(key))
        if "ingestion" in normalized_key and "code evidence" not in normalized_key:
            flags.append(BLOCKED_UNAUTHORISED_INGESTION_CLAIM)
        elif "corpus" in normalized_key or "code evidence" in normalized_key:
            flags.append(BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM)
        elif any(
            term in normalized_key
            for term in (
                "db",
                "database",
                "retrieval",
                "llm",
                "answer",
                "chat",
                "endpoint",
                "route",
                "workforce",
                "analytics",
                "runtime",
                "production",
                "deployment",
                "migration",
            )
        ):
            flags.append(BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT)
        else:
            flags.append(NEEDS_REVIEW)
    return tuple(flags)


def _phase_status(review_flags: tuple[str, ...]) -> str:
    if BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM in review_flags:
        return BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM
    if BLOCKED_UNAUTHORISED_INGESTION_CLAIM in review_flags:
        return BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    if BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT in review_flags:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if review_flags:
        return NEEDS_REVIEW
    return GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE


def _metadata_text(
    *,
    components: tuple[Any, ...],
    remaining_work: tuple[Any, ...],
    next_decision_point: str,
    recommended_next_phase_options: tuple[Any, ...],
    no_action_attestation: str,
    runbook_steps: tuple[Any, ...],
    stop_conditions: tuple[Any, ...],
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
                *runbook_steps,
                *stop_conditions,
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
    return f"governed-evidence-intake-closeout-{digest}"


def _explanation(phase_status: str, review_flags: tuple[str, ...]) -> str:
    if phase_status == GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE:
        return (
            "Governed evidence intake is complete at planning/readiness level only; "
            "the next phase must be chosen deliberately before any ingestion or "
            "runtime behaviour is authorised."
        )
    return (
        "Governed evidence intake closeout requires review because blocked or "
        "overstated metadata was detected: "
        + ", ".join(review_flags)
        + "."
    )

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evaluation_batch_summary_service import (
    _has_positive_claim,
    _normalize_text,
)
from app.services.controlled_evidence_intake_dry_run_service import (
    NO_ACTION_ATTESTATION,
)


CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE = (
    "CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE"
)
NEEDS_REVIEW = "NEEDS_REVIEW"
BLOCKED_MUTATION_OR_INGESTION_CLAIM = "BLOCKED_MUTATION_OR_INGESTION_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM"
)

PHASE_NAME = "Controlled Evidence Intake Dry-Run Phase Closeout / No-Mutation Ledger v0.1"
PROGRESS_BEFORE_SLICE = "approximately 90%"
PROGRESS_AFTER_SLICE = "100%"

COMPLETED_COMPONENTS = (
    "Controlled evidence intake dry-run service v0.1",
    "Controlled evidence intake dry-run summary service v0.1",
    "Controlled evidence intake fixture execution service v0.1",
    "Controlled evidence intake review pack service v0.1",
    "Controlled evidence intake fixture pack / golden intake baselines v0.1",
    "Evidence intake taxonomy v0.1",
    "Evidence intake planning gate v0.1",
    "Evidence source-status boundary v0.1",
)

REMAINING_WORK = (
    "Choose the next controlled evidence intake phase before authorising further work.",
)

NEXT_DECISION_POINT = (
    "Choose one explicit next phase before authorising evidence ingestion, corpus "
    "mutation, Code Evidence ingestion, DB access, DB writes, live retrieval, "
    "live LLM use, final answer generation, chat exposure, endpoint exposure, "
    "runtime integration, deployment, production, or runtime readiness claims."
)

RECOMMENDED_NEXT_PHASE_OPTIONS = (
    "Option A: Controlled Evidence Intake Authorisation Gate / First No-Mutation Intake Candidate.",
    "Option B: Controlled External Evidence Summary Catalogue.",
    "Option C: Code Evidence Readiness Planning.",
    "Option D: Keep Minerva paused while award recovery continues.",
)

PROHIBITED_ACTION_STATES = (
    ("evidence_ingestion", "performed", False),
    ("corpus_mutation", "performed", False),
    ("code_evidence_ingestion", "performed", False),
    ("db_access", "performed", False),
    ("db_write", "performed", False),
    ("live_retrieval", "performed", False),
    ("live_llm", "performed", False),
    ("final_answer_generation", "performed", False),
    ("chat_exposure", "authorised", False),
    ("endpoint_exposure", "authorised", False),
    ("workforce_runtime_integration", "authorised", False),
    ("analytics_runtime_integration", "authorised", False),
    ("production_readiness_claim", "permitted", False),
    ("deployment_readiness_claim", "permitted", False),
    ("runtime_readiness_claim", "permitted", False),
)

MUTATION_OR_INGESTION_PATTERNS = (
    "evidence ingestion authorised",
    "evidence ingestion enabled",
    "evidence ingestion performed",
    "evidence ingestion occurred",
    "ingestion authorised",
    "ingestion enabled",
    "ingestion performed",
    "ingested evidence",
    "corpus mutation authorised",
    "corpus mutation enabled",
    "corpus mutation performed",
    "corpus mutation occurred",
    "mutated the corpus",
    "code evidence ingestion authorised",
    "code evidence ingestion enabled",
    "code evidence ingestion performed",
    "code evidence ingestion occurred",
    "ingested code evidence",
)

RUNTIME_OR_PRODUCTION_PATTERNS = (
    "db access authorised",
    "db access performed",
    "db access occurred",
    "database access authorised",
    "database access occurred",
    "db read authorised",
    "db reads authorised",
    "database reads authorised",
    "db write authorised",
    "db writes authorised",
    "database writes authorised",
    "read from the database",
    "write to the database",
    "wrote to the database",
    "migration authorised",
    "migrations authorised",
    "live retrieval authorised",
    "live retrieval enabled",
    "live retrieval performed",
    "live retrieval backend authorised",
    "live retrieval backend enabled",
    "live llm authorised",
    "live llm enabled",
    "live llm performed",
    "calls the live llm",
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

EXPOSURE_OR_FINAL_ANSWER_PATTERNS = (
    "final answer generation authorised",
    "final answer generation enabled",
    "final answer generation performed",
    "final natural-language answer generation authorised",
    "final natural-language answer generation enabled",
    "chat exposure authorised",
    "chat exposure enabled",
    "internal chat authorised",
    "public chat authorised",
    "tenant chat authorised",
    "customer chat authorised",
    "endpoint exposure authorised",
    "endpoint exposure enabled",
    "endpoint exposed",
    "api endpoint authorised",
    "route registered",
    "route registration authorised",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeDryRunCloseoutResult:
    closeout_id: str
    phase_name: str
    phase_status: str
    progress_before_slice: str
    progress_after_slice: str
    controlled_dry_run_phase_complete: bool
    completed_components: tuple[str, ...]
    remaining_work: tuple[str, ...]
    next_decision_point: str
    recommended_next_phase_options: tuple[str, ...]
    evidence_ingestion_performed: bool
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
    no_mutation_ledger: tuple[dict[str, Any], ...]
    no_action_attestation: str
    explanation: str
    review_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_evidence_intake_dry_run_closeout(
    *,
    completed_components: Any = COMPLETED_COMPONENTS,
    remaining_work: Any = REMAINING_WORK,
    next_decision_point: str = NEXT_DECISION_POINT,
    recommended_next_phase_options: Any = RECOMMENDED_NEXT_PHASE_OPTIONS,
    no_action_attestation: str = NO_ACTION_ATTESTATION,
    notes: Any = (),
    claims: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return deterministic closeout metadata for the non-mutating dry-run phase."""

    components = _as_tuple(completed_components)
    remaining = _as_tuple(remaining_work)
    options = _as_tuple(recommended_next_phase_options)
    ledger = _no_mutation_ledger()
    review_flags = _review_flags(
        components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        no_action_attestation=no_action_attestation,
        notes=_as_tuple(notes),
        claims=claims or {},
    )
    phase_status = _phase_status(review_flags)
    complete = (
        phase_status == CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE
        and set(COMPLETED_COMPONENTS).issubset(set(str(item) for item in components))
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
        "no_mutation_ledger": ledger,
        "no_action_attestation": no_action_attestation,
        "review_flags": review_flags,
    }

    return ControlledEvidenceIntakeDryRunCloseoutResult(
        closeout_id=_closeout_id(material),
        phase_name=PHASE_NAME,
        phase_status=phase_status,
        progress_before_slice=PROGRESS_BEFORE_SLICE,
        progress_after_slice=PROGRESS_AFTER_SLICE,
        controlled_dry_run_phase_complete=complete,
        completed_components=components,
        remaining_work=remaining,
        next_decision_point=next_decision_point,
        recommended_next_phase_options=options,
        evidence_ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_access_performed=False,
        db_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        chat_exposure_authorised=False,
        endpoint_exposure_authorised=False,
        workforce_runtime_integration_authorised=False,
        analytics_runtime_integration_authorised=False,
        production_readiness_claim_permitted=False,
        deployment_readiness_claim_permitted=False,
        runtime_readiness_claim_permitted=False,
        no_mutation_ledger=ledger,
        no_action_attestation=no_action_attestation,
        explanation=_explanation(phase_status, review_flags),
        review_flags=review_flags,
    ).to_dict()


def build_minerva_controlled_evidence_intake_dry_run_closeout(
    **kwargs: Any,
) -> dict[str, Any]:
    return build_controlled_evidence_intake_dry_run_closeout(**kwargs)


def _no_mutation_ledger() -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "action": action,
            state_field: state,
            "state": "false" if state is False else str(state).lower(),
            "authorised": False,
        }
        for action, state_field, state in PROHIBITED_ACTION_STATES
    )


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

    if not set(COMPLETED_COMPONENTS).issubset(set(str(item) for item in components)):
        flags.append("MISSING_COMPLETED_COMPONENT")
    if remaining_work != REMAINING_WORK:
        flags.append("REMAINING_WORK_NOT_LIMITED_TO_NEXT_PHASE_DECISION")
    if recommended_next_phase_options != RECOMMENDED_NEXT_PHASE_OPTIONS:
        flags.append("NEXT_PHASE_OPTIONS_NOT_EXPLICIT")
    if not no_action_attestation:
        flags.append("NO_ACTION_ATTESTATION_MISSING")
    if _contains_positive_claim(text, MUTATION_OR_INGESTION_PATTERNS):
        flags.append(BLOCKED_MUTATION_OR_INGESTION_CLAIM)
    if _contains_positive_claim(text, RUNTIME_OR_PRODUCTION_PATTERNS):
        flags.append(BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT)
    if _contains_positive_claim(text, EXPOSURE_OR_FINAL_ANSWER_PATTERNS):
        flags.append(BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM)
    if any(bool(value) for value in claims.values()):
        flags.extend(_claim_flags(claims))

    return tuple(dict.fromkeys(flags))


def _claim_flags(claims: dict[str, Any]) -> tuple[str, ...]:
    flags: list[str] = []
    for key, value in claims.items():
        if not value:
            continue
        normalized_key = _normalize_text(str(key))
        if (
            "ingestion" in normalized_key
            or "corpus" in normalized_key
            or "code evidence" in normalized_key
        ):
            flags.append(BLOCKED_MUTATION_OR_INGESTION_CLAIM)
        elif any(
            term in normalized_key
            for term in (
                "answer",
                "chat",
                "endpoint",
                "route",
                "exposure",
            )
        ):
            flags.append(BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM)
        elif any(
            term in normalized_key
            for term in (
                "db",
                "database",
                "retrieval",
                "llm",
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
    if BLOCKED_MUTATION_OR_INGESTION_CLAIM in review_flags:
        return BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM in review_flags:
        return BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    if BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT in review_flags:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if review_flags:
        return NEEDS_REVIEW
    return CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE


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
    return f"controlled-evidence-intake-dry-run-closeout-{digest}"


def _explanation(phase_status: str, review_flags: tuple[str, ...]) -> str:
    if phase_status == CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE:
        return (
            "Controlled evidence intake dry-run is complete at controlled-readiness "
            "level only; no ingestion, mutation, runtime exposure, or readiness "
            "claim is authorised, and the next phase must be explicitly chosen."
        )
    return (
        "Controlled evidence intake dry-run closeout requires review because "
        "blocked or overstated metadata was detected: "
        + ", ".join(review_flags)
        + "."
    )

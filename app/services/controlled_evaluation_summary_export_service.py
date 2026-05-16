import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evaluation_batch_summary_service import (
    PROHIBITED_METADATA_CLAIM_FAILURE,
    PROHIBITED_POSITIVE_PATTERNS,
    _has_positive_claim,
    _normalize_text,
)


CONTROLLED_INTERNAL_SUMMARY = "CONTROLLED_INTERNAL_SUMMARY"
DEVELOPER_HANDOFF_SUMMARY = "DEVELOPER_HANDOFF_SUMMARY"
CI_CHECK_SUMMARY = "CI_CHECK_SUMMARY"
PHASE_PROGRESS_SUMMARY = "PHASE_PROGRESS_SUMMARY"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

SUPPORTED_EXPORT_TYPES = (
    CONTROLLED_INTERNAL_SUMMARY,
    DEVELOPER_HANDOFF_SUMMARY,
    CI_CHECK_SUMMARY,
    PHASE_PROGRESS_SUMMARY,
)

DEFAULT_PROHIBITED_CAPABILITIES_PRESERVED = (
    "RUNTIME_READINESS",
    "DEPLOYMENT_READINESS",
    "PRODUCTION_READINESS",
    "CHAT_EXPOSURE",
    "ENDPOINT_EXPOSURE",
    "LIVE_LLM",
    "DB_ACCESS",
    "DB_READS",
    "DB_WRITES",
    "MIGRATIONS",
    "CORPUS_MUTATION",
    "CODE_EVIDENCE_INGESTION",
    "WORKFORCE_RUNTIME_INTEGRATION",
    "ANALYTICS_RUNTIME_INTEGRATION",
    "FINAL_ANSWER_GENERATION",
)

DEFAULT_EXPORT_CAVEATS = (
    "Internal deterministic evaluation metadata only.",
    "No runtime, deployment, production, chat, endpoint, live LLM, DB, corpus, "
    "Code Evidence, workforce-platform, analytics, or final-answer-generation "
    "capability is authorised.",
)

NO_ACTION_ATTESTATION = (
    "No runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, final "
    "answer generation, UI, deployment, production, migration, credential, or "
    "cross-repo runtime action was performed by this in-memory export service."
)


@dataclass(frozen=True)
class ControlledEvaluationSummaryExportResult:
    export_id: str
    source_summary_id: str
    export_type: str
    phase_name: str
    generated_from_controlled_inputs: bool
    overall_status: str
    all_passed: bool
    total_fixtures: int
    passed_fixtures: int
    failed_fixtures: int
    safety_failures: tuple[str, ...]
    drift_failures: tuple[str, ...]
    blocked_claim_failures: tuple[str, ...]
    remaining_phase_work: tuple[Any, ...]
    recommended_next_slice: str
    progress_before_slice: Any
    progress_after_slice: Any
    safe_for_developer_handoff: bool
    safe_for_final_answer_generation: bool
    no_action_attestation: str
    prohibited_capabilities_preserved: tuple[str, ...]
    export_caveats: tuple[str, ...]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def export_controlled_evaluation_summary(
    batch_summary: dict[str, Any],
    *,
    export_type: str = CONTROLLED_INTERNAL_SUMMARY,
    generated_from_controlled_inputs: bool = True,
    export_caveats: Any = DEFAULT_EXPORT_CAVEATS,
    prohibited_capabilities_preserved: Any = DEFAULT_PROHIBITED_CAPABILITIES_PRESERVED,
) -> dict[str, Any]:
    """Return deterministic in-memory export metadata for a controlled batch summary."""

    normalized_export_type = (
        export_type if export_type in SUPPORTED_EXPORT_TYPES else UNKNOWN_REQUIRES_REVIEW
    )
    caveats = _as_tuple(export_caveats)
    preserved_capabilities = _as_tuple(prohibited_capabilities_preserved)
    summary_safety_failures = _as_tuple(batch_summary.get("safety_failures"))
    summary_drift_failures = _as_tuple(batch_summary.get("drift_failures"))
    summary_blocked_claim_failures = _as_tuple(
        batch_summary.get("blocked_claim_failures")
    )
    export_policy_failures = _export_policy_failures(
        batch_summary=batch_summary,
        export_type=normalized_export_type,
        generated_from_controlled_inputs=generated_from_controlled_inputs,
        export_caveats=caveats,
        prohibited_capabilities_preserved=preserved_capabilities,
    )
    safety_failures = _dedupe(summary_safety_failures + export_policy_failures)
    drift_failures = _dedupe(summary_drift_failures + export_policy_failures)
    all_passed = bool(batch_summary.get("all_passed")) and not export_policy_failures
    overall_status = "PASS" if all_passed else "FAIL"
    safe_for_developer_handoff = (
        normalized_export_type == DEVELOPER_HANDOFF_SUMMARY
        and all_passed
        and bool(batch_summary.get("safe_for_developer_handoff"))
        and bool(caveats)
        and bool(batch_summary.get("no_action_attestation"))
    )

    material = {
        "source_summary_id": batch_summary.get("summary_id", ""),
        "export_type": normalized_export_type,
        "generated_from_controlled_inputs": generated_from_controlled_inputs,
        "overall_status": overall_status,
        "safety_failures": safety_failures,
        "drift_failures": drift_failures,
        "blocked_claim_failures": summary_blocked_claim_failures,
        "progress_before_slice": batch_summary.get(
            "current_phase_progress_before_slice"
        ),
        "progress_after_slice": batch_summary.get(
            "expected_phase_progress_after_slice"
        ),
        "export_caveats": caveats,
        "prohibited_capabilities_preserved": preserved_capabilities,
    }

    return ControlledEvaluationSummaryExportResult(
        export_id=_export_id(material),
        source_summary_id=str(batch_summary.get("summary_id", "")),
        export_type=normalized_export_type,
        phase_name=str(batch_summary.get("phase_name", "")),
        generated_from_controlled_inputs=generated_from_controlled_inputs,
        overall_status=overall_status,
        all_passed=all_passed,
        total_fixtures=int(batch_summary.get("total_fixtures", 0)),
        passed_fixtures=int(batch_summary.get("passed_fixtures", 0)),
        failed_fixtures=int(batch_summary.get("failed_fixtures", 0)),
        safety_failures=safety_failures,
        drift_failures=drift_failures,
        blocked_claim_failures=summary_blocked_claim_failures,
        remaining_phase_work=_as_tuple(batch_summary.get("remaining_phase_work")),
        recommended_next_slice=str(batch_summary.get("recommended_next_slice", "")),
        progress_before_slice=batch_summary.get("current_phase_progress_before_slice"),
        progress_after_slice=batch_summary.get("expected_phase_progress_after_slice"),
        safe_for_developer_handoff=safe_for_developer_handoff,
        safe_for_final_answer_generation=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        prohibited_capabilities_preserved=preserved_capabilities,
        export_caveats=caveats,
        explanation=_explanation(normalized_export_type, overall_status, safety_failures),
    ).to_dict()


def build_controlled_evaluation_summary_export(
    batch_summary: dict[str, Any],
    **metadata: Any,
) -> dict[str, Any]:
    return export_controlled_evaluation_summary(batch_summary, **metadata)


def _export_policy_failures(
    *,
    batch_summary: dict[str, Any],
    export_type: str,
    generated_from_controlled_inputs: bool,
    export_caveats: tuple[Any, ...],
    prohibited_capabilities_preserved: tuple[Any, ...],
) -> tuple[str, ...]:
    failures: list[str] = []
    if export_type == UNKNOWN_REQUIRES_REVIEW:
        failures.append("UNKNOWN_EXPORT_TYPE_REQUIRES_REVIEW")
    if export_type == DEVELOPER_HANDOFF_SUMMARY:
        if not export_caveats or not batch_summary.get("no_action_attestation"):
            failures.append("DEVELOPER_HANDOFF_BOUNDARY_MISSING")
    if export_type == CI_CHECK_SUMMARY and not generated_from_controlled_inputs:
        failures.append("CI_CHECK_REQUIRES_CONTROLLED_INPUTS")
    if not prohibited_capabilities_preserved:
        failures.append("PROHIBITED_CAPABILITIES_BOUNDARY_MISSING")
    if _contains_positive_prohibited_claim(batch_summary, export_caveats):
        failures.append(PROHIBITED_METADATA_CLAIM_FAILURE)
    return tuple(failures)


def _contains_positive_prohibited_claim(
    batch_summary: dict[str, Any],
    export_caveats: tuple[Any, ...],
) -> bool:
    text = _normalize_text(
        json.dumps(batch_summary, sort_keys=True, default=str)
        + "\n"
        + "\n".join(str(item) for item in export_caveats)
    )
    return any(_has_positive_claim(text, pattern) for pattern in PROHIBITED_POSITIVE_PATTERNS)


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


def _dedupe(values: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if value))


def _export_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"controlled-evaluation-summary-export-{digest}"


def _explanation(
    export_type: str,
    overall_status: str,
    safety_failures: tuple[str, ...],
) -> str:
    if overall_status == "PASS":
        return (
            f"{export_type} was produced from deterministic controlled inputs for "
            "internal evaluation metadata only."
        )
    if safety_failures:
        return (
            f"{export_type} requires review because export safety checks failed: "
            + ", ".join(safety_failures)
            + "."
        )
    return f"{export_type} requires review because the source summary did not pass."

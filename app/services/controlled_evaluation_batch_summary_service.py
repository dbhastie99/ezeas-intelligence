import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


DEFAULT_PHASE_NAME = (
    "Controlled regression execution and internal evaluation summary readiness"
)
DEFAULT_REMAINING_PHASE_WORK = (
    "Add controlled regression summary consumers.",
    "Add next-slice readiness reporting around deterministic batch results.",
    "Keep internal chat exposure, runtime retrieval, live LLM use, DB access, "
    "corpus mutation, Code Evidence ingestion, and cross-repo runtime integration deferred.",
)
DEFAULT_RECOMMENDED_NEXT_SLICE = (
    "Add a controlled evaluation summary consumer for developer handoff metadata "
    "without enabling runtime, chat exposure, DB access, live LLM use, or final answer generation."
)
PROHIBITED_METADATA_CLAIM_FAILURE = "PROHIBITED_SUMMARY_METADATA_CLAIM"

PROHIBITED_POSITIVE_PATTERNS = (
    "production-ready",
    "production ready",
    "ready for production",
    "deployment-ready",
    "deployment ready",
    "ready for deployment",
    "runtime-ready",
    "runtime ready",
    "runtime enabled",
    "chat exposure enabled",
    "internal chat enabled",
    "public chat enabled",
    "tenant chat enabled",
    "customer chat enabled",
    "endpoint exposed",
    "api endpoint enabled",
    "route registered",
    "final answer generation enabled",
    "final natural-language answer generation enabled",
    "live llm enabled",
    "calls the live llm",
    "db access occurred",
    "database access occurred",
    "read from the database",
    "write to the database",
    "wrote to the database",
    "corpus mutation occurred",
    "mutated the corpus",
    "code evidence ingestion occurred",
    "ingested code evidence",
    "workforce-platform runtime integration enabled",
    "analytics runtime integration enabled",
    "ezeas-analytics runtime integration enabled",
)

NEGATION_PATTERNS = (
    "no ",
    "not ",
    "never ",
    "without ",
    "deferred",
    "pending",
    "not performed",
    "has not occurred",
    "did not occur",
    "does not ",
    "must not ",
    "is not ",
    "remains deferred",
)


@dataclass(frozen=True)
class ControlledEvaluationBatchSummaryResult:
    summary_id: str
    source_batch_id: str
    phase_name: str
    current_phase_progress_before_slice: Any
    expected_phase_progress_after_slice: Any
    overall_status: str
    all_passed: bool
    total_fixtures: int
    passed_fixtures: int
    failed_fixtures: int
    safety_failures: tuple[str, ...]
    drift_failures: tuple[str, ...]
    blocked_claim_failures: tuple[str, ...]
    remaining_phase_work: tuple[str, ...]
    recommended_next_slice: str
    safe_for_developer_handoff: bool
    safe_for_final_answer_generation: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def summarize_controlled_evaluation_batch_result(
    batch_result: dict[str, Any],
    *,
    phase_name: str = DEFAULT_PHASE_NAME,
    current_phase_progress_before_slice: Any = "35%",
    expected_phase_progress_after_slice: Any = "70%",
    remaining_phase_work: Any = DEFAULT_REMAINING_PHASE_WORK,
    recommended_next_slice: str = DEFAULT_RECOMMENDED_NEXT_SLICE,
) -> dict[str, Any]:
    remaining = _as_tuple(remaining_phase_work)
    metadata_claim_failures = _prohibited_metadata_claim_failures(
        phase_name=phase_name,
        remaining_phase_work=remaining,
        recommended_next_slice=recommended_next_slice,
    )
    safety_failures = _safety_failures(batch_result, metadata_claim_failures)
    drift_failures = _drift_failures(batch_result, metadata_claim_failures)
    all_passed = bool(batch_result.get("all_passed")) and not metadata_claim_failures
    overall_status = "PASS" if all_passed else "FAIL"
    safe_for_developer_handoff = (
        all_passed
        and not safety_failures
        and bool(batch_result.get("safe_for_controlled_evaluation_summary"))
        and bool(batch_result.get("no_action_attestation"))
    )

    material = {
        "batch_result": batch_result,
        "phase_name": phase_name,
        "current_phase_progress_before_slice": current_phase_progress_before_slice,
        "expected_phase_progress_after_slice": expected_phase_progress_after_slice,
        "remaining_phase_work": remaining,
        "recommended_next_slice": recommended_next_slice,
        "overall_status": overall_status,
        "safety_failures": safety_failures,
        "drift_failures": drift_failures,
    }

    return ControlledEvaluationBatchSummaryResult(
        summary_id=_summary_id(material),
        source_batch_id=str(batch_result.get("batch_id", "")),
        phase_name=phase_name,
        current_phase_progress_before_slice=current_phase_progress_before_slice,
        expected_phase_progress_after_slice=expected_phase_progress_after_slice,
        overall_status=overall_status,
        all_passed=all_passed,
        total_fixtures=int(batch_result.get("fixture_count", 0)),
        passed_fixtures=int(batch_result.get("passed_count", 0)),
        failed_fixtures=int(batch_result.get("failed_count", 0)),
        safety_failures=safety_failures,
        drift_failures=drift_failures,
        blocked_claim_failures=_as_tuple(batch_result.get("blocked_claim_failures")),
        remaining_phase_work=remaining,
        recommended_next_slice=recommended_next_slice,
        safe_for_developer_handoff=safe_for_developer_handoff,
        safe_for_final_answer_generation=False,
        no_action_attestation=(
            "No runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, "
            "final answer generation, UI, deployment, production, migration, credential, "
            "or cross-repo runtime action was performed by this summary model."
        ),
        explanation=_explanation(overall_status, batch_result, safety_failures, drift_failures),
    ).to_dict()


def build_controlled_evaluation_batch_summary(
    batch_result: dict[str, Any],
    **metadata: Any,
) -> dict[str, Any]:
    return summarize_controlled_evaluation_batch_result(batch_result, **metadata)


def _safety_failures(
    batch_result: dict[str, Any],
    metadata_claim_failures: tuple[str, ...],
) -> tuple[str, ...]:
    failures: list[str] = []
    failures.extend(_as_tuple(batch_result.get("final_answer_generation_safety_failures")))
    failures.extend(_as_tuple(batch_result.get("runtime_or_exposure_safety_failures")))
    failures.extend(metadata_claim_failures)
    return tuple(dict.fromkeys(str(failure) for failure in failures if failure))


def _drift_failures(
    batch_result: dict[str, Any],
    metadata_claim_failures: tuple[str, ...],
) -> tuple[str, ...]:
    failures: list[str] = []
    failures.extend(_as_tuple(batch_result.get("unexpected_publication_decision_failures")))
    failures.extend(_as_tuple(batch_result.get("missing_caveat_failures")))
    failures.extend(_as_tuple(batch_result.get("blocked_claim_failures")))
    failures.extend(metadata_claim_failures)
    return tuple(dict.fromkeys(str(failure) for failure in failures if failure))


def _prohibited_metadata_claim_failures(
    *,
    phase_name: str,
    remaining_phase_work: tuple[Any, ...],
    recommended_next_slice: str,
) -> tuple[str, ...]:
    text = _normalize_text(
        "\n".join(
            (
                phase_name,
                recommended_next_slice,
                "\n".join(str(item) for item in remaining_phase_work),
            )
        )
    )
    if any(_has_positive_claim(text, pattern) for pattern in PROHIBITED_POSITIVE_PATTERNS):
        return (PROHIBITED_METADATA_CLAIM_FAILURE,)
    return ()


def _has_positive_claim(normalized_text: str, pattern: str) -> bool:
    start = normalized_text.find(pattern)
    while start != -1:
        if not _is_negated(normalized_text, start):
            return True
        start = normalized_text.find(pattern, start + len(pattern))
    return False


def _is_negated(normalized_text: str, start: int) -> bool:
    window_start = max(0, start - 50)
    window = normalized_text[window_start:start]
    return any(negation in window for negation in NEGATION_PATTERNS)


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


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().replace("_", " ").split())


def _summary_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"controlled-evaluation-summary-{digest}"


def _explanation(
    overall_status: str,
    batch_result: dict[str, Any],
    safety_failures: tuple[str, ...],
    drift_failures: tuple[str, ...],
) -> str:
    if overall_status == "PASS":
        return (
            "The controlled evaluation batch passed and the summary remains internal "
            "developer-handoff metadata only."
        )
    failure_parts = []
    if safety_failures:
        failure_parts.append("safety failures: " + ", ".join(safety_failures))
    if drift_failures:
        failure_parts.append("drift failures: " + ", ".join(drift_failures))
    if not failure_parts and not batch_result.get("all_passed"):
        failure_parts.append("one or more fixtures failed")
    return "The controlled evaluation batch summary failed due to " + "; ".join(failure_parts) + "."

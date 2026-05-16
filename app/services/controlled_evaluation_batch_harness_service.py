import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from app.services.controlled_evaluation_report_assembler_service import (
    assemble_controlled_evaluation_report,
)
from app.services.evaluation_output_publication_gate_service import (
    evaluate_evaluation_output_publication_gate,
)


FINAL_ANSWER_GENERATION_FAILURE = "FINAL_ANSWER_GENERATION_MARKED_SAFE"
NO_ACTION_FAILURE = "NO_ACTION_ATTESTATION_MISMATCH"
PRESERVED_BOUNDARY_FAILURE = "PRESERVED_BOUNDARIES_MISMATCH"
MISSING_CAVEAT_FAILURE = "REQUIRED_CAVEATS_MISSING"
PUBLICATION_DECISION_FAILURE = "PUBLICATION_DECISION_MISMATCH"
CONTROLLED_REPORT_SAFETY_FAILURE = "CONTROLLED_EVALUATION_REPORT_SAFETY_MISMATCH"
VIOLATED_BOUNDARY_FAILURE = "VIOLATED_BOUNDARIES_MISMATCH"
BLOCK_REASON_FAILURE = "BLOCK_REASONS_MISMATCH"

RUNTIME_OR_EXPOSURE_BOUNDARIES = {
    "PRODUCTION_READINESS",
    "DEPLOYMENT_READINESS",
    "RUNTIME_READINESS",
    "CHAT_EXPOSURE",
    "ENDPOINT_EXPOSURE",
    "LIVE_LLM",
    "DB_ACCESS",
    "DB_VALIDATION",
    "CORPUS_MUTATION",
    "CODE_EVIDENCE_INGESTION",
    "WORKFORCE_RUNTIME_INTEGRATION",
    "ANALYTICS_RUNTIME_INTEGRATION",
}


@dataclass(frozen=True)
class ControlledEvaluationFixtureResult:
    fixture_id: str
    fixture_path: str
    fixture_purpose: str
    passed: bool
    expected_publication_decision: Any
    actual_publication_decision: str
    expected_safe_for_controlled_evaluation_report: Any
    actual_safe_for_controlled_evaluation_report: bool
    expected_safe_for_final_answer_generation: Any
    actual_safe_for_final_answer_generation: bool
    failures: tuple[str, ...]
    preserved_boundaries: tuple[str, ...]
    violated_boundaries: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ControlledEvaluationBatchHarnessResult:
    batch_id: str
    fixture_count: int
    passed_count: int
    failed_count: int
    skipped_count: int
    all_passed: bool
    fixture_results: tuple[dict[str, Any], ...]
    blocked_claim_failures: tuple[str, ...]
    missing_caveat_failures: tuple[str, ...]
    unexpected_publication_decision_failures: tuple[str, ...]
    final_answer_generation_safety_failures: tuple[str, ...]
    runtime_or_exposure_safety_failures: tuple[str, ...]
    deterministic_output: bool
    safe_for_controlled_evaluation_summary: bool
    safe_for_final_answer_generation: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_evaluation_fixture_payloads(
    fixture_payloads: Iterable[dict[str, Any]],
    *,
    batch_id: str | None = None,
) -> dict[str, Any]:
    fixtures = [
        _fixture_entry(payload=payload, fixture_path="")
        for payload in fixture_payloads
    ]
    return _evaluate_batch(fixtures, batch_id=batch_id)


def evaluate_controlled_evaluation_fixture_paths(
    fixture_paths: Iterable[str | Path],
    *,
    batch_id: str | None = None,
) -> dict[str, Any]:
    fixtures = [
        _fixture_entry(payload=_load_fixture(path), fixture_path=str(Path(path)))
        for path in sorted((Path(path) for path in fixture_paths), key=lambda item: str(item))
    ]
    return _evaluate_batch(fixtures, batch_id=batch_id)


def evaluate_controlled_evaluation_fixture_directory(
    fixture_directory: str | Path,
    *,
    batch_id: str | None = None,
) -> dict[str, Any]:
    directory = Path(fixture_directory)
    fixture_paths = sorted(directory.glob("*.json"), key=lambda item: str(item))
    return evaluate_controlled_evaluation_fixture_paths(fixture_paths, batch_id=batch_id)


def _evaluate_batch(
    fixtures: list[dict[str, Any]],
    *,
    batch_id: str | None,
) -> dict[str, Any]:
    fixture_results = tuple(_evaluate_fixture(fixture) for fixture in fixtures)
    failed = tuple(result for result in fixture_results if not result["passed"])
    blocked_claim_failures = _failure_fixture_ids(
        failed,
        (BLOCK_REASON_FAILURE, VIOLATED_BOUNDARY_FAILURE),
    )
    missing_caveat_failures = _failure_fixture_ids(failed, (MISSING_CAVEAT_FAILURE,))
    publication_failures = _failure_fixture_ids(failed, (PUBLICATION_DECISION_FAILURE,))
    final_answer_failures = _failure_fixture_ids(
        failed,
        (FINAL_ANSWER_GENERATION_FAILURE,),
    )
    runtime_or_exposure_failures = _runtime_or_exposure_failures(failed)
    all_passed = not failed

    return ControlledEvaluationBatchHarnessResult(
        batch_id=batch_id or _batch_id(fixtures),
        fixture_count=len(fixtures),
        passed_count=len(fixture_results) - len(failed),
        failed_count=len(failed),
        skipped_count=0,
        all_passed=all_passed,
        fixture_results=fixture_results,
        blocked_claim_failures=blocked_claim_failures,
        missing_caveat_failures=missing_caveat_failures,
        unexpected_publication_decision_failures=publication_failures,
        final_answer_generation_safety_failures=final_answer_failures,
        runtime_or_exposure_safety_failures=runtime_or_exposure_failures,
        deterministic_output=True,
        safe_for_controlled_evaluation_summary=all_passed,
        safe_for_final_answer_generation=False,
        no_action_attestation=(
            "No runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, "
            "final answer generation, UI, deployment, production, or cross-repo action "
            "was performed by this in-memory batch harness."
        ),
        explanation=_batch_explanation(all_passed, failed),
    ).to_dict()


def _evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    payload = fixture["payload"]
    input_metadata = payload.get("input_metadata", {})
    actual = assemble_controlled_evaluation_report(input_metadata)
    gate = evaluate_evaluation_output_publication_gate(input_metadata)
    failures = _fixture_failures(payload, actual, gate)

    return ControlledEvaluationFixtureResult(
        fixture_id=str(payload.get("fixture_id", "")),
        fixture_path=fixture["fixture_path"],
        fixture_purpose=str(payload.get("fixture_purpose", "")),
        passed=not failures,
        expected_publication_decision=payload.get("expected_publication_decision"),
        actual_publication_decision=actual["publication_decision"],
        expected_safe_for_controlled_evaluation_report=payload.get(
            "expected_safe_for_controlled_evaluation_report"
        ),
        actual_safe_for_controlled_evaluation_report=actual[
            "safe_for_controlled_evaluation_report"
        ],
        expected_safe_for_final_answer_generation=payload.get(
            "expected_safe_for_final_answer_generation"
        ),
        actual_safe_for_final_answer_generation=actual[
            "safe_for_final_answer_generation"
        ],
        failures=failures,
        preserved_boundaries=tuple(actual.get("preserved_boundaries", ())),
        violated_boundaries=tuple(actual.get("violated_boundaries", ())),
    ).to_dict()


def _fixture_failures(
    payload: dict[str, Any],
    actual: dict[str, Any],
    gate: dict[str, Any],
) -> tuple[str, ...]:
    failures: list[str] = []

    if actual["publication_decision"] != payload.get("expected_publication_decision"):
        failures.append(PUBLICATION_DECISION_FAILURE)
    if actual["safe_for_controlled_evaluation_report"] is not payload.get(
        "expected_safe_for_controlled_evaluation_report"
    ):
        failures.append(CONTROLLED_REPORT_SAFETY_FAILURE)
    if actual["safe_for_final_answer_generation"] is not False:
        failures.append(FINAL_ANSWER_GENERATION_FAILURE)
    if payload.get("expected_safe_for_final_answer_generation") is not False:
        failures.append(FINAL_ANSWER_GENERATION_FAILURE)
    if tuple(payload.get("expected_preserved_boundaries", ())) != tuple(
        actual.get("preserved_boundaries", ())
    ):
        failures.append(PRESERVED_BOUNDARY_FAILURE)
    if tuple(payload.get("expected_violated_boundaries", ())) != tuple(
        actual.get("violated_boundaries", ())
    ):
        failures.append(VIOLATED_BOUNDARY_FAILURE)
    if tuple(payload.get("expected_block_reasons", ())) != tuple(
        gate.get("block_reasons", ())
    ):
        failures.append(BLOCK_REASON_FAILURE)
    if not set(payload.get("expected_required_caveats", ())).issubset(
        set(actual.get("required_caveats", ()))
    ):
        failures.append(MISSING_CAVEAT_FAILURE)
    if actual.get("no_action_attestation") != payload.get("expected_no_action_attestation"):
        failures.append(NO_ACTION_FAILURE)

    return tuple(dict.fromkeys(failures))


def _fixture_entry(payload: dict[str, Any], fixture_path: str) -> dict[str, Any]:
    return {
        "fixture_path": fixture_path,
        "payload": dict(payload),
    }


def _load_fixture(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _batch_id(fixtures: list[dict[str, Any]]) -> str:
    material = json.dumps(fixtures, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
    return f"controlled-evaluation-batch-{digest}"


def _failure_fixture_ids(
    failed_results: tuple[dict[str, Any], ...],
    failure_codes: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        result["fixture_id"]
        for result in failed_results
        if any(code in result["failures"] for code in failure_codes)
    )


def _runtime_or_exposure_failures(
    failed_results: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    return tuple(
        result["fixture_id"]
        for result in failed_results
        if any(boundary in RUNTIME_OR_EXPOSURE_BOUNDARIES for boundary in result["violated_boundaries"])
        or PRESERVED_BOUNDARY_FAILURE in result["failures"]
        or NO_ACTION_FAILURE in result["failures"]
    )


def _batch_explanation(all_passed: bool, failed: tuple[dict[str, Any], ...]) -> str:
    if all_passed:
        return (
            "All supplied controlled evaluation fixtures matched their deterministic "
            "expected metadata. The batch remains controlled-evaluation-summary only."
        )
    return (
        "One or more controlled evaluation fixtures drifted from expected metadata: "
        + ", ".join(result["fixture_id"] for result in failed)
        + "."
    )

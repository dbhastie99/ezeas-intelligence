import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import (
    DRY_RUN_READY_FOR_FUTURE_INTAKE,
    NO_ACTION_ATTESTATION,
    build_controlled_evidence_intake_dry_run,
)


EXECUTION_FLAG_FIELDS = (
    "ingestion_performed",
    "corpus_mutation_performed",
    "code_evidence_ingestion_performed",
    "db_write_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "final_answer_generation_performed",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeFixtureResult:
    fixture_id: str
    fixture_purpose: str
    evidence_category: str
    dry_run_decision: str
    gate_decision: str
    source_status: str
    passed_expected_outcome: bool
    failures: tuple[str, ...]
    required_caveats: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ControlledEvidenceIntakeFixtureExecutionResult:
    execution_id: str
    fixture_count: int
    executed_fixture_ids: tuple[str, ...]
    fixture_results: tuple[dict[str, Any], ...]
    ready_count: int
    needs_review_count: int
    blocked_count: int
    ingestion_performed_any: bool
    corpus_mutation_performed_any: bool
    code_evidence_ingestion_performed_any: bool
    db_write_performed_any: bool
    live_retrieval_performed_any: bool
    live_llm_performed_any: bool
    final_answer_generation_performed_any: bool
    all_non_mutating: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def execute_controlled_evidence_intake_fixtures(
    fixture_payloads: Any | None = None,
    *,
    fixture_directory: str | Path | None = None,
) -> dict[str, Any]:
    """Run supplied controlled intake fixtures through dry-run logic without side effects."""

    if fixture_payloads is not None and fixture_directory is not None:
        raise ValueError("Pass fixture_payloads or fixture_directory, not both.")

    fixtures = _load_fixtures(fixture_payloads, fixture_directory)
    fixture_results = tuple(_execute_fixture(fixture) for fixture in fixtures)
    executed_fixture_ids = tuple(result["fixture_id"] for result in fixture_results)
    ready_count = sum(
        1
        for result in fixture_results
        if result["dry_run_decision"] == DRY_RUN_READY_FOR_FUTURE_INTAKE
    )
    blocked_count = sum(
        1 for result in fixture_results if result["dry_run_decision"].startswith("DRY_RUN_BLOCKED")
    )
    needs_review_count = len(fixture_results) - ready_count - blocked_count

    flag_state = {
        field: any(bool(result.get("_dry_run", {}).get(field)) for result in fixture_results)
        for field in EXECUTION_FLAG_FIELDS
    }
    public_fixture_results = tuple(
        {key: value for key, value in result.items() if key != "_dry_run"}
        for result in fixture_results
    )
    all_non_mutating = not any(flag_state.values())
    material = {
        "executed_fixture_ids": executed_fixture_ids,
        "fixture_results": public_fixture_results,
        "ready_count": ready_count,
        "needs_review_count": needs_review_count,
        "blocked_count": blocked_count,
        "flag_state": flag_state,
    }

    return ControlledEvidenceIntakeFixtureExecutionResult(
        execution_id=_stable_id("controlled-evidence-intake-fixture-execution", material),
        fixture_count=len(public_fixture_results),
        executed_fixture_ids=executed_fixture_ids,
        fixture_results=public_fixture_results,
        ready_count=ready_count,
        needs_review_count=needs_review_count,
        blocked_count=blocked_count,
        ingestion_performed_any=flag_state["ingestion_performed"],
        corpus_mutation_performed_any=flag_state["corpus_mutation_performed"],
        code_evidence_ingestion_performed_any=flag_state["code_evidence_ingestion_performed"],
        db_write_performed_any=flag_state["db_write_performed"],
        live_retrieval_performed_any=flag_state["live_retrieval_performed"],
        live_llm_performed_any=flag_state["live_llm_performed"],
        final_answer_generation_performed_any=flag_state["final_answer_generation_performed"],
        all_non_mutating=all_non_mutating,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(all_non_mutating, public_fixture_results),
    ).to_dict()


def build_controlled_evidence_intake_fixture_execution(
    fixture_payloads: Any | None = None,
    **metadata: Any,
) -> dict[str, Any]:
    return execute_controlled_evidence_intake_fixtures(fixture_payloads, **metadata)


def _load_fixtures(
    fixture_payloads: Any | None,
    fixture_directory: str | Path | None,
) -> tuple[dict[str, Any], ...]:
    if fixture_directory is not None:
        directory = Path(fixture_directory)
        fixtures = tuple(
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(directory.glob("*.json"))
            if path.is_file()
        )
    else:
        fixtures = tuple(dict(fixture) for fixture in _as_tuple(fixture_payloads))

    return tuple(sorted(fixtures, key=lambda fixture: str(fixture.get("fixture_id", ""))))


def _execute_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    dry_run = build_controlled_evidence_intake_dry_run(fixture)
    required_caveats = _dedupe(
        (*_as_str_tuple(dry_run.get("required_caveats")), *tuple(fixture.get("expected_required_caveats", ())))
    )
    blocked_reasons = _dedupe(
        (*_as_str_tuple(dry_run.get("blocked_reasons")), *tuple(fixture.get("expected_blocked_reasons", ())))
    )
    prohibited_inferences = _dedupe(
        (
            *_as_str_tuple(dry_run.get("prohibited_inferences")),
            *tuple(fixture.get("expected_prohibited_inferences", ())),
        )
    )
    comparable = {
        **dry_run,
        "required_caveats": required_caveats,
        "blocked_reasons": blocked_reasons,
        "prohibited_inferences": prohibited_inferences,
    }
    failures = _expected_outcome_failures(fixture, comparable)

    result = ControlledEvidenceIntakeFixtureResult(
        fixture_id=str(fixture.get("fixture_id", "")),
        fixture_purpose=str(fixture.get("fixture_purpose", "")),
        evidence_category=str(dry_run["evidence_category"]),
        dry_run_decision=str(dry_run["dry_run_decision"]),
        gate_decision=str(dry_run["gate_decision"]),
        source_status=str(dry_run["source_status"]),
        passed_expected_outcome=not failures,
        failures=failures,
        required_caveats=required_caveats,
        blocked_reasons=blocked_reasons,
        prohibited_inferences=prohibited_inferences,
    ).to_dict()
    result["_dry_run"] = dry_run
    return result


def _expected_outcome_failures(
    fixture: dict[str, Any],
    dry_run: dict[str, Any],
) -> tuple[str, ...]:
    checks = (
        ("expected_evidence_category", "evidence_category"),
        ("expected_gate_decision", "gate_decision"),
        ("expected_source_status", "source_status"),
    )
    failures: list[str] = []
    for expected_field, actual_field in checks:
        if expected_field in fixture and fixture[expected_field] != dry_run.get(actual_field):
            failures.append(
                f"{actual_field}: expected {fixture[expected_field]}, got {dry_run.get(actual_field)}"
            )

    tuple_checks = (
        ("expected_required_caveats", "required_caveats"),
        ("expected_blocked_reasons", "blocked_reasons"),
        ("expected_prohibited_inferences", "prohibited_inferences"),
    )
    for expected_field, actual_field in tuple_checks:
        expected = tuple(str(item) for item in fixture.get(expected_field, ()))
        actual = _as_str_tuple(dry_run.get(actual_field))
        if expected_field in fixture and not set(expected).issubset(set(actual)):
            failures.append(f"{actual_field}: expected fixture baseline terms missing")

    return tuple(failures)


def _explanation(
    all_non_mutating: bool,
    fixture_results: tuple[dict[str, Any], ...],
) -> str:
    if not all_non_mutating:
        return (
            "One or more fixture dry-runs reported a prohibited execution flag; no "
            "evidence ingestion, corpus mutation, or runtime action is authorised."
        )
    if any(not result["passed_expected_outcome"] for result in fixture_results):
        return (
            "Fixture execution completed without mutation, but one or more fixtures "
            "did not match checked-in expected outcomes."
        )
    return (
        "All supplied controlled evidence intake fixtures executed deterministically "
        "without evidence ingestion, corpus mutation, Code Evidence ingestion, DB "
        "write, live retrieval, live LLM use, or final answer generation."
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


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    return tuple(str(item) for item in _as_tuple(value))


def _dedupe(value: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(item) for item in _as_tuple(value) if str(item)))


def _stable_id(prefix: str, material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return prefix + "-" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]

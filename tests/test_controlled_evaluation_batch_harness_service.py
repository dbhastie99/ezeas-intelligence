import json
from pathlib import Path

from app.services.controlled_evaluation_batch_harness_service import (
    FINAL_ANSWER_GENERATION_FAILURE,
    MISSING_CAVEAT_FAILURE,
    NO_ACTION_FAILURE,
    PRESERVED_BOUNDARY_FAILURE,
    PUBLICATION_DECISION_FAILURE,
    evaluate_controlled_evaluation_fixture_directory,
    evaluate_controlled_evaluation_fixture_payloads,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evaluation_reports"
EXPECTED_FIXTURE_COUNT = 15


def _load_fixtures():
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(FIXTURE_DIR.glob("*.json"))
    ]


def _fixture_by_id(fixture_id):
    return {
        fixture["fixture_id"]: fixture
        for fixture in _load_fixtures()
    }[fixture_id]


def _result_by_id(batch, fixture_id):
    return {
        result["fixture_id"]: result
        for result in batch["fixture_results"]
    }[fixture_id]


def test_all_existing_golden_fixtures_can_be_loaded_and_evaluated():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    assert batch["fixture_count"] == EXPECTED_FIXTURE_COUNT
    assert len(batch["fixture_results"]) == EXPECTED_FIXTURE_COUNT


def test_passing_batch_reports_expected_counts_and_all_passed_true():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    assert batch["fixture_count"] == EXPECTED_FIXTURE_COUNT
    assert batch["passed_count"] == EXPECTED_FIXTURE_COUNT
    assert batch["failed_count"] == 0
    assert batch["skipped_count"] == 0
    assert batch["all_passed"] is True


def test_safe_fixtures_pass():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    for fixture_id in (
        "safe_controlled_evaluation_report",
        "safe_developer_handoff",
        "safe_progress_summary",
        "safe_next_slice_recommendation",
    ):
        assert _result_by_id(batch, fixture_id)["passed"] is True


def test_blocked_overstatement_fixtures_pass_when_blocked_as_expected():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    blocked_results = [
        result
        for result in batch["fixture_results"]
        if result["fixture_id"].startswith("blocked_")
    ]
    assert blocked_results
    assert all(result["passed"] for result in blocked_results)


def test_mismatched_expected_publication_decision_fails():
    fixture = _fixture_by_id("safe_controlled_evaluation_report")
    fixture["expected_publication_decision"] = "BLOCKED_OVERSTATED_PRODUCTION"

    batch = evaluate_controlled_evaluation_fixture_payloads([fixture])
    result = batch["fixture_results"][0]

    assert batch["all_passed"] is False
    assert result["passed"] is False
    assert PUBLICATION_DECISION_FAILURE in result["failures"]
    assert batch["unexpected_publication_decision_failures"] == (
        "safe_controlled_evaluation_report",
    )


def test_fixture_safe_for_final_answer_generation_fails():
    fixture = _fixture_by_id("safe_controlled_evaluation_report")
    fixture["expected_safe_for_final_answer_generation"] = True

    batch = evaluate_controlled_evaluation_fixture_payloads([fixture])
    result = batch["fixture_results"][0]

    assert result["passed"] is False
    assert FINAL_ANSWER_GENERATION_FAILURE in result["failures"]
    assert batch["final_answer_generation_safety_failures"] == (
        "safe_controlled_evaluation_report",
    )


def test_missing_no_action_or_deferred_boundary_expectation_fails():
    fixture = _fixture_by_id("safe_controlled_evaluation_report")
    fixture["expected_no_action_attestation"] = "No action attestation drifted."
    fixture["expected_preserved_boundaries"] = ["CONTROLLED_READINESS_ONLY"]

    batch = evaluate_controlled_evaluation_fixture_payloads([fixture])
    result = batch["fixture_results"][0]

    assert result["passed"] is False
    assert NO_ACTION_FAILURE in result["failures"]
    assert PRESERVED_BOUNDARY_FAILURE in result["failures"]
    assert batch["runtime_or_exposure_safety_failures"] == (
        "safe_controlled_evaluation_report",
    )


def test_missing_required_caveat_fails():
    fixture = _fixture_by_id("safe_controlled_evaluation_report")
    fixture["expected_required_caveats"] = ["Required caveat that is not emitted."]

    batch = evaluate_controlled_evaluation_fixture_payloads([fixture])
    result = batch["fixture_results"][0]

    assert result["passed"] is False
    assert MISSING_CAVEAT_FAILURE in result["failures"]
    assert batch["missing_caveat_failures"] == ("safe_controlled_evaluation_report",)


def test_batch_output_is_deterministic_for_repeated_runs():
    first = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)
    second = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    assert first == second
    assert first["deterministic_output"] is True


def test_batch_is_never_safe_for_final_answer_generation():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    assert batch["safe_for_final_answer_generation"] is False
    assert all(
        result["actual_safe_for_final_answer_generation"] is False
        for result in batch["fixture_results"]
    )


def test_fixture_files_are_not_mutated_by_harness():
    before = {
        path.name: path.read_bytes()
        for path in sorted(FIXTURE_DIR.glob("*.json"))
    }

    evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    after = {
        path.name: path.read_bytes()
        for path in sorted(FIXTURE_DIR.glob("*.json"))
    }
    assert after == before


def test_harness_does_not_write_generated_reports_in_this_slice():
    before = {path.name for path in FIXTURE_DIR.iterdir()}

    evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)

    after = {path.name for path in FIXTURE_DIR.iterdir()}
    assert after == before

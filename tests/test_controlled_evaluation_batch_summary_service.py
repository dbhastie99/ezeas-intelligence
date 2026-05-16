import json
from pathlib import Path

from app.services.controlled_evaluation_batch_harness_service import (
    evaluate_controlled_evaluation_fixture_directory,
    evaluate_controlled_evaluation_fixture_payloads,
)
from app.services.controlled_evaluation_batch_summary_service import (
    PROHIBITED_METADATA_CLAIM_FAILURE,
    summarize_controlled_evaluation_batch_result,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evaluation_reports"


def _passing_batch():
    return evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)


def _failed_batch():
    fixture = json.loads(
        (FIXTURE_DIR / "safe_controlled_evaluation_report.json").read_text(
            encoding="utf-8"
        )
    )
    fixture["expected_publication_decision"] = "BLOCKED_OVERSTATED_PRODUCTION"
    return evaluate_controlled_evaluation_fixture_payloads([fixture])


def test_passing_batch_produces_pass_overall_status():
    summary = summarize_controlled_evaluation_batch_result(_passing_batch())

    assert summary["overall_status"] == "PASS"
    assert summary["all_passed"] is True


def test_failed_batch_produces_fail_overall_status():
    summary = summarize_controlled_evaluation_batch_result(_failed_batch())

    assert summary["overall_status"] == "FAIL"
    assert summary["all_passed"] is False
    assert summary["failed_fixtures"] == 1


def test_progress_before_and_after_percentages_are_preserved():
    summary = summarize_controlled_evaluation_batch_result(
        _passing_batch(),
        current_phase_progress_before_slice="35%",
        expected_phase_progress_after_slice="70%",
    )

    assert summary["current_phase_progress_before_slice"] == "35%"
    assert summary["expected_phase_progress_after_slice"] == "70%"


def test_remaining_phase_work_is_listed():
    remaining_work = (
        "Add controlled regression summary consumers.",
        "Add next-slice readiness reporting.",
    )

    summary = summarize_controlled_evaluation_batch_result(
        _passing_batch(),
        remaining_phase_work=remaining_work,
    )

    assert summary["remaining_phase_work"] == remaining_work


def test_recommended_next_slice_is_preserved():
    recommended_next_slice = (
        "Add a deterministic controlled summary consumer while keeping runtime deferred."
    )

    summary = summarize_controlled_evaluation_batch_result(
        _passing_batch(),
        recommended_next_slice=recommended_next_slice,
    )

    assert summary["recommended_next_slice"] == recommended_next_slice


def test_summary_is_safe_for_developer_handoff_when_caveats_are_present():
    summary = summarize_controlled_evaluation_batch_result(_passing_batch())

    assert summary["safe_for_developer_handoff"] is True


def test_summary_is_never_safe_for_final_answer_generation():
    summary = summarize_controlled_evaluation_batch_result(_passing_batch())

    assert summary["safe_for_final_answer_generation"] is False


def test_runtime_deployment_production_exposure_llm_db_corpus_code_evidence_and_cross_repo_claims_are_not_permitted():
    summary = summarize_controlled_evaluation_batch_result(
        _passing_batch(),
        recommended_next_slice="Enable runtime and make the system production ready.",
    )

    assert summary["overall_status"] == "FAIL"
    assert summary["safe_for_developer_handoff"] is False
    assert PROHIBITED_METADATA_CLAIM_FAILURE in summary["safety_failures"]
    assert PROHIBITED_METADATA_CLAIM_FAILURE in summary["drift_failures"]


def test_summary_output_is_deterministic_for_repeated_input():
    batch = _passing_batch()

    first = summarize_controlled_evaluation_batch_result(batch)
    second = summarize_controlled_evaluation_batch_result(batch)

    assert first == second

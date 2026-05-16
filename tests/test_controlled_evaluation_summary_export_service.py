import json
from pathlib import Path

from app.services.controlled_evaluation_batch_harness_service import (
    evaluate_controlled_evaluation_fixture_directory,
    evaluate_controlled_evaluation_fixture_payloads,
)
from app.services.controlled_evaluation_batch_summary_service import (
    summarize_controlled_evaluation_batch_result,
)
from app.services.controlled_evaluation_summary_export_service import (
    CI_CHECK_SUMMARY,
    CONTROLLED_INTERNAL_SUMMARY,
    DEVELOPER_HANDOFF_SUMMARY,
    PHASE_PROGRESS_SUMMARY,
    export_controlled_evaluation_summary,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evaluation_reports"
PROHIBITED_CLAIM_TERMS = (
    "production-ready",
    "deployment-ready",
    "runtime-ready",
    "chat exposure enabled",
    "endpoint exposed",
    "live llm enabled",
    "db access occurred",
    "database access occurred",
    "corpus mutation occurred",
    "code evidence ingestion occurred",
    "workforce-platform runtime integration enabled",
    "analytics runtime integration enabled",
)


def _passing_summary():
    batch = evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR)
    return summarize_controlled_evaluation_batch_result(
        batch,
        current_phase_progress_before_slice="70%",
        expected_phase_progress_after_slice="95%",
    )


def _failed_summary():
    fixture = json.loads(
        (FIXTURE_DIR / "safe_controlled_evaluation_report.json").read_text(
            encoding="utf-8"
        )
    )
    fixture["expected_publication_decision"] = "BLOCKED_OVERSTATED_PRODUCTION"
    batch = evaluate_controlled_evaluation_fixture_payloads([fixture])
    return summarize_controlled_evaluation_batch_result(batch)


def test_passing_batch_summary_exports_as_controlled_internal_summary():
    export = export_controlled_evaluation_summary(_passing_summary())

    assert export["export_type"] == CONTROLLED_INTERNAL_SUMMARY
    assert export["overall_status"] == "PASS"
    assert export["all_passed"] is True


def test_failed_batch_summary_preserves_failure_details():
    export = export_controlled_evaluation_summary(_failed_summary())

    assert export["overall_status"] == "FAIL"
    assert export["failed_fixtures"] == 1
    assert export["drift_failures"] == ("safe_controlled_evaluation_report",)


def test_developer_handoff_export_requires_caveats_and_no_action_boundaries():
    summary = _passing_summary()

    permitted = export_controlled_evaluation_summary(
        summary,
        export_type=DEVELOPER_HANDOFF_SUMMARY,
    )
    blocked = export_controlled_evaluation_summary(
        {**summary, "no_action_attestation": ""},
        export_type=DEVELOPER_HANDOFF_SUMMARY,
        export_caveats=(),
    )

    assert permitted["safe_for_developer_handoff"] is True
    assert blocked["safe_for_developer_handoff"] is False
    assert "DEVELOPER_HANDOFF_BOUNDARY_MISSING" in blocked["safety_failures"]


def test_ci_check_summary_requires_deterministic_controlled_inputs():
    export = export_controlled_evaluation_summary(
        _passing_summary(),
        export_type=CI_CHECK_SUMMARY,
        generated_from_controlled_inputs=False,
    )

    assert export["overall_status"] == "FAIL"
    assert "CI_CHECK_REQUIRES_CONTROLLED_INPUTS" in export["safety_failures"]


def test_phase_progress_before_and_after_percentages_are_preserved():
    export = export_controlled_evaluation_summary(
        _passing_summary(),
        export_type=PHASE_PROGRESS_SUMMARY,
    )

    assert export["progress_before_slice"] == "70%"
    assert export["progress_after_slice"] == "95%"


def test_export_is_never_safe_for_final_answer_generation():
    export = export_controlled_evaluation_summary(_passing_summary())

    assert export["safe_for_final_answer_generation"] is False


def test_no_action_attestation_is_preserved():
    export = export_controlled_evaluation_summary(_passing_summary())

    assert "No runtime" in export["no_action_attestation"]
    assert "final answer generation" in export["no_action_attestation"]


def test_prohibited_capabilities_are_preserved():
    export = export_controlled_evaluation_summary(_passing_summary())

    assert "LIVE_LLM" in export["prohibited_capabilities_preserved"]
    assert "DB_ACCESS" in export["prohibited_capabilities_preserved"]
    assert "FINAL_ANSWER_GENERATION" in export["prohibited_capabilities_preserved"]


def test_runtime_deployment_production_exposure_llm_db_corpus_code_evidence_and_cross_repo_claims_are_not_permitted():
    for claim in PROHIBITED_CLAIM_TERMS:
        summary = summarize_controlled_evaluation_batch_result(
            evaluate_controlled_evaluation_fixture_directory(FIXTURE_DIR),
            recommended_next_slice=f"This export is {claim}.",
        )
        export = export_controlled_evaluation_summary(summary)

        assert export["overall_status"] == "FAIL"
        assert export["safe_for_developer_handoff"] is False


def test_export_output_is_deterministic_for_repeated_input():
    summary = _passing_summary()

    first = export_controlled_evaluation_summary(summary)
    second = export_controlled_evaluation_summary(summary)

    assert first == second


def test_export_service_does_not_write_files_in_this_slice():
    before = {path.name for path in FIXTURE_DIR.iterdir()}

    export_controlled_evaluation_summary(_passing_summary())

    after = {path.name for path in FIXTURE_DIR.iterdir()}
    assert after == before

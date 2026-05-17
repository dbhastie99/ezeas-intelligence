from app.services.controlled_regression_execution_closeout_service import (
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_OVERSTATED_PRODUCTION,
    BLOCKED_OVERSTATED_RUNTIME,
    COMPLETED_COMPONENTS,
    CONTROLLED_REGRESSION_EXECUTION_COMPLETE,
    REMAINING_WORK,
    build_controlled_regression_execution_closeout,
)


def _closeout(**kwargs):
    return build_controlled_regression_execution_closeout(**kwargs)


def test_complete_inputs_produce_controlled_regression_execution_complete():
    closeout = _closeout()

    assert closeout["closeout_status"] == CONTROLLED_REGRESSION_EXECUTION_COMPLETE
    assert closeout["controlled_regression_execution_complete"] is True


def test_progress_before_slice_is_95_percent():
    assert _closeout()["progress_before_slice"] == "95%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_completed_components_include_all_prior_controlled_regression_components():
    components = _closeout()["completed_components"]

    for component in COMPLETED_COMPONENTS:
        assert component in components


def test_remaining_work_is_limited_to_choosing_next_phase():
    assert _closeout()["remaining_work"] == REMAINING_WORK


def test_next_phase_options_are_deterministic_and_explicit():
    first = _closeout()["recommended_next_phase_options"]
    second = _closeout()["recommended_next_phase_options"]

    assert first == second
    assert "Option A: Controlled Evaluation Report Export File Writer." in first
    assert "Option B: Controlled Corpus / Evidence Intake Planning." in first
    assert "Option C: Code Evidence Readiness Planning." in first
    assert "Option D: Keep Minerva paused while award recovery continues." in first


def test_final_answer_generation_is_not_authorised():
    assert _closeout()["final_answer_generation_authorised"] is False


def test_live_llm_is_not_authorised():
    assert _closeout()["live_llm_authorised"] is False


def test_chat_and_endpoint_exposure_are_not_authorised():
    closeout = _closeout()

    assert closeout["chat_exposure_authorised"] is False
    assert closeout["endpoint_exposure_authorised"] is False


def test_db_access_is_not_authorised():
    assert _closeout()["db_access_authorised"] is False


def test_corpus_mutation_is_not_authorised():
    assert _closeout()["corpus_mutation_authorised"] is False


def test_code_evidence_ingestion_is_not_authorised():
    assert _closeout()["code_evidence_ingestion_authorised"] is False


def test_workforce_runtime_integration_is_not_authorised():
    assert _closeout()["workforce_runtime_integration_authorised"] is False


def test_analytics_runtime_integration_is_not_authorised():
    assert _closeout()["analytics_runtime_integration_authorised"] is False


def test_production_deployment_and_runtime_readiness_claims_are_not_permitted():
    closeout = _closeout()

    assert closeout["production_readiness_claim_permitted"] is False
    assert closeout["deployment_readiness_claim_permitted"] is False
    assert closeout["runtime_readiness_claim_permitted"] is False


def test_no_action_attestation_is_preserved():
    attestation = _closeout()["no_action_attestation"]

    assert "No runtime" in attestation
    assert "final answer generation" in attestation
    assert "cross-repo runtime action" in attestation


def test_output_is_deterministic_for_repeated_input():
    assert _closeout() == _closeout()


def test_overstated_runtime_claim_is_blocked_or_marked_review():
    closeout = _closeout(notes="runtime enabled for live use")

    assert closeout["closeout_status"] in {
        BLOCKED_OVERSTATED_RUNTIME,
        "NEEDS_REVIEW",
    }
    assert closeout["closeout_status"] != CONTROLLED_REGRESSION_EXECUTION_COMPLETE


def test_overstated_production_claim_is_blocked_or_marked_review():
    closeout = _closeout(notes="production-ready")

    assert closeout["closeout_status"] in {
        BLOCKED_OVERSTATED_PRODUCTION,
        "NEEDS_REVIEW",
    }
    assert closeout["closeout_status"] != CONTROLLED_REGRESSION_EXECUTION_COMPLETE


def test_exposure_or_final_answer_claim_is_blocked_or_marked_review():
    closeout = _closeout(notes="final answer generation enabled")

    assert closeout["closeout_status"] in {
        BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
        "NEEDS_REVIEW",
    }
    assert closeout["closeout_status"] != CONTROLLED_REGRESSION_EXECUTION_COMPLETE


def test_llm_db_corpus_code_evidence_and_cross_repo_runtime_claims_are_not_complete():
    claims = (
        "live LLM authorised",
        "DB access authorised",
        "corpus mutation authorised",
        "Code Evidence ingestion authorised",
        "workforce-platform runtime integration authorised",
        "analytics runtime integration authorised",
    )

    for claim in claims:
        closeout = _closeout(notes=claim)

        assert closeout["closeout_status"] in {
            BLOCKED_OVERSTATED_RUNTIME,
            "NEEDS_REVIEW",
        }
        assert closeout["closeout_status"] != CONTROLLED_REGRESSION_EXECUTION_COMPLETE

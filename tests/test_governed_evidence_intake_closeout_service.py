from app.services.governed_evidence_intake_closeout_service import (
    BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    COMPLETED_COMPONENTS,
    GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE,
    REMAINING_WORK,
    RUNBOOK_STEPS,
    STOP_CONDITIONS,
    build_governed_evidence_intake_closeout,
)


def _closeout(**kwargs):
    return build_governed_evidence_intake_closeout(**kwargs)


def test_complete_inputs_produce_governed_evidence_intake_phase_complete():
    closeout = _closeout()

    assert closeout["phase_status"] == GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE
    assert closeout["governed_evidence_intake_phase_complete"] is True


def test_progress_before_slice_is_approximately_85_percent():
    assert _closeout()["progress_before_slice"] == "approximately 85%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_completed_components_include_required_governed_intake_components():
    components = _closeout()["completed_components"]

    for component in COMPLETED_COMPONENTS:
        assert component in components
    assert any("taxonomy" in component for component in components)
    assert any("planning gate" in component for component in components)
    assert any("source-status boundary" in component for component in components)
    assert any("Golden intake fixture baselines" in component for component in components)


def test_remaining_work_is_limited_to_choosing_next_phase():
    assert _closeout()["remaining_work"] == REMAINING_WORK


def test_next_phase_options_are_deterministic_and_explicit():
    first = _closeout()["recommended_next_phase_options"]
    second = _closeout()["recommended_next_phase_options"]

    assert first == second
    assert "Option A: Controlled Evidence Intake Dry-Run / No-Corpus-Mutation." in first
    assert "Option B: Controlled External Evidence Summary Catalogue." in first
    assert "Option C: Code Evidence Readiness Planning." in first
    assert "Option D: Keep Minerva paused while award recovery continues." in first


def test_evidence_ingestion_is_not_authorised():
    assert _closeout()["evidence_ingestion_authorised"] is False


def test_corpus_mutation_is_not_authorised():
    assert _closeout()["corpus_mutation_authorised"] is False


def test_code_evidence_ingestion_is_not_authorised():
    assert _closeout()["code_evidence_ingestion_authorised"] is False


def test_db_access_and_writes_are_not_authorised():
    closeout = _closeout()

    assert closeout["db_access_authorised"] is False
    assert closeout["db_writes_authorised"] is False


def test_live_retrieval_is_not_authorised():
    assert _closeout()["live_retrieval_authorised"] is False


def test_live_llm_is_not_authorised():
    assert _closeout()["live_llm_authorised"] is False


def test_final_answer_generation_is_not_authorised():
    assert _closeout()["final_answer_generation_authorised"] is False


def test_chat_and_endpoint_exposure_are_not_authorised():
    closeout = _closeout()

    assert closeout["chat_exposure_authorised"] is False
    assert closeout["endpoint_exposure_authorised"] is False


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

    assert "No evidence ingestion" in attestation
    assert "live LLM call" in attestation
    assert "runtime action" in attestation


def test_runbook_steps_are_deterministic_and_future_authorisation_gated():
    closeout = _closeout()

    assert closeout["runbook_steps"] == RUNBOOK_STEPS
    assert _closeout()["runbook_steps"] == closeout["runbook_steps"]
    assert any("future-ingestion slice" in step for step in closeout["runbook_steps"])


def test_stop_conditions_cover_required_blockers():
    stops = " ".join(_closeout()["stop_conditions"])

    for expected in (
        "unauthorised evidence ingestion",
        "unauthorised corpus mutation",
        "unauthorised Code Evidence ingestion",
        "unauthorised DB access",
        "unauthorised live retrieval",
        "unauthorised live LLM",
        "unauthorised chat or endpoint exposure",
        "runtime integration",
        "production, deployment, or runtime readiness overstatement",
    ):
        assert expected in stops
    assert _closeout()["stop_conditions"] == STOP_CONDITIONS


def test_output_is_deterministic_for_repeated_input():
    assert _closeout() == _closeout()


def test_unauthorised_ingestion_claim_is_blocked_or_marked_review():
    closeout = _closeout(notes="evidence ingestion authorised")

    assert closeout["phase_status"] in {
        BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
        "NEEDS_REVIEW",
    }
    assert closeout["phase_status"] != GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE


def test_corpus_mutation_or_code_evidence_claim_is_blocked_or_marked_review():
    claims = (
        "corpus mutation authorised",
        "Code Evidence ingestion authorised",
    )

    for claim in claims:
        closeout = _closeout(notes=claim)

        assert closeout["phase_status"] in {
            BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM,
            "NEEDS_REVIEW",
        }
        assert closeout["phase_status"] != GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE


def test_runtime_or_production_overstatement_is_blocked_or_marked_review():
    claims = (
        "DB access authorised",
        "live retrieval authorised",
        "live LLM authorised",
        "chat exposure authorised",
        "workforce-platform runtime integration authorised",
        "analytics runtime integration authorised",
        "production-ready",
        "deployment-ready",
        "runtime ready",
    )

    for claim in claims:
        closeout = _closeout(notes=claim)

        assert closeout["phase_status"] in {
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
            "NEEDS_REVIEW",
        }
        assert closeout["phase_status"] != GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE

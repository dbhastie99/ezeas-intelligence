from app.services.controlled_evidence_intake_dry_run_closeout_service import (
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_MUTATION_OR_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    COMPLETED_COMPONENTS,
    CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE,
    REMAINING_WORK,
    build_controlled_evidence_intake_dry_run_closeout,
)


def _closeout(**kwargs):
    return build_controlled_evidence_intake_dry_run_closeout(**kwargs)


def test_complete_inputs_produce_controlled_evidence_intake_dry_run_complete():
    closeout = _closeout()

    assert closeout["phase_status"] == CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE
    assert closeout["controlled_dry_run_phase_complete"] is True


def test_progress_before_slice_is_approximately_90_percent():
    assert _closeout()["progress_before_slice"] == "approximately 90%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_completed_components_include_required_dry_run_components():
    components = _closeout()["completed_components"]

    for component in COMPLETED_COMPONENTS:
        assert component in components
    assert any("dry-run service" in component for component in components)
    assert any("dry-run summary service" in component for component in components)
    assert any("fixture execution service" in component for component in components)
    assert any("review pack service" in component for component in components)
    assert any("golden intake baselines" in component for component in components)
    assert any("taxonomy" in component for component in components)
    assert any("planning gate" in component for component in components)
    assert any("source-status boundary" in component for component in components)


def test_remaining_work_is_limited_to_choosing_next_phase():
    assert _closeout()["remaining_work"] == REMAINING_WORK


def test_next_phase_options_are_deterministic_and_explicit():
    first = _closeout()["recommended_next_phase_options"]
    second = _closeout()["recommended_next_phase_options"]

    assert first == second
    assert (
        "Option A: Controlled Evidence Intake Authorisation Gate / First No-Mutation Intake Candidate."
        in first
    )
    assert "Option B: Controlled External Evidence Summary Catalogue." in first
    assert "Option C: Code Evidence Readiness Planning." in first
    assert "Option D: Keep Minerva paused while award recovery continues." in first


def test_evidence_ingestion_performed_is_false():
    assert _closeout()["evidence_ingestion_performed"] is False


def test_corpus_mutation_performed_is_false():
    assert _closeout()["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_false():
    assert _closeout()["code_evidence_ingestion_performed"] is False


def test_db_access_and_write_performed_are_false():
    closeout = _closeout()

    assert closeout["db_access_performed"] is False
    assert closeout["db_write_performed"] is False


def test_live_retrieval_performed_is_false():
    assert _closeout()["live_retrieval_performed"] is False


def test_live_llm_performed_is_false():
    assert _closeout()["live_llm_performed"] is False


def test_final_answer_generation_performed_is_false():
    assert _closeout()["final_answer_generation_performed"] is False


def test_chat_and_endpoint_exposure_authorised_are_false():
    closeout = _closeout()

    assert closeout["chat_exposure_authorised"] is False
    assert closeout["endpoint_exposure_authorised"] is False


def test_workforce_runtime_integration_authorised_is_false():
    assert _closeout()["workforce_runtime_integration_authorised"] is False


def test_analytics_runtime_integration_authorised_is_false():
    assert _closeout()["analytics_runtime_integration_authorised"] is False


def test_production_deployment_and_runtime_claims_are_not_permitted():
    closeout = _closeout()

    assert closeout["production_readiness_claim_permitted"] is False
    assert closeout["deployment_readiness_claim_permitted"] is False
    assert closeout["runtime_readiness_claim_permitted"] is False


def test_no_mutation_ledger_lists_prohibited_actions_and_false_state():
    ledger = _closeout()["no_mutation_ledger"]
    by_action = {item["action"]: item for item in ledger}

    for action in (
        "evidence_ingestion",
        "corpus_mutation",
        "code_evidence_ingestion",
        "db_access",
        "db_write",
        "live_retrieval",
        "live_llm",
        "final_answer_generation",
        "chat_exposure",
        "endpoint_exposure",
        "workforce_runtime_integration",
        "analytics_runtime_integration",
        "production_readiness_claim",
        "deployment_readiness_claim",
        "runtime_readiness_claim",
    ):
        assert action in by_action
        assert by_action[action]["authorised"] is False
        assert by_action[action]["state"] == "false"


def test_no_action_attestation_is_preserved():
    attestation = _closeout()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM use" in attestation


def test_output_is_deterministic_for_repeated_input():
    assert _closeout() == _closeout()


def test_ingestion_or_corpus_mutation_claim_is_blocked_or_marked_review():
    claims = (
        "evidence ingestion performed",
        "corpus mutation performed",
    )

    for claim in claims:
        closeout = _closeout(notes=claim)

        assert closeout["phase_status"] in {
            BLOCKED_MUTATION_OR_INGESTION_CLAIM,
            "NEEDS_REVIEW",
        }
        assert closeout["phase_status"] != CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE


def test_code_evidence_db_write_live_retrieval_or_llm_claim_is_blocked_or_review():
    claims = (
        ("Code Evidence ingestion performed", BLOCKED_MUTATION_OR_INGESTION_CLAIM),
        ("DB write authorised", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("live retrieval performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("live LLM performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
    )

    for claim, expected_status in claims:
        closeout = _closeout(notes=claim)

        assert closeout["phase_status"] in {expected_status, "NEEDS_REVIEW"}
        assert closeout["phase_status"] != CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE


def test_exposure_final_answer_runtime_or_production_claim_is_blocked_or_review():
    claims = (
        ("chat exposure authorised", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
        ("endpoint exposure authorised", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
        ("final answer generation performed", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
        (
            "workforce-platform runtime integration authorised",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            "analytics runtime integration authorised",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        ("production-ready", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("deployment-ready", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("runtime ready", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
    )

    for claim, expected_status in claims:
        closeout = _closeout(notes=claim)

        assert closeout["phase_status"] in {expected_status, "NEEDS_REVIEW"}
        assert closeout["phase_status"] != CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE

from app.services.controlled_durable_evidence_intake_authorisation_gate_service import (
    build_controlled_durable_evidence_intake_authorisation_gate,
)
from app.services.controlled_durable_intake_authorisation_phase_closeout_service import (
    BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM,
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE,
    build_controlled_durable_intake_authorisation_phase_closeout,
)
from app.services.controlled_durable_intake_candidate_eligibility_service import (
    build_controlled_durable_intake_candidate_eligibility,
)
from app.services.controlled_durable_intake_execution_review_pack_service import (
    build_controlled_durable_intake_execution_review_pack,
)
from app.services.controlled_durable_intake_first_candidate_execution_design_service import (
    build_controlled_durable_intake_first_candidate_execution_design,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


def _candidate():
    return {
        "candidate_id": "durable-candidate-001",
        "candidate_type": "DEVELOPER_LOG",
        "source_reference": "docs/evaluation/source.md",
        "source_status_boundary": "CONTROLLED_READINESS_ONLY",
        "evidence_envelope": True,
        "audit_envelope": True,
        "reviewer_confirmation": True,
        "rollback_policy": "remove candidate and derived references before ingestion",
        "sensitive_data_review": True,
    }


def _review_pack(**overrides):
    candidate = _candidate()
    gate = build_controlled_durable_evidence_intake_authorisation_gate(candidate)
    eligibility = build_controlled_durable_intake_candidate_eligibility(candidate)
    design = build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        eligibility,
    )
    review_pack = build_controlled_durable_intake_execution_review_pack(design)
    review_pack.update(overrides)
    return review_pack


def _closeout(**overrides):
    return build_controlled_durable_intake_authorisation_phase_closeout(
        _review_pack(**overrides)
    )


def test_complete_inputs_produce_phase_complete():
    result = _closeout()

    assert result["phase_status"] == DURABLE_INTAKE_AUTHORISATION_PHASE_COMPLETE
    assert result["durable_intake_authorisation_phase_complete"] is True


def test_progress_before_and_after_are_recorded():
    result = _closeout()

    assert result["progress_before_slice"] == "approximately 85-90%"
    assert result["progress_after_slice"] == "100%"


def test_completed_components_include_required_phase_components():
    result = _closeout()

    for component in (
        "durable evidence intake authorisation gate",
        "durable intake candidate eligibility",
        "first-candidate execution design",
        "execution review pack",
    ):
        assert component in result["completed_components"]


def test_remaining_work_is_limited_to_choosing_next_phase():
    result = _closeout()

    assert result["remaining_work"] == ("choose_next_phase",)
    assert "choose the next" in result["next_decision_point"]


def test_next_phase_options_are_deterministic_and_explicit():
    first = _closeout()
    second = _closeout()

    assert first["recommended_next_phase_options"] == second[
        "recommended_next_phase_options"
    ]
    assert first["recommended_next_phase_options"] == (
        "Option A: Controlled Durable Intake Execution / Review-Only First Candidate",
        "Option B: External Evidence Summary Catalogue",
        "Option C: Code Evidence Readiness Planning",
        "Option D: Pause Minerva While Demo Stabilisation Continues",
    )


def test_durable_ingestion_corpus_mutation_and_code_evidence_are_false():
    result = _closeout()

    assert result["durable_ingestion_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False


def test_db_live_retrieval_llm_and_final_answer_are_false():
    result = _closeout()

    assert result["db_access_performed"] is False
    assert result["db_write_performed"] is False
    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False
    assert result["final_answer_generation_performed"] is False


def test_exposure_and_runtime_integrations_are_false():
    result = _closeout()

    assert result["chat_exposure_authorised"] is False
    assert result["endpoint_exposure_authorised"] is False
    assert result["workforce_runtime_integration_authorised"] is False
    assert result["analytics_runtime_integration_authorised"] is False


def test_readiness_claims_are_not_permitted():
    result = _closeout()

    assert result["production_readiness_claim_permitted"] is False
    assert result["deployment_readiness_claim_permitted"] is False
    assert result["runtime_readiness_claim_permitted"] is False


def test_attestations_are_preserved_from_input_when_present():
    result = _closeout(
        no_ingestion_attestation="custom no ingestion",
        no_mutation_attestation="custom no mutation",
        no_action_attestation="custom no action",
    )

    assert result["no_ingestion_attestation"] == "custom no ingestion"
    assert result["no_mutation_attestation"] == "custom no mutation"
    assert result["no_action_attestation"] == "custom no action"


def test_default_no_action_attestation_is_preserved():
    result = _closeout()

    assert result["no_action_attestation"] == NO_ACTION_ATTESTATION


def test_output_is_deterministic_for_repeated_input():
    review_pack = _review_pack()

    assert build_controlled_durable_intake_authorisation_phase_closeout(
        review_pack
    ) == build_controlled_durable_intake_authorisation_phase_closeout(review_pack)


def test_durable_ingestion_corpus_mutation_or_code_evidence_claim_is_blocked():
    for claim in (
        "durable_ingestion_performed",
        "corpus_mutation_performed",
        "code_evidence_ingestion_performed",
    ):
        result = _closeout(**{claim: True})

        assert (
            result["phase_status"]
            == BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM
        )


def test_db_live_retrieval_llm_or_final_answer_claim_is_blocked_or_review():
    for claim, expected in (
        ("db_access_performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("db_write_performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("live_retrieval_performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("live_llm_performed", BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        ("final_answer_generation_performed", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
    ):
        result = _closeout(**{claim: True})

        assert result["phase_status"] == expected


def test_exposure_runtime_or_production_claim_is_blocked_or_review():
    for claim, expected in (
        ("chat_exposure_authorised", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
        ("endpoint_exposure_authorised", BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM),
        (
            "workforce_runtime_integration_authorised",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            "analytics_runtime_integration_authorised",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            "production_readiness_claim_permitted",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            "deployment_readiness_claim_permitted",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            "runtime_readiness_claim_permitted",
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
    ):
        result = _closeout(**{claim: True})

        assert result["phase_status"] == expected

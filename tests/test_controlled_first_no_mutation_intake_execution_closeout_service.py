from app.services.controlled_evidence_intake_authorisation_gate_service import (
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    build_controlled_evidence_intake_first_candidate_review,
)
from app.services.controlled_evidence_intake_first_candidate_service import (
    build_controlled_evidence_intake_first_candidate,
)
from app.services.controlled_first_no_mutation_intake_execution_closeout_service import (
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE,
    build_controlled_first_no_mutation_intake_execution_closeout,
)
from app.services.controlled_first_no_mutation_intake_execution_review_service import (
    build_controlled_first_no_mutation_intake_execution_review,
)
from app.services.controlled_first_no_mutation_intake_execution_service import (
    build_controlled_first_no_mutation_intake_execution,
)
from app.services.controlled_no_mutation_intake_evidence_envelope_service import (
    build_controlled_no_mutation_intake_evidence_envelope,
)
from app.services.controlled_no_mutation_intake_verification_pack_service import (
    build_controlled_no_mutation_intake_verification_pack,
)


def _candidate():
    return {
        "candidate_id": "analytics",
        "candidate_type": "ANALYTICS_READINESS_SUMMARY",
        "source_repo": "ezeas-intelligence",
        "source_phase": "controlled evidence intake dry-run closeout",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Future no-mutation intake only.",),
    }


def _verification_pack(**overrides):
    selection = build_controlled_evidence_intake_first_candidate((_candidate(),))
    authorisation = build_controlled_evidence_intake_authorisation_gate(_candidate())
    candidate_review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    execution = build_controlled_first_no_mutation_intake_execution(candidate_review)
    envelope = build_controlled_no_mutation_intake_evidence_envelope(execution)
    review = build_controlled_first_no_mutation_intake_execution_review(
        execution,
        envelope,
    )
    pack = build_controlled_no_mutation_intake_verification_pack(review)
    pack.update(overrides)
    return pack


def _closeout(pack=None):
    return build_controlled_first_no_mutation_intake_execution_closeout(
        _verification_pack() if pack is None else pack
    )


def test_complete_inputs_produce_phase_complete():
    result = _closeout()

    assert result["phase_status"] == FIRST_NO_MUTATION_INTAKE_EXECUTION_PHASE_COMPLETE
    assert result["first_no_mutation_intake_execution_phase_complete"] is True


def test_progress_before_slice_is_approximately_90_percent():
    assert _closeout()["progress_before_slice"] == "approximately 90%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_completed_components_include_required_services():
    components = _closeout()["completed_components"]

    assert "controlled_first_no_mutation_intake_execution_service" in components
    assert "controlled_no_mutation_intake_evidence_envelope_service" in components
    assert "controlled_first_no_mutation_intake_execution_review_service" in components
    assert "controlled_no_mutation_intake_verification_pack_service" in components


def test_remaining_work_is_limited_to_choosing_next_phase():
    assert _closeout()["remaining_work"] == ("choose_next_phase",)


def test_next_phase_options_are_deterministic_and_explicit():
    options = _closeout()["recommended_next_phase_options"]

    assert options == _closeout()["recommended_next_phase_options"]
    assert options == (
        "Option A: Controlled Durable Evidence Intake Design",
        "Option B: External Evidence Summary Catalogue",
        "Option C: Code Evidence Readiness Planning",
        "Option D: Pause Minerva While Award Recovery Continues",
    )


def test_durable_ingestion_performed_is_false():
    assert _closeout()["durable_ingestion_performed"] is False


def test_corpus_mutation_performed_is_false():
    assert _closeout()["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_false():
    assert _closeout()["code_evidence_ingestion_performed"] is False


def test_db_access_and_write_performed_are_false():
    result = _closeout()

    assert result["db_access_performed"] is False
    assert result["db_write_performed"] is False


def test_live_retrieval_performed_is_false():
    assert _closeout()["live_retrieval_performed"] is False


def test_live_llm_performed_is_false():
    assert _closeout()["live_llm_performed"] is False


def test_final_answer_generation_performed_is_false():
    assert _closeout()["final_answer_generation_performed"] is False


def test_chat_and_endpoint_exposure_authorised_are_false():
    result = _closeout()

    assert result["chat_exposure_authorised"] is False
    assert result["endpoint_exposure_authorised"] is False


def test_workforce_runtime_integration_authorised_is_false():
    assert _closeout()["workforce_runtime_integration_authorised"] is False


def test_analytics_runtime_integration_authorised_is_false():
    assert _closeout()["analytics_runtime_integration_authorised"] is False


def test_production_deployment_runtime_readiness_claims_are_not_permitted():
    result = _closeout()

    assert result["production_readiness_claim_permitted"] is False
    assert result["deployment_readiness_claim_permitted"] is False
    assert result["runtime_readiness_claim_permitted"] is False


def test_no_mutation_attestation_is_preserved():
    attestation = _closeout()["no_mutation_attestation"]

    assert "controlled-readiness/no-mutation level only" in attestation
    assert "no durable ingestion" in attestation


def test_no_action_attestation_is_preserved():
    attestation = _closeout()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    pack = _verification_pack()

    assert _closeout(pack) == _closeout(pack)


def test_durable_ingestion_corpus_mutation_or_code_evidence_claim_is_blocked():
    cases = (
        _verification_pack(durable_ingestion_performed=True),
        _verification_pack(corpus_mutation_performed=True),
        _verification_pack(code_evidence_ingestion_performed=True),
    )

    for pack in cases:
        result = _closeout(pack)
        assert result["phase_status"] == BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
        assert result["first_no_mutation_intake_execution_phase_complete"] is False


def test_db_live_retrieval_llm_or_final_answer_claim_is_blocked():
    runtime_cases = (
        _verification_pack(db_access_performed=True),
        _verification_pack(db_write_performed=True),
        _verification_pack(live_retrieval_performed=True),
        _verification_pack(live_llm_performed=True),
    )

    for pack in runtime_cases:
        assert _closeout(pack)["phase_status"] == (
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
        )

    final_answer = _verification_pack(final_answer_generation_performed=True)
    assert _closeout(final_answer)["phase_status"] == (
        BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    )


def test_exposure_runtime_or_production_claim_is_blocked():
    exposure_cases = (
        _verification_pack(chat_exposure_authorised=True),
        _verification_pack(endpoint_exposure_authorised=True),
    )
    runtime_cases = (
        _verification_pack(workforce_runtime_integration_authorised=True),
        _verification_pack(analytics_runtime_integration_authorised=True),
        _verification_pack(production_readiness_claim_permitted=True),
        _verification_pack(deployment_readiness_claim_permitted=True),
        _verification_pack(runtime_readiness_claim_permitted=True),
    )

    for pack in exposure_cases:
        assert _closeout(pack)["phase_status"] == (
            BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
        )

    for pack in runtime_cases:
        assert _closeout(pack)["phase_status"] == (
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
        )

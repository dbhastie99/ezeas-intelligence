from app.services.controlled_durable_evidence_intake_closeout_readiness_service import (
    build_controlled_durable_evidence_intake_closeout_readiness,
)
from app.services.controlled_durable_evidence_intake_design_service import (
    build_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_evidence_intake_design_verification_service import (
    verify_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_evidence_intake_phase_closeout_service import (
    BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM,
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_PHASE_COMPLETE,
    build_controlled_durable_evidence_intake_phase_closeout,
)
from app.services.controlled_durable_intake_audit_envelope_service import (
    build_controlled_durable_intake_audit_envelope,
)
from app.services.controlled_durable_intake_authorisation_requirements_service import (
    build_controlled_durable_intake_authorisation_requirements,
)


def _design():
    return build_controlled_durable_evidence_intake_design(
        {
            "storage_boundary_model": "review-only source metadata; no corpus writes",
            "mutation_boundary_model": "future explicit gate required before mutation",
            "review_boundary_model": "reviewer confirmation required before action",
            "rollback_or_removal_policy": "rollback/removal policy must be approved",
        }
    )


def _requirements():
    return build_controlled_durable_intake_authorisation_requirements(
        {
            "reviewer_confirmation": True,
            "source_status_boundary": True,
            "evidence_envelope": True,
            "no_overstatement_check": True,
            "rollback_policy": True,
            "audit_metadata": True,
            "dry_run_review": True,
        }
    )


def _audit():
    return build_controlled_durable_intake_audit_envelope(
        {
            "source_reference": "controlled-no-mutation-envelope",
            "source_status": "CONTROLLED_READINESS_ONLY",
            "reviewer": "reviewer-id",
            "decision_timestamp": "2026-05-17T00:00:00Z",
            "no_mutation_history": "first no-mutation intake execution complete",
            "rollback_policy": "approved rollback/removal policy required",
            "prohibited_claims_checked": True,
            "sensitive_data_review": True,
        }
    )


def _verified_metadata():
    return verify_controlled_durable_evidence_intake_design(
        _design(),
        _requirements(),
        _audit(),
    )


def _readiness(**overrides):
    metadata = build_controlled_durable_evidence_intake_closeout_readiness(
        _verified_metadata()
    )
    metadata.update(overrides)
    return metadata


def _closeout(metadata=None):
    return build_controlled_durable_evidence_intake_phase_closeout(
        _readiness() if metadata is None else metadata
    )


def test_complete_inputs_produce_durable_evidence_intake_design_phase_complete():
    result = _closeout()

    assert result["phase_status"] == DURABLE_EVIDENCE_INTAKE_DESIGN_PHASE_COMPLETE
    assert result["durable_evidence_intake_design_phase_complete"] is True


def test_progress_before_slice_is_approximately_85_to_90_percent():
    assert _closeout()["progress_before_slice"] == "approximately 85-90%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_completed_components_include_required_services():
    components = _closeout()["completed_components"]

    assert "controlled_durable_evidence_intake_design_service" in components
    assert "controlled_durable_intake_authorisation_requirements_service" in components
    assert "controlled_durable_intake_audit_envelope_service" in components
    assert "controlled_durable_evidence_intake_design_verification_service" in components
    assert "controlled_durable_evidence_intake_closeout_readiness_service" in components


def test_remaining_work_is_limited_to_choosing_next_phase():
    assert _closeout()["remaining_work"] == ("choose_next_phase",)


def test_next_phase_options_are_deterministic_and_explicit():
    options = _closeout()["recommended_next_phase_options"]

    assert options == _closeout()["recommended_next_phase_options"]
    assert options == (
        "Option A: Controlled Durable Evidence Intake Authorisation Gate",
        "Option B: External Evidence Summary Catalogue",
        "Option C: Code Evidence Readiness Planning",
        "Option D: Pause Minerva While Demo Stabilisation Continues",
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


def test_no_ingestion_attestation_is_preserved():
    attestation = _closeout()["no_ingestion_attestation"]

    assert "no durable evidence ingestion" in attestation
    assert "design/readiness level only" in attestation


def test_no_mutation_attestation_is_preserved():
    attestation = _closeout()["no_mutation_attestation"]

    assert "no corpus mutation" in attestation
    assert "Code Evidence ingestion" in attestation


def test_no_action_attestation_is_preserved():
    attestation = _closeout()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    metadata = _readiness()

    assert _closeout(metadata) == _closeout(metadata)


def test_durable_ingestion_corpus_mutation_or_code_evidence_claim_is_blocked():
    cases = (
        _readiness(durable_ingestion_performed=True),
        _readiness(corpus_mutation_performed=True),
        _readiness(code_evidence_ingestion_performed=True),
    )

    for metadata in cases:
        result = _closeout(metadata)
        assert result["phase_status"] == BLOCKED_DURABLE_INGESTION_OR_MUTATION_CLAIM
        assert result["durable_evidence_intake_design_phase_complete"] is False


def test_db_live_retrieval_llm_or_final_answer_claim_is_blocked():
    runtime_cases = (
        _readiness(db_access_performed=True),
        _readiness(db_write_performed=True),
        _readiness(live_retrieval_performed=True),
        _readiness(live_llm_performed=True),
    )

    for metadata in runtime_cases:
        assert _closeout(metadata)["phase_status"] == (
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
        )

    final_answer = _readiness(final_answer_generation_performed=True)
    assert _closeout(final_answer)["phase_status"] == (
        BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    )


def test_exposure_runtime_or_production_claim_is_blocked():
    exposure_cases = (
        _readiness(chat_exposure_authorised=True),
        _readiness(endpoint_exposure_authorised=True),
    )
    runtime_cases = (
        _readiness(workforce_runtime_integration_authorised=True),
        _readiness(analytics_runtime_integration_authorised=True),
        _readiness(production_readiness_claim_permitted=True),
        _readiness(deployment_readiness_claim_permitted=True),
        _readiness(runtime_readiness_claim_permitted=True),
    )

    for metadata in exposure_cases:
        assert _closeout(metadata)["phase_status"] == (
            BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
        )

    for metadata in runtime_cases:
        assert _closeout(metadata)["phase_status"] == (
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
        )

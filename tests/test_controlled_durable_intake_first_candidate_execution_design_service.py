from app.services.controlled_durable_evidence_intake_authorisation_gate_service import (
    build_controlled_durable_evidence_intake_authorisation_gate,
)
from app.services.controlled_durable_intake_candidate_eligibility_service import (
    build_controlled_durable_intake_candidate_eligibility,
)
from app.services.controlled_durable_intake_first_candidate_execution_design_service import (
    BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM,
    BLOCKED_MUTATION_OR_DB_WRITE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_INTAKE_EXECUTION_DESIGN_READY,
    NEEDS_AUTHORISATION_GATE,
    NEEDS_CANDIDATE_ELIGIBILITY,
    build_controlled_durable_intake_first_candidate_execution_design,
)


def _candidate(**overrides):
    metadata = {
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
    metadata.update(overrides)
    return metadata


def _design(**overrides):
    candidate = _candidate(**overrides)
    gate = build_controlled_durable_evidence_intake_authorisation_gate(candidate)
    eligibility = build_controlled_durable_intake_candidate_eligibility(candidate)
    return build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        eligibility,
    )


def test_complete_authorisation_and_eligibility_metadata_produces_design_ready():
    result = _design()

    assert result["design_status"] == DURABLE_INTAKE_EXECUTION_DESIGN_READY


def test_candidate_authorised_for_future_execution_can_be_true():
    result = _design()

    assert result["candidate_authorised_for_future_execution"] is True


def test_no_action_boundary_fields_are_false():
    result = _design()

    assert result["durable_intake_execution_authorised_now"] is False
    assert result["durable_intake_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["db_write_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False
    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False
    assert result["final_answer_generation_performed"] is False


def test_required_execution_steps_are_deterministic():
    result = _design()

    assert result["required_execution_steps"] == _design()["required_execution_steps"]
    assert result["required_execution_steps"] == (
        "confirm_explicit_execution_authorisation",
        "lock_first_candidate_source_reference",
        "verify_source_status_boundary",
        "prepare_evidence_record_envelope",
        "prepare_audit_envelope",
        "confirm_sensitive_data_review",
        "execute_single_candidate_durable_intake_only_in_later_slice",
        "record_rollback_or_removal_evidence",
        "complete_reviewer_closeout",
    )


def test_required_pre_execution_checks_include_required_controls():
    result = _design()

    for item in (
        "reviewer_approval",
        "source_reference",
        "source_status_boundary",
        "evidence_envelope",
        "audit_envelope",
        "rollback_removal_policy",
        "sensitive_data_review",
        "no_overstatement_check",
        "explicit_execution_authorisation",
    ):
        assert item in result["required_pre_execution_checks"]


def test_required_post_execution_checks_include_required_controls():
    result = _design()

    for item in (
        "evidence_record_verification",
        "corpus_mutation_verification",
        "rollback_removal_evidence",
        "sensitive_data_confirmation",
        "reviewer_closeout",
    ):
        assert item in result["required_post_execution_checks"]


def test_missing_authorisation_gate_requires_authorisation_gate():
    eligibility = build_controlled_durable_intake_candidate_eligibility(_candidate())

    result = build_controlled_durable_intake_first_candidate_execution_design(
        None,
        eligibility,
    )

    assert result["design_status"] == NEEDS_AUTHORISATION_GATE


def test_missing_candidate_eligibility_requires_candidate_eligibility():
    gate = build_controlled_durable_evidence_intake_authorisation_gate(_candidate())

    result = build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        None,
    )

    assert result["design_status"] == NEEDS_CANDIDATE_ELIGIBILITY


def test_durable_intake_already_performed_claim_is_blocked():
    result = _design(durable_intake_performed=True)

    assert result["design_status"] == BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    assert result["durable_intake_performed"] is False


def test_mutation_or_db_write_claim_is_blocked():
    for claim_key in ("corpus_mutation_performed", "db_write_performed"):
        result = _design(**{claim_key: True})

        assert result["design_status"] == BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
        assert result[claim_key] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _design(production_readiness_claim_permitted=True)

    assert result["design_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["durable_intake_execution_authorised_now"] is False


def test_output_is_deterministic():
    candidate = _candidate()
    gate = build_controlled_durable_evidence_intake_authorisation_gate(candidate)
    eligibility = build_controlled_durable_intake_candidate_eligibility(candidate)

    assert build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        eligibility,
    ) == build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        eligibility,
    )

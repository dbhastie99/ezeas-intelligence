from app.services.controlled_durable_evidence_intake_authorisation_gate_service import (
    AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION,
    BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM,
    BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM,
    BLOCKED_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_MUTATION_OR_DB_WRITE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    NEEDS_AUDIT_ENVELOPE,
    NEEDS_EVIDENCE_ENVELOPE,
    NEEDS_REVIEWER_CONFIRMATION,
    NEEDS_ROLLBACK_POLICY,
    NEEDS_SENSITIVE_DATA_REVIEW,
    NEEDS_SOURCE_REFERENCE,
    NEEDS_SOURCE_STATUS_BOUNDARY,
    build_controlled_durable_evidence_intake_authorisation_gate,
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


def _gate(**overrides):
    return build_controlled_durable_evidence_intake_authorisation_gate(
        _candidate(**overrides)
    )


def test_complete_candidate_and_prerequisites_authorise_future_execution():
    result = _gate()

    assert (
        result["authorisation_status"]
        == AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION
    )
    assert result["eligible_for_future_durable_intake_execution"] is True


def test_future_execution_authorisation_does_not_authorise_intake_now():
    result = _gate()

    assert result["eligible_for_future_durable_intake_execution"] is True
    assert result["durable_intake_authorised_now"] is False


def test_no_action_boundary_fields_are_false():
    result = _gate()

    assert result["durable_intake_authorised_now"] is False
    assert result["durable_intake_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["db_write_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False
    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False
    assert result["final_answer_generation_performed"] is False
    assert result["chat_exposure_authorised"] is False
    assert result["runtime_integration_authorised"] is False


def test_missing_source_reference_requires_source_reference():
    result = _gate(source_reference="")

    assert result["authorisation_status"] == NEEDS_SOURCE_REFERENCE
    assert "source_reference" in result["missing_prerequisites"]


def test_missing_source_status_boundary_requires_source_status_boundary():
    result = _gate(source_status_boundary="")

    assert result["authorisation_status"] == NEEDS_SOURCE_STATUS_BOUNDARY
    assert "source_status_boundary" in result["missing_prerequisites"]


def test_missing_evidence_envelope_requires_evidence_envelope():
    result = _gate(evidence_envelope=False)

    assert result["authorisation_status"] == NEEDS_EVIDENCE_ENVELOPE
    assert "evidence_envelope" in result["missing_prerequisites"]


def test_missing_audit_envelope_requires_audit_envelope():
    result = _gate(audit_envelope=False)

    assert result["authorisation_status"] == NEEDS_AUDIT_ENVELOPE
    assert "audit_envelope" in result["missing_prerequisites"]


def test_missing_reviewer_confirmation_requires_reviewer_confirmation():
    result = _gate(reviewer_confirmation=False)

    assert result["authorisation_status"] == NEEDS_REVIEWER_CONFIRMATION
    assert "reviewer_confirmation" in result["missing_prerequisites"]


def test_missing_rollback_policy_requires_rollback_policy():
    result = _gate(rollback_policy="")

    assert result["authorisation_status"] == NEEDS_ROLLBACK_POLICY
    assert "rollback_policy" in result["missing_prerequisites"]


def test_missing_sensitive_data_review_requires_sensitive_data_review():
    result = _gate(sensitive_data_review=False)

    assert result["authorisation_status"] == NEEDS_SENSITIVE_DATA_REVIEW
    assert "sensitive_data_review" in result["missing_prerequisites"]


def test_durable_intake_already_performed_claim_is_blocked():
    result = _gate(durable_intake_performed=True)

    assert (
        result["authorisation_status"]
        == BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    )
    assert "durable_intake_already_performed_claim" in result["blocked_reasons"]
    assert result["durable_intake_performed"] is False


def test_corpus_mutation_or_db_write_claim_is_blocked():
    for claim_key in ("corpus_mutation_performed", "db_write_performed"):
        result = _gate(**{claim_key: True})

        assert result["authorisation_status"] == BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
        assert "mutation_or_db_write_claim" in result["blocked_reasons"]
        assert result[claim_key] is False


def test_code_evidence_ingestion_claim_is_blocked():
    result = _gate(code_evidence_ingestion_performed=True)

    assert result["authorisation_status"] == BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM
    assert "code_evidence_ingestion_claim" in result["blocked_reasons"]
    assert result["code_evidence_ingestion_performed"] is False


def test_live_retrieval_llm_or_final_answer_claim_is_blocked():
    for claim_key in (
        "live_retrieval_performed",
        "live_llm_performed",
        "final_answer_generation_performed",
    ):
        result = _gate(**{claim_key: True})

        assert (
            result["authorisation_status"]
            == BLOCKED_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM
        )
        assert "live_retrieval_llm_or_final_answer_claim" in result["blocked_reasons"]
        assert result[claim_key] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _gate(production_readiness_claim_permitted=True)

    assert result["authorisation_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]
    assert result["runtime_integration_authorised"] is False


def test_output_is_deterministic():
    metadata = _candidate()

    assert build_controlled_durable_evidence_intake_authorisation_gate(
        metadata
    ) == build_controlled_durable_evidence_intake_authorisation_gate(metadata)

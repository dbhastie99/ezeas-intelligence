from app.services.controlled_durable_intake_candidate_eligibility_service import (
    BLOCKED_PROHIBITED_CLAIMS,
    DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE,
    NEEDS_AUDIT_ENVELOPE,
    NEEDS_EVIDENCE_ENVELOPE,
    NEEDS_REVIEWER_CONFIRMATION,
    NEEDS_ROLLBACK_POLICY,
    NEEDS_SENSITIVE_DATA_REVIEW,
    NEEDS_SOURCE_REFERENCE,
    NEEDS_SOURCE_STATUS_BOUNDARY,
    UNKNOWN_REQUIRES_REVIEW,
    build_controlled_durable_intake_candidate_eligibility,
)


def _metadata(**overrides):
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


def _eligibility(**overrides):
    return build_controlled_durable_intake_candidate_eligibility(_metadata(**overrides))


def test_complete_candidate_metadata_produces_eligible_for_gate():
    result = _eligibility()

    assert result["eligibility_status"] == DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE
    assert result["eligible_for_authorisation_gate"] is True


def test_unknown_candidate_type_requires_review():
    result = _eligibility(candidate_type="UNKNOWN_TYPE")

    assert result["eligibility_status"] == UNKNOWN_REQUIRES_REVIEW
    assert result["eligible_for_authorisation_gate"] is False


def test_missing_source_reference_blocks_eligibility():
    result = _eligibility(source_reference="")

    assert result["eligibility_status"] == NEEDS_SOURCE_REFERENCE
    assert "source_reference" in result["missing_prerequisites"]


def test_missing_source_status_boundary_blocks_eligibility():
    result = _eligibility(source_status_boundary="")

    assert result["eligibility_status"] == NEEDS_SOURCE_STATUS_BOUNDARY
    assert "source_status_boundary" in result["missing_prerequisites"]


def test_missing_evidence_envelope_blocks_eligibility():
    result = _eligibility(evidence_envelope=False)

    assert result["eligibility_status"] == NEEDS_EVIDENCE_ENVELOPE
    assert "evidence_envelope" in result["missing_prerequisites"]


def test_missing_audit_envelope_blocks_eligibility():
    result = _eligibility(audit_envelope=False)

    assert result["eligibility_status"] == NEEDS_AUDIT_ENVELOPE
    assert "audit_envelope" in result["missing_prerequisites"]


def test_missing_reviewer_confirmation_blocks_eligibility():
    result = _eligibility(reviewer_confirmation=False)

    assert result["eligibility_status"] == NEEDS_REVIEWER_CONFIRMATION
    assert "reviewer_confirmation" in result["missing_prerequisites"]


def test_missing_rollback_policy_blocks_eligibility():
    result = _eligibility(rollback_policy="")

    assert result["eligibility_status"] == NEEDS_ROLLBACK_POLICY
    assert "rollback_policy" in result["missing_prerequisites"]


def test_missing_sensitive_data_review_blocks_eligibility():
    result = _eligibility(sensitive_data_review=False)

    assert result["eligibility_status"] == NEEDS_SENSITIVE_DATA_REVIEW
    assert "sensitive_data_review" in result["missing_prerequisites"]


def test_prohibited_runtime_production_mutation_claims_block_eligibility():
    for claim_key in (
        "runtime_readiness_claim_permitted",
        "production_readiness_claim_permitted",
        "corpus_mutation_performed",
        "db_write_performed",
    ):
        result = _eligibility(**{claim_key: True})

        assert result["eligibility_status"] == BLOCKED_PROHIBITED_CLAIMS
        assert result["prohibited_claims_present"] is True


def test_no_action_attestation_is_preserved():
    attestation = _eligibility()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic():
    metadata = _metadata()

    assert build_controlled_durable_intake_candidate_eligibility(
        metadata
    ) == build_controlled_durable_intake_candidate_eligibility(metadata)

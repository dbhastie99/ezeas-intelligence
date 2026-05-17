from app.services.controlled_durable_intake_audit_envelope_service import (
    AUDIT_ENVELOPE_INCOMPLETE,
    DURABLE_INTAKE_AUDIT_ENVELOPE_READY,
    build_controlled_durable_intake_audit_envelope,
)


def _metadata(**overrides):
    metadata = {
        "source_reference": "controlled-no-mutation-envelope",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "reviewer": "reviewer-id",
        "decision_timestamp": "2026-05-17T00:00:00Z",
        "no_mutation_history": "first no-mutation intake execution complete",
        "rollback_policy": "approved rollback/removal policy required",
        "prohibited_claims_checked": True,
        "sensitive_data_review": True,
    }
    metadata.update(overrides)
    return metadata


def _audit(metadata=None):
    return build_controlled_durable_intake_audit_envelope(
        _metadata() if metadata is None else metadata
    )


def test_complete_audit_metadata_produces_ready_status():
    assert _audit()["audit_status"] == DURABLE_INTAKE_AUDIT_ENVELOPE_READY


def test_missing_source_reference_is_incomplete():
    result = _audit(_metadata(source_reference=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "source_reference" in result["missing_audit_fields"]


def test_missing_source_status_is_incomplete():
    result = _audit(_metadata(source_status=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "source_status" in result["missing_audit_fields"]


def test_missing_reviewer_is_incomplete():
    result = _audit(_metadata(reviewer=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "reviewer" in result["missing_audit_fields"]


def test_missing_decision_timestamp_is_incomplete():
    result = _audit(_metadata(decision_timestamp=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "decision_timestamp" in result["missing_audit_fields"]


def test_missing_no_mutation_history_is_incomplete():
    result = _audit(_metadata(no_mutation_history=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "no_mutation_history" in result["missing_audit_fields"]


def test_missing_rollback_policy_is_incomplete():
    result = _audit(_metadata(rollback_policy=""))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "rollback_policy" in result["missing_audit_fields"]


def test_prohibited_claims_check_is_required():
    result = _audit(_metadata(prohibited_claims_checked=False))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert "prohibited_claims_checked" in result["missing_audit_fields"]


def test_sensitive_data_review_is_required():
    result = _audit(_metadata(sensitive_data_review=False))

    assert result["audit_status"] == AUDIT_ENVELOPE_INCOMPLETE
    assert result["sensitive_data_review_required"] is True
    assert "sensitive_data_review" in result["missing_audit_fields"]


def test_durable_intake_performed_is_false():
    assert _audit()["durable_intake_performed"] is False


def test_corpus_mutation_performed_is_false():
    assert _audit()["corpus_mutation_performed"] is False


def test_db_write_performed_is_false():
    assert _audit()["db_write_performed"] is False


def test_output_is_deterministic_for_repeated_input():
    metadata = _metadata()

    assert _audit(metadata) == _audit(metadata)

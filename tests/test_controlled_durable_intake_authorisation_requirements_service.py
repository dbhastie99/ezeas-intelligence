from app.services.controlled_durable_intake_authorisation_requirements_service import (
    DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY,
    MISSING_REQUIRED_PREREQUISITES,
    build_controlled_durable_intake_authorisation_requirements,
)


def _metadata(**overrides):
    metadata = {
        "reviewer_confirmation": True,
        "source_status_boundary": True,
        "evidence_envelope": True,
        "no_overstatement_check": True,
        "rollback_policy": True,
        "audit_metadata": True,
        "dry_run_review": True,
    }
    metadata.update(overrides)
    return metadata


def _requirements(metadata=None):
    return build_controlled_durable_intake_authorisation_requirements(
        _metadata() if metadata is None else metadata
    )


def test_complete_prerequisites_produce_ready_status():
    assert _requirements()["requirements_status"] == (
        DURABLE_INTAKE_AUTHORISATION_REQUIREMENTS_READY
    )


def test_missing_reviewer_confirmation_blocks_readiness():
    result = _requirements(_metadata(reviewer_confirmation=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "reviewer_confirmation" in result["missing_prerequisites"]


def test_missing_source_status_boundary_blocks_readiness():
    result = _requirements(_metadata(source_status_boundary=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "source_status_boundary" in result["missing_prerequisites"]


def test_missing_evidence_envelope_blocks_readiness():
    result = _requirements(_metadata(evidence_envelope=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "evidence_envelope" in result["missing_prerequisites"]


def test_missing_no_overstatement_check_blocks_readiness():
    result = _requirements(_metadata(no_overstatement_check=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "no_overstatement_check" in result["missing_prerequisites"]


def test_missing_rollback_policy_blocks_readiness():
    result = _requirements(_metadata(rollback_policy=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "rollback_policy" in result["missing_prerequisites"]


def test_missing_audit_metadata_blocks_readiness():
    result = _requirements(_metadata(audit_metadata=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "audit_metadata" in result["missing_prerequisites"]


def test_missing_dry_run_review_blocks_readiness():
    result = _requirements(_metadata(dry_run_review=False))

    assert result["requirements_status"] == MISSING_REQUIRED_PREREQUISITES
    assert "dry_run_review" in result["missing_prerequisites"]


def test_durable_intake_authorised_now_is_false():
    assert _requirements()["durable_intake_authorised_now"] is False


def test_corpus_mutation_authorised_now_is_false():
    assert _requirements()["corpus_mutation_authorised_now"] is False


def test_db_write_authorised_now_is_false():
    assert _requirements()["db_write_authorised_now"] is False


def test_output_is_deterministic_for_repeated_input():
    metadata = _metadata()

    assert _requirements(metadata) == _requirements(metadata)

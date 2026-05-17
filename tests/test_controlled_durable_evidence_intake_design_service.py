from app.services.controlled_durable_evidence_intake_design_service import (
    BLOCKED_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_READY,
    NEEDS_MUTATION_BOUNDARY,
    NEEDS_REVIEW_BOUNDARY,
    NEEDS_ROLLBACK_POLICY,
    NEEDS_STORAGE_BOUNDARY,
    build_controlled_durable_evidence_intake_design,
)


def _metadata(**overrides):
    metadata = {
        "storage_boundary_model": "review-only source metadata; no corpus writes",
        "mutation_boundary_model": "future explicit gate required before mutation",
        "review_boundary_model": "reviewer confirmation required before action",
        "rollback_or_removal_policy": "rollback/removal policy must be approved",
    }
    metadata.update(overrides)
    return metadata


def _design(metadata=None):
    return build_controlled_durable_evidence_intake_design(
        _metadata() if metadata is None else metadata
    )


def test_complete_design_metadata_produces_ready_status():
    assert _design()["design_status"] == DURABLE_EVIDENCE_INTAKE_DESIGN_READY


def test_durable_intake_design_ready_can_be_true():
    assert _design()["durable_intake_design_ready"] is True


def test_durable_intake_authorised_now_is_false():
    assert _design()["durable_intake_authorised_now"] is False


def test_corpus_mutation_authorised_now_is_false():
    assert _design()["corpus_mutation_authorised_now"] is False


def test_db_write_authorised_now_is_false():
    assert _design()["db_write_authorised_now"] is False


def test_code_evidence_ingestion_authorised_now_is_false():
    assert _design()["code_evidence_ingestion_authorised_now"] is False


def test_missing_storage_boundary_produces_needs_storage_boundary():
    metadata = _metadata(storage_boundary_model="")

    assert _design(metadata)["design_status"] == NEEDS_STORAGE_BOUNDARY


def test_missing_mutation_boundary_produces_needs_mutation_boundary():
    metadata = _metadata(mutation_boundary_model="")

    assert _design(metadata)["design_status"] == NEEDS_MUTATION_BOUNDARY


def test_missing_review_boundary_produces_needs_review_boundary():
    metadata = _metadata(review_boundary_model="")

    assert _design(metadata)["design_status"] == NEEDS_REVIEW_BOUNDARY


def test_missing_rollback_or_removal_policy_produces_needs_rollback_policy():
    metadata = _metadata(rollback_or_removal_policy="")

    assert _design(metadata)["design_status"] == NEEDS_ROLLBACK_POLICY


def test_durable_ingestion_already_authorised_claim_is_blocked():
    result = _design(_metadata(durable_intake_authorised_now=True))

    assert result["design_status"] == BLOCKED_DURABLE_INGESTION_CLAIM
    assert result["durable_intake_authorised_now"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _design(_metadata(production_readiness_claim_permitted=True))

    assert result["design_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["db_write_authorised_now"] is False


def test_output_is_deterministic_for_repeated_input():
    metadata = _metadata()

    assert _design(metadata) == _design(metadata)

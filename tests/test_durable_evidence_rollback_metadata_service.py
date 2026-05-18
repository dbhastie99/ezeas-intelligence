from app.services.durable_evidence_rollback_metadata_service import (
    ROLLBACK_METADATA_READY,
    build_durable_evidence_rollback_metadata,
)


def _record(**overrides):
    metadata = {
        "record_id": "durable-evidence-record-local-fixture-v0-1",
        "record_status": "LOCAL_DURABLE_RECORD_PREPARED",
        "record_storage_mode": "LOCAL_CHECKED_IN_FIXTURE_ONLY",
        "reviewer_confirmation_available": True,
    }
    metadata.update(overrides)
    return metadata


def _rollback(**overrides):
    return build_durable_evidence_rollback_metadata(_record(**overrides))


def test_valid_local_durable_record_produces_ready():
    result = _rollback()

    assert result["rollback_status"] == ROLLBACK_METADATA_READY


def test_removal_supported_is_true():
    assert _rollback()["removal_supported"] is True


def test_reviewer_confirmation_is_required():
    result = _rollback()

    assert result["reviewer_confirmation_required"] is True


def test_audit_trail_is_required():
    result = _rollback()

    assert result["audit_trail_required"] is True


def test_live_corpus_mutation_performed_is_false():
    assert _rollback()["live_corpus_mutation_performed"] is False


def test_db_write_performed_is_false():
    assert _rollback()["db_write_performed"] is False


def test_missing_source_record_blocks_readiness():
    result = _rollback(record_id="")

    assert result["rollback_status"] == "NEEDS_SOURCE_RECORD"
    assert result["removal_supported"] is False


def test_reviewer_confirmation_missing_blocks_readiness():
    result = _rollback(reviewer_confirmation_available=False)

    assert result["rollback_status"] == "NEEDS_REVIEWER_CONFIRMATION"
    assert result["removal_supported"] is False


def test_output_is_deterministic():
    metadata = _record()

    assert build_durable_evidence_rollback_metadata(
        metadata
    ) == build_durable_evidence_rollback_metadata(metadata)

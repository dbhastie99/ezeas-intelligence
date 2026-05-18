import json
from copy import deepcopy
from pathlib import Path

from app.services.durable_evidence_retrieval_readiness_service import (
    BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM,
    DURABLE_EVIDENCE_RETRIEVAL_READY,
    NEEDS_CAVEATS,
    NEEDS_EVIDENCE_CATEGORY,
    NEEDS_RECORD_STATUS,
    NEEDS_ROLLBACK_METADATA,
    NEEDS_SOURCE_REFERENCE,
    NEEDS_SOURCE_STATUS,
    build_durable_evidence_retrieval_readiness,
)


FIXTURE_ROOT = Path("tests/fixtures/durable_evidence_intake")


def _json_fixture(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def _record(**overrides):
    record = _json_fixture("developer_log_durable_record_envelope_v0_1.json")
    record.update(overrides)
    return record


def _rollback(**overrides):
    rollback = _json_fixture("developer_log_rollback_metadata_v0_1.json")
    rollback.update(overrides)
    return rollback


def _readiness(record=None, rollback=None):
    return build_durable_evidence_retrieval_readiness(
        _record() if record is None else record,
        _rollback() if rollback is None else rollback,
    )


def test_complete_local_durable_record_produces_retrieval_ready():
    result = _readiness()

    assert result["readiness_status"] == DURABLE_EVIDENCE_RETRIEVAL_READY
    assert result["retrieval_ready"] is True


def test_missing_source_reference_blocks_readiness():
    result = _readiness(record=_record(source_reference=""))

    assert result["readiness_status"] == NEEDS_SOURCE_REFERENCE
    assert "source_reference" in result["missing_prerequisites"]


def test_missing_source_status_blocks_readiness():
    result = _readiness(record=_record(source_status=""))

    assert result["readiness_status"] == NEEDS_SOURCE_STATUS
    assert "source_status" in result["missing_prerequisites"]


def test_missing_evidence_category_blocks_readiness():
    result = _readiness(record=_record(evidence_category=""))

    assert result["readiness_status"] == NEEDS_EVIDENCE_CATEGORY
    assert "evidence_category" in result["missing_prerequisites"]


def test_missing_record_status_blocks_readiness():
    result = _readiness(record=_record(record_status=""))

    assert result["readiness_status"] == NEEDS_RECORD_STATUS
    assert "record_status" in result["missing_prerequisites"]


def test_missing_rollback_metadata_blocks_readiness():
    result = _readiness(rollback={})

    assert result["readiness_status"] == NEEDS_ROLLBACK_METADATA
    assert "rollback_metadata" in result["missing_prerequisites"]


def test_missing_caveats_blocks_readiness():
    result = _readiness(record=_record(required_caveats=[]))

    assert result["readiness_status"] == NEEDS_CAVEATS
    assert "required_caveats" in result["missing_prerequisites"]


def test_live_retrieval_and_llm_are_false():
    result = _readiness()

    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False


def test_db_read_and_write_are_false():
    result = _readiness()

    assert result["db_read_performed"] is False
    assert result["db_write_performed"] is False


def test_chat_exposure_authorised_is_false():
    assert _readiness()["chat_exposure_authorised"] is False


def test_live_retrieval_or_llm_claim_is_blocked():
    result = _readiness(record=_record(live_llm_performed=True))

    assert result["readiness_status"] == BLOCKED_LIVE_RETRIEVAL_OR_LLM_CLAIM
    assert result["live_llm_performed"] is False


def test_output_is_deterministic():
    record = _record()
    rollback = _rollback()

    assert _readiness(deepcopy(record), deepcopy(rollback)) == _readiness(
        deepcopy(record),
        deepcopy(rollback),
    )

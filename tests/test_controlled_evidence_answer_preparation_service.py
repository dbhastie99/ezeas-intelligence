import json
from copy import deepcopy
from pathlib import Path

from app.services.controlled_evidence_answer_preparation_service import (
    BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    CONTROLLED_ANSWER_PREPARATION_READY,
    build_controlled_evidence_answer_preparation,
)
from app.services.developer_log_evidence_retrieval_metadata_service import (
    build_developer_log_evidence_retrieval_metadata,
)
from app.services.durable_evidence_retrieval_readiness_service import (
    build_durable_evidence_retrieval_readiness,
)


FIXTURE_ROOT = Path("tests/fixtures/durable_evidence_intake")


def _json_fixture(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def _record():
    return _json_fixture("developer_log_durable_record_envelope_v0_1.json")


def _rollback():
    return _json_fixture("developer_log_rollback_metadata_v0_1.json")


def _retrieval_metadata(**overrides):
    record = _record()
    readiness = build_durable_evidence_retrieval_readiness(record, _rollback())
    metadata = build_developer_log_evidence_retrieval_metadata(record, readiness)
    metadata.update(overrides)
    return metadata


def _preparation(metadata=None):
    return build_controlled_evidence_answer_preparation(
        _retrieval_metadata() if metadata is None else metadata,
    )


def test_complete_retrieval_metadata_produces_controlled_preparation_ready():
    result = _preparation()

    assert result["preparation_status"] == CONTROLLED_ANSWER_PREPARATION_READY


def test_answer_ready_for_controlled_synthesis_can_be_true():
    assert _preparation()["answer_ready_for_controlled_synthesis"] is True


def test_final_answer_generated_is_false():
    assert _preparation()["final_answer_generated"] is False


def test_live_llm_performed_is_false():
    assert _preparation()["live_llm_performed"] is False


def test_chat_exposure_authorised_is_false():
    assert _preparation()["chat_exposure_authorised"] is False


def test_required_caveats_include_control_boundaries():
    caveats = _preparation()["required_answer_caveats"]

    assert "evidence-boundary" in caveats
    assert "implementation-status-boundary" in caveats
    assert "no-runtime-claim" in caveats
    assert "source-reference requirement" in caveats


def test_safe_answer_modes_are_controlled_summary_modes():
    safe_modes = _preparation()["safe_answer_modes"]

    assert "status-summary" in safe_modes
    assert "decision-summary" in safe_modes
    assert "risk-summary" in safe_modes
    assert "still-to-do-summary" in safe_modes


def test_final_answer_or_live_llm_claim_is_blocked():
    result = _preparation(_retrieval_metadata(final_answer_generated=True))

    assert result["preparation_status"] == BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM
    assert result["final_answer_generated"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _preparation(_retrieval_metadata(production_ready=True))

    assert result["preparation_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["chat_exposure_authorised"] is False


def test_output_is_deterministic():
    metadata = _retrieval_metadata()

    assert _preparation(deepcopy(metadata)) == _preparation(deepcopy(metadata))

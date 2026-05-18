import json
from copy import deepcopy
from pathlib import Path

from app.services.controlled_answer_synthesis_rehearsal_service import (
    BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM,
    BLOCKED_PROHIBITED_CLAIMS,
    CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY,
    build_controlled_answer_synthesis_rehearsal,
)
from app.services.controlled_evidence_answer_preparation_service import (
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


def _preparation(metadata=None, **overrides):
    metadata = _retrieval_metadata() if metadata is None else metadata
    preparation = build_controlled_evidence_answer_preparation(metadata)
    preparation.update(overrides)
    return preparation


def _rehearsal(preparation=None, metadata=None):
    metadata = _retrieval_metadata() if metadata is None else metadata
    preparation = _preparation(metadata) if preparation is None else preparation
    return build_controlled_answer_synthesis_rehearsal(preparation, metadata)


def test_complete_metadata_produces_controlled_synthesis_rehearsal_ready():
    result = _rehearsal()

    assert result["rehearsal_status"] == CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY


def test_answer_skeleton_prepared_can_be_true():
    assert _rehearsal()["answer_skeleton_prepared"] is True


def test_final_answer_generated_is_false():
    assert _rehearsal()["final_answer_generated"] is False


def test_live_llm_performed_is_false():
    assert _rehearsal()["live_llm_performed"] is False


def test_chat_exposure_authorised_is_false():
    assert _rehearsal()["chat_exposure_authorised"] is False


def test_evidence_references_are_preserved():
    metadata = _retrieval_metadata()
    result = _rehearsal(metadata=metadata)

    assert metadata["source_reference"] in result["evidence_references_used"]


def test_required_caveats_are_included():
    caveats = _rehearsal()["required_caveats_included"]

    assert "evidence-boundary" in caveats
    assert "implementation-status-boundary" in caveats
    assert "no-runtime-claim" in caveats
    assert "source-reference requirement" in caveats


def test_prohibited_claims_are_blocked():
    metadata = _retrieval_metadata(production_ready=True)
    result = _rehearsal(preparation=_preparation(), metadata=metadata)

    assert result["rehearsal_status"] == BLOCKED_PROHIBITED_CLAIMS
    assert "production_ready" in result["prohibited_claims_detected"]


def test_final_answer_or_live_llm_claim_is_blocked():
    result = _rehearsal(preparation=_preparation(final_answer_generated=True))

    assert result["rehearsal_status"] == BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM
    assert result["final_answer_generated"] is False


def test_safe_answer_sections_include_required_sections():
    sections = _rehearsal()["safe_answer_sections"]

    assert "status summary" in sections
    assert "decisions captured" in sections
    assert "risks" in sections
    assert "still-to-do" in sections
    assert "evidence boundaries" in sections


def test_answer_modes_include_controlled_summary_modes():
    modes = _rehearsal()["answer_modes_supported"]

    assert "status-summary" in modes
    assert "decision-summary" in modes
    assert "risk-summary" in modes
    assert "still-to-do-summary" in modes


def test_output_is_deterministic():
    metadata = _retrieval_metadata()
    preparation = _preparation(metadata)

    assert _rehearsal(deepcopy(preparation), deepcopy(metadata)) == _rehearsal(
        deepcopy(preparation),
        deepcopy(metadata),
    )

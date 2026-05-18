import json
from copy import deepcopy
from pathlib import Path

from app.services.controlled_answer_review_metadata_service import (
    BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    CONTROLLED_ANSWER_REVIEW_READY,
    build_controlled_answer_review_metadata,
)
from app.services.controlled_answer_synthesis_rehearsal_service import (
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


def _retrieval_metadata():
    record = _record()
    readiness = build_durable_evidence_retrieval_readiness(record, _rollback())
    return build_developer_log_evidence_retrieval_metadata(record, readiness)


def _rehearsal(**overrides):
    metadata = _retrieval_metadata()
    preparation = build_controlled_evidence_answer_preparation(metadata)
    rehearsal = build_controlled_answer_synthesis_rehearsal(preparation, metadata)
    rehearsal.update(overrides)
    return rehearsal


def _review(rehearsal=None):
    return build_controlled_answer_review_metadata(
        _rehearsal() if rehearsal is None else rehearsal,
    )


def test_clean_rehearsal_output_produces_controlled_answer_review_ready():
    result = _review()

    assert result["review_status"] == CONTROLLED_ANSWER_REVIEW_READY


def test_answer_skeleton_ready_for_human_review_can_be_true():
    assert _review()["answer_skeleton_ready_for_human_review"] is True


def test_final_answer_generated_is_false():
    assert _review()["final_answer_generated"] is False


def test_live_llm_performed_is_false():
    assert _review()["live_llm_performed"] is False


def test_chat_exposure_authorised_is_false():
    assert _review()["chat_exposure_authorised"] is False


def test_reviewer_confirmation_is_required():
    assert _review()["reviewer_confirmation_required"] is True


def test_required_review_checks_include_controlled_boundaries():
    checks = _review()["required_review_checks"]

    assert "source references" in checks
    assert "caveats" in checks
    assert "prohibited claim scan" in checks
    assert "evidence/implementation boundary" in checks
    assert "no-runtime claim" in checks
    assert "still-to-do clarity" in checks


def test_final_answer_or_chat_exposure_claim_is_blocked():
    result = _review(_rehearsal(final_answer_generated=True))

    assert result["review_status"] == BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM
    assert result["final_answer_generated"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _review(_rehearsal(production_ready=True))

    assert result["review_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["chat_exposure_authorised"] is False


def test_output_is_deterministic():
    rehearsal = _rehearsal()

    assert _review(deepcopy(rehearsal)) == _review(deepcopy(rehearsal))

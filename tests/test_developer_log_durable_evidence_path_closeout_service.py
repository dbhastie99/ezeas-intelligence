from copy import deepcopy

from app.services.developer_log_durable_evidence_path_closeout_service import (
    BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM,
    BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE,
    UNKNOWN_REQUIRES_REVIEW,
    build_developer_log_durable_evidence_path_closeout,
)


def _closeout(**overrides):
    return build_developer_log_durable_evidence_path_closeout(overrides)


def test_complete_practical_path_metadata_produces_complete_status():
    result = _closeout()

    assert (
        result["path_status"]
        == DEVELOPER_LOG_DURABLE_EVIDENCE_CONTROLLED_ANSWER_PATH_COMPLETE
    )


def test_progress_before_slice_is_approximately_85_to_90_percent():
    assert _closeout()["progress_before_slice"] == "approximately 85-90%"


def test_progress_after_slice_is_100_percent():
    assert _closeout()["progress_after_slice"] == "100%"


def test_all_practical_path_components_are_ready():
    result = _closeout()

    assert result["developer_log_candidate_ready"] is True
    assert result["durable_record_envelope_ready"] is True
    assert result["rollback_metadata_ready"] is True
    assert result["retrieval_readiness_ready"] is True
    assert result["retrieval_metadata_ready"] is True
    assert result["answer_preparation_ready"] is True
    assert result["synthesis_rehearsal_ready"] is True
    assert result["answer_review_metadata_ready"] is True
    assert result["answer_boundary_enforcement_ready"] is True


def test_live_llm_performed_is_false():
    assert _closeout()["live_llm_performed"] is False


def test_final_answer_generated_is_false():
    assert _closeout()["final_answer_generated"] is False


def test_chat_exposure_authorised_is_false():
    assert _closeout()["chat_exposure_authorised"] is False


def test_db_read_and_write_performed_are_false():
    result = _closeout()

    assert result["db_read_performed"] is False
    assert result["db_write_performed"] is False


def test_live_corpus_mutation_performed_is_false():
    assert _closeout()["live_corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_false():
    assert _closeout()["code_evidence_ingestion_performed"] is False


def test_runtime_integration_authorised_is_false():
    assert _closeout()["runtime_integration_authorised"] is False


def test_remaining_work_is_next_practical_path_decision_only():
    assert _closeout()["remaining_work"] == (
        "Choose the next practical Minerva value path.",
    )


def test_recommended_next_phase_options_are_explicit():
    options = _closeout()["recommended_next_phase_options"]

    assert "Option A: Add Hardening Log as second durable evidence type." in options
    assert "Option B: Add Platform Doctrine as second durable evidence type." in options
    assert (
        "Option C: Build a controlled retrieval harness over durable evidence fixtures."
        in options
    )
    assert "Option D: Pause Minerva while analytics schema work continues." in options


def test_live_llm_final_answer_or_chat_claim_is_blocked_or_review():
    status = _closeout(live_llm_performed=True)["path_status"]

    assert status in (
        BLOCKED_LIVE_LLM_OR_FINAL_ANSWER_CLAIM,
        UNKNOWN_REQUIRES_REVIEW,
    )


def test_db_or_live_corpus_mutation_claim_is_blocked_or_review():
    status = _closeout(db_write_performed=True)["path_status"]

    assert status in (
        BLOCKED_DB_OR_LIVE_CORPUS_MUTATION_CLAIM,
        UNKNOWN_REQUIRES_REVIEW,
    )


def test_runtime_or_production_overstatement_is_blocked_or_review():
    status = _closeout(production_ready=True)["path_status"]

    assert status in (
        BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        UNKNOWN_REQUIRES_REVIEW,
    )


def test_output_is_deterministic():
    metadata = {
        "developer_log_candidate_ready": True,
        "durable_record_envelope_ready": True,
        "rollback_metadata_ready": True,
    }

    assert _closeout(**deepcopy(metadata)) == _closeout(**deepcopy(metadata))

from app.services.developer_log_durable_evidence_candidate_service import (
    REQUIRED_DEVELOPER_LOG_SECTIONS,
    build_developer_log_durable_evidence_candidate,
)
from app.services.first_durable_evidence_intake_execution_service import (
    BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM,
    FIRST_DURABLE_EVIDENCE_RECORD_PREPARED,
    NEEDS_READY_CANDIDATE,
    NEEDS_ROLLBACK_METADATA,
    build_first_durable_evidence_intake_execution,
)


def _candidate(**overrides):
    metadata = {
        "candidate_id": "developer-log-candidate-test",
        "candidate_type": "DEVELOPER_LOG",
        "source_reference": "docs/evaluation/source.md",
        "source_status": "CONTROLLED_LOCAL_DURABLE_CANDIDATE_ONLY",
        "evidence_title": "Developer Log Candidate",
        "evidence_date": "2026-05-18",
        "repository_context": "ezeas-intelligence",
        "phase_context": "First practical durable evidence intake execution path",
        "sections_present": REQUIRED_DEVELOPER_LOG_SECTIONS,
        "sensitive_data_review_completed": True,
    }
    metadata.update(overrides)
    return build_developer_log_durable_evidence_candidate(metadata)


def _rollback(**overrides):
    metadata = {
        "rollback_status": "ROLLBACK_METADATA_READY",
        "source_record_id": "durable-evidence-record-local-fixture-v0-1",
    }
    metadata.update(overrides)
    return metadata


def _execution(**overrides):
    return build_first_durable_evidence_intake_execution(
        _candidate(**overrides),
        _rollback(),
    )


def test_ready_developer_log_candidate_produces_record_prepared():
    result = _execution()

    assert result["execution_status"] == FIRST_DURABLE_EVIDENCE_RECORD_PREPARED
    assert result["durable_record_prepared"] is True


def test_local_fixture_artifact_record_preparation_can_be_true():
    result = _execution()

    assert result["durable_record_written_to_local_fixture"] is True
    assert result["record_storage_mode"] == "LOCAL_CHECKED_IN_FIXTURE_ONLY"


def test_live_corpus_mutation_performed_is_false():
    assert _execution()["live_corpus_mutation_performed"] is False


def test_db_write_performed_is_false():
    assert _execution()["db_write_performed"] is False


def test_code_evidence_ingestion_performed_is_false():
    assert _execution()["code_evidence_ingestion_performed"] is False


def test_live_retrieval_performed_is_false():
    assert _execution()["live_retrieval_performed"] is False


def test_live_llm_performed_is_false():
    assert _execution()["live_llm_performed"] is False


def test_final_answer_generation_performed_is_false():
    assert _execution()["final_answer_generation_performed"] is False


def test_chat_exposure_authorised_is_false():
    assert _execution()["chat_exposure_authorised"] is False


def test_rollback_metadata_is_required():
    result = build_first_durable_evidence_intake_execution(_candidate(), None)

    assert result["execution_status"] == NEEDS_ROLLBACK_METADATA
    assert result["rollback_metadata_required"] is True


def test_non_ready_candidate_blocks_execution():
    result = build_first_durable_evidence_intake_execution(
        _candidate(source_reference=""),
        _rollback(),
    )

    assert result["execution_status"] == NEEDS_READY_CANDIDATE
    assert result["durable_record_prepared"] is False


def test_live_corpus_or_db_claim_blocks_execution():
    candidate = _candidate()
    candidate["db_write_performed"] = True

    result = build_first_durable_evidence_intake_execution(candidate, _rollback())

    assert result["execution_status"] == BLOCKED_LIVE_CORPUS_OR_DB_MUTATION_CLAIM
    assert result["db_write_performed"] is False


def test_output_is_deterministic():
    candidate = _candidate()
    rollback = _rollback()

    assert build_first_durable_evidence_intake_execution(
        candidate,
        rollback,
    ) == build_first_durable_evidence_intake_execution(candidate, rollback)

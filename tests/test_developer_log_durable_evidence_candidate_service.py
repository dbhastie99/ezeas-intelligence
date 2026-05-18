from app.services.developer_log_durable_evidence_candidate_service import (
    BLOCKED_PROHIBITED_CLAIMS,
    DEVELOPER_LOG_CANDIDATE_READY,
    NEEDS_REQUIRED_SECTIONS,
    NEEDS_SENSITIVE_DATA_REVIEW,
    NEEDS_SOURCE_REFERENCE,
    NEEDS_SOURCE_STATUS,
    REQUIRED_DEVELOPER_LOG_SECTIONS,
    build_developer_log_durable_evidence_candidate,
)


def _metadata(**overrides):
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
    return metadata


def _candidate(**overrides):
    return build_developer_log_durable_evidence_candidate(_metadata(**overrides))


def test_complete_developer_log_metadata_produces_ready():
    result = _candidate()

    assert result["candidate_status"] == DEVELOPER_LOG_CANDIDATE_READY
    assert result["candidate_type"] == "DEVELOPER_LOG"


def test_missing_source_reference_blocks_readiness():
    result = _candidate(source_reference="")

    assert result["candidate_status"] == NEEDS_SOURCE_REFERENCE
    assert result["eligible_for_durable_intake"] is False


def test_missing_source_status_blocks_readiness():
    result = _candidate(source_status="")

    assert result["candidate_status"] == NEEDS_SOURCE_STATUS
    assert result["eligible_for_durable_intake"] is False


def test_missing_required_sections_blocks_readiness():
    result = _candidate(sections_present=REQUIRED_DEVELOPER_LOG_SECTIONS[:-1])

    assert result["candidate_status"] == NEEDS_REQUIRED_SECTIONS
    assert result["required_sections_present"] is False
    assert "User Guide / Rationale & Operating Model" in result["missing_sections"]


def test_sensitive_data_review_is_required():
    result = _candidate(sensitive_data_review_completed=False)

    assert result["candidate_status"] == NEEDS_SENSITIVE_DATA_REVIEW
    assert result["sensitive_data_review_required"] is True


def test_prohibited_runtime_production_implementation_claims_block_readiness():
    for key in (
        "production_readiness_claim_permitted",
        "runtime_readiness_claim_permitted",
        "db_write_performed",
        "live_llm_performed",
    ):
        result = _candidate(**{key: True})

        assert result["candidate_status"] == BLOCKED_PROHIBITED_CLAIMS
        assert result["prohibited_claims_present"] is True


def test_eligible_for_durable_intake_only_when_complete_and_reviewed():
    assert _candidate()["eligible_for_durable_intake"] is True
    assert _candidate(sensitive_data_review_completed=False)[
        "eligible_for_durable_intake"
    ] is False
    assert _candidate(source_reference="")["eligible_for_durable_intake"] is False


def test_output_is_deterministic():
    metadata = _metadata()

    assert build_developer_log_durable_evidence_candidate(
        metadata
    ) == build_developer_log_durable_evidence_candidate(metadata)

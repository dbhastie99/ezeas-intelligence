from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
    build_controlled_durable_evidence_retrieval_harness,
)


EXPECTED_FALSE_BOUNDARIES = (
    "LiveLLMCalled",
    "FinalAnswerGenerated",
    "ChatExposureEnabled",
    "DatabaseReadPerformed",
    "DatabaseWritePerformed",
    "LiveCorpusMutationPerformed",
    "CodeEvidenceIngestionPerformed",
    "RetrievalBackendChanged",
    "RuntimeIntegrationPerformed",
    "ProductionReadinessClaimed",
)


def _retrieve(query):
    return build_controlled_durable_evidence_retrieval_harness(query)


def test_positive_developer_log_status_query_returns_fixture_result():
    result = _retrieve("Developer Log durable evidence path status")

    assert result["RetrievalMode"] == "DETERMINISTIC_KEYWORD_METADATA_FIXTURE_RETRIEVAL_V0_1"
    assert result["FixtureUniverse"] == "CONTROLLED_DURABLE_DEVELOPER_LOG_FIXTURES_V0_1"
    assert result["EvidenceTypesInScope"] == ("DEVELOPER_LOG",)
    assert result["ResultCount"] >= 1
    assert result["Results"][0]["RecordId"] == "controlled-evidence-intake-developer-log-v0-1"


def test_live_llm_boundary_query_retrieves_developer_log_fixture():
    result = _retrieve("What evidence says Minerva did not call a live LLM?")

    assert result["ResultCount"] >= 1
    top = result["Results"][0]
    assert "live" in top["MatchedTerms"]
    assert "llm" in top["MatchedTerms"]
    assert top["FinalAnswerPermitted"] is False


def test_controlled_answer_path_closeout_query_returns_retrieval_story_only():
    result = _retrieve("Developer Log controlled answer path closeout")

    assert result["ResultCount"] >= 1
    assert result["RetrievalStoryOnly"] is True
    assert result["FinalAnswerPermitted"] is False


def test_prohibited_boundary_query_preserves_cannot_prove_terms():
    result = _retrieve("What remains prohibited for Minerva Developer Log evidence?")

    assert result["ResultCount"] >= 1
    cannot_prove = " ".join(result["Results"][0]["CannotProve"])
    assert "runtime readiness" in cannot_prove
    assert "production readiness" in cannot_prove
    assert "Code Evidence ingestion" in cannot_prove


def test_boundary_flags_are_false_on_envelope_and_results():
    result = _retrieve("Developer Log durable evidence path status")

    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert result["BoundaryFlags"][flag] is False
    assert result["BoundaryFlags"] == BOUNDARY_FLAGS
    for retrieval_result in result["Results"]:
        for flag in EXPECTED_FALSE_BOUNDARIES:
            assert retrieval_result["BoundaryFlags"][flag] is False


def test_source_and_status_boundaries_are_preserved():
    result = _retrieve("Developer Log durable evidence path status")
    top = result["Results"][0]

    assert top["SourceType"] == "developer log"
    assert top["SourceTitle"] == "Developer Log - governed evidence intake planning"
    assert top["SourceStatus"] == "PLANNING_EVIDENCE"
    assert top["ImplementationStatus"] == "IMPLEMENTATION_NOT_PROVEN_BY_THIS_FIXTURE"
    assert top["AnswerUseStatus"] == "FINAL_ANSWER_NOT_PERMITTED_RETRIEVAL_ONLY"
    assert top["CaveatRequired"] is True


def test_hardening_log_query_does_not_fabricate_evidence():
    result = _retrieve("What does the Hardening Log say?")

    assert result["ResultCount"] == 0
    assert result["Results"] == ()
    assert result["UnsupportedEvidenceTypes"] == ("HARDENING_LOG",)
    assert any("Developer Log fixtures" in caveat for caveat in result["Caveats"])


def test_platform_doctrine_query_does_not_fabricate_evidence():
    result = _retrieve("What does Platform Doctrine say?")

    assert result["ResultCount"] == 0
    assert result["Results"] == ()
    assert result["UnsupportedEvidenceTypes"] == ("PLATFORM_DOCTRINE",)
    assert any("future slice" in caveat for caveat in result["Caveats"])


def test_ordering_is_deterministic_for_same_fixture_set():
    first = _retrieve("Developer Log durable evidence path status")
    second = _retrieve("Developer Log durable evidence path status")

    assert [item["RecordId"] for item in first["Results"]] == [
        item["RecordId"] for item in second["Results"]
    ]
    assert first["Results"] == second["Results"]


def test_output_is_not_final_natural_language_answer_generation():
    result = _retrieve("Developer Log durable evidence path status")

    assert result["RetrievalStoryOnly"] is True
    assert result["FinalAnswerPermitted"] is False
    assert result["BoundaryFlags"]["FinalAnswerGenerated"] is False
    assert "FinalAnswer" not in result
    assert "AnswerText" not in result
    assert "GeneratedAnswer" not in result
    for retrieval_result in result["Results"]:
        assert retrieval_result["FinalAnswerPermitted"] is False

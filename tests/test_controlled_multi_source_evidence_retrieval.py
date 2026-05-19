from app.services.controlled_multi_source_evidence_retrieval_service import (
    BOUNDARY_FLAGS,
    build_controlled_multi_source_evidence_retrieval,
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

REQUIRED_RESULT_FIELDS = (
    "EvidenceType",
    "SourceStatus",
    "AuthorityLevel",
    "ImplementationStatus",
    "CurrentTruthStatus",
    "AnswerUseStatus",
    "CanProve",
    "CannotProve",
    "RequiredCaveats",
)


def _retrieve(query, filters=None):
    return build_controlled_multi_source_evidence_retrieval(query, filters)


def _top_type(result):
    return result["Results"][0]["EvidenceType"]


def test_platform_doctrine_query_returns_platform_doctrine_fixture_first():
    result = _retrieve("What does Platform Doctrine say about no live Minerva runtime?")

    assert result["RetrievalMode"] == "DETERMINISTIC_MULTI_SOURCE_KEYWORD_METADATA_FIXTURE_RETRIEVAL_V0_1"
    assert result["EvidenceUniverse"] == "CONTROLLED_MULTI_SOURCE_LOCAL_FIXTURES_V0_1"
    assert result["EvidenceTypesSearched"] == (
        "PLATFORM_DOCTRINE",
        "HARDENING_LOG",
        "DEVELOPER_LOG",
    )
    assert result["ResultCount"] >= 1
    assert _top_type(result) == "PLATFORM_DOCTRINE"
    assert result["Results"][0]["RecordId"] == "fixture-platform-doctrine"
    assert "doctrine" in result["Results"][0]["MatchedTerms"]
    assert any("doctrine context" in caveat.lower() for caveat in result["Results"][0]["RequiredCaveats"])


def test_hardening_query_returns_hardening_log_fixture_first():
    result = _retrieve("What hardening remains for Minerva evidence paths?")

    assert result["ResultCount"] >= 1
    assert _top_type(result) == "HARDENING_LOG"
    assert result["Results"][0]["RecordId"] == "fixture-hardening-log"
    assert "hardening" in result["Results"][0]["MatchedTerms"]
    assert any("not implementation proof" in caveat.lower() for caveat in result["Results"][0]["RequiredCaveats"])


def test_developer_log_durable_path_query_returns_developer_log_fixture_first():
    result = _retrieve("What did the Developer Log durable evidence path complete?")

    assert result["ResultCount"] >= 1
    assert _top_type(result) == "DEVELOPER_LOG"
    assert result["Results"][0]["RecordId"] == "fixture-developer-log"
    assert "developer" in result["Results"][0]["MatchedTerms"]
    assert "complete" in result["Results"][0]["MatchedTerms"]


def test_source_authority_combines_with_query_relevance():
    doctrine = _retrieve("What is the doctrine on no live Minerva runtime?")
    completed = _retrieve("What did the Developer Log durable evidence path complete?")
    prohibited = _retrieve("What remains prohibited after Minerva controlled-readiness?")

    assert _top_type(doctrine) == "PLATFORM_DOCTRINE"
    assert _top_type(completed) == "DEVELOPER_LOG"
    assert prohibited["Results"][0]["EvidenceType"] in {"HARDENING_LOG", "PLATFORM_DOCTRINE"}
    assert "Source authority is not treated as the same thing as query relevance" in prohibited["AuthorityPolicyApplied"]


def test_every_result_preserves_source_status_and_answer_use_boundaries():
    result = _retrieve("What remains prohibited after Minerva controlled-readiness?")

    assert result["ResultCount"] >= 2
    for retrieval_result in result["Results"]:
        for field in REQUIRED_RESULT_FIELDS:
            assert retrieval_result[field]
        assert retrieval_result["FinalAnswerPermitted"] is False
        assert retrieval_result["AnswerUseStatus"] == "FINAL_ANSWER_NOT_PERMITTED_RETRIEVAL_ONLY"
        assert retrieval_result["ImplementationStatus"] == "IMPLEMENTATION_NOT_PROVEN_BY_THIS_FIXTURE"
        assert isinstance(retrieval_result["CanProve"], tuple)
        assert isinstance(retrieval_result["CannotProve"], tuple)
        assert isinstance(retrieval_result["RequiredCaveats"], tuple)


def test_boundary_flags_are_false_on_envelope_and_results():
    result = _retrieve("What remains prohibited after Minerva controlled-readiness?")

    assert result["BoundaryFlags"] == BOUNDARY_FLAGS
    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert result["BoundaryFlags"][flag] is False
    for retrieval_result in result["Results"]:
        for flag in EXPECTED_FALSE_BOUNDARIES:
            assert retrieval_result["BoundaryFlags"][flag] is False


def test_retrieval_does_not_overclaim_runtime_current_truth_or_implementation():
    result = _retrieve("What remains prohibited after Minerva controlled-readiness?")
    combined_cannot = " ".join(
        " ".join(retrieval_result["CannotProve"])
        for retrieval_result in result["Results"]
    )
    combined_caveats = " ".join(result["Caveats"])

    assert "controlled-readiness does not imply runtime" in combined_caveats.lower()
    assert "historical evidence is not current truth by default" in combined_caveats.lower()
    assert "runtime implementation" in combined_cannot
    assert "execution proof" in combined_cannot
    assert "implementation proof" in combined_cannot
    assert result["FinalAnswerPermitted"] is False
    assert result["RetrievalStoryOnly"] is True
    assert "FinalAnswer" not in result
    assert "AnswerText" not in result
    assert "GeneratedAnswer" not in result


def test_unsupported_source_queries_do_not_fabricate_results():
    for query, expected_type in (
        ("What does Code Evidence say?", "CODE_EVIDENCE"),
        ("What is the live DB state?", "LIVE_DB"),
        ("What does Analytics Readiness Summary say?", "ANALYTICS_READINESS_SUMMARY"),
    ):
        result = _retrieve(query)

        assert result["ResultCount"] == 0
        assert result["Results"] == ()
        assert expected_type in result["UnsupportedEvidenceTypes"]
        assert any("No evidence is fabricated" in caveat for caveat in result["Caveats"])
        for flag in EXPECTED_FALSE_BOUNDARIES:
            assert result["BoundaryFlags"][flag] is False


def test_supported_filter_searches_only_requested_supported_source_type():
    result = _retrieve(
        "What remains prohibited after Minerva controlled-readiness?",
        filters={"evidence_type": "HARDENING_LOG"},
    )

    assert result["ResultCount"] == 1
    assert result["Results"][0]["EvidenceType"] == "HARDENING_LOG"


def test_ordering_is_deterministic_for_same_query():
    first = _retrieve("What remains prohibited after Minerva controlled-readiness?")
    second = _retrieve("What remains prohibited after Minerva controlled-readiness?")

    assert [item["RecordId"] for item in first["Results"]] == [
        item["RecordId"] for item in second["Results"]
    ]
    assert first["Results"] == second["Results"]

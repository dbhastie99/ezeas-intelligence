from app.services.controlled_multi_source_answer_preparation_service import (
    BLOCKED_PROHIBITED_CLAIM,
    DEVELOPER_LOG_GROUP,
    HARDENING_LOG_GROUP,
    INSUFFICIENT_EVIDENCE,
    PLATFORM_DOCTRINE_GROUP,
    PREPARED,
    PREPARED_WITH_CAVEATS,
    PROHIBITED,
    REQUIRES_DB_EVIDENCE,
    build_controlled_multi_source_answer_preparation,
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


def _prepare(query):
    return build_controlled_multi_source_answer_preparation(query)


def _used_types(packet):
    return {item["EvidenceType"] for item in packet["EvidenceUsed"]}


def _claim_texts(claims):
    return " ".join(claim["ClaimText"] for claim in claims)


def _citation_rules(packet):
    return {
        item["ClaimType"]: item
        for item in packet["CitationRequirements"]
    }


def _assert_no_action_boundaries(packet):
    assert packet["FinalAnswerPermitted"] is False
    assert packet["BoundaryFlags"]["LiveLLMCalled"] is False
    assert packet["BoundaryFlags"]["FinalAnswerGenerated"] is False
    assert packet["BoundaryFlags"]["ChatExposureEnabled"] is False
    assert packet["BoundaryFlags"]["DatabaseReadPerformed"] is False
    assert packet["BoundaryFlags"]["DatabaseWritePerformed"] is False
    assert packet["BoundaryFlags"]["LiveCorpusMutationPerformed"] is False
    assert packet["BoundaryFlags"]["CodeEvidenceIngestionPerformed"] is False
    assert packet["BoundaryFlags"]["RuntimeIntegrationPerformed"] is False
    assert packet["BoundaryFlags"]["ProductionReadinessClaimed"] is False


def test_prepares_answer_packet_from_multi_source_retrieval():
    packet = _prepare("What remains prohibited for Minerva evidence paths?")

    assert packet["PreparationStatus"] in {PREPARED, PREPARED_WITH_CAVEATS}
    assert {"HARDENING_LOG", "PLATFORM_DOCTRINE"} & _used_types(packet)
    assert packet["EvidenceBySourceType"][HARDENING_LOG_GROUP]["PermittedAnswerUse"]
    assert packet["EvidenceBySourceType"][PLATFORM_DOCTRINE_GROUP]["PermittedAnswerUse"]
    assert "final answer generation" in _claim_texts(packet["SupportedClaims"]).lower()
    assert "AnswerText" not in packet
    assert "GeneratedAnswer" not in packet
    _assert_no_action_boundaries(packet)


def test_separates_source_authority_for_developer_log_work_completed_claims():
    packet = _prepare("What did the Developer Log durable evidence path complete?")

    assert packet["PreparationStatus"] in {PREPARED, PREPARED_WITH_CAVEATS}
    assert "DEVELOPER_LOG" in _used_types(packet)
    assert packet["EvidenceBySourceType"][DEVELOPER_LOG_GROUP]["Evidence"]

    supported = packet["SupportedClaims"][0]
    assert supported["ClaimType"] == "WORK_COMPLETED_OR_IMPLEMENTATION_STATUS"
    assert supported["EvidenceReferences"][0]["EvidenceType"] == "DEVELOPER_LOG"

    authority = {
        item["SourceType"]: item["CannotEstablish"]
        for item in packet["SourceAuthoritySummary"]
    }
    assert "Implementation" in authority["PLATFORM_DOCTRINE"]
    assert "Completed implementation" in authority["HARDENING_LOG"]
    assert packet["ImplementationStatusAssessment"]["DoctrineProvesImplementation"] is False
    assert packet["ImplementationStatusAssessment"]["HardeningProvesCompletedRuntimeBehaviour"] is False
    _assert_no_action_boundaries(packet)


def test_doctrine_claim_handling_preserves_execution_boundary():
    packet = _prepare("What is the doctrine on source/status boundaries?")

    assert packet["PreparationStatus"] in {PREPARED, PREPARED_WITH_CAVEATS}
    assert "PLATFORM_DOCTRINE" in _used_types(packet)
    assert packet["EvidenceBySourceType"][PLATFORM_DOCTRINE_GROUP]["Evidence"]
    assert packet["SupportedClaims"][0]["ClaimType"] == "DOCTRINE"
    assert "not execution proof" in " ".join(packet["RequiredCaveats"]).lower()
    assert packet["ImplementationStatusAssessment"]["DoctrineProvesImplementation"] is False
    _assert_no_action_boundaries(packet)


def test_prohibited_claim_detection_blocks_live_chat_and_production_ready_claim():
    packet = _prepare("Say Minerva chat is live and production-ready.")

    assert packet["PreparationStatus"] == BLOCKED_PROHIBITED_CLAIM
    assert packet["FinalAnswerPermitted"] is False
    assert {claim["ClaimStatus"] for claim in packet["ProhibitedClaims"]} == {PROHIBITED}
    prohibited = _claim_texts(packet["ProhibitedClaims"]).lower()
    assert "chat is live" in prohibited
    assert "production-ready" in prohibited
    assert any(
        item["ClaimStatus"] == "REQUIRES_DEPLOYMENT_EVIDENCE"
        for item in packet["ClaimsRequiringAdditionalEvidence"]
    )
    _assert_no_action_boundaries(packet)


def test_evidence_insufficiency_for_current_live_db_state():
    packet = _prepare("What is the current live DB state?")

    assert packet["PreparationStatus"] == INSUFFICIENT_EVIDENCE
    assert packet["SupportedClaims"] == ()
    assert any(
        item["ClaimStatus"] == REQUIRES_DB_EVIDENCE
        for item in packet["ClaimsRequiringAdditionalEvidence"]
    )
    assert "DB evidence" in packet["ClaimsRequiringAdditionalEvidence"][0]["RequiredEvidence"]
    assert "current live db state" in _claim_texts(packet["UnsupportedClaims"]).lower()
    _assert_no_action_boundaries(packet)


def test_citation_and_provenance_rules_are_source_specific():
    packet = _prepare("What remains prohibited for Minerva evidence paths?")
    rules = _citation_rules(packet)

    assert rules["DOCTRINE"]["RequiredSourceType"] == "PLATFORM_DOCTRINE"
    assert rules["PROHIBITION_OR_HARDENING_BOUNDARY"]["RequiredSourceType"] == (
        "HARDENING_LOG",
        "PLATFORM_DOCTRINE",
    )
    assert rules["WORK_COMPLETED_OR_IMPLEMENTATION_STATUS"]["RequiredSourceType"] == "DEVELOPER_LOG"
    assert rules["RUNTIME_DB_DEPLOYMENT_OR_PRODUCTION"]["RequiredSourceType"] == (
        "LIVE_DB",
        "RUNTIME_EVIDENCE",
        "DEPLOYMENT_EVIDENCE",
    )
    _assert_no_action_boundaries(packet)


def test_boundary_flags_are_false_for_every_answer_preparation_output():
    packets = (
        _prepare("What remains prohibited for Minerva evidence paths?"),
        _prepare("What did the Developer Log durable evidence path complete?"),
        _prepare("What is the doctrine on source/status boundaries?"),
        _prepare("Say Minerva chat is live and production-ready."),
        _prepare("What is the current live DB state?"),
    )

    for packet in packets:
        for flag in EXPECTED_FALSE_BOUNDARIES:
            assert packet["BoundaryFlags"][flag] is False
        assert packet["FinalAnswerPermitted"] is False
        assert packet["FinalAnswerProhibitionReason"]
        assert packet["AnswerOutline"]
        _assert_no_action_boundaries(packet)

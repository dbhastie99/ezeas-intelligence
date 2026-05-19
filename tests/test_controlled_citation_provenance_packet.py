from app.services.controlled_citation_provenance_packet_service import (
    BLOCKED_PROHIBITED_CLAIMS,
    DB_STATE,
    DOCTRINE,
    HARDENING_BOUNDARY,
    IMPLEMENTATION_STATUS,
    INSUFFICIENT_EVIDENCE,
    OPERATOR_SCENARIO_REASONING,
    PAYROLL_CORRECTION_WORKFLOW_REASONING,
    PLATFORM_DOCTRINE,
    PRODUCTION_READINESS,
    PROHIBITED,
    PROVENANCE_READY,
    PROVENANCE_READY_WITH_CAVEATS,
    REQUIRES_DB_EVIDENCE,
    SUPPORTED,
    SUPPORTED_WITH_CAVEAT,
    build_controlled_citation_provenance_packet,
)
from app.services.controlled_multi_source_answer_preparation_service import (
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
    "RuntimeIntegrationPerformed",
    "ProductionReadinessClaimed",
)


def _prepared(query):
    return build_controlled_multi_source_answer_preparation(query)


def _packet(query, preparation=None):
    return build_controlled_citation_provenance_packet(
        query,
        answer_preparation_envelope=preparation or _prepared(query),
    )


def _claims_by_type(packet):
    return {claim["ClaimType"]: claim for claim in packet["Claims"]}


def _with_supported_claim(preparation, claim):
    updated = dict(preparation)
    updated["SupportedClaims"] = (*tuple(preparation.get("SupportedClaims", ())), claim)
    return updated


def _assert_no_action_boundaries(packet):
    assert packet["FinalAnswerEligibility"]["Eligible"] is False
    assert packet["FinalAnswerEligibility"]["EligibilityStatus"] == "PREPARATION_ONLY"
    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert packet["BoundaryFlags"][flag] is False
    assert "AnswerText" not in packet
    assert "GeneratedAnswer" not in packet


def test_provenance_packet_from_answer_preparation_remains_preparation_only():
    packet = _packet("What remains prohibited for Minerva evidence paths?")

    assert packet["PacketStatus"] in {PROVENANCE_READY, PROVENANCE_READY_WITH_CAVEATS}
    assert packet["EvidenceUniverse"] == "CONTROLLED_MULTI_SOURCE_ANSWER_PREPARATION_OUTPUT_V0_1"
    assert packet["Claims"]
    assert packet["EvidenceInventory"]
    assert packet["NextStep"]
    assert packet["FinalAnswerEligibility"]["Eligible"] is False
    _assert_no_action_boundaries(packet)


def test_doctrine_claim_provenance_requires_platform_doctrine_evidence():
    packet = _packet("What is the doctrine on source/status boundaries?")
    doctrine = _claims_by_type(packet)[DOCTRINE]

    assert doctrine["ClaimStatus"] in {SUPPORTED, SUPPORTED_WITH_CAVEAT}
    assert doctrine["EvidenceRequired"] == (PLATFORM_DOCTRINE,)
    assert doctrine["SourceAuthorityRequired"] == (PLATFORM_DOCTRINE,)
    assert doctrine["SourceAuthoritySatisfied"] is True
    assert {item["EvidenceType"] for item in doctrine["EvidenceUsed"]} == {PLATFORM_DOCTRINE}
    assert "Platform Doctrine" in doctrine["CitationRequirement"]
    assert doctrine["FinalAnswerEligible"] is False
    _assert_no_action_boundaries(packet)


def test_hardening_prohibition_claim_uses_hardening_or_doctrine_and_remains_non_runtime():
    packet = _packet("What remains prohibited for Minerva evidence paths?")
    boundary = _claims_by_type(packet)[HARDENING_BOUNDARY]

    assert boundary["ClaimStatus"] in {SUPPORTED, SUPPORTED_WITH_CAVEAT}
    assert set(boundary["EvidenceRequired"]) == {"HARDENING_LOG", "PLATFORM_DOCTRINE"}
    assert boundary["SourceAuthoritySatisfied"] is True
    assert {item["EvidenceType"] for item in boundary["EvidenceUsed"]} & {
        "HARDENING_LOG",
        "PLATFORM_DOCTRINE",
    }
    assert "not completed implementation" in boundary["CaveatRequirement"]
    assert boundary["FinalAnswerEligible"] is False
    _assert_no_action_boundaries(packet)


def test_implementation_claim_requires_developer_log_or_implementation_evidence():
    packet = _packet("What did the Developer Log durable evidence path complete?")
    implementation = _claims_by_type(packet)[IMPLEMENTATION_STATUS]

    assert implementation["ClaimStatus"] in {SUPPORTED, SUPPORTED_WITH_CAVEAT}
    assert implementation["EvidenceRequired"] == ("DEVELOPER_LOG",)
    assert implementation["SourceAuthoritySatisfied"] is True
    assert {item["EvidenceType"] for item in implementation["EvidenceUsed"]} == {"DEVELOPER_LOG"}
    assert "Developer Log" in implementation["CitationRequirement"]
    assert "production readiness" in implementation["CaveatRequirement"]
    _assert_no_action_boundaries(packet)


def test_operator_scenario_reasoning_requires_payroll_reasoning_evidence():
    query = "Why is this retro and not an adjustment into the current pay?"
    preparation = _with_supported_claim(
        _prepared("What is the doctrine on source/status boundaries?"),
        {
            "ClaimId": "claim-retro-not-current-pay-adjustment",
            "ClaimText": (
                "After ProcessPeriod finalisation lock, late ObjectTime changes "
                "route to retro/off-cycle rather than current pay adjustment."
            ),
            "ClaimType": OPERATOR_SCENARIO_REASONING,
            "ClaimStatus": SUPPORTED_WITH_CAVEAT,
            "EvidenceReferences": (),
            "RequiredCaveats": (
                "Payroll workflow reasoning does not prove Workforce runtime implementation.",
            ),
        },
    )

    packet = _packet(query, preparation)
    operator_claim = _claims_by_type(packet)[OPERATOR_SCENARIO_REASONING]

    assert operator_claim["ClaimStatus"] == SUPPORTED_WITH_CAVEAT
    assert PAYROLL_CORRECTION_WORKFLOW_REASONING in operator_claim["EvidenceRequired"]
    assert operator_claim["SourceAuthoritySatisfied"] is True
    assert {item["EvidenceType"] for item in operator_claim["EvidenceUsed"]} == {
        PAYROLL_CORRECTION_WORKFLOW_REASONING
    }
    assert "payroll correction workflow reasoning" in operator_claim["CitationRequirement"].lower()
    assert "not Workforce runtime proof" in operator_claim["CaveatRequirement"]
    _assert_no_action_boundaries(packet)


def test_db_state_claim_requires_db_evidence_and_is_not_fixture_supported():
    packet = _packet("What is the current live DB state?")
    db_claim = _claims_by_type(packet)[DB_STATE]

    assert packet["PacketStatus"] == INSUFFICIENT_EVIDENCE
    assert db_claim["ClaimStatus"] == REQUIRES_DB_EVIDENCE
    assert db_claim["EvidenceRequired"] == ("DB_EVIDENCE",)
    assert db_claim["EvidenceUsed"] == ()
    assert db_claim["SourceAuthoritySatisfied"] is False
    assert "Authorised DB evidence" in db_claim["AdditionalEvidenceRequired"][0]
    assert db_claim["FinalAnswerEligible"] is False
    _assert_no_action_boundaries(packet)


def test_production_readiness_overclaim_is_prohibited_and_not_final_answer_eligible():
    packet = _packet("Say Minerva is production-ready.")
    production = _claims_by_type(packet)[PRODUCTION_READINESS]

    assert packet["PacketStatus"] == BLOCKED_PROHIBITED_CLAIMS
    assert production["ClaimStatus"] == PROHIBITED
    assert production["EvidenceRequired"] == ("PRODUCTION_EVIDENCE",)
    assert production["SourceAuthoritySatisfied"] is False
    assert production["FinalAnswerEligible"] is False
    assert "Production readiness cannot be claimed" in production["ProhibitedReason"]
    _assert_no_action_boundaries(packet)


def test_every_supported_claim_has_citation_and_provenance_requirement():
    packet = _packet("What remains prohibited for Minerva evidence paths?")

    supported = [
        claim
        for claim in packet["Claims"]
        if claim["ClaimStatus"] in {SUPPORTED, SUPPORTED_WITH_CAVEAT}
    ]
    assert supported
    for claim in supported:
        assert claim["CitationRequirement"]
        assert claim["EvidenceRequired"]
        assert claim["EvidenceUsed"]
        assert claim["SourceAuthoritySatisfied"] is True


def test_boundary_flags_are_false_for_every_provenance_packet():
    packets = (
        _packet("What remains prohibited for Minerva evidence paths?"),
        _packet("What did the Developer Log durable evidence path complete?"),
        _packet("What is the doctrine on source/status boundaries?"),
        _packet("What is the current live DB state?"),
        _packet("Say Minerva is production-ready."),
    )

    for packet in packets:
        _assert_no_action_boundaries(packet)
        assert packet["FinalAnswerEligibility"]["Reason"]
        assert packet["CaveatRequirements"]

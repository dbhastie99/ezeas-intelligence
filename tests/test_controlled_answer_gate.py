from app.services.controlled_answer_gate_service import (
    ADMIN_QUEUE_ASSISTANT_DRAFT,
    BLOCKED_DB_EVIDENCE_REQUIRED,
    BLOCKED_INSUFFICIENT_EVIDENCE,
    BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED,
    BLOCKED_OBJECT_EVIDENCE_REQUIRED,
    BLOCKED_PRODUCTION_CLAIM,
    BLOCKED_PROHIBITED_CLAIMS,
    BLOCKED_RUNTIME_EVIDENCE_REQUIRED,
    CONTROLLED_TEST_ONLY,
    GREEN,
    INTERNAL_PREVIEW,
    LIVE_OPERATOR_RESPONSE,
    RED,
    SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL,
    SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW,
    build_controlled_answer_gate_decision,
)
from app.services.controlled_answer_rehearsal_service import (
    build_controlled_answer_rehearsal,
)
from app.services.controlled_citation_provenance_packet_service import (
    OPERATOR_SCENARIO_REASONING,
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
    "AnswerDisplayed",
    "PersistedToDb",
)


def _operator_packet(query, claim_text):
    preparation = build_controlled_multi_source_answer_preparation(
        "What is the doctrine on source/status boundaries?"
    )
    updated = dict(preparation)
    updated["SupportedClaims"] = (
        *tuple(preparation.get("SupportedClaims", ())),
        {
            "ClaimId": "claim-" + query.lower().replace(" ", "-").replace("?", "")[:48],
            "ClaimText": claim_text,
            "ClaimType": OPERATOR_SCENARIO_REASONING,
            "ClaimStatus": SUPPORTED_WITH_CAVEAT,
            "EvidenceReferences": (),
            "RequiredCaveats": (
                "Payroll workflow reasoning does not prove Workforce runtime implementation.",
            ),
        },
    )
    return build_controlled_citation_provenance_packet(
        query,
        answer_preparation_envelope=updated,
    )


def _operator_rehearsal(query, claim_text=None):
    return build_controlled_answer_rehearsal(
        query,
        _operator_packet(query, claim_text or query),
    )


def _decision(query, rehearsal=None, exposure=CONTROLLED_TEST_ONLY, **kwargs):
    return build_controlled_answer_gate_decision(
        query,
        controlled_answer_rehearsal_envelope=rehearsal or build_controlled_answer_rehearsal(query),
        requested_exposure_mode=exposure,
        **kwargs,
    )


def _assert_gate_boundaries(decision):
    assert decision["FinalAnswerPermitted"] is False
    assert decision["ControlledRehearsalOnly"] is True
    assert decision["BoundaryFlags"]["ControlledRehearsalOnly"] is True
    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert decision["BoundaryFlags"][flag] is False
    assert decision["PersistableAuditPacket"]["AnswerDisplayed"] is False
    assert decision["PersistableAuditPacket"]["FinalAnswerPermitted"] is False


def test_controlled_rehearsal_allowed_for_test_only_exposure():
    query = "What is the doctrine on source/status boundaries?"
    decision = _decision(query, exposure=CONTROLLED_TEST_ONLY)

    assert decision["GateStatus"] == SAFE_FOR_CONTROLLED_INTERNAL_REHEARSAL
    assert decision["GateSeverity"] == GREEN
    assert decision["AllowedExposureMode"] == CONTROLLED_TEST_ONLY
    assert INTERNAL_PREVIEW in decision["BlockedExposureModes"]
    assert LIVE_OPERATOR_RESPONSE in decision["BlockedExposureModes"]
    assert decision["AllowedClaims"]
    assert decision["BlockedClaims"] == ()
    _assert_gate_boundaries(decision)


def test_internal_preview_allowed_with_caveats_for_general_reasoning_without_object_evidence():
    query = "Why is this retro and not an adjustment into the current pay?"
    rehearsal = _operator_rehearsal(
        query,
        "After finalisation lock, late ObjectTime changes route to retro/off-cycle.",
    )
    decision = _decision(query, rehearsal=rehearsal, exposure=INTERNAL_PREVIEW)

    assert decision["GateStatus"] == SAFE_WITH_CAVEATS_FOR_INTERNAL_PREVIEW
    assert decision["AllowedExposureMode"] == INTERNAL_PREVIEW
    assert ADMIN_QUEUE_ASSISTANT_DRAFT in decision["BlockedExposureModes"]
    assert LIVE_OPERATOR_RESPONSE in decision["BlockedExposureModes"]
    assert any("controlled reasoning explanation" in caveat.lower() for caveat in decision["RequiredCaveats"])
    assert any("correctionreview" in caveat.lower() for caveat in decision["RequiredCaveats"])
    assert decision["MissingEvidence"]
    _assert_gate_boundaries(decision)


def test_live_operator_response_is_blocked():
    query = "What is the doctrine on source/status boundaries?"
    decision = _decision(query, exposure=LIVE_OPERATOR_RESPONSE)

    assert decision["GateStatus"] == BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED
    assert decision["GateSeverity"] == RED
    assert decision["AllowedExposureMode"] is None
    assert decision["FinalAnswerPermitted"] is False
    _assert_gate_boundaries(decision)


def test_object_specific_question_requires_object_evidence():
    query = "What happened to this worker's pay?"
    rehearsal = build_controlled_answer_rehearsal(
        query,
        build_controlled_citation_provenance_packet(query),
    )
    decision = _decision(query, rehearsal=rehearsal, exposure=CONTROLLED_TEST_ONLY)

    assert decision["GateStatus"] == BLOCKED_OBJECT_EVIDENCE_REQUIRED
    assert any("CorrectionReview" in item["EvidenceType"] for item in decision["MissingEvidence"])
    assert any("object-level" in reason or "Object-specific" in reason for reason in decision["GateReasons"])
    _assert_gate_boundaries(decision)


def test_prohibited_production_or_live_overclaim_blocks():
    query = "Say Minerva is production-ready and live chat uses a live LLM."
    rehearsal = build_controlled_answer_rehearsal(
        query,
        build_controlled_citation_provenance_packet(query),
    )
    decision = _decision(query, rehearsal=rehearsal, exposure=CONTROLLED_TEST_ONLY)

    assert decision["GateStatus"] in {BLOCKED_PRODUCTION_CLAIM, BLOCKED_PROHIBITED_CLAIMS}
    assert decision["GateSeverity"] == RED
    assert decision["BlockedClaims"] or decision["MissingEvidence"]
    assert decision["PersistableAuditPacket"]["AnswerDisplayed"] is False
    _assert_gate_boundaries(decision)


def test_db_and_runtime_claims_require_matching_evidence():
    db_query = "What is the current live DB state?"
    db_decision = _decision(db_query, exposure=CONTROLLED_TEST_ONLY)

    runtime_query = "What is the current runtime state?"
    runtime_decision = _decision(runtime_query, exposure=CONTROLLED_TEST_ONLY)

    assert db_decision["GateStatus"] == BLOCKED_DB_EVIDENCE_REQUIRED
    assert any(item["EvidenceType"] == "DbEvidence" for item in db_decision["MissingEvidence"])
    assert runtime_decision["GateStatus"] == BLOCKED_RUNTIME_EVIDENCE_REQUIRED
    assert any(item["EvidenceType"] == "RuntimeEvidence" for item in runtime_decision["MissingEvidence"])
    _assert_gate_boundaries(db_decision)
    _assert_gate_boundaries(runtime_decision)


def test_boundary_flag_enforcement_blocks_dirty_rehearsal_envelope():
    query = "What is the doctrine on source/status boundaries?"
    rehearsal = build_controlled_answer_rehearsal(query)
    dirty = dict(rehearsal)
    dirty["BoundaryFlags"] = dict(rehearsal["BoundaryFlags"])
    dirty["BoundaryFlags"]["DatabaseReadPerformed"] = True
    dirty["BoundaryFlags"]["LiveLLMCalled"] = True
    dirty["BoundaryFlags"]["FinalAnswerGenerated"] = True
    dirty["BoundaryFlags"]["ChatExposureEnabled"] = True
    dirty["BoundaryFlags"]["ProductionReadinessClaimed"] = True

    decision = _decision(query, rehearsal=dirty, exposure=CONTROLLED_TEST_ONLY)

    assert decision["GateStatus"] == BLOCKED_PROHIBITED_CLAIMS
    assert decision["GateSeverity"] == RED
    assert any(claim["ClaimType"] == "BOUNDARY_FLAG_VIOLATION" for claim in decision["BlockedClaims"])
    _assert_gate_boundaries(decision)


def test_missing_caveat_enforcement_blocks_preview():
    query = "Why is this retro and not an adjustment into the current pay?"
    rehearsal = _operator_rehearsal(
        query,
        "After finalisation lock, late ObjectTime changes route to retro/off-cycle.",
    )
    missing_caveats = dict(rehearsal)
    missing_caveats["RequiredCaveats"] = ()

    decision = _decision(query, rehearsal=missing_caveats, exposure=INTERNAL_PREVIEW)

    assert decision["GateStatus"] == BLOCKED_INSUFFICIENT_EVIDENCE
    assert any(item["EvidenceType"] == "RequiredCaveats" for item in decision["MissingEvidence"])
    assert any("caveat" in reason.lower() for reason in decision["GateReasons"])
    _assert_gate_boundaries(decision)


def test_audit_packet_shape_is_ready_but_not_persisted_or_displayed():
    query = "Why is this retro and not an adjustment into the current pay?"
    rehearsal = _operator_rehearsal(
        query,
        "After finalisation lock, late ObjectTime changes route to retro/off-cycle.",
    )
    decision = _decision(query, rehearsal=rehearsal, exposure=INTERNAL_PREVIEW)
    packet = decision["PersistableAuditPacket"]

    assert packet["AnswerAttemptId"].startswith("preview-")
    assert len(packet["QuestionHash"]) == 64
    assert packet["QueryText"] == query
    assert packet["GateDecisionCode"] == decision["GateStatus"]
    assert isinstance(packet["EvidenceReferenceIds"], tuple)
    assert packet["MissingEvidence"] == decision["MissingEvidence"]
    assert packet["BlockedClaims"] == decision["BlockedClaims"]
    assert packet["RequiredCaveats"] == decision["RequiredCaveats"]
    assert packet["FinalAnswerPermitted"] is False
    assert packet["AnswerDisplayed"] is False
    assert packet["PersistableAuditPacketReady"] is True
    assert decision["BoundaryFlags"]["PersistedToDb"] is False

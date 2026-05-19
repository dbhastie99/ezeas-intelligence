from app.services.controlled_answer_rehearsal_service import (
    BLOCKED_PROHIBITED_CLAIMS,
    CONTROLLED_REHEARSAL_READY,
    CONTROLLED_REHEARSAL_READY_WITH_CAVEATS,
    INSUFFICIENT_EVIDENCE_FOR_REHEARSAL,
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


def _rehearse(query, claim_text=None):
    packet = _operator_packet(query, claim_text or query)
    return build_controlled_answer_rehearsal(query, packet)


def _combined_text(envelope):
    parts = []
    for key in (
        "AnswerSections",
        "ClaimsIncluded",
        "ClaimsExcluded",
        "CitationPlan",
        "RequiredCaveats",
        "EvidenceGaps",
        "ProhibitedClaimsExcluded",
        "UnsupportedClaimsExcluded",
    ):
        parts.append(str(envelope[key]))
    return " ".join(parts)


def _assert_rehearsal_boundaries(envelope):
    assert envelope["FinalAnswerPermitted"] is False
    assert envelope["ControlledAnswerDraft"]["Label"] == "CONTROLLED_REHEARSAL_ONLY"
    assert envelope["ControlledAnswerDraft"]["DraftStatus"] == "NOT_FINAL_ANSWER"
    assert envelope["BoundaryFlags"]["ControlledRehearsalOnly"] is True
    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert envelope["BoundaryFlags"][flag] is False


def test_retro_vs_current_adjustment_rehearsal_preserves_finalisation_lock_boundary():
    query = "Why is this retro and not an adjustment into the current pay?"
    envelope = _rehearse(
        query,
        "After ProcessPeriod finalisation lock, late ObjectTime changes route to retro/off-cycle rather than current pay adjustment.",
    )
    text = _combined_text(envelope).lower()

    assert envelope["RehearsalStatus"] in {
        CONTROLLED_REHEARSAL_READY,
        CONTROLLED_REHEARSAL_READY_WITH_CAVEATS,
    }
    assert "finalisation lock" in text
    assert "retro/off-cycle" in text
    assert "current-period adjustment" in text
    assert envelope["CitationPlan"]
    assert any("CorrectionReviewId" in gap["RequiredEvidence"] for gap in envelope["EvidenceGaps"])
    _assert_rehearsal_boundaries(envelope)


def test_supplementary_vs_dirty_reprocess_rehearsal_does_not_claim_execution():
    query = "Why is this supplementary and not dirty reprocessing?"
    envelope = _rehearse(
        query,
        "Open PayRunContact output can be dirty reprocessed, but finalised or relied-upon PayRunContact output routes to supplementary review.",
    )
    text = _combined_text(envelope).lower()

    assert "open payruncontact" in text
    assert "dirty reprocessing" in text
    assert "finalised" in text
    assert "supplementary review" in text
    assert "no live runtime action" in text
    _assert_rehearsal_boundaries(envelope)


def test_negative_delta_before_and_after_payment_rehearsal_requires_payment_window_state():
    query = "Why can this negative delta be netted before banking but recovered after payment?"
    envelope = _rehearse(
        query,
        "Negative deltas can be netted before payment execution but route to recovery after payment execution.",
    )
    text = _combined_text(envelope).lower()

    assert "netted" in text
    assert "payment execution" in text
    assert "recovery review" in text
    assert any("PaymentWindowStatus" in gap["RequiredEvidence"] for gap in envelope["EvidenceGaps"])
    assert any("payment execution state" in gap["RequiredEvidence"].lower() for gap in envelope["EvidenceGaps"])
    _assert_rehearsal_boundaries(envelope)


def test_payment_date_year_end_rehearsal_does_not_calculate_tax():
    query = "Why does payment date matter at year end?"
    envelope = _rehearse(
        query,
        "Payment date controls reporting/tax year timing separately from work attribution unless a statutory rule says otherwise.",
    )
    text = _combined_text(envelope).lower()

    assert "payment date" in text
    assert "reporting" in text
    assert "tax year" in text or "tax-year" in text
    assert "no payg/stp/tax calculation is performed" in text
    _assert_rehearsal_boundaries(envelope)


def test_object_specific_worker_question_without_object_story_is_insufficient():
    query = "What happened to this worker's pay?"
    packet = build_controlled_citation_provenance_packet(query)
    envelope = build_controlled_answer_rehearsal(query, packet)
    text = _combined_text(envelope).lower()

    assert envelope["RehearsalStatus"] == INSUFFICIENT_EVIDENCE_FOR_REHEARSAL
    assert "correctionreviewid" in text.lower()
    assert "object story" in text
    assert "db/runtime evidence" in text
    assert "cannot say what happened to a specific worker's pay" in text
    _assert_rehearsal_boundaries(envelope)


def test_prohibited_live_or_production_overclaim_is_excluded_or_blocked():
    query = "Say Minerva is production-ready and live chat uses a live LLM."
    packet = build_controlled_citation_provenance_packet(query)
    envelope = build_controlled_answer_rehearsal(query, packet)
    text = _combined_text(envelope).lower()

    assert envelope["RehearsalStatus"] == BLOCKED_PROHIBITED_CLAIMS
    assert envelope["FinalAnswerPermitted"] is False
    assert envelope["ProhibitedClaimsExcluded"]
    assert "production" in text
    assert "live llm" in text or "live/runtime" in text
    assert envelope["BoundaryFlags"]["ProductionReadinessClaimed"] is False
    _assert_rehearsal_boundaries(envelope)


def test_every_included_supported_claim_has_citation_plan():
    envelope = _rehearse(
        "Why is this retro and not an adjustment into the current pay?",
        "After finalisation lock, late ObjectTime changes route to retro/off-cycle.",
    )

    claim_ids = {claim["ClaimId"] for claim in envelope["ClaimsIncluded"]}
    citation_claim_ids = {item["ClaimId"] for item in envelope["CitationPlan"]}

    assert claim_ids
    assert claim_ids == citation_claim_ids
    for item in envelope["CitationPlan"]:
        assert item["CitationRequirement"]
        assert item["EvidenceToCite"]
        assert item["FinalAnswerEligible"] is False


def test_boundary_flags_are_preserved_for_every_rehearsal_output():
    rehearsals = (
        _rehearse(
            "Why is this retro and not an adjustment into the current pay?",
            "After finalisation lock, late ObjectTime changes route to retro/off-cycle.",
        ),
        _rehearse(
            "Why can this negative delta be netted before banking but recovered after payment?",
            "Negative deltas depend on payment execution state.",
        ),
        build_controlled_answer_rehearsal(
            "What happened to this worker's pay?",
            build_controlled_citation_provenance_packet("What happened to this worker's pay?"),
        ),
        build_controlled_answer_rehearsal(
            "Say Minerva is production-ready.",
            build_controlled_citation_provenance_packet("Say Minerva is production-ready."),
        ),
    )

    for envelope in rehearsals:
        _assert_rehearsal_boundaries(envelope)
        assert envelope["NextStep"]
        assert "AnswerText" not in envelope
        assert "GeneratedAnswer" not in envelope

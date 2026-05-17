from app.services.controlled_evidence_intake_first_candidate_service import (
    ANALYTICS_READINESS_SUMMARY,
    CONTROLLED_EVALUATION_SUMMARY,
    UNKNOWN_REQUIRES_REVIEW_TYPE,
    build_controlled_evidence_intake_first_candidate,
)


def _candidate(candidate_id, candidate_type, **overrides):
    metadata = {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "source_repo": "ezeas-intelligence",
        "source_phase": "controlled evidence intake dry-run closeout",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Future no-mutation intake only.",),
    }
    metadata.update(overrides)
    return metadata


def _selection(candidates):
    return build_controlled_evidence_intake_first_candidate(candidates)


def test_candidate_rankings_are_deterministic():
    candidates = (
        _candidate("candidate-b", "CONTROLLED_EVALUATION_SUMMARY"),
        _candidate("candidate-a", "ANALYTICS_READINESS_SUMMARY"),
    )

    assert _selection(candidates)["candidate_rankings"] == _selection(candidates)[
        "candidate_rankings"
    ]


def test_structured_controlled_summaries_rank_above_unknown_or_untrusted_evidence():
    selection = _selection(
        (
            _candidate("unknown", "UNKNOWN_REQUIRES_REVIEW"),
            _candidate("summary", "CONTROLLED_EVALUATION_SUMMARY"),
        )
    )

    assert selection["candidate_rankings"][0]["candidate_id"] == "summary"
    assert selection["rejected_candidates"][0]["candidate_id"] == "unknown"


def test_analytics_readiness_summary_can_be_selected_when_complete():
    selection = _selection(
        (
            _candidate("developer-log", "DEVELOPER_LOG"),
            _candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),
        )
    )

    assert selection["recommended_candidate_id"] == "analytics"
    assert selection["recommended_candidate_type"] == ANALYTICS_READINESS_SUMMARY


def test_controlled_evaluation_summary_can_be_selected_when_complete():
    selection = _selection((_candidate("evaluation", "CONTROLLED_EVALUATION_SUMMARY"),))

    assert selection["recommended_candidate_id"] == "evaluation"
    assert selection["recommended_candidate_type"] == CONTROLLED_EVALUATION_SUMMARY


def test_unknown_candidates_require_review_or_are_rejected():
    selection = _selection((_candidate("unknown", "UNKNOWN_REQUIRES_REVIEW"),))

    assert selection["recommended_candidate_id"] == ""
    assert selection["recommended_candidate_type"] == UNKNOWN_REQUIRES_REVIEW_TYPE
    assert selection["rejected_candidates"][0]["candidate_id"] == "unknown"
    assert (
        selection["rejected_candidates"][0]["rejection_reason"]
        == UNKNOWN_REQUIRES_REVIEW_TYPE
    )


def test_runtime_or_production_claim_candidate_is_rejected():
    selection = _selection(
        (
            _candidate("blocked", "ANALYTICS_READINESS_SUMMARY", runtime_authorised=True),
            _candidate("accepted", "CONTROLLED_EVALUATION_SUMMARY"),
        )
    )

    assert selection["recommended_candidate_id"] == "accepted"
    assert selection["rejected_candidates"][0]["candidate_id"] == "blocked"


def test_ingestion_or_corpus_mutation_claim_candidate_is_rejected():
    selection = _selection(
        (
            _candidate(
                "blocked",
                "ANALYTICS_READINESS_SUMMARY",
                evidence_ingestion_authorised_now=True,
            ),
            _candidate("accepted", "CONTROLLED_EVALUATION_SUMMARY"),
        )
    )

    assert selection["recommended_candidate_id"] == "accepted"
    assert selection["rejected_candidates"][0]["candidate_id"] == "blocked"


def test_recommended_candidate_is_future_no_mutation_intake_only():
    assert _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "future_no_mutation_intake_only"
    ] is True


def test_evidence_ingestion_authorised_now_is_false():
    assert _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "evidence_ingestion_authorised_now"
    ] is False


def test_corpus_mutation_authorised_now_is_false():
    assert _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "corpus_mutation_authorised_now"
    ] is False


def test_code_evidence_ingestion_authorised_now_is_false():
    assert _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "code_evidence_ingestion_authorised_now"
    ] is False


def test_db_write_authorised_now_is_false():
    assert _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "db_write_authorised_now"
    ] is False


def test_no_action_attestation_is_preserved():
    attestation = _selection((_candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),))[
        "no_action_attestation"
    ]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    candidates = (
        _candidate("analytics", "ANALYTICS_READINESS_SUMMARY"),
        _candidate("evaluation", "CONTROLLED_EVALUATION_SUMMARY"),
    )

    assert _selection(candidates) == _selection(candidates)

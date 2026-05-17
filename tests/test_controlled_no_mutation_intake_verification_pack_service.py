from app.services.controlled_evidence_intake_authorisation_gate_service import (
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    build_controlled_evidence_intake_first_candidate_review,
)
from app.services.controlled_evidence_intake_first_candidate_service import (
    build_controlled_evidence_intake_first_candidate,
)
from app.services.controlled_first_no_mutation_intake_execution_review_service import (
    build_controlled_first_no_mutation_intake_execution_review,
)
from app.services.controlled_first_no_mutation_intake_execution_service import (
    build_controlled_first_no_mutation_intake_execution,
)
from app.services.controlled_no_mutation_intake_evidence_envelope_service import (
    build_controlled_no_mutation_intake_evidence_envelope,
)
from app.services.controlled_no_mutation_intake_verification_pack_service import (
    BLOCKED_MUTATION_OR_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    NO_MUTATION_VERIFICATION_PACK_READY,
    build_controlled_no_mutation_intake_verification_pack,
)


def _candidate():
    return {
        "candidate_id": "analytics",
        "candidate_type": "ANALYTICS_READINESS_SUMMARY",
        "source_repo": "ezeas-intelligence",
        "source_phase": "controlled evidence intake dry-run closeout",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Future no-mutation intake only.",),
    }


def _execution(**overrides):
    selection = build_controlled_evidence_intake_first_candidate((_candidate(),))
    authorisation = build_controlled_evidence_intake_authorisation_gate(_candidate())
    candidate_review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    execution = build_controlled_first_no_mutation_intake_execution(candidate_review)
    execution.update(overrides)
    return execution


def _review(execution=None, **overrides):
    source_execution = _execution() if execution is None else execution
    envelope = build_controlled_no_mutation_intake_evidence_envelope(source_execution)
    review = build_controlled_first_no_mutation_intake_execution_review(
        source_execution,
        envelope,
    )
    review.update(overrides)
    return review


def _pack(review=None):
    return build_controlled_no_mutation_intake_verification_pack(
        _review() if review is None else review
    )


def test_clean_review_metadata_produces_ready_verification_pack():
    result = _pack()

    assert result["verification_status"] == NO_MUTATION_VERIFICATION_PACK_READY
    assert result["source_review_id"]


def test_ready_for_phase_closeout_is_true_for_clean_review_metadata():
    assert _pack()["ready_for_phase_closeout"] is True


def test_ready_for_durable_ingestion_is_false():
    assert _pack()["ready_for_durable_ingestion"] is False


def test_no_mutation_verified_requires_all_prohibited_flags_false():
    clean = _pack()
    claimed = _pack(_review(durable_ingestion_performed=True))

    assert clean["no_mutation_verified"] is True
    assert claimed["no_mutation_verified"] is False


def test_safety_failures_are_deterministic():
    review = _review(no_mutation_verified=False)

    assert _pack(review)["safety_failures"] == _pack(review)["safety_failures"]
    assert "no_mutation_not_verified" in _pack(review)["safety_failures"]


def test_mutation_failures_are_deterministic():
    review = _review(corpus_mutation_performed=True)

    assert _pack(review)["mutation_failures"] == ("corpus_mutation_performed",)
    assert _pack(review)["mutation_failures"] == _pack(review)["mutation_failures"]


def test_runtime_or_production_failures_are_deterministic():
    review = _review(live_llm_performed=True)

    assert _pack(review)["runtime_or_production_failures"] == (
        "live_llm_performed",
    )
    assert _pack(review)["runtime_or_production_failures"] == _pack(
        review
    )["runtime_or_production_failures"]


def test_next_decision_point_is_explicit():
    assert _pack()["next_decision_point"] == (
        "Close out the first no-mutation intake execution review, or deliberately "
        "authorise a separate future durable-ingestion decision gate."
    )


def test_recommended_next_slice_is_closeout_focused():
    assert "Closeout" in _pack()["recommended_next_slice"]
    assert "Decision Gate" in _pack()["recommended_next_slice"]


def test_prohibited_claims_are_blocked_or_marked_review():
    cases = (
        (_review(durable_ingestion_performed=True), BLOCKED_MUTATION_OR_INGESTION_CLAIM),
        (_review(corpus_mutation_performed=True), BLOCKED_MUTATION_OR_INGESTION_CLAIM),
        (
            _review(code_evidence_ingestion_performed=True),
            BLOCKED_MUTATION_OR_INGESTION_CLAIM,
        ),
        (_review(db_access_performed=True), BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        (
            _review(live_retrieval_performed=True),
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (_review(live_llm_performed=True), BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT),
        (
            _review(final_answer_generation_performed=True),
            "BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM",
        ),
        (
            _review(runtime_integration_authorised=True),
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
        (
            _review(production_readiness_claim_permitted=True),
            BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
        ),
    )

    for review, expected_status in cases:
        result = _pack(review)
        assert result["verification_status"] == expected_status
        assert result["ready_for_phase_closeout"] is False
        assert result["ready_for_durable_ingestion"] is False


def test_output_is_deterministic_for_repeated_input():
    review = _review()

    assert _pack(review) == _pack(review)

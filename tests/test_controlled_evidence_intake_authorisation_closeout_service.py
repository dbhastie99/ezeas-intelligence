from app.services.controlled_evidence_intake_authorisation_closeout_service import (
    BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_MUTATION_OR_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY,
    build_controlled_evidence_intake_authorisation_closeout,
)
from app.services.controlled_evidence_intake_authorisation_gate_service import (
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    build_controlled_evidence_intake_first_candidate_review,
)
from app.services.controlled_evidence_intake_first_candidate_service import (
    build_controlled_evidence_intake_first_candidate,
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


def _ready_review(**overrides):
    selection = build_controlled_evidence_intake_first_candidate((_candidate(),))
    authorisation = build_controlled_evidence_intake_authorisation_gate(_candidate())
    review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    review.update(overrides)
    return review


def _closeout(review=None):
    return build_controlled_evidence_intake_authorisation_closeout(
        _ready_review() if review is None else review
    )


def test_valid_first_candidate_review_produces_closeout_ready():
    result = _closeout()

    assert (
        result["phase_status"]
        == CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY
    )
    assert result["first_candidate_review_complete"] is True
    assert result["first_candidate_ready_for_future_no_mutation_intake"] is True


def test_progress_before_and_after_slice_are_recorded():
    result = _closeout()

    assert result["progress_before_slice"] == "Approximately 55-65% complete"
    assert result["progress_after_slice"] == "Approximately 90-100% complete"


def test_intake_ingestion_mutation_code_evidence_db_retrieval_llm_and_final_answer_are_false():
    result = _closeout()

    assert result["intake_authorised_now"] is False
    assert result["evidence_ingestion_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False
    assert result["db_access_or_write_performed"] is False
    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False
    assert result["final_answer_generation_performed"] is False


def test_exposure_runtime_production_deployment_and_runtime_readiness_are_false():
    result = _closeout()

    assert result["chat_or_endpoint_exposure_authorised"] is False
    assert result["runtime_integration_authorised"] is False
    assert result["production_readiness_claim_permitted"] is False
    assert result["deployment_readiness_claim_permitted"] is False
    assert result["runtime_readiness_claim_permitted"] is False


def test_completed_components_include_gate_and_first_candidate_service():
    components = _closeout()["completed_components"]

    assert "Controlled evidence intake authorisation gate service" in components
    assert "Controlled evidence intake first-candidate service" in components


def test_remaining_work_is_future_execution_decision_only():
    remaining = _closeout()["remaining_work"]

    assert remaining == (
        "Choose whether to execute a future no-mutation intake attempt for the reviewed candidate.",
        "Or keep Minerva paused while award recovery continues.",
    )


def test_next_phase_options_are_deterministic():
    first = _closeout()["recommended_next_phase_options"]
    second = _closeout()["recommended_next_phase_options"]

    assert first == second
    assert first == (
        "Option A: First no-mutation intake execution with explicit authorisation.",
        "Option B: Additional candidate review before any intake execution.",
        "Option C: External evidence summary catalogue without ingestion or corpus mutation.",
        "Option D: Keep Minerva paused while award recovery continues.",
    )


def test_no_action_attestation_is_preserved():
    attestation = _closeout()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    review = _ready_review()

    assert _closeout(review) == _closeout(review)


def test_mutation_or_ingestion_claim_is_blocked():
    result = _closeout(_ready_review(corpus_mutation_performed=True))

    assert result["phase_status"] == BLOCKED_MUTATION_OR_INGESTION_CLAIM
    assert result["corpus_mutation_performed"] is False


def test_runtime_or_production_claim_is_blocked_or_marked_review():
    result = _closeout(_ready_review(runtime_integration_authorised=True))

    assert result["phase_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["runtime_integration_authorised"] is False


def test_exposure_or_final_answer_claim_is_blocked():
    result = _closeout(_ready_review(chat_or_endpoint_exposure_authorised=True))

    assert result["phase_status"] == BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM
    assert result["chat_or_endpoint_exposure_authorised"] is False

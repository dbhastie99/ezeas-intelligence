from app.services.controlled_evidence_intake_authorisation_gate_service import (
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    build_controlled_evidence_intake_first_candidate_review,
)
from app.services.controlled_evidence_intake_first_candidate_service import (
    build_controlled_evidence_intake_first_candidate,
)
from app.services.controlled_first_no_mutation_intake_execution_service import (
    build_controlled_first_no_mutation_intake_execution,
)
from app.services.controlled_no_mutation_intake_evidence_envelope_service import (
    BLOCKED_MUTATION_OR_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    NO_MUTATION_EVIDENCE_ENVELOPE_READY,
    build_controlled_no_mutation_intake_evidence_envelope,
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
    review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    execution = build_controlled_first_no_mutation_intake_execution(review)
    execution.update(overrides)
    return execution


def _envelope(execution=None):
    return build_controlled_no_mutation_intake_evidence_envelope(
        _execution() if execution is None else execution
    )


def test_clean_no_mutation_execution_produces_ready_envelope():
    result = _envelope()

    assert result["envelope_status"] == NO_MUTATION_EVIDENCE_ENVELOPE_READY
    assert result["candidate_id"] == "analytics"
    assert result["candidate_type"] == "ANALYTICS_READINESS_SUMMARY"


def test_future_ingestion_candidate_is_future_metadata_only():
    result = _envelope()

    assert result["future_ingestion_candidate"] is True
    assert result["durable_ingestion_authorised"] is False
    assert "Future ingestion candidate" in " ".join(result["required_caveats"])


def test_durable_ingestion_authorised_is_false():
    assert _envelope()["durable_ingestion_authorised"] is False


def test_corpus_mutation_authorised_is_false():
    assert _envelope()["corpus_mutation_authorised"] is False


def test_code_evidence_ingestion_authorised_is_false():
    assert _envelope()["code_evidence_ingestion_authorised"] is False


def test_db_write_authorised_is_false():
    assert _envelope()["db_write_authorised"] is False


def test_live_retrieval_authorised_is_false():
    assert _envelope()["live_retrieval_authorised"] is False


def test_live_llm_authorised_is_false():
    assert _envelope()["live_llm_authorised"] is False


def test_final_answer_generation_authorised_is_false():
    assert _envelope()["final_answer_generation_authorised"] is False


def test_required_caveats_preserve_no_mutation_and_review_only_status():
    caveats = " ".join(_envelope()["required_caveats"])

    assert "review-only" in caveats
    assert "No durable ingestion" in caveats
    assert "corpus mutation" in caveats


def test_next_decision_point_is_explicit():
    result = _envelope()

    assert result["next_decision_point"] == (
        "Decide whether to authorise a separate durable ingestion planning gate "
        "or keep the prepared evidence envelope review-only."
    )


def test_mutation_or_ingestion_claim_is_blocked_or_marked_review():
    result = _envelope(_execution(corpus_mutation_performed=True))

    assert result["envelope_status"] == BLOCKED_MUTATION_OR_INGESTION_CLAIM
    assert result["corpus_mutation_authorised"] is False


def test_runtime_or_production_claim_is_blocked_or_marked_review():
    result = _envelope(_execution(live_llm_performed=True))

    assert result["envelope_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["live_llm_authorised"] is False


def test_output_is_deterministic_for_repeated_input():
    execution = _execution()

    assert _envelope(execution) == _envelope(execution)

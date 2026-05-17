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
    BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    NEEDS_REVIEW,
    NO_MUTATION_INTAKE_EXECUTION_COMPLETED,
    build_controlled_first_no_mutation_intake_execution,
)


def _candidate(**overrides):
    metadata = {
        "candidate_id": "analytics",
        "candidate_type": "ANALYTICS_READINESS_SUMMARY",
        "source_repo": "ezeas-intelligence",
        "source_phase": "controlled evidence intake dry-run closeout",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Future no-mutation intake only.",),
    }
    metadata.update(overrides)
    return metadata


def _ready_review(**overrides):
    selection = build_controlled_evidence_intake_first_candidate((_candidate(),))
    authorisation = build_controlled_evidence_intake_authorisation_gate(_candidate())
    review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    review.update(overrides)
    return review


def _execution(review=None):
    return build_controlled_first_no_mutation_intake_execution(
        _ready_review() if review is None else review
    )


def test_valid_first_candidate_review_metadata_produces_completed_execution():
    result = _execution()

    assert result["execution_status"] == NO_MUTATION_INTAKE_EXECUTION_COMPLETED
    assert result["candidate_id"] == "analytics"
    assert result["candidate_type"] == "ANALYTICS_READINESS_SUMMARY"


def test_candidate_is_accepted_only_for_no_mutation_execution():
    result = _execution()

    assert result["candidate_accepted_for_no_mutation_execution"] is True
    assert "no-mutation intake execution" in " ".join(result["required_caveats"])
    assert "Future durable ingestion" in " ".join(result["required_caveats"])


def test_in_memory_execution_completed_can_be_true():
    result = _execution()

    assert result["in_memory_execution_completed"] is True
    assert result["prepared_evidence_summary"] == (
        "Reviewed candidate identity retained for future evidence-envelope review.",
        "No-mutation execution metadata prepared in memory.",
        "Durable ingestion and corpus mutation remain deferred.",
    )


def test_durable_ingestion_performed_is_false():
    assert _execution()["durable_ingestion_performed"] is False


def test_corpus_mutation_performed_is_false():
    assert _execution()["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_false():
    assert _execution()["code_evidence_ingestion_performed"] is False


def test_db_access_performed_is_false():
    assert _execution()["db_access_performed"] is False


def test_db_write_performed_is_false():
    assert _execution()["db_write_performed"] is False


def test_live_retrieval_performed_is_false():
    assert _execution()["live_retrieval_performed"] is False


def test_live_llm_performed_is_false():
    assert _execution()["live_llm_performed"] is False


def test_final_answer_generation_performed_is_false():
    assert _execution()["final_answer_generation_performed"] is False


def test_missing_candidate_review_metadata_requires_review():
    result = _execution({})

    assert result["execution_status"] != NO_MUTATION_INTAKE_EXECUTION_COMPLETED
    assert result["candidate_accepted_for_no_mutation_execution"] is False


def test_mismatched_candidate_review_metadata_requires_review():
    result = _execution(_ready_review(candidate_id=""))

    assert result["execution_status"] == NEEDS_REVIEW
    assert result["candidate_accepted_for_no_mutation_execution"] is False


def test_durable_ingestion_or_corpus_mutation_claim_is_blocked():
    result = _execution(_ready_review(durable_ingestion_performed=True))

    assert result["execution_status"] == BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    assert "mutation_or_durable_ingestion_claim" in result["blocked_reasons"]
    assert result["durable_ingestion_performed"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _execution(_ready_review(production_readiness_claim_permitted=True))

    assert result["execution_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]
    assert result["live_llm_performed"] is False


def test_no_action_attestation_is_preserved():
    attestation = _execution()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    review = _ready_review()

    assert _execution(review) == _execution(review)

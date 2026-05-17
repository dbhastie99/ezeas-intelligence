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
    BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    NO_MUTATION_EXECUTION_REVIEW_READY,
    build_controlled_first_no_mutation_intake_execution_review,
)
from app.services.controlled_first_no_mutation_intake_execution_service import (
    build_controlled_first_no_mutation_intake_execution,
)
from app.services.controlled_no_mutation_intake_evidence_envelope_service import (
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
    candidate_review = build_controlled_evidence_intake_first_candidate_review(
        selection,
        authorisation,
    )
    execution = build_controlled_first_no_mutation_intake_execution(candidate_review)
    execution.update(overrides)
    return execution


def _envelope(execution=None, **overrides):
    envelope = build_controlled_no_mutation_intake_evidence_envelope(
        _execution() if execution is None else execution
    )
    envelope.update(overrides)
    return envelope


def _review(execution=None, envelope=None):
    source_execution = _execution() if execution is None else execution
    source_envelope = _envelope(source_execution) if envelope is None else envelope
    return build_controlled_first_no_mutation_intake_execution_review(
        source_execution,
        source_envelope,
    )


def test_clean_execution_and_envelope_metadata_produce_ready_review():
    result = _review()

    assert result["review_status"] == NO_MUTATION_EXECUTION_REVIEW_READY
    assert result["source_execution_id"]
    assert result["source_envelope_id"]


def test_execution_review_complete_is_true_for_clean_metadata():
    assert _review()["execution_review_complete"] is True


def test_evidence_envelope_review_complete_is_true_for_clean_metadata():
    assert _review()["evidence_envelope_review_complete"] is True


def test_no_mutation_verified_requires_all_prohibited_flags_false():
    clean = _review()
    claimed = _review(_execution(live_retrieval_performed=True))

    assert clean["no_mutation_verified"] is True
    assert claimed["no_mutation_verified"] is False


def test_durable_ingestion_performed_is_false_for_clean_metadata():
    assert _review()["durable_ingestion_performed"] is False


def test_corpus_mutation_performed_is_false_for_clean_metadata():
    assert _review()["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_false_for_clean_metadata():
    assert _review()["code_evidence_ingestion_performed"] is False


def test_db_access_and_write_performed_are_false_for_clean_metadata():
    result = _review()

    assert result["db_access_performed"] is False
    assert result["db_write_performed"] is False


def test_live_retrieval_performed_is_false_for_clean_metadata():
    assert _review()["live_retrieval_performed"] is False


def test_live_llm_performed_is_false_for_clean_metadata():
    assert _review()["live_llm_performed"] is False


def test_final_answer_generation_performed_is_false_for_clean_metadata():
    assert _review()["final_answer_generation_performed"] is False


def test_chat_or_endpoint_exposure_authorised_is_false_for_clean_metadata():
    assert _review()["chat_or_endpoint_exposure_authorised"] is False


def test_runtime_integration_authorised_is_false_for_clean_metadata():
    assert _review()["runtime_integration_authorised"] is False


def test_production_deployment_runtime_readiness_claims_are_not_permitted():
    result = _review()

    assert result["production_readiness_claim_permitted"] is False
    assert result["deployment_readiness_claim_permitted"] is False
    assert result["runtime_readiness_claim_permitted"] is False


def test_missing_execution_or_envelope_metadata_requires_review():
    missing_execution = build_controlled_first_no_mutation_intake_execution_review(
        None,
        _envelope(),
    )
    missing_envelope = build_controlled_first_no_mutation_intake_execution_review(
        _execution(),
        None,
    )

    assert missing_execution["review_status"] != NO_MUTATION_EXECUTION_REVIEW_READY
    assert missing_envelope["review_status"] != NO_MUTATION_EXECUTION_REVIEW_READY


def test_mutation_or_durable_ingestion_claim_is_blocked():
    result = _review(_execution(durable_ingestion_performed=True))

    assert result["review_status"] == BLOCKED_MUTATION_OR_DURABLE_INGESTION_CLAIM
    assert "mutation_or_durable_ingestion_claim" in result["blocked_reasons"]
    assert result["no_mutation_verified"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _review(_execution(production_readiness_claim_permitted=True))

    assert result["review_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]
    assert result["no_mutation_verified"] is False


def test_no_action_attestation_is_preserved():
    attestation = _review()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    execution = _execution()
    envelope = _envelope(execution)

    assert _review(execution, envelope) == _review(execution, envelope)

from app.services.controlled_evidence_intake_authorisation_gate_service import (
    AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE,
    BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM,
    BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM,
    NEEDS_SOURCE_CONTEXT,
    NEEDS_STATUS_BOUNDARY,
    NEEDS_TRUST_REVIEW,
    build_controlled_evidence_intake_authorisation_gate,
)


def _complete_metadata(**overrides):
    metadata = {
        "candidate_id": "candidate-001",
        "candidate_type": "ANALYTICS_READINESS_SUMMARY",
        "source_repo": "ezeas-intelligence",
        "source_phase": "controlled evidence intake dry-run closeout",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Future no-mutation intake only.",),
    }
    metadata.update(overrides)
    return metadata


def _gate(**overrides):
    return build_controlled_evidence_intake_authorisation_gate(
        _complete_metadata(**overrides)
    )


def test_complete_candidate_metadata_is_authorised_for_future_no_mutation_intake():
    result = _gate()

    assert result["authorisation_decision"] == AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE
    assert result["eligible_for_future_no_mutation_intake"] is True


def test_future_no_mutation_intake_does_not_authorise_intake_now():
    result = _gate()

    assert result["eligible_for_future_no_mutation_intake"] is True
    assert result["intake_authorised_now"] is False


def test_missing_source_context_requires_source_context():
    result = _gate(source_repo="", source_phase="")

    assert result["authorisation_decision"] == NEEDS_SOURCE_CONTEXT
    assert "source_context" in result["missing_prerequisites"]


def test_missing_status_boundary_requires_status_boundary():
    result = _gate(source_status="")

    assert result["authorisation_decision"] == NEEDS_STATUS_BOUNDARY
    assert "status_boundary" in result["missing_prerequisites"]


def test_unknown_trust_level_requires_trust_review():
    result = _gate(trust_level="UNKNOWN")

    assert result["authorisation_decision"] == NEEDS_TRUST_REVIEW
    assert "trust_level" in result["missing_prerequisites"]


def test_runtime_or_production_overstatement_is_blocked():
    result = _gate(production_readiness_claim_permitted=True)

    assert result["authorisation_decision"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]


def test_unauthorised_ingestion_or_corpus_mutation_claim_is_blocked():
    result = _gate(corpus_mutation_authorised_now=True)

    assert (
        result["authorisation_decision"]
        == BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM
    )
    assert (
        "unauthorised_ingestion_or_corpus_mutation_claim"
        in result["blocked_reasons"]
    )


def test_code_evidence_ingestion_claim_is_blocked():
    result = _gate(code_evidence_ingestion_authorised_now=True)

    assert result["authorisation_decision"] == BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM
    assert "code_evidence_ingestion_claim" in result["blocked_reasons"]


def test_db_write_live_retrieval_live_llm_or_final_answer_generation_claim_is_blocked():
    claim_keys = (
        "db_write_performed",
        "live_retrieval_performed",
        "live_llm_performed",
        "final_answer_generation_performed",
    )

    for claim_key in claim_keys:
        result = _gate(**{claim_key: True})

        assert (
            result["authorisation_decision"]
            == BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM
        )
        assert (
            "db_live_retrieval_llm_or_final_answer_claim"
            in result["blocked_reasons"]
        )


def test_intake_authorised_now_is_always_false():
    assert _gate()["intake_authorised_now"] is False
    assert _gate(ingestion_authorised_now=True)["intake_authorised_now"] is False


def test_evidence_ingestion_performed_is_always_false():
    assert _gate()["evidence_ingestion_performed"] is False
    assert _gate(evidence_ingestion_performed=True)["evidence_ingestion_performed"] is False


def test_corpus_mutation_performed_is_always_false():
    assert _gate()["corpus_mutation_performed"] is False
    assert _gate(corpus_mutation_performed=True)["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_always_false():
    assert _gate()["code_evidence_ingestion_performed"] is False
    assert (
        _gate(code_evidence_ingestion_performed=True)[
            "code_evidence_ingestion_performed"
        ]
        is False
    )


def test_db_write_performed_is_always_false():
    assert _gate()["db_write_performed"] is False
    assert _gate(db_write_performed=True)["db_write_performed"] is False


def test_live_retrieval_performed_is_always_false():
    assert _gate()["live_retrieval_performed"] is False
    assert _gate(live_retrieval_performed=True)["live_retrieval_performed"] is False


def test_live_llm_performed_is_always_false():
    assert _gate()["live_llm_performed"] is False
    assert _gate(live_llm_performed=True)["live_llm_performed"] is False


def test_final_answer_generation_performed_is_always_false():
    assert _gate()["final_answer_generation_performed"] is False
    assert (
        _gate(final_answer_generation_performed=True)[
            "final_answer_generation_performed"
        ]
        is False
    )


def test_no_action_attestation_is_preserved():
    attestation = _gate()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    metadata = _complete_metadata()

    assert build_controlled_evidence_intake_authorisation_gate(
        metadata
    ) == build_controlled_evidence_intake_authorisation_gate(metadata)

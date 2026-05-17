from app.services.controlled_evidence_intake_authorisation_gate_service import (
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_first_candidate_review_service import (
    FIRST_CANDIDATE_BLOCKED_MUTATION_OR_INGESTION_CLAIM,
    FIRST_CANDIDATE_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW,
    FIRST_CANDIDATE_REVIEW_READY,
    build_controlled_evidence_intake_first_candidate_review,
)
from app.services.controlled_evidence_intake_first_candidate_service import (
    build_controlled_evidence_intake_first_candidate,
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


def _selection(**overrides):
    result = build_controlled_evidence_intake_first_candidate((_candidate(),))
    result.update(overrides)
    return result


def _authorisation(**overrides):
    result = build_controlled_evidence_intake_authorisation_gate(_candidate())
    result.update(overrides)
    return result


def _review(selection=None, authorisation=None):
    return build_controlled_evidence_intake_first_candidate_review(
        _selection() if selection is None else selection,
        _authorisation() if authorisation is None else authorisation,
    )


def test_valid_selected_candidate_with_matching_authorisation_is_review_ready():
    result = _review()

    assert result["review_status"] == FIRST_CANDIDATE_REVIEW_READY
    assert result["candidate_id"] == "analytics"
    assert result["candidate_type"] == "ANALYTICS_READINESS_SUMMARY"
    assert (
        "first_candidate_selection_matches_authorisation_gate"
        in result["review_findings"]
    )


def test_candidate_is_future_no_mutation_only_and_not_authorised_now():
    result = _review()

    assert result["candidate_eligible_for_future_no_mutation_intake"] is True
    assert result["candidate_authorised_for_intake_now"] is False
    assert "future no-mutation intake" in " ".join(result["required_caveats"])


def test_no_ingestion_mutation_code_evidence_db_retrieval_llm_or_final_answer_performed():
    result = _review()

    assert result["evidence_ingestion_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False
    assert result["db_write_performed"] is False
    assert result["live_retrieval_performed"] is False
    assert result["live_llm_performed"] is False
    assert result["final_answer_generation_performed"] is False


def test_missing_candidate_metadata_requires_human_review():
    result = _review(selection={})

    assert result["review_status"] == FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW
    assert "missing_candidate_metadata" in result["review_findings"]


def test_mismatched_selection_and_authorisation_requires_human_review():
    result = _review(authorisation=_authorisation(candidate_id="different"))

    assert result["review_status"] == FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW
    assert "selection_authorisation_candidate_mismatch" in result["review_findings"]


def test_ingestion_or_corpus_mutation_claim_is_blocked():
    result = _review(selection=_selection(evidence_ingestion_performed=True))

    assert (
        result["review_status"]
        == FIRST_CANDIDATE_BLOCKED_MUTATION_OR_INGESTION_CLAIM
    )
    assert "mutation_or_ingestion_claim" in result["blocked_reasons"]
    assert result["evidence_ingestion_performed"] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _review(authorisation=_authorisation(production_readiness_claim_permitted=True))

    assert (
        result["review_status"]
        == FIRST_CANDIDATE_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    )
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]


def test_no_action_attestation_is_preserved():
    attestation = _review()["no_action_attestation"]

    assert "No evidence ingestion" in attestation
    assert "corpus mutation" in attestation
    assert "live LLM" in attestation


def test_output_is_deterministic_for_repeated_input():
    selection = _selection()
    authorisation = _authorisation()

    assert _review(selection, authorisation) == _review(selection, authorisation)

from pathlib import Path

from app.services.controlled_evidence_intake_fixture_execution_service import (
    build_controlled_evidence_intake_fixture_execution,
)
from app.services.controlled_evidence_intake_review_pack_service import (
    REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM,
    REVIEW_PACK_NEEDS_HUMAN_REVIEW,
    REVIEW_PACK_READY,
    build_controlled_evidence_intake_review_pack,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evidence_intake"


def _execution():
    return build_controlled_evidence_intake_fixture_execution(
        fixture_directory=FIXTURE_DIR
    )


def _review_pack(execution=None):
    return build_controlled_evidence_intake_review_pack(execution or _execution())


def test_clean_non_mutating_fixture_execution_produces_review_pack_ready():
    result = _review_pack()

    assert result["review_status"] == REVIEW_PACK_READY


def test_mutation_or_execution_flag_produces_blocked_or_review_status():
    execution = dict(_execution())
    execution["corpus_mutation_performed_any"] = True
    execution["all_non_mutating"] = False
    result = _review_pack(execution)

    assert result["review_status"] == REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM


def test_unexpected_fixture_outcome_produces_review_status():
    execution = dict(_execution())
    fixture_results = [dict(item) for item in execution["fixture_results"]]
    fixture_results[0]["passed_expected_outcome"] = False
    fixture_results[0]["failures"] = ("forced mismatch",)
    execution["fixture_results"] = tuple(fixture_results)
    result = _review_pack(execution)

    assert result["review_status"] == REVIEW_PACK_NEEDS_HUMAN_REVIEW


def test_human_review_items_are_listed_deterministically():
    first = _review_pack()
    second = _review_pack()

    assert first["required_human_review_items"] == tuple(
        sorted(first["required_human_review_items"])
    )
    assert first["required_human_review_items"] == second["required_human_review_items"]
    assert first["required_human_review_items"]


def test_evidence_ingestion_authorised_is_false():
    assert _review_pack()["evidence_ingestion_authorised"] is False


def test_corpus_mutation_authorised_is_false():
    assert _review_pack()["corpus_mutation_authorised"] is False


def test_code_evidence_ingestion_authorised_is_false():
    assert _review_pack()["code_evidence_ingestion_authorised"] is False


def test_db_write_authorised_is_false():
    assert _review_pack()["db_write_authorised"] is False


def test_live_retrieval_authorised_is_false():
    assert _review_pack()["live_retrieval_authorised"] is False


def test_live_llm_authorised_is_false():
    assert _review_pack()["live_llm_authorised"] is False


def test_final_answer_generation_authorised_is_false():
    assert _review_pack()["final_answer_generation_authorised"] is False


def test_runtime_and_production_readiness_claims_are_not_permitted():
    result = _review_pack()

    assert result["runtime_readiness_claim_permitted"] is False
    assert result["production_readiness_claim_permitted"] is False


def test_recommended_next_slice_is_explicit():
    result = _review_pack()

    assert result["recommended_next_slice"]
    assert "no-corpus-mutation" in result["recommended_next_slice"]


def test_output_is_deterministic_for_repeated_input():
    execution = _execution()

    assert _review_pack(execution) == _review_pack(execution)

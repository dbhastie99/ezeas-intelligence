from pathlib import Path

from app.services.controlled_evidence_intake_fixture_execution_service import (
    build_controlled_evidence_intake_fixture_execution,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evidence_intake"


def _execution():
    return build_controlled_evidence_intake_fixture_execution(
        fixture_directory=FIXTURE_DIR
    )


def test_all_checked_in_controlled_evidence_intake_fixtures_load_and_execute():
    result = _execution()

    assert result["fixture_count"] == 15
    assert len(result["fixture_results"]) == 15


def test_fixture_ids_are_deterministic_and_sorted():
    result = _execution()

    assert result["executed_fixture_ids"] == tuple(sorted(result["executed_fixture_ids"]))


def test_fixture_count_matches_checked_in_fixture_count():
    result = _execution()
    fixture_count = len(tuple(FIXTURE_DIR.glob("*.json")))

    assert result["fixture_count"] == fixture_count


def test_safe_fixtures_produce_expected_ready_or_review_outcomes():
    result = _execution()
    by_id = {item["fixture_id"]: item for item in result["fixture_results"]}

    assert (
        by_id["controlled-evidence-intake-developer-log-v0-1"]["dry_run_decision"]
        == "DRY_RUN_READY_FOR_FUTURE_INTAKE"
    )
    assert (
        by_id["controlled-evidence-intake-unknown-requires-review-v0-1"][
            "dry_run_decision"
        ]
        == "DRY_RUN_UNKNOWN_REQUIRES_REVIEW"
    )
    assert all(item["passed_expected_outcome"] for item in result["fixture_results"])


def test_blocked_fixtures_produce_expected_blocked_or_review_outcomes():
    result = _execution()
    by_id = {item["fixture_id"]: item for item in result["fixture_results"]}

    assert (
        by_id["controlled-evidence-intake-blocked-corpus-mutation-claim-v0-1"][
            "dry_run_decision"
        ]
        == "DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
    )
    assert (
        by_id["controlled-evidence-intake-blocked-runtime-overstatement-v0-1"][
            "dry_run_decision"
        ]
        == "DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
    )
    assert (
        by_id["controlled-evidence-intake-blocked-analysis-claims-repair-complete-v0-1"][
            "dry_run_decision"
        ]
        == "DRY_RUN_NEEDS_TRUST_REVIEW"
    )


def test_ready_review_and_blocked_counts_match_checked_in_fixtures():
    result = _execution()

    assert result["ready_count"] == 9
    assert result["needs_review_count"] == 2
    assert result["blocked_count"] == 4


def test_ingestion_performed_any_is_false():
    assert _execution()["ingestion_performed_any"] is False


def test_corpus_mutation_performed_any_is_false():
    assert _execution()["corpus_mutation_performed_any"] is False


def test_code_evidence_ingestion_performed_any_is_false():
    assert _execution()["code_evidence_ingestion_performed_any"] is False


def test_db_write_performed_any_is_false():
    assert _execution()["db_write_performed_any"] is False


def test_live_retrieval_performed_any_is_false():
    assert _execution()["live_retrieval_performed_any"] is False


def test_live_llm_performed_any_is_false():
    assert _execution()["live_llm_performed_any"] is False


def test_final_answer_generation_performed_any_is_false():
    assert _execution()["final_answer_generation_performed_any"] is False


def test_all_non_mutating_is_true():
    assert _execution()["all_non_mutating"] is True


def test_output_is_deterministic_for_repeated_input():
    assert _execution() == _execution()

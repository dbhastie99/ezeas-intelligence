import json
from pathlib import Path

import pytest

from app.services.controlled_evaluation_report_assembler_service import (
    assemble_controlled_evaluation_report,
)
from app.services.evaluation_output_publication_gate_service import (
    evaluate_evaluation_output_publication_gate,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evaluation_reports"
EXPECTED_FIXTURE_FILES = {
    "safe_controlled_evaluation_report.json",
    "safe_developer_handoff.json",
    "safe_progress_summary.json",
    "safe_next_slice_recommendation.json",
    "ambiguous_requires_review.json",
    "blocked_production_overstatement.json",
    "blocked_deployment_overstatement.json",
    "blocked_runtime_overstatement.json",
    "blocked_exposure_overstatement.json",
    "blocked_final_answer_generation_overstatement.json",
    "blocked_live_llm_overstatement.json",
    "blocked_db_access_validation_overstatement.json",
    "blocked_corpus_code_evidence_overstatement.json",
    "blocked_workforce_runtime_integration_overstatement.json",
    "blocked_analytics_runtime_integration_overstatement.json",
}

BLOCKED_OR_REVIEW_DECISIONS = {
    "NEEDS_CAVEAT_BEFORE_PUBLICATION",
    "UNKNOWN_REQUIRES_HUMAN_REVIEW",
    "BLOCKED_OVERSTATED_RUNTIME",
    "BLOCKED_OVERSTATED_DEPLOYMENT",
    "BLOCKED_OVERSTATED_PRODUCTION",
    "BLOCKED_OVERSTATED_EXPOSURE",
    "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM",
    "BLOCKED_LIVE_LLM_CLAIM",
    "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM",
    "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
    "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
}

APPROVAL_BOUNDARY_TERMS = (
    "RUNTIME_READINESS",
    "DEPLOYMENT_READINESS",
    "PRODUCTION_READINESS",
    "CHAT_EXPOSURE",
    "ENDPOINT_EXPOSURE",
    "LIVE_LLM",
    "DB_ACCESS",
    "DB_VALIDATION",
    "CORPUS_MUTATION",
    "CODE_EVIDENCE_INGESTION",
    "WORKFORCE_RUNTIME_INTEGRATION",
    "ANALYTICS_RUNTIME_INTEGRATION",
)


def _fixtures():
    assert FIXTURE_DIR.is_dir()
    paths = sorted(FIXTURE_DIR.glob("*.json"))
    assert {path.name for path in paths} == EXPECTED_FIXTURE_FILES
    return [(path, json.loads(path.read_text(encoding="utf-8"))) for path in paths]


def _fixture_by_id(fixture_id):
    return {fixture["fixture_id"]: fixture for _, fixture in _fixtures()}[fixture_id]


def _result(fixture):
    return assemble_controlled_evaluation_report(fixture["input_metadata"])


def _gate_result(fixture):
    return evaluate_evaluation_output_publication_gate(fixture["input_metadata"])


@pytest.mark.parametrize("path,fixture", _fixtures())
def test_fixture_files_are_valid_json_and_have_required_keys(path, fixture):
    assert path.name.endswith(".json")
    assert set(fixture) == {
        "fixture_id",
        "fixture_purpose",
        "input_metadata",
        "expected_publication_decision",
        "expected_safe_for_controlled_evaluation_report",
        "expected_safe_for_developer_handoff",
        "expected_safe_for_progress_summary",
        "expected_safe_for_final_answer_generation",
        "expected_required_caveats",
        "expected_block_reasons",
        "expected_preserved_boundaries",
        "expected_violated_boundaries",
        "expected_no_action_attestation",
        "expected_recommended_next_slice",
        "expected_summary_terms",
    }


def test_all_fixture_ids_are_unique():
    fixture_ids = [fixture["fixture_id"] for _, fixture in _fixtures()]

    assert len(fixture_ids) == len(set(fixture_ids))


@pytest.mark.parametrize("path,fixture", _fixtures())
def test_fixture_outputs_are_deterministic_for_repeated_runs(path, fixture):
    assert _result(fixture) == _result(fixture)
    assert _gate_result(fixture) == _gate_result(fixture)


@pytest.mark.parametrize("path,fixture", _fixtures())
def test_fixture_outputs_match_expected_baselines(path, fixture):
    result = _result(fixture)

    assert result["publication_decision"] == fixture["expected_publication_decision"]
    assert (
        result["safe_for_controlled_evaluation_report"]
        is fixture["expected_safe_for_controlled_evaluation_report"]
    )
    assert (
        result["safe_for_developer_handoff"]
        is fixture["expected_safe_for_developer_handoff"]
    )
    assert (
        result["safe_for_progress_summary"]
        is fixture["expected_safe_for_progress_summary"]
    )
    assert (
        result["safe_for_final_answer_generation"]
        is fixture["expected_safe_for_final_answer_generation"]
    )
    assert set(fixture["expected_required_caveats"]).issubset(result["required_caveats"])
    assert tuple(fixture["expected_preserved_boundaries"]) == result["preserved_boundaries"]
    assert tuple(fixture["expected_violated_boundaries"]) == result["violated_boundaries"]
    assert result["no_action_attestation"] == fixture["expected_no_action_attestation"]
    assert result["recommended_next_slice"] == fixture["expected_recommended_next_slice"]

    gate = _gate_result(fixture)
    assert tuple(fixture["expected_block_reasons"]) == gate["block_reasons"]


def test_safe_controlled_evaluation_report_fixture_remains_report_only():
    result = _result(_fixture_by_id("safe_controlled_evaluation_report"))

    assert result["safe_for_controlled_evaluation_report"] is True
    assert result["safe_for_developer_handoff"] is False
    assert result["safe_for_progress_summary"] is False
    assert result["safe_for_final_answer_generation"] is False


def test_safe_developer_handoff_fixture_remains_safe_for_handoff():
    result = _result(_fixture_by_id("safe_developer_handoff"))

    assert result["publication_decision"] == "PUBLISH_DEVELOPER_HANDOFF"
    assert result["safe_for_developer_handoff"] is True


def test_safe_progress_summary_fixture_remains_safe_for_progress_summary():
    result = _result(_fixture_by_id("safe_progress_summary"))

    assert result["publication_decision"] == "PUBLISH_PROGRESS_SUMMARY"
    assert result["safe_for_progress_summary"] is True


def test_safe_next_slice_recommendation_preserves_recommendation_output():
    fixture = _fixture_by_id("safe_next_slice_recommendation")
    result = _result(fixture)

    assert result["report_type"] == "NEXT_SLICE_RECOMMENDATION"
    assert result["recommended_next_slice"] == fixture["expected_recommended_next_slice"]
    assert result["sections"]["recommended_next_slice"] == fixture["expected_recommended_next_slice"]


def test_ambiguous_fixture_requires_caveat_or_human_review():
    result = _result(_fixture_by_id("ambiguous_requires_review"))

    assert result["publication_decision"] in {
        "NEEDS_CAVEAT_BEFORE_PUBLICATION",
        "UNKNOWN_REQUIRES_HUMAN_REVIEW",
    }
    assert result["missing_caveats"]
    assert result["safe_for_controlled_evaluation_report"] is False


@pytest.mark.parametrize(
    ("fixture_id", "decision", "violated_boundary"),
    [
        ("blocked_production_overstatement", "BLOCKED_OVERSTATED_PRODUCTION", "PRODUCTION_READINESS"),
        ("blocked_deployment_overstatement", "BLOCKED_OVERSTATED_DEPLOYMENT", "DEPLOYMENT_READINESS"),
        ("blocked_runtime_overstatement", "BLOCKED_OVERSTATED_RUNTIME", "RUNTIME_READINESS"),
        ("blocked_exposure_overstatement", "BLOCKED_OVERSTATED_EXPOSURE", "CHAT_EXPOSURE"),
        (
            "blocked_final_answer_generation_overstatement",
            "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM",
            "FINAL_ANSWER_GENERATION",
        ),
        ("blocked_live_llm_overstatement", "BLOCKED_LIVE_LLM_CLAIM", "LIVE_LLM"),
        (
            "blocked_db_access_validation_overstatement",
            "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM",
            "DB_ACCESS",
        ),
        (
            "blocked_corpus_code_evidence_overstatement",
            "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
            "CORPUS_MUTATION",
        ),
        (
            "blocked_workforce_runtime_integration_overstatement",
            "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
            "WORKFORCE_RUNTIME_INTEGRATION",
        ),
        (
            "blocked_analytics_runtime_integration_overstatement",
            "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
            "ANALYTICS_RUNTIME_INTEGRATION",
        ),
    ],
)
def test_overstatement_fixtures_are_blocked(fixture_id, decision, violated_boundary):
    result = _result(_fixture_by_id(fixture_id))

    assert result["publication_decision"] == decision
    assert result["safe_for_controlled_evaluation_report"] is False
    assert violated_boundary in result["violated_boundaries"]


def test_db_pending_or_not_performed_wording_is_not_blocked_by_gate():
    gate = evaluate_evaluation_output_publication_gate(
        "Minerva remains controlled-readiness only. DB validation pending and not performed. No DB access."
    )

    assert gate["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    assert gate["db_access_claim_detected"] is False
    assert gate["db_validation_claim_detected"] is False


@pytest.mark.parametrize("path,fixture", _fixtures())
def test_no_fixture_is_safe_for_final_answer_generation(path, fixture):
    result = _result(fixture)
    gate = _gate_result(fixture)

    assert result["safe_for_final_answer_generation"] is False
    assert result["sections"]["safe_for_final_answer_generation"] is False
    assert gate["safe_for_final_answer_generation"] is False


@pytest.mark.parametrize("path,fixture", _fixtures())
def test_no_fixture_introduces_unblocked_runtime_or_exposure_approval(path, fixture):
    result = _result(fixture)
    decision = result["publication_decision"]

    if result["violated_boundaries"]:
        assert decision in BLOCKED_OR_REVIEW_DECISIONS

    for boundary in result["violated_boundaries"]:
        assert boundary in APPROVAL_BOUNDARY_TERMS or boundary == "FINAL_ANSWER_GENERATION"

    blocked_or_deferred_text = " ".join(result["blocked_or_deferred_capabilities"]).lower()
    assert "production readiness deferred" in blocked_or_deferred_text or decision in BLOCKED_OR_REVIEW_DECISIONS
    assert "deployment readiness deferred" in blocked_or_deferred_text or decision in BLOCKED_OR_REVIEW_DECISIONS
    assert "runtime enablement deferred" in blocked_or_deferred_text or decision in BLOCKED_OR_REVIEW_DECISIONS

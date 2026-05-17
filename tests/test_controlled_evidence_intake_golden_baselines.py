import json
from pathlib import Path

import pytest

from app.services.controlled_evidence_intake_planning_gate_service import (
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    NEEDS_TRUST_REVIEW,
    NO_ACTION_ATTESTATION,
    READY_FOR_INTAKE_PLANNING,
    UNKNOWN_REQUIRES_REVIEW,
    build_controlled_evidence_intake_planning_gate,
)
from app.services.controlled_evidence_intake_taxonomy_service import (
    ANALYTICS_READINESS_SUMMARY,
    AWARD_RECOVERY_ANALYSIS,
    CODE_EVIDENCE_PLANNING_OUTPUT,
    CONTROLLED_EVALUATION_SUMMARY,
    DEVELOPER_LOG,
    HARDENING_LOG,
    PLATFORM_DOCTRINE,
    THREAD_CONTINUANCE_PROMPT,
    UNKNOWN_REQUIRES_REVIEW as UNKNOWN_CATEGORY_REQUIRES_REVIEW,
    WORKFORCE_CONTROLLED_READINESS_DOC,
    build_controlled_evidence_intake_taxonomy,
)
from app.services.evidence_source_status_boundary_service import (
    ANALYSIS_EVIDENCE,
    PLANNING_EVIDENCE,
    UNKNOWN_REQUIRES_REVIEW as UNKNOWN_STATUS_REQUIRES_REVIEW,
    build_evidence_source_status_boundary,
)


FIXTURE_DIR = Path("tests/fixtures/controlled_evidence_intake")
BLOCKED_OR_REVIEW_DECISIONS = {
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    NEEDS_TRUST_REVIEW,
    UNKNOWN_REQUIRES_REVIEW,
}
PROHIBITED_RUNTIME_TERMS = (
    "deployment readiness",
    "live LLM",
    "chat exposure",
    "DB access",
    "workforce runtime integration",
    "analytics runtime integration",
    "production readiness",
)


def _fixture_files():
    return sorted(FIXTURE_DIR.glob("*.json"))


def _load_fixture(path):
    with path.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


@pytest.fixture(scope="module")
def fixtures():
    return [_load_fixture(path) for path in _fixture_files()]


def _taxonomy(fixture):
    return build_controlled_evidence_intake_taxonomy(fixture["input_metadata"])


def _gate(fixture):
    return build_controlled_evidence_intake_planning_gate(fixture["input_metadata"])


def _boundary(fixture):
    return build_evidence_source_status_boundary(fixture["input_metadata"])


def _fixture_by_id(fixtures, fixture_id):
    return next(fixture for fixture in fixtures if fixture["fixture_id"] == fixture_id)


def test_all_fixture_files_are_valid_json(fixtures):
    assert len(fixtures) == 15


def test_all_fixture_ids_are_unique(fixtures):
    fixture_ids = [fixture["fixture_id"] for fixture in fixtures]

    assert len(fixture_ids) == len(set(fixture_ids))


def test_required_fixture_contract_is_present(fixtures):
    required_fields = {
        "fixture_id",
        "fixture_purpose",
        "input_metadata",
        "expected_evidence_category",
        "expected_gate_decision",
        "expected_source_status",
        "expected_ingestion_authorised",
        "expected_corpus_mutation_authorised",
        "expected_runtime_claim_permitted",
        "expected_production_claim_permitted",
        "expected_required_caveats",
        "expected_blocked_reasons",
        "expected_prohibited_inferences",
        "expected_no_action_attestation",
        "expected_summary_terms",
    }

    for fixture in fixtures:
        assert required_fields <= set(fixture)


def test_fixture_outputs_are_deterministic_for_repeated_runs(fixtures):
    for fixture in fixtures:
        assert _taxonomy(fixture) == _taxonomy(fixture)
        assert _gate(fixture) == _gate(fixture)
        assert _boundary(fixture) == _boundary(fixture)


@pytest.mark.parametrize(
    ("fixture_id", "expected_category"),
    (
        ("controlled-evidence-intake-developer-log-v0-1", DEVELOPER_LOG),
        ("controlled-evidence-intake-hardening-log-v0-1", HARDENING_LOG),
        ("controlled-evidence-intake-platform-doctrine-v0-1", PLATFORM_DOCTRINE),
        ("controlled-evidence-intake-thread-continuance-prompt-v0-1", THREAD_CONTINUANCE_PROMPT),
        ("controlled-evidence-intake-analytics-readiness-summary-v0-1", ANALYTICS_READINESS_SUMMARY),
        ("controlled-evidence-intake-award-recovery-analysis-v0-1", AWARD_RECOVERY_ANALYSIS),
        ("controlled-evidence-intake-workforce-controlled-readiness-doc-v0-1", WORKFORCE_CONTROLLED_READINESS_DOC),
        ("controlled-evidence-intake-code-evidence-planning-output-v0-1", CODE_EVIDENCE_PLANNING_OUTPUT),
        ("controlled-evidence-intake-controlled-evaluation-summary-v0-1", CONTROLLED_EVALUATION_SUMMARY),
    ),
)
def test_named_fixtures_classify_to_expected_categories(fixtures, fixture_id, expected_category):
    fixture = _fixture_by_id(fixtures, fixture_id)

    assert _taxonomy(fixture)["evidence_category"] == expected_category
    assert fixture["expected_evidence_category"] == expected_category


def test_unknown_fixture_requires_review(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-unknown-requires-review-v0-1")

    assert _taxonomy(fixture)["evidence_category"] == UNKNOWN_CATEGORY_REQUIRES_REVIEW
    assert _gate(fixture)["gate_decision"] == UNKNOWN_REQUIRES_REVIEW
    assert _boundary(fixture)["source_status"] == UNKNOWN_STATUS_REQUIRES_REVIEW


def test_runtime_overstatement_fixture_is_blocked_or_reviewed(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-blocked-runtime-overstatement-v0-1")
    gate = _gate(fixture)
    boundary = _boundary(fixture)

    assert gate["gate_decision"] in BLOCKED_OR_REVIEW_DECISIONS
    assert gate["gate_decision"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert boundary["runtime_claim_permitted"] is False


def test_production_overstatement_fixture_is_blocked_or_reviewed(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-blocked-production-overstatement-v0-1")
    gate = _gate(fixture)
    boundary = _boundary(fixture)

    assert gate["gate_decision"] in BLOCKED_OR_REVIEW_DECISIONS
    assert gate["gate_decision"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert boundary["production_claim_permitted"] is False


def test_unauthorised_ingestion_claim_fixture_is_blocked(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-blocked-unauthorised-ingestion-claim-v0-1")
    gate = _gate(fixture)

    assert gate["gate_decision"] == BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    assert "unauthorised_ingestion_claim" in gate["blocked_reasons"]


def test_corpus_mutation_claim_fixture_is_blocked(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-blocked-corpus-mutation-claim-v0-1")
    gate = _gate(fixture)

    assert gate["gate_decision"] == BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    assert "unauthorised_corpus_mutation_claim" in gate["blocked_reasons"]


def test_analysis_evidence_claiming_repair_complete_is_blocked_or_reviewed(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-blocked-analysis-claims-repair-complete-v0-1")
    gate = _gate(fixture)
    boundary = _boundary(fixture)

    assert gate["gate_decision"] in BLOCKED_OR_REVIEW_DECISIONS
    assert gate["gate_decision"] == NEEDS_TRUST_REVIEW
    assert boundary["source_status"] == ANALYSIS_EVIDENCE
    assert boundary["implementation_claim_permitted"] is False
    assert "repair completed" in boundary["prohibited_inferences"]


def test_expected_golden_baseline_outputs_match_services(fixtures):
    for fixture in fixtures:
        taxonomy = _taxonomy(fixture)
        gate = _gate(fixture)
        boundary = _boundary(fixture)

        assert taxonomy["evidence_category"] == fixture["expected_evidence_category"]
        assert gate["gate_decision"] == fixture["expected_gate_decision"]
        assert boundary["source_status"] == fixture["expected_source_status"]
        assert taxonomy["ingestion_authorised"] == fixture["expected_ingestion_authorised"]
        assert taxonomy["corpus_mutation_authorised"] == fixture["expected_corpus_mutation_authorised"]
        assert boundary["runtime_claim_permitted"] == fixture["expected_runtime_claim_permitted"]
        assert boundary["production_claim_permitted"] == fixture["expected_production_claim_permitted"]
        assert tuple(gate["blocked_reasons"]) == tuple(fixture["expected_blocked_reasons"])
        assert gate["no_action_attestation"] == fixture["expected_no_action_attestation"]
        assert gate["no_action_attestation"] == NO_ACTION_ATTESTATION


def test_no_fixture_authorises_ingestion_or_corpus_mutation(fixtures):
    for fixture in fixtures:
        taxonomy = _taxonomy(fixture)
        gate = _gate(fixture)

        assert taxonomy["ingestion_authorised"] is False
        assert taxonomy["corpus_mutation_authorised"] is False
        assert gate["ingestion_authorised_now"] is False
        assert gate["corpus_mutation_authorised_now"] is False


def test_no_fixture_permits_runtime_or_production_claims_by_default(fixtures):
    for fixture in fixtures:
        taxonomy = _taxonomy(fixture)
        boundary = _boundary(fixture)

        assert taxonomy["runtime_claim_permitted"] is False
        assert taxonomy["production_claim_permitted"] is False
        assert boundary["runtime_claim_permitted"] is False
        assert boundary["production_claim_permitted"] is False


def test_no_fixture_implies_runtime_deployment_or_cross_repo_exposure(fixtures):
    for fixture in fixtures:
        prohibited = set(fixture["expected_prohibited_inferences"])
        caveats = " ".join(fixture["expected_required_caveats"])
        summary_terms = " ".join(fixture["expected_summary_terms"])

        for term in PROHIBITED_RUNTIME_TERMS:
            if term in caveats or term in summary_terms:
                assert term.startswith("no ") or "does not" in caveats
            else:
                assert term in prohibited or term not in summary_terms


def test_source_status_boundary_preserves_evidence_exists_vs_implementation_truth(fixtures):
    planning_fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-developer-log-v0-1")
    unknown_fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-unknown-requires-review-v0-1")
    planning_boundary = _boundary(planning_fixture)
    unknown_boundary = _boundary(unknown_fixture)

    assert planning_boundary["source_status"] == PLANNING_EVIDENCE
    assert planning_boundary["evidence_exists"] is True
    assert planning_boundary["implementation_claim_permitted"] is False
    assert unknown_boundary["evidence_exists"] is False


def test_source_status_boundary_preserves_analysis_vs_repair_truth(fixtures):
    fixture = _fixture_by_id(fixtures, "controlled-evidence-intake-award-recovery-analysis-v0-1")
    boundary = _boundary(fixture)

    assert boundary["source_status"] == ANALYSIS_EVIDENCE
    assert boundary["implementation_claim_permitted"] is False
    assert "repair completed" in boundary["prohibited_inferences"]


def test_required_caveats_and_no_action_attestation_are_preserved(fixtures):
    for fixture in fixtures:
        taxonomy = _taxonomy(fixture)
        gate = _gate(fixture)

        assert tuple(taxonomy["required_caveats"]) == tuple(fixture["expected_required_caveats"])
        assert tuple(gate["required_caveats"]) == tuple(fixture["expected_required_caveats"])
        assert gate["no_action_attestation"] == fixture["expected_no_action_attestation"]


def test_ready_fixtures_are_planning_ready_only(fixtures):
    ready_fixtures = [fixture for fixture in fixtures if fixture["expected_gate_decision"] == READY_FOR_INTAKE_PLANNING]

    assert ready_fixtures
    for fixture in ready_fixtures:
        gate = _gate(fixture)
        assert gate["ready_for_future_intake_planning"] is True
        assert gate["ingestion_authorised_now"] is False
        assert gate["corpus_mutation_authorised_now"] is False

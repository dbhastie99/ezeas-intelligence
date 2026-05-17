from app.services.controlled_evidence_intake_dry_run_service import (
    build_controlled_evidence_intake_dry_run,
)
from app.services.controlled_evidence_intake_dry_run_summary_service import (
    build_controlled_evidence_intake_dry_run_summary,
)


def _complete_metadata(**overrides):
    metadata = {
        "evidence_id": "fixture-developer-log",
        "evidence_category": "DEVELOPER_LOG",
        "source_repo": "ezeas-intelligence",
        "source_phase": "governed corpus intake planning",
        "source_status": "PLANNING_EVIDENCE",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Planning evidence only.",),
    }
    metadata.update(overrides)
    return metadata


def _dry_run(**overrides):
    return build_controlled_evidence_intake_dry_run(_complete_metadata(**overrides))


def _mixed_results():
    return (
        _dry_run(evidence_id="ready"),
        _dry_run(evidence_id="review", source_repo="", source_phase=""),
        _dry_run(evidence_id="runtime-blocked", runtime_claim_permitted=True),
        _dry_run(evidence_id="ingestion-blocked", ingestion_authorised=True),
    )


def test_multiple_dry_run_results_aggregate_deterministically():
    results = _mixed_results()

    assert build_controlled_evidence_intake_dry_run_summary(results) == build_controlled_evidence_intake_dry_run_summary(results)


def test_ready_review_and_blocked_counts_are_correct():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["dry_run_count"] == 4
    assert summary["ready_count"] == 1
    assert summary["needs_review_count"] == 1
    assert summary["blocked_count"] == 2


def test_all_non_mutating_is_true_when_no_execution_flags_are_present():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["all_non_mutating"] is True


def test_mutation_or_execution_flag_makes_all_non_mutating_false():
    result = dict(_dry_run())
    result["corpus_mutation_performed"] = True
    summary = build_controlled_evidence_intake_dry_run_summary((result,))

    assert summary["all_non_mutating"] is False
    assert summary["needs_review_count"] == 1


def test_ingestion_performed_any_is_false_for_normal_dry_run_outputs():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["ingestion_performed_any"] is False


def test_corpus_mutation_performed_any_is_false_for_normal_dry_run_outputs():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["corpus_mutation_performed_any"] is False


def test_code_evidence_ingestion_performed_any_is_false_for_normal_outputs():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["code_evidence_ingestion_performed_any"] is False


def test_db_write_performed_any_is_false_for_normal_dry_run_outputs():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["db_write_performed_any"] is False


def test_runtime_or_production_overstatement_count_is_correct():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["runtime_or_production_overstatement_count"] == 1


def test_unauthorised_ingestion_claim_count_is_correct():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["unauthorised_ingestion_claim_count"] == 1


def test_recommended_next_slice_is_explicit():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert summary["recommended_next_slice"]
    assert "no-corpus-mutation" in summary["recommended_next_slice"]


def test_summary_never_authorises_ingestion_or_corpus_mutation():
    summary = build_controlled_evidence_intake_dry_run_summary(_mixed_results())

    assert "no ingestion" in summary["explanation"].lower()
    assert "corpus mutation" in summary["explanation"].lower()
    assert "No evidence ingestion" in summary["no_action_attestation"]


def test_output_is_deterministic_for_repeated_input():
    results = (_dry_run(evidence_id="ready-one"), _dry_run(evidence_id="ready-two"))

    assert build_controlled_evidence_intake_dry_run_summary(results) == build_controlled_evidence_intake_dry_run_summary(results)

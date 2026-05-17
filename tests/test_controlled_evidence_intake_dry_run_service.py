import json
from pathlib import Path

from app.services.controlled_evidence_intake_dry_run_service import (
    DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM,
    DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    DRY_RUN_NEEDS_SOURCE_CONTEXT,
    DRY_RUN_NEEDS_STATUS_BOUNDARY,
    DRY_RUN_NEEDS_TRUST_REVIEW,
    DRY_RUN_READY_FOR_FUTURE_INTAKE,
    build_controlled_evidence_intake_dry_run,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "controlled_evidence_intake"


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


def test_complete_known_evidence_metadata_is_ready_for_future_intake():
    result = _dry_run()

    assert result["dry_run_decision"] == DRY_RUN_READY_FOR_FUTURE_INTAKE
    assert result["would_ingest_in_future_if_authorised"] is True


def test_ready_for_future_intake_does_not_authorise_ingestion_now():
    result = _dry_run()

    assert result["would_ingest_in_future_if_authorised"] is True
    assert result["ingestion_performed"] is False


def test_missing_source_context_requires_source_context():
    result = _dry_run(source_repo="", source_phase="")

    assert result["dry_run_decision"] == DRY_RUN_NEEDS_SOURCE_CONTEXT


def test_missing_status_boundary_requires_status_boundary():
    result = _dry_run(source_status="")

    assert result["dry_run_decision"] == DRY_RUN_NEEDS_STATUS_BOUNDARY


def test_unknown_trust_level_requires_trust_review():
    result = _dry_run(trust_level="UNKNOWN")

    assert result["dry_run_decision"] == DRY_RUN_NEEDS_TRUST_REVIEW


def test_runtime_or_production_overstatement_is_blocked():
    result = _dry_run(runtime_claim_permitted=True)

    assert result["dry_run_decision"] == DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT


def test_unauthorised_ingestion_claim_is_blocked():
    result = _dry_run(ingestion_authorised=True)

    assert result["dry_run_decision"] == DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM


def test_corpus_mutation_claim_is_blocked():
    result = _dry_run(corpus_mutation_authorised=True)

    assert result["dry_run_decision"] == DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM


def test_code_evidence_ingestion_claim_is_blocked():
    result = _dry_run(code_evidence_ingestion_authorised=True)

    assert result["dry_run_decision"] == DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM


def test_ingestion_performed_is_always_false():
    assert _dry_run()["ingestion_performed"] is False
    assert _dry_run(ingestion_authorised=True)["ingestion_performed"] is False


def test_corpus_mutation_performed_is_always_false():
    assert _dry_run()["corpus_mutation_performed"] is False
    assert _dry_run(corpus_mutation_authorised=True)["corpus_mutation_performed"] is False


def test_code_evidence_ingestion_performed_is_always_false():
    assert _dry_run()["code_evidence_ingestion_performed"] is False
    assert _dry_run(code_evidence_ingestion_authorised=True)["code_evidence_ingestion_performed"] is False


def test_db_write_performed_is_always_false():
    assert _dry_run()["db_write_performed"] is False
    assert _dry_run(db_write_authorised=True)["db_write_performed"] is False


def test_live_retrieval_performed_is_always_false():
    assert _dry_run()["live_retrieval_performed"] is False
    assert _dry_run(live_retrieval_authorised=True)["live_retrieval_performed"] is False


def test_live_llm_performed_is_always_false():
    assert _dry_run()["live_llm_performed"] is False
    assert _dry_run(live_llm_authorised=True)["live_llm_performed"] is False


def test_final_answer_generation_performed_is_always_false():
    assert _dry_run()["final_answer_generation_performed"] is False
    assert _dry_run(final_answer_generation_authorised=True)["final_answer_generation_performed"] is False


def test_no_action_attestation_is_preserved():
    result = _dry_run()

    assert "No evidence ingestion" in result["no_action_attestation"]
    assert "corpus mutation" in result["no_action_attestation"]
    assert "live LLM" in result["no_action_attestation"]


def test_output_is_deterministic_for_repeated_input():
    metadata = _complete_metadata()

    assert build_controlled_evidence_intake_dry_run(metadata) == build_controlled_evidence_intake_dry_run(metadata)


def test_fixture_payload_input_metadata_is_supported():
    result = build_controlled_evidence_intake_dry_run(
        {"fixture_id": "fixture", "input_metadata": _complete_metadata()}
    )

    assert result["dry_run_decision"] == DRY_RUN_READY_FOR_FUTURE_INTAKE


def test_existing_governed_evidence_intake_fixture_can_be_dry_run():
    fixture = json.loads(
        (FIXTURE_DIR / "developer_log_evidence.json").read_text(encoding="utf-8")
    )

    result = build_controlled_evidence_intake_dry_run(fixture)

    assert result["evidence_id"] == "fixture-developer-log"
    assert result["dry_run_decision"] == DRY_RUN_READY_FOR_FUTURE_INTAKE
    assert result["ingestion_performed"] is False

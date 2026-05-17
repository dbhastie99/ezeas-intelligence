from app.services.controlled_durable_evidence_intake_closeout_readiness_service import (
    BLOCKED_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY,
    NEEDS_VERIFICATION,
    build_controlled_durable_evidence_intake_closeout_readiness,
)
from app.services.controlled_durable_evidence_intake_design_service import (
    build_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_evidence_intake_design_verification_service import (
    verify_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_intake_audit_envelope_service import (
    build_controlled_durable_intake_audit_envelope,
)
from app.services.controlled_durable_intake_authorisation_requirements_service import (
    build_controlled_durable_intake_authorisation_requirements,
)


def _design():
    return build_controlled_durable_evidence_intake_design(
        {
            "storage_boundary_model": "review-only source metadata; no corpus writes",
            "mutation_boundary_model": "future explicit gate required before mutation",
            "review_boundary_model": "reviewer confirmation required before action",
            "rollback_or_removal_policy": "rollback/removal policy must be approved",
        }
    )


def _requirements():
    return build_controlled_durable_intake_authorisation_requirements(
        {
            "reviewer_confirmation": True,
            "source_status_boundary": True,
            "evidence_envelope": True,
            "no_overstatement_check": True,
            "rollback_policy": True,
            "audit_metadata": True,
            "dry_run_review": True,
        }
    )


def _audit():
    return build_controlled_durable_intake_audit_envelope(
        {
            "source_reference": "controlled-no-mutation-envelope",
            "source_status": "CONTROLLED_READINESS_ONLY",
            "reviewer": "reviewer-id",
            "decision_timestamp": "2026-05-17T00:00:00Z",
            "no_mutation_history": "first no-mutation intake execution complete",
            "rollback_policy": "approved rollback/removal policy required",
            "prohibited_claims_checked": True,
            "sensitive_data_review": True,
        }
    )


def _verified_metadata():
    return verify_controlled_durable_evidence_intake_design(
        _design(),
        _requirements(),
        _audit(),
    )


def _readiness(metadata=None):
    return build_controlled_durable_evidence_intake_closeout_readiness(
        _verified_metadata() if metadata is None else metadata
    )


def test_verified_durable_intake_design_produces_closeout_ready_status():
    assert (
        _readiness()["readiness_status"]
        == DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY
    )


def test_unverified_design_produces_needs_verification():
    result = _readiness({"verification_status": NEEDS_VERIFICATION})

    assert result["readiness_status"] == NEEDS_VERIFICATION


def test_ready_for_design_phase_closeout_is_true_only_for_verified_design():
    assert _readiness()["ready_for_design_phase_closeout"] is True
    assert (
        _readiness({"verification_status": NEEDS_VERIFICATION})[
            "ready_for_design_phase_closeout"
        ]
        is False
    )


def test_remaining_work_is_limited_to_authorisation_decision_or_pause():
    assert _readiness()["remaining_work"] == (
        "Make an explicit future durable-intake authorisation decision.",
        "Keep Minerva paused if durable intake is not explicitly authorised.",
    )


def test_recommended_next_slice_is_explicit():
    assert "Controlled Durable Evidence Intake Authorisation Decision" in _readiness()[
        "recommended_next_slice"
    ]


def test_durable_intake_authorised_now_is_false():
    assert _readiness()["durable_intake_authorised_now"] is False


def test_corpus_mutation_authorised_now_is_false():
    assert _readiness()["corpus_mutation_authorised_now"] is False


def test_db_write_authorised_now_is_false():
    assert _readiness()["db_write_authorised_now"] is False


def test_code_evidence_ingestion_authorised_now_is_false():
    assert _readiness()["code_evidence_ingestion_authorised_now"] is False


def test_live_retrieval_authorised_now_is_false():
    assert _readiness()["live_retrieval_authorised_now"] is False


def test_live_llm_authorised_now_is_false():
    assert _readiness()["live_llm_authorised_now"] is False


def test_final_answer_generation_authorised_now_is_false():
    assert _readiness()["final_answer_generation_authorised_now"] is False


def test_production_deployment_runtime_readiness_claims_are_not_permitted():
    result = _readiness()

    assert result["production_readiness_claim_permitted"] is False
    assert result["deployment_readiness_claim_permitted"] is False
    assert result["runtime_readiness_claim_permitted"] is False


def test_durable_ingestion_claim_is_blocked():
    metadata = _verified_metadata()
    metadata["durable_intake_authorised_now"] = True

    result = _readiness(metadata)

    assert result["readiness_status"] == BLOCKED_DURABLE_INGESTION_CLAIM
    assert result["durable_intake_authorised_now"] is False


def test_runtime_or_production_overstatement_is_blocked():
    metadata = _verified_metadata()
    metadata["production_readiness_claim_permitted"] = True

    result = _readiness(metadata)

    assert result["readiness_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["production_readiness_claim_permitted"] is False


def test_output_is_deterministic_for_repeated_input():
    metadata = _verified_metadata()

    assert _readiness(metadata) == _readiness(metadata)

from app.services.controlled_durable_evidence_intake_authorisation_gate_service import (
    build_controlled_durable_evidence_intake_authorisation_gate,
)
from app.services.controlled_durable_intake_candidate_eligibility_service import (
    build_controlled_durable_intake_candidate_eligibility,
)
from app.services.controlled_durable_intake_execution_review_pack_service import (
    BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM,
    BLOCKED_MUTATION_OR_DB_WRITE_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY,
    build_controlled_durable_intake_execution_review_pack,
)
from app.services.controlled_durable_intake_first_candidate_execution_design_service import (
    build_controlled_durable_intake_first_candidate_execution_design,
)


def _candidate():
    return {
        "candidate_id": "durable-candidate-001",
        "candidate_type": "DEVELOPER_LOG",
        "source_reference": "docs/evaluation/source.md",
        "source_status_boundary": "CONTROLLED_READINESS_ONLY",
        "evidence_envelope": True,
        "audit_envelope": True,
        "reviewer_confirmation": True,
        "rollback_policy": "remove candidate and derived references before ingestion",
        "sensitive_data_review": True,
    }


def _execution_design(**overrides):
    candidate = _candidate()
    gate = build_controlled_durable_evidence_intake_authorisation_gate(candidate)
    eligibility = build_controlled_durable_intake_candidate_eligibility(candidate)
    design = build_controlled_durable_intake_first_candidate_execution_design(
        gate,
        eligibility,
    )
    design.update(overrides)
    return design


def _review_pack(**overrides):
    return build_controlled_durable_intake_execution_review_pack(
        _execution_design(**overrides)
    )


def test_clean_execution_design_produces_review_pack_ready():
    result = _review_pack()

    assert result["review_pack_status"] == DURABLE_INTAKE_EXECUTION_REVIEW_PACK_READY
    assert result["execution_design_ready"] is True


def test_no_action_boundary_fields_are_false():
    result = _review_pack()

    assert result["durable_intake_execution_authorised_now"] is False
    assert result["durable_intake_performed"] is False
    assert result["corpus_mutation_performed"] is False
    assert result["db_write_performed"] is False
    assert result["code_evidence_ingestion_performed"] is False


def test_required_review_items_include_required_controls():
    result = _review_pack()

    for item in (
        "source_evidence",
        "candidate_eligibility",
        "authorisation_gate",
        "audit_envelope",
        "rollback_removal_policy",
        "sensitive_data_review",
        "reviewer_confirmation",
    ):
        assert item in result["required_review_items"]


def test_required_evidence_items_are_deterministic():
    result = _review_pack()

    assert result["required_evidence_items"] == _review_pack()[
        "required_evidence_items"
    ]
    assert result["required_evidence_items"] == (
        "source_reference_record",
        "source_status_boundary_record",
        "candidate_eligibility_record",
        "authorisation_gate_record",
        "evidence_envelope_record",
        "audit_envelope_record",
        "rollback_or_removal_policy_record",
        "sensitive_data_review_record",
        "no_overstatement_attestation",
        "explicit_execution_authorisation_record",
    )


def test_prohibited_execution_claims_include_required_claims():
    result = _review_pack()

    for item in (
        "already_ingested",
        "corpus_mutated",
        "db_written",
        "code_evidence_ingested",
        "live_retrieval_used",
        "llm_used",
        "final_answer_generated",
        "chat_exposed",
        "runtime_integrated",
        "production_ready",
    ):
        assert item in result["prohibited_execution_claims"]


def test_stop_conditions_are_deterministic():
    result = _review_pack()

    assert result["stop_conditions"] == _review_pack()["stop_conditions"]
    assert "missing_execution_design" in result["stop_conditions"]
    assert "durable_intake_already_performed_claim" in result["stop_conditions"]
    assert "corpus_mutation_or_db_write_claim" in result["stop_conditions"]
    assert "runtime_deployment_or_production_overstatement" in result[
        "stop_conditions"
    ]


def test_recommended_next_slice_is_explicit():
    result = _review_pack()

    assert result["recommended_next_slice"]
    assert "Controlled Durable Intake First Candidate Execution Authorisation" in result[
        "recommended_next_slice"
    ]


def test_durable_intake_already_performed_claim_is_blocked():
    result = _review_pack(durable_intake_performed=True)

    assert result["review_pack_status"] == BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM
    assert result["durable_intake_performed"] is False


def test_mutation_or_db_write_claim_is_blocked():
    for claim_key in ("corpus_mutation_performed", "db_write_performed"):
        result = _review_pack(**{claim_key: True})

        assert result["review_pack_status"] == BLOCKED_MUTATION_OR_DB_WRITE_CLAIM
        assert result[claim_key] is False


def test_runtime_or_production_overstatement_is_blocked():
    result = _review_pack(production_readiness_claim_permitted=True)

    assert result["review_pack_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT


def test_output_is_deterministic():
    design = _execution_design()

    assert build_controlled_durable_intake_execution_review_pack(
        design
    ) == build_controlled_durable_intake_execution_review_pack(design)

from app.services.controlled_evidence_intake_planning_gate_service import (
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    NEEDS_SOURCE_CONTEXT,
    NEEDS_STATUS_BOUNDARY,
    NEEDS_TRUST_REVIEW,
    READY_FOR_INTAKE_PLANNING,
    build_controlled_evidence_intake_planning_gate,
)


def _complete_metadata(**overrides):
    metadata = {
        "evidence_category": "DEVELOPER_LOG",
        "source_repo": "ezeas-intelligence",
        "source_phase": "governed corpus intake planning",
        "source_status": "PLANNING_EVIDENCE",
        "trust_level": "CONTROLLED_INTERNAL",
        "required_caveats": ("Planning only.",),
    }
    metadata.update(overrides)
    return metadata


def _gate(**overrides):
    return build_controlled_evidence_intake_planning_gate(_complete_metadata(**overrides))


def test_complete_evidence_metadata_is_ready_for_intake_planning():
    result = _gate()

    assert result["gate_decision"] == READY_FOR_INTAKE_PLANNING
    assert result["ready_for_future_intake_planning"] is True


def test_missing_source_context_requires_source_context():
    result = _gate(source_repo="", source_phase="")

    assert result["gate_decision"] == NEEDS_SOURCE_CONTEXT
    assert "source_context" in result["missing_prerequisites"]


def test_missing_status_boundary_requires_status_boundary():
    result = _gate(source_status="")

    assert result["gate_decision"] == NEEDS_STATUS_BOUNDARY
    assert "status_boundary" in result["missing_prerequisites"]


def test_unknown_trust_requires_trust_review():
    result = _gate(trust_level="UNKNOWN")

    assert result["gate_decision"] == NEEDS_TRUST_REVIEW
    assert "trust_level" in result["missing_prerequisites"]


def test_runtime_or_production_overstatement_is_blocked():
    result = _gate(runtime_claim_permitted=True)

    assert result["gate_decision"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert "runtime_or_production_overstatement" in result["blocked_reasons"]


def test_unauthorised_ingestion_claim_is_blocked():
    result = _gate(ingestion_authorised=True)

    assert result["gate_decision"] == BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    assert "unauthorised_ingestion_claim" in result["blocked_reasons"]


def test_ingestion_authorised_now_is_always_false():
    assert _gate()["ingestion_authorised_now"] is False
    assert _gate(ingestion_authorised=True)["ingestion_authorised_now"] is False


def test_corpus_mutation_authorised_now_is_always_false():
    assert _gate()["corpus_mutation_authorised_now"] is False
    assert _gate(corpus_mutation_authorised=True)["corpus_mutation_authorised_now"] is False


def test_output_is_deterministic():
    metadata = _complete_metadata()

    assert build_controlled_evidence_intake_planning_gate(metadata) == build_controlled_evidence_intake_planning_gate(metadata)

from app.services.evidence_source_status_boundary_service import (
    ANALYSIS_EVIDENCE,
    CONTROLLED_READINESS_EVIDENCE,
    DEPLOYMENT_EVIDENCE,
    IMPLEMENTATION_CANDIDATE_EVIDENCE,
    PLANNING_EVIDENCE,
    PRODUCTION_EVIDENCE,
    RUNTIME_EVIDENCE,
    UNKNOWN_REQUIRES_REVIEW,
    build_evidence_source_status_boundary,
)


def _boundary(source_status, **overrides):
    metadata = {"source_status": source_status}
    metadata.update(overrides)
    return build_evidence_source_status_boundary(metadata)


def test_controlled_readiness_evidence_does_not_imply_runtime():
    result = _boundary(CONTROLLED_READINESS_EVIDENCE)

    assert result["runtime_claim_permitted"] is False
    assert "runtime readiness" in result["prohibited_inferences"]


def test_planning_evidence_does_not_imply_implementation():
    result = _boundary(PLANNING_EVIDENCE)

    assert result["implementation_claim_permitted"] is False
    assert "implementation completed" in result["prohibited_inferences"]


def test_analysis_evidence_does_not_imply_repair_completed():
    result = _boundary(ANALYSIS_EVIDENCE)

    assert result["implementation_claim_permitted"] is False
    assert "repair completed" in result["prohibited_inferences"]


def test_implementation_candidate_evidence_does_not_imply_deployed_or_runtime_enabled():
    result = _boundary(IMPLEMENTATION_CANDIDATE_EVIDENCE)

    assert result["deployment_claim_permitted"] is False
    assert result["runtime_claim_permitted"] is False
    assert "deployed" in result["prohibited_inferences"]


def test_runtime_evidence_requires_explicit_proof():
    without_proof = _boundary(RUNTIME_EVIDENCE)
    with_proof = _boundary(RUNTIME_EVIDENCE, explicit_proof=True)

    assert without_proof["runtime_claim_permitted"] is False
    assert with_proof["runtime_claim_permitted"] is True


def test_deployment_evidence_requires_explicit_proof():
    without_proof = _boundary(DEPLOYMENT_EVIDENCE)
    with_proof = _boundary(DEPLOYMENT_EVIDENCE, explicit_proof=True)

    assert without_proof["deployment_claim_permitted"] is False
    assert with_proof["deployment_claim_permitted"] is True


def test_production_evidence_requires_explicit_proof():
    without_proof = _boundary(PRODUCTION_EVIDENCE)
    with_proof = _boundary(PRODUCTION_EVIDENCE, explicit_proof=True)

    assert without_proof["production_claim_permitted"] is False
    assert with_proof["production_claim_permitted"] is True


def test_unknown_evidence_requires_review():
    result = _boundary("unregistered")

    assert result["source_status"] == UNKNOWN_REQUIRES_REVIEW
    assert result["evidence_exists"] is False


def test_output_is_deterministic():
    metadata = {"source_status": PLANNING_EVIDENCE, "source": "docs/example.md"}

    assert build_evidence_source_status_boundary(metadata) == build_evidence_source_status_boundary(metadata)

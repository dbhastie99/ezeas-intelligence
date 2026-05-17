from app.services.controlled_durable_evidence_intake_design_service import (
    build_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_evidence_intake_design_verification_service import (
    BLOCKED_DURABLE_INGESTION_CLAIM,
    BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED,
    NEEDS_AUDIT_ENVELOPE_REVIEW,
    NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW,
    NEEDS_DESIGN_REVIEW,
    verify_controlled_durable_evidence_intake_design,
)
from app.services.controlled_durable_intake_audit_envelope_service import (
    build_controlled_durable_intake_audit_envelope,
)
from app.services.controlled_durable_intake_authorisation_requirements_service import (
    build_controlled_durable_intake_authorisation_requirements,
)


def _design_metadata(**overrides):
    metadata = {
        "storage_boundary_model": "review-only source metadata; no corpus writes",
        "mutation_boundary_model": "future explicit gate required before mutation",
        "review_boundary_model": "reviewer confirmation required before action",
        "rollback_or_removal_policy": "rollback/removal policy must be approved",
    }
    metadata.update(overrides)
    return metadata


def _requirements_metadata(**overrides):
    metadata = {
        "reviewer_confirmation": True,
        "source_status_boundary": True,
        "evidence_envelope": True,
        "no_overstatement_check": True,
        "rollback_policy": True,
        "audit_metadata": True,
        "dry_run_review": True,
    }
    metadata.update(overrides)
    return metadata


def _audit_metadata(**overrides):
    metadata = {
        "source_reference": "controlled-no-mutation-envelope",
        "source_status": "CONTROLLED_READINESS_ONLY",
        "reviewer": "reviewer-id",
        "decision_timestamp": "2026-05-17T00:00:00Z",
        "no_mutation_history": "first no-mutation intake execution complete",
        "rollback_policy": "approved rollback/removal policy required",
        "prohibited_claims_checked": True,
        "sensitive_data_review": True,
    }
    metadata.update(overrides)
    return metadata


def _complete_design():
    return build_controlled_durable_evidence_intake_design(_design_metadata())


def _complete_requirements():
    return build_controlled_durable_intake_authorisation_requirements(
        _requirements_metadata()
    )


def _complete_audit():
    return build_controlled_durable_intake_audit_envelope(_audit_metadata())


def _verification(design=None, requirements=None, audit=None):
    return verify_controlled_durable_evidence_intake_design(
        _complete_design() if design is None else design,
        _complete_requirements() if requirements is None else requirements,
        _complete_audit() if audit is None else audit,
    )


def test_complete_design_requirements_audit_metadata_produces_verified_status():
    assert (
        _verification()["verification_status"]
        == DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED
    )


def test_missing_design_metadata_requires_design_review():
    assert _verification(design={})["verification_status"] == NEEDS_DESIGN_REVIEW


def test_missing_requirements_metadata_requires_authorisation_requirements_review():
    assert (
        _verification(requirements={})["verification_status"]
        == NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW
    )


def test_missing_audit_envelope_metadata_requires_audit_envelope_review():
    assert (
        _verification(audit={})["verification_status"]
        == NEEDS_AUDIT_ENVELOPE_REVIEW
    )


def test_storage_boundary_is_verified():
    assert _verification()["storage_boundary_verified"] is True


def test_mutation_boundary_is_verified():
    assert _verification()["mutation_boundary_verified"] is True


def test_review_boundary_is_verified():
    assert _verification()["review_boundary_verified"] is True


def test_rollback_policy_is_required():
    assert _verification()["rollback_policy_required"] is True


def test_sensitive_data_review_is_required():
    assert _verification()["sensitive_data_review_required"] is True


def test_no_overstatement_check_is_required():
    assert _verification()["no_overstatement_check_required"] is True


def test_dry_run_review_is_required():
    assert _verification()["dry_run_review_required"] is True


def test_durable_intake_authorised_now_is_false():
    assert _verification()["durable_intake_authorised_now"] is False


def test_corpus_mutation_authorised_now_is_false():
    assert _verification()["corpus_mutation_authorised_now"] is False


def test_db_write_authorised_now_is_false():
    assert _verification()["db_write_authorised_now"] is False


def test_code_evidence_ingestion_authorised_now_is_false():
    assert _verification()["code_evidence_ingestion_authorised_now"] is False


def test_durable_ingestion_claim_is_blocked():
    design = _complete_design()
    design["durable_intake_authorised_now"] = True

    result = _verification(design=design)

    assert result["verification_status"] == BLOCKED_DURABLE_INGESTION_CLAIM
    assert result["durable_intake_authorised_now"] is False


def test_runtime_or_production_overstatement_is_blocked():
    design = _complete_design()
    design["production_readiness_claim_permitted"] = True

    result = _verification(design=design)

    assert result["verification_status"] == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    assert result["db_write_authorised_now"] is False


def test_output_is_deterministic_for_repeated_input():
    design = _complete_design()
    requirements = _complete_requirements()
    audit = _complete_audit()

    assert _verification(design, requirements, audit) == _verification(
        design,
        requirements,
        audit,
    )

from app.services.controlled_evidence_intake_taxonomy_service import (
    ANALYTICS_READINESS_SUMMARY,
    AWARD_RECOVERY_ANALYSIS,
    DEVELOPER_LOG,
    HARDENING_LOG,
    PLATFORM_DOCTRINE,
    UNKNOWN_REQUIRES_REVIEW,
    build_controlled_evidence_intake_taxonomy,
)


def _classify(**metadata):
    return build_controlled_evidence_intake_taxonomy(metadata)


def test_developer_log_classification():
    result = _classify(source_type="developer log", source_repo="ezeas-intelligence")

    assert result["evidence_category"] == DEVELOPER_LOG


def test_hardening_log_classification():
    result = _classify(title="Minerva hardening log", source_repo="ezeas-intelligence")

    assert result["evidence_category"] == HARDENING_LOG


def test_platform_doctrine_classification():
    result = _classify(category="PLATFORM_DOCTRINE", source_repo="ezeas-intelligence")

    assert result["evidence_category"] == PLATFORM_DOCTRINE


def test_analytics_readiness_summary_classification():
    result = _classify(description="Analytics readiness summary for controlled planning")

    assert result["evidence_category"] == ANALYTICS_READINESS_SUMMARY


def test_award_recovery_analysis_classification():
    result = _classify(path="docs/award_recovery_analysis_outputs/example.md")

    assert result["evidence_category"] == AWARD_RECOVERY_ANALYSIS


def test_unknown_metadata_requires_review():
    result = _classify(title="unregistered external memo")

    assert result["evidence_category"] == UNKNOWN_REQUIRES_REVIEW
    assert result["trust_level"] == "UNKNOWN"


def test_no_category_authorises_ingestion():
    categories = (
        DEVELOPER_LOG,
        HARDENING_LOG,
        PLATFORM_DOCTRINE,
        ANALYTICS_READINESS_SUMMARY,
        AWARD_RECOVERY_ANALYSIS,
        UNKNOWN_REQUIRES_REVIEW,
    )

    for category in categories:
        assert _classify(evidence_category=category)["ingestion_authorised"] is False


def test_no_category_authorises_corpus_mutation():
    categories = (
        DEVELOPER_LOG,
        HARDENING_LOG,
        PLATFORM_DOCTRINE,
        ANALYTICS_READINESS_SUMMARY,
        AWARD_RECOVERY_ANALYSIS,
        UNKNOWN_REQUIRES_REVIEW,
    )

    for category in categories:
        assert _classify(evidence_category=category)["corpus_mutation_authorised"] is False


def test_no_category_permits_runtime_or_production_claims_by_default():
    result = _classify(evidence_category=DEVELOPER_LOG)

    assert result["runtime_claim_permitted"] is False
    assert result["production_claim_permitted"] is False


def test_output_is_deterministic():
    metadata = {
        "source_type": "developer log",
        "source_repo": "ezeas-intelligence",
        "source_phase": "governed corpus intake planning",
    }

    assert build_controlled_evidence_intake_taxonomy(metadata) == build_controlled_evidence_intake_taxonomy(metadata)

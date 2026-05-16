from app.services.candidate_answer_readiness_classifier_service import (
    classify_candidate_answer_readiness,
)


def test_controlled_readiness_no_action_text_is_safe_for_controlled_evaluation_only():
    result = classify_candidate_answer_readiness(
        "Minerva remains controlled-readiness only. No deployment, no runtime, "
        "no chat exposure, no DB access, no corpus mutation, and no Code Evidence ingestion."
    )

    assert result["readiness_classification"] == "SAFE_CONTROLLED_EVALUATION_ONLY"
    assert result["safe_for_controlled_evaluation"] is True
    assert result["safe_for_developer_handoff"] is False
    assert result["safe_for_final_answer_generation"] is False


def test_production_ready_claim_is_blocked():
    result = classify_candidate_answer_readiness("Minerva is production-ready.")

    assert result["readiness_classification"] == "BLOCKED_OVERSTATED_PRODUCTION"
    assert "PRODUCTION_READINESS_CLAIM" in result["prohibited_claims_detected"]


def test_deployed_claim_is_blocked():
    result = classify_candidate_answer_readiness("Minerva is deployed.")
    deferred = classify_candidate_answer_readiness(
        "Minerva remains controlled-readiness only. It is not deployed."
    )

    assert result["readiness_classification"] == "BLOCKED_OVERSTATED_DEPLOYMENT"
    assert "DEPLOYMENT_READINESS_CLAIM" in result["prohibited_claims_detected"]
    assert deferred["readiness_classification"] == "SAFE_CONTROLLED_EVALUATION_ONLY"


def test_runtime_enabled_claim_is_blocked():
    result = classify_candidate_answer_readiness("Minerva is runtime-enabled.")

    assert result["readiness_classification"] == "BLOCKED_OVERSTATED_RUNTIME"
    assert "RUNTIME_READINESS_CLAIM" in result["prohibited_claims_detected"]


def test_chat_exposure_enabled_claim_is_blocked():
    result = classify_candidate_answer_readiness("Internal chat enabled for Minerva.")

    assert result["readiness_classification"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert result["chat_exposure_claim_detected"] is True


def test_endpoint_exposure_enabled_claim_is_blocked():
    result = classify_candidate_answer_readiness("The API endpoint enabled Minerva access.")

    assert result["readiness_classification"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert result["endpoint_exposure_claim_detected"] is True


def test_final_answer_generation_enabled_claim_is_blocked():
    result = classify_candidate_answer_readiness("Final answer generation enabled.")

    assert (
        result["readiness_classification"]
        == "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM"
    )
    assert result["final_answer_generation_claim_detected"] is True


def test_live_llm_enabled_claim_is_blocked():
    result = classify_candidate_answer_readiness("Live LLM enabled for answer checks.")

    assert result["readiness_classification"] == "BLOCKED_LIVE_LLM_CLAIM"
    assert result["live_llm_claim_detected"] is True


def test_db_access_occurred_claim_is_blocked():
    result = classify_candidate_answer_readiness("DB access occurred during validation.")

    assert result["readiness_classification"] == "BLOCKED_DB_ACCESS_CLAIM"
    assert result["db_access_claim_detected"] is True


def test_db_validation_occurred_claim_is_blocked_unless_pending_or_not_performed():
    blocked = classify_candidate_answer_readiness("DB validation completed.")
    pending = classify_candidate_answer_readiness(
        "Minerva remains controlled-readiness only. DB validation pending and not performed."
    )

    assert blocked["readiness_classification"] == "BLOCKED_DB_ACCESS_CLAIM"
    assert blocked["db_validation_claim_detected"] is True
    assert pending["readiness_classification"] == "SAFE_CONTROLLED_EVALUATION_ONLY"
    assert pending["db_validation_claim_detected"] is False


def test_corpus_mutation_occurred_claim_is_blocked():
    result = classify_candidate_answer_readiness("Corpus mutation occurred.")

    assert (
        result["readiness_classification"]
        == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
    )
    assert result["corpus_mutation_claim_detected"] is True


def test_code_evidence_ingestion_occurred_claim_is_blocked():
    result = classify_candidate_answer_readiness("Code Evidence ingestion occurred.")

    assert (
        result["readiness_classification"]
        == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
    )
    assert result["code_evidence_ingestion_claim_detected"] is True


def test_workforce_platform_runtime_integration_occurred_claim_is_blocked():
    result = classify_candidate_answer_readiness(
        "Workforce-platform runtime integration occurred."
    )

    assert result["readiness_classification"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"
    assert result["workforce_runtime_integration_claim_detected"] is True


def test_analytics_runtime_integration_occurred_claim_is_blocked():
    result = classify_candidate_answer_readiness(
        "ezeas-analytics runtime integration occurred."
    )

    assert result["readiness_classification"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"
    assert result["analytics_runtime_integration_claim_detected"] is True


def test_ambiguous_status_without_caveat_requires_review():
    result = classify_candidate_answer_readiness("Minerva status looks good.")

    assert result["readiness_classification"] == "UNKNOWN_REQUIRES_REVIEW"
    assert result["safe_for_controlled_evaluation"] is False


def test_final_artefact_preference_plus_controlled_readiness_is_developer_handoff_only():
    result = classify_candidate_answer_readiness(
        {
            "status": "Prefer final/current artefact evidence.",
            "caveat": "Minerva remains controlled-readiness only. No runtime, no deployment, no chat exposure.",
        }
    )

    assert result["readiness_classification"] == "SAFE_CONTROLLED_EVALUATION_ONLY"
    assert result["safe_for_controlled_evaluation"] is True
    assert result["safe_for_developer_handoff"] is True
    assert result["safe_for_final_answer_generation"] is False

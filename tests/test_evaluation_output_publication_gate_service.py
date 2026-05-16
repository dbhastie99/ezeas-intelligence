from app.services.evaluation_output_publication_gate_service import (
    evaluate_evaluation_output_publication_gate,
)


def test_controlled_readiness_no_action_output_is_publishable_as_report_only():
    result = evaluate_evaluation_output_publication_gate(
        {
            "publication_target": "controlled evaluation report",
            "content": (
                "Minerva remains controlled-readiness only. No deployment, no runtime, "
                "no chat exposure, no DB access, no corpus mutation, and no Code Evidence ingestion."
            ),
        }
    )

    assert result["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    assert result["safe_for_controlled_evaluation_report"] is True
    assert result["safe_for_developer_handoff"] is False
    assert result["safe_for_progress_summary"] is False
    assert result["safe_for_final_answer_generation"] is False


def test_developer_handoff_output_with_caveats_is_publishable_as_handoff():
    result = evaluate_evaluation_output_publication_gate(
        {
            "publication_target": "developer handoff",
            "content": (
                "Developer handoff: Minerva remains controlled-readiness only. Runtime deferred, "
                "not deployed, no chat exposure, no DB access, no Code Evidence ingestion."
            ),
        }
    )

    assert result["publication_decision"] == "PUBLISH_DEVELOPER_HANDOFF"
    assert result["safe_for_developer_handoff"] is True
    assert result["safe_for_controlled_evaluation_report"] is False


def test_progress_summary_output_with_caveats_is_publishable_as_progress_summary():
    result = evaluate_evaluation_output_publication_gate(
        {
            "publication_target": "progress summary",
            "content": (
                "Progress summary: Minerva remains controlled-readiness only. No production, "
                "no deployment, no runtime, no endpoint, and no final natural-language answer generation."
            ),
        }
    )

    assert result["publication_decision"] == "PUBLISH_PROGRESS_SUMMARY"
    assert result["safe_for_progress_summary"] is True


def test_ambiguous_status_without_caveat_requires_caveat_or_human_review():
    result = evaluate_evaluation_output_publication_gate("Minerva status looks good.")

    assert result["publication_decision"] == "NEEDS_CAVEAT_BEFORE_PUBLICATION"
    assert result["human_review_required"] is True
    assert result["publication_blocked"] is False


def test_production_ready_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Minerva is production-ready.")

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_PRODUCTION"
    assert result["production_readiness_claim_detected"] is True
    assert "PRODUCTION_READINESS_CLAIM" in result["block_reasons"]


def test_deployed_or_deployment_ready_claim_is_blocked_unless_not_deployed():
    deployed = evaluate_evaluation_output_publication_gate("Minerva is deployed.")
    deployment_ready = evaluate_evaluation_output_publication_gate(
        "Minerva is deployment-ready."
    )
    deferred = evaluate_evaluation_output_publication_gate(
        "Minerva remains controlled-readiness only. It is not deployed."
    )

    assert deployed["publication_decision"] == "BLOCKED_OVERSTATED_DEPLOYMENT"
    assert deployment_ready["publication_decision"] == "BLOCKED_OVERSTATED_DEPLOYMENT"
    assert deferred["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"


def test_runtime_enabled_claim_is_blocked_unless_runtime_deferred():
    blocked = evaluate_evaluation_output_publication_gate("Minerva is runtime-enabled.")
    deferred = evaluate_evaluation_output_publication_gate(
        "Minerva remains controlled-readiness only. Runtime deferred."
    )

    assert blocked["publication_decision"] == "BLOCKED_OVERSTATED_RUNTIME"
    assert blocked["runtime_readiness_claim_detected"] is True
    assert deferred["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"


def test_chat_exposure_enabled_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Internal chat enabled for Minerva.")

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert result["chat_exposure_claim_detected"] is True


def test_endpoint_exposure_enabled_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("The API endpoint enabled Minerva access.")

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert result["endpoint_exposure_claim_detected"] is True


def test_final_answer_generation_enabled_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Final answer generation enabled.")

    assert result["publication_decision"] == "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM"
    assert result["final_answer_generation_claim_detected"] is True


def test_live_llm_enabled_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Live LLM enabled for answer checks.")

    assert result["publication_decision"] == "BLOCKED_LIVE_LLM_CLAIM"
    assert result["live_llm_claim_detected"] is True


def test_db_access_or_db_validation_claim_is_blocked_unless_pending_or_not_performed():
    db_access = evaluate_evaluation_output_publication_gate("DB access occurred during validation.")
    db_validation = evaluate_evaluation_output_publication_gate("DB validation completed.")
    pending = evaluate_evaluation_output_publication_gate(
        "Minerva remains controlled-readiness only. DB validation pending and not performed."
    )

    assert db_access["publication_decision"] == "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM"
    assert db_access["db_access_claim_detected"] is True
    assert db_validation["publication_decision"] == "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM"
    assert db_validation["db_validation_claim_detected"] is True
    assert pending["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    assert pending["db_validation_claim_detected"] is False


def test_corpus_mutation_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Corpus mutation occurred.")

    assert result["publication_decision"] == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
    assert result["corpus_mutation_claim_detected"] is True


def test_code_evidence_ingestion_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate("Code Evidence ingestion occurred.")

    assert result["publication_decision"] == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"
    assert result["code_evidence_ingestion_claim_detected"] is True


def test_workforce_platform_runtime_integration_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate(
        "Workforce-platform runtime integration occurred."
    )

    assert result["publication_decision"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"
    assert result["workforce_runtime_integration_claim_detected"] is True


def test_analytics_runtime_integration_claim_is_blocked():
    result = evaluate_evaluation_output_publication_gate(
        "ezeas-analytics runtime integration occurred."
    )

    assert result["publication_decision"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"
    assert result["analytics_runtime_integration_claim_detected"] is True


def test_nothing_is_safe_for_final_answer_generation_in_this_slice():
    result = evaluate_evaluation_output_publication_gate(
        "Minerva remains controlled-readiness only. No runtime, no deployment, no chat exposure."
    )

    assert result["safe_for_final_answer_generation"] is False


def test_output_is_deterministic_for_repeated_input():
    candidate = {
        "publication_target": "developer handoff",
        "content": (
            "Developer handoff: Minerva remains controlled-readiness only. No runtime, "
            "no deployment, no chat exposure, no DB access."
        ),
    }

    assert evaluate_evaluation_output_publication_gate(candidate) == (
        evaluate_evaluation_output_publication_gate(candidate)
    )

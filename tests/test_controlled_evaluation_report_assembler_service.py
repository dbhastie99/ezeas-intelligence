from app.services.controlled_evaluation_report_assembler_service import (
    assemble_controlled_evaluation_report,
)


def _base_metadata(report_type="CONTROLLED_EVALUATION_REPORT"):
    return {
        "report_title": "Minerva Controlled Evaluation Report",
        "report_type": report_type,
        "report_scope": "Internal controlled evaluation artefact only.",
        "current_status": "Minerva remains controlled-readiness only.",
        "evidence_inputs": ("final status", "no-action attestation"),
        "preferred_current_state_evidence": "Prefer final/current artefact evidence.",
        "controlled_readiness_summary": (
            "Minerva remains controlled-readiness only. No production, no deployment, "
            "runtime deferred, no chat exposure, no endpoint, no DB access, "
            "DB validation pending and not performed, no corpus mutation, "
            "no Code Evidence ingestion, no workforce-platform runtime integration, "
            "no ezeas-analytics runtime integration, live LLM use remains deferred, "
            "and no final natural-language answer generation."
        ),
        "blocked_or_deferred_capabilities": ("internal chat exposure deferred",),
        "no_action_attestation": "No action was taken against runtime, DB, corpus, routes, or integrations.",
        "risks_and_unknowns": ("Runtime and DB validation remain deferred.",),
        "recommended_next_slice": "Keep final answer generation deferred.",
        "developer_handoff": "Use only as controlled metadata.",
    }


def test_controlled_readiness_no_action_metadata_assembles_controlled_evaluation_report():
    result = assemble_controlled_evaluation_report(_base_metadata())

    assert result["report_type"] == "CONTROLLED_EVALUATION_REPORT"
    assert result["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    assert result["safe_for_controlled_evaluation_report"] is True
    assert result["safe_for_final_answer_generation"] is False
    assert result["sections"]["no_action_attestation"]


def test_developer_handoff_metadata_with_caveats_assembles_handoff_report():
    metadata = _base_metadata("DEVELOPER_HANDOFF")
    metadata["report_title"] = "Minerva Developer Handoff"

    result = assemble_controlled_evaluation_report(metadata)

    assert result["report_type"] == "DEVELOPER_HANDOFF"
    assert result["publication_decision"] == "PUBLISH_DEVELOPER_HANDOFF"
    assert result["safe_for_developer_handoff"] is True
    assert result["safe_for_controlled_evaluation_report"] is False


def test_progress_summary_metadata_with_caveats_assembles_progress_summary():
    metadata = _base_metadata("PROGRESS_SUMMARY")

    result = assemble_controlled_evaluation_report(metadata)

    assert result["report_type"] == "PROGRESS_SUMMARY"
    assert result["publication_decision"] == "PUBLISH_PROGRESS_SUMMARY"
    assert result["safe_for_progress_summary"] is True


def test_next_slice_recommendation_metadata_assembles_next_slice_report():
    metadata = _base_metadata("NEXT_SLICE_RECOMMENDATION")
    metadata["recommended_next_slice"] = "Next-slice recommendation: add a deterministic review checklist."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["report_type"] == "NEXT_SLICE_RECOMMENDATION"
    assert result["publication_decision"] == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    assert result["safe_for_controlled_evaluation_report"] is True
    assert result["recommended_next_slice"] == metadata["recommended_next_slice"]


def test_ambiguous_metadata_without_caveat_requires_review_or_missing_caveat_output():
    result = assemble_controlled_evaluation_report({"current_status": "Minerva status looks good."})

    assert result["report_type"] == "UNKNOWN_REQUIRES_REVIEW"
    assert result["safe_for_controlled_evaluation_report"] is False
    assert result["missing_caveats"]


def test_production_ready_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Minerva is production-ready."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_PRODUCTION"
    assert result["safe_for_controlled_evaluation_report"] is False
    assert "PRODUCTION_READINESS" in result["violated_boundaries"]


def test_deployed_or_deployment_ready_claim_blocks_safe_report_output():
    deployed = _base_metadata()
    deployed["current_status"] = "Minerva is deployed."
    deployment_ready = _base_metadata()
    deployment_ready["current_status"] = "Minerva is deployment-ready."

    assert (
        assemble_controlled_evaluation_report(deployed)["publication_decision"]
        == "BLOCKED_OVERSTATED_DEPLOYMENT"
    )
    assert (
        assemble_controlled_evaluation_report(deployment_ready)["publication_decision"]
        == "BLOCKED_OVERSTATED_DEPLOYMENT"
    )


def test_runtime_enabled_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Minerva is runtime-enabled."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_RUNTIME"
    assert result["safe_for_controlled_evaluation_report"] is False


def test_chat_exposure_enabled_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Internal chat enabled for Minerva."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert "CHAT_EXPOSURE" in result["violated_boundaries"]


def test_endpoint_exposure_enabled_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "The API endpoint enabled Minerva access."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_OVERSTATED_EXPOSURE"
    assert "ENDPOINT_EXPOSURE" in result["violated_boundaries"]


def test_final_answer_generation_enabled_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Final natural-language answer generation enabled."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM"
    assert result["safe_for_final_answer_generation"] is False


def test_live_llm_enabled_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Live LLM enabled for answer checks."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_LIVE_LLM_CLAIM"


def test_db_access_or_db_validation_claim_blocks_unless_pending_or_not_performed():
    db_access = _base_metadata()
    db_access["current_status"] = "DB access occurred during validation."
    db_validation = _base_metadata()
    db_validation["current_status"] = "DB validation completed."
    pending = _base_metadata()
    pending["current_status"] = (
        "Minerva remains controlled-readiness only. DB validation pending and not performed."
    )

    assert (
        assemble_controlled_evaluation_report(db_access)["publication_decision"]
        == "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM"
    )
    assert (
        assemble_controlled_evaluation_report(db_validation)["publication_decision"]
        == "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM"
    )
    assert (
        assemble_controlled_evaluation_report(pending)["publication_decision"]
        == "PUBLISH_CONTROLLED_EVALUATION_REPORT"
    )


def test_corpus_mutation_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Corpus mutation occurred."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"


def test_code_evidence_ingestion_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Code Evidence ingestion occurred."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM"


def test_workforce_platform_runtime_integration_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "Workforce-platform runtime integration occurred."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"


def test_analytics_runtime_integration_claim_blocks_safe_report_output():
    metadata = _base_metadata()
    metadata["current_status"] = "ezeas-analytics runtime integration occurred."

    result = assemble_controlled_evaluation_report(metadata)

    assert result["publication_decision"] == "BLOCKED_CROSS_REPO_RUNTIME_CLAIM"


def test_output_is_never_safe_for_final_answer_generation():
    result = assemble_controlled_evaluation_report(_base_metadata())

    assert result["safe_for_final_answer_generation"] is False
    assert result["sections"]["safe_for_final_answer_generation"] is False


def test_output_is_deterministic_for_repeated_input():
    metadata = _base_metadata("DEVELOPER_HANDOFF")

    assert assemble_controlled_evaluation_report(metadata) == assemble_controlled_evaluation_report(
        metadata
    )


def test_explicit_no_action_and_deferred_boundaries_are_preserved_in_report_sections():
    result = assemble_controlled_evaluation_report(_base_metadata())

    assert "RUNTIME_DEFERRED" in result["sections"]["preserved_boundaries"]
    assert "CHAT_EXPOSURE_DEFERRED" in result["sections"]["preserved_boundaries"]
    assert "DB_ACCESS_DEFERRED" in result["sections"]["preserved_boundaries"]
    assert "runtime enablement deferred" in result["sections"]["blocked_or_deferred_capabilities"]
    assert result["sections"]["no_action_attestation"].startswith("No action was taken")

from app.services.controlled_readiness_status_guard_service import (
    evaluate_controlled_readiness_status_guard,
    recognize_controlled_readiness_evidence_type,
)


def test_final_index_beats_older_design_pack():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "DESIGN_PACK",
                "content": "Older design pack suggested future implementation candidate work.",
            },
            {
                "evidence_type": "FINAL_INDEX",
                "content": "Final index records controlled-readiness complete, exposure deferred.",
            },
        ]
    )

    assert result["preferred_evidence_type"] == "FINAL_INDEX"
    assert result["current_state_confidence"] == "HIGH"
    assert result["exposure_deferred_preserved"] is True


def test_final_status_beats_implementation_candidate():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "IMPLEMENTATION_CANDIDATE",
                "content": "Implementation candidate only; not approval for runtime.",
            },
            {
                "evidence_type": "FINAL_STATUS",
                "content": "Final status says controlled-readiness only and no internal chat exposure.",
            },
        ]
    )

    assert result["preferred_evidence_type"] == "FINAL_STATUS"
    assert "IMPLEMENTATION_CANDIDATE_IS_NOT_RUNTIME_APPROVAL" in result["prohibited_overstatements"]


def test_resume_map_beats_midstream_planning_note():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "MIDSTREAM_PLANNING_NOTE",
                "content": "Midstream planning note considered possible later endpoint work.",
            },
            {
                "evidence_type": "RESUME_MAP",
                "content": "Resume map says future work requires explicit approval and no deployment.",
            },
        ]
    )

    assert result["preferred_evidence_type"] == "RESUME_MAP"
    assert result["deployment_deferred_preserved"] is True


def test_no_action_attestation_preserves_not_implemented_not_exposed_not_deployed():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "NO_ACTION_ATTESTATION",
                "content": "No-action attestation: not implemented, not exposed, not deployed.",
            }
        ]
    )

    assert result["preferred_evidence_type"] == "NO_ACTION_ATTESTATION"
    assert result["runtime_deferred_preserved"] is True
    assert result["exposure_deferred_preserved"] is True
    assert result["deployment_deferred_preserved"] is True


def test_controlled_readiness_is_not_production_readiness():
    result = evaluate_controlled_readiness_status_guard(
        [{"evidence_type": "FINAL_STATUS", "content": "Controlled-readiness only."}]
    )

    assert result["production_readiness_claim_permitted"] is False
    assert "CONTROLLED_READINESS_IS_NOT_PRODUCTION_READINESS" in result["prohibited_overstatements"]


def test_controlled_readiness_is_not_deployment_readiness():
    result = evaluate_controlled_readiness_status_guard(
        [{"evidence_type": "FINAL_STATUS", "content": "Controlled-readiness only."}]
    )

    assert "CONTROLLED_READINESS_IS_NOT_DEPLOYMENT_READINESS" in result["prohibited_overstatements"]


def test_controlled_readiness_is_not_runtime_readiness():
    result = evaluate_controlled_readiness_status_guard(
        [{"evidence_type": "FINAL_STATUS", "content": "Controlled-readiness only."}]
    )

    assert "CONTROLLED_READINESS_IS_NOT_RUNTIME_READINESS" in result["prohibited_overstatements"]


def test_minerva_exposure_deferred_language_is_preserved():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "CLOSEOUT",
                "content": "Minerva exposure-deferred boundary remains: no internal chat exposure.",
            }
        ]
    )

    assert result["exposure_deferred_preserved"] is True
    assert "EXPOSURE_DEFERRED" in result["status_terms_detected"]


def test_workforce_runtime_creation_deferred_language_is_preserved():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "FINAL_STATUS",
                "content": "Workforce runtime-creation-deferred language remains in evidence.",
            }
        ]
    )

    assert result["runtime_deferred_preserved"] is True
    assert "RUNTIME_DEFERRED" in result["status_terms_detected"]


def test_analytics_deployment_and_db_validation_deferred_language_is_preserved():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "FINAL_STATUS",
                "content": "Analytics deployment-deferred / DB-validation-deferred language remains.",
            }
        ]
    )

    assert result["deployment_deferred_preserved"] is True
    assert "DB_VALIDATION_DEFERRED" in result["status_terms_detected"]


def test_unknown_evidence_type_requires_caveat_and_fallback():
    result = evaluate_controlled_readiness_status_guard(
        [{"evidence_type": "unlabelled note", "content": "Some unclassified status text."}]
    )

    assert result["preferred_evidence_type"] == "UNKNOWN"
    assert result["fallback_required"] is True
    assert result["current_state_confidence"] == "LOW"
    assert any("Unknown evidence type" in caveat for caveat in result["required_caveats"])


def test_implementation_candidate_is_not_approval():
    result = evaluate_controlled_readiness_status_guard(
        [{"evidence_type": "IMPLEMENTATION_CANDIDATE", "content": "Candidate only."}]
    )

    assert result["preferred_evidence_type"] == "IMPLEMENTATION_CANDIDATE"
    assert "IMPLEMENTATION_CANDIDATE_IS_NOT_EXPOSURE_APPROVAL" in result["prohibited_overstatements"]
    assert "IMPLEMENTATION_CANDIDATE_IS_NOT_DEPLOYMENT_APPROVAL" in result["prohibited_overstatements"]
    assert "IMPLEMENTATION_CANDIDATE_IS_NOT_RUNTIME_APPROVAL" in result["prohibited_overstatements"]
    assert "IMPLEMENTATION_CANDIDATE_IS_NOT_PRODUCTION_APPROVAL" in result["prohibited_overstatements"]


def test_guard_never_claims_final_natural_language_answer_generation_enabled():
    result = evaluate_controlled_readiness_status_guard(
        [
            {
                "evidence_type": "FINAL_INDEX",
                "content": "No final natural-language answer generation is authorised.",
            }
        ]
    )

    assert result["final_answer_generation_claim_permitted"] is False
    assert "FINAL_NATURAL_LANGUAGE_ANSWER_GENERATION_NOT_ENABLED" in result["prohibited_overstatements"]


def test_recognizes_evidence_type_from_content_when_type_missing():
    evidence_type = recognize_controlled_readiness_evidence_type(
        {"title": "Historical read-only chat pilot final index", "content": "Controlled-readiness only."}
    )

    assert evidence_type == "FINAL_INDEX"

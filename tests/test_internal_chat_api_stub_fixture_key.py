from pathlib import Path

from app.services.internal_chat_api_stub_service import InternalChatApiStubService
from app.services.internal_chat_evidence_fixture_harness_service import InternalChatFixtureKey
from app.services.internal_chat_orchestrator_service import InternalChatRole, InternalChatSourceScope


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_fixture_key_api_support_v0_1.md"
EVALUATION_DIR = ROOT / "docs" / "evaluation" / "minerva_internal_chat_fixture_key_api_support_v0_1"
EVALUATION_BASELINE = EVALUATION_DIR / "FIXTURE_KEY_API_BASELINE.md"
SAMPLE_RESPONSES = EVALUATION_DIR / "FIXTURE_KEY_SAMPLE_RESPONSES.json"
PROMPT_ARTEFACT = ROOT / "docs" / "codex_prompts" / "2026-05-22_minerva_internal_chat_fixture_key_api_support_v01.md"


def _service() -> InternalChatApiStubService:
    return InternalChatApiStubService()


def _request(**overrides) -> dict:
    payload = {
        "Question": "Can the platform manually process an admitted draft action?",
        "Role": InternalChatRole.PAYROLL_ADMINISTRATOR.value,
        "SourceScopes": [],
        "DomainTags": [],
        "CandidateEvidence": [],
    }
    payload.update(overrides)
    return payload


def _response(**overrides) -> dict:
    return _service().build_response(_request(**overrides)).model_dump()


def _explicit_evidence() -> dict:
    return {
        "source_type": "IMPLEMENTATION_STATE_DOC",
        "evidence_category": "IMPLEMENTATION_STATE",
        "source_scope": InternalChatSourceScope.IMPLEMENTATION_STATE.value,
        "title": "explicit implementation note",
        "summary": "Explicit caller evidence must be preserved before fixture evidence.",
        "evidence_tags": ["explicit", "manual"],
    }


def test_request_without_fixture_key_remains_compatible():
    response = _response(
        SourceScopes=[InternalChatSourceScope.IMPLEMENTATION_STATE.value],
        CandidateEvidence=[_explicit_evidence()],
        DomainTags=["manual"],
    )

    assert response["Status"] == "STUB_RESPONSE_BUILT"
    assert response["FixtureEvidence"]["FixtureEvidenceUsed"] is False
    assert response["RequestEcho"]["FixtureKey"] is None


def test_valid_fixture_key_resolves_fixture_and_supplies_candidate_evidence():
    response = _response(
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value
    )

    assert response["Status"] == "STUB_RESPONSE_BUILT"
    assert response["FixtureEvidence"]["FixtureKey"] == "ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED"
    assert response["FixtureEvidence"]["FixtureEvidenceUsed"] is True
    assert response["RequestEcho"]["CandidateEvidenceCount"] > 0
    assert response["EvidenceSupportPacket"]["support_status"] == "SUPPORTED"


def test_explicit_candidate_evidence_is_preserved_and_fixture_evidence_appended():
    response = _response(
        CandidateEvidence=[_explicit_evidence()],
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )
    packet = response["EvidenceSupportPacket"]

    assert response["FixtureEvidence"]["ExplicitCandidateEvidenceCount"] == 1
    assert response["FixtureEvidence"]["MergedCandidateEvidenceCount"] > 1
    assert packet["implementation_state_evidence"][0]["title"] == "explicit implementation note"


def test_domain_tags_are_merged_deterministically():
    response = _response(
        DomainTags=["explicit", "manual"],
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )

    assert response["RequestEcho"]["DomainTags"] == [
        "explicit",
        "manual",
        "admitted",
        "draft",
        "processing",
        "payrun",
        "action",
    ]


def test_source_scopes_are_merged_deterministically():
    response = _response(
        SourceScopes=[InternalChatSourceScope.CODE_EVIDENCE.value],
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )

    assert response["RequestEcho"]["SourceScopes"] == [
        "CODE_EVIDENCE",
        "PLATFORM_KNOWLEDGE",
        "IMPLEMENTATION_STATE",
        "TEST_EVIDENCE",
        "PROMPT_ARTEFACTS",
        "EVALUATION_BASELINES",
    ]


def test_response_includes_fixture_evidence_metadata_and_warning():
    response = _response(
        FixtureKey=InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES.value
    )

    fixture = response["FixtureEvidence"]
    assert fixture["FixtureEvidenceUsed"] is True
    assert fixture["FixtureEvidenceSynthetic"] is True
    assert fixture["FixtureEvidenceStatus"] == "SUPPORTED"
    assert "synthetic/internal test evidence" in fixture["FixtureEvidenceWarning"]
    assert any("does not prove runtime/customer availability" in caveat for caveat in response["RequiredCaveats"])


def test_developer_fixture_response_can_include_technical_evidence():
    response = _response(
        Role=InternalChatRole.DEVELOPER.value,
        Question="What evidence supports manual admitted draft action processing?",
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )
    dumped = str(response)

    assert "app/services/admitted_draft_payrun_processing_bridge_service.py" in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" in dumped


def test_payroll_user_fixture_response_does_not_expose_technical_names():
    response = _response(
        Role=InternalChatRole.PAYROLL_USER.value,
        Question="What should I do with this post-finalisation ObjectTime action?",
        FixtureKey=InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED.value,
    )
    dumped = str(response)

    assert "The platform can support this workflow" in response["DeterministicDraft"]["DraftText"]
    assert "app/services/post_finalisation_objecttime_action_service.py" not in dumped
    assert "PostFinalisationObjectTimeActionService" not in dumped
    assert "test_post_finalisation_objecttime_action_keeps_finalised_payrun_protected" not in dumped


def test_worker_fixture_response_remains_role_restricted_for_code_evidence():
    response = _response(
        Role=InternalChatRole.WORKER.value,
        Question="What evidence supports manual admitted draft action processing?",
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )

    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_ROLE_RESTRICTED"
    assert response["EvidenceSupportPacket"]["code_evidence"] == []
    assert response["EvidenceSupportPacket"]["test_evidence"] == []


def test_invalid_fixture_key_returns_deterministic_invalid_response():
    response = _response(FixtureKey="NOT_A_FIXTURE")

    assert response["Status"] == "INVALID_FIXTURE_KEY"
    assert response["AnswerPermitted"] is False
    assert response["OrchestratorEnvelope"]["AnswerPermitted"] is False
    assert response["DeterministicDraft"] is None
    assert "AvailableFixtureKeys" in response["FixtureEvidence"]


def test_invalid_fixture_key_does_not_call_live_llm_or_generate_final_answer():
    response = _response(FixtureKey="NOT_A_FIXTURE", AllowLiveLlm=True, AllowFinalAnswerGeneration=True)

    assert response["LiveLlmUsed"] is False
    assert response["IsFinalAnswer"] is False
    assert response["FinalAnswerText"] is None
    assert response["FinalAnswerGenerationPermitted"] is False
    assert response["NoActionAttestation"]["LiveLlmCalled"] is False
    assert response["NoActionAttestation"]["FinalAnswerGenerated"] is False


def test_fixture_backed_response_remains_non_final_no_live_llm_and_no_action():
    response = _response(
        FixtureKey=InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED.value
    )

    assert response["IsFinalAnswer"] is False
    assert response["LiveLlmUsed"] is False
    assert response["NoActionAttestation"]["WriteActionPerformed"] is False
    assert "No live LLM called" in response["NoActionAttestationText"]


def test_fixture_evidence_is_not_treated_as_runtime_object_evidence():
    response = _response(
        Question="Is this implementation enabled for my tenant in production?",
        Role=InternalChatRole.CUSTOMER_ADMINISTRATOR.value,
        FixtureKey=InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME.value,
    )

    assert response["FixtureEvidence"]["RuntimeObjectEvidenceFetched"] is False
    assert response["FixtureEvidence"]["RuntimeObjectEvidenceSupplied"] is False
    assert response["DisclosureMetadata"]["RuntimeObjectEvidenceFetched"] is False
    assert response["DisclosureMetadata"]["ProductionAvailabilityConfirmed"] is False
    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_RUNTIME_EVIDENCE_REQUIRED"


def test_api_route_accepts_fixture_key(client):
    response = client.post(
        "/api/v1/internal/minerva/chat/stub",
        json=_request(
            FixtureKey=InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES.value
        ),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["Status"] == "STUB_RESPONSE_BUILT"
    assert body["FixtureEvidence"]["FixtureEvidenceUsed"] is True
    assert body["RequestEcho"]["FixtureKey"] == "ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES"


def test_fixture_key_docs_and_samples_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert SAMPLE_RESPONSES.exists()
    assert PROMPT_ARTEFACT.exists()

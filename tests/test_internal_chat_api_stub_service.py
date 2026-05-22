from pathlib import Path

from app.services.internal_chat_api_stub_service import (
    InternalChatApiStubService,
    NO_ACTION_ATTESTATION,
)
from app.services.internal_chat_orchestrator_service import InternalChatRole, InternalChatSourceScope


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_api_stub_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_api_stub_v0_1"
    / "API_STUB_BASELINE.md"
)
PROMPT_ARTEFACT = ROOT / "docs" / "codex_prompts" / "2026-05-22_minerva_internal_chat_api_stub_v01.md"
SAMPLE_RESPONSE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_api_stub_v0_1"
    / "INTERNAL_CHAT_API_STUB_SAMPLE_RESPONSE.json"
)


def _service() -> InternalChatApiStubService:
    return InternalChatApiStubService()


def _sample_evidence() -> list[dict]:
    return [
        {
            "source_type": "DOCTRINE",
            "evidence_category": "DOCTRINE",
            "title": "Manual admitted draft processing doctrine",
            "summary": "Admitted draft actions require governed manual processing support.",
            "tags": ["manual", "admitted", "draft", "processing", "payrun"],
        },
        {
            "source_type": "IMPLEMENTATION_STATE_DOC",
            "evidence_category": "IMPLEMENTATION_STATE",
            "title": "manual admitted draft processing implementation state",
            "file_path": "docs/evaluation/admitted_draft/IMPLEMENTATION_STATE_BASELINE.md",
            "tags": ["manual", "admitted", "draft", "processing", "implementation_state"],
        },
        {
            "source_type": "ROUTE_DEFINITION",
            "evidence_category": "CODE",
            "title": "manual admitted draft processing endpoint",
            "repo_name": "workforce-platform",
            "repo_family": "WORKFORCE_PLATFORM",
            "file_path": "app/routes/payroll/admitted_draft_actions.py",
            "route_path": "/payruns/{payrun_id}/admitted-draft-actions/{action_id}/process",
            "tags": ["manual", "admitted", "draft", "processing", "endpoint", "implementation_support"],
        },
        {
            "source_type": "SERVICE_CLASS",
            "evidence_category": "CODE",
            "title": "AdmittedDraftPayRunProcessingBridgeService",
            "repo_name": "workforce-platform",
            "repo_family": "WORKFORCE_PLATFORM",
            "file_path": "app/services/admitted_draft_payrun_processing_bridge_service.py",
            "symbol_name": "AdmittedDraftPayRunProcessingBridgeService",
            "tags": ["manual", "admitted", "draft", "processing", "implementation_support"],
        },
        {
            "source_type": "TEST_FILE",
            "evidence_category": "TEST",
            "title": "manual admitted draft processing bridge test",
            "repo_name": "ezeas-intelligence",
            "repo_family": "MINERVA",
            "file_path": "tests/test_admitted_draft_payrun_processing_bridge_source_response.py",
            "test_name": "test_manual_admitted_draft_processing_bridge_evidence",
            "tags": ["manual", "admitted", "draft", "processing", "behavioural_evidence"],
        },
        {
            "source_type": "PROMPT_ARTEFACT",
            "evidence_category": "PROMPT",
            "title": "manual admitted draft processing prompt",
            "file_path": "docs/codex_prompts/2026-05-21_manual_admitted_draft_processing.md",
            "tags": ["manual", "admitted", "draft", "processing", "prompt"],
        },
        {
            "source_type": "EVALUATION_DOC",
            "evidence_category": "EVALUATION",
            "title": "manual admitted draft processing evaluation baseline",
            "file_path": "docs/evaluation/admitted_draft/ANSWER_SUPPORT_BASELINE.md",
            "tags": ["manual", "admitted", "draft", "processing", "evaluation"],
        },
    ]


def _request(role=InternalChatRole.DEVELOPER, question=None, **overrides) -> dict:
    payload = {
        "Question": question or "Where is the manual admitted draft processing endpoint implemented?",
        "Role": role.value if isinstance(role, InternalChatRole) else role,
        "SourceScopes": [
            InternalChatSourceScope.PLATFORM_KNOWLEDGE.value,
            InternalChatSourceScope.IMPLEMENTATION_STATE.value,
            InternalChatSourceScope.CODE_EVIDENCE.value,
            InternalChatSourceScope.TEST_EVIDENCE.value,
            InternalChatSourceScope.PROMPT_ARTEFACTS.value,
            InternalChatSourceScope.EVALUATION_BASELINES.value,
        ],
        "DomainTags": ["manual", "admitted", "draft", "processing"],
        "CandidateEvidence": _sample_evidence(),
    }
    payload.update(overrides)
    return payload


def _response(role=InternalChatRole.DEVELOPER, question=None, **overrides) -> dict:
    return _service().build_response(_request(role=role, question=question, **overrides)).model_dump()


def test_developer_request_returns_orchestrator_envelope_and_deterministic_draft():
    response = _response(InternalChatRole.DEVELOPER)

    assert response["Status"] == "STUB_RESPONSE_BUILT"
    assert response["OrchestratorEnvelope"]["Status"] == "ANSWER_SUPPORT_BUILT"
    assert response["EvidenceSupportPacket"]["support_status"] == "SUPPORTED"
    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_READY"
    assert "app/routes/payroll/admitted_draft_actions.py" in str(response["OrchestratorEnvelope"])


def test_payroll_administrator_returns_implementation_confirmation_style_and_runtime_caveat():
    response = _response(
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Can the platform manually process an admitted draft action?",
    )

    assert response["DisclosureMetadata"]["DisclosureMode"] == "IMPLEMENTATION_CONFIRMATION"
    assert "Current implementation evidence supports this capability" in response["DeterministicDraft"]["DraftText"]
    assert any("cannot prove production availability" in caveat for caveat in response["RequiredCaveats"])


def test_payroll_user_response_hides_technical_file_function_and_test_names():
    response = _response(
        InternalChatRole.PAYROLL_USER,
        question="What should I do with this post-finalisation ObjectTime action?",
    )
    dumped = str(response)

    assert "The platform can support this workflow" in response["DeterministicDraft"]["DraftText"]
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" not in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" not in dumped


def test_customer_administrator_includes_customer_availability_caveat():
    response = _response(
        InternalChatRole.CUSTOMER_ADMINISTRATOR,
        question="Is this feature enabled for my tenant?",
    )

    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_RUNTIME_EVIDENCE_REQUIRED"
    assert response["DisclosureMetadata"]["CustomerAvailabilityConfirmed"] is False
    assert any("tenant, or customer availability" in caveat for caveat in response["RequiredCaveats"])


def test_worker_code_request_is_role_restricted_and_has_no_code_evidence():
    response = _response(InternalChatRole.WORKER, question="Can I see the code behind my payslip?")
    dumped = str(response)

    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_ROLE_RESTRICTED"
    assert response["EvidenceSupportPacket"]["code_evidence"] == []
    assert "raw code disclosure request blocked" in response["BlockedClaims"]
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped


def test_allow_live_llm_true_does_not_call_llm():
    response = _response(AllowLiveLlm=True)

    assert response["OrchestratorEnvelope"]["Status"] == "LIVE_LLM_DISABLED"
    assert response["LiveLlmUsed"] is False
    assert response["NoActionAttestation"]["LiveLlmCalled"] is False
    assert "LIVE_LLM_DISABLED" in response["Boundaries"]


def test_allow_final_answer_generation_true_still_returns_non_final_response():
    response = _response(AllowFinalAnswerGeneration=True)

    assert response["OrchestratorEnvelope"]["Status"] == "FINAL_ANSWER_GENERATION_DISABLED"
    assert response["IsFinalAnswer"] is False
    assert response["FinalAnswerText"] is None
    assert response["FinalAnswerGenerationPermitted"] is False


def test_runtime_object_scope_without_evidence_returns_needs_evidence_or_unsupported_scope():
    response = _response(
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Why did this worker get overtime?",
        SourceScopes=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE.value],
        CandidateEvidence=[],
        DomainTags=["overtime"],
    )

    assert response["OrchestratorEnvelope"]["Status"] in {"NEEDS_MORE_EVIDENCE", "UNSUPPORTED_SCOPE"}
    assert "RUNTIME_OBJECT_EVIDENCE" in response["UnsupportedScopes"]
    assert response["NoActionAttestation"]["RuntimeObjectEvidenceFetched"] is False


def test_analytics_scope_returns_deferred_inactive_status_without_safe_metadata():
    response = _response(
        InternalChatRole.ANALYTICS_USER,
        question="Explain this payroll trend chart.",
        SourceScopes=[InternalChatSourceScope.ANALYTICS_EVIDENCE.value],
        CandidateEvidence=[],
        DomainTags=["analytics", "trend"],
    )

    assert response["OrchestratorEnvelope"]["Status"] == "UNSUPPORTED_SCOPE"
    assert "ANALYTICS_EVIDENCE" in response["UnsupportedScopes"]
    assert any("inactive by default" in caveat for caveat in response["RequiredCaveats"])


def test_payroll_calculation_and_write_requests_are_blocked():
    calculation = _response(
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Calculate this worker's overtime pay.",
        SourceScopes=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE.value],
        CandidateEvidence=[],
        DomainTags=["overtime"],
    )
    write = _response(
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Please approve and process this payrun now.",
    )

    assert calculation["OrchestratorEnvelope"]["Status"] == "PROHIBITED_CLAIM_BLOCKED"
    assert "payroll calculation request blocked" in calculation["BlockedClaims"]
    assert write["OrchestratorEnvelope"]["Status"] == "PROHIBITED_CLAIM_BLOCKED"
    assert "write action request blocked" in write["BlockedClaims"]


def test_response_includes_no_action_attestation():
    response = _response()

    assert response["NoActionAttestation"] == NO_ACTION_ATTESTATION
    for phrase in [
        "No live LLM called",
        "no DB accessed",
        "no external API called",
        "no code executed",
        "no write action performed",
        "no runtime object evidence fetched",
        "no final answer generated",
    ]:
        assert phrase in response["NoActionAttestationText"]


def test_response_includes_support_packet_and_deterministic_draft():
    response = _response()

    assert response["EvidenceSupportPacket"]["support_status"] == "SUPPORTED"
    assert response["DeterministicDraft"]["DeterministicDraftAvailable"] is True


def test_raw_code_snippets_are_absent():
    response = _response(CandidateEvidence={**_sample_evidence()[2], "raw_code_snippet": "def unsafe(): pass"})
    dumped = str(response)

    assert "raw_code_snippet" not in dumped
    assert "def unsafe" not in dumped
    assert "return {" not in dumped


def test_response_is_deterministic_for_same_input():
    request = _request(InternalChatRole.PAYROLL_ADMINISTRATOR)

    assert _service().build_response(request).model_dump() == _service().build_response(request).model_dump()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_internal_chat_api_stub_docs_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()
    assert SAMPLE_RESPONSE.exists()


def test_internal_chat_api_stub_docs_include_samples_and_guardrails():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for sample_question in [
        "Where is the manual admitted draft processing endpoint implemented?",
        "Can the platform manually process an admitted draft action?",
        "What should I do with this post-finalisation ObjectTime action?",
        "Is this feature enabled for my tenant?",
        "Can I see the code behind my payslip?",
        "Why did this worker get overtime?",
        "Explain this payroll trend chart.",
        "Calculate this worker's overtime pay.",
        "Please approve and process this payrun now.",
    ]:
        assert sample_question in combined

    for phrase in [
        "No live LLM called",
        "No DB accessed",
        "No external API called",
        "No code executed",
        "No write action performed",
        "No runtime object evidence fetched",
        "Final answer generation remains disabled",
        "DeterministicDraft",
        "NoActionAttestation",
    ]:
        assert phrase in combined


def test_internal_chat_api_stub_docs_have_no_mojibake_markers():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in combined

from pathlib import Path

from app.services.code_evidence_answer_policy_service import CodeEvidenceDisclosureMode
from app.services.internal_chat_orchestrator_service import (
    InternalChatOrchestratorService,
    InternalChatRequest,
    InternalChatRole,
    InternalChatSourceScope,
    InternalChatStatus,
)


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_orchestrator_envelope_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_orchestrator_envelope_v0_1"
    / "CHAT_ORCHESTRATOR_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT / "docs" / "codex_prompts" / "2026-05-21_minerva_internal_chat_orchestrator_envelope_v01.md"
)
SAMPLE_PACKET = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_orchestrator_envelope_v0_1"
    / "CHAT_ORCHESTRATOR_SAMPLE_PACKET.json"
)


def _service() -> InternalChatOrchestratorService:
    return InternalChatOrchestratorService()


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


def _request(role=InternalChatRole.DEVELOPER, question=None, **overrides) -> InternalChatRequest:
    payload = {
        "question_text": question or "Where is the manual admitted draft processing endpoint implemented?",
        "user_role": role,
        "source_scopes_requested": [
            InternalChatSourceScope.PLATFORM_KNOWLEDGE,
            InternalChatSourceScope.IMPLEMENTATION_STATE,
            InternalChatSourceScope.CODE_EVIDENCE,
            InternalChatSourceScope.TEST_EVIDENCE,
            InternalChatSourceScope.PROMPT_ARTEFACTS,
            InternalChatSourceScope.EVALUATION_BASELINES,
        ],
        "domain_topic_tags": ["manual", "admitted", "draft", "processing"],
        "candidate_evidence_metadata": _sample_evidence(),
    }
    payload.update(overrides)
    return InternalChatRequest(
        **payload,
    )


def test_developer_request_with_code_evidence_builds_technical_envelope():
    envelope = _service().orchestrate(_request(InternalChatRole.DEVELOPER))

    assert envelope.status == InternalChatStatus.ANSWER_SUPPORT_BUILT
    assert envelope.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE
    assert "app/routes/payroll/admitted_draft_actions.py" in envelope.evidence_summary
    assert "raw_code_snippet" not in str(envelope.model_dump())


def test_payroll_administrator_receives_implementation_confirmation_without_raw_code():
    envelope = _service().orchestrate(
        _request(
            InternalChatRole.PAYROLL_ADMINISTRATOR,
            question="Can the platform manually process an admitted draft action?",
        )
    )

    assert envelope.status == InternalChatStatus.ANSWER_SUPPORT_BUILT
    assert envelope.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    assert "Implementation confirmation summary" in envelope.role_safe_evidence_summary
    assert "def " not in str(envelope.model_dump())


def test_payroll_user_gets_background_confidence_without_internal_names():
    envelope = _service().orchestrate(
        _request(
            InternalChatRole.PAYROLL_USER,
            question="What should I do with this post-finalisation ObjectTime action?",
        )
    )
    dumped = str(envelope.model_dump())

    assert envelope.disclosure_mode == CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY
    assert "Operational confidence summary" in envelope.role_safe_evidence_summary
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" not in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" not in dumped


def test_customer_administrator_request_includes_customer_availability_runtime_caveat():
    envelope = _service().orchestrate(
        _request(
            InternalChatRole.CUSTOMER_ADMINISTRATOR,
            question="Is this feature enabled for my tenant?",
        )
    )

    assert envelope.status == InternalChatStatus.NEEDS_MORE_EVIDENCE
    assert envelope.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    assert any("Runtime, production, tenant, or customer availability" in caveat for caveat in envelope.required_caveats)
    assert "Customer-safe implementation summary" in envelope.role_safe_evidence_summary


def test_worker_request_excludes_code_evidence_and_is_role_restricted():
    envelope = _service().orchestrate(
        _request(InternalChatRole.WORKER, question="Can I see the code behind my payslip?")
    )
    dumped = str(envelope.model_dump())

    assert envelope.status == InternalChatStatus.PROHIBITED_CLAIM_BLOCKED
    assert envelope.disclosure_mode == CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE
    assert envelope.evidence_support_packet.code_evidence == []
    assert envelope.evidence_support_packet.test_evidence == []
    assert "raw code disclosure request blocked" in envelope.blocked_claims
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped


def test_runtime_scope_without_supplied_runtime_metadata_needs_more_evidence():
    request = _request(
        InternalChatRole.PAYROLL_MANAGER,
        question="Why did this worker get overtime?",
        source_scopes_requested=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE],
        candidate_evidence_metadata=[],
        domain_topic_tags=["overtime"],
    )

    envelope = _service().orchestrate(request)

    assert envelope.status in {InternalChatStatus.NEEDS_MORE_EVIDENCE, InternalChatStatus.UNSUPPORTED_SCOPE}
    assert InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE in envelope.unsupported_scopes


def test_analytics_scope_is_recognised_but_deferred_by_default():
    request = _request(
        InternalChatRole.ANALYTICS_USER,
        question="Explain this payroll trend chart.",
        source_scopes_requested=[InternalChatSourceScope.ANALYTICS_EVIDENCE],
        candidate_evidence_metadata=[],
        domain_topic_tags=["analytics", "trend"],
    )

    envelope = _service().orchestrate(request)

    assert envelope.status == InternalChatStatus.UNSUPPORTED_SCOPE
    assert InternalChatSourceScope.ANALYTICS_EVIDENCE in envelope.unsupported_scopes
    assert any("inactive by default" in caveat for caveat in envelope.required_caveats)


def test_production_availability_claim_with_only_code_evidence_requires_runtime_evidence():
    request = _request(
        InternalChatRole.DEVELOPER,
        question="Is the manual admitted draft processing endpoint live in production?",
        candidate_evidence_metadata=[
            item for item in _sample_evidence() if item["evidence_category"] in {"CODE", "TEST"}
        ],
    )

    envelope = _service().orchestrate(request)

    assert envelope.status == InternalChatStatus.NEEDS_MORE_EVIDENCE
    assert envelope.evidence_support_packet.support_status.value == "NEEDS_RUNTIME_EVIDENCE"


def test_payroll_calculation_request_is_blocked():
    envelope = _service().orchestrate(
        _request(
            InternalChatRole.PAYROLL_MANAGER,
            question="Calculate this worker's overtime pay.",
            source_scopes_requested=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE],
            candidate_evidence_metadata=[],
            domain_topic_tags=["overtime"],
        )
    )

    assert envelope.status == InternalChatStatus.PROHIBITED_CLAIM_BLOCKED
    assert "payroll calculation request blocked" in envelope.blocked_claims
    assert envelope.no_action_attestation["PayrollCalculationPerformed"] is False


def test_write_action_request_is_blocked():
    envelope = _service().orchestrate(
        _request(InternalChatRole.PAYROLL_ADMINISTRATOR, question="Please approve and process this payrun now.")
    )

    assert envelope.status == InternalChatStatus.PROHIBITED_CLAIM_BLOCKED
    assert "write action request blocked" in envelope.blocked_claims
    assert envelope.no_action_attestation["WriteActionPerformed"] is False


def test_allow_live_llm_true_still_disables_live_llm():
    envelope = _service().orchestrate(_request(allow_live_llm=True))

    assert envelope.status == InternalChatStatus.LIVE_LLM_DISABLED
    assert envelope.live_llm_used is False
    assert envelope.final_answer_generation_permitted is False


def test_allow_final_answer_generation_true_still_disables_final_answer_generation():
    envelope = _service().orchestrate(_request(allow_final_answer_generation=True))

    assert envelope.status == InternalChatStatus.FINAL_ANSWER_GENERATION_DISABLED
    assert envelope.final_answer_generation_permitted is False
    assert envelope.final_answer_text is None


def test_every_envelope_includes_no_action_attestation():
    envelope = _service().orchestrate(_request())

    assert set(envelope.no_action_attestation) >= {
        "LiveLlmCalled",
        "DatabaseAccessed",
        "ExternalRepoMutated",
        "PayrollCalculationPerformed",
        "WriteActionPerformed",
        "RuntimeObjectEvidenceFetched",
        "FinalAnswerGenerationPerformed",
    }
    assert all(value is False for value in envelope.no_action_attestation.values())


def test_every_envelope_includes_answer_support_required_caveats():
    envelope = _service().orchestrate(_request())

    assert any("cannot prove production availability" in caveat for caveat in envelope.required_caveats)
    assert any("Final natural-language answer generation remains disabled" in caveat for caveat in envelope.required_caveats)


def test_suggested_deterministic_summary_is_not_final_answer_text():
    envelope = _service().orchestrate(_request())

    assert envelope.suggested_deterministic_summary
    assert "Deterministic envelope status" in envelope.suggested_deterministic_summary
    assert envelope.final_answer_text is None


def test_role_safe_evidence_summary_differs_between_developer_and_payroll_user():
    developer = _service().orchestrate(_request(InternalChatRole.DEVELOPER))
    payroll_user = _service().orchestrate(_request(InternalChatRole.PAYROLL_USER))

    assert developer.role_safe_evidence_summary != payroll_user.role_safe_evidence_summary
    assert "Technical evidence summary" in developer.role_safe_evidence_summary
    assert "Operational confidence summary" in payroll_user.role_safe_evidence_summary


def test_raw_code_snippets_never_appear():
    for role in InternalChatRole:
        envelope = _service().orchestrate(_request(role))
        dumped = str(envelope.model_dump())

        assert "raw_code_snippet" not in dumped
        assert "return {" not in dumped
        assert "class " not in dumped


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_internal_chat_orchestrator_docs_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()
    assert SAMPLE_PACKET.exists()


def test_internal_chat_orchestrator_docs_include_samples_statuses_and_guardrails():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for status in [
        "READY_FOR_ANSWER_SUPPORT",
        "ANSWER_SUPPORT_BUILT",
        "ANSWER_NOT_PERMITTED",
        "ROLE_RESTRICTED",
        "NEEDS_MORE_EVIDENCE",
        "PROHIBITED_CLAIM_BLOCKED",
        "LIVE_LLM_DISABLED",
        "FINAL_ANSWER_GENERATION_DISABLED",
        "UNSUPPORTED_SCOPE",
    ]:
        assert status in combined

    for sample_question in [
        "Where is the manual admitted draft processing endpoint implemented?",
        "Can the platform manually process an admitted draft action?",
        "What should I do with this post-finalisation ObjectTime action?",
        "Is this feature enabled for my tenant?",
        "Can I see the code behind my payslip?",
        "Why did this worker get overtime?",
        "Explain this payroll trend chart.",
    ]:
        assert sample_question in combined

    for phrase in [
        "No live LLM called",
        "No DB accessed",
        "No runtime object evidence fetched",
        "No write action performed",
        "No final answer generation performed",
        "runtime object evidence is recognised but not fetched",
        "analytics evidence is recognised as future and inactive by default",
    ]:
        assert phrase in combined


def test_internal_chat_orchestrator_docs_have_no_mojibake_markers():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in combined

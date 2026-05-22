from pathlib import Path

from app.services.internal_chat_deterministic_answer_draft_service import (
    DeterministicAnswerDraftFormattingMode,
    DeterministicAnswerDraftRequest,
    DeterministicAnswerDraftStatus,
    InternalChatDeterministicAnswerDraftService,
)
from app.services.internal_chat_orchestrator_service import (
    InternalChatOrchestratorService,
    InternalChatRequest,
    InternalChatRole,
    InternalChatSourceScope,
)


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_deterministic_answer_draft_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_deterministic_answer_draft_v0_1"
    / "DETERMINISTIC_ANSWER_DRAFT_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_internal_chat_deterministic_answer_draft_v01.md"
)
SAMPLE_FIXTURE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_internal_chat_deterministic_answer_draft_v0_1"
    / "DETERMINISTIC_ANSWER_DRAFT_SAMPLE.json"
)


def _orchestrator() -> InternalChatOrchestratorService:
    return InternalChatOrchestratorService()


def _draft_service() -> InternalChatDeterministicAnswerDraftService:
    return InternalChatDeterministicAnswerDraftService()


def _sample_evidence(include_implementation_state: bool = True) -> list[dict]:
    evidence = [
        {
            "source_type": "DOCTRINE",
            "evidence_category": "DOCTRINE",
            "title": "Manual admitted draft processing doctrine",
            "summary": "Admitted draft actions require governed manual processing support.",
            "tags": ["manual", "admitted", "draft", "processing", "payrun"],
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
    if include_implementation_state:
        evidence.append(
            {
                "source_type": "IMPLEMENTATION_STATE_DOC",
                "evidence_category": "IMPLEMENTATION_STATE",
                "title": "manual admitted draft processing implementation state",
                "file_path": "docs/evaluation/admitted_draft/IMPLEMENTATION_STATE_BASELINE.md",
                "tags": ["manual", "admitted", "draft", "processing", "implementation_state"],
            }
        )
    return evidence


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
    return InternalChatRequest(**payload)


def _draft(role=InternalChatRole.DEVELOPER, question=None, **overrides):
    envelope = _orchestrator().orchestrate(_request(role=role, question=question, **overrides))
    return _draft_service().build_draft(envelope)


def test_supported_developer_envelope_produces_ready_draft_with_technical_references():
    draft = _draft(InternalChatRole.DEVELOPER)
    dumped = str(draft.model_dump())

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_READY
    assert draft.deterministic_draft_available is True
    assert "app/routes/payroll/admitted_draft_actions.py" in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" in dumped
    assert "raw_code_snippet" not in dumped
    assert "def " not in dumped
    assert "return {" not in dumped


def test_payroll_administrator_draft_uses_implementation_confirmation_and_runtime_caveat():
    draft = _draft(
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Can the platform manually process an admitted draft action?",
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_READY
    assert "Current implementation evidence supports this capability" in draft.draft_text
    assert "cannot prove production availability" in draft.caveats_text
    assert "raw_code_snippet" not in str(draft.model_dump())


def test_payroll_user_draft_hides_internal_identifiers_and_uses_operational_wording():
    draft = _draft(
        InternalChatRole.PAYROLL_USER,
        question="What should I do with this post-finalisation ObjectTime action?",
    )
    dumped = str(draft.model_dump())

    assert "The platform can support this workflow" in draft.draft_text
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" not in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" not in dumped


def test_customer_administrator_draft_includes_tenant_availability_caveat():
    draft = _draft(
        InternalChatRole.CUSTOMER_ADMINISTRATOR,
        question="Is this enabled for my tenant?",
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED
    assert "customer-safe implementation confirmation" in draft.draft_text
    assert "tenant" in draft.caveats_text.lower()
    assert "runtime" in draft.suggested_next_step.lower()


def test_worker_draft_excludes_code_evidence_and_is_role_restricted():
    draft = _draft(InternalChatRole.WORKER, question="Can I see the code behind my payslip?")
    dumped = str(draft.model_dump())

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED
    assert "not available in the current role-safe mode" in draft.draft_text
    assert "worker-facing mode" in draft.withheld_evidence_notice
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" not in dumped


def test_needs_implementation_state_review_says_code_exists_but_curated_state_is_missing():
    draft = _draft(
        InternalChatRole.DEVELOPER,
        candidate_evidence_metadata=_sample_evidence(include_implementation_state=False),
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_NEEDS_MORE_EVIDENCE
    assert "Code evidence exists" in draft.draft_text
    assert "implementation-state evidence is missing" in draft.draft_text


def test_needs_runtime_evidence_produces_runtime_required_wording():
    draft = _draft(
        InternalChatRole.DEVELOPER,
        question="Is the manual admitted draft processing endpoint live in production?",
        candidate_evidence_metadata=[
            item for item in _sample_evidence(False) if item["evidence_category"] in {"CODE", "TEST"}
        ],
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED
    assert "cannot be confirmed" in draft.draft_text
    assert "runtime" in draft.suggested_next_step.lower()


def test_prohibited_claim_blocked_draft_does_not_affirm_claim():
    draft = _draft(
        InternalChatRole.DEVELOPER,
        claimed_answer_to_validate="Code evidence proves production availability for this feature.",
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_PROHIBITED_CLAIM_BLOCKED
    assert "does not affirm" in draft.draft_text
    assert "supports production availability" not in draft.draft_text.lower()


def test_runtime_object_scope_without_evidence_requires_more_runtime_evidence():
    draft = _draft(
        InternalChatRole.PAYROLL_MANAGER,
        question="Why did this worker get overtime?",
        source_scopes_requested=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE],
        candidate_evidence_metadata=[],
        domain_topic_tags=["overtime"],
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED
    assert "object-specific availability cannot be confirmed" in draft.draft_text


def test_analytics_deferred_scope_produces_analytics_deferred_wording():
    draft = _draft(
        InternalChatRole.ANALYTICS_USER,
        question="Explain this payroll trend chart.",
        source_scopes_requested=[InternalChatSourceScope.ANALYTICS_EVIDENCE],
        candidate_evidence_metadata=[],
        domain_topic_tags=["analytics", "trend"],
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_UNSUPPORTED_SCOPE
    assert "analytics interpretation is not active by default" in draft.draft_text


def test_payroll_calculation_request_is_blocked():
    draft = _draft(
        InternalChatRole.PAYROLL_MANAGER,
        question="Calculate this worker's overtime pay.",
        source_scopes_requested=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE],
        candidate_evidence_metadata=[],
        domain_topic_tags=["overtime"],
    )

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_BLOCKED
    assert "must not calculate payroll" in draft.draft_text
    assert "payroll calculation request blocked" in draft.blocked_claims_text


def test_allow_final_answer_generation_does_not_make_draft_final():
    envelope = _orchestrator().orchestrate(_request(allow_final_answer_generation=True))
    draft = _draft_service().build_draft(
        DeterministicAnswerDraftRequest(envelope=envelope, allow_final_answer_generation=True)
    )

    assert draft.is_final_answer is False
    assert draft.final_answer_generation_permitted is False
    assert "FINAL_ANSWER_GENERATION_PERMITTED_FALSE" in draft.safety_flags


def test_live_llm_used_remains_false():
    draft = _draft(allow_live_llm=True)

    assert draft.draft_status == DeterministicAnswerDraftStatus.DRAFT_LIVE_LLM_DISABLED
    assert draft.live_llm_used is False
    assert "LIVE_LLM_USED_FALSE" in draft.safety_flags


def test_final_answer_generation_permitted_remains_false():
    draft = _draft()

    assert draft.final_answer_generation_permitted is False
    assert draft.model_dump()["FinalAnswerGenerationPermitted"] is False


def test_every_draft_includes_no_action_attestation():
    draft = _draft()

    for phrase in [
        "No live LLM called",
        "no DB accessed",
        "no payroll calculation performed",
        "no write action performed",
        "no runtime object evidence fetched",
        "no final answer generation performed",
    ]:
        assert phrase in draft.no_action_attestation_text


def test_raw_code_snippets_are_absent_in_all_role_drafts():
    for role in InternalChatRole:
        draft = _draft(role)
        dumped = str(draft.model_dump())

        assert "raw_code_snippet" not in dumped
        assert "return {" not in dumped
        assert "def " not in dumped
        assert "class " not in dumped


def test_draft_text_includes_caveats_when_required():
    draft = _draft()

    assert "Caveats:" in draft.draft_text
    assert "cannot prove production availability" in draft.caveats_text


def test_formatting_modes_are_deterministic_and_distinct():
    envelope = _orchestrator().orchestrate(_request())
    service = _draft_service()

    concise_a = service.build_draft(envelope, formatting_mode=DeterministicAnswerDraftFormattingMode.CONCISE)
    concise_b = service.build_draft(envelope, formatting_mode="CONCISE")
    standard = service.build_draft(envelope, formatting_mode=DeterministicAnswerDraftFormattingMode.STANDARD)
    technical = service.build_draft(envelope, formatting_mode=DeterministicAnswerDraftFormattingMode.TECHNICAL)

    assert concise_a.draft_text == concise_b.draft_text
    assert concise_a.draft_text != standard.draft_text
    assert technical.draft_text != standard.draft_text
    assert "Draft status:" in technical.draft_text


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_deterministic_answer_draft_docs_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()
    assert SAMPLE_FIXTURE.exists()


def test_deterministic_answer_draft_docs_include_required_statuses_samples_and_guardrails():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for status in [
        "DRAFT_READY",
        "DRAFT_BLOCKED",
        "DRAFT_NEEDS_MORE_EVIDENCE",
        "DRAFT_ROLE_RESTRICTED",
        "DRAFT_PROHIBITED_CLAIM_BLOCKED",
        "DRAFT_RUNTIME_EVIDENCE_REQUIRED",
        "DRAFT_UNSUPPORTED_SCOPE",
        "DRAFT_LIVE_LLM_DISABLED",
    ]:
        assert status in combined

    for sample_question in [
        "Where is the manual admitted draft processing endpoint implemented?",
        "Can the platform manually process an admitted draft action?",
        "What should I do with this post-finalisation ObjectTime action?",
        "Is this enabled for my tenant?",
        "Can I see the code behind my payslip?",
        "Why did this worker get overtime?",
        "Explain this payroll trend chart.",
        "calculate payroll",
        "tests prove production availability",
    ]:
        assert sample_question in combined

    for phrase in [
        "No live LLM called",
        "No DB accessed",
        "No runtime object evidence fetched",
        "No write action performed",
        "No final answer generation performed",
        "DeterministicDraftAvailable",
        "IsFinalAnswer",
        "FinalAnswerGenerationPermitted",
        "LiveLlmUsed",
    ]:
        assert phrase in combined


def test_deterministic_answer_draft_docs_have_no_mojibake_markers():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in combined

from pathlib import Path

from app.services.code_evidence_answer_policy_service import (
    CodeEvidenceDisclosureMode,
    CodeEvidenceRole,
)
from app.services.code_evidence_answer_support_service import (
    CODE_CANNOT_PROVE_RUNTIME_CAVEAT,
    NO_ACTION_ATTESTATION,
    CodeEvidenceAnswerSupportService,
    CodeEvidenceSupportStatus,
)


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_code_evidence_answer_support_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_code_evidence_answer_support_v0_1"
    / "ANSWER_SUPPORT_BASELINE.md"
)
PROMPT_ARTEFACT = ROOT / "docs" / "codex_prompts" / "2026-05-21_minerva_code_evidence_answer_support_v01.md"
SAMPLE_FIXTURE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_code_evidence_answer_support_v0_1"
    / "CODE_EVIDENCE_ANSWER_SUPPORT_SAMPLE.json"
)


def _service() -> CodeEvidenceAnswerSupportService:
    return CodeEvidenceAnswerSupportService()


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
            "source_type": "KNOWLEDGE_DOC",
            "evidence_category": "KNOWLEDGE",
            "title": "manual admitted draft processing knowledge",
            "file_path": "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md",
            "tags": ["manual", "admitted", "draft", "processing", "knowledge"],
        },
    ]
    if include_implementation_state:
        evidence.append(
            {
                "source_type": "IMPLEMENTATION_STATE_DOC",
                "evidence_category": "IMPLEMENTATION_STATE",
                "title": "manual admitted draft processing implementation state",
                "file_path": "docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/IMPLEMENTATION_STATE_BASELINE.md",
                "tags": ["manual", "admitted", "draft", "processing", "implementation_state"],
            }
        )
    return evidence


def _packet(role=CodeEvidenceRole.DEVELOPER, include_implementation_state=True, answer_claim=None):
    return _service().build_support_packet(
        question_text="Where is the manual admitted draft processing endpoint implemented?",
        user_role=role,
        domain_key="admitted_draft_payrun_processing",
        topic_tags=["manual", "admitted", "draft", "processing"],
        expected_doctrine_terms=["admitted draft"],
        implementation_state_terms=["implementation state"],
        candidate_evidence_items=_sample_evidence(include_implementation_state),
        answer_claim=answer_claim,
    )


def test_developer_with_code_service_test_evidence_receives_technical_references():
    packet = _packet(CodeEvidenceRole.DEVELOPER)

    assert packet.support_status == CodeEvidenceSupportStatus.SUPPORTED
    assert packet.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE
    assert any(source.file_path == "app/routes/payroll/admitted_draft_actions.py" for source in packet.code_evidence)
    assert any(source.symbol_name == "AdmittedDraftPayRunProcessingBridgeService" for source in packet.code_evidence)
    assert any(
        source.test_name == "test_manual_admitted_draft_processing_bridge_evidence"
        for source in packet.test_evidence
    )


def test_payroll_administrator_receives_implementation_confirmation_without_raw_code_snippets():
    packet = _packet(CodeEvidenceRole.PAYROLL_ADMINISTRATOR)
    dumped = str(packet.model_dump())

    assert packet.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    assert "app/routes/payroll/admitted_draft_actions.py" in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" in dumped
    assert "raw_code_snippet" not in dumped
    assert "def " not in dumped


def test_payroll_user_receives_background_confidence_only_without_internal_names():
    packet = _packet(CodeEvidenceRole.PAYROLL_USER)
    dumped = str(packet.model_dump())

    assert packet.disclosure_mode == CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY
    assert packet.code_evidence
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" not in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" not in dumped
    assert "Operational confidence summary" in packet.role_safe_evidence_summary


def test_customer_administrator_receives_customer_safe_confirmation_and_production_caveat():
    packet = _service().build_support_packet(
        question_text="Is this feature available for my tenant?",
        user_role=CodeEvidenceRole.CUSTOMER_ADMINISTRATOR,
        topic_tags=["manual", "admitted", "draft", "processing"],
        candidate_evidence_items=_sample_evidence(include_implementation_state=True),
    )
    dumped = str(packet.model_dump())

    assert packet.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    assert packet.support_status == CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE
    assert "Customer-safe implementation summary" in packet.role_safe_evidence_summary
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped
    assert any("Runtime, production, tenant, or customer availability" in caveat for caveat in packet.required_caveats)


def test_worker_receives_no_code_evidence_and_role_restricted_packet():
    packet = _packet(CodeEvidenceRole.WORKER)
    dumped = str(packet.model_dump())

    assert packet.support_status == CodeEvidenceSupportStatus.ROLE_RESTRICTED
    assert packet.disclosure_mode == CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE
    assert packet.code_evidence == []
    assert packet.test_evidence == []
    assert "NO_CODE_EVIDENCE" in " ".join(packet.withheld_evidence)
    assert "app/routes/payroll/admitted_draft_actions.py" not in dumped


def test_code_implementation_state_and_tests_return_supported():
    packet = _packet(CodeEvidenceRole.DEVELOPER, include_implementation_state=True)

    assert packet.support_status == CodeEvidenceSupportStatus.SUPPORTED


def test_code_without_implementation_state_returns_review_status():
    packet = _packet(CodeEvidenceRole.DEVELOPER, include_implementation_state=False)

    assert packet.support_status == CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW
    assert any("Implementation-state documentation is missing" in caveat for caveat in packet.required_caveats)


def test_production_or_customer_availability_claim_with_only_code_needs_runtime_evidence():
    packet = _service().build_support_packet(
        question_text="Is the manual admitted draft processing endpoint live for customers?",
        user_role=CodeEvidenceRole.DEVELOPER,
        topic_tags=["manual", "admitted", "draft", "processing"],
        candidate_evidence_items=[
            item
            for item in _sample_evidence(include_implementation_state=False)
            if item["evidence_category"] in {"CODE", "TEST"}
        ],
    )

    assert packet.support_status == CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE
    assert packet.runtime_availability_caveat_required is True


def test_prohibited_claim_is_blocked():
    packet = _packet(
        CodeEvidenceRole.DEVELOPER,
        answer_claim="Code evidence proves production availability for the manual admitted draft processing feature.",
    )

    assert packet.support_status == CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED
    assert packet.answer_permitted is False
    assert "code proves production availability" in packet.blocked_claims


def test_every_code_packet_includes_code_cannot_prove_runtime_caveat():
    packet = _packet(CodeEvidenceRole.PAYROLL_ADMINISTRATOR)

    assert packet.runtime_availability_caveat_required is True
    assert packet.code_cannot_prove_runtime_caveat == CODE_CANNOT_PROVE_RUNTIME_CAVEAT
    assert any("cannot prove production availability" in caveat for caveat in packet.required_caveats)


def test_every_packet_includes_no_action_attestation():
    packet = _packet(CodeEvidenceRole.DEVELOPER)

    assert packet.no_action_attestation == NO_ACTION_ATTESTATION
    for phrase in [
        "No code executed",
        "no DB accessed",
        "no external repo mutated",
        "no live LLM called",
        "no final user-facing answer generated",
        "no payroll calculation performed",
    ]:
        assert phrase in packet.no_action_attestation


def test_final_answer_generation_is_never_permitted_in_v0_1():
    packet = _packet(CodeEvidenceRole.DEVELOPER)

    assert packet.final_answer_generation_permitted is False


def test_no_raw_code_snippets_appear_in_any_role_packet():
    for role in CodeEvidenceRole:
        packet = _packet(role)
        dumped = str(packet.model_dump())

        assert "raw_code_snippet" not in dumped
        assert "return {" not in dumped
        assert "class " not in dumped


def test_test_evidence_is_distinguished_from_code_existence():
    packet = _packet(CodeEvidenceRole.DEVELOPER)

    assert packet.code_evidence
    assert packet.test_evidence
    assert all(source.evidence_category == "CODE" for source in packet.code_evidence)
    assert all(source.evidence_category == "TEST" for source in packet.test_evidence)


def test_role_safe_evidence_summary_differs_from_full_evidence_summary():
    packet = _packet(CodeEvidenceRole.PAYROLL_USER)

    assert packet.evidence_summary != packet.role_safe_evidence_summary
    assert "Matched evidence counts" in packet.evidence_summary
    assert "Operational confidence summary" in packet.role_safe_evidence_summary


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_answer_support_docs_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()
    assert SAMPLE_FIXTURE.exists()


def test_answer_support_docs_include_required_statuses_samples_and_guardrails():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for status in [
        "SUPPORTED",
        "PARTIALLY_SUPPORTED",
        "UNSUPPORTED",
        "NEEDS_IMPLEMENTATION_STATE_REVIEW",
        "NEEDS_RUNTIME_EVIDENCE",
        "ROLE_RESTRICTED",
        "PROHIBITED_CLAIM_BLOCKED",
    ]:
        assert status in combined

    for sample_question in [
        "Where is the manual admitted draft processing endpoint implemented?",
        "Can the platform manually process an admitted draft action?",
        "What should I do with this action?",
        "Is this feature available for my tenant?",
        "Can I see the code for my payslip?",
    ]:
        assert sample_question in combined

    for phrase in [
        "code evidence proves production readiness",
        "code evidence proves customer availability",
        "code evidence proves migration applied",
        "code evidence proves payroll result correctness",
        "tests passing means production enabled",
        "route file means route is deployed",
    ]:
        assert phrase in combined

    for phrase in [
        "No code executed",
        "No DB accessed",
        "No external repo mutated",
        "No live LLM called",
        "No final user-facing answer generated",
        "No payroll calculation performed",
    ]:
        assert phrase in combined


def test_answer_support_docs_have_no_mojibake_markers():
    combined = "\n".join(_read(path) for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT])

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in combined

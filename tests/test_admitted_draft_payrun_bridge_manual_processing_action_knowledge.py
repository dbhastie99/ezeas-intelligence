from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md"
)
STRUCTURED_KNOWLEDGE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_bridge_manual_processing_action_v0_1.md"
)
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "admitted_draft_payrun_bridge_manual_processing_action_v0_1"
    / "ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_admitted_draft_payrun_bridge_manual_processing_action_knowledge_v01.md"
)

GOLDEN_QUESTIONS = [
    "1. What is the Admitted Draft PayRun Bridge Manual Processing Action?",
    "2. Why did we choose manual action instead of a separate visible preview workflow?",
    "3. What role does preview/preflight still play?",
    "4. What is the manual processing workflow?",
    "5. What backend authority is required before processing?",
    "6. What PayRun guardrails must pass before processing?",
    "7. Why must the PayRunContact already exist?",
    "8. Why is this manual action not automation?",
    "9. What may the planned Workforce slice implement?",
    "10. What must the planned Workforce slice not implement?",
    "11. What should the endpoint response include?",
    "12. What should the UI do and not do?",
    "13. How does this preserve deterministic payroll authority?",
    "14. What runtime-overstatement risks should Minerva avoid?",
    "15. How does this relate to the earlier operator preview surface knowledge?",
    "16. What remains for a later slice after manual processing action?",
]

PRIOR_LINKS = [
    "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md",
    "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md",
    "docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md",
    "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md",
    "docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md",
    "docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md",
    "docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _all_docs() -> str:
    return "\n".join(
        [
            _read(SOURCE_RESPONSE),
            _read(STRUCTURED_KNOWLEDGE),
            _read(EVALUATION_BASELINE),
            _read(PROMPT_ARTEFACT),
        ]
    )


def test_required_files_exist():
    assert SOURCE_RESPONSE.exists()
    assert STRUCTURED_KNOWLEDGE.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_source_response_contains_title_and_sections_1_through_19():
    content = _read(SOURCE_RESPONSE)

    assert (
        "# Minerva Knowledge Capture — Admitted Draft PayRun Bridge Manual Processing Action"
        in content
    )
    assert "## Purpose of this knowledge capture" in content

    for section_number in range(1, 20):
        assert f"## {section_number}." in content


def test_all_sixteen_golden_questions_are_present_in_core_documents():
    source = _read(SOURCE_RESPONSE)
    structured = _read(STRUCTURED_KNOWLEDGE)
    baseline = _read(EVALUATION_BASELINE)

    for question in GOLDEN_QUESTIONS:
        assert question in source
        assert question in structured
        assert question in baseline


def test_answer_guidance_exists_for_all_sixteen_questions():
    source = _read(SOURCE_RESPONSE)
    structured = _read(STRUCTURED_KNOWLEDGE)

    assert source.count("Answer guidance:") == 16
    assert structured.count("Answer guidance:") == 16


def test_manual_action_and_preflight_doctrine_are_present():
    content = _all_docs()

    required = [
        "Manual action is not automation",
        "manual action is not automation",
        "Preview/preflight is internal safety logic",
        "preview/preflight is internal safety logic",
        "not a separate visible workflow",
        "not a separate visible user journey",
    ]

    for phrase in required:
        assert phrase in content


def test_backend_authority_and_ui_boundaries_are_present():
    content = _all_docs()

    required = [
        "backend is the source of eligibility truth",
        "Backend is source of eligibility truth",
        "UI must not infer eligibility independently",
        "active PayRunActionDecision",
        "Active PayRunActionDecision",
        "authorised admission evidence",
        "Authorised admission evidence",
        "existing PayRunContact",
        "Existing PayRunContact required",
        "ProcessPeriod.LifecycleStatusCode",
    ]

    for phrase in required:
        assert phrase in content


def test_no_creation_finalisation_payment_or_bank_file_boundary_is_present():
    content = _all_docs()

    required = [
        "no PayRun creation",
        "no PayRunContact creation",
        "no PayRun/PayRunContact creation",
        "must not create PayRuns or PayRunContacts",
        "no finalisation",
        "no payment",
        "no bank file",
        "No finalisation/payment/bank file",
        "payment batches or bank files",
    ]

    for phrase in required:
        assert phrase in content


def test_prohibited_claims_are_captured():
    content = _all_docs()

    prohibited_claims = [
        "the separate visible preview workflow is still the preferred operator path",
        "preview itself executes processing",
        "manual action is automation",
        "the action processes all admitted actions",
        "the action creates PayRuns",
        "the action creates PayRunContacts",
        "the action finalises PayRuns",
        "the action pays workers",
        "the action creates payment batches or bank files",
        "the action mutates finalised/frozen/paid PayRuns",
        "Minerva calculates or authorises payroll",
        "UI determines eligibility without backend authority",
    ]

    for claim in prohibited_claims:
        assert claim in content


def test_no_action_no_runtime_attestation_is_present():
    content = _all_docs()

    attestations = [
        "No runtime changes",
        "No live LLM calls",
        "No DB access, reads, writes, migrations, or validation",
        "No workforce-platform changes",
        "No retrieval-plan/runtime behaviour changes",
        "No chat exposure",
        "No operational corpus/runtime state mutation",
        "This Minerva slice is knowledge only",
    ]

    for attestation in attestations:
        assert attestation in content


def test_prior_bridge_and_operator_preview_links_are_present():
    content = _all_docs()

    for link in PRIOR_LINKS:
        assert link in content


def test_response_packet_expectations_are_present():
    content = _all_docs()

    response_fields = [
        "Status",
        "Processed / AlreadyProcessed / Blocked flags",
        "ActionIdentity",
        "DecisionAuthority",
        "AdmissionAuthority",
        "TargetPayRun",
        "TargetPayRunContact",
        "Guardrails",
        "ProcessingEntrypoint",
        "ProcessingOutcome",
        "Readiness",
        "Evidence",
        "OperatorNextActions",
        "NonGoals",
        "ActionsTaken",
        "ActionsNotTaken",
        "Idempotency",
    ]

    for field in response_fields:
        assert field in content


def test_structured_retrieval_keywords_and_aliases_are_present():
    content = _read(STRUCTURED_KNOWLEDGE)

    keywords = [
        "manual admitted draft processing action",
        "process admitted action",
        "backend preflight",
        "bridge manual processing",
        "PayRunActionDecision authority",
        "admission evidence",
        "existing PayRunContact required",
        "not automation",
        "not preview workflow",
        "Pay Process action surface",
        "Admin Queue action",
        "ProcessPeriod LifecycleStatusCode",
        "no PayRun creation",
        "no finalisation payment bank file",
    ]

    for keyword in keywords:
        assert keyword in content


def test_mojibake_markers_are_absent_from_new_documents():
    content = _all_docs()

    mojibake_markers = ["â†’", "â€”", "�"]

    for marker in mojibake_markers:
        assert marker not in content

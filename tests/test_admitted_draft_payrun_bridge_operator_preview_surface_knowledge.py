from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md"
)
STRUCTURED_KNOWLEDGE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md"
)
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "admitted_draft_payrun_bridge_operator_preview_surface_v0_1"
    / "ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_admitted_draft_payrun_bridge_operator_preview_surface_knowledge_v01.md"
)

GOLDEN_QUESTIONS = [
    "1. What is the Admitted Draft PayRun Bridge Operator Preview Surface?",
    "2. Why is the Operator Preview Surface needed after the bridge operator action contract?",
    "3. What does preview mean in this context?",
    "4. Why is preview not execution?",
    "5. What should the operator see in the preview card?",
    "6. What should the guarded preview endpoint return?",
    "7. Why must the endpoint be dry-run/read-only by default?",
    "8. Why should there be no Process Now button yet?",
    "9. What has already been implemented in Workforce Platform before this slice?",
    "10. What is planned for the next Workforce slice?",
    "11. What must this slice not implement?",
    "12. How should Minerva explain this slice without overstating runtime behaviour?",
    "13. What runtime-overstatement risks should Minerva avoid?",
    "14. How does this slice preserve deterministic payroll authority?",
    "15. What evidence/story should be exposed by the preview surface?",
    "16. What is the next valid slice after preview visibility?",
]

PRIOR_BRIDGE_LINKS = [
    "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md",
    "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md",
    "docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md",
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
        "# Minerva Knowledge Capture — Admitted Draft PayRun Bridge Operator Preview Surface"
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


def test_preview_visibility_and_endpoint_doctrine_are_present():
    content = _all_docs()

    required = [
        "Preview is not execution",
        "preview is not execution",
        "Visibility is not mutation",
        "visibility is not mutation",
        "Endpoint is dry-run/read-only by default",
        "endpoint is dry-run/read-only by default",
        "dry-run/read-only by default",
        "No Process Now button yet",
        "no Process Now button",
        "no route",
        "no processing call",
        "must not call processing",
        "no route execution",
    ]

    for phrase in required:
        assert phrase in content


def test_no_payrun_or_payruncontact_creation_boundary_is_present():
    content = _all_docs()

    required = [
        "no PayRun creation",
        "no PayRunContact creation",
        "must not create PayRuns or PayRunContacts",
        "preview creates PayRuns or PayRunContacts",
    ]

    for phrase in required:
        assert phrase in content


def test_no_finalisation_payment_bank_file_or_automation_boundary_is_present():
    content = _all_docs()

    required = [
        "no finalisation",
        "no payment",
        "no bank file",
        "no payment batch",
        "no automation",
        "preview finalises or pays",
        "preview generates bank files",
        "preview is automation",
    ]

    for phrase in required:
        assert phrase in content


def test_prior_bridge_links_are_present():
    content = _all_docs()

    for link in PRIOR_BRIDGE_LINKS:
        assert link in content


def test_prohibited_claims_are_captured():
    content = _all_docs()

    prohibited_claims = [
        "operators can execute admitted draft processing from the UI",
        "the bridge route performs processing",
        "the UI has a Process Now button",
        "preview mutates PayRuns",
        "preview creates PayRuns or PayRunContacts",
        "preview finalises or pays",
        "preview generates bank files",
        "preview is automation",
        "Minerva calculates payroll",
        "deterministic processing authority moved to Minerva",
    ]

    for claim in prohibited_claims:
        assert claim in content


def test_no_action_attestation_is_present():
    content = _all_docs()

    attestations = [
        "No runtime changes",
        "No live LLM calls",
        "No DB access, reads, writes, migrations, or validation",
        "No workforce-platform changes",
        "No retrieval-plan/runtime behaviour changes",
        "No chat exposure",
        "No operational corpus/runtime state mutation",
    ]

    for attestation in attestations:
        assert attestation in content


def test_retrieval_keywords_and_aliases_are_present():
    content = _read(STRUCTURED_KNOWLEDGE)

    keywords = [
        "admitted draft bridge preview",
        "operator preview surface",
        "guarded preview endpoint",
        "dry-run pay process endpoint",
        "Pay Process bridge preview",
        "Command Centre bridge eligibility",
        "Admin Queue bridge preview",
        "no Process Now button",
        "preview is not execution",
        "actions not taken",
        "deterministic payroll authority",
        "execution gate later",
    ]

    for keyword in keywords:
        assert keyword in content


def test_mojibake_markers_are_absent_from_new_documents():
    content = _all_docs()

    mojibake_markers = ["â†’", "â€”", "�"]

    for marker in mojibake_markers:
        assert marker not in content

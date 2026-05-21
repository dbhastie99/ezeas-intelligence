from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
)
STRUCTURED_PACK = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_processing_bridge_v0_1.md"
)

GOLDEN_QUESTIONS = [
    "1. What is the Admitted Draft PayRun Processing Bridge?",
    "2. Why is this bridge needed after PayRun admission?",
    "3. What is the canonical governed path from source change to readiness update?",
    "4. Why does PayRunActionDecision remain the authority source?",
    "5. Can the bridge create a PayRun by itself?",
    "6. Can the bridge create a PayRunContact by itself?",
    "7. What guardrails protect finalised, frozen, paid, or payment-batch-generated PayRuns?",
    "8. Why must the bridge use existing deterministic processing paths?",
    "9. What should happen if the existing processing path is unsafe or unclear?",
    "10. Why must Minerva not calculate payroll outcomes?",
    "11. What is the difference between admission and processing?",
    "12. Why is ObjectTime payroll impact worker-period scoped?",
    "13. What idempotency risks does the bridge need to prevent?",
    "14. What evidence should the bridge preserve?",
    "15. How should readiness be updated after processing?",
    "16. What may this slice implement?",
    "17. What must this slice not implement?",
    "18. Why is this a large but bounded slice?",
    "19. How should Minerva explain admitted draft processing without overstating runtime behaviour?",
    "20. How does this bridge preserve deterministic payroll authority?",
]


def _content() -> str:
    return STRUCTURED_PACK.read_text(encoding="utf-8")


def test_source_response_and_structured_pack_exist():
    assert SOURCE_RESPONSE.exists()
    assert STRUCTURED_PACK.exists()


def test_structured_pack_declares_source_authority_and_linkage():
    content = _content()

    assert "Status: v0.1 structured Minerva knowledge pack." in content
    assert "derived from the reconstructed canonical source response" in content
    assert (
        "docs/knowledge/payroll/"
        "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
    ) in content
    assert (
        "[admitted_draft_payrun_processing_bridge_v0_1_source_response.md]"
        "(admitted_draft_payrun_processing_bridge_v0_1_source_response.md)"
    ) in content


def test_structured_pack_preserves_canonical_governed_path_terms():
    content = _content()

    required_terms = [
        "source change",
        "impact assessment",
        "action register",
        "PayRunActionDecision",
        "admission authority",
        "PayRun / PayRunContact resolved or created where authorised",
        "deterministic draft PayRunContact processing",
        "calculated draft payroll output",
        "evidence/story",
        "readiness update",
    ]

    for term in required_terms:
        assert term in content


def test_structured_pack_preserves_authority_lifecycle_scope_and_boundaries():
    content = _content()

    required_doctrine = [
        "PayRunActionDecision remains the authority source",
        "ProcessPeriod.LifecycleStatusCode is payroll-control truth",
        "IsOpen/IsClosed alone is insufficient",
        "ObjectTime payroll impact is worker-period scoped",
        "Minerva is advisory only",
        "Minerva must not calculate payroll dollars",
        "A parallel payroll processor is prohibited",
        "no parallel payroll processor",
        "finalised PayRuns",
        "paid PayRuns",
        "frozen PayRuns",
        "payment-batch-generated PayRuns",
        "bank-file-generated PayRuns",
        "lifecycle-closed PayRuns",
    ]

    for doctrine in required_doctrine:
        assert doctrine in content


def test_structured_pack_contains_all_twenty_golden_questions():
    content = _content()

    for question in GOLDEN_QUESTIONS:
        assert question in content


def test_structured_pack_contains_answer_guidance_for_all_twenty_questions():
    content = _content()

    assert content.count("Answer guidance:") == 20

    for question in GOLDEN_QUESTIONS:
        question_number = question.split(".", maxsplit=1)[0]
        heading = f"### {question}"
        assert heading in content

        guidance_start = content.find(heading)
        assert guidance_start != -1
        next_heading = content.find(f"### {int(question_number) + 1}.", guidance_start + 1)
        section = content[guidance_start:next_heading] if next_heading != -1 else content[guidance_start:]
        assert "Answer guidance:" in section


def test_structured_pack_contains_retrieval_keywords_and_aliases():
    content = _content()

    assert "## Retrieval Keywords And Aliases" in content
    keywords = [
        "admitted draft PayRun processing bridge",
        "PayRunActionDecision",
        "Pay Process admission",
        "admission authority",
        "action register",
        "draft PayRunContact processing",
        "deterministic payroll processing",
        "readiness update",
        "ProcessPeriod LifecycleStatusCode",
        "ObjectTime worker-period scope",
        "no parallel payroll processor",
        "Minerva advisory only",
        "payroll calculation authority",
        "finalised PayRun guardrail",
        "payment batch guardrail",
    ]

    for keyword in keywords:
        assert keyword in content


def test_structured_pack_contains_non_goal_warnings():
    content = _content()

    warnings = [
        "Do not treat Minerva as a payroll calculator.",
        "Do not treat admission as processing.",
        "Do not treat IsOpen/IsClosed as sufficient lifecycle control.",
        "Do not mutate finalised, frozen, paid, payment-batch-generated, bank-file-generated, or lifecycle-closed PayRuns.",
        "Do not create a new payroll engine.",
        "Do not overstate runtime implementation.",
    ]

    for warning in warnings:
        assert warning in content


def test_structured_pack_has_no_mojibake_markers():
    content = _content()

    mojibake_markers = ["â†’", "â€”", "�"]

    for marker in mojibake_markers:
        assert marker not in content

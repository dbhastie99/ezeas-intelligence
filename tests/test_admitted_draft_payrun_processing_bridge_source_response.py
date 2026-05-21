from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_RESPONSE = (
    ROOT
    / "docs"
    / "knowledge"
    / "payroll"
    / "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
)


def _content() -> str:
    return SOURCE_RESPONSE.read_text(encoding="utf-8")


def test_admitted_draft_payrun_processing_bridge_source_response_exists():
    assert SOURCE_RESPONSE.exists()


def test_reconstructed_source_note_and_heading_are_present():
    content = _content()

    assert "# Minerva Knowledge Capture — Admitted Draft PayRun Processing Bridge" in content
    assert (
        "This document is a reconstructed canonical source response created after the original full "
        "source response was unavailable in the repository/current Codex context."
    ) in content
    assert "Admitted Draft PayRun Processing Bridge v0.1" in content


def test_all_numbered_sections_are_present():
    content = _content()

    for section_number in range(1, 21):
        assert f"## {section_number}." in content

    assert "## 19. Suggested Minerva golden questions" in content


def test_all_golden_questions_are_present():
    content = _content()

    questions = [
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

    for question in questions:
        assert question in content


def test_canonical_governed_path_terms_are_present():
    content = _content()

    terms = [
        "source change",
        "impact assessment",
        "action register",
        "PayRunActionDecision",
        "admission authority",
        "PayRun / PayRunContact",
        "deterministic draft PayRunContact processing",
        "calculated draft payroll output",
        "evidence/story",
        "readiness update",
    ]

    for term in terms:
        assert term in content


def test_non_goals_are_present():
    content = _content()

    non_goals = [
        "no finalisation",
        "no payment",
        "no bank file",
        "no Minerva payroll calculation",
        "no parallel payroll processor",
    ]

    for non_goal in non_goals:
        assert non_goal in content


def test_mojibake_markers_are_absent():
    content = _content()

    mojibake_markers = ["\u00e2\u2020\u2019", "\u00e2\u20ac\u201d", "\ufffd"]

    for marker in mojibake_markers:
        assert marker not in content

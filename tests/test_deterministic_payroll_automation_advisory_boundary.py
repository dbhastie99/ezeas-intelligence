from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_deterministic_payroll_automation_advisory_boundary_v01.md"
)
KNOWLEDGE_DOCUMENT = (
    ROOT
    / "docs"
    / "knowledge"
    / "payroll"
    / "deterministic_payroll_automation_minerva_advisory_boundary_v0_1.md"
)
KNOWLEDGE_INDEX = ROOT / "docs" / "knowledge" / "README.md"


def _content() -> str:
    return KNOWLEDGE_DOCUMENT.read_text(encoding="utf-8")


def _normalise(text: str) -> str:
    return " ".join(text.split())


def test_prompt_artefact_contains_late_supplied_source_text():
    assert PROMPT_ARTEFACT.exists()

    content = PROMPT_ARTEFACT.read_text(encoding="utf-8")

    assert "## Knowledge Capture Source Text Supplied After Initial Stop" in content
    assert "Deterministic Payroll Automation and Minerva Advisory Boundary" in content
    assert "Minerva must not calculate or decide payroll dollars." in content


def test_deterministic_payroll_automation_advisory_boundary_document_exists_and_is_not_short_summary():
    assert KNOWLEDGE_DOCUMENT.exists()

    content = _content()

    assert len(content.splitlines()) >= 85
    assert len(content.split()) >= 650
    assert "Purpose of this knowledge capture" in content
    assert "The core doctrine" in content
    assert "Repository Doctrine Phrase Anchors" in content
    assert "Suggested Minerva Golden Questions" in content


def test_deterministic_payroll_automation_advisory_boundary_required_doctrine_phrases():
    content = _content()

    required_phrases = [
        "Minerva must not calculate payroll dollars.",
        "Payroll amounts, tax, net pay, deductions, statutory obligations, award entitlements, and payment amounts must be calculated deterministically.",
        "Minerva is a pattern-recognition and advisory evidence layer.",
        "Minerva may recommend hold/proceed/review, but it does not become the calculation authority.",
        "Automation may use Minerva advisory output as a risk signal, but not as a calculation source.",
        "Customer-configured guardrails determine how far automation may proceed.",
        "Human hold/defer/reject decisions generally override automation unless a governed policy says otherwise.",
        "Pay Process Orchestration preserves the action/decision/admission/processing chain.",
        "The next Workforce slice should be an admitted draft PayRun processing bridge.",
        "The admitted draft PayRun processing bridge must be deterministic.",
    ]

    for phrase in required_phrases:
        assert phrase in content


def test_deterministic_payroll_automation_advisory_boundary_preserves_core_source_text():
    normalised = _normalise(_content())

    source_anchors = [
        "This knowledge capture records a critical platform doctrine decision",
        "Every payroll decision that impacts gross pay, net pay, tax, deductions, statutory obligations, award entitlements, payment amounts, or final payroll outcomes must be made deterministically by the platform.",
        "Minerva must not calculate or decide payroll dollars.",
        "The deterministic Workforce Platform remains responsible for all payroll calculation truth.",
        "No amount that affects payroll outcome should exist because",
        "A payroll amount must come from deterministic source truth, governed configuration, deterministic rule selection, deterministic calculation, and auditable evidence.",
        "source truth → deterministic rule/configuration selection → deterministic calculation → deterministic payroll result → evidence/story → optional Minerva explanation/advisory assessment",
    ]

    for anchor in source_anchors:
        assert anchor in normalised


def test_deterministic_payroll_automation_advisory_boundary_preserves_suggested_golden_questions():
    content = _content()

    questions = [
        "Why must Minerva not calculate payroll dollars?",
        "Which payroll outcomes must remain deterministic platform outputs?",
        "What is Minerva allowed to do when payroll automation is configured?",
        "How can automation use Minerva advisory output without making Minerva the calculation source?",
        "Why are customer-configured guardrails required for payroll automation?",
        "Why do human hold, defer, or reject decisions generally override automation?",
        "How should Minerva explain the difference between a deterministic payroll result and an advisory risk signal?",
        "Why must Pay Process Orchestration preserve the action, decision, admission, and processing chain?",
        "What should the next Workforce slice build after this advisory-boundary knowledge pack?",
        "Why must an admitted draft PayRun processing bridge remain deterministic?",
    ]

    for question in questions:
        assert question in content


def test_deterministic_calculation_is_distinguished_from_minerva_advisory_risk_assessment():
    normalised = _normalise(_content())

    assert "deterministic Workforce Platform remains responsible for all payroll calculation truth" in normalised
    assert "Minerva’s role is to become an evidence intelligence and advisory layer" in normalised
    assert "Minerva advisory output as a risk signal, but not as a calculation source" in normalised
    assert "Minerva may recommend hold/proceed/review, but it does not become the calculation authority" in normalised


def test_deterministic_payroll_automation_advisory_boundary_non_goals_are_preserved():
    content = _content()

    non_goals = [
        "No live LLM calls.",
        "No operational JSON ingestion.",
        "No database mutation.",
        "No Workforce runtime integration.",
        "No chat/API/UI exposure.",
        "No payroll calculation implementation.",
        "No automation runtime implementation.",
        "No payment/banking execution implementation.",
        "No corpus mutation beyond adding repository knowledge docs/tests.",
    ]

    for non_goal in non_goals:
        assert non_goal in content


def test_deterministic_payroll_automation_advisory_boundary_is_linked_from_knowledge_index():
    assert KNOWLEDGE_INDEX.exists()

    index = KNOWLEDGE_INDEX.read_text(encoding="utf-8")

    assert "payroll/deterministic_payroll_automation_minerva_advisory_boundary_v0_1.md" in index
    assert "Deterministic Payroll Automation and Minerva Advisory Boundary" in index

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_RESPONSE = ROOT / "docs" / "knowledge" / "minerva_code_evidence_role_model_v0_1_source_response.md"
STRUCTURED_KNOWLEDGE = ROOT / "docs" / "knowledge" / "minerva_code_evidence_role_model_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "minerva_code_evidence_role_model_v0_1"
    / "ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_role_scoped_code_evidence_foundation_v01.md"
)

GOLDEN_QUESTIONS = [
    "1. Why does Minerva need code evidence?",
    "2. What are the two main uses of code evidence?",
    "3. How is developer technical use different from payroll-manager confirmation use?",
    "4. What can code evidence prove?",
    "5. What can code evidence not prove?",
    "6. Why is code evidence not payroll calculation authority?",
    "7. How should a developer answer expose code evidence?",
    "8. How should a payroll administrator answer use code evidence?",
    "9. How should a payroll user answer use code evidence?",
    "10. How should a worker answer use code evidence?",
    "11. What are the code evidence disclosure modes?",
    "12. How are roles mapped to disclosure modes?",
    "13. Why should Analytics be included as a future code evidence target?",
    "14. Why should Analytics full indexing be optional or deferred in v0.1?",
    "15. How should Minerva handle doctrine/code conflicts?",
    "16. How should Minerva handle code evidence without implementation-state documentation?",
    "17. Why do tests provide stronger evidence than code existence alone?",
    "18. What must Minerva never infer from code evidence alone?",
    "19. What repositories are active code evidence targets in v0.1?",
    "20. What remains out of scope for the Code Evidence foundation?",
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


def test_source_response_contains_required_title_and_sections():
    content = _read(SOURCE_RESPONSE)

    assert "# Minerva Knowledge Capture — Role-Scoped Code Evidence Foundation" in content
    assert "## Purpose of this knowledge capture" in content
    for section_number in range(1, 21):
        assert f"## {section_number}." in content


def test_all_twenty_golden_questions_exist_in_source_structured_and_evaluation_files():
    source = _read(SOURCE_RESPONSE)
    structured = _read(STRUCTURED_KNOWLEDGE)
    evaluation = _read(EVALUATION_BASELINE)

    for question in GOLDEN_QUESTIONS:
        assert question in source
        assert question in structured
        assert question in evaluation


def test_role_names_exist():
    content = _all_docs()

    for role in [
        "DEVELOPER",
        "PAYROLL_ADMINISTRATOR",
        "PAYROLL_USER",
        "CUSTOMER_ADMINISTRATOR",
        "WORKER",
    ]:
        assert role in content


def test_disclosure_modes_exist():
    content = _all_docs()

    for mode in [
        "TECHNICAL_DISCLOSURE",
        "IMPLEMENTATION_CONFIRMATION",
        "BACKGROUND_CONFIDENCE_ONLY",
        "NO_CODE_EVIDENCE",
    ]:
        assert mode in content


def test_analytics_future_optional_target_statement_exists():
    content = _all_docs()

    assert "ezeas-analytics" in content
    assert "future" in content.lower()
    assert "optional" in content.lower()
    assert "deferred" in content.lower()


def test_code_cannot_prove_runtime_availability_statement_exists():
    content = _all_docs().lower()

    assert "code evidence cannot prove runtime availability" in content
    assert "production/runtime availability requires route registration" in content


def test_prohibited_uses_section_exists():
    source = _read(SOURCE_RESPONSE)

    assert "## 18. Prohibited uses" in source
    for phrase in [
        "expose secrets",
        "dump raw code to non-developer users",
        "infer production readiness",
        "claim runtime availability from code alone",
        "execute code",
        "mutate repos",
        "bypass role access",
        "expose credentials",
        "suggest payroll calculation from code evidence",
    ]:
        assert phrase in source


def test_no_action_no_runtime_no_live_llm_no_db_no_repo_mutation_attestation_exists():
    content = _all_docs()

    for phrase in [
        "No runtime changes",
        "No live LLM calls",
        "No DB access",
        "No database migrations",
        "No repo mutation outside ezeas-intelligence",
        "No code execution",
        "No chat exposure",
    ]:
        assert phrase in content


def test_mojibake_markers_are_absent():
    content = _all_docs()

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in content

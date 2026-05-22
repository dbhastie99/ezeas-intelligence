from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "post_finalisation_treatment_decision_persistence_v0_1_source_response.md"
)
STRUCTURED_KNOWLEDGE = (
    PAYROLL_KNOWLEDGE_DIR
    / "post_finalisation_treatment_decision_persistence_v0_1.md"
)
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "post_finalisation_treatment_decision_persistence_v0_1"
    / "ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-22_minerva_post_finalisation_treatment_decision_persistence_knowledge_v01.md"
)

GOLDEN_QUESTIONS = [
    "1. What happens when ObjectTime changes after a regular PayRun is finalised?",
    "2. Why can’t the finalised regular PayRun just be reprocessed?",
    "3. What does “finalised PayRun protected” mean?",
    "4. What is a post-finalisation treatment decision?",
    "5. What is the difference between committing a treatment decision and executing treatment?",
    "6. When should supplementary be recommended?",
    "7. When should out-of-cycle or later treatment be considered?",
    "8. Why should retro not be offered unless evidence supports a retro scenario?",
    "9. What does the Admin Queue treatment workspace let the operator do?",
    "10. Is editing ObjectTime from Admin Queue the same as treatment execution?",
    "11. What should happen after ObjectTime is saved from Admin Queue?",
    "12. Which Worker Story is shown before the supplementary/correction run exists?",
    "13. What happens to Worker Story after a future supplementary run is created?",
    "14. What should finalisation details show?",
    "15. What information should be hidden or secondary rather than GUID-first?",
    "16. What does the backend decide versus what the UI displays?",
    "17. What remains deferred after treatment decision persistence?",
    "18. What must Minerva avoid overstating?",
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
        "# Minerva Knowledge Capture — Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace"
        in content
    )
    assert "## Purpose of this knowledge capture" in content

    for section_number in range(1, 20):
        assert f"## {section_number}." in content


def test_all_eighteen_golden_questions_are_present_in_core_documents():
    source = _read(SOURCE_RESPONSE)
    structured = _read(STRUCTURED_KNOWLEDGE)
    baseline = _read(EVALUATION_BASELINE)

    for question in GOLDEN_QUESTIONS:
        assert question in source
        assert question in structured
        assert question in baseline


def test_answer_guidance_exists_for_all_eighteen_questions():
    source = _read(SOURCE_RESPONSE)
    structured = _read(STRUCTURED_KNOWLEDGE)

    assert source.count("Answer guidance:") == 18
    assert structured.count("Answer guidance:") == 18


def test_treatment_decision_is_distinguished_from_treatment_execution():
    content = _all_docs()

    required = [
        "Reviewing a treatment item is not payroll execution",
        "Committing a treatment path is also not payroll execution",
        "Treatment decision commitment is not treatment execution",
        "Commit to supplementary does not mean a supplementary PayRun was created",
        "Commitment alone does not execute payroll",
    ]

    for phrase in required:
        assert phrase in content


def test_finalised_payrun_and_payruncontact_are_not_mutated():
    content = _all_docs()

    required = [
        "Finalised PayRuns and PayRunContacts must not be silently mutated",
        "finalised PayRun and finalised PayRunContact must remain protected",
        "No finalised PayRun mutation",
        "No finalised PayRunContact mutation",
        "finalised PayRunContact was dirtied",
    ]

    for phrase in required:
        assert phrase in content


def test_worker_story_regular_run_and_future_treatment_distinction_is_present():
    content = _all_docs()

    required = [
        "finalised regular-run worker story",
        "It is not the future supplementary/correction story",
        "future treatment run will produce its own Worker Story",
        "future supplementary/correction run will have its own Worker Story",
        "multiple stories exist for the same ProcessPeriod",
    ]

    for phrase in required:
        assert phrase in content


def test_objecttime_edit_is_source_truth_edit_not_treatment_execution():
    content = _all_docs()

    required = [
        "ObjectTime edit from Admin Queue is source-truth edit, not treatment execution",
        "Saving ObjectTime is a source-truth edit",
        "It is not supplementary, out-of-cycle, or retro payroll execution",
        "persist source truth, close the ObjectTime modal, and refresh Admin Queue / Pay Process state",
    ]

    for phrase in required:
        assert phrase in content


def test_backend_owns_treatment_recommendation():
    content = _all_docs()

    required = [
        "The backend owns",
        "treatment recommendation",
        "treatment path classification",
        "retro/supplementary/out-of-cycle recommendation",
        "whether execution is available",
        "UI must not infer",
        "backend-driven treatment recommendation",
    ]

    for phrase in required:
        assert phrase in content


def test_prohibited_claims_are_captured():
    content = _all_docs()

    prohibited_claims = [
        "committing supplementary means a supplementary PayRun was created",
        "committing a treatment decision means the worker has been paid",
        "the finalised regular PayRun was reprocessed",
        "the finalised PayRunContact was dirtied",
        "retro should be offered for every post-finalisation source change",
        "Worker Story shown is the future supplementary story",
        "Minerva calculated or authorised the treatment",
        "UI decides treatment path independently from backend evidence",
    ]

    for claim in prohibited_claims:
        assert claim in content


def test_no_action_no_runtime_attestation_is_present():
    content = _all_docs()

    attestations = [
        "No workforce-platform changes",
        "No runtime retrieval behaviour changes",
        "No retrieval-plan changes",
        "No database connection, reads, writes, migrations, or validation",
        "No live LLM calls",
        "No chat exposure",
        "No operational corpus/runtime state mutation",
        "No payroll calculation",
        "No supplementary execution",
        "No out-of-cycle execution",
        "No retro/correction execution",
        "No payment or banking execution",
        "No finalisation changes",
        "This Minerva slice is knowledge only",
    ]

    for attestation in attestations:
        assert attestation in content


def test_required_ui_explanation_terms_are_present():
    content = _all_docs()

    required_terms = [
        "Admin Queue",
        "sticky footer",
        "GUID-first",
        "finalisation details",
        "payroll totals",
    ]

    for term in required_terms:
        assert term in content


def test_structured_retrieval_keywords_and_aliases_are_present():
    content = _read(STRUCTURED_KNOWLEDGE)

    keywords = [
        "post-finalisation ObjectTime change",
        "treatment decision persistence",
        "commit to supplementary",
        "treatment decision versus execution",
        "finalised PayRun protected",
        "finalised regular-run worker story",
        "future supplementary worker story",
        "Admin Queue treatment workspace",
        "ObjectTime edit from Admin Queue",
        "no finalised PayRun mutation",
        "no retro unless evidence supports retro",
        "backend-driven treatment recommendation",
    ]

    for keyword in keywords:
        assert keyword in content


def test_mojibake_markers_are_absent_from_new_documents():
    content = _all_docs()

    mojibake_markers = ["â†’", "â€”", "�"]

    for marker in mojibake_markers:
        assert marker not in content


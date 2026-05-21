from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
)
STRUCTURED_PACK = PAYROLL_KNOWLEDGE_DIR / "admitted_draft_payrun_processing_bridge_v0_1.md"
EVALUATION_BASELINE = (
    ROOT
    / "docs"
    / "evaluation"
    / "admitted_draft_payrun_processing_bridge_v0_1"
    / "ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_admitted_draft_payrun_processing_bridge_answer_evaluation_v01.md"
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

PROHIBITED_CLAIMS = [
    "Minerva calculates payroll outcomes",
    "The bridge finalises PayRuns",
    "The bridge pays workers",
    "The bridge creates bank files",
    "The bridge creates payment batches",
    "The bridge can mutate finalised PayRuns",
    "The bridge can mutate paid PayRuns",
    "The bridge can mutate frozen PayRuns",
    "The bridge can mutate payment-batch-generated PayRuns",
    "The bridge can mutate bank-file-generated PayRuns",
    "Admission is the same as processing",
    "PayRunActionDecision is optional",
    "IsOpen/IsClosed alone is enough lifecycle truth",
    "ObjectTime impact is only row-scoped",
    "The bridge may invent a parallel payroll processor",
    "The runtime bridge is implemented and live unless implementation evidence is later ingested and tested",
    "The structured knowledge document replaces the source response",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _baseline() -> str:
    return _read(EVALUATION_BASELINE)


def _section_for(content: str, question: str) -> str:
    heading = f"### {question}"
    start = content.find(heading)
    assert start != -1
    next_heading = content.find("\n### ", start + len(heading))
    return content[start:] if next_heading == -1 else content[start:next_heading]


def _candidate_answer_passes(answer: str) -> bool:
    required_terms = (
        "PayRunActionDecision",
        "deterministic",
        "draft",
        "Minerva is advisory",
    )
    blocked_terms = (
        "Minerva calculates payroll outcomes",
        "runtime bridge is implemented and live",
        "parallel payroll processor",
    )

    return all(term in answer for term in required_terms) and not any(
        term in answer for term in blocked_terms
    )


def test_source_structured_and_evaluation_baseline_files_exist():
    assert SOURCE_RESPONSE.exists()
    assert STRUCTURED_PACK.exists()
    assert EVALUATION_BASELINE.exists()


def test_evaluation_baseline_links_to_source_and_structured_knowledge_files():
    content = _baseline()

    assert (
        "docs/knowledge/payroll/"
        "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
    ) in content
    assert "docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md" in content
    assert "Source-response path:" in content
    assert "Structured knowledge path:" in content


def test_all_twenty_golden_questions_are_present_in_evaluation_baseline():
    content = _baseline()

    for question in GOLDEN_QUESTIONS:
        assert question in content

    assert content.count("### ") == 20


def test_each_golden_question_has_expected_answer_guidance():
    content = _baseline()

    assert content.count("Expected answer themes:") == 20
    assert content.count("Prohibited claims:") == 20
    assert content.count("Required caveats:") == 20

    for question in GOLDEN_QUESTIONS:
        section = _section_for(content, question)
        assert "Expected answer themes:" in section
        assert "Prohibited claims:" in section
        assert "Required caveats:" in section


def test_evaluation_baseline_contains_prohibited_answer_claims():
    content = _baseline()

    for claim in PROHIBITED_CLAIMS:
        assert claim in content


def test_evaluation_baseline_contains_runtime_overstatement_caveat():
    content = _baseline()

    assert "Required Runtime Caveat" in content
    assert "doctrine, design, and current intended bridge behaviour" in content
    assert "must not claim the runtime bridge is implemented and live unless" in content
    assert "does not prove runtime bridge implementation" in content
    assert "production readiness" in content


def test_evaluation_baseline_contains_no_action_attestation():
    content = _baseline()

    attestations = [
        "No runtime changes: yes",
        "No live LLM calls: yes",
        "No DB access, reads, writes, migrations, or validation: yes",
        "No workforce-platform changes: yes",
        "No endpoint or UI changes: yes",
        "No external service calls: yes",
        "No corpus mutation: yes",
    ]

    for attestation in attestations:
        assert attestation in content


def test_minerva_advisory_no_payroll_calculation_boundary_is_present():
    content = _baseline()

    required = [
        "Minerva must not calculate payroll outcomes",
        "Minerva is advisory and evidence intelligence only",
        "payroll dollars",
        "gross, net, tax",
        "deductions",
        "award entitlements",
        "payment amounts",
        "bank-file values",
    ]

    for phrase in required:
        assert phrase in content


def test_finalised_frozen_paid_payment_batch_guardrails_are_present():
    content = _baseline()

    required = [
        "draft, unfinalised, unfrozen PayRuns",
        "Finalised, paid, frozen, payment-batch-generated, or bank-file-generated PayRuns must not be silently mutated",
        "payment-batch-generated",
        "bank-file-generated",
        "lifecycle-closed",
    ]

    for phrase in required:
        assert phrase in content


def test_process_period_lifecycle_status_doctrine_is_present():
    content = _baseline()

    assert "ProcessPeriod.LifecycleStatusCode is payroll-control truth" in content
    assert "IsOpen/IsClosed alone is insufficient" in content


def test_objecttime_worker_period_scope_doctrine_is_present():
    content = _baseline()

    assert "ObjectTime payroll impact is worker-period scoped" in content
    assert "not row scoped" in content
    assert "Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime" in content


def test_no_parallel_payroll_processor_doctrine_is_present():
    content = _baseline()

    assert "A parallel payroll processor is prohibited" in content
    assert "The bridge may invent a parallel payroll processor" in content
    assert "Do not say Minerva or the bridge may invent a new payroll engine" in content


def test_test_only_candidate_answer_evaluator_rejects_prohibited_claims():
    safe_answer = (
        "PayRunActionDecision remains authority. The bridge targets draft PayRuns, uses deterministic "
        "processing where safe, and Minerva is advisory."
    )
    unsafe_answer = (
        "PayRunActionDecision remains authority, but the runtime bridge is implemented and live and "
        "Minerva calculates payroll outcomes through a parallel payroll processor."
    )

    assert _candidate_answer_passes(safe_answer) is True
    assert _candidate_answer_passes(unsafe_answer) is False


def test_prompt_artefact_exists_and_preserves_evaluation_only_boundary():
    assert PROMPT_ARTEFACT.exists()
    content = _read(PROMPT_ARTEFACT)

    assert "Admitted Draft PayRun Processing Bridge Answer Evaluation v0.1" in content
    assert "evaluation-only" in content
    assert "no runtime changes" in content
    assert "no workforce-platform changes" in content
    assert "no live LLM calls" in content
    assert "no database migrations" in content


def test_evaluation_baseline_has_no_mojibake_markers():
    content = _baseline()

    mojibake_markers = ["\u00e2\u2020\u2019", "\u00e2\u20ac\u201d", "\ufffd"]

    for marker in mojibake_markers:
        assert marker not in content

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LIFECYCLE_PACK = ROOT / "docs" / "knowledge" / "pay_process_lifecycle_automation_policy_foundation_v0_1.md"
ORCHESTRATION_PACK = ROOT / "docs" / "knowledge" / "payroll" / "pay_process_orchestration_v0_1.md"
ORCHESTRATION_SOURCE_RESPONSE = (
    ROOT / "docs" / "knowledge" / "payroll" / "pay_process_orchestration_v0_1_source_response.md"
)
KNOWLEDGE_INDEX = ROOT / "docs" / "knowledge" / "README.md"


def _content() -> str:
    return LIFECYCLE_PACK.read_text(encoding="utf-8")


def _orchestration_content() -> str:
    return ORCHESTRATION_SOURCE_RESPONSE.read_text(encoding="utf-8")


def _normalise(text: str) -> str:
    return " ".join(text.split())


def test_process_period_lifecycle_automation_policy_pack_exists_and_is_verbose():
    assert LIFECYCLE_PACK.exists()

    content = _content()

    assert len(content.splitlines()) >= 650
    assert "Minerva Knowledge Capture" in content
    assert "ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation" in content
    assert "Purpose of this knowledge capture" in content
    assert "Suggested Minerva golden questions" in content


def test_process_period_lifecycle_automation_policy_required_doctrine_phrases():
    content = _content()

    required_phrases = [
        "ProcessPeriod lifecycle status is payroll-control truth",
        "Automation policy is a governed payroll-control contract",
        "Adding automation policy fields does not mean automation execution is implemented",
        "Automation must be optional, configurable, auditable, and explainable",
        "Payment/bank batch generation is an absolute financial-control freeze",
        "Regular close-for-review and supplementary close-for-review are distinct gates",
        "The UI must not infer payroll lifecycle, treatment routing, automation eligibility, admission status, or readiness",
        "This slice implements the policy/status foundation required for future automation",
        "Automation is not a shortcut around governance",
        "action → decision/policy authority → admission → processing → readiness",
    ]

    for phrase in required_phrases:
        assert phrase in content


def test_process_period_lifecycle_automation_policy_required_sections():
    content = _content()

    required_sections = [
        "What we are doing",
        "Why we are doing it now",
        "Why ProcessPeriod lifecycle status matters",
        "Why lifecycle status must not be hidden or implicit",
        "Why users need to modify lifecycle status",
        "Why automation policy matters",
        "Why automation fields probably belong on ProcessPeriodGroup",
        "Why automation must not be execution yet",
        "Why human decisions must generally override automation",
        "Why operators will benefit",
        "Why flexibility matters",
        "Why this benefits the Command Centre",
        "Why this benefits Admin Queue",
        "Why this benefits PayRun Detail",
        "Consequences for system design",
        "Consequences for implementation sequence",
        "Important non-goals",
        "Operator-facing explanation",
        "Minerva answer guidance",
        "Suggested Minerva golden questions",
    ]

    for section in required_sections:
        assert section in content


def test_process_period_lifecycle_automation_policy_non_goals_are_preserved():
    content = _content()

    non_goals = [
        "finalisation execution",
        "payment execution",
        "bank file generation",
        "payment batch creation",
        "automatic PayRun creation",
        "automatic PayRunContact creation",
        "automatic ObjectTime processing",
        "automatic decision creation",
        "admission execution",
        "interpreter runtime changes",
        "tax calculation",
        "deduction calculation",
        "retro execution",
        "recovery execution",
        "manual adjustment creation",
        "arbitrary pay-line creation",
        "Admin Queue rebuild",
        "customer-specific hardcoded automation",
    ]

    for non_goal in non_goals:
        assert non_goal in content


def test_process_period_lifecycle_automation_policy_golden_questions_are_preserved():
    content = _content()

    questions = [
        "Why does Pay Process Orchestration need ProcessPeriod lifecycle status?",
        "What is the difference between regular close-for-review and supplementary close-for-review?",
        "Why is payment/bank batch generation treated as a freeze?",
        "Why does automation policy belong on ProcessPeriodGroup rather than being hidden in code?",
        "Does adding automation policy fields mean automation is now executing?",
        "Why must human hold/defer/reject decisions generally override automation?",
        "How does automation help payroll operators without weakening control?",
        "Why does the Command Centre need pay-process lifecycle and automation visibility?",
        "Why does Admin Queue need pay-process context?",
        "What should Minerva say if a user asks whether the platform automatically creates PayRuns now?",
        "How should Minerva explain the difference between lifecycle status, automation policy, PayRunActionDecision, and PayRun admission?",
        "Why should the UI not infer payroll treatment routing?",
        "Why is this slice required before the Pay Process Operator Surface?",
        "What are the non-goals of the ProcessPeriod Lifecycle + Automation Policy Foundation slice?",
        "How does this work support future same-cycle supplementary processing?",
        "How does this work support future retro routing?",
        "How does this work support customer-specific payroll automation preferences?",
        "Why is this more flexible than a fixed payroll cutoff model?",
        "Why is this safer than hidden background automation?",
        "How does this slice preserve the difference between controlled-readiness and runtime execution?",
    ]

    for question in questions:
        assert question in content


def test_process_period_lifecycle_automation_policy_is_linked_from_knowledge_index():
    assert KNOWLEDGE_INDEX.exists()

    index = KNOWLEDGE_INDEX.read_text(encoding="utf-8")

    assert "pay_process_lifecycle_automation_policy_foundation_v0_1.md" in index
    assert "ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation" in index


def test_pay_process_orchestration_source_response_exists_and_is_authoritative():
    assert ORCHESTRATION_SOURCE_RESPONSE.exists()

    content = _orchestration_content()
    normalised = _normalise(content)

    assert "Canonical source response" in content
    assert "intentionally verbose and must not be summarised" in content
    assert "Minerva Knowledge Pack — Pay Process Orchestration v0.1" in content
    assert "It must not yet execute payment, mutate finalised payroll truth, create bank files, run full retro execution, or bypass review gates." in normalised


def test_pay_process_orchestration_source_response_required_sections_are_preserved():
    content = _orchestration_content()

    required_sections = [
        "Purpose",
        "Core Decision",
        "Slice 1 Purpose",
        "Existing Admin Queue Is Not Rebuilt",
        "ObjectTime Is the Primary Payroll Source-Truth Driver",
        "ObjectTime Impact Action Scope",
        "Period-Level ObjectTime Assessment",
        "ObjectTime Is 1:1 With ProcessPeriod",
        "ProcessPeriodGroup Must Be Effective-Date Aware",
        "ProcessPeriod State and Routing",
        "Supplementary Close for Review",
        "Supplementary vs Out-of-Cycle vs Bank Execution",
        "Bank File / Payment Batch Generation Is an Absolute Freeze",
        "Inclusion Status Matters",
        "Approved Actions Become Stale If Source Truth Changes",
        "No-Impact Changes",
        "Bank Account Doctrine",
        "Deduction Doctrine",
        "Tax Doctrine",
        "Key Consequence",
    ]

    for section in required_sections:
        assert f"## {section}" in content


def test_pay_process_orchestration_source_response_required_anchor_phrases_are_preserved():
    normalised = _normalise(_orchestration_content())

    required_phrases = [
        "ObjectTime impact action scope =",
        "Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime",
        "Admin Queue = cross-platform exception/review workbench",
        "PayRun Control Centre = pay-process operating surface",
        "ObjectTime drives payroll calculation impact.",
        "Bank accounts drive payment instruction resolution.",
        "Tax settings drive withholding/gross-to-net context.",
        "Deductions drive deduction application and remittance context.",
        "Supplementary = extra/corrective payroll treatment",
        "Out-of-cycle = payment timing",
        "Bank/payment execution = cash movement",
        "Once the bank file/payment batch is generated, its contents cannot be silently changed.",
        "Approval attaches to the assessed snapshot.",
        "NO_PAYROLL_IMPACT",
        "FIELD_LEVEL_IMPACT_FILTER_DEFERRED",
        "NO_PAYROLL_IMPACT_DETECTION_NOT_IMPLEMENTED",
        "A bank account change is not tied to a PayRun.",
        "Deduction setup changes are not ObjectTime-style payroll source truth.",
        "Tax setting changes are gross-to-net and payment-date context.",
        "It must not yet execute payment, mutate finalised payroll truth, create bank files, run full retro execution, or bypass review gates.",
    ]

    for phrase in required_phrases:
        assert phrase in normalised


def test_pay_process_orchestration_source_response_preserves_full_reasoning_anchors():
    normalised = _normalise(_orchestration_content())

    reasoning_anchors = [
        "first \"bring it together\" payroll theme after the correction and retro foundation slices",
        "The existing Admin Queue is consumed and not rebuilt.",
        "The action is period-scoped because the question is: given the current ObjectTime truth",
        "repeated edits should update one active action and preserve every edit in evidence",
        "One ObjectTime record change requires assessment of the worker's ObjectTime set for the ProcessPeriod.",
        "Historical ObjectTime must use effective-date-aware ProcessPeriodGroup resolution.",
        "Regular close for review, supplementary close for review, and bank/payment batch generation are separate gates.",
        "Supplementary close-for-review gives operators a separate gate",
        "This freeze is stronger than ordinary review stability.",
        "Slice 1 needs inclusion status rather than only readiness.",
        "Approved actions become stale if source truth changes.",
        "Field-level no-impact detection is deferred because",
        "Bank account changes are date-effective payment instruction truth.",
        "Deduction setup changes are date-effective deduction instruction changes.",
        "Tax setting changes are gross-to-net and payment-date context.",
        "Slice 1 is visibility/classification, not execution.",
    ]

    for anchor in reasoning_anchors:
        assert anchor in normalised


def test_pay_process_orchestration_golden_questions_and_expected_anchors_are_preserved():
    content = _orchestration_content()
    normalised = _normalise(content)

    questions = [
        "What is the full purpose of Pay Process Orchestration v0.1?",
        "Why is the Admin Queue not rebuilt?",
        "What is the ObjectTime impact action scope?",
        "Why is the ObjectTime impact action period-scoped rather than row-scoped?",
        "What is the difference between supplementary, out-of-cycle, and bank/payment execution?",
        "Why is bank/payment batch generation an absolute freeze point?",
        "Why is a bank account change not tied to a PayRun?",
        "Why are deductions not ObjectTime-style payroll source truth?",
        "Why are tax settings gross-to-net/payment-date context?",
        "What is the consequence of Slice 1?",
    ]
    expected_answer_anchors = [
        "Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime",
        "Admin Queue = cross-platform exception/review workbench",
        "PayRun Control Centre = pay-process operating surface",
        "Supplementary = payroll treatment / extra or corrective payroll treatment",
        "Out-of-cycle = payment timing",
        "Bank/payment execution = cash movement",
        "bank/payment batch generation is an absolute freeze",
        "approval attaches to assessed snapshot",
        "bank account changes are date-effective payment instruction truth",
        "deduction setup changes are date-effective deduction instruction changes",
        "tax setting changes are gross-to-net/payment-date context",
        "Slice 1 is visibility/classification, not execution",
    ]

    for question in questions:
        assert question in content

    for anchor in expected_answer_anchors:
        assert anchor in normalised


def test_pay_process_orchestration_structured_pack_references_canonical_source_response():
    assert ORCHESTRATION_PACK.exists()

    content = ORCHESTRATION_PACK.read_text(encoding="utf-8")

    assert "pay_process_orchestration_v0_1_source_response.md" in content
    assert "authoritative full knowledge capture" in content
    assert "Structured summaries in this file are not complete replacements" in content
    assert "live LLM calls" in content
    assert "database mutation" in content
    assert "Workforce runtime integration" in content
    assert "API exposure" in content
    assert "UI/chat exposure" in content
    assert "operational payroll execution" in content
    assert "payment execution" in content
    assert "finalised truth mutation" in content


def test_pay_process_orchestration_is_linked_from_knowledge_index():
    assert KNOWLEDGE_INDEX.exists()

    index = KNOWLEDGE_INDEX.read_text(encoding="utf-8")

    assert "payroll/pay_process_orchestration_v0_1.md" in index
    assert "payroll/pay_process_orchestration_v0_1_source_response.md" in index

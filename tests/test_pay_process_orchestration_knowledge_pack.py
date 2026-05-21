from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LIFECYCLE_PACK = ROOT / "docs" / "knowledge" / "pay_process_lifecycle_automation_policy_foundation_v0_1.md"
KNOWLEDGE_INDEX = ROOT / "docs" / "knowledge" / "README.md"


def _content() -> str:
    return LIFECYCLE_PACK.read_text(encoding="utf-8")


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

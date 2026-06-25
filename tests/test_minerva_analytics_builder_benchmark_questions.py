import json
from pathlib import Path


BENCHMARK_PATH = Path("metadata/minerva/analytics_builder_benchmark_questions.v0_1.json")
DOMAIN_RETRIEVAL_PLAN_PATH = Path("app/services/domain_retrieval_plan_service.py")


REQUIRED_QUESTIONS = {
    "Which dataset should I use for payroll cost by worksite?",
    "Which visual recipe should I use for payroll cost by rate type?",
    "Why is final-paid payroll truth blocked?",
    "Can I use PayrollLedger as bank-paid proof?",
    "Does CalcInterpreterLine prove payment execution?",
    "Does ObjectTime prove payment finality?",
    "Why are there zero Certified assets?",
    "What is the difference between Diagnostic, Transitional, Blocked, and Certified?",
    "What validations exist for payroll outcome analytics?",
    "What validation gaps remain?",
    "What should a reviewer look at first?",
    "What blocked gaps need upstream proof?",
    "How should Minerva explain blocked gaps?",
    "What claims are prohibited for final-paid truth?",
    "What is the recommended next stream after static v0.2?",
}


def _load_benchmark():
    return json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))


def test_analytics_builder_benchmark_question_plan_parses():
    benchmark = _load_benchmark()

    assert benchmark["benchmark_plan_id"] == "analytics_builder_benchmark_questions_v0_1"
    assert benchmark["domain_key"] == "analytics_builder_guide"
    assert benchmark["status"] == "planned_pending_source_ingestion"
    assert benchmark["actual_answer_baselines_created"] is False


def test_analytics_builder_benchmark_question_plan_includes_all_required_questions():
    benchmark = _load_benchmark()
    questions = {entry["question"] for entry in benchmark["questions"]}

    assert REQUIRED_QUESTIONS.issubset(questions)
    assert len(benchmark["questions"]) >= 15


def test_analytics_builder_benchmark_entries_contain_required_safety_and_prohibited_fields():
    benchmark = _load_benchmark()
    required_fields = {
        "id",
        "question",
        "expected_answer_intent",
        "required_source_artifact_types",
        "required_safety_wording",
        "prohibited_wording",
        "expected_status_terms",
        "answer_definitiveness",
    }

    for entry in benchmark["questions"]:
        assert required_fields.issubset(entry)
        assert entry["required_source_artifact_types"]
        assert entry["required_safety_wording"]
        assert entry["prohibited_wording"]
        assert entry["expected_status_terms"]


def test_analytics_builder_benchmark_final_paid_questions_require_qualified_or_blocked_wording():
    benchmark = _load_benchmark()
    final_paid_entries = [
        entry
        for entry in benchmark["questions"]
        if "final-paid" in json.dumps(entry).lower() or "bank-paid" in json.dumps(entry).lower()
    ]

    assert final_paid_entries
    for entry in final_paid_entries:
        entry_text = json.dumps(entry)
        assert "UNPROVEN" in entry_text or "Blocked" in entry_text
        assert "not enough governed proof" in entry_text or "Final-paid payroll truth remains UNPROVEN / Blocked" in entry_text


def test_analytics_builder_planned_domain_was_not_added_to_runtime_retrieval_registry():
    service_text = DOMAIN_RETRIEVAL_PLAN_PATH.read_text(encoding="utf-8")

    assert "ANALYTICS_BUILDER_GUIDE" not in service_text
    assert "analytics_builder_guide" not in service_text

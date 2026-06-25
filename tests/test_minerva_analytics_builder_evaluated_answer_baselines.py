import json
from pathlib import Path


BASELINE_PATH = Path("metadata/minerva/analytics_builder_evaluated_answer_baselines.v0_1.json")
SAMPLE_EVAL_PATH = Path("samples/eval/analytics_builder_benchmark.evaluated_non_production.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_beautiful2_evaluated_answer_baselines.json")


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


def _load_baseline():
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _entry(question):
    entries = {entry["question"]: entry for entry in _load_baseline()["evaluated_baseline_entries"]}
    return entries[question]


def _text(value):
    return json.dumps(value, sort_keys=True)


def test_analytics_builder_evaluated_answer_baseline_metadata_parses():
    baseline = _load_baseline()

    assert baseline["baseline_id"] == "analytics_builder_evaluated_answer_baselines_v0_1"
    assert baseline["baseline_version"] == "v0_1"
    assert baseline["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_evaluated_baselines_are_non_production_pending_promotion():
    baseline = _load_baseline()

    assert baseline["baseline_status"] == "evaluated_non_production_pending_safety_promotion"
    assert baseline["production_answer_use_status"] == "not_allowed_pending_safety_promotion"
    assert baseline["production_passed"] is False
    assert baseline["runtime_enabled"] is False
    assert baseline["beautiful3_safety_promotion_required"] is True
    assert baseline["no_runtime_behavior"] is True
    assert baseline["no_trust_posture_change"] is True
    assert baseline["no_source_repo_modification"] is True


def test_analytics_builder_evaluated_baselines_reference_required_sources():
    baseline = _load_baseline()

    assert baseline["source_import_ref"] == "metadata/minerva/analytics_builder_governed_source_import.v0_1.json"
    assert baseline["source_benchmark_question_plan_ref"] == "metadata/minerva/analytics_builder_benchmark_questions.v0_1.json"
    assert baseline["source_answer_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert baseline["source_retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"
    assert baseline["source_answer_baseline_stubs_ref"] == "metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json"
    assert baseline["source_safety_harness_ref"] == "metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json"


def test_analytics_builder_all_15_questions_have_evaluated_entries():
    baseline = _load_baseline()
    questions = {entry["question"] for entry in baseline["evaluated_baseline_entries"]}

    assert len(baseline["evaluated_baseline_entries"]) == 15
    assert questions == REQUIRED_QUESTIONS
    assert all(entry["evaluated_answer_status"] == "evaluated_non_production" for entry in baseline["evaluated_baseline_entries"])


def test_analytics_builder_every_evaluated_answer_has_sources_and_safety_fields():
    for entry in _load_baseline()["evaluated_baseline_entries"]:
        assert entry["expected_answer"]
        assert entry["source_extract_refs"]
        assert all(ref.startswith("docs/knowledge/minerva/analytics_builder/imported_corpus/") for ref in entry["source_extract_refs"])
        assert entry["required_safety_terms_present"]
        assert entry["prohibited_claims_absent"]
        assert entry["proof_status_terms"]
        assert entry["certification_status_terms"]
        assert entry["blocked_status_terms"]
        assert entry["answer_limitations"]
        assert entry["allowed_confidence"]
        assert entry["not_allowed_claims"]
        assert entry["readiness_for_safety_promotion"] == "ready_for_beautiful3_static_safety_checks"


def test_analytics_builder_final_paid_answer_preserves_unproven_blocked_posture():
    entry = _entry("Why is final-paid payroll truth blocked?")
    text = _text(entry)

    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in text
    assert "not enough governed proof" in text
    assert "settlement" in text
    assert "bank acceptance" in text
    assert "remittance" in text


def test_analytics_builder_payrollledger_answer_says_not_bank_paid_proof():
    text = _text(_entry("Can I use PayrollLedger as bank-paid proof?"))

    assert "PayrollLedger is not bank-paid proof" in text
    assert "does not prove settlement" in text


def test_analytics_builder_calcinterpreterline_answer_says_not_payment_execution_proof():
    text = _text(_entry("Does CalcInterpreterLine prove payment execution?"))

    assert "CalcInterpreterLine is calculation/detail evidence" in text
    assert "does not prove payment execution" in text


def test_analytics_builder_objecttime_answer_says_not_payment_finality_proof():
    text = _text(_entry("Does ObjectTime prove payment finality?"))

    assert "ObjectTime is source-context evidence" in text
    assert "not payment finality proof" in text


def test_analytics_builder_certified_assets_answer_preserves_zero_count():
    text = _text(_entry("Why are there zero Certified assets?"))

    assert "zero Certified assets" in text
    assert "not Certified" in text
    assert "Blocked assets require upstream proof" in text


def test_analytics_builder_blocked_gap_answers_treat_gaps_as_safety_controls():
    text = _text(_entry("How should Minerva explain blocked gaps?")) + _text(
        _entry("What blocked gaps need upstream proof?")
    )

    assert "safety controls" in text
    assert "not enough governed proof" in text
    assert "review/exception analytics" in text
    assert "final bank-paid payroll truth" in text


def test_analytics_builder_sample_eval_file_is_non_production_not_passed():
    sample = json.loads(SAMPLE_EVAL_PATH.read_text(encoding="utf-8"))

    assert sample["benchmark_status"] == "evaluated_non_production_pending_safety_promotion"
    assert sample["production_passed"] is False
    assert sample["runtime_enabled"] is False
    assert sample["live_llm_evaluation_used"] is False
    assert sample["production_answer_use_status"] == "not_allowed_pending_safety_promotion"
    assert sample["beautiful3_safety_promotion_required"] is True
    assert len(sample["questions"]) == 15


def test_analytics_builder_diagnostic_records_non_runtime_and_no_trust_change():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["status"] == "completed_evaluated_non_production_pending_safety_promotion"
    assert diagnostic["evaluated_question_count"] == 15
    assert diagnostic["production_passed"] is False
    assert diagnostic["runtime_enabled"] is False
    assert diagnostic["live_llm_evaluation_used"] is False
    assert diagnostic["beautiful3_safety_promotion_required"] is True
    assert diagnostic["certified_asset_count"] == 0
    assert diagnostic["final_paid_truth"] == "UNPROVEN / Blocked"
    assert diagnostic["no_runtime_behavior"] is True
    assert diagnostic["no_trust_posture_change"] is True
    assert diagnostic["no_source_repo_modification"] is True

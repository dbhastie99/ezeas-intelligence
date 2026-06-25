import json
from pathlib import Path


STUB_PATH = Path("metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m6_answer_baseline_stubs.json")
SAMPLE_EVAL_PATH = Path("samples/eval/analytics_builder_benchmark.planned.v0_1.json")


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


def _load_stubs():
    return json.loads(STUB_PATH.read_text(encoding="utf-8"))


def _entry(question):
    entries = {entry["question"]: entry for entry in _load_stubs()["baseline_entries"]}
    return entries[question]


def _text(value):
    return json.dumps(value, sort_keys=True)


def test_analytics_builder_answer_baseline_stubs_parse():
    stubs = _load_stubs()

    assert stubs["baseline_stub_id"] == "analytics_builder_answer_baseline_stubs_v0_1"
    assert stubs["baseline_stub_version"] == "v0_1"
    assert stubs["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_answer_baseline_stubs_reference_required_milestones():
    stubs = _load_stubs()

    assert stubs["source_benchmark_question_plan_ref"] == "metadata/minerva/analytics_builder_benchmark_questions.v0_1.json"
    assert stubs["answer_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert stubs["retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"
    assert stubs["governed_import_manifest_ref"] == "metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json"


def test_analytics_builder_answer_baseline_stubs_are_planned_pending_not_production_passed():
    stubs = _load_stubs()

    assert stubs["baseline_status"] == "planned_pending_governed_source_import"
    assert stubs["production_answer_use_status"] == "not_allowed_pending_governed_source_ingestion_and_evaluation"
    assert stubs["production_passed"] is False
    assert stubs["runtime_enabled"] is False
    assert stubs["no_runtime_behavior"] is True
    assert stubs["no_trust_posture_change"] is True
    assert stubs["no_source_repo_modification"] is True


def test_analytics_builder_all_m1_benchmark_questions_have_stubs():
    stubs = _load_stubs()
    questions = {entry["question"] for entry in stubs["baseline_entries"]}

    assert len(stubs["baseline_entries"]) == 15
    assert questions == REQUIRED_QUESTIONS
    assert all(entry["baseline_status"] == "planned_pending" for entry in stubs["baseline_entries"])


def test_analytics_builder_every_baseline_entry_has_required_safety_and_prohibited_wording():
    for entry in _load_stubs()["baseline_entries"]:
        assert entry["required_safety_wording"]
        assert entry["prohibited_wording"]
        assert entry["required_status_terms"]
        assert entry["required_qualification"]
        assert entry["answer_definitiveness_limit"]
        assert entry["expected_outline"]
        assert entry["must_not_claim"]
        assert entry["safety_assertions"]
        assert entry["readiness_blockers"]
        assert entry["allowed_when"]
        assert entry["evaluation_notes"]


def test_analytics_builder_final_paid_question_blocks_final_paid_overclaims():
    entry = _entry("Why is final-paid payroll truth blocked?")
    text = _text(entry)

    assert "final-paid payroll truth remains UNPROVEN / Blocked" in text
    assert "not enough governed proof" in text
    assert "final-paid truth is proven" in text
    assert "PayRun finalisation proves payment" in text
    assert "PayrollLedger proves bank-paid truth" in text


def test_analytics_builder_payrollledger_question_blocks_bank_paid_overclaim():
    entry = _entry("Can I use PayrollLedger as bank-paid proof?")
    text = _text(entry)

    assert "PayrollLedger does not prove bank-paid truth" in text
    assert "PayrollLedger proves bank-paid proof" in text
    assert "settlement" in text
    assert "remittance" in text


def test_analytics_builder_calcinterpreterline_question_blocks_payment_execution_overclaim():
    entry = _entry("Does CalcInterpreterLine prove payment execution?")
    text = _text(entry)

    assert "CalcInterpreterLine is calculation/detail evidence" in text
    assert "not payment execution" in text
    assert "CalcInterpreterLine proves payment execution" in text
    assert "CalcInterpreterLine proves final-paid truth" in text


def test_analytics_builder_objecttime_question_blocks_payment_finality_overclaim():
    entry = _entry("Does ObjectTime prove payment finality?")
    text = _text(entry)

    assert "ObjectTime is source-context evidence" in text
    assert "not payment finality" in text
    assert "ObjectTime proves payment finality" in text
    assert "ObjectTime proves final-paid truth" in text


def test_analytics_builder_certification_question_preserves_zero_certified_assets():
    entry = _entry("Why are there zero Certified assets?")
    text = _text(entry)

    assert "Current Certified asset count is zero" in text
    assert "not Certified unless source metadata says Certified" in text
    assert "Diagnostic/Transitional assets may be useful with warnings but are not Certified" in text
    assert "production-certified" in text


def test_analytics_builder_blocked_gap_question_treats_gaps_as_safety_controls():
    entry = _entry("How should Minerva explain blocked gaps?")
    text = _text(entry)

    assert "Blocked gaps are safety controls, not failures" in text
    assert "not enough governed proof" in text
    assert "blocked gaps are defects" in text
    assert "blocked means broken" in text


def test_analytics_builder_sample_eval_file_is_planned_pending_if_created():
    assert SAMPLE_EVAL_PATH.exists()

    sample = json.loads(SAMPLE_EVAL_PATH.read_text(encoding="utf-8"))
    assert sample["benchmark_status"] == "planned_pending_governed_source_import"
    assert sample["production_passed"] is False
    assert sample["runtime_enabled"] is False
    assert sample["production_answer_use_status"] == "not_allowed_pending_governed_source_ingestion_and_evaluation"
    assert len(sample["questions"]) == 15
    assert all(question["status"] == "planned_pending" for question in sample["questions"])


def test_analytics_builder_m6_diagnostic_records_no_runtime_or_trust_change():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["status"] == "completed_planned_pending_only"
    assert diagnostic["production_passed"] is False
    assert diagnostic["runtime_enabled"] is False
    assert diagnostic["no_runtime_behavior"] is True
    assert diagnostic["no_trust_posture_change"] is True
    assert diagnostic["no_source_repo_modification"] is True
    assert diagnostic["safety_posture"]["certified_asset_count"] == 0
    assert diagnostic["safety_posture"]["final_paid_truth"] == "UNPROVEN / Blocked"

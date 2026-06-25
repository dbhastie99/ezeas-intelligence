import json
from pathlib import Path


PACK_PATH = Path("metadata/minerva/analytics_builder_demo_readiness_pack.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m8_demo_readiness_pack.json")
DOC_PATHS = [
    Path("docs/minerva/analytics_builder/20260624_demo_readiness_pack.md"),
    Path("docs/minerva/analytics_builder/20260624_demo_script.md"),
    Path("docs/minerva/analytics_builder/20260624_reviewer_checklist.md"),
    Path("docs/minerva/analytics_builder/20260624_good_bad_answer_examples.md"),
]
GOOD_BAD_PATH = Path("docs/minerva/analytics_builder/20260624_good_bad_answer_examples.md")


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


def _load_pack():
    return json.loads(PACK_PATH.read_text(encoding="utf-8"))


def _text(value):
    return json.dumps(value, sort_keys=True)


def test_analytics_builder_demo_readiness_metadata_parses():
    pack = _load_pack()

    assert pack["pack_id"] == "analytics_builder_demo_readiness_pack_v0_1"
    assert pack["pack_version"] == "v0_1"
    assert pack["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_demo_readiness_references_m1_to_m7_artifacts():
    pack = _load_pack()

    assert pack["source_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert pack["answer_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert pack["benchmark_question_plan_ref"] == "metadata/minerva/analytics_builder_benchmark_questions.v0_1.json"
    assert pack["retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"
    assert pack["governed_import_manifest_ref"] == "metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json"
    assert pack["answer_baseline_stubs_ref"] == "metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json"
    assert pack["safety_regression_harness_ref"] == "metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json"


def test_analytics_builder_demo_readiness_is_non_production_and_blocked():
    pack = _load_pack()

    assert pack["demo_status"] == "static_non_production_demo_readiness"
    assert pack["production_answer_use_status"] == "not_allowed_pending_governed_source_ingestion_and_evaluation"
    assert pack["production_passed"] is False
    assert pack["runtime_enabled"] is False
    assert pack["live_llm_evaluation_enabled"] is False
    assert pack["no_runtime_behavior"] is True
    assert pack["no_trust_posture_change"] is True
    assert pack["no_source_repo_modification"] is True


def test_analytics_builder_demo_readiness_covers_all_15_benchmark_questions():
    pack = _load_pack()
    questions = {entry["question"] for entry in pack["demo_questions"]}

    assert len(pack["demo_questions"]) == 15
    assert questions == REQUIRED_QUESTIONS
    sequence_ids = {group["sequence_id"] for group in pack["demo_sequence"]}
    assert sequence_ids == {
        "dataset_recipe_selection",
        "validation_certification",
        "final_paid_safety",
        "blocked_gap_review",
        "next_stream_decision",
    }


def test_analytics_builder_demo_question_entries_include_required_safety_and_review_fields():
    for entry in _load_pack()["demo_questions"]:
        assert entry["question_id"]
        assert entry["demo_status"] == "planned_pending_only"
        assert entry["expected_safe_answer_shape"]
        assert entry["required_source_refs"]
        assert entry["required_safety_rules"]
        assert entry["prohibited_claims"]
        assert entry["reviewer_observation_points"]
        assert entry["current_readiness_blocker"]
        assert entry["future_promotion_requirement"]


def test_analytics_builder_demo_readiness_docs_exist():
    for path in DOC_PATHS:
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()


def test_analytics_builder_good_bad_examples_cover_required_safety_cases():
    content = GOOD_BAD_PATH.read_text(encoding="utf-8")

    assert "Final-paid payroll truth is available" in content
    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in content
    assert "PayrollLedger proves the worker has been paid by the bank" in content
    assert "PayrollLedger is reconciliation evidence, not bank-paid proof" in content
    assert "CalcInterpreterLine confirms payment execution" in content
    assert "CalcInterpreterLine is calculation/detail evidence" in content
    assert "ObjectTime proves payment finality" in content
    assert "ObjectTime is source-context evidence, not payment finality" in content
    assert "There are Certified Analytics Builder assets" in content
    assert "Current Certified asset count is zero" in content
    assert "This rendered visual is certified" in content
    assert "Visual rendering is presentation output only and is not certification proof" in content
    assert "Blocked gaps are defects" in content
    assert "Blocked gaps are safety controls that identify missing upstream proof" in content


def test_analytics_builder_demo_pack_preserves_promotion_gate_and_blockers():
    pack = _load_pack()
    text = _text(pack)

    assert pack["promotion_gate_summary"]["current_gate_result"] == "blocked_pending_governed_source_ingestion_and_answer_evaluation"
    assert "governed_source_ingestion_not_executed" in pack["readiness_blockers"]
    assert "answer_evaluation_not_recorded" in pack["readiness_blockers"]
    assert "production_answer_use_explicitly_authorized_by_governed_review" in text
    assert "Minerva can answer Analytics Builder questions in production." in text


def test_analytics_builder_m8_diagnostic_records_static_non_runtime_status():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["status"] == "completed_static_non_production_demo_readiness"
    assert diagnostic["demo_status"] == "static_non_production_demo_readiness"
    assert diagnostic["demo_question_count"] == 15
    assert diagnostic["production_passed"] is False
    assert diagnostic["runtime_enabled"] is False
    assert diagnostic["live_llm_evaluation_enabled"] is False
    assert diagnostic["no_runtime_behavior"] is True
    assert diagnostic["no_trust_posture_change"] is True
    assert diagnostic["no_source_repo_modification"] is True
    assert diagnostic["certified_asset_count"] == 0
    assert diagnostic["final_paid_truth"] == "UNPROVEN / Blocked"

import json
from pathlib import Path


DOMAIN_PATH = Path("metadata/minerva/analytics_builder_retrieval_domain.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m2_retrieval_domain.json")
RUNTIME_RETRIEVAL_PLAN_PATH = Path("app/services/domain_retrieval_plan_service.py")


REQUIRED_GROUP_IDS = {
    "dataset_selection",
    "visual_recipe_selection",
    "certification_status",
    "validation_manifest",
    "certification_evidence_packets",
    "certification_readiness",
    "internal_review_demo_walkthroughs",
    "blocked_gap_roadmap",
    "blocked_gap_action_pack",
    "final_paid_truth_safety",
    "payrollledger_bridge_safety",
    "calcinterpreterline_safety",
    "objecttime_safety",
    "prohibited_claims",
    "next_stream_decision",
}


REQUIRED_ROUTING_QUESTIONS = {
    "Which dataset should I use for payroll cost by worksite?",
    "Why is final-paid truth blocked?",
    "Can PayrollLedger prove bank-paid truth?",
    "What validations exist?",
    "Why are there zero Certified assets?",
    "What should a reviewer look at first?",
    "What blocked gaps need upstream proof?",
}


def _load_domain():
    return json.loads(DOMAIN_PATH.read_text(encoding="utf-8"))


def _group(domain, group_id):
    groups = {group["group_id"]: group for group in domain["retrieval_term_groups"]}
    return groups[group_id]


def _combined_text(value):
    return json.dumps(value, sort_keys=True)


def test_analytics_builder_retrieval_domain_metadata_parses():
    domain = _load_domain()

    assert domain["retrieval_domain_id"] == "analytics_builder_retrieval_domain_v0_1"
    assert domain["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_retrieval_domain_is_not_production_enabled_without_registry_update():
    domain = _load_domain()

    assert domain["domain_status"] == "planned_static_corpus_pending"
    assert domain["registry_update_made"] is False
    assert domain["not_production_enabled"] is True
    assert domain["no_runtime_behavior"] is True
    assert domain["no_trust_posture_change"] is True


def test_analytics_builder_retrieval_domain_references_m1_artifacts():
    domain = _load_domain()

    assert domain["source_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert domain["answer_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert domain["benchmark_question_plan_ref"] == "metadata/minerva/analytics_builder_benchmark_questions.v0_1.json"


def test_analytics_builder_retrieval_domain_contains_required_term_groups():
    domain = _load_domain()
    group_ids = {group["group_id"] for group in domain["retrieval_term_groups"]}

    assert REQUIRED_GROUP_IDS.issubset(group_ids)
    for group in domain["retrieval_term_groups"]:
        assert group["purpose"]
        assert group["positive_terms"]
        assert group["negative_or_confusion_terms"]
        assert group["required_source_artifact_groups"]
        assert group["required_safety_rules"]
        assert group["benchmark_question_ids_supported"]


def test_final_paid_retrieval_terms_include_blocked_unproven_and_finality_safety():
    domain = _load_domain()
    text = _combined_text(_group(domain, "final_paid_truth_safety"))

    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in text
    assert "not enough governed proof" in text
    assert "PayRun finalisation or SUCCEEDED status alone does not prove settlement" in text
    assert "payment finality" in text


def test_payrollledger_retrieval_terms_include_not_bank_paid_proof_warning():
    domain = _load_domain()
    text = _combined_text(_group(domain, "payrollledger_bridge_safety"))

    assert "PayrollLedger does not prove bank-paid truth" in text
    assert "not enough governed proof" in text
    assert "not standalone settlement" in text


def test_calcinterpreterline_retrieval_terms_include_calculation_detail_warning():
    domain = _load_domain()
    text = _combined_text(_group(domain, "calcinterpreterline_safety"))

    assert "CalcInterpreterLine is calculation/detail evidence" in text
    assert "not payment execution" in text
    assert "not final-paid truth" in text


def test_objecttime_retrieval_terms_include_source_context_not_payment_finality_warning():
    domain = _load_domain()
    text = _combined_text(_group(domain, "objecttime_safety"))

    assert "ObjectTime is source-context evidence, not payment finality" in text
    assert "not bank-paid, settlement, remittance, final-paid, or certification proof" in text
    assert "roster-vs-actual is proven" in text


def test_prohibited_routing_confusions_are_present():
    domain = _load_domain()
    confusions = set(domain["prohibited_routing_confusions"])

    assert "Do not route final-paid proof questions only to generic payroll lifecycle material." in confusions
    assert "Do not route payment execution questions as if Analytics Builder has certified final-paid proof." in confusions
    assert "Do not route ObjectTime scheduling questions as if roster-vs-actual is proven." in confusions
    assert "Do not route CalcInterpreterLine questions as if it is final-paid proof." in confusions
    assert "Do not route rendered visual questions as certification proof." in confusions
    assert "Do not route blocked-gap questions as defects/failures." in confusions


def test_routing_examples_cover_key_m1_benchmark_questions():
    domain = _load_domain()
    questions = {example["question"] for example in domain["routing_examples"]}

    assert REQUIRED_ROUTING_QUESTIONS.issubset(questions)
    assert all(example["route_to_domain"] == "analytics_builder_guide" for example in domain["routing_examples"])


def test_retrieval_domain_runtime_registry_was_not_modified_for_m2():
    domain = _load_domain()
    service_text = RUNTIME_RETRIEVAL_PLAN_PATH.read_text(encoding="utf-8")

    assert domain["registry_update_made"] is False
    assert "ANALYTICS_BUILDER_GUIDE" not in service_text
    assert "analytics_builder_guide" not in service_text


def test_retrieval_domain_diagnostic_records_no_runtime_or_trust_changes():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["runtime_registry_changed"] is False
    assert diagnostic["runtime_retrieval_behavior_changed"] is False
    assert diagnostic["production_enabled"] is False
    assert diagnostic["source_documents_ingested"] is False
    assert diagnostic["app_routes_created"] is False
    assert diagnostic["runtime_ui_created"] is False
    assert diagnostic["bi_dashboards_created"] is False
    assert diagnostic["sql_write_paths_created"] is False
    assert diagnostic["stored_procedures_created"] is False
    assert diagnostic["final_paid_truth_changed"] is False
    assert diagnostic["certification_posture_changed"] is False
    assert diagnostic["trust_posture_changed"] is False
    assert diagnostic["ezeas_analytics_modified"] is False

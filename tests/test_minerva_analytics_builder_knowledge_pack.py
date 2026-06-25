import json
from pathlib import Path


PACK_PATH = Path("metadata/minerva/analytics_builder_knowledge_pack.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m3_corpus_knowledge_pack.json")

STATIC_DOCS = [
    Path("docs/knowledge/minerva/analytics_builder/README.md"),
    Path("docs/knowledge/minerva/analytics_builder/static_corpus_index.md"),
    Path("docs/knowledge/minerva/analytics_builder/source_artifact_groups.md"),
    Path("docs/knowledge/minerva/analytics_builder/safety_summary.md"),
    Path("docs/minerva/analytics_builder/20260624_knowledge_pack.md"),
    Path("docs/minerva/analytics_builder/20260624_static_corpus_registration.md"),
]

REQUIRED_GROUPS = {
    "analytics_builder_guide_spine",
    "dataset_catalogue",
    "dataset_cards",
    "visual_recipe_library",
    "visual_recipe_cards",
    "certification_rules",
    "prohibited_claims",
    "validation_manifest",
    "certification_evidence_packets",
    "certification_readiness_report",
    "internal_review_demo_walkthrough_pack",
    "blocked_gap_roadmap",
    "blocked_gap_action_pack",
    "v0_2_closeout",
    "generated_static_guide",
}


def _load_pack():
    return json.loads(PACK_PATH.read_text(encoding="utf-8"))


def test_analytics_builder_knowledge_pack_manifest_parses():
    pack = _load_pack()

    assert pack["knowledge_pack_id"] == "analytics_builder_knowledge_pack_v0_1"
    assert pack["pack_version"] == "v0_1"
    assert pack["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_knowledge_pack_references_m1_and_m2_artifacts():
    pack = _load_pack()

    assert pack["source_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert pack["answer_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert pack["benchmark_question_plan_ref"] == "metadata/minerva/analytics_builder_benchmark_questions.v0_1.json"
    assert pack["retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"


def test_analytics_builder_knowledge_pack_includes_required_source_artifact_groups():
    pack = _load_pack()
    groups = {group["artifact_group_id"] for group in pack["source_artifact_groups"]}

    assert REQUIRED_GROUPS.issubset(groups)
    assert set(pack["missing_source_artifacts"]) == REQUIRED_GROUPS


def test_analytics_builder_knowledge_pack_has_status_and_ingestion_method():
    pack = _load_pack()

    assert pack["pack_status"] == "static_corpus_registered_metadata_only"
    assert pack["ingestion_method"] == "metadata_registration_only"
    assert pack["source_content_copied"] is False
    assert pack["generated_content_copied"] is False


def test_analytics_builder_knowledge_pack_does_not_claim_production_answer_use():
    pack = _load_pack()

    assert pack["production_answer_use_status"] == "not_allowed_pending_governed_source_ingestion"
    assert pack["no_runtime_behavior"] is True
    assert pack["no_trust_posture_change"] is True
    assert pack["no_source_repo_modification"] is True


def test_analytics_builder_knowledge_pack_includes_required_safety_requirements():
    text = json.dumps(_load_pack(), sort_keys=True)

    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in text
    assert "PayrollLedger does not prove bank-paid truth" in text
    assert "CalcInterpreterLine is calculation/detail evidence" in text
    assert "ObjectTime is source-context evidence, not payment finality" in text
    assert "Current Certified asset count is zero" in text
    assert "Visual rendering is not certification proof" in text
    assert "not enough governed proof" in text


def test_analytics_builder_static_knowledge_pack_docs_exist():
    for path in STATIC_DOCS:
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()


def test_analytics_builder_knowledge_pack_source_groups_have_required_fields():
    pack = _load_pack()
    required = {
        "artifact_group_id",
        "source_paths_expected",
        "knowledge_pack_status",
        "minerva_use",
        "safety_notes",
        "required_before_baseline_answers",
        "required_before_production_answer_use",
    }

    for group in pack["source_artifact_groups"]:
        assert required.issubset(group)
        assert group["source_paths_expected"]
        assert "pending" in group["knowledge_pack_status"]


def test_analytics_builder_m3_diagnostic_records_no_runtime_or_trust_changes():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["source_content_copied"] is False
    assert diagnostic["generated_content_copied"] is False
    assert diagnostic["runtime_ingestion_created"] is False
    assert diagnostic["production_answer_use_enabled"] is False
    assert diagnostic["app_routes_created"] is False
    assert diagnostic["runtime_ui_created"] is False
    assert diagnostic["bi_dashboards_created"] is False
    assert diagnostic["sql_write_paths_created"] is False
    assert diagnostic["stored_procedures_created"] is False
    assert diagnostic["runtime_behavior_changed"] is False
    assert diagnostic["ezeas_analytics_modified"] is False
    assert diagnostic["final_paid_truth_changed"] is False
    assert diagnostic["certification_posture_changed"] is False
    assert diagnostic["trust_posture_changed"] is False

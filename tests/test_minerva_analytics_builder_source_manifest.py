import json
from pathlib import Path


MANIFEST_PATH = Path("metadata/minerva/analytics_builder_source_manifest.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_ingestion_slice1.json")


REQUIRED_ARTIFACT_GROUPS = {
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


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_analytics_builder_source_manifest_parses():
    manifest = _load_manifest()

    assert manifest["manifest_id"] == "analytics_builder_source_manifest_v0_1"
    assert manifest["domain_key"] == "analytics_builder_guide"
    assert manifest["source_repo"] == "ezeas-analytics"
    assert manifest["recommended_source_tag"] == "analytics-builder-static-omg-v0.2-20260624"


def test_analytics_builder_source_manifest_includes_required_ezeas_analytics_artifact_groups():
    manifest = _load_manifest()
    artifacts = manifest["source_artifacts"]
    groups = {artifact["artifact_group"] for artifact in artifacts}

    assert REQUIRED_ARTIFACT_GROUPS.issubset(groups)
    assert all(artifact["source_repo"] == "ezeas-analytics" for artifact in artifacts)


def test_analytics_builder_source_manifest_entries_have_required_readiness_fields():
    manifest = _load_manifest()
    required_fields = {
        "source_repo",
        "source_path",
        "expected_purpose",
        "expected_minerva_use",
        "trust_finality_warning_requirement",
        "ingestion_status",
        "required_before_production_answer_use",
    }

    for artifact in manifest["source_artifacts"]:
        assert required_fields.issubset(artifact)
        assert artifact["ingestion_status"] == "expected_source_pending_review"
        assert artifact["trust_finality_warning_requirement"]


def test_analytics_builder_source_manifest_preserves_v0_2_portfolio_status():
    manifest = _load_manifest()
    status = manifest["portfolio_status"]

    assert status["datasets"] == 9
    assert status["visual_recipes"] == 13
    assert status["validation_assets"] == 6
    assert status["validation_gaps"] == 4
    assert status["certification_evidence_packets"] == 22
    assert status["certified_assets"] == 0
    assert status["certification_status_counts"]["Certified"] == 0
    assert status["proof_status_counts"] == {"LIKELY": 14, "UNPROVEN": 8}


def test_analytics_builder_source_manifest_is_not_runtime_ingestion():
    manifest = _load_manifest()
    ingestion_state = manifest["ingestion_state"]

    assert ingestion_state["status"] == "static_corpus_pending"
    assert ingestion_state["actual_source_content_copied"] is False
    assert ingestion_state["runtime_indexing_performed"] is False
    assert ingestion_state["production_answer_use_allowed"] is False


def test_analytics_builder_slice_diagnostic_records_no_runtime_or_external_repo_changes():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["retrieval_registry_changed"] is False
    assert diagnostic["source_documents_ingested"] is False
    assert diagnostic["runtime_index_created"] is False
    assert diagnostic["app_routes_created"] is False
    assert diagnostic["runtime_ui_created"] is False
    assert diagnostic["bi_dashboards_created"] is False
    assert diagnostic["sql_write_paths_created"] is False
    assert diagnostic["stored_procedures_created"] is False
    assert diagnostic["runtime_behavior_changed"] is False
    assert diagnostic["external_repositories_modified"] is False
    assert diagnostic["ezeas_analytics_modified"] is False
    assert diagnostic["final_paid_truth_changed"] is False
    assert diagnostic["certification_posture_changed"] is False

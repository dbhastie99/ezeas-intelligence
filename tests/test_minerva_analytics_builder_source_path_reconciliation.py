import json
from pathlib import Path


RECONCILIATION_PATH = Path("metadata/minerva/analytics_builder_source_path_reconciliation.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m4_source_path_reconciliation.json")

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


def _load_reconciliation():
    return json.loads(RECONCILIATION_PATH.read_text(encoding="utf-8"))


def test_analytics_builder_source_path_reconciliation_metadata_parses():
    reconciliation = _load_reconciliation()

    assert reconciliation["reconciliation_id"] == "analytics_builder_source_path_reconciliation_v0_1"
    assert reconciliation["reconciliation_version"] == "v0_1"
    assert reconciliation["source_repo"] == "ezeas-analytics"
    assert reconciliation["analytics_tag_expected"] == "analytics-builder-static-omg-v0.2-20260624"


def test_analytics_builder_source_path_reconciliation_references_m1_and_m3():
    reconciliation = _load_reconciliation()

    assert reconciliation["m1_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert reconciliation["m3_knowledge_pack_ref"] == "metadata/minerva/analytics_builder_knowledge_pack.v0_1.json"
    assert reconciliation["m2_retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"


def test_analytics_builder_source_path_reconciliation_includes_all_m1_artifact_groups():
    reconciliation = _load_reconciliation()
    expected_groups = set(reconciliation["expected_artifact_groups"])
    result_groups = {result["artifact_group_id"] for result in reconciliation["expected_path_results"]}

    assert REQUIRED_GROUPS.issubset(expected_groups)
    assert REQUIRED_GROUPS.issubset(result_groups)


def test_analytics_builder_source_path_reconciliation_each_group_has_path_results_and_recommendation():
    reconciliation = _load_reconciliation()

    for result in reconciliation["expected_path_results"]:
        assert result["artifact_group_id"]
        assert result["expected_paths"]
        assert "found_exact_paths" in result
        assert "discovered_alternative_paths" in result
        assert result["recommended_canonical_source_paths"]
        assert result["import_recommendation"] in {
            "reference_only",
            "compact_extract",
            "metadata_copy",
            "do_not_copy_generated_artifact",
            "unresolved",
        }
        assert result["reason"]
        assert result["required_before_m5_answer_baselines"]


def test_analytics_builder_generated_html_is_not_marked_bulk_copy_source_truth():
    reconciliation = _load_reconciliation()
    generated = next(
        result
        for result in reconciliation["expected_path_results"]
        if result["artifact_group_id"] == "generated_static_guide"
    )

    assert generated["import_recommendation"] == "do_not_copy_generated_artifact"
    assert "docs/generated/analytics_builder_guide/index.html" in generated["recommended_canonical_source_paths"]
    assert "presentation output only" in generated["reason"]
    assert any("docs/generated/analytics_builder_guide/**/*.html" in item["path"] for item in reconciliation["artifacts_not_safe_to_copy"])


def test_analytics_builder_production_answer_use_remains_blocked_before_governed_import():
    reconciliation = _load_reconciliation()

    assert reconciliation["production_answer_use_allowed"] is False
    assert reconciliation["readiness_for_answer_baselines"] == "blocked_until_governed_import_manifest_is_created_and_reviewed"
    assert "Dataset portfolio count is 9" in json.dumps(reconciliation["missing_or_unresolved_artifacts"])
    assert "Visual recipe portfolio count is 13" in json.dumps(reconciliation["missing_or_unresolved_artifacts"])


def test_analytics_builder_reconciliation_records_actual_canonical_roots():
    reconciliation = _load_reconciliation()
    discovered = reconciliation["discovered_actual_paths"]

    assert discovered["metadata_root"] == "metadata/analytics_builder/"
    assert discovered["guide_markdown_root"] == "docs/analytics_builder_guide/"
    assert discovered["generated_html_root"] == "docs/generated/analytics_builder_guide/"
    assert discovered["certification_packet_count_discovered"] == 22
    assert discovered["generated_html_count_discovered"] == 38


def test_analytics_builder_m4_diagnostic_records_no_runtime_or_source_repo_changes():
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert diagnostic["source_repo_modified"] is False
    assert diagnostic["runtime_behavior_changed"] is False
    assert diagnostic["app_routes_created"] is False
    assert diagnostic["runtime_ui_created"] is False
    assert diagnostic["bi_dashboards_created"] is False
    assert diagnostic["sql_write_paths_created"] is False
    assert diagnostic["stored_procedures_created"] is False
    assert diagnostic["final_paid_truth_changed"] is False
    assert diagnostic["certification_posture_changed"] is False
    assert diagnostic["trust_posture_changed"] is False
    assert diagnostic["m5_answer_baselines_safe"] is False

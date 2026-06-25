import json
from pathlib import Path


IMPORT_PATH = Path("metadata/minerva/analytics_builder_governed_source_import.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_beautiful1_governed_source_import.json")
CORPUS_ROOT = Path("docs/knowledge/minerva/analytics_builder/imported_corpus")


def _load_import():
    return json.loads(IMPORT_PATH.read_text(encoding="utf-8"))


def _read_extract(name):
    return (CORPUS_ROOT / name).read_text(encoding="utf-8")


def _text(value):
    return json.dumps(value, sort_keys=True)


def test_analytics_builder_governed_source_import_metadata_parses():
    metadata = _load_import()

    assert metadata["import_id"] == "analytics_builder_governed_source_import_v0_1"
    assert metadata["import_version"] == "v0_1"
    assert metadata["import_status"] == "governed_static_source_import_executed"
    assert metadata["domain_key"] == "analytics_builder_guide"


def test_analytics_builder_governed_source_import_references_m1_to_m8_artifacts():
    metadata = _load_import()

    assert metadata["m1_source_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert metadata["m2_retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"
    assert metadata["m3_knowledge_pack_ref"] == "metadata/minerva/analytics_builder_knowledge_pack.v0_1.json"
    assert metadata["m4_source_path_reconciliation_ref"] == "metadata/minerva/analytics_builder_source_path_reconciliation.v0_1.json"
    assert metadata["m5_governed_import_manifest_ref"] == "metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json"
    assert metadata["m6_answer_baseline_stubs_ref"] == "metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json"
    assert metadata["m7_safety_harness_ref"] == "metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json"
    assert metadata["m8_demo_readiness_ref"] == "metadata/minerva/analytics_builder_demo_readiness_pack.v0_1.json"


def test_analytics_builder_governed_source_import_records_source_repo_and_tag_or_commit():
    metadata = _load_import()
    source = metadata["source_tag_or_commit_checked"]

    assert metadata["source_repo"] == "ezeas-analytics"
    assert metadata["source_repo_path_checked"] == "C:/Projects/ezeas-analytics"
    assert source["expected_tag"] == "analytics-builder-static-omg-v0.2-20260624"
    assert source["expected_tag_commit"] == "ec6728fda1fbf107b2be0253066c55ac2a242675"
    assert source["current_head_commit_inspected"] == "177fa0533e9758d349f6ef009f5ffcfa98cb91c9"
    assert metadata["source_status_at_import"]["git_status_short"] == "clean"


def test_analytics_builder_governed_source_import_includes_artifact_groups_and_extracts():
    metadata = _load_import()
    group_ids = {group["artifact_group_id"] for group in metadata["imported_artifact_groups"]}

    assert group_ids == {
        "dataset_catalogue",
        "visual_recipe_library",
        "validation_and_certification",
        "blocked_gaps",
        "cockpit_contracts",
        "minerva_safety",
    }
    assert len(metadata["compact_extracts_created"]) == 8
    for extract in metadata["compact_extracts_created"]:
        assert Path(extract).exists()


def test_analytics_builder_generated_html_is_not_source_truth_or_bulk_copied():
    metadata = _load_import()
    policy = metadata["generated_html_reference_policy"]
    text = _text(metadata["artifacts_not_copied"])

    assert policy["bulk_copied"] is False
    assert policy["source_truth"] is False
    assert policy["allowed_use"] == "reference_only_for_static_guide_navigation"
    assert "docs/generated/analytics_builder_guide/**/*.html" in text
    assert "Generated HTML is presentation output only" in text


def test_analytics_builder_dataset_extract_exists_and_includes_9_datasets():
    content = _read_extract("dataset_catalogue_extract.md")

    assert "Total dataset count: 9." in content
    assert "5 governed active dataset cards plus 4 blocked/gap dataset assets" in content
    assert "payroll_outcome_line_v0_1" in content
    assert "worker_worksite_context_dimensions_v0_1" in content
    assert "standalone_calc_interpreter_line_detail" in content
    assert "final_bank_paid_payroll_truth" in content


def test_analytics_builder_visual_recipe_extract_exists_and_includes_13_recipes():
    content = _read_extract("visual_recipe_extract.md")

    assert "Total visual recipe count: 13." in content
    assert "9 governed active visual recipe cards plus 4 blocked recipe assets" in content
    assert "payroll_cost_by_rate_type" in content
    assert "payroll_cost_by_worksite" in content
    assert "worker_pay_story" in content
    assert "roster_vs_actual_scheduling_coverage" in content


def test_analytics_builder_validation_certification_extract_preserves_counts_and_zero_certified():
    content = _read_extract("validation_and_certification_extract.md")

    assert "Validation assets: 6." in content
    assert "Validation gaps: 4." in content
    assert "Certification evidence packets: 22." in content
    assert "Certified assets: 0." in content
    assert "Current Certified asset count remains zero." in content


def test_analytics_builder_blocked_gap_extract_includes_all_four_blocked_gaps():
    content = _read_extract("blocked_gap_extract.md")

    assert "review/exception analytics" in content
    assert "roster-vs-actual/ObjectTime scheduling coverage" in content
    assert "standalone CalcInterpreterLine detail" in content
    assert "final bank-paid payroll truth" in content
    assert "Blocked gaps are safety controls, not failures." in content


def test_analytics_builder_cockpit_contract_extract_exists_and_covers_contracts():
    content = _read_extract("cockpit_contract_extract.md")

    assert "Cockpit functional contract." in content
    assert "Cockpit data contract." in content
    assert "Cockpit export and evidence pack contract." in content
    assert "Module connector contract." in content
    assert "Runtime entrypoint contract." in content
    assert "Access-control doctrine." in content
    assert "Refresh model doctrine." in content
    assert "Standalone/hybrid cockpit architecture discovery." in content
    assert "analytics.ezeas.com" in content


def test_analytics_builder_safety_extract_preserves_final_paid_blocked_posture():
    content = _read_extract("minerva_safety_extract.md")

    assert "Final-paid payroll truth remains UNPROVEN / Blocked." in content
    assert "PayrollLedger is not bank-paid proof." in content
    assert "CalcInterpreterLine is calculation/detail evidence, not payment execution proof." in content
    assert "ObjectTime is source-context evidence, not payment finality proof." in content
    assert "Visual rendering is not certification proof." in content


def test_analytics_builder_production_answer_use_remains_blocked_and_baselines_can_proceed_non_production():
    metadata = _load_import()
    readiness = metadata["answer_baseline_readiness_after_import"]

    assert metadata["production_answer_use_status"] == "not_allowed_pending_evaluated_baselines_and_safety_promotion"
    assert readiness["beautiful_slice_2_evaluated_answer_baselines_can_proceed"] is True
    assert readiness["allowed_scope"] == "evaluated_non_production_answer_baselines_only"
    assert readiness["production_passed_baselines_allowed"] is False


def test_analytics_builder_governed_source_import_preserves_static_non_runtime_boundaries():
    metadata = _load_import()
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert metadata["no_runtime_behavior"] is True
    assert metadata["no_trust_posture_change"] is True
    assert metadata["no_source_repo_modification"] is True
    assert diagnostic["generated_html_copied"] is False
    assert diagnostic["certified_asset_count"] == 0
    assert diagnostic["final_paid_truth"] == "UNPROVEN / Blocked"
    assert diagnostic["beautiful_slice_2_evaluated_answer_baselines_can_proceed"] is True

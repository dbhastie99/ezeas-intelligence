import json
from pathlib import Path


MANIFEST_PATH = Path("metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json")
DIAGNOSTIC_PATH = Path("docs/diagnostics/20260624_minerva_analytics_builder_m5_source_count_import_manifest.json")


def _load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_analytics_builder_governed_import_manifest_parses():
    manifest = _load_manifest()

    assert manifest["import_manifest_id"] == "analytics_builder_governed_import_manifest_v0_1"
    assert manifest["import_manifest_version"] == "v0_1"
    assert manifest["source_repo"] == "ezeas-analytics"
    assert manifest["source_tag_checked"] == "analytics-builder-static-omg-v0.2-20260624"


def test_analytics_builder_governed_import_manifest_references_m1_m3_and_m4():
    manifest = _load_manifest()

    assert manifest["m1_source_manifest_ref"] == "metadata/minerva/analytics_builder_source_manifest.v0_1.json"
    assert manifest["m3_knowledge_pack_ref"] == "metadata/minerva/analytics_builder_knowledge_pack.v0_1.json"
    assert manifest["m4_reconciliation_ref"] == "metadata/minerva/analytics_builder_source_path_reconciliation.v0_1.json"
    assert manifest["required_safety_contract_ref"] == "metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json"
    assert manifest["required_retrieval_domain_ref"] == "metadata/minerva/analytics_builder_retrieval_domain.v0_1.json"


def test_analytics_builder_dataset_count_reconciliation_explains_mismatch():
    reconciliation = _load_manifest()["dataset_count_reconciliation"]

    assert reconciliation["expected_count_from_m1"] == 9
    assert reconciliation["catalogue_count"] == 5
    assert reconciliation["governed_dataset_card_count"] == 5
    assert reconciliation["candidate_gap_dataset_count"] == 4
    assert reconciliation["dataset_packet_count"] == 9
    assert len(reconciliation["ids_without_individual_card_files"]) == 4
    assert "5 governed datasets plus 4 blocked/gap datasets" in reconciliation["explanation_of_discrepancy"]


def test_analytics_builder_visual_recipe_count_reconciliation_explains_mismatch():
    reconciliation = _load_manifest()["visual_recipe_count_reconciliation"]

    assert reconciliation["expected_count_from_m1"] == 13
    assert reconciliation["visual_recipe_library_count"] == 9
    assert reconciliation["governed_recipe_card_count"] == 9
    assert reconciliation["blocked_recipe_count"] == 4
    assert reconciliation["recipe_packet_count"] == 13
    assert len(reconciliation["ids_without_individual_recipe_files"]) == 4
    assert "9 governed recipes plus 4 blocked recipes" in reconciliation["explanation_of_discrepancy"]


def test_analytics_builder_generated_html_is_reference_only_not_source_truth():
    manifest = _load_manifest()
    generated_units = [
        unit
        for unit in manifest["canonical_import_units"]
        if unit["source_type"] == "generated_html_reference"
    ]

    assert generated_units
    assert all(unit["import_method"] == "do_not_copy_reference_only" for unit in generated_units)
    assert "docs/generated/analytics_builder_guide/**/*.html" in json.dumps(manifest["source_artifacts_not_to_copy"])
    assert "Generated HTML is presentation output only" in json.dumps(manifest["source_artifacts_not_to_copy"])


def test_analytics_builder_all_canonical_import_units_have_import_methods():
    manifest = _load_manifest()
    allowed = {
        "reference_only",
        "compact_extract",
        "metadata_copy",
        "do_not_copy_reference_only",
        "unresolved",
    }

    assert manifest["canonical_import_units"]
    for unit in manifest["canonical_import_units"]:
        assert unit["unit_id"]
        assert unit["source_path"]
        assert unit["source_type"] in {
            "json_metadata",
            "markdown_doc",
            "generated_html_reference",
            "test_reference",
            "diagnostic_reference",
        }
        assert unit["import_method"] in allowed
        assert unit["purpose_for_minerva"]
        assert unit["safety_requirements"]
        assert unit["required_before_answer_baselines"]
        assert unit["required_before_production_answer_use"]


def test_analytics_builder_answer_baseline_readiness_is_explicit_and_restricted():
    readiness = _load_manifest()["answer_baseline_readiness"]

    assert readiness["m6_can_proceed"] is True
    assert readiness["readiness_level"] == "restricted_baseline_stubs_only"
    assert readiness["production_passed_baselines_allowed"] is False
    assert "planned/pending baseline stubs only" in readiness["reason"]


def test_analytics_builder_production_answer_use_remains_blocked():
    manifest = _load_manifest()

    assert manifest["production_answer_use_status"] == "not_allowed_pending_governed_source_import_and_answer_evaluation"
    assert manifest["no_source_repo_modification"] is True
    assert manifest["no_runtime_behavior"] is True
    assert manifest["no_trust_posture_change"] is True


def test_analytics_builder_final_paid_certification_and_trust_posture_unchanged():
    manifest_text = json.dumps(_load_manifest(), sort_keys=True)
    diagnostic = json.loads(DIAGNOSTIC_PATH.read_text(encoding="utf-8"))

    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in manifest_text
    assert "PayrollLedger does not prove bank-paid truth" in manifest_text
    assert "Visual rendering is not certification proof" in manifest_text
    assert diagnostic["production_answer_use_allowed"] is False
    assert diagnostic["final_paid_truth_changed"] is False
    assert diagnostic["certification_posture_changed"] is False
    assert diagnostic["trust_posture_changed"] is False
    assert diagnostic["certified_assets_count"] == 0

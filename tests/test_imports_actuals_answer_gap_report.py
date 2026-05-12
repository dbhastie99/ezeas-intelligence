import json
import sys

from app.services.imports_actuals_answer_gap_report_service import build_imports_actuals_answer_gap_report
from scripts import build_imports_actuals_answer_gap_report as build_imports_actuals_answer_gap_report_script


CORE_GROUPS = [
    "purpose_and_operator_meaning",
    "imported_timesheet_source_truth",
    "imported_payroll_actuals_lane",
    "source_system_mapping_and_validation",
    "pay_code_and_rate_type_mapping",
    "position_classification_mapping",
    "objecttime_and_source_truth_connection",
    "comparison_and_remediation_connection",
    "reconciliation_and_movement_review_connection",
    "worker_story_and_admin_queue_connection",
    "evidence_provenance_and_audit",
]
SUPPORTING_GROUPS = [
    "outstanding_hardening",
]


def _coverage_group(group_key: str, status: str) -> dict:
    matched = 2 if status == "STRONG" else 1 if status == "WEAK" else 0
    return {
        "group_key": group_key,
        "group_label": group_key.replace("_", " ").title(),
        "search_terms_used": ["Imports / Actuals", group_key],
        "matched_chunk_count": matched,
        "matched_document_count": matched,
        "matched_sources": [],
        "representative_matched_terms": ["Imports / Actuals"] if matched else [],
        "coverage_status": status,
        "diagnostic_notes": [f"{status} fixture for {group_key}."],
    }


def _coverage_report(statuses: dict[str, str]) -> dict:
    groups = [
        _coverage_group(group_key, statuses.get(group_key, "STRONG"))
        for group_key in CORE_GROUPS + SUPPORTING_GROUPS
    ]
    coverage_counts = {"STRONG": 0, "WEAK": 0, "MISSING": 0}
    for group in groups:
        coverage_counts[group["coverage_status"]] += 1
    return {
        "plan_id": "IMPORTS_ACTUALS",
        "domain": "Imports / Actuals",
        "total_evidence_groups": len(groups),
        "coverage_counts": coverage_counts,
        "corpus_document_count": 3,
        "corpus_chunk_count": 12,
        "mutation_performed": False,
        "live_llm_call_performed": False,
        "operational_json_ingestion_performed": False,
        "groups": groups,
    }


def test_imports_actuals_gap_report_good_when_groups_are_strong():
    report = build_imports_actuals_answer_gap_report(_coverage_report({})).to_dict()

    assert report["report_type"] == "IMPORTS_ACTUALS_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert all(finding["recommended_action"] == "KEEP" for finding in report["group_findings"])


def test_imports_actuals_gap_report_needs_refinement_when_weak_groups_exist():
    coverage = _coverage_report(
        {
            "pay_code_and_rate_type_mapping": "WEAK",
            "outstanding_hardening": "WEAK",
        }
    )

    report = build_imports_actuals_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert findings["pay_code_and_rate_type_mapping"]["answer_impact"] == "MEDIUM"
    assert findings["pay_code_and_rate_type_mapping"]["recommended_action"] == "IMPROVE_SYNTHESIS"
    assert findings["outstanding_hardening"]["recommended_action"] == "IMPROVE_RETRIEVAL_TERMS"


def test_imports_actuals_gap_report_insufficient_corpus_when_core_groups_are_missing():
    coverage = _coverage_report(
        {
            "imported_payroll_actuals_lane": "MISSING",
            "evidence_provenance_and_audit": "MISSING",
        }
    )

    report = build_imports_actuals_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "INSUFFICIENT_CORPUS"
    assert findings["imported_payroll_actuals_lane"]["answer_impact"] == "HIGH"
    assert findings["imported_payroll_actuals_lane"]["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"
    assert "Treat Imports / Actuals answers as corpus-limited" in " ".join(report["recommended_next_actions"])


def test_imports_actuals_gap_report_group_action_mapping_for_supporting_missing_group():
    coverage = _coverage_report({"outstanding_hardening": "MISSING"})

    report = build_imports_actuals_answer_gap_report(coverage).to_dict()
    finding = next(item for item in report["group_findings"] if item["group_key"] == "outstanding_hardening")

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert finding["answer_impact"] == "MEDIUM"
    assert finding["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"


def test_imports_actuals_gap_report_json_output_shape(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_imports_actuals_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--json",
        ],
    )

    exit_code = build_imports_actuals_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_type"] == "IMPORTS_ACTUALS_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["group_findings"]
    assert report["recommended_next_actions"]


def test_imports_actuals_gap_report_writes_output_file(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    output_path = tmp_path / "gap-report.json"
    coverage_path.write_text(json.dumps(_coverage_report({"pay_code_and_rate_type_mapping": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_imports_actuals_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--output",
            str(output_path),
        ],
    )

    exit_code = build_imports_actuals_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Imports / Actuals answer gap report" in captured.out
    assert report["overall_status"] == "NEEDS_REFINEMENT"


def test_imports_actuals_gap_report_human_output_is_diagnostic_only(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({"pay_code_and_rate_type_mapping": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_imports_actuals_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_imports_actuals_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_imports_actuals_gap_report_invalid_coverage_report_fails_clearly(
    tmp_path,
    monkeypatch,
    capsys,
):
    coverage_path = tmp_path / "invalid.json"
    coverage_path.write_text(json.dumps({"plan_id": "OTHER", "groups": []}), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_imports_actuals_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_imports_actuals_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Imports / Actuals answer gap report failed" in captured.out
    assert "plan_id IMPORTS_ACTUALS" in captured.out

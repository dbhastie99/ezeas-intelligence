import json
import sys
from pathlib import Path

from app.services.annual_leave_answer_gap_report_service import build_annual_leave_answer_gap_report
from scripts import build_annual_leave_answer_gap_report as build_annual_leave_gap_script


CORE_GROUPS = [
    "configuration",
    "accrual",
    "taken",
    "valuation",
    "payrun",
    "worker_story",
    "outstanding",
]
VALID_ACTIONS = {
    "KEEP",
    "IMPROVE_RETRIEVAL_TERMS",
    "IMPROVE_SYNTHESIS",
    "ADD_FORMAL_SOURCE_EVIDENCE_LATER",
}


def _coverage_group(group_key: str, status: str) -> dict:
    matched = 2 if status == "STRONG" else 1 if status == "WEAK" else 0
    return {
        "group_key": group_key,
        "group_label": group_key.replace("_", " ").title(),
        "search_terms_used": ["Annual Leave / Leave Management", group_key],
        "matched_chunk_count": matched,
        "matched_document_count": matched,
        "matched_sources": [],
        "representative_matched_terms": ["Annual Leave"] if matched else [],
        "coverage_status": status,
        "diagnostic_notes": [f"{status} fixture for {group_key}."],
    }


def _coverage_report(statuses: dict[str, str]) -> dict:
    groups = [_coverage_group(group_key, statuses.get(group_key, "STRONG")) for group_key in CORE_GROUPS]
    coverage_counts = {"STRONG": 0, "WEAK": 0, "MISSING": 0}
    for group in groups:
        coverage_counts[group["coverage_status"]] += 1
    return {
        "plan_id": "ANNUAL_LEAVE_MANAGEMENT",
        "domain": "Annual Leave / Leave Management",
        "total_evidence_groups": len(groups),
        "coverage_counts": coverage_counts,
        "corpus_document_count": 3,
        "corpus_chunk_count": 10,
        "mutation_performed": False,
        "live_llm_call_performed": False,
        "operational_json_ingestion_performed": False,
        "groups": groups,
    }


def test_annual_leave_gap_report_shape_and_diagnostic_flags():
    report = build_annual_leave_answer_gap_report(_coverage_report({})).to_dict()

    assert report["report_type"] == "ANNUAL_LEAVE_MANAGEMENT_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["source_coverage_plan_id"] == "ANNUAL_LEAVE_MANAGEMENT"
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert all(finding["recommended_action"] == "KEEP" for finding in report["group_findings"])
    assert {finding["recommended_action"] for finding in report["group_findings"]} <= VALID_ACTIONS


def test_annual_leave_gap_report_maps_weak_core_group_to_synthesis():
    report = build_annual_leave_answer_gap_report(_coverage_report({"valuation": "WEAK"})).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert findings["valuation"]["answer_impact"] == "MEDIUM"
    assert findings["valuation"]["recommended_action"] == "IMPROVE_SYNTHESIS"
    assert "Tighten Annual Leave / Leave Management answer synthesis" in " ".join(report["recommended_next_actions"])


def test_annual_leave_gap_report_insufficient_corpus_when_core_groups_are_missing():
    report = build_annual_leave_answer_gap_report(
        _coverage_report({"configuration": "MISSING", "valuation": "MISSING"})
    ).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "INSUFFICIENT_CORPUS"
    assert findings["configuration"]["answer_impact"] == "HIGH"
    assert findings["configuration"]["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"
    assert "Treat Annual Leave / Leave Management answers as corpus-limited" in " ".join(
        report["recommended_next_actions"]
    )


def test_annual_leave_gap_report_json_output_shape(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_annual_leave_answer_gap_report.py", "--coverage-report", str(coverage_path), "--json"],
    )

    exit_code = build_annual_leave_gap_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_type"] == "ANNUAL_LEAVE_MANAGEMENT_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["group_findings"]
    assert report["recommended_next_actions"]
    assert report["live_llm_call_performed"] is False


def test_annual_leave_gap_report_writes_output_file(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    output_path = tmp_path / "gap-report.json"
    coverage_path.write_text(json.dumps(_coverage_report({"payrun": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_annual_leave_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--output",
            str(output_path),
        ],
    )

    exit_code = build_annual_leave_gap_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Annual Leave / Leave Management answer gap report" in captured.out
    assert report["overall_status"] == "NEEDS_REFINEMENT"


def test_annual_leave_gap_report_human_output_is_diagnostic_only(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({"accrual": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_annual_leave_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_annual_leave_gap_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Annual Leave / Leave Management answer gap report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out


def test_annual_leave_gap_report_invalid_coverage_report_fails_clearly(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "invalid.json"
    coverage_path.write_text(json.dumps({"plan_id": "OTHER", "groups": []}), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_annual_leave_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_annual_leave_gap_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Annual Leave / Leave Management answer gap report failed" in captured.out
    assert "plan_id ANNUAL_LEAVE_MANAGEMENT" in captured.out


def test_annual_leave_gap_report_missing_coverage_report_path_fails_clearly(tmp_path, monkeypatch, capsys):
    missing_path = tmp_path / "missing.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_annual_leave_answer_gap_report.py", "--coverage-report", str(missing_path)],
    )

    exit_code = build_annual_leave_gap_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Coverage report does not exist" in captured.out


def test_annual_leave_gap_report_does_not_require_committed_generated_json_or_baseline_pack():
    assert not Path("docs/evaluation/worker_story_baselines/annual_leave/v0_1").exists()
    assert not Path("artifacts/eval/annual_leave_answer_gap_report.json").exists()

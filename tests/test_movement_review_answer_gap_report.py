import json
import sys

from app.services.movement_review_answer_gap_report_service import build_movement_review_answer_gap_report
from scripts import build_movement_review_answer_gap_report as build_movement_review_answer_gap_report_script


CORE_GROUPS = [
    "purpose_and_operator_meaning",
    "reasonableness_not_error",
    "variance_and_comparable_periods",
    "current_effective_truth",
    "trend_only_and_threshold_treatment",
]
SUPPORTING_GROUPS = [
    "worker_and_organisation_lenses",
    "payroll_bases_connection",
    "worker_story_connection",
    "admin_queue_connection",
    "filters_and_return_context",
    "outstanding_hardening",
]


def _coverage_group(group_key: str, status: str) -> dict:
    matched = 2 if status == "STRONG" else 1 if status == "WEAK" else 0
    return {
        "group_key": group_key,
        "group_label": group_key.replace("_", " ").title(),
        "search_terms_used": ["Movement Review", group_key],
        "matched_chunk_count": matched,
        "matched_document_count": matched,
        "matched_sources": [],
        "representative_matched_terms": ["Movement Review"] if matched else [],
        "coverage_status": status,
        "diagnostic_notes": [f"{status} fixture for {group_key}."],
    }


def _coverage_report(statuses: dict[str, str]) -> dict:
    groups = [_coverage_group(group_key, statuses.get(group_key, "STRONG")) for group_key in CORE_GROUPS + SUPPORTING_GROUPS]
    coverage_counts = {"STRONG": 0, "WEAK": 0, "MISSING": 0}
    for group in groups:
        coverage_counts[group["coverage_status"]] += 1
    return {
        "plan_id": "MOVEMENT_REVIEW",
        "domain": "Movement Review",
        "total_evidence_groups": len(groups),
        "coverage_counts": coverage_counts,
        "corpus_document_count": 3,
        "corpus_chunk_count": 11,
        "mutation_performed": False,
        "live_llm_call_performed": False,
        "operational_json_ingestion_performed": False,
        "groups": groups,
    }


def test_movement_review_gap_report_good_when_groups_are_strong():
    report = build_movement_review_answer_gap_report(_coverage_report({})).to_dict()

    assert report["report_type"] == "MOVEMENT_REVIEW_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert all(finding["recommended_action"] == "KEEP" for finding in report["group_findings"])


def test_movement_review_gap_report_needs_refinement_when_weak_groups_exist():
    coverage = _coverage_report({"variance_and_comparable_periods": "WEAK", "worker_story_connection": "WEAK"})

    report = build_movement_review_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert findings["variance_and_comparable_periods"]["answer_impact"] == "MEDIUM"
    assert findings["variance_and_comparable_periods"]["recommended_action"] == "IMPROVE_SYNTHESIS"
    assert findings["worker_story_connection"]["recommended_action"] == "IMPROVE_RETRIEVAL_TERMS"


def test_movement_review_gap_report_insufficient_corpus_when_core_groups_are_missing():
    coverage = _coverage_report(
        {
            "reasonableness_not_error": "MISSING",
            "current_effective_truth": "MISSING",
        }
    )

    report = build_movement_review_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "INSUFFICIENT_CORPUS"
    assert findings["current_effective_truth"]["answer_impact"] == "HIGH"
    assert findings["current_effective_truth"]["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"
    assert "Treat Movement Review answers as corpus-limited" in " ".join(report["recommended_next_actions"])


def test_movement_review_gap_report_group_action_mapping_for_supporting_missing_group():
    coverage = _coverage_report({"admin_queue_connection": "MISSING"})

    report = build_movement_review_answer_gap_report(coverage).to_dict()
    finding = next(item for item in report["group_findings"] if item["group_key"] == "admin_queue_connection")

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert finding["answer_impact"] == "MEDIUM"
    assert finding["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"


def test_movement_review_gap_report_json_output_shape(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_movement_review_answer_gap_report.py", "--coverage-report", str(coverage_path), "--json"],
    )

    exit_code = build_movement_review_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_type"] == "MOVEMENT_REVIEW_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["group_findings"]
    assert report["recommended_next_actions"]


def test_movement_review_gap_report_writes_output_file(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    output_path = tmp_path / "gap-report.json"
    coverage_path.write_text(json.dumps(_coverage_report({"variance_and_comparable_periods": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_movement_review_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--output",
            str(output_path),
        ],
    )

    exit_code = build_movement_review_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Movement Review answer gap report" in captured.out
    assert report["overall_status"] == "NEEDS_REFINEMENT"


def test_movement_review_gap_report_human_output_is_diagnostic_only(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({"variance_and_comparable_periods": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_movement_review_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_movement_review_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_movement_review_gap_report_invalid_coverage_report_fails_clearly(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "invalid.json"
    coverage_path.write_text(json.dumps({"plan_id": "OTHER", "groups": []}), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_movement_review_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_movement_review_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Movement Review answer gap report failed" in captured.out
    assert "plan_id MOVEMENT_REVIEW" in captured.out

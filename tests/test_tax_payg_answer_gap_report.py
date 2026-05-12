import json
import sys

from app.services.tax_payg_answer_gap_report_service import build_tax_payg_answer_gap_report
from scripts import build_tax_payg_answer_gap_report as build_tax_payg_answer_gap_report_script


CORE_GROUPS = [
    "purpose_and_operator_meaning",
    "deterministic_tax_boundary",
    "tax_story_and_explainability",
    "taxable_basis_and_payroll_bases",
    "worker_tax_declaration_and_withholding_inputs",
    "payment_date_and_process_period_context",
    "pay_frequency_and_provider_support",
    "gross_to_net_and_finalised_totals",
    "supplementary_incremental_payg",
    "unsupported_and_review_states",
]
SUPPORTING_GROUPS = [
    "worker_story_and_admin_queue_connection",
    "outstanding_hardening",
]


def _coverage_group(group_key: str, status: str) -> dict:
    matched = 2 if status == "STRONG" else 1 if status == "WEAK" else 0
    return {
        "group_key": group_key,
        "group_label": group_key.replace("_", " ").title(),
        "search_terms_used": ["Tax / PAYG", group_key],
        "matched_chunk_count": matched,
        "matched_document_count": matched,
        "matched_sources": [],
        "representative_matched_terms": ["Tax / PAYG"] if matched else [],
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
        "plan_id": "TAX_PAYG",
        "domain": "Tax / PAYG",
        "total_evidence_groups": len(groups),
        "coverage_counts": coverage_counts,
        "corpus_document_count": 3,
        "corpus_chunk_count": 12,
        "mutation_performed": False,
        "live_llm_call_performed": False,
        "operational_json_ingestion_performed": False,
        "groups": groups,
    }


def test_tax_payg_gap_report_good_when_groups_are_strong():
    report = build_tax_payg_answer_gap_report(_coverage_report({})).to_dict()

    assert report["report_type"] == "TAX_PAYG_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert all(finding["recommended_action"] == "KEEP" for finding in report["group_findings"])


def test_tax_payg_gap_report_needs_refinement_when_weak_groups_exist():
    coverage = _coverage_report({"tax_story_and_explainability": "WEAK", "worker_story_and_admin_queue_connection": "WEAK"})

    report = build_tax_payg_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert findings["tax_story_and_explainability"]["answer_impact"] == "MEDIUM"
    assert findings["tax_story_and_explainability"]["recommended_action"] == "IMPROVE_SYNTHESIS"
    assert findings["worker_story_and_admin_queue_connection"]["recommended_action"] == "IMPROVE_RETRIEVAL_TERMS"


def test_tax_payg_gap_report_insufficient_corpus_when_core_groups_are_missing():
    coverage = _coverage_report(
        {
            "deterministic_tax_boundary": "MISSING",
            "supplementary_incremental_payg": "MISSING",
        }
    )

    report = build_tax_payg_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "INSUFFICIENT_CORPUS"
    assert findings["supplementary_incremental_payg"]["answer_impact"] == "HIGH"
    assert findings["supplementary_incremental_payg"]["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"
    assert "Treat Tax / PAYG answers as corpus-limited" in " ".join(report["recommended_next_actions"])


def test_tax_payg_gap_report_group_action_mapping_for_supporting_missing_group():
    coverage = _coverage_report({"worker_story_and_admin_queue_connection": "MISSING"})

    report = build_tax_payg_answer_gap_report(coverage).to_dict()
    finding = next(item for item in report["group_findings"] if item["group_key"] == "worker_story_and_admin_queue_connection")

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert finding["answer_impact"] == "MEDIUM"
    assert finding["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"


def test_tax_payg_gap_report_json_output_shape(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_tax_payg_answer_gap_report.py", "--coverage-report", str(coverage_path), "--json"],
    )

    exit_code = build_tax_payg_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_type"] == "TAX_PAYG_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["group_findings"]
    assert report["recommended_next_actions"]


def test_tax_payg_gap_report_writes_output_file(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    output_path = tmp_path / "gap-report.json"
    coverage_path.write_text(json.dumps(_coverage_report({"tax_story_and_explainability": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_tax_payg_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--output",
            str(output_path),
        ],
    )

    exit_code = build_tax_payg_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Tax / PAYG answer gap report" in captured.out
    assert report["overall_status"] == "NEEDS_REFINEMENT"


def test_tax_payg_gap_report_human_output_is_diagnostic_only(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({"tax_story_and_explainability": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_tax_payg_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_tax_payg_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_tax_payg_gap_report_invalid_coverage_report_fails_clearly(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "invalid.json"
    coverage_path.write_text(json.dumps({"plan_id": "OTHER", "groups": []}), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_tax_payg_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_tax_payg_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Tax / PAYG answer gap report failed" in captured.out
    assert "plan_id TAX_PAYG" in captured.out

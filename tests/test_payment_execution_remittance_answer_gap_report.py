import json
import sys

from app.services.payment_execution_remittance_answer_gap_report_service import (
    build_payment_execution_remittance_answer_gap_report,
)
from scripts import build_payment_execution_remittance_answer_gap_report as build_payment_execution_remittance_answer_gap_report_script


CORE_GROUPS = [
    "purpose_and_operator_meaning",
    "finalised_gross_to_net_source",
    "worker_net_pay_and_bank_allocation",
    "payment_destination_readiness",
    "negative_net_pay_and_obligation_interaction",
    "deduction_and_third_party_remittance",
    "payment_file_generation_and_period_close",
    "remittance_batching_and_reconciliation",
    "worker_attention_and_admin_queue_connection",
    "worker_story_and_audit_evidence",
]
SUPPORTING_GROUPS = [
    "outstanding_hardening",
]


def _coverage_group(group_key: str, status: str) -> dict:
    matched = 2 if status == "STRONG" else 1 if status == "WEAK" else 0
    return {
        "group_key": group_key,
        "group_label": group_key.replace("_", " ").title(),
        "search_terms_used": ["Payment Execution / Remittance", group_key],
        "matched_chunk_count": matched,
        "matched_document_count": matched,
        "matched_sources": [],
        "representative_matched_terms": ["Payment Execution / Remittance"] if matched else [],
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
        "plan_id": "PAYMENT_EXECUTION_REMITTANCE",
        "domain": "Payment Execution / Remittance",
        "total_evidence_groups": len(groups),
        "coverage_counts": coverage_counts,
        "corpus_document_count": 3,
        "corpus_chunk_count": 11,
        "mutation_performed": False,
        "live_llm_call_performed": False,
        "operational_json_ingestion_performed": False,
        "groups": groups,
    }


def test_payment_execution_remittance_gap_report_good_when_groups_are_strong():
    report = build_payment_execution_remittance_answer_gap_report(_coverage_report({})).to_dict()

    assert report["report_type"] == "PAYMENT_EXECUTION_REMITTANCE_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert all(finding["recommended_action"] == "KEEP" for finding in report["group_findings"])


def test_payment_execution_remittance_gap_report_needs_refinement_when_weak_groups_exist():
    coverage = _coverage_report(
        {
            "payment_destination_readiness": "WEAK",
            "outstanding_hardening": "WEAK",
        }
    )

    report = build_payment_execution_remittance_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert findings["payment_destination_readiness"]["answer_impact"] == "MEDIUM"
    assert findings["payment_destination_readiness"]["recommended_action"] == "IMPROVE_SYNTHESIS"
    assert findings["outstanding_hardening"]["recommended_action"] == "IMPROVE_RETRIEVAL_TERMS"


def test_payment_execution_remittance_gap_report_insufficient_corpus_when_core_groups_are_missing():
    coverage = _coverage_report(
        {
            "finalised_gross_to_net_source": "MISSING",
            "payment_file_generation_and_period_close": "MISSING",
        }
    )

    report = build_payment_execution_remittance_answer_gap_report(coverage).to_dict()
    findings = {finding["group_key"]: finding for finding in report["group_findings"]}

    assert report["overall_status"] == "INSUFFICIENT_CORPUS"
    assert findings["finalised_gross_to_net_source"]["answer_impact"] == "HIGH"
    assert findings["finalised_gross_to_net_source"]["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"
    assert "Treat Payment Execution / Remittance answers as corpus-limited" in " ".join(report["recommended_next_actions"])


def test_payment_execution_remittance_gap_report_group_action_mapping_for_supporting_missing_group():
    coverage = _coverage_report({"outstanding_hardening": "MISSING"})

    report = build_payment_execution_remittance_answer_gap_report(coverage).to_dict()
    finding = next(item for item in report["group_findings"] if item["group_key"] == "outstanding_hardening")

    assert report["overall_status"] == "NEEDS_REFINEMENT"
    assert finding["answer_impact"] == "MEDIUM"
    assert finding["recommended_action"] == "ADD_FORMAL_SOURCE_EVIDENCE_LATER"


def test_payment_execution_remittance_gap_report_json_output_shape(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_payment_execution_remittance_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--json",
        ],
    )

    exit_code = build_payment_execution_remittance_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["report_type"] == "PAYMENT_EXECUTION_REMITTANCE_ANSWER_GAP_REPORT"
    assert report["overall_status"] == "GOOD"
    assert report["group_findings"]
    assert report["recommended_next_actions"]


def test_payment_execution_remittance_gap_report_writes_output_file(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    output_path = tmp_path / "gap-report.json"
    coverage_path.write_text(json.dumps(_coverage_report({"payment_destination_readiness": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_payment_execution_remittance_answer_gap_report.py",
            "--coverage-report",
            str(coverage_path),
            "--output",
            str(output_path),
        ],
    )

    exit_code = build_payment_execution_remittance_answer_gap_report_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Payment Execution / Remittance answer gap report" in captured.out
    assert report["overall_status"] == "NEEDS_REFINEMENT"


def test_payment_execution_remittance_gap_report_human_output_is_diagnostic_only(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(_coverage_report({"payment_destination_readiness": "WEAK"})), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_payment_execution_remittance_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_payment_execution_remittance_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_payment_execution_remittance_gap_report_invalid_coverage_report_fails_clearly(tmp_path, monkeypatch, capsys):
    coverage_path = tmp_path / "invalid.json"
    coverage_path.write_text(json.dumps({"plan_id": "OTHER", "groups": []}), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["build_payment_execution_remittance_answer_gap_report.py", "--coverage-report", str(coverage_path)],
    )

    exit_code = build_payment_execution_remittance_answer_gap_report_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Payment Execution / Remittance answer gap report failed" in captured.out
    assert "plan_id PAYMENT_EXECUTION_REMITTANCE" in captured.out

from pathlib import Path


LEDGER_PATH = Path("docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md")


def _ledger() -> str:
    return LEDGER_PATH.read_text(encoding="utf-8")


def test_completed_domain_baseline_decision_ledger_exists_and_is_linked_from_readme():
    assert LEDGER_PATH.exists()

    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md" in readme


def test_completed_domain_baseline_decision_ledger_contains_status_enum_values_and_core_columns():
    ledger = _ledger()

    for status in (
        "BASELINE_REQUIRED",
        "BASELINE_ALREADY_EXISTS",
        "NO_BASELINE_NEEDED",
        "RUNBOOK_OUTSTANDING",
        "NEEDS_REVIEW",
    ):
        assert status in ledger

    for column in (
        "DomainName",
        "LatestKnownVersion",
        "HasRetrievalPlan",
        "HasBroadBenchmark",
        "HasFocusedCoverage",
        "HasCoverageDiagnostic",
        "HasAnswerGapReport",
        "HasEvaluationRunbook",
        "HasCheckedInBaselineArtefact",
        "EvidencePaths",
        "DecisionStatus",
        "DecisionReason",
        "RecommendedFollowUpSlice",
    ):
        assert column in ledger


def test_completed_domain_baseline_decision_ledger_contains_guardrails():
    ledger = _ledger()

    assert "does not mutate corpus" in ledger
    assert "does not change routing" in ledger
    assert "does not change answer generation" in ledger
    assert "does not call live LLM" in ledger
    assert "does not ingest operational JSON" in ledger
    assert "does not connect Code Evidence" in ledger
    assert "does not prove runtime platform truth" in ledger
    assert "does not create v0.5 slices automatically" in ledger


def test_completed_domain_baseline_decision_ledger_includes_required_domains_and_completed_v04_domains():
    ledger = _ledger()

    for domain in (
        "Annual Leave / Leave Management",
        "Worker Story",
        "Payroll Bases & Totals",
        "PayRun Admin Queue",
        "Movement Review",
        "Comparison / Remediation",
        "Tax / PAYG",
        "Deductions / Obligations",
        "Retro / Replay",
        "Payment Execution / Remittance",
        "Leave Accrual / Processing",
        "Finalisation Readiness",
        "Leave Source Model",
        "On-costs / Employer Liabilities",
        "Award Build / Award Evidence",
        "Imports / Actuals",
        "ObjectTime / Source Truth",
        "Contacts / Employee Appointments",
        "Process Periods / PayRun Lifecycle",
        "Costing / GL Consequence Evidence",
        "Worker Attention / Issue Resolution",
        "Gross-to-Net",
        "RateSource / Rate Story",
        "Decision Story",
        "Payroll Output",
        "Contact Payroll History",
        "Leave Requests / Leave Workflow",
        "Public Holidays",
        "Rosters / Patterns / Scheduling",
        "Award Positions / Classifications",
        "Payroll Tax / WorkCover / WIC Liability Detail",
    ):
        assert domain in ledger

    assert "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md" in ledger
    assert "PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md" in ledger
    assert "ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md" in ledger
    assert "AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md" in ledger


def test_completed_domain_baseline_decision_ledger_summary_and_counts_are_documented():
    ledger = _ledger()

    assert "## Summary" in ledger
    assert "Total domains inventoried: 31" in ledger
    assert "`BASELINE_REQUIRED`: 22" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 9" in ledger
    assert "`NO_BASELINE_NEEDED`: 0" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger
    assert "`NEEDS_REVIEW`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management; Finalisation Readiness; Payroll Output; RateSource / Rate Story" in ledger
    assert "Recommended next slice: keep Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Gross-to-Net, Annual Leave / Leave Management, Finalisation Readiness, Payroll Output and RateSource / Rate Story as captured comparison controls" in ledger
    assert "keep Decision Story as a blocked `BASELINE_REQUIRED` domain until DB readiness returns `READY` for its own capture" in ledger
    assert "Domains with runbook outstanding: none" in ledger


def test_annual_leave_is_baseline_already_exists_with_baseline_pack():
    ledger = _ledger()

    assert "## Annual Leave / Leave Management Baseline Captured Finding" in ledger
    assert "Annual Leave / Leave Management is now `BASELINE_ALREADY_EXISTS`" in ledger
    assert "Annual Leave-specific v0.4 evaluation runbook foundation" in ledger
    assert "corpus coverage diagnostic service/script" in ledger
    assert "answer gap report service/script" in ledger
    assert "Adjacent leave-domain v0.4 diagnostics are not substitutes" in ledger
    assert "checked-in Annual Leave baseline pack" in ledger
    assert "benchmark 1 total, 1 passed, 0 failed" in ledger
    assert "corpus coverage 7 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 7 KEEP actions" in ledger

    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | yes | yes | yes | yes |" in ledger
    assert "samples/eval/golden_questions.annual_leave.json" in ledger
    assert "app/services/annual_leave_corpus_coverage_service.py" in ledger
    assert "app/services/annual_leave_answer_gap_report_service.py" in ledger
    assert "scripts/scan_annual_leave_corpus_coverage.py" in ledger
    assert "scripts/build_annual_leave_answer_gap_report.py" in ledger
    assert "scripts/scan_leave_corpus_candidates.py" in ledger
    assert "scripts/build_leave_manifest_from_candidates.py" in ledger
    assert "ANNUAL_LEAVE_CORPUS_CHECKLIST.md" in ledger
    assert "docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md" in ledger
    assert "docs/evaluation/worker_story_baselines/annual_leave/v0_1/BASELINE_SUMMARY.md" in ledger


def test_annual_leave_diagnostics_are_present_with_baseline_pack():
    assert Path("docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md").exists()
    assert Path("app/services/annual_leave_corpus_coverage_service.py").exists()
    assert Path("app/services/annual_leave_answer_gap_report_service.py").exists()
    assert Path("scripts/scan_annual_leave_corpus_coverage.py").exists()
    assert Path("scripts/build_annual_leave_answer_gap_report.py").exists()
    assert Path("docs/evaluation/worker_story_baselines/annual_leave/v0_1").exists()

    assert Path("docs/LEAVE_ACCRUAL_PROCESSING_EVALUATION_RUNBOOK.md").exists()
    assert Path("docs/LEAVE_SOURCE_MODEL_EVALUATION_RUNBOOK.md").exists()
    assert Path("docs/LEAVE_REQUESTS_WORKFLOW_EVALUATION_RUNBOOK.md").exists()


def test_completed_domain_baseline_decision_ledger_records_captured_baselines():
    ledger = _ledger()

    assert "This summary is not authorization to run benchmarks" in ledger
    assert "For every other completed v0.4 domain, this ledger does not claim baseline capture has already happened" in ledger
    assert "Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 8 total, 8 passed, 0 failed" in ledger
    assert "Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "gross-to-net-current-effective-worker-story" in ledger
    assert "Failure is benchmark answer-term expectation drift, not corpus gap" in ledger
    assert "| Worker Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/worker_story/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Worker Story now has a checked-in baseline artefact pack" in ledger
    assert "| Payroll Bases & Totals | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/payroll_bases_totals/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Payroll Bases & Totals now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| PayRun Admin Queue | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/payrun_admin_queue/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | PayRun Admin Queue now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 8 total, 6 passed, 2 failed" in ledger
    assert "Failures are benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in ledger
    assert "| Movement Review | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/movement_review/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Gross-to-Net | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/gross_to_net/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "docs/evaluation/worker_story_baselines/annual_leave/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Annual Leave / Leave Management now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Finalisation Readiness | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/finalisation_readiness/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Finalisation Readiness now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 12 total, 12 passed, 0 failed" in ledger
    assert "corpus coverage 11 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 11 KEEP actions and 1 IMPROVE_SYNTHESIS action for `purpose_and_operator_meaning`" in ledger
    assert "| Payroll Output | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/payroll_output/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Payroll Output now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 7 total, 6 passed, 1 failed" in ledger
    assert "payroll-output-rich-answer" in ledger
    assert "corpus coverage 10 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `worker_level_output`" in ledger
    assert "Failure is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in ledger
    assert "| RateSource / Rate Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/ratesource_rate_story/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | RateSource / Rate Story now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "rate-source-rate-story-rich-answer" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `rate_source_evidence_index`" in ledger
    assert "| Payroll Tax / WorkCover / WIC Liability Detail | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger


def test_core_payroll_domains_capture_progress_keeps_decision_story_blocked():
    ledger = _ledger()

    assert "## Finalisation Readiness Baseline Captured Finding" in ledger
    assert "Finalisation Readiness is now `BASELINE_ALREADY_EXISTS`" in ledger
    assert "benchmark 12 total, 12 passed, 0 failed" in ledger
    assert "corpus coverage 11 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status `NEEDS_REFINEMENT` with 11 KEEP actions and 1 IMPROVE_SYNTHESIS action" in ledger
    assert "weak/refinement group is `purpose_and_operator_meaning`" in ledger
    assert "## Payroll Output Baseline Captured Finding" in ledger
    assert "Payroll Output is now `BASELINE_ALREADY_EXISTS`" in ledger
    assert "benchmark 7 total, 6 passed, 1 failed" in ledger
    assert "failed case `payroll-output-rich-answer`" in ledger
    assert "corpus coverage 10 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status `NEEDS_REFINEMENT` with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action" in ledger
    assert "weak/refinement group is `worker_level_output`" in ledger
    assert "Failure is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in ledger
    assert "## RateSource / Rate Story Baseline Captured Finding" in ledger
    assert "RateSource / Rate Story is now `BASELINE_ALREADY_EXISTS`" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "failed case `rate-source-rate-story-rich-answer`" in ledger
    assert "corpus coverage 10 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status `NEEDS_REFINEMENT` with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action" in ledger
    assert "weak/refinement group is `rate_source_evidence_index`" in ledger
    assert "`BASELINE_REQUIRED`: 22" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 9" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger

    assert "## Core Payroll Explanation Blocked Baseline Finding" in ledger
    assert "Decision Story remains `BASELINE_REQUIRED`" in ledger
    assert "Finalisation Readiness, Payroll Output and RateSource / Rate Story are no longer part of this blocked set" in ledger
    assert "| Finalisation Readiness | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| Payroll Output | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| RateSource / Rate Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger

    assert "docs/evaluation/worker_story_baselines/decision_story/v0_1/" in ledger
    assert "| Decision Story | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger

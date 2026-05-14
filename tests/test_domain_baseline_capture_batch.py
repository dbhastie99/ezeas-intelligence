import subprocess
from pathlib import Path


BASELINE_ROOT = Path("docs/evaluation/worker_story_baselines")
LEDGER_PATH = BASELINE_ROOT / "COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md"
CLOSEOUT_PATH = BASELINE_ROOT / "BASELINE_BATCH_CLOSEOUT_2026_05_13.md"
MATURITY_CLOSEOUT_PATH = BASELINE_ROOT / "BASELINE_MATURITY_CLOSEOUT_2026_05_13.md"
WORKER_STORY_PACK = BASELINE_ROOT / "worker_story" / "v0_1"
ANNUAL_LEAVE_PACK = BASELINE_ROOT / "annual_leave" / "v0_1"
CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH = BASELINE_ROOT / "CORE_PAYROLL_EXPLANATION_BASELINE_BATCH_2026_05_13.md"
CORE_PAYROLL_CLOSEOUT_PATH = BASELINE_ROOT / "CORE_PAYROLL_EXPLANATION_BATCH_CLOSEOUT_2026_05_13.md"
PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH = (
    BASELINE_ROOT / "PAYROLL_EVIDENCE_CONTEXT_BASELINE_BATCH_2026_05_13.md"
)
REQUIRED_FILES = (
    "BASELINE_SUMMARY.md",
    "BENCHMARK_BASELINE.md",
    "CORPUS_COVERAGE_BASELINE.md",
    "ANSWER_GAP_REPORT_BASELINE.md",
    "REVIEW_NOTES.md",
)

CAPTURED_BATCH_DOMAINS = {
    "payroll_bases_totals": {
        "name": "Payroll Bases & Totals",
        "runbook": "docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.payroll_bases_and_totals.json",
        "scan": "scripts\\scan_payroll_bases_corpus_coverage.py",
        "gap": "scripts\\build_payroll_bases_answer_gap_report.py",
    },
    "payrun_admin_queue": {
        "name": "PayRun Admin Queue",
        "runbook": "docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.payrun_admin_queue.json",
        "scan": "scripts\\scan_payrun_admin_queue_corpus_coverage.py",
        "gap": "scripts\\build_payrun_admin_queue_answer_gap_report.py",
    },
    "movement_review": {
        "name": "Movement Review",
        "runbook": "docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.movement_review.json",
        "scan": "scripts\\scan_movement_review_corpus_coverage.py",
        "gap": "scripts\\build_movement_review_answer_gap_report.py",
    },
    "gross_to_net": {
        "name": "Gross-to-Net",
        "runbook": "docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.gross_to_net.json",
        "scan": "scripts\\scan_gross_to_net_corpus_coverage.py",
        "gap": "scripts\\build_gross_to_net_answer_gap_report.py",
    },
}

PAYROLL_OUTPUT_CAPTURED_DOMAIN = {
    "name": "Payroll Output",
    "runbook": "docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.payroll_output.json",
    "scan": "scripts\\scan_payroll_output_corpus_coverage.py",
    "gap": "scripts\\build_payroll_output_answer_gap_report.py",
}

RATE_SOURCE_RATE_STORY_CAPTURED_DOMAIN = {
    "name": "RateSource / Rate Story",
    "runbook": "docs/RATE_SOURCE_RATE_STORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.rate_source_rate_story.json",
    "scan": "scripts\\scan_rate_source_rate_story_corpus_coverage.py",
    "gap": "scripts\\build_rate_source_rate_story_answer_gap_report.py",
}

DECISION_STORY_CAPTURED_DOMAIN = {
    "name": "Decision Story",
    "runbook": "docs/DECISION_STORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.decision_story.json",
    "scan": "scripts\\scan_decision_story_corpus_coverage.py",
    "gap": "scripts\\build_decision_story_answer_gap_report.py",
}

FINALISATION_READINESS_CAPTURED_DOMAIN = {
    "name": "Finalisation Readiness",
    "runbook": "docs/FINALISATION_READINESS_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.finalisation_readiness.json",
    "scan": "scripts\\scan_finalisation_readiness_corpus_coverage.py",
    "gap": "scripts\\build_finalisation_readiness_answer_gap_report.py",
}

CONTACT_PAYROLL_HISTORY_CAPTURED_DOMAIN = {
    "name": "Contact Payroll History",
    "runbook": "docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.contact_payroll_history.json",
    "scan": "scripts\\scan_contact_payroll_history_corpus_coverage.py",
    "gap": "scripts\\build_contact_payroll_history_answer_gap_report.py",
}

PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS = {
    "process_periods_payrun_lifecycle": {
        "name": "Process Periods / PayRun Lifecycle",
        "runbook": "docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.process_period_payrun_lifecycle.json",
        "scan": "scripts\\scan_process_period_payrun_lifecycle_corpus_coverage.py",
        "gap": "scripts\\build_process_period_payrun_lifecycle_answer_gap_report.py",
    },
    "imports_actuals": {
        "name": "Imports / Actuals",
        "runbook": "docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.imports_actuals.json",
        "scan": "scripts\\scan_imports_actuals_corpus_coverage.py",
        "gap": "scripts\\build_imports_actuals_answer_gap_report.py",
    },
}

OBJECTTIME_SOURCE_TRUTH_RECAPTURED_DOMAIN = {
    "name": "ObjectTime / Source Truth",
    "runbook": "docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.objecttime_source_truth.json",
    "scan": "scripts\\scan_objecttime_source_truth_corpus_coverage.py",
    "gap": "scripts\\build_objecttime_source_truth_answer_gap_report.py",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_batch_baseline_packs_exist_with_required_files():
    for slug in CAPTURED_BATCH_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        assert pack_path.exists()
        for file_name in REQUIRED_FILES:
            assert (pack_path / file_name).exists()


def test_four_domain_batch_closeout_exists_and_is_linked_from_readme():
    assert CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/BASELINE_BATCH_CLOSEOUT_2026_05_13.md" in readme


def test_six_domain_maturity_closeout_exists_and_is_linked_from_readme():
    assert MATURITY_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/BASELINE_MATURITY_CLOSEOUT_2026_05_13.md" in readme


def test_six_domain_maturity_closeout_records_packs_and_final_ledger_counts():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 6" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Domains with runbook outstanding: none" in closeout
    assert "Annual Leave / Leave Management is no longer `RUNBOOK_OUTSTANDING`; it is now `BASELINE_ALREADY_EXISTS`" in closeout

    for pack_name in (
        "worker_story/v0_1/",
        "payroll_bases_totals/v0_1/",
        "payrun_admin_queue/v0_1/",
        "movement_review/v0_1/",
        "gross_to_net/v0_1/",
        "annual_leave/v0_1/",
    ):
        assert f"docs/evaluation/worker_story_baselines/{pack_name}" in closeout


def test_core_payroll_explanation_blocked_closeout_exists_and_is_linked_from_readme():
    assert CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/CORE_PAYROLL_EXPLANATION_BASELINE_BATCH_2026_05_13.md" in readme


def test_core_payroll_explanation_batch_closeout_exists_and_is_linked_from_readme():
    assert CORE_PAYROLL_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/CORE_PAYROLL_EXPLANATION_BATCH_CLOSEOUT_2026_05_13.md" in readme


def test_payroll_evidence_context_blocked_closeout_exists_and_is_linked_from_readme():
    assert PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/PAYROLL_EVIDENCE_CONTEXT_BASELINE_BATCH_2026_05_13.md" in readme


def test_decision_story_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "decision_story" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_finalisation_readiness_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "finalisation_readiness" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_payroll_output_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "payroll_output" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_rate_source_rate_story_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "ratesource_rate_story" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_payroll_evidence_context_blocked_packs_exist_with_required_files():
    for slug in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        assert pack_path.exists()
        for file_name in REQUIRED_FILES:
            assert (pack_path / file_name).exists()


def test_contact_payroll_history_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "contact_payroll_history" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_core_payroll_explanation_blocked_closeout_records_honest_statuses():
    closeout = _read(CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 6" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Readiness status: `DATABASE_CONNECTION_FAILED`" in closeout
    assert "Because readiness was not `READY`, benchmark, corpus coverage and answer gap commands were not run" in closeout
    assert "No other baseline-required domains were attempted" in closeout
    assert "No benchmark, corpus coverage or answer gap JSON reports were generated for this batch" in closeout

    for domain in ("Finalisation Readiness", "Payroll Output", "RateSource / Rate Story", "Decision Story"):
        assert f"| {domain} | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |" in closeout


def test_payroll_evidence_context_blocked_closeout_records_honest_statuses():
    closeout = _read(PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 21" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 10" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Readiness status: `DATABASE_CONNECTION_FAILED`" in closeout
    assert "Because readiness was not `READY`, benchmark, corpus coverage and answer gap commands were not run" in closeout
    assert "No other baseline-required domains were attempted" in closeout
    assert "No benchmark, corpus coverage or answer gap JSON reports were generated for this batch" in closeout

    for domain in (
        "Contact Payroll History",
        "ObjectTime / Source Truth",
        "Process Periods / PayRun Lifecycle",
        "Imports / Actuals",
    ):
        assert f"| {domain} | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |" in closeout


def test_core_payroll_explanation_batch_closeout_records_ledger_and_packs():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 21" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 10" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "No Core Payroll Explanation batch domains remain blocked" in closeout

    for pack_name in (
        "finalisation_readiness/v0_1/",
        "payroll_output/v0_1/",
        "ratesource_rate_story/v0_1/",
        "decision_story/v0_1/",
    ):
        assert f"docs/evaluation/worker_story_baselines/{pack_name}" in closeout


def test_core_payroll_explanation_batch_closeout_records_outcomes_without_changing_numbers():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "| Finalisation Readiness | Passed baseline with refinement | 12 total / 12 passed / 0 failed | STRONG=11, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 11 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| Payroll Output | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| RateSource / Rate Story | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| Decision Story | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout
    assert "Passed baselines and captured-with-failures baselines are both durable comparison controls, but they are different signals" in closeout


def test_core_payroll_explanation_batch_closeout_records_failure_and_refinement_classifications():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "payroll-output-rich-answer" in closeout
    assert "rate-source-rate-story-rich-answer" in closeout
    assert "decision-story-rich-answer" in closeout
    assert "Payroll Output failure is not corpus gap" in closeout
    assert "RateSource / Rate Story failure is not corpus gap" in closeout
    assert "Decision Story failure is not corpus gap" in closeout
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in closeout
    assert "Finalisation Readiness needs synthesis refinement for `purpose_and_operator_meaning`" in closeout
    assert "Payroll Output needs synthesis refinement for `worker_level_output`" in closeout
    assert "RateSource / Rate Story needs synthesis refinement for `rate_source_evidence_index`" in closeout


def test_core_payroll_explanation_batch_closeout_records_transient_json_policy_and_guardrails():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout
    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "No operational JSON ingestion occurred" in closeout
    assert "No Code Evidence answer integration occurred" in closeout
    assert "No live LLM call occurred" in closeout
    assert "No corpus mutation occurred" in closeout
    assert "No DB or schema migration occurred" in closeout
    assert "No endpoint or UI change occurred" in closeout
    assert "No workforce-platform change occurred" in closeout
    assert "should be small" in closeout
    assert "not attempt all remaining 21 `BASELINE_REQUIRED` domains at once" in closeout


def test_payroll_evidence_context_blocked_packs_record_non_execution_honestly():
    for slug, metadata in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS.items():
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert metadata["name"] in combined
        assert metadata["runbook"] in combined
        assert metadata["manifest"] in combined
        assert metadata["scan"] in combined
        assert metadata["gap"] in combined
        assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" in combined
        assert "Result status: `BLOCKED_DATABASE_CONNECTION`" in combined
        assert "Baseline pack created: blocked pack only" in combined
        assert "Benchmark result: not run" in combined
        assert "Corpus coverage result: not run" in combined
        assert "Answer gap report: not run" in combined
        assert "Total: not run" in combined
        assert "`STRONG`: not evaluated" in combined
        assert "Overall status: not evaluated" in combined
        assert "Generated artefact committed: no" in combined
        assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
        assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
        assert "Code Evidence answer integration: no" in combined
        assert "READY` before running commands" in combined
        assert "Result status: `COMPLETED`" not in combined
        assert "Result status: `COMPLETED_WITH_FAILURES`" not in combined


def test_payroll_evidence_context_blocked_packs_are_diagnostic_only_not_runtime_truth():
    for slug in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "does not change routing" in combined
        assert "does not change answer generation" in combined
        assert "does not call live LLM" in combined
        assert "does not ingest operational JSON" in combined
        assert "does not connect Code Evidence" in combined
        assert "does not create DB schema or migrations" in combined
        assert "does not add endpoints or UI" in combined
        assert "does not change workforce-platform" in combined


def test_objecttime_source_truth_recaptured_pack_records_refinement_required_state():
    metadata = OBJECTTIME_SOURCE_TRUTH_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "objecttime_source_truth" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness returned `READY`" in combined
    assert "Ready: yes" in combined
    assert "Selected ODBC driver: `ODBC Driver 17 for SQL Server`" in combined
    assert "Result status: `RECAPTURED_REQUIRES_REFINEMENT`" in combined
    assert "captured evidence with promotion withheld" in combined
    assert "Total: 12" in combined
    assert "Passed: 8" in combined
    assert "Failed: 4" in combined
    assert "Audit/chat rows created: false" in combined
    assert "objecttime-payrun-inclusion" in combined
    assert "objecttime-sourcetruth-vs-workedhours" in combined
    assert "objecttime-current-effective-output" in combined
    assert "objecttime-worker-story-source-truth" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 11" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 1" in combined
    assert "`outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`" in combined
    assert "benchmark failures are answer-synthesis/term-coverage issues, not corpus absence issues" in combined
    assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
    assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined


def test_objecttime_source_truth_recaptured_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "objecttime_source_truth" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "ObjectTimeAttribute",
        "ObjectTimeAssessment",
        "ObjectTimeAssessmentResponse",
        "SourceTruth is not WorkedHours",
        "Raw span hours are not user-facing payroll worked hours",
        "RoundedStart boundary for WORK ObjectTime",
        "changed-field detection",
        "previous value capture",
        "new value capture",
        "Finalised or protected dirty exclusion",
        "finalised correction review pathway",
        "EnableFinalisedCorrectionObjectTimeHookDryRun",
        "FinalisedCorrectionObjectTimeHookDryRunPreview",
        "DRY_RUN_PREVIEW_ERROR",
        "runtime intake readiness versus runtime intake implementation",
        "no mutation guarantee",
        "no dirty runtime call guarantee",
        "no review request creation guarantee",
    ):
        assert term in combined

    assert "Do not overclaim v5.56" in combined
    assert "It is not runtime intake" in combined
    assert "runtime source-change hook or intake" in combined
    assert "correction execution" in combined
    assert "payment or remittance execution" in combined
    assert "finalisation mutation" in combined


def test_process_periods_payrun_lifecycle_blocked_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "process_periods_payrun_lifecycle" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "not merely a date range or run list domain",
        "ProcessPeriod",
        "ProcessPeriodGroup",
        "PaymentDate",
        "PayRunBatch",
        "PayRunContact",
        "worker story PayRun context",
        "Contact Payroll History dependency",
        "reconciliation dependency",
        "source truth impact on PayRun outcomes",
        "`PaymentDate` belongs on `ProcessPeriod`",
        "payment-date derivation policy belongs on `ProcessPeriodGroup`",
        "`DAILY`, `WEEKLY`, `FORTNIGHTLY`, `MONTHLY` and `QUARTERLY`",
        "Dirty contact doctrine",
        "full contact-level PayRun reprocessing",
        "Finalised or protected PayRuns require correction or review pathways",
        "no runtime mutation guarantee",
    ):
        assert term in combined


def test_imports_actuals_blocked_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "imports_actuals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "not merely file upload or CSV parsing",
        "import batch",
        "import row",
        "import validation",
        "import error",
        "import warning",
        "award-specific CSV template",
        "timesheet import",
        "payroll actuals import",
        "external actuals",
        "calculated versus actual",
        "reconciliation",
        "variance",
        "pay code mapping",
        "RateType mapping",
        "tenant override mapping",
        "mapping snapshot",
        "shift assessment import",
        "shift attribute import",
        "claim import",
        "Claimable",
        "Claimable Hourly",
        "Claim Amount",
        "piece work / expense / mileage amount import context",
        "source truth provenance",
        "evidence preservation",
        "worker story explanation context",
        "source truth impact on PayRun outcomes",
        "no runtime mutation guarantee",
        "no benchmark promotion when DB readiness is blocked",
        "Imported actuals are evidence for reconciliation",
        "not the same as calculated payroll truth",
        "Minerva baseline packs do not mutate operational payroll data",
    ):
        assert term in combined


def test_contact_payroll_history_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CONTACT_PAYROLL_HISTORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "contact_payroll_history" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 5" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "contact-payroll-history-rich-answer" in combined
    assert "contact-payroll-history-retro-replay-correction" in combined
    assert "combination of benchmark answer-term expectation gap and source-evidence/matched-phrase drift" in combined
    assert "with corpus gap present for `gross_to_net_history`" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 7" in combined
    assert "`WEAK`: 3" in combined
    assert "`MISSING`: 1" in combined
    assert "`gross_to_net_history`" in combined
    assert "`current_and_historical_payroll_output`" in combined
    assert "`retro_replay_and_correction_relationship`" in combined
    assert "`outstanding_hardening`" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 7" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 2" in combined
    assert "`ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 1" in combined
    assert "Report type: `CONTACT_PAYROLL_HISTORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `CONTACT_PAYROLL_HISTORY`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_decision_story_baseline_pack_records_captured_ready_results_with_failures():
    metadata = DECISION_STORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "decision_story" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 6" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "decision-story-rich-answer" in combined
    assert "Source snippets/matched phrases did not contain all expected terms: Decision Story, DecisionEvidenceIndex, why a treatment" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 10" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 10" in combined
    assert "Report type: `DECISION_STORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `DECISION_STORY`" in combined
    assert "Keep current Decision Story retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_finalisation_readiness_baseline_pack_records_captured_ready_results():
    metadata = FINALISATION_READINESS_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "finalisation_readiness" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 12" in combined
    assert "Passed: 12" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 11" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `FINALISATION_READINESS_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `FINALISATION_READINESS`" in combined
    assert "`purpose_and_operator_meaning` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten Finalisation Readiness answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_payroll_output_baseline_pack_records_captured_ready_results_with_failures():
    metadata = PAYROLL_OUTPUT_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "payroll_output" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 6" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "payroll-output-rich-answer" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 10" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `PAYROLL_OUTPUT_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `PAYROLL_OUTPUT`" in combined
    assert "`worker_level_output` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten Payroll Output answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_rate_source_rate_story_baseline_pack_records_captured_ready_results_with_failures():
    metadata = RATE_SOURCE_RATE_STORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "ratesource_rate_story" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 6" in combined
    assert "Passed: 5" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "rate-source-rate-story-rich-answer" in combined
    assert "Source snippets/matched phrases did not contain all expected terms: RateSource, Rate Story, rate amount" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 10" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `RATE_SOURCE_RATE_STORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `RATE_SOURCE_RATE_STORY`" in combined
    assert "`rate_source_evidence_index` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten RateSource / Rate Story answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_core_payroll_explanation_blocked_packs_are_diagnostic_only_not_runtime_truth():
    for slug in ("decision_story",):
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "change routing" in combined
        assert "change answer generation" in combined
        assert "call live LLM" in combined
        assert "ingest operational JSON" in combined
        assert "connect Code Evidence" in combined
        assert "create DB schema or migrations" in combined
        assert "add endpoints or UI" in combined
        assert "change workforce-platform" in combined


def test_six_domain_maturity_closeout_records_outcomes_without_changing_numbers():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Original v0.3 history records 5 total / 4 passed / 1 failed" in closeout
    assert "later rerun records 5 total / 5 passed / 0 failed" in closeout
    assert "| Payroll Bases & Totals | Passed baseline with refinement | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT |" in closeout
    assert "| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout
    assert "| Annual Leave / Leave Management | Passed baseline | 1 total / 1 passed / 0 failed | STRONG=7, WEAK=0, MISSING=0 | GOOD; 7 KEEP actions |" in closeout


def test_six_domain_maturity_closeout_records_failure_and_refinement_classifications():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Payroll Bases & Totals remains `NEEDS_REFINEMENT`" in closeout
    assert "weak `outstanding_hardening` coverage maps to `IMPROVE_RETRIEVAL_TERMS`" in closeout
    assert "payrun-admin-queue-rich-answer" in closeout
    assert "payrun-admin-queue-cleanliness-assurance" in closeout
    assert "PayRun Admin Queue failures are not corpus gaps" in closeout
    assert "gross-to-net-current-effective-worker-story" in closeout
    assert "Gross-to-Net failure is not a corpus gap" in closeout
    assert "Do not weaken benchmark expectations" in closeout


def test_six_domain_maturity_closeout_records_transient_json_policy_and_guardrails():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout
    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "No operational JSON ingestion occurred" in closeout
    assert "No Code Evidence answer integration occurred" in closeout
    assert "No live LLM call occurred" in closeout
    assert "No corpus mutation occurred" in closeout
    assert "No DB or schema migration occurred" in closeout
    assert "No endpoint or UI change occurred" in closeout
    assert "No workforce-platform change occurred" in closeout
    assert "should be small" in closeout
    assert "not attempt all remaining 25 `BASELINE_REQUIRED` domains at once" in closeout


def test_four_domain_batch_closeout_records_all_domain_outcomes_and_ledger_counts():
    closeout = _read(CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 5" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 1" in closeout
    assert "Baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net" in closeout
    assert "Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING`" in closeout

    assert "| Payroll Bases & Totals | Passed baseline | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT |" in closeout
    assert "| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout


def test_four_domain_batch_closeout_preserves_failure_and_refinement_classifications():
    closeout = _read(CLOSEOUT_PATH)

    assert "Weak `outstanding_hardening` coverage requires retrieval-term hardening" in closeout
    assert "`outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`" in closeout
    assert "This is not a corpus gap" in closeout
    assert "payrun-admin-queue-rich-answer" in closeout
    assert "payrun-admin-queue-cleanliness-assurance" in closeout
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in closeout
    assert "gross-to-net-current-effective-worker-story" in closeout
    assert "benchmark answer-term expectation drift, not corpus gap" in closeout
    assert "Do not weaken benchmark expectations" in closeout
    assert "Movement Review is the clean baseline in this batch" in closeout


def test_four_domain_batch_closeout_records_diagnostic_boundaries_and_json_policy():
    closeout = _read(CLOSEOUT_PATH)

    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout


def test_payroll_bases_baseline_pack_records_captured_ready_results():
    metadata = CAPTURED_BATCH_DOMAINS["payroll_bases_totals"]
    pack_path = BASELINE_ROOT / "payroll_bases_totals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 6" in combined
    assert "Passed: 6" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 8" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 8" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 1" in combined
    assert "`outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`" in combined


def test_payrun_admin_queue_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CAPTURED_BATCH_DOMAINS["payrun_admin_queue"]
    pack_path = BASELINE_ROOT / "payrun_admin_queue" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 8" in combined
    assert "Passed: 6" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "payrun-admin-queue-rich-answer" in combined
    assert "payrun-admin-queue-cleanliness-assurance" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 11" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_movement_review_baseline_pack_records_captured_ready_results():
    metadata = CAPTURED_BATCH_DOMAINS["movement_review"]
    pack_path = BASELINE_ROOT / "movement_review" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 8" in combined
    assert "Passed: 8" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 11" in combined
    assert "Report type: `MOVEMENT_REVIEW_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `MOVEMENT_REVIEW`" in combined
    assert "Keep current Movement Review retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_gross_to_net_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CAPTURED_BATCH_DOMAINS["gross_to_net"]
    pack_path = BASELINE_ROOT / "gross_to_net" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 6" in combined
    assert "Passed: 5" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "gross-to-net-current-effective-worker-story" in combined
    assert "benchmark answer-term expectation drift, not corpus gap" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 10" in combined
    assert "Report type: `GROSS_TO_NET_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `GROSS_TO_NET`" in combined
    assert "Keep current Gross-to-Net retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_batch_baseline_packs_are_diagnostic_only_not_runtime_truth():
    for slug in CAPTURED_BATCH_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "does not change routing" in combined
        assert "does not change answer generation" in combined
        assert "does not call live LLM" in combined
        assert "does not ingest operational JSON" in combined
        assert "does not connect Code Evidence" in combined
        assert "does not create DB schema or migrations" in combined
        assert "does not add endpoints or UI" in combined
        assert "does not change workforce-platform" in combined


def test_ledger_counts_remain_honest_for_captured_batch():
    ledger = _read(LEDGER_PATH)

    assert "`BASELINE_REQUIRED`: 20" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 11" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management; Finalisation Readiness; Payroll Output; RateSource / Rate Story; Decision Story; Contact Payroll History" in ledger
    assert "Annual Leave / Leave Management" in ledger
    assert "Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "gross-to-net-current-effective-worker-story" in ledger
    assert "Failure is benchmark answer-term expectation drift, not corpus gap" in ledger
    assert "| PayRun Admin Queue | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| Movement Review | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 8 total, 8 passed, 0 failed" in ledger
    assert "| Gross-to-Net | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Payroll Bases & Totals | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Annual Leave / Leave Management now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Finalisation Readiness | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Finalisation Readiness now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 12 total, 12 passed, 0 failed" in ledger
    assert "corpus coverage 11 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 11 KEEP actions and 1 IMPROVE_SYNTHESIS action for `purpose_and_operator_meaning`" in ledger
    assert "| Payroll Output | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Payroll Output now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 7 total, 6 passed, 1 failed" in ledger
    assert "payroll-output-rich-answer" in ledger
    assert "corpus coverage 10 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `worker_level_output`" in ledger
    assert "Failure is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in ledger
    assert "| RateSource / Rate Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | RateSource / Rate Story now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "rate-source-rate-story-rich-answer" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `rate_source_evidence_index`" in ledger
    assert "| Decision Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Decision Story now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "decision-story-rich-answer" in ledger
    assert "answer gap status GOOD with 10 KEEP actions" in ledger
    assert "| Contact Payroll History | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Contact Payroll History now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 7 total, 5 passed, 2 failed" in ledger
    assert "contact-payroll-history-rich-answer" in ledger
    assert "contact-payroll-history-retro-replay-correction" in ledger
    assert "corpus coverage 7 STRONG, 3 WEAK, 1 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 7 KEEP actions, 1 IMPROVE_SYNTHESIS action, 2 IMPROVE_RETRIEVAL_TERMS actions and 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER action" in ledger
    assert "| ObjectTime / Source Truth | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger
    assert "| Process Periods / PayRun Lifecycle | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger
    assert "| Imports / Actuals | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger


def test_worker_story_baseline_history_remains_unchanged_after_batch():
    summary = _read(WORKER_STORY_PACK / "BASELINE_SUMMARY.md")
    benchmark = _read(WORKER_STORY_PACK / "BENCHMARK_BASELINE.md")

    assert "Benchmark result: 5 total, 4 passed, 1 failed" in summary
    assert "Failed benchmark: `worker-story-evidence-rich-answer`" in summary
    assert "synthesis/routing/answer-mode drift" in summary
    assert "Worker Story benchmark rerun: 5 total, 5 passed, 0 failed" in summary
    assert "Result status: `COMPLETED_WITH_FAILURES`" in benchmark


def test_annual_leave_baseline_pack_records_captured_ready_results():
    ledger = _read(LEDGER_PATH)
    combined = "\n".join(_read(ANNUAL_LEAVE_PACK / file_name) for file_name in REQUIRED_FILES)

    assert ANNUAL_LEAVE_PACK.exists()
    for file_name in REQUIRED_FILES:
        assert (ANNUAL_LEAVE_PACK / file_name).exists()

    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Annual Leave / Leave Management now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "app/services/annual_leave_answer_gap_report_service.py" in ledger
    assert "scripts/build_annual_leave_answer_gap_report.py" in ledger
    assert "Adjacent leave-domain v0.4 diagnostics are not substitutes" in ledger
    assert "Domains with runbook outstanding: none" in ledger

    assert "Annual Leave / Leave Management" in combined
    assert "docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md" in combined
    assert "samples\\eval\\rich_answer_benchmark.annual_leave.json" in combined
    assert "scripts\\scan_annual_leave_corpus_coverage.py" in combined
    assert "scripts\\build_annual_leave_answer_gap_report.py" in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 1" in combined
    assert "Passed: 1" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 7" in combined
    assert "`STRONG`: 7" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 7" in combined
    assert "Report type: `ANNUAL_LEAVE_MANAGEMENT_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `ANNUAL_LEAVE_MANAGEMENT`" in combined
    assert "Keep current Annual Leave / Leave Management retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_annual_leave_baseline_is_diagnostic_only_not_runtime_truth():
    combined = "\n".join(_read(ANNUAL_LEAVE_PACK / file_name) for file_name in REQUIRED_FILES)

    assert "diagnostic-only" in combined
    assert "not operational truth" in combined
    assert "does not mutate corpus" in combined
    assert "does not change routing" in combined
    assert "does not change answer generation" in combined
    assert "does not call live LLM" in combined
    assert "does not ingest operational JSON" in combined
    assert "does not connect Code Evidence" in combined
    assert "does not create DB schema or migrations" in combined
    assert "does not add endpoints or UI" in combined
    assert "does not change workforce-platform" in combined


def test_generated_json_reports_are_not_required_committed_baseline_artefacts():
    policy = _read(BASELINE_ROOT / "BASELINE_CAPTURE_POLICY.md")
    ledger = _read(LEDGER_PATH)

    assert "Generated outputs are transient evaluation materials" in policy
    assert "those command targets are not themselves checked-in baseline artefacts" in ledger

    for relative_path in (
        "reports/worker_story_corpus_coverage.json",
        "reports/worker_story_answer_gap_report.json",
        "artifacts/eval/payroll_bases_corpus_coverage.json",
        "artifacts/eval/payroll_bases_answer_gap_report.json",
        "artifacts/eval/payrun_admin_queue_corpus_coverage.json",
        "artifacts/eval/payrun_admin_queue_answer_gap_report.json",
        "artifacts/eval/movement_review_corpus_coverage.json",
        "artifacts/eval/movement_review_answer_gap_report.json",
        "artifacts/eval/gross_to_net_corpus_coverage.json",
        "artifacts/eval/gross_to_net_answer_gap_report.json",
        "artifacts/eval/annual_leave_corpus_coverage.json",
        "artifacts/eval/annual_leave_answer_gap_report.json",
        "artifacts/eval/finalisation_readiness_corpus_coverage.json",
        "artifacts/eval/finalisation_readiness_answer_gap_report.json",
        "artifacts/eval/payroll_output_corpus_coverage.json",
        "artifacts/eval/payroll_output_answer_gap_report.json",
        "artifacts/eval/rate_source_rate_story_corpus_coverage.json",
        "artifacts/eval/rate_source_rate_story_answer_gap_report.json",
        "artifacts/eval/decision_story_corpus_coverage.json",
        "artifacts/eval/decision_story_answer_gap_report.json",
        "artifacts/eval/contact_payroll_history_corpus_coverage.json",
        "artifacts/eval/contact_payroll_history_answer_gap_report.json",
        "artifacts/eval/objecttime_source_truth_corpus_coverage.json",
        "artifacts/eval/objecttime_source_truth_answer_gap_report.json",
        "artifacts/eval/process_period_payrun_lifecycle_corpus_coverage.json",
        "artifacts/eval/process_period_payrun_lifecycle_answer_gap_report.json",
        "artifacts/eval/imports_actuals_corpus_coverage.json",
        "artifacts/eval/imports_actuals_answer_gap_report.json",
    ):
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative_path],
            capture_output=True,
            text=True,
            check=False,
        )
        assert tracked.returncode != 0

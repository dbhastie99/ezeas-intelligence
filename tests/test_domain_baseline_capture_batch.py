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

PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS = {}

PROCESS_PERIODS_PAYRUN_LIFECYCLE_RECAPTURED_DOMAIN = {
    "name": "Process Periods / PayRun Lifecycle",
    "runbook": "docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.process_period_payrun_lifecycle.json",
    "scan": "scripts\\scan_process_period_payrun_lifecycle_corpus_coverage.py",
    "gap": "scripts\\build_process_period_payrun_lifecycle_answer_gap_report.py",
}

OBJECTTIME_SOURCE_TRUTH_RECAPTURED_DOMAIN = {
    "name": "ObjectTime / Source Truth",
    "runbook": "docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.objecttime_source_truth.json",
    "scan": "scripts\\scan_objecttime_source_truth_corpus_coverage.py",
    "gap": "scripts\\build_objecttime_source_truth_answer_gap_report.py",
}

IMPORTS_ACTUALS_RECAPTURED_DOMAIN = {
    "name": "Imports / Actuals",
    "runbook": "docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.imports_actuals.json",
    "scan": "scripts\\scan_imports_actuals_corpus_coverage.py",
    "gap": "scripts\\build_imports_actuals_answer_gap_report.py",
}

TAX_PAYG_RECAPTURED_DOMAIN = {
    "name": "Tax / PAYG",
    "runbook": "docs/TAX_PAYG_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.tax_payg.json",
    "scan": "scripts\\scan_tax_payg_corpus_coverage.py",
    "gap": "scripts\\build_tax_payg_answer_gap_report.py",
}

COMPARISON_REMEDIATION_CAPTURED_DOMAIN = {
    "name": "Comparison / Remediation",
    "runbook": "docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.comparison_remediation.json",
    "scan": "scripts\\scan_comparison_remediation_corpus_coverage.py",
    "gap": "scripts\\build_comparison_remediation_answer_gap_report.py",
}
IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN = (
    BASELINE_ROOT / "imports_actuals" / "v0_1" / "FORMAL_EVIDENCE_GAP_PLAN.md"
)
TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN = (
    BASELINE_ROOT / "tax_payg" / "v0_1" / "FORMAL_EVIDENCE_GAP_PLAN.md"
)
IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md"
)
TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md"
)
TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md"
)
IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md"
)
FORMAL_EVIDENCE_REVIEW_GATE_INDEX = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md"
)
FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md"
)
FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md"
)
SOURCE_EVIDENCE_DRAFTS_README = Path("docs/evaluation/source_evidence_drafts/README.md")
FORMAL_EVIDENCE_CONTROL_README_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md"
)
TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md"
)
IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md"
)


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


def test_process_periods_payrun_lifecycle_pack_records_promoted_state():
    metadata = PROCESS_PERIODS_PAYRUN_LIFECYCLE_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "process_periods_payrun_lifecycle" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "Readiness status: `READY`" in combined
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 13" in combined
    assert "Passed: 13" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 13" in combined
    assert "`STRONG`: 13" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`LOW` / `KEEP` groups: 13" in combined
    assert "`MEDIUM` refinement groups: 0" in combined
    assert "`purpose_and_operator_meaning`: STRONG -> `KEEP`" in combined
    assert "`close_rolls_forward`: STRONG -> `KEEP`" in combined
    assert "`outstanding_hardening`: STRONG -> `KEEP`" in combined
    assert "Baseline pack state: captured evidence and promoted" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "not corpus absence issues" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined


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


def test_imports_actuals_recaptured_pack_records_unpromoted_refinement_state():
    metadata = IMPORTS_ACTUALS_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "imports_actuals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 11" in combined
    assert "Passed: 8" in combined
    assert "Failed: 3" in combined
    assert "Audit/chat rows created: false" in combined
    assert "imports-actuals-pay-code-ratetype-mapping" in combined
    assert "imports-actuals-comparison-remediation-connection" in combined
    assert "imports-actuals-worker-story-admin-queue" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 9" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 2" in combined
    assert "`purpose_and_operator_meaning`: MISSING" in combined
    assert "`pay_code_and_rate_type_mapping`: WEAK" in combined
    assert "`outstanding_hardening`: MISSING" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`LOW` / `KEEP` groups: 9" in combined
    assert "`MEDIUM` / `IMPROVE_SYNTHESIS` groups: 1" in combined
    assert "`ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 2" in combined
    assert "This is not a successful captured/promoted baseline" in combined
    assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
    assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
    assert "real formal-corpus gaps" in combined
    assert "Promotion cannot happen solely through synthesis hardening" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "Baseline pack created: blocked pack only" not in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" not in combined


def test_tax_payg_recaptured_pack_records_unpromoted_refinement_state():
    metadata = TAX_PAYG_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "tax_payg" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 9" in combined
    assert "Passed: 7" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "tax-payg-rich-answer" in combined
    assert "tax-payg-minerva-not-calculate" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 1" in combined
    assert "`purpose_and_operator_meaning`: MISSING" in combined
    assert "`outstanding_hardening`: WEAK" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`LOW` / `KEEP` groups: 10" in combined
    assert "`HIGH` / `ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 1" in combined
    assert "`MEDIUM` / `IMPROVE_RETRIEVAL_TERMS` groups: 1" in combined
    assert "This is not a successful captured/promoted baseline" in combined
    assert "It is not DB-blocked" in combined
    assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
    assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
    assert "real formal source-evidence gap" in combined
    assert "Promotion cannot happen solely through synthesis hardening" in combined
    assert "Minerva must explain Tax / PAYG but must not calculate PAYG withholding" in combined
    assert "Deterministic services and tax providers own withholding calculation" in combined
    assert "Tax/PAYG rates, thresholds, bands, offsets and formulas must be governed data/rule-pack/configuration" in combined
    assert "PaymentDate and payroll context matter for Tax / PAYG selection" in combined
    assert "no tax runtime changes" in combined
    assert "no PAYG runtime changes" in combined
    assert "no ledger promotion" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "Baseline pack created: blocked pack only" not in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" not in combined


def test_tax_payg_formal_evidence_gap_plan_records_required_gaps_and_guardrails():
    assert TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN.exists()

    plan = _read(TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN)

    assert "Tax / PAYG remains `BASELINE_REQUIRED`" in plan
    assert "cannot be promoted solely through answer-synthesis hardening" in plan
    assert "DB readiness was not the blocker" in plan
    assert "Benchmark: 9 total / 7 passed / 2 failed" in plan
    assert "STRONG=10, WEAK=1, MISSING=1" in plan
    assert "Answer gap: `NEEDS_REFINEMENT`" in plan
    assert "10 KEEP, 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER, 1 IMPROVE_RETRIEVAL_TERMS" in plan
    assert "`purpose_and_operator_meaning`" in plan
    assert "`outstanding_hardening`" in plan
    assert "Missing formal source evidence group" in plan
    assert "Weak formal source evidence group" in plan
    assert "Minerva explains Tax / PAYG but does not calculate PAYG withholding" in plan
    assert "Formal source evidence is added to the corpus through the governed ingestion process" in plan
    assert "Coverage improves to no MISSING groups" in plan
    assert "`outstanding_hardening` becomes STRONG or is otherwise accepted with documented rationale" in plan
    assert "Benchmark passes 9/9" in plan
    assert "Answer gap becomes GOOD or acceptable" in plan
    assert "Ledger is promoted only after real command results support it" in plan
    assert "no corpus mutation" in plan
    assert "no operational JSON ingestion" in plan
    assert "no Code Evidence answer integration" in plan
    assert "no ledger promotion" in plan


def test_objecttime_source_truth_recaptured_pack_records_promoted_state():
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
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "captured evidence and promoted" in combined
    assert "Total: 12" in combined
    assert "Passed: 12" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 12" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 12" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 0" in combined
    assert "`outstanding_hardening` -> `KEEP`" in combined
    assert "previous promotion blocker is resolved without adding corpus" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "objecttime-payrun-inclusion" not in combined
    assert "objecttime-sourcetruth-vs-workedhours" not in combined
    assert "objecttime-current-effective-output" not in combined
    assert "objecttime-worker-story-source-truth" not in combined


def test_comparison_remediation_pack_records_promoted_state():
    metadata = COMPARISON_REMEDIATION_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "comparison_remediation" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness returned `READY`" in combined
    assert "Ready: yes" in combined
    assert "Selected ODBC driver: `ODBC Driver 17 for SQL Server`" in combined
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "captured evidence and promoted" in combined
    assert "Total: 9" in combined
    assert "Passed: 9" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 12" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`LOW` / `KEEP` groups: 12" in combined
    assert "`MEDIUM` refinement groups: 0" in combined
    assert "`three_lane_comparison_model`: STRONG -> `KEEP`" in combined
    assert "`actuals_as_external_outcome_truth`: STRONG -> `KEEP`" in combined
    assert "`outstanding_hardening`: STRONG -> `KEEP`" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined


def test_comparison_remediation_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "comparison_remediation" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "payroll evidence and review/remediation context, not generic diffing",
        "primary calculated",
        "comparator calculated",
        "actual imported / actuals lane",
        "primary award path remains operational payroll truth",
        "Imported actuals are external outcome truth",
        "comparison policy",
        "comparator selection",
        "active lanes",
        "offset policy",
        "output mode",
        "variance treatment",
        "review requirements",
        "Comparison run and line evidence",
        "Variance/top-up is a governed consequence",
        "Position/classification mapping",
        "Worker Story, Admin Queue, and Movement Review consume comparison evidence",
        "Baseline capture does not implement runtime comparison/remediation behaviour",
    ):
        assert term in combined


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


def test_process_periods_payrun_lifecycle_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "process_periods_payrun_lifecycle" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "not merely a date range or run list domain",
        "ProcessPeriod",
        "ProcessPeriodGroup",
        "PaymentDate",
        "PayRunContact",
        "Worker Story",
        "PayRun Admin Queue",
        "Movement Review",
        "`PaymentDate` belongs on `ProcessPeriod`",
        "payment-date derivation policy belongs on `ProcessPeriodGroup`",
        "admission is not processing",
        "closed dominates open",
        "current-effective payroll output",
    ):
        assert term in combined


def test_imports_actuals_recaptured_pack_preserves_domain_boundaries():
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
        "no promotion while benchmark failures and formal corpus gaps remain",
        "Imported actuals are evidence for reconciliation",
        "not the same as calculated payroll truth",
        "Minerva baseline packs do not mutate operational payroll data",
    ):
        assert term in combined


def test_imports_actuals_formal_evidence_gap_plan_records_required_gaps_and_guardrails():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN.exists()

    plan = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN)

    assert "Imports / Actuals remains `BASELINE_REQUIRED`" in plan
    assert "cannot be promoted solely through answer-synthesis hardening" in plan
    assert "DB readiness was not the blocker" in plan
    assert "Benchmark: 11 total / 8 passed / 3 failed" in plan
    assert "STRONG=9, WEAK=1, MISSING=2" in plan
    assert "Answer gap: `NEEDS_REFINEMENT`" in plan
    assert "9 KEEP, 1 IMPROVE_SYNTHESIS, 2 ADD_FORMAL_SOURCE_EVIDENCE_LATER" in plan
    assert "`purpose_and_operator_meaning`" in plan
    assert "`outstanding_hardening`" in plan
    assert "`pay_code_and_rate_type_mapping`" in plan
    assert "Missing formal source evidence groups" in plan
    assert "Weak formal source evidence group" in plan
    assert "Formal source evidence is added to the corpus through the governed ingestion process" in plan
    assert "Coverage improves to no MISSING groups" in plan
    assert "Benchmark passes 11/11" in plan
    assert "Answer gap becomes GOOD or acceptable" in plan
    assert "Ledger is promoted only after real command results support it" in plan
    assert "no corpus mutation" in plan
    assert "no operational JSON ingestion" in plan
    assert "no Code Evidence answer integration" in plan
    assert "no ledger promotion" in plan


def test_imports_actuals_formal_source_evidence_draft_records_required_evidence_and_guardrails():
    assert IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT.exists()

    draft = _read(IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT)

    assert "not merely file upload or CSV parsing" in draft
    assert "not calculated payroll truth" in draft
    assert "`purpose_and_operator_meaning`: MISSING" in draft
    assert "`outstanding_hardening`: MISSING" in draft
    assert "`pay_code_and_rate_type_mapping`: WEAK" in draft
    assert "pay code mapping" in draft
    assert "RateType mapping" in draft
    assert "imported actuals lane" in draft
    assert "primary calculated lane" in draft
    assert "comparator calculated lane" in draft
    assert "actuals lane" in draft
    assert "variance" in draft
    assert "Worker Story" in draft
    assert "Admin Queue" in draft
    assert "Mapping issues must be visible as reviewable issues" in draft
    assert "no operational JSON ingestion" in draft
    assert "no Code Evidence answer integration" in draft
    assert "no corpus mutation in this slice" in draft
    assert "no ledger promotion in this slice" in draft
    assert "Future Corpus-Ingestion Acceptance Criteria" in draft
    assert "Coverage rerun shows no MISSING groups" in draft
    assert "Benchmark passes 11/11" in draft
    assert "Ledger promotion happens only after real command results support promotion" in draft
    assert "Imports / Actuals is not promoted" in draft


def test_tax_payg_formal_source_evidence_draft_records_required_evidence_and_guardrails():
    assert TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT.exists()

    draft = _read(TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT)

    assert "not a generic calculator" in draft
    assert "Minerva explains Tax / PAYG but does not calculate PAYG withholding" in draft
    assert "`purpose_and_operator_meaning`: MISSING" in draft
    assert "`outstanding_hardening`: WEAK" in draft
    assert "governed withholding calculation evidence" in draft
    assert "deterministic services" in draft
    assert "tax providers" in draft
    assert "TaxStory" in draft
    assert "worker tax profile" in draft
    assert "ProcessPeriod PaymentDate" in draft
    assert "pay frequency" in draft
    assert "taxable basis" in draft
    assert "Payroll Bases & Totals" in draft
    assert "finalised totals" in draft
    assert "supplementary incremental PAYG" in draft
    assert "same-period taxable earnings" in draft
    assert "prior PAYG withheld" in draft
    assert "Worker Story" in draft
    assert "Admin Queue" in draft
    assert "no operational JSON ingestion" in draft
    assert "no Code Evidence answer integration" in draft
    assert "no corpus mutation in this slice" in draft
    assert "no ledger promotion in this slice" in draft
    assert "Future Corpus-Ingestion Acceptance Criteria" in draft
    assert "Coverage rerun shows no MISSING groups" in draft
    assert "`outstanding_hardening` becomes STRONG or is documented accepted" in draft
    assert "Benchmark passes 9/9" in draft
    assert "Answer gap becomes GOOD or acceptable" in draft
    assert "Ledger is promoted only after real command results support promotion" in draft
    assert "Tax / PAYG is not promoted" in draft


def test_imports_actuals_formal_evidence_review_gate_blocks_ingestion_until_ready():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE.exists()

    gate = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE)

    assert "Current review status: `NOT_REVIEWED`" in gate
    assert "Default review status: `NOT_REVIEWED`" in gate
    assert "`REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Current review status: `REVIEWED_READY_FOR_INGESTION`" not in gate
    assert "FORMAL_EVIDENCE_GAP_PLAN.md" in gate
    assert "IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md" in gate
    assert "`purpose_and_operator_meaning`" in gate
    assert "`outstanding_hardening`" in gate
    assert "`pay_code_and_rate_type_mapping`" in gate
    assert "no corpus mutation" in gate
    assert "no operational JSON ingestion" in gate
    assert "no Code Evidence answer integration" in gate
    assert "no ledger promotion" in gate
    assert "future explicit ingestion slice after review readiness" in gate


def test_tax_payg_formal_evidence_review_gate_blocks_ingestion_until_ready():
    assert TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE.exists()

    gate = _read(TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE)

    assert "Review gate version: v0.1" in gate
    assert "Current review status: `NOT_REVIEWED`" in gate
    assert "Default review status: `NOT_REVIEWED`" in gate
    assert "`NOT_REVIEWED`" in gate
    assert "`NEEDS_REVISION`" in gate
    assert "`REVIEWED_READY_FOR_INGESTION`" in gate
    assert "`SUPERSEDED`" in gate
    assert "Current review status: `REVIEWED_READY_FOR_INGESTION`" not in gate
    assert "FORMAL_EVIDENCE_GAP_PLAN.md" in gate
    assert "TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md" in gate
    assert "governed corpus ingestion is blocked" in gate
    assert "Governed ingestion must not happen until this review gate is marked `REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Status is `REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Tax / PAYG remains `BASELINE_REQUIRED`" in gate
    assert "The formal source-evidence draft is not enough by itself to permit ingestion" in gate
    assert "Minerva must not calculate PAYG withholding" in gate
    assert "control artefact, not a runtime feature" in gate
    assert "`purpose_and_operator_meaning`" in gate
    assert "`outstanding_hardening`" in gate
    assert "no corpus mutation" in gate
    assert "no operational JSON ingestion" in gate
    assert "no Code Evidence answer integration" in gate
    assert "no benchmark recapture" in gate
    assert "no baseline promotion" in gate
    assert "no ledger promotion" in gate
    assert "benchmark promotion" not in gate.lower()
    assert "runtime PAYG calculation has been implemented" not in gate


def test_formal_evidence_review_gate_index_records_ingestion_guards():
    assert FORMAL_EVIDENCE_REVIEW_GATE_INDEX.exists()

    index = _read(FORMAL_EVIDENCE_REVIEW_GATE_INDEX)

    assert "Imports / Actuals" in index
    assert "Tax / PAYG" in index
    assert "Tax / PAYG is not promoted and remains `BASELINE_REQUIRED`" in index
    assert "Imports / Actuals is not promoted and remains `BASELINE_REQUIRED`" in index
    assert "A review gate with `NOT_REVIEWED` blocks governed ingestion" in index
    assert "Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice" in index
    assert "A formal source-evidence draft alone does not permit governed ingestion" in index
    assert "Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence" in index
    assert "| Tax / PAYG | `BASELINE_REQUIRED`" in index
    assert "| Imports / Actuals | `BASELINE_REQUIRED`" in index
    assert "| Tax / PAYG | `BASELINE_ALREADY_EXISTS`" not in index
    assert "| Imports / Actuals | `BASELINE_ALREADY_EXISTS`" not in index
    assert "Tax / PAYG is promoted" not in index
    assert "Imports / Actuals is promoted" not in index


def test_formal_evidence_review_decision_record_template_records_review_decision_guards():
    assert FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.exists()

    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "`NOT_REVIEWED`" in template
    assert "`NEEDS_REVISION`" in template
    assert "`REVIEWED_READY_FOR_INGESTION`" in template
    assert "`SUPERSEDED`" in template
    assert "A formal source-evidence draft alone does not permit governed ingestion" in template
    assert "A review gate with `NOT_REVIEWED` blocks governed ingestion" in template
    assert "A review gate with `NEEDS_REVISION` blocks governed ingestion" in template
    assert "Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice" in template
    assert "`REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus" in template
    assert "`REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline" in template
    assert "Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence" in template
    assert "No domain is promoted merely because a review decision exists" in template
    assert "Minerva must not overstate review, ingestion, runtime, or promotion state" in template
    assert "Reviewer name:" in template
    assert "Review date:" in template
    assert "Reviewer rationale:" in template
    assert "Reviewed source artefacts:" in template
    assert "Required follow-up actions:" in template
    assert "Whether governed ingestion is permitted:" in template
    assert "Whether recapture is permitted:" in template
    assert "Whether promotion is permitted:" in template
    assert "Imports / Actuals" in template
    assert "Tax / PAYG" in template
    assert "These examples are placeholders for future completed decision records. They do not mark either domain as reviewed or ready." in template
    assert "Governed ingestion permitted: No unless `REVIEWED_READY_FOR_INGESTION`" in template
    assert "Promotion permitted: No" in template
    assert "Imports / Actuals is not merely file upload or CSV parsing" in template
    assert "Minerva may explain Tax / PAYG but must not calculate PAYG withholding" in template
    assert "Imports / Actuals remains `BASELINE_ALREADY_EXISTS`" not in template
    assert "Tax / PAYG remains `BASELINE_ALREADY_EXISTS`" not in template


def test_formal_evidence_review_decision_record_template_has_required_sections():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for section in (
        "## 1. Review Decision Record Header",
        "## 2. Domain and Baseline Status",
        "## 3. Source Artefacts Reviewed",
        "## 4. Review Gate Status Before Decision",
        "## 5. Review Decision",
        "## 6. Allowed Decision Statuses",
        "## 7. Doctrine Review Findings",
        "## 8. Implementation-State Review Findings",
        "## 9. Evidence-Gap Coverage Findings",
        "## 10. Non-Overclaiming Review",
        "## 11. Ingestion Decision",
        "## 12. Recapture Decision",
        "## 13. Promotion Decision",
        "## 14. Reviewer Details",
        "## 15. Required Follow-Up Actions",
        "## 16. Minerva Answering Implications",
        "## 17. Non-Goals / Explicitly Not Changed",
        "## Domain Example Placeholders",
        "### Imports / Actuals",
        "### Tax / PAYG",
    ):
        assert section in template


def test_formal_evidence_review_decision_record_template_has_required_fillable_fields():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for field in (
        "Decision record title: `<domain name> Formal Evidence Review Decision Record <version>`",
        "Decision record version: `<version>`",
        "Domain name: `<domain name>`",
        "Domain slug: `<domain slug>`",
        "Review date: `<YYYY-MM-DD>`",
        "Reviewer name: `<reviewer name>`",
        "Reviewer rationale: `<brief rationale for the selected decision status>`",
        "Baseline status before review: `<BASELINE_REQUIRED | BASELINE_ALREADY_EXISTS | other recorded status>`",
        "Review gate file path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_EVIDENCE_REVIEW_GATE_...md>`",
        "Formal evidence gap plan path: `<docs/evaluation/worker_story_baselines/.../FORMAL_EVIDENCE_GAP_PLAN.md>`",
        "Formal source-evidence draft path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_SOURCE_EVIDENCE_DRAFT_...md>`",
        "Reviewed source artefacts: `<list every artefact reviewed>`",
        "Current review status before decision: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`",
        "Governed ingestion permitted before decision: `<Yes | No>`",
        "Recapture permitted before decision: `<Yes | No>`",
        "Promotion permitted before decision: `<Yes | No>`",
        "Selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`",
        "Doctrine review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Implementation-state review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Evidence-gap review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Non-overclaiming review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Whether governed ingestion is permitted: `<Yes | No>`",
        "Whether recapture is permitted: `<Yes | No>`",
        "Whether promotion is permitted: `<Yes | No>`",
        "Required promotion evidence: `real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture`",
        "Minerva may say: `<allowed answer implication>`",
        "Minerva must not say: `<blocked answer implication>`",
    ):
        assert field in template


def test_formal_evidence_review_decision_record_template_lists_allowed_statuses_and_rules_explicitly():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "The selected decision status must be exactly one of:" in template
    for status in (
        "`NOT_REVIEWED`",
        "`NEEDS_REVISION`",
        "`REVIEWED_READY_FOR_INGESTION`",
        "`SUPERSEDED`",
    ):
        assert status in template

    for rule in (
        "1. A formal source-evidence draft alone does not permit governed ingestion.",
        "2. A review gate with `NOT_REVIEWED` blocks governed ingestion.",
        "3. A review gate with `NEEDS_REVISION` blocks governed ingestion.",
        "4. A `SUPERSEDED` draft/gate must not be used for governed ingestion.",
        "5. Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice.",
        "6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.",
        "7. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.",
        "8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.",
        "9. No domain is promoted merely because a review decision exists.",
        "10. Minerva must not overstate review, ingestion, runtime, or promotion state.",
    ):
        assert rule in template


def test_formal_evidence_review_decision_record_template_preserves_examples_and_non_goals():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for required_text in (
        "These examples are placeholders for future completed decision records. They do not mark either domain as reviewed or ready.",
        "Domain name: `Imports / Actuals`",
        "Domain slug: `imports_actuals`",
        "Example current review status before decision: `NOT_REVIEWED`",
        "Example selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | SUPERSEDED, unless a future reviewer explicitly selects REVIEWED_READY_FOR_INGESTION>`",
        "Note: Imports / Actuals is not merely file upload or CSV parsing.",
        "Domain name: `Tax / PAYG`",
        "Domain slug: `tax_payg`",
        "Note: Minerva may explain Tax / PAYG but must not calculate PAYG withholding.",
        "It does not change completed-domain ledger counts.",
    ):
        assert required_text in template

    for non_goal in (
        "DB writes",
        "migrations",
        "corpus mutation",
        "operational JSON ingestion",
        "Code Evidence integration",
        "live LLM calls",
        "benchmark recapture",
        "baseline promotion",
        "ledger promotion",
        "endpoint changes",
        "UI changes",
        "workforce-platform changes",
        "award-configurator-v1 changes",
        "payroll runtime changes",
        "tax runtime changes",
    ):
        assert f"- {non_goal}" in template


def test_formal_evidence_review_decision_record_template_does_not_overclaim_approval_ingestion_or_promotion():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "Do not treat draft text, chat agreement or file existence as review approval." in template
    assert "Governed ingestion is permitted only when the selected decision status is `REVIEWED_READY_FOR_INGESTION`" in template
    assert "this decision record only permits a future governed ingestion slice; it does not perform ingestion or mutate corpus" in template
    assert "Recapture must not be treated as permitted merely because a draft exists or because a review decision exists" in template
    assert "No domain is promoted merely because a review decision exists" in template
    assert "It must not describe a formal source-evidence draft as ingested corpus evidence unless a later governed ingestion artefact records that fact" in template

    for overclaim in (
        "Current review status: `REVIEWED_READY_FOR_INGESTION`",
        "Example current review status before decision: `REVIEWED_READY_FOR_INGESTION`",
        "Governed ingestion permitted: Yes",
        "Promotion permitted: Yes",
        "baseline has been promoted",
        "ledger has been promoted",
        "corpus evidence has been ingested",
        "review approval is implied",
    ):
        assert overclaim not in template


def test_tax_payg_not_reviewed_decision_record_blocks_ingestion_recapture_and_promotion():
    assert TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED.exists()

    record = _read(TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED)

    for referenced_path in (
        "docs/evaluation/worker_story_baselines/tax_payg/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
    ):
        assert referenced_path in record

    for required_text in (
        "Domain name: `Tax / PAYG`",
        "Domain slug: `tax_payg`",
        "Baseline status before review: `BASELINE_REQUIRED`",
        "Review gate status before decision: `NOT_REVIEWED`",
        "Selected decision status: `NOT_REVIEWED`",
        "Reviewer name: not assigned",
        "Review date: not recorded",
        "Doctrine review outcome: not reviewed",
        "Implementation-state review outcome: not reviewed",
        "Evidence-gap review outcome: not reviewed",
        "Non-overclaiming review outcome: not reviewed",
        "Governed ingestion permitted: No",
        "Recapture permitted: No",
        "Promotion permitted: No",
        "Minerva must not calculate PAYG withholding",
        "Tax / PAYG remains `BASELINE_REQUIRED`",
        "No Tax / PAYG corpus mutation has occurred in this slice",
        "No Tax / PAYG benchmark recapture has occurred in this slice",
        "No Tax / PAYG ledger promotion occurred in this slice",
    ):
        assert required_text in record

    assert "Selected decision status: `REVIEWED_READY_FOR_INGESTION`" not in record
    assert "Tax / PAYG is `BASELINE_ALREADY_EXISTS`" not in record
    assert "governed ingestion has occurred" not in record
    assert "corpus has been mutated" not in record
    assert "ledger has been promoted" not in record


def test_imports_actuals_not_reviewed_decision_record_blocks_ingestion_recapture_and_promotion():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED.exists()

    record = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED)

    for referenced_path in (
        "docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
    ):
        assert referenced_path in record

    for required_text in (
        "Domain name: `Imports / Actuals`",
        "Domain slug: `imports_actuals`",
        "Baseline status before review: `BASELINE_REQUIRED`",
        "Review gate status before decision: `NOT_REVIEWED`",
        "Selected decision status: `NOT_REVIEWED`",
        "Reviewer name: not assigned",
        "Review date: not recorded",
        "Doctrine review outcome: not reviewed",
        "Implementation-state review outcome: not reviewed",
        "Evidence-gap review outcome: not reviewed",
        "Non-overclaiming review outcome: not reviewed",
        "Governed ingestion permitted: No",
        "Recapture permitted: No",
        "Promotion permitted: No",
        "Imports / Actuals is not merely file upload or CSV parsing",
        "Imported actuals are evidence for reconciliation and comparison; they are not the same as calculated payroll truth.",
        "Pay code and RateType mapping must remain evidence-bearing and reviewable.",
        "Imports / Actuals remains `BASELINE_REQUIRED`",
        "No Imports / Actuals corpus mutation has occurred in this slice",
        "No Imports / Actuals benchmark recapture has occurred in this slice",
        "No Imports / Actuals ledger promotion occurred in this slice",
    ):
        assert required_text in record

    assert "Selected decision status: `REVIEWED_READY_FOR_INGESTION`" not in record
    assert "Imports / Actuals is `BASELINE_ALREADY_EXISTS`" not in record
    assert "governed ingestion has occurred" not in record
    assert "corpus has been mutated" not in record
    assert "ledger has been promoted" not in record


def test_formal_evidence_review_decision_record_index_records_not_reviewed_decisions_and_guards():
    assert FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.exists()

    index = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
    ):
        assert referenced_path in index

    for required_text in (
        "| Tax / PAYG | `tax_payg` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |",
        "| Imports / Actuals | `imports_actuals` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |",
        "Tax / PAYG remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.",
        "1. A filled decision record does not itself permit governed ingestion.",
        "2. A `NOT_REVIEWED` decision record blocks governed ingestion.",
        "3. A `NEEDS_REVISION` decision record blocks governed ingestion.",
        "4. A `SUPERSEDED` decision record must not be used for governed ingestion.",
        "5. Only `REVIEWED_READY_FOR_INGESTION` can permit planning a future governed ingestion slice.",
        "6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.",
        "7. `REVIEWED_READY_FOR_INGESTION` does not itself run recapture.",
        "8. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.",
        "9. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.",
        "10. No domain is promoted merely because a decision record exists.",
        "11. Minerva must not overstate review, ingestion, runtime, recapture, or promotion state.",
    ):
        assert required_text in index

    assert "| Tax / PAYG | `tax_payg` | `BASELINE_ALREADY_EXISTS`" not in index
    assert "| Imports / Actuals | `imports_actuals` | `BASELINE_ALREADY_EXISTS`" not in index
    assert "governed ingestion has occurred" not in index
    assert "corpus has been mutated" not in index
    assert "ledger has been promoted" not in index


def test_source_evidence_drafts_readme_records_formal_evidence_control_model():
    assert SOURCE_EVIDENCE_DRAFTS_README.exists()

    readme = _read(SOURCE_EVIDENCE_DRAFTS_README)

    for section in (
        "## 1. Purpose",
        "## 2. Scope",
        "## 3. Formal Evidence Lifecycle",
        "## 4. Artefact Types",
        "## 5. Current Controlled Domains",
        "## 6. Status and Permission Rules",
        "## 7. Minerva Usage Guidance",
        "## 8. Codex Prompt Preservation Workflow",
        "## 9. Generated Artefact Policy",
        "## 10. Non-Goals",
        "## 11. Follow-Up Workflow",
    ):
        assert section in readme

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/codex_prompts/",
    ):
        assert referenced_path in readme

    for lifecycle_step in (
        "evidence gap identified",
        "→ formal evidence gap plan",
        "→ formal source-evidence draft",
        "→ formal evidence review gate",
        "→ review-gate index",
        "→ formal evidence review decision record template",
        "→ filled review decision record",
        "→ decision-record index",
        "→ REVIEWED_READY_FOR_INGESTION only after explicit review",
        "→ separate governed ingestion slice",
        "→ recapture",
        "→ benchmark/corpus/answer-gap evidence",
        "→ possible ledger promotion",
    ):
        assert lifecycle_step in readme

    for required_text in (
        "`BASELINE_REQUIRED`: 17",
        "`BASELINE_ALREADY_EXISTS`: 14",
        "`RUNBOOK_OUTSTANDING`: 0",
        "`NEEDS_REVIEW`: 0",
        "Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED`.",
        "Both domains have complete `NOT_REVIEWED` control chains.",
        "A draft is not ingested corpus evidence and does not permit recapture or promotion.",
        "A `NOT_REVIEWED` decision record is a durable block, not approval.",
        "Only `REVIEWED_READY_FOR_INGESTION` can permit planning a separate governed ingestion slice.",
        "Minerva must say that both domains remain `BASELINE_REQUIRED` while the latest decision records are `NOT_REVIEWED`.",
        "repository artefacts, not chat, as the durable source of truth",
        "Generated benchmark, corpus coverage, answer-gap, and evaluation JSON outputs are transient",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md",
    ):
        assert required_text in readme

    for blocked_claim in (
        "review approval has occurred",
        "governed ingestion has occurred",
        "corpus has been mutated",
        "ledger has been promoted",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in readme


def test_formal_evidence_control_readme_prompt_is_preserved():
    assert FORMAL_EVIDENCE_CONTROL_README_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_CONTROL_README_PROMPT)

    for required_text in (
        "# Codex Prompt — Minerva Formal Evidence Control README v0.1",
        "Mode: Documentation/control-readme hardening only",
        "Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, recapture, or governed ingestion.",
        "Both domains now have complete NOT_REVIEWED control chains.",
        "Chat is not the durable source of truth.",
        "docs/evaluation/source_evidence_drafts/README.md",
        "tests/test_domain_baseline_capture_batch.py",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md",
        "→ REVIEWED_READY_FOR_INGESTION only after explicit review",
        "→ possible ledger promotion",
    ):
        assert required_text in prompt


def test_tax_payg_review_notes_reference_review_gate_and_preserve_not_promoted_state():
    notes_path = BASELINE_ROOT / "tax_payg" / "v0_1" / "REVIEW_NOTES.md"
    notes = _read(notes_path)

    assert "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md" in notes
    assert "current review status `NOT_REVIEWED`" in notes
    assert "governed corpus ingestion remains blocked until the gate is marked `REVIEWED_READY_FOR_INGESTION`" in notes
    assert "Tax / PAYG as `BASELINE_REQUIRED`" in notes
    assert "Do not promote Tax / PAYG" in notes
    assert "no ledger promotion" in notes


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

    assert "`BASELINE_REQUIRED`: 17" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 14" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management; Finalisation Readiness; Payroll Output; RateSource / Rate Story; Decision Story; Contact Payroll History; ObjectTime / Source Truth; Process Periods / PayRun Lifecycle; Comparison / Remediation" in ledger
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
    assert "| ObjectTime / Source Truth | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | ObjectTime / Source Truth now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "corpus coverage 12 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 12 KEEP actions" in ledger
    assert "| Process Periods / PayRun Lifecycle | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Process Periods / PayRun Lifecycle now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "corpus coverage 13 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 13 KEEP actions" in ledger
    assert "| Comparison / Remediation | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Comparison / Remediation now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 9 total, 9 passed, 0 failed" in ledger
    assert "corpus coverage 12 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 12 KEEP actions" in ledger
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
        "artifacts/eval/tax_payg_corpus_coverage.json",
        "artifacts/eval/tax_payg_answer_gap_report.json",
        "artifacts/eval/comparison_remediation_corpus_coverage.json",
        "artifacts/eval/comparison_remediation_answer_gap_report.json",
    ):
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative_path],
            capture_output=True,
            text=True,
            check=False,
        )
        assert tracked.returncode != 0

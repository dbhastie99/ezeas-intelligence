from pathlib import Path


BASELINE_ROOT = Path("docs/evaluation/worker_story_baselines")
POLICY_PATH = BASELINE_ROOT / "BASELINE_CAPTURE_POLICY.md"
LEDGER_PATH = BASELINE_ROOT / "COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md"
PACK_PATH = BASELINE_ROOT / "worker_story" / "v0_1"
REQUIRED_FILES = (
    "BASELINE_SUMMARY.md",
    "BENCHMARK_BASELINE.md",
    "CORPUS_COVERAGE_BASELINE.md",
    "ANSWER_GAP_REPORT_BASELINE.md",
    "REVIEW_NOTES.md",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_worker_story_baseline_policy_and_pack_files_exist():
    assert POLICY_PATH.exists()
    assert PACK_PATH.exists()

    for file_name in REQUIRED_FILES:
        assert (PACK_PATH / file_name).exists()


def test_worker_story_baseline_files_contain_diagnostic_guardrails():
    files = [POLICY_PATH, *(PACK_PATH / file_name for file_name in REQUIRED_FILES)]

    for path in files:
        text = _read(path)
        assert "diagnostic" in text
        assert "not operational truth" in text
        assert "does not mutate corpus" in text or "do not mutate corpus" in text
        assert "does not change routing" in text or "do not change routing" in text
        assert "does not change answer generation" in text or "do not change answer generation" in text
        assert "does not call live LLM" in text or "do not call live LLM" in text or "live LLM" in text
        assert "does not ingest operational JSON" in text or "do not ingest operational JSON" in text
        assert "does not connect Code Evidence" in text or "do not connect Code Evidence" in text


def test_worker_story_baseline_summary_references_sources_and_evidence_groups():
    summary = _read(PACK_PATH / "BASELINE_SUMMARY.md")

    assert "Worker Story Baseline Capture v0.3" in summary
    assert "Record READY Baseline Results" in summary
    assert "docs/WORKER_STORY_EVALUATION_RUNBOOK.md" in summary
    assert "docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md" in summary
    assert "Captured on 2026-05-12" in summary
    assert "DB readiness result: `READY`" in summary
    assert "Benchmark result: 5 total, 4 passed, 1 failed" in summary
    assert "Corpus coverage result: `STRONG` = 10, `WEAK` = 0, `MISSING` = 0" in summary
    assert "Answer gap report: `GOOD`; all groups `KEEP`" in summary
    assert "synthesis/routing/answer-mode drift" in summary
    assert "not a missing corpus evidence gap" in summary

    for group in (
        "worker_story_purpose",
        "source_truth_and_inclusion",
        "interpreted_worked_hours",
        "calculated_payroll_outcome",
        "decision_story_and_rate_story",
        "leave_and_accrual_outcome",
        "payroll_bases_and_totals",
        "movement_review_and_admin_queue",
        "current_effective_truth",
        "outstanding_hardening",
    ):
        assert group in summary


def test_worker_story_v03_baseline_failure_remains_recorded():
    summary = _read(PACK_PATH / "BASELINE_SUMMARY.md")
    benchmark = _read(PACK_PATH / "BENCHMARK_BASELINE.md")
    combined = f"{summary}\n{benchmark}"

    assert "Benchmark result: 5 total, 4 passed, 1 failed" in summary
    assert "Result status: `COMPLETED_WITH_FAILURES`" in benchmark
    assert "Total: 5" in benchmark
    assert "Passed: 4" in benchmark
    assert "Failed: 1" in benchmark
    assert "worker-story-evidence-rich-answer" in combined
    assert "synthesis/routing/answer-mode drift" in combined
    assert "not corpus coverage gap" in benchmark
    assert "not a missing corpus evidence gap" in summary


def test_worker_story_post_baseline_hardening_note_records_clean_reruns():
    summary = _read(PACK_PATH / "BASELINE_SUMMARY.md")
    benchmark = _read(PACK_PATH / "BENCHMARK_BASELINE.md")
    notes = _read(PACK_PATH / "REVIEW_NOTES.md")
    combined = f"{summary}\n{benchmark}\n{notes}"

    assert "Post-Baseline Hardening Note v0.1" in summary
    assert "Post-Baseline Hardening Note v0.1" in benchmark
    assert "Post-Baseline Hardening Note v0.1" in notes
    assert "DB readiness returned `READY`" in combined
    assert "Worker Story benchmark rerun: 5 total, 5 passed, 0 failed" in summary
    assert "Worker Story benchmark: 5 total, 5 passed, 0 failed" in benchmark
    assert "Worker Story benchmark: 5 total, 5 passed, 0 failed" in notes
    assert "Annual Leave regression benchmark: 1 total, 1 passed, 0 failed" in combined
    assert "Audit/chat rows created: false" in combined
    assert "considered addressed by synthesis/routing hardening" in combined
    assert "Corpus coverage remains interpreted as sufficient" in combined
    assert "not the source of the issue" in summary
    assert "does not overwrite the v0.3 baseline history" in combined


def test_worker_story_post_baseline_note_preserves_diagnostic_only_boundaries():
    combined = "\n".join(_read(PACK_PATH / file_name) for file_name in REQUIRED_FILES)

    for forbidden_claim in (
        "Corpus mutation: yes",
        "Live LLM calls: yes",
        "Operational JSON ingestion: yes",
        "Code Evidence connected: yes",
        "DB/schema/migration added",
        "endpoint added",
        "UI added",
        "workforce-platform changed",
    ):
        assert forbidden_claim not in combined

    assert "does not mutate corpus" in combined
    assert "does not ingest operational JSON" in combined
    assert "does not connect Code Evidence" in combined
    assert "does not call live LLM" in combined
    assert "does not claim corpus mutation" in combined
    assert "database schema changes" in combined
    assert "endpoints or UI changes" in combined


def test_worker_story_baseline_pack_records_ready_results_without_runtime_truth_claims():
    combined = "\n".join(_read(PACK_PATH / file_name) for file_name in REQUIRED_FILES)

    assert "not operational truth" in combined
    assert "does not prove runtime platform truth" in combined
    assert "does not prove payroll/runtime truth" in combined
    assert "DB readiness returned `READY`" in combined
    assert "Total: 5" in combined
    assert "Passed: 4" in combined
    assert "Failed: 1" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 10" in combined
    assert "called a live LLM" in combined
    assert "connected Code Evidence to answer generation" in combined
    assert "does not mutate corpus" in combined
    assert "Corpus mutation: no" in combined
    assert "Live LLM calls: no" in combined
    assert "does not connect Code Evidence to answer generation" in combined


def test_worker_story_baseline_files_include_executed_command_summaries():
    benchmark = _read(PACK_PATH / "BENCHMARK_BASELINE.md")
    coverage = _read(PACK_PATH / "CORPUS_COVERAGE_BASELINE.md")
    gap_report = _read(PACK_PATH / "ANSWER_GAP_REPORT_BASELINE.md")

    assert "## Command Executed" in benchmark
    assert ".\\.venv\\Scripts\\python.exe scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures" in benchmark
    assert "Result status: `COMPLETED_WITH_FAILURES`" in benchmark
    assert "Total: 5" in benchmark
    assert "Passed: 4" in benchmark
    assert "Failed: 1" in benchmark
    assert "worker-story-evidence-rich-answer" in benchmark
    assert "What is Worker Story and what evidence does it show?" in benchmark
    assert "Worker Story, platform evidence surface, source truth, calculated payroll outcome, current-effective payroll output, Decision Story, Rate Story, evidence, outstanding hardening" in benchmark
    assert "Annual Leave wording" in benchmark
    assert "synthesis/routing/answer-mode drift" in benchmark
    assert "Audit/chat rows created: false" in benchmark

    assert "## Commands Executed" in coverage
    assert ".\\.venv\\Scripts\\python.exe scripts/scan_worker_story_corpus_coverage.py" in coverage
    assert ".\\.venv\\Scripts\\python.exe scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json" in coverage
    assert "Domain: Worker Story / Worker Calculation Story" in coverage
    assert "Indexed corpus: 5 active documents, 4583 chunks" in coverage
    assert "`STRONG`: 10" in coverage
    assert "`WEAK`: 0" in coverage
    assert "`MISSING`: 0" in coverage
    assert "Live LLM calls: no" in coverage
    assert "Corpus mutation: no" in coverage
    assert "not be treated as a formal corpus gap" in coverage

    assert "## Commands Executed" in gap_report
    assert ".\\.venv\\Scripts\\python.exe scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json" in gap_report
    assert ".\\.venv\\Scripts\\python.exe scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json" in gap_report
    assert "Result status: `COMPLETED`" in gap_report
    assert "Overall status: `GOOD`" in gap_report
    assert "`KEEP`: 10" in gap_report
    assert "`IMPROVE_RETRIEVAL_TERMS`: 0" in gap_report
    assert "`IMPROVE_SYNTHESIS`: 0" in gap_report
    assert "`ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 0" in gap_report
    assert "STRONG` -> `KEEP`" in gap_report
    assert "Keep current Worker Story retrieval terms and answer synthesis under benchmark watch" in gap_report
    assert "benchmark still exposes answer synthesis/routing/answer-mode drift" in gap_report


def test_worker_story_baseline_ledger_status_and_counts_are_consistent():
    ledger = _read(LEDGER_PATH)

    assert "| Worker Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Worker Story now has a checked-in baseline artefact pack" in ledger
    assert "`BASELINE_REQUIRED`: 26" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 5" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net" in ledger


def test_worker_story_baseline_readme_pointer_exists():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/evaluation/worker_story_baselines/" in readme
    assert "Worker Story baseline capture policy" in readme
    assert "v0.3 captured baseline" in readme
    assert "5 total / 4 passed / 1 failed" in readme
    assert "10 STRONG / 0 WEAK / 0 MISSING" in readme
    assert "answer gap status GOOD with all groups KEEP" in readme
    assert "comparison controls only" in readme

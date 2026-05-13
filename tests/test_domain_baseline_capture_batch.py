import subprocess
from pathlib import Path


BASELINE_ROOT = Path("docs/evaluation/worker_story_baselines")
LEDGER_PATH = BASELINE_ROOT / "COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md"
CLOSEOUT_PATH = BASELINE_ROOT / "BASELINE_BATCH_CLOSEOUT_2026_05_13.md"
WORKER_STORY_PACK = BASELINE_ROOT / "worker_story" / "v0_1"
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

    assert "`BASELINE_REQUIRED`: 25" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 5" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 1" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net" in ledger
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


def test_worker_story_baseline_history_remains_unchanged_after_batch():
    summary = _read(WORKER_STORY_PACK / "BASELINE_SUMMARY.md")
    benchmark = _read(WORKER_STORY_PACK / "BENCHMARK_BASELINE.md")

    assert "Benchmark result: 5 total, 4 passed, 1 failed" in summary
    assert "Failed benchmark: `worker-story-evidence-rich-answer`" in summary
    assert "synthesis/routing/answer-mode drift" in summary
    assert "Worker Story benchmark rerun: 5 total, 5 passed, 0 failed" in summary
    assert "Result status: `COMPLETED_WITH_FAILURES`" in benchmark


def test_annual_leave_remains_runbook_outstanding():
    ledger = _read(LEDGER_PATH)

    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | no | no | yes | no |" in ledger
    assert "RUNBOOK_OUTSTANDING | Retrieval, broad benchmark, golden-question, seed-corpus, regression artefacts and v0.4 runbook foundation exist" in ledger
    assert "no Annual Leave-specific corpus coverage diagnostic service/script or answer gap report service/script was found" in ledger
    assert "Adjacent leave-domain v0.4 diagnostics are not substitutes" in ledger
    assert "Domains with runbook outstanding: Annual Leave / Leave Management" in ledger
    assert not (BASELINE_ROOT / "annual_leave" / "v0_1").exists()


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
    ):
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative_path],
            capture_output=True,
            text=True,
            check=False,
        )
        assert tracked.returncode != 0

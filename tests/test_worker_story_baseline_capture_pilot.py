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

    assert "Worker Story Baseline-Capture Pilot v0.1" in summary
    assert "docs/WORKER_STORY_EVALUATION_RUNBOOK.md" in summary
    assert "docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md" in summary

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


def test_worker_story_baseline_pack_does_not_claim_runtime_truth_or_execution():
    combined = "\n".join(_read(PACK_PATH / file_name) for file_name in REQUIRED_FILES)

    assert "not operational truth" in combined
    assert "does not prove runtime platform truth" in combined
    assert "does not prove payroll/runtime truth" in combined
    assert "No benchmark pass/fail result is claimed by this file" in combined
    assert "No `STRONG`, `WEAK` or `MISSING` result is claimed by this file" in combined
    assert "No `GOOD`, `NEEDS_REFINEMENT` or `INSUFFICIENT_CORPUS` result is claimed by this file" in combined
    assert "called a live LLM" in combined
    assert "connected Code Evidence to answer generation" in combined


def test_worker_story_baseline_ledger_status_and_counts_are_consistent():
    ledger = _read(LEDGER_PATH)

    assert "| Worker Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Worker Story now has a checked-in baseline artefact pack" in ledger
    assert "`BASELINE_REQUIRED`: 29" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 1" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 1" in ledger
    assert "Domains with baseline already existing: Worker Story" in ledger


def test_worker_story_baseline_readme_pointer_exists():
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/evaluation/worker_story_baselines/" in readme
    assert "Worker Story baseline capture policy" in readme
    assert "comparison controls only" in readme

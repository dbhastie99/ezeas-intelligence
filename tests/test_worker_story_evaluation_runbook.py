from pathlib import Path


def test_worker_story_evaluation_runbook_exists_and_lists_required_commands():
    runbook_path = Path("docs/WORKER_STORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "run_golden_questions.py" in runbook
    assert "scan_worker_story_corpus_coverage.py" in runbook
    assert "build_worker_story_answer_gap_report.py" in runbook


def test_payroll_bases_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payroll_bases_and_totals.json" in runbook
    assert "scan_payroll_bases_corpus_coverage.py" in runbook
    assert "build_payroll_bases_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook


def test_payrun_admin_queue_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payrun_admin_queue.json" in runbook
    assert "scan_payrun_admin_queue_corpus_coverage.py" in runbook
    assert "build_payrun_admin_queue_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "queue cleanliness is not assurance" in runbook


def test_movement_review_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.movement_review.json" in runbook
    assert "scan_movement_review_corpus_coverage.py" in runbook
    assert "build_movement_review_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "variance is not automatic proof of error" in runbook
    assert "not every movement creates a fix action" in runbook


def test_comparison_remediation_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.comparison_remediation.json" in runbook
    assert "scan_comparison_remediation_corpus_coverage.py" in runbook
    assert "build_comparison_remediation_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "comparison evidence before variance" in runbook
    assert "actuals as external outcome truth" in runbook
    assert "comparator classification can be guessed" in runbook


def test_tax_payg_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/TAX_PAYG_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.tax_payg.json" in runbook
    assert "scan_tax_payg_corpus_coverage.py" in runbook
    assert "build_tax_payg_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Minerva does not calculate tax" in runbook
    assert "TaxStory" in runbook
    assert "unsupported frequencies must be explicit" in runbook
    assert "supplementary incremental PAYG" in runbook


def test_deductions_obligations_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/DEDUCTIONS_OBLIGATIONS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.deductions_obligations.json" in runbook
    assert "scan_deductions_obligations_corpus_coverage.py" in runbook
    assert "build_deductions_obligations_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "LibraryDeductionTemplate -> AccountDeductionTemplate -> ContactPayrollDeduction -> PayRunDeductionApplication" in runbook
    assert "PayRunDeductionApplication is event/outcome memory" in runbook
    assert "applicability before affordability" in runbook
    assert "obligations are durable balance-bearing recovery records" in runbook
    assert "reducing-balance recovery" in runbook
    assert "negative net pay is a governed policy outcome" in runbook

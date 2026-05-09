from pathlib import Path


def test_worker_story_evaluation_runbook_exists_and_lists_required_commands():
    runbook_path = Path("docs/WORKER_STORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "run_golden_questions.py" in runbook
    assert "scan_worker_story_corpus_coverage.py" in runbook
    assert "build_worker_story_answer_gap_report.py" in runbook

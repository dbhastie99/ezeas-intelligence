# Decision Story Benchmark Baseline

This file records the Decision Story benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.decision_story.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

Result status: `COMPLETED_WITH_FAILURES`

- Manifest: `samples\eval\rich_answer_benchmark.decision_story.json`
- Total: 7
- Passed: 6
- Failed: 1
- Failed case: `decision-story-rich-answer`
- Failure detail: Source snippets/matched phrases did not contain all expected terms: Decision Story, DecisionEvidenceIndex, why a treatment.
- Observed answer: directionally Decision Story-specific.
- Failure classification: benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap.
- Audit/chat rows created: false

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/DECISION_STORY_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.decision_story.json`
- Runner: `scripts\run_golden_questions.py`

## Diagnostic Interpretation

The failed benchmark case is preserved as captured. The failure is not classified as a corpus gap, and benchmark expectations were not weakened.

## Diagnostic-Only Guardrails

This benchmark baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not prove runtime platform truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform.

# Decision Story Benchmark Baseline

This file records that benchmark capture was blocked. It is diagnostic-only and not operational truth.

## Command Not Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.decision_story.json
```

Result status: `BLOCKED_DATABASE_CONNECTION`

The benchmark was not run because `scripts\check_worker_story_baseline_db_readiness.py` returned `DATABASE_CONNECTION_FAILED`.

- Total: not run
- Passed: not run
- Failed: not run
- Audit/chat rows created: false

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/DECISION_STORY_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.decision_story.json`
- Runner: `scripts\run_golden_questions.py`

## Diagnostic-Only Guardrails

This benchmark baseline does not mutate corpus, change routing, change answer generation, call live LLM, ingest operational JSON, connect Code Evidence, prove runtime platform truth, create DB schema or migrations, add endpoints or UI, or change workforce-platform.

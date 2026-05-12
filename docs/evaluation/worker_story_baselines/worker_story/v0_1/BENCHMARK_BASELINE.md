# Worker Story Benchmark Baseline

This file records the Worker Story benchmark baseline shape for comparison control. It is diagnostic-only and not operational truth.

## Command

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
```

## Scope

The benchmark scope is the Worker Story rich-answer manifest:

```text
samples/eval/rich_answer_benchmark.worker_story.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for Worker Story / Worker Calculation Story questions. It is not a live LLM review and does not prove runtime payroll correctness.

## Current Baseline Finding

The command was not executed as a baseline-capture command in this v0.1 slice. This file defines the checked-in benchmark baseline capture shape and must be populated by a future rerun if generated benchmark output is intentionally versioned.

No benchmark pass/fail result is claimed by this file.

## Source References

- Runbook: `docs/WORKER_STORY_EVALUATION_RUNBOOK.md`
- Manifest: `samples/eval/rich_answer_benchmark.worker_story.json`
- Runner: `scripts/run_golden_questions.py`

## Diagnostic-Only Guardrails

This benchmark baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.

# Worker Story Benchmark Baseline

This file records the Worker Story benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
```

Captured on 2026-05-12 from `C:\Projects\ezeas-intelligence`.

## Scope

The benchmark scope is the Worker Story rich-answer manifest:

```text
samples/eval/rich_answer_benchmark.worker_story.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for Worker Story / Worker Calculation Story questions. It is not a live LLM review and does not prove runtime payroll correctness.

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Total: 5
- Passed: 4
- Failed: 1
- Audit/chat rows created: false

Failed benchmark:

- Case: `worker-story-evidence-rich-answer`
- Question: "What is Worker Story and what evidence does it show?"
- Failure reason: answer did not contain all expected terms.
- Missing expected terms: Worker Story, platform evidence surface, source truth, calculated payroll outcome, current-effective payroll output, Decision Story, Rate Story, evidence, outstanding hardening.
- Observed issue: the answer drifted into Annual Leave wording for a Worker Story question.
- Classification: synthesis/routing/answer-mode drift, not corpus coverage gap.

Generated artefact committed: no.

## Post-Baseline Hardening Note v0.1

After Worker Story answer synthesis/routing drift hardening, the real DB-backed benchmark was rerun in the same environment after DB readiness returned `READY`.

Confirmed rerun result:

- DB readiness: `READY`.
- Worker Story benchmark: 5 total, 5 passed, 0 failed.
- Annual Leave regression benchmark: 1 total, 1 passed, 0 failed.
- Audit/chat rows created: false.
- The v0.3 failed case, `worker-story-evidence-rich-answer`, is considered addressed by synthesis/routing hardening.
- Corpus coverage remains interpreted as sufficient for this issue; the v0.3 failure is not treated as a corpus coverage gap.

This note records the post-baseline control result only. It does not overwrite the v0.3 baseline history above.

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
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.

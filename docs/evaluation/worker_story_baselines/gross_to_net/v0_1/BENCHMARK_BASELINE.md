# Gross-to-Net Benchmark Baseline

This file records the Gross-to-Net benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.gross_to_net.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Scope

The benchmark scope is the Gross-to-Net rich-answer manifest:

```text
samples/eval/rich_answer_benchmark.gross_to_net.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for Gross-to-Net questions. It is not a live LLM review and does not prove runtime payroll correctness.

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Total: 6
- Passed: 5
- Failed: 1
- Audit/chat rows created: false

Failed cases:

- `gross-to-net-current-effective-worker-story`
  - Question: How does Gross-to-Net relate to current-effective payroll output and Worker Story?
  - Failure: Answer did not contain all expected terms: current-effective payroll output truth, full run, targeted reprocess, Worker Story, calculated payroll outcome, line proof, amounts, deductions, net pay, superseded output, current truth, audit story.

Observed answer framing was directionally Gross-to-Net-specific, but the benchmark answer-term expectation failed for the current-effective Worker Story relationship case. Failure classification: benchmark answer-term expectation drift, not corpus gap. Corpus coverage was 10 STRONG, 0 WEAK, 0 MISSING.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md`
- Manifest: `samples/eval/rich_answer_benchmark.gross_to_net.json`
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

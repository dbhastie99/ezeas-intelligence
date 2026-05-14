# Comparison / Remediation Benchmark Baseline

This file records manually captured benchmark output for the Comparison / Remediation promoted baseline. It is diagnostic-only and not operational truth.

## Command

```powershell
python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.comparison_remediation.json
```

Captured on 2026-05-14 from `C:\Projects\ezeas-intelligence` after DB readiness returned `READY`.

## Scope

The benchmark scope is the Comparison / Remediation rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.comparison_remediation.json
```

The manifest covers Comparison / Remediation as governed payroll evidence and review/remediation context. It expects answers to preserve the three-lane comparison model, primary award path truth, imported actuals as external outcome truth, comparison policy, comparison run and line evidence, variance/top-up governance, position/classification mapping, Worker Story, Admin Queue, Movement Review, outstanding hardening and non-goals.

## Captured Result Summary

Result status: `PROMOTED_BASELINE_CAPTURED`

- Golden questions: Comparison / Remediation rich-answer benchmark
- Total: 9
- Passed: 9
- Failed: 0
- Audit/chat rows created: false

Benchmark result: completed with full pass.

Baseline pack state: captured evidence and promoted.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

Code Evidence answer integration: no.

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Boundary Expectations

The benchmark did not weaken expectations that:

- Comparison / Remediation is payroll evidence and review/remediation context, not generic diffing.
- The model includes primary calculated, comparator calculated, and actual imported / actuals lane.
- The primary award path remains operational payroll truth.
- Imported actuals are external outcome truth and must not be collapsed into calculated interpreter output.
- Variance/top-up is a governed consequence of comparison, not an invisible calculation side effect.
- Baseline capture does not implement runtime comparison/remediation behaviour.

## Source References

- Runbook: `docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.comparison_remediation.json`
- Runner: `scripts/run_golden_questions.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

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
- does not prove payroll/runtime truth;
- does not change workforce-platform.

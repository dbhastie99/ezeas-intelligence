# Contact Payroll History Benchmark Baseline

This file records the captured benchmark result for the Contact Payroll History baseline pack. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contact_payroll_history.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness result: `READY`.

## Scope

The benchmark scope is the Contact Payroll History rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.contact_payroll_history.json
```

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Total: 7
- Passed: 5
- Failed: 2
- Audit/chat rows created: false

Failed cases:

- `contact-payroll-history-rich-answer`
- `contact-payroll-history-retro-replay-correction`

Failure details:

1. `contact-payroll-history-rich-answer`: Answer did not contain all expected terms including Contact Payroll History, contact/worker-level historical payroll evidence surface, payroll outcomes, PayRun participation, current and historical payroll output, Gross-to-Net history, deductions, obligations, tax, payment readiness, leave/accrual evidence, Worker Story, Movement Review, Admin Queue, retro/replay/correction implications, status honesty, and guardrail terms.
2. `contact-payroll-history-retro-replay-correction`: Source snippets/matched phrases did not contain expected terms: historical payroll evidence, finalised truth preservation, attributed-period, paid-period.

Failure classification: combination of benchmark answer-term expectation gap and source-evidence/matched-phrase drift, with corpus gap present for `gross_to_net_history`. Do not classify this as purely a benchmark drift because corpus coverage has one MISSING group.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.contact_payroll_history.json`
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
- does not prove payroll/runtime truth.

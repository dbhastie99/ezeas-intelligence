# Imports / Actuals Answer Gap Report Baseline

This file records intentional answer gap report non-execution for the Imports / Actuals baseline pack. It is diagnostic-only and not operational truth.

## Commands Not Run

```powershell
.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --json --output .\artifacts\eval\imports_actuals_answer_gap_report.json
```

DB readiness returned `DATABASE_CONNECTION_FAILED`, so the answer gap report was not run.

## Scope

The Imports / Actuals answer gap report consumes the corpus coverage JSON and recommends whether each evidence group should be kept, refined or deferred for formal source evidence. Because corpus coverage did not run, no answer gap conclusion exists for this slice.

## Blocked Result Summary

Result status: `BLOCKED_DATABASE_CONNECTION`

- Domain: Imports / Actuals
- Report type: not evaluated
- Source coverage plan: not evaluated
- Overall status: not evaluated
- `KEEP`: not evaluated
- `IMPROVE_RETRIEVAL_TERMS`: not evaluated
- `IMPROVE_SYNTHESIS`: not evaluated
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: not evaluated
- Answer gap JSON generated: no
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Answer gap report: not run.

Baseline pack created: blocked pack only.

Final ledger status remains `BASELINE_REQUIRED`; this blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Boundary Expectations

When DB readiness returns `READY`, answer gap classification must preserve:

- imported actuals as evidence for reconciliation, not calculated payroll truth;
- source truth provenance and evidence preservation;
- imported timesheet truth and imported external/payroll-system results;
- source-to-payroll comparison and actual-versus-calculated reconciliation;
- validation and error-resolution workflow;
- award-specific import template expectations;
- shift assessment and shift attribute import expectations;
- claim and claim amount import expectations;
- rate type/pay code mapping context, tenant overrides and mapping snapshots;
- worker story explanation context.

## Source References

- Runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`
- Answer gap service: `app/services/imports_actuals_answer_gap_report_service.py`
- Answer gap script: `scripts\build_imports_actuals_answer_gap_report.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Interpretation

No answer gap conclusion exists for this slice. Imports / Actuals must remain blocked until DB readiness is `READY` and actual benchmark, coverage and gap results are captured.

## Diagnostic-Only Guardrails

This answer gap baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.

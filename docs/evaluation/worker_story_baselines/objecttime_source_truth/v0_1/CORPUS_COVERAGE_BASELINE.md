# ObjectTime / Source Truth Corpus Coverage Baseline

This file records intentional corpus coverage non-execution for the ObjectTime / Source Truth baseline pack. It is diagnostic-only and not operational truth.

## Commands Not Run

```powershell
.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py --json --output .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
```

DB readiness returned `DATABASE_CONNECTION_FAILED`, so the coverage diagnostic was not run.

## Scope

The ObjectTime / Source Truth corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage should preserve evidence for:

- ObjectTime;
- ObjectTimeAttribute;
- ObjectTimeAssessment;
- ObjectTimeAssessmentResponse;
- source truth;
- PayRun inclusion context;
- SourceTruth versus WorkedHours;
- raw span hours non-display;
- ObjectTime journey and why it did or did not calculate;
- RoundedStart boundary for WORK ObjectTime;
- source truth mutation;
- changed-field detection;
- previous value capture;
- new value capture;
- affected open or non-finalised scope;
- affected Finalised or protected scope;
- ordinary dirty boundary for open or non-finalised PayRunContacts;
- Finalised or protected dirty exclusion;
- finalised correction review pathway;
- dry-run source-change hook;
- guarded dry-run route wiring;
- `EnableFinalisedCorrectionObjectTimeHookDryRun`;
- `FinalisedCorrectionObjectTimeHookDryRunPreview`;
- `DRY_RUN_PREVIEW_ERROR`;
- redaction and payload guardrails;
- runtime intake readiness versus runtime intake implementation;
- no mutation guarantee;
- no intake creation guarantee;
- no dirty runtime call guarantee;
- no review request creation guarantee;
- no correction, retro, replay, supplementary, adjustment, payment, remittance or finalisation execution guarantee.

## Blocked Result Summary

Result status: `BLOCKED_DATABASE_CONNECTION`

- Domain: ObjectTime / Source Truth
- Plan id: not evaluated
- Evidence groups: not evaluated
- `STRONG`: not evaluated
- `WEAK`: not evaluated
- `MISSING`: not evaluated
- Coverage JSON generated: no
- Generated artefact committed: no
- Indexed corpus: not evaluated
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Corpus coverage result: not run.

Baseline pack created: blocked pack only.

Final ledger status remains `BASELINE_REQUIRED`; this blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Source References

- Runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/objecttime_source_truth_corpus_coverage_service.py`
- Coverage script: `scripts\scan_objecttime_source_truth_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Interpretation

No coverage conclusion exists for this slice. The next run must wait for readiness to be `READY` before running commands and must report ObjectTime / Source Truth evidence gaps from actual diagnostic output.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

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

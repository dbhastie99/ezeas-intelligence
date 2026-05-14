# ObjectTime / Source Truth Corpus Coverage Baseline

This file records manually captured corpus coverage output for the ObjectTime / Source Truth promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\scan_objecttime_source_truth_corpus_coverage.py
python scripts\scan_objecttime_source_truth_corpus_coverage.py --json --output .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
```

DB readiness returned `READY`, and the coverage diagnostic was captured from manual PowerShell output. Generated JSON remains a transient evaluation artefact and is not a committed baseline artefact.

## Scope

The ObjectTime / Source Truth corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for:

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

## Captured Result Summary

Result status: `PROMOTED_BASELINE_CAPTURED`

- Plan/domain: `OBJECTTIME_SOURCE_TRUTH` / ObjectTime / Source Truth
- Evidence groups: 12
- `STRONG`: 12
- `WEAK`: 0
- `MISSING`: 0
- Coverage JSON generated: yes, transient only
- Generated artefact committed: no
- Indexed corpus: 5 active documents, 4583 chunks
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Corpus coverage result: completed with all groups strong and no missing groups.

Baseline pack state: captured evidence and promoted.

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Coverage Groups

- STRONG `purpose_and_operator_meaning`
- STRONG `objecttime_as_source_evidence`
- STRONG `payrun_inclusion_and_source_truth`
- STRONG `imported_and_generated_source_rows`
- STRONG `source_truth_vs_worked_hours`
- STRONG `current_effective_output_connection`
- STRONG `worker_story_connection`
- STRONG `payroll_bases_and_leave_accrual_connection`
- STRONG `comparison_movement_and_replay_connection`
- STRONG `corrections_dirty_contacts_and_reprocessing`
- STRONG `evidence_provenance_and_audit`
- STRONG `outstanding_hardening`

The `outstanding_hardening` group matched 4 chunks across 2 documents. Representative matched terms were `guardrails`, `command-centre source hours cleanup` and `dependency detection`; the planned retrieval aliases also include guarded dry-run, readiness contract, source-change runtime intake readiness, runtime source-change hook, not implemented, not production enabled, finalised correction intake, review request creation, no correction execution, production enablement and non-goals.

## Source References

- Runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/objecttime_source_truth_corpus_coverage_service.py`
- Coverage script: `scripts\scan_objecttime_source_truth_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Interpretation

Coverage is no longer a promotion blocker. The earlier weak `outstanding_hardening` group was a retrieval-term gap, not a corpus gap.

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

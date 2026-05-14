# Imports / Actuals Corpus Coverage Baseline

This file records the manually captured corpus coverage result for the Imports / Actuals baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
python scripts\scan_imports_actuals_corpus_coverage.py
python scripts\scan_imports_actuals_corpus_coverage.py --json --output .\artifacts\eval\imports_actuals_corpus_coverage.json
```

## Scope

The Imports / Actuals corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for:

- import batch;
- import row;
- import validation;
- import error;
- import warning;
- import template;
- award-specific CSV template;
- timesheet import;
- payroll actuals import;
- external actuals;
- calculated versus actual;
- reconciliation;
- variance;
- pay code mapping;
- RateType mapping;
- tenant override mapping;
- mapping snapshot;
- shift assessment import;
- shift attribute import;
- claim import;
- Claimable;
- Claimable Hourly;
- Claim Amount;
- piece work / expense / mileage amount import context;
- evidence/provenance;
- source truth impact on PayRun outcomes;
- worker story explanation context;
- no runtime mutation guarantee.

## Captured Result Summary

Result status: `COMPLETED_WITH_CORPUS_GAPS`

- Plan/domain: `IMPORTS_ACTUALS` / Imports / Actuals
- Evidence groups: 12
- `STRONG`: 9
- `WEAK`: 1
- `MISSING`: 2
- Coverage JSON generated: yes
- Generated artefact committed: no
- Indexed corpus: 5 active documents, 4583 chunks
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Corpus coverage result: recaptured with real formal-corpus gaps.

Baseline pack state: recaptured result, not promoted.

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Evidence Groups

- `purpose_and_operator_meaning`: MISSING
- `imported_timesheet_source_truth`: STRONG
- `imported_payroll_actuals_lane`: STRONG
- `source_system_mapping_and_validation`: STRONG
- `pay_code_and_rate_type_mapping`: WEAK
- `position_classification_mapping`: STRONG
- `objecttime_and_source_truth_connection`: STRONG
- `comparison_and_remediation_connection`: STRONG
- `reconciliation_and_movement_review_connection`: STRONG
- `worker_story_and_admin_queue_connection`: STRONG
- `evidence_provenance_and_audit`: STRONG
- `outstanding_hardening`: MISSING

Important details:

- `purpose_and_operator_meaning` matched 0 chunks across 0 documents.
- `outstanding_hardening` matched 0 chunks across 0 documents.
- `pay_code_and_rate_type_mapping` matched 4 chunks across 1 document and is WEAK.
- `worker_story_and_admin_queue_connection` is STRONG, but the benchmark source-evidence check still failed for expected terms Worker Story, Admin Queue and mapping issues.
- `comparison_and_remediation_connection` is STRONG, but the benchmark answer still missed expected lane terms.

## Source References

- Runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/imports_actuals_corpus_coverage_service.py`
- Coverage script: `scripts\scan_imports_actuals_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`
- Transient JSON: `.\artifacts\eval\imports_actuals_corpus_coverage.json`

## Interpretation

Imports / Actuals has genuine formal-corpus gaps: 9 STRONG, 1 WEAK and 2 MISSING coverage groups. The missing groups mean this domain cannot be promoted solely through synthesis hardening unless formal source evidence is added or the coverage plan is legitimately revised with justification.

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

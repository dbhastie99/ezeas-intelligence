# Minerva Controlled Evaluation Batch Harness + Summary Model v0.1

## Durable Prompt / Control Artefact

Date: 2026-05-17

Slice: Minerva Controlled Evaluation Batch Harness + Summary Model v0.1

## Objective

Create and execute a deterministic local controlled evaluation batch harness and summary model for checked-in Minerva controlled evaluation report fixtures under `tests/fixtures/controlled_evaluation_reports`.

The harness must run supplied fixture payloads, supplied fixture file paths, or an explicitly supplied fixture directory through the existing deterministic Minerva controlled chain and return structured internal pass/fail metadata.

The summary model must convert batch results into deterministic internal controlled regression execution summary metadata for developer handoff, controlled evaluation summaries, golden baseline drift detection, and next-slice readiness reporting.

## Required Posture

This slice is local deterministic batch-evaluation, runbook, tests, and docs only.

It must not:

- enable internal chat exposure;
- enable public, production, tenant, or customer chat exposure;
- add or register an API route;
- call a live LLM;
- generate final natural-language answers;
- connect to a database;
- read from a database;
- write to a database;
- create migrations;
- mutate corpus;
- ingest Code Evidence;
- alter live retrieval backend behaviour;
- add credentials or connection strings;
- change workforce-platform;
- change ezeas-analytics;
- change UI;
- claim production readiness;
- claim deployment readiness;
- claim runtime readiness.

## Implementation Scope

Create or update:

- `app/services/controlled_evaluation_batch_harness_service.py`
- `app/services/controlled_evaluation_batch_summary_service.py`
- `tests/test_controlled_evaluation_batch_harness_service.py`
- `tests/test_controlled_evaluation_batch_summary_service.py`
- `docs/evaluation/controlled_evaluation_batch_harness_v0_1.md`
- `docs/evaluation/controlled_evaluation_batch_summary_model_v0_1.md`
- `docs/evaluation/minerva_controlled_regression_execution_phase_progress_v0_1.md`

## Batch Harness Requirements

The batch harness must return deterministic batch metadata including fixture counts, pass/fail counts, skipped count, all-passed status, fixture results, drift and safety failure categories, deterministic-output flag, controlled-summary safety flag, final-answer-generation safety flag, no-action attestation, and explanation.

Each fixture result must include fixture identity, fixture path, purpose, pass/fail status, expected and actual publication decisions, expected and actual controlled-report safety, expected and actual final-answer-generation safety, failures, preserved boundaries, and violated boundaries.

The harness must not scan arbitrary repo paths unless explicitly passed a fixture directory. It must not mutate fixture files and must not write generated reports.

## Summary Model Requirements

The summary model must convert a batch result into deterministic internal summary metadata including summary id, source batch id, phase name, progress before and after the slice, overall status, fixture counts, safety failures, drift failures, blocked claim failures, remaining work, recommended next slice, developer-handoff safety, final-answer-generation safety, no-action attestation, and explanation.

The summary is safe for developer handoff only when the batch passes and no-action/caveat boundaries are preserved. It is never safe for final answer generation.

## Phase Metadata

Record:

- current phase progress before slice: approximately 35%;
- expected phase progress after slice: approximately 70%;
- current phase: Controlled regression execution and internal evaluation summary readiness.

## Verification Plan

Run these commands using Windows PowerShell syntax:

```powershell
python -m pytest tests\test_controlled_evaluation_batch_harness_service.py tests\test_controlled_evaluation_batch_summary_service.py
python -m compileall app\services\controlled_evaluation_batch_harness_service.py app\services\controlled_evaluation_batch_summary_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Completion Criteria

This slice is complete when the batch harness, summary model, docs, and focused tests exist; focused verification passes; fixture files are not mutated; generated reports are not written; `.pytest_tmp` is absent; and the final response explicitly confirms no runtime, exposure, DB, corpus, Code Evidence, cross-repo runtime integration, deployment, production, live LLM, UI, route, migration, credential, or final answer generation action occurred.

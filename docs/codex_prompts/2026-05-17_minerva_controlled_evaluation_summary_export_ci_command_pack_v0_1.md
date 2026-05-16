# Minerva Controlled Evaluation Summary Export / CI Command Pack v0.1

## Control Artefact

Create and execute the local deterministic slice named Minerva Controlled Evaluation Summary Export / CI Command Pack v0.1.

## Context

This slice follows:

- Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1.
- Candidate Answer Readiness Classifier v0.1.
- Evaluation Output Publication Gate v0.1.
- Controlled Evaluation Report Assembler v0.1.
- Controlled Evaluation Report Fixture Pack / Golden Report Baselines v0.1.
- Controlled Evaluation Batch Harness + Summary Model v0.1.

The current phase is controlled regression execution and internal evaluation summary readiness.

Progress before this slice is approximately 70%. Expected progress after this slice is approximately 95%.

## Objective

Add a deterministic controlled summary export model and a PowerShell-only CI command pack for internal controlled evaluation regression checks.

## Required Outputs

- `app/services/controlled_evaluation_summary_export_service.py`
- `app/services/controlled_evaluation_ci_command_pack_service.py`
- `tests/test_controlled_evaluation_summary_export_service.py`
- `tests/test_controlled_evaluation_ci_command_pack_service.py`
- `docs/evaluation/controlled_evaluation_summary_export_v0_1.md`
- `docs/evaluation/controlled_evaluation_ci_command_pack_v0_1.md`
- `docs/evaluation/minerva_controlled_regression_execution_phase_closeout_readiness_v0_1.md`

## Required Behaviours

The summary export service must produce in-memory deterministic export metadata only. It must preserve source summary status, fixture counts, safety failures, drift failures, blocked claim failures, phase progress, remaining work, recommended next slice, no-action attestation, prohibited capability boundaries, caveats, and explanation.

The CI command pack service must produce deterministic PowerShell-only command metadata for focused controlled evaluation tests, golden baseline tests, relevant `py_compile` checks, `git diff --check`, and `.pytest_tmp` absence checks.

## Required Boundaries

This slice authorises local deterministic export/docs/tests only.

This slice does not authorise internal chat exposure, public chat exposure, production chat exposure, tenant chat exposure, customer chat exposure, API route registration, live LLM calls, final natural-language answer generation, DB connection, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, live retrieval backend changes, credentials, workforce-platform changes, ezeas-analytics changes, UI changes, production readiness, deployment readiness, or runtime readiness.

## Verification

Use Windows PowerShell syntax only:

- `python -m pytest tests\test_controlled_evaluation_summary_export_service.py tests\test_controlled_evaluation_ci_command_pack_service.py`
- `python -m py_compile app\services\controlled_evaluation_summary_export_service.py app\services\controlled_evaluation_ci_command_pack_service.py`
- `git diff --check`
- `if (Test-Path .pytest_tmp) { throw '.pytest_tmp exists' } else { Write-Output '.pytest_tmp absent' }`

## Final Response Requirements

Report files changed, export behaviour, CI command pack behaviour, progress before and after, no-action confirmation, exact tests run and results, warnings or limitations, and `git status --short`.

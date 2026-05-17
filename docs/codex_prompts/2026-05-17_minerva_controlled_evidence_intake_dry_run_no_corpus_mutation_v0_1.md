# Minerva Controlled Evidence Intake Dry-Run / No-Corpus-Mutation v0.1

## Purpose

Create and execute a durable control artefact for the Minerva controlled evidence intake dry-run slice.

## Slice

Controlled Evidence Intake Dry-Run / No-Corpus-Mutation v0.1.

## Context

This slice follows completion of:

- Controlled Regression Execution Phase Closeout Ledger v0.1.
- Controlled Corpus / Evidence Intake Planning Pack v0.1.
- Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1.
- Governed Evidence Intake Phase Closeout / Intake Runbook v0.1.

The governed evidence intake phase is complete at planning/readiness level only. Evidence ingestion, corpus mutation, Code Evidence ingestion, database access, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, runtime integration, deployment, and production readiness remain deferred.

## Objective

Add a deterministic controlled evidence intake dry-run layer that rehearses classification, gate evaluation, source-status boundary evaluation, caveat generation, no-action checks, and batch summary output using supplied metadata or checked-in controlled fixtures.

## Required Posture

This slice is local deterministic services, documentation, and tests only. It must not ingest evidence, mutate corpus, ingest Code Evidence, connect to a database, read from a database, write to a database, create migrations, call live retrieval, call a live LLM, generate final natural-language answers, expose chat, add or register API routes, change UI, change workforce-platform, change ezeas-analytics, or claim runtime, deployment, or production readiness.

## Implementation Instructions

Create:

- `app/services/controlled_evidence_intake_dry_run_service.py`
- `app/services/controlled_evidence_intake_dry_run_summary_service.py`
- `tests/test_controlled_evidence_intake_dry_run_service.py`
- `tests/test_controlled_evidence_intake_dry_run_summary_service.py`
- `docs/evaluation/controlled_evidence_intake_dry_run_no_corpus_mutation_v0_1.md`
- `docs/evaluation/controlled_evidence_intake_dry_run_summary_model_v0_1.md`
- `docs/evaluation/minerva_controlled_evidence_intake_dry_run_phase_progress_v0_1.md`

The dry-run service must accept supplied metadata or fixture payloads and return structured decisions including dry-run ID, evidence ID, category, planning gate decision, source status, dry-run decision, future-if-authorised eligibility, no-action flags, caveats, blocked reasons, prohibited inferences, no-action attestation, and explanation.

The summary service must aggregate dry-run outputs deterministically, count ready/review/blocked results, prove non-mutation across the batch, preserve caveats and no-action attestation, and recommend the next slice without authorising ingestion or corpus mutation.

## Required Decisions

- `DRY_RUN_READY_FOR_FUTURE_INTAKE`
- `DRY_RUN_NEEDS_SOURCE_CONTEXT`
- `DRY_RUN_NEEDS_STATUS_BOUNDARY`
- `DRY_RUN_NEEDS_TRUST_REVIEW`
- `DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`
- `DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM`
- `DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`
- `DRY_RUN_UNKNOWN_REQUIRES_REVIEW`

## Behavioural Requirements

- Complete known metadata that passes taxonomy, gate, and source-status checks can be ready for future intake.
- Ready-for-future-intake does not authorise ingestion now.
- Missing source context, missing status boundary, and unknown trust level produce their specific review decisions.
- Runtime, deployment, production, DB, live retrieval, live LLM, endpoint, chat, or final-answer overstatement is blocked.
- Unauthorised ingestion claims are blocked.
- Corpus mutation or Code Evidence ingestion claims are blocked.
- All performed flags are always `False` in normal dry-run service output.
- No-action attestation is preserved.
- Output is deterministic for repeated input.

## Verification

Run the focused tests for both new service areas, compile-check the new service files, run `git diff --check`, confirm `.pytest_tmp` is absent, and report `git status --short`.

## Execution Notes

All commands and verification notes must use Windows PowerShell syntax.

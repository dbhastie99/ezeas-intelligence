# Minerva Controlled Evidence Intake Dry-Run Fixture Execution / Review Pack v0.1

## Control Artefact

Create and execute a local deterministic slice for controlled evidence intake dry-run fixture execution and review-pack generation.

## Context

This slice continues after:

- Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1.
- Governed Evidence Intake Phase Closeout / Intake Runbook v0.1.
- Controlled Evidence Intake Dry-Run / No-Corpus-Mutation v0.1.

The current phase is controlled evidence intake dry-run / no-corpus-mutation. Progress before this slice is approximately 60-70%. Expected progress after this slice is approximately 90%.

## Objective

Add deterministic fixture execution and review-pack behavior over the checked-in controlled evidence intake fixtures. The output must record fixture counts, ready/review/blocked counts, non-mutation attestations, denial of ingestion and runtime actions, and the next review decision.

## Required Work

- Add `app/services/controlled_evidence_intake_fixture_execution_service.py`.
- Add `app/services/controlled_evidence_intake_review_pack_service.py`.
- Add focused tests for fixture execution and review pack behavior.
- Add evaluation docs for fixture execution, review pack, and phase progress.
- Run focused tests, compile checks, `git diff --check`, and confirm `.pytest_tmp` is absent.

## Guardrails

The slice is local deterministic service/docs/tests only. It must not call a live LLM, generate final natural-language answers, expose chat, add routes, connect to a DB, read or write a DB, create migrations, mutate corpus, ingest evidence, ingest Code Evidence, alter live retrieval, alter workforce-platform, alter ezeas-analytics, change UI, or claim production, deployment, or runtime readiness.

## Execution Notes

Use Windows PowerShell syntax for commands and verification notes. Keep outputs deterministic and sorted. Preserve no-action attestation in all execution and review-pack outputs.

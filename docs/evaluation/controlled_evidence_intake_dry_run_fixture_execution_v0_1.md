# Controlled Evidence Intake Dry-Run Fixture Execution v0.1

## Purpose

This document records the deterministic fixture execution layer for Minerva controlled evidence intake dry-runs. The layer runs checked-in fixture payloads through existing dry-run services and records reviewable metadata without ingesting evidence or mutating corpus.

## Scope

The scope is local deterministic service logic, documentation, and focused tests only.

## Current Phase

Controlled evidence intake dry-run / no-corpus-mutation.

## Current Estimated Progress Before Slice

Approximately 60-70% complete.

## Expected Progress After Slice

Approximately 90% complete, because checked-in fixture execution and review-pack behavior are now modeled, documented, and tested.

## Relationship to Golden Intake Fixtures

The executor accepts supplied fixture payloads or an explicitly supplied fixture directory. The checked-in fixtures under `tests/fixtures/controlled_evidence_intake` remain the golden baseline source for this slice.

## Relationship to Dry-Run Service

Each fixture is passed through `controlled_evidence_intake_dry_run_service.py`. The executor does not reclassify evidence independently; it aggregates dry-run decisions, compares expected outcomes, and records no-action flags.

## Fixture Execution Model

Fixture IDs are sorted deterministically. Execution output includes `execution_id`, fixture count, executed fixture IDs, per-fixture results, ready/review/blocked counts, prohibited action flags, `all_non_mutating`, no-action attestation, and explanation.

## Expected Outcome Model

Each fixture result records fixture purpose, category, dry-run decision, gate decision, source status, expected-outcome pass/fail, failures, required caveats, blocked reasons, and prohibited inferences. Expected outcomes are compared against checked-in fixture baseline fields.

## No-Corpus-Mutation Boundary

Normal fixture execution reports `corpus_mutation_performed_any` as `False` and `all_non_mutating` as `True`. Corpus mutation claims remain blocked or review-only according to the dry-run decision.

## No Evidence Ingestion Boundary

Fixture execution performs no evidence ingestion. `ingestion_performed_any` remains `False`.

## No Code Evidence Ingestion Boundary

Fixture execution performs no Code Evidence ingestion. `code_evidence_ingestion_performed_any` remains `False`.

## DB / Live Retrieval / LLM Boundary

Fixture execution performs no DB write, live retrieval, live LLM call, or final natural-language answer generation.

## Runtime / Deployment / Production Boundary

Fixture execution does not permit runtime, deployment, or production readiness claims and does not add routes, endpoints, chat exposure, or runtime integration.

## No-Action Attestation

No evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, route registration, runtime integration, deployment, or production action was performed or authorised by this dry-run.

## What This Slice Authorises

This slice authorises local deterministic fixture execution service behavior, documentation, and tests.

## What This Slice Does Not Authorise

This slice does not authorise evidence ingestion, corpus mutation, Code Evidence ingestion, DB access, DB reads, DB writes, migrations, live retrieval, live LLM calls, final answer generation, chat exposure, API endpoints, route registration, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## Recommended Next Slice

Controlled evidence intake review ledger / promotion criteria / no-corpus-mutation v0.1.

## Developer Handoff

Use `build_controlled_evidence_intake_fixture_execution` with explicit fixture payloads or an explicit fixture directory. Do not add implicit repository scanning or runtime integrations.

# Controlled Evidence Intake Dry-Run / No-Corpus-Mutation v0.1

## Purpose

This document records the deterministic Minerva controlled evidence intake dry-run slice. The slice rehearses how supplied evidence metadata or controlled fixtures would be classified, gated, status-boundary checked, caveated, and summarised without ingesting evidence or mutating corpus.

## Scope

The scope is local deterministic service logic, documentation, and focused tests only.

## Current Phase

Controlled evidence intake dry-run / no-corpus-mutation.

## Current Estimated Progress Before Slice

0% complete.

## Expected Progress After Slice

Approximately 60-70% complete, because this slice adds deterministic dry-run services, no-corpus-mutation output contracts, dry-run documentation, and focused tests using the existing governed evidence intake controls.

## Relationship to Evidence Intake Taxonomy

The dry-run first classifies metadata through the controlled evidence intake taxonomy. The taxonomy supplies evidence category, trust level, default caveats, and non-authorisation boundaries for ingestion, corpus mutation, runtime claims, and production claims.

## Relationship to Intake Planning Gate

The dry-run evaluates enriched metadata through the intake planning gate. A ready gate decision means future intake planning may proceed only if a later slice explicitly authorises ingestion. It does not authorise ingestion now.

## Relationship to Source-Status Boundary

The dry-run evaluates source status through the source-status boundary. Planning evidence does not prove implementation, analysis evidence does not prove repair, readiness evidence does not prove runtime enablement, and runtime, deployment, or production statuses still require explicit proof before claims are permitted.

## Dry-Run Decision Model

The dry-run decision model returns:

- `DRY_RUN_READY_FOR_FUTURE_INTAKE`
- `DRY_RUN_NEEDS_SOURCE_CONTEXT`
- `DRY_RUN_NEEDS_STATUS_BOUNDARY`
- `DRY_RUN_NEEDS_TRUST_REVIEW`
- `DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`
- `DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM`
- `DRY_RUN_BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`
- `DRY_RUN_UNKNOWN_REQUIRES_REVIEW`

## No-Corpus-Mutation Boundary

`corpus_mutation_performed` is always `False` in normal dry-run output. Corpus mutation claims are blocked and do not change corpus state.

## No Evidence Ingestion Boundary

`ingestion_performed` is always `False`. Ready-for-future-intake means only that metadata could be considered by a later authorised intake process.

## No Code Evidence Ingestion Boundary

`code_evidence_ingestion_performed` is always `False`. Code Evidence ingestion claims are blocked.

## DB / Live Retrieval / LLM Boundary

The dry-run does not connect to a database, read from a database, write to a database, create migrations, call live retrieval, call a live LLM, or generate final natural-language answers.

## Runtime / Deployment / Production Boundary

Runtime, deployment, production, endpoint, chat, and route-registration claims remain outside this slice. Runtime or production overstatement is blocked.

## No-Action Attestation

No evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, route registration, runtime integration, deployment, or production action was performed or authorised by this dry-run.

## What This Slice Authorises

This slice authorises local deterministic dry-run service code, dry-run summary service code, documentation, and focused tests.

## What This Slice Does Not Authorise

This slice does not authorise evidence ingestion, corpus mutation, Code Evidence ingestion, DB access, DB reads, DB writes, migrations, live retrieval, live LLM calls, final answer generation, chat exposure, endpoint exposure, route registration, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## Recommended Next Slice

The recommended next slice is a controlled evidence intake review ledger / no-corpus-mutation slice that records reviewed dry-run outcomes and promotion criteria without performing ingestion.

## Developer Handoff

Use `app/services/controlled_evidence_intake_dry_run_service.py` for single-item dry-run decisions and `app/services/controlled_evidence_intake_dry_run_summary_service.py` for deterministic batch summaries. Use the focused tests as the regression surface before changing any intake semantics.

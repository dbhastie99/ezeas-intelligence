# Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1

## Purpose

This document records the deterministic fixture and golden-baseline pack for Minerva controlled evidence intake planning. The pack gives future changes a stable regression surface for detecting drift, unsafe ingestion claims, missing caveats, source-status confusion, and accidental runtime, deployment, or production overstatement.

## Scope

This is a deterministic fixture/golden-baseline pack only. It adds checked-in JSON fixtures and focused tests for existing local services.

## Current Phase

Governed corpus / evidence intake planning.

## Current Estimated Progress Before Slice

Approximately 55-65% complete.

## Expected Progress After Slice

Approximately 85% complete, because the governed intake planning services now have checked-in golden fixtures and regression tests covering taxonomy, gate, and source-status boundaries.

## Relationship to Evidence Intake Taxonomy

The fixtures assert stable classification for Developer Log, Hardening Log, Platform Doctrine, Thread continuance prompt, Analytics readiness summary, Award recovery analysis, Workforce controlled-readiness document, Code Evidence planning output, Controlled evaluation summary, and unknown evidence requiring review.

## Relationship to Planning Gate

The fixtures assert that complete controlled metadata may be ready for future intake planning, but no fixture authorises ingestion or corpus mutation now. Unsafe runtime, production, ingestion, and corpus mutation claims are blocked. Incomplete or uncertain material remains review-gated.

## Relationship to Source-Status Boundary

The fixtures assert that evidence existence is not implementation truth. Planning evidence does not prove implementation, analysis evidence does not prove repair completion, readiness evidence does not prove runtime enablement, and runtime/deployment/production statuses still require explicit proof before claims are permitted.

## Fixture Categories

- Developer Log evidence.
- Hardening Log evidence.
- Platform Doctrine evidence.
- Thread continuance prompt evidence.
- Analytics readiness summary evidence.
- Award recovery analysis evidence.
- Workforce controlled-readiness document evidence.
- Code Evidence planning output.
- Controlled evaluation summary evidence.
- Unknown evidence requiring review.
- Runtime overstatement blocked.
- Production overstatement blocked.
- Unauthorised ingestion claim blocked.
- Corpus mutation claim blocked.
- Analysis evidence incorrectly claiming repair complete blocked or marked review.

## Golden Baseline Expectations

The golden baseline expects deterministic JSON fixtures, unique fixture IDs, deterministic service output, stable category classification, preserved no-action attestation, blocked unsafe claims, and explicit caveats/prohibited inferences for every fixture.

## Drift Risks Prevented

The pack prevents silent drift in category names, trust defaults, caveats, gate decisions, source-status interpretation, unknown-source handling, and deterministic IDs.

## Overstatement Risks Prevented

The pack prevents claims that planning evidence proves implementation, analysis evidence proves repair, readiness evidence proves runtime enablement, or any local fixture permits deployment, production, live LLM use, chat exposure, database access, workforce runtime integration, or analytics runtime integration.

## Ingestion Boundary

This is not an evidence ingestion slice. No fixture authorises evidence ingestion.

## Corpus Mutation Boundary

This is not a corpus mutation slice. No fixture authorises corpus mutation.

## Code Evidence Boundary

This is not a Code Evidence ingestion slice. Code Evidence planning output remains planning-only evidence and does not authorise Code Evidence ingestion.

## Runtime / Deployment / Production Boundary

This does not claim runtime readiness, deployment readiness, or production readiness. Runtime, deployment, and production claims remain blocked unless a future governed slice creates explicit proof and policy.

## DB / Live Retrieval / LLM Boundary

This does not connect to a database, query a database, write to a database, create migrations, alter live retrieval, call a live LLM, or generate final natural-language answers.

## Cross-Repo Runtime Boundary

This does not integrate workforce-platform or ezeas-analytics runtime behaviour. It changes no workforce-platform files and no ezeas-analytics files.

## What This Slice Authorises

This slice authorises local deterministic fixtures, documentation, and focused regression tests for the existing controlled evidence intake planning services.

## What This Slice Does Not Authorise

This slice does not authorise evidence ingestion, corpus mutation, Code Evidence ingestion, live retrieval, live LLM use, final answer generation, chat exposure, API endpoints, route registration, database reads, database writes, migrations, credentials, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, runtime readiness, deployment readiness, or production readiness.

## Recommended Next Slice

The recommended next slice is a controlled evidence intake review ledger that records reviewed fixture outcomes and defines the future promotion criteria for any governed intake implementation. That next slice should still avoid ingestion and corpus mutation unless explicitly authorised by a later control artefact.

## Developer Handoff

Use `tests/fixtures/controlled_evidence_intake/` as the checked-in golden fixture pack and `tests/test_controlled_evidence_intake_golden_baselines.py` as the focused regression surface. Any future change to taxonomy, planning gate, or source-status semantics should update fixtures and docs deliberately, with the no-action boundaries preserved unless a separately authorised slice changes them.


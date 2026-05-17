# Minerva Evidence Intake Runbook v0.1

## Purpose

Provide a deterministic runbook for future governed evidence intake work after the planning/readiness phase closeout.

## Intake Runbook Scope

This runbook describes future-authorisation gates only. It does not authorise evidence ingestion, corpus mutation, Code Evidence ingestion, DB access, live retrieval, live LLM use, answer generation, chat exposure, endpoint exposure, runtime integration, deployment, or production use.

## Preconditions Before Any Future Ingestion

A separate explicit ingestion slice must be approved. The slice must define source scope, status boundaries, allowed outputs, regression checks, no-corpus-mutation posture or mutation authority, and stop conditions.

## Evidence Classification Step

Classify candidate evidence with the controlled evidence taxonomy. Preserve category, source repo, source phase, trust level, status, and required caveats.

## Intake Planning Gate Step

Evaluate classified candidate evidence through the intake planning gate. A ready decision means future planning readiness only.

## Source-Status Boundary Step

Apply the source-status boundary before any future handling. Unknown, untrusted, mixed, or caveated material must remain review-only.

## Fixture/Baseline Regression Step

Run the golden intake fixture/baseline regression before trusting any later dry-run output or catalogue output.

## Required Caveats Step

Carry forward caveats that state planning-only status, no ingestion authority, no corpus mutation authority, no runtime authority, and no production/deployment/runtime readiness claim.

## Stop Conditions

- Unauthorised evidence ingestion claim.
- Unauthorised corpus mutation claim.
- Unauthorised Code Evidence ingestion claim.
- Unauthorised DB access, DB read, DB write, migration, credential, or connection string.
- Unauthorised live retrieval or live LLM claim.
- Unauthorised final natural-language answer generation claim.
- Unauthorised chat exposure, endpoint exposure, or route registration.
- Unauthorised workforce-platform or analytics runtime integration.
- Production, deployment, or runtime readiness overstatement.

## Evidence That Must Not Be Ingested Yet

No external evidence, internal evidence, developer log, hardening log, platform doctrine, analytics readiness summary, workforce-platform readiness document, award recovery analysis, thread continuance prompt, controlled evaluation summary, or Code Evidence may be ingested by this closeout.

## What Must Not Be Inferred

Do not infer runtime readiness, deployment readiness, production readiness, final answer safety, chat exposure approval, endpoint approval, DB availability, corpus mutation approval, live retrieval availability, or live LLM approval from this runbook.

## Developer Handoff

Choose the next phase deliberately and create a separate control artefact before proceeding. The recommended default is a controlled evidence intake dry-run with no corpus mutation if future intake exploration is required.

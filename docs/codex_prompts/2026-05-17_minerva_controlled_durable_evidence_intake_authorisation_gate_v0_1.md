# Minerva Controlled Durable Evidence Intake Authorisation Gate v0.1

## Purpose
This durable prompt/control artefact governs the Controlled Durable Evidence Intake Authorisation Gate v0.1 slice for ezeas-intelligence.

## Context
The durable evidence intake design phase is complete at design/readiness level only. Minerva remains controlled-readiness only. Durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB access, DB writes, live retrieval, live LLM use, final answer generation, chat exposure, runtime integration, deployment readiness, and production readiness remain deferred.

## Objective
Create a deterministic controlled durable evidence intake authorisation gate that determines whether supplied durable intake candidate metadata is eligible for a future, separate, explicitly authorised durable intake execution slice.

## Required Implementation
Create deterministic, side-effect-free services:

- `app/services/controlled_durable_evidence_intake_authorisation_gate_service.py`
- `app/services/controlled_durable_intake_candidate_eligibility_service.py`

Create focused tests:

- `tests/test_controlled_durable_evidence_intake_authorisation_gate_service.py`
- `tests/test_controlled_durable_intake_candidate_eligibility_service.py`

Create docs:

- `docs/evaluation/controlled_durable_evidence_intake_authorisation_gate_v0_1.md`
- `docs/evaluation/controlled_durable_intake_candidate_eligibility_v0_1.md`
- `docs/evaluation/minerva_durable_evidence_intake_authorisation_phase_progress_v0_1.md`
- `docs/evaluation/minerva_next_durable_intake_execution_decision_point_v0_1.md`

## Status Model
The authorisation gate must distinguish complete future-execution eligibility from missing source reference, source-status boundary, evidence envelope, audit envelope, reviewer confirmation, rollback policy, sensitive-data review, durable intake already performed claims, mutation or DB write claims, Code Evidence ingestion claims, live retrieval/LLM/final answer claims, runtime/deployment/production overstatement, and unknown review-required metadata.

The candidate eligibility service must distinguish complete candidate eligibility from unknown candidate type, missing prerequisites, prohibited runtime/production/mutation claims, and unknown review-required metadata.

## Non-Action Boundary
This slice must not perform or authorise durable intake now. It must not ingest evidence, mutate corpus, ingest Code Evidence, connect to or read from a database, write to a database, create migrations, call a live LLM, alter live retrieval, generate final natural-language answers, expose chat, add API routes, change UI, change workforce-platform, change ezeas-analytics, or claim runtime, deployment, or production readiness.

## Verification
Run focused tests for both new service areas, compile-check the new service files, run `git diff --check`, and confirm `.pytest_tmp` is absent using Windows PowerShell syntax.

## Execution Record
This artefact was created for the slice and executed locally as a deterministic docs/services/tests-only change.

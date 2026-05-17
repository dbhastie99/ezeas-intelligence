# Minerva Controlled Durable Intake First Candidate Execution Design / Review Pack v0.1

## Purpose
This durable prompt/control artefact governs the Controlled Durable Intake First Candidate Execution Design / Review Pack v0.1 slice for ezeas-intelligence.

## Context
The Controlled Durable Evidence Intake Design Phase Closeout v0.1 and Controlled Durable Evidence Intake Authorisation Gate v0.1 slices are complete. Minerva remains controlled-readiness only. Durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB access, DB writes, live retrieval, live LLM use, final answer generation, chat exposure, runtime integration, deployment readiness, and production readiness remain deferred.

## Objective
Create deterministic first-candidate durable-intake execution design metadata and deterministic review-pack metadata for a future execution slice, without performing or authorising durable intake now.

## Required Implementation
Create deterministic, side-effect-free services:

- `app/services/controlled_durable_intake_first_candidate_execution_design_service.py`
- `app/services/controlled_durable_intake_execution_review_pack_service.py`

Create focused tests:

- `tests/test_controlled_durable_intake_first_candidate_execution_design_service.py`
- `tests/test_controlled_durable_intake_execution_review_pack_service.py`

Create docs:

- `docs/evaluation/controlled_durable_intake_first_candidate_execution_design_v0_1.md`
- `docs/evaluation/controlled_durable_intake_execution_review_pack_v0_1.md`
- `docs/evaluation/minerva_durable_intake_execution_design_phase_progress_v0_1.md`

## Status Model
The execution design service must distinguish design-ready metadata from missing authorisation gate, missing candidate eligibility, missing reviewer confirmation, durable intake already performed claims, mutation or DB write claims, runtime or production overstatement, and unknown review-required metadata.

The review pack service must distinguish ready review-pack metadata from missing execution design, durable intake already performed claims, mutation or DB write claims, runtime or production overstatement, and unknown review-required metadata.

## Non-Action Boundary
This slice must not perform durable evidence intake, corpus mutation, Code Evidence ingestion, DB reads, DB writes, migrations, live retrieval, live LLM calls, final natural-language answer generation, chat exposure, API routes, UI changes, workforce-platform changes, ezeas-analytics changes, runtime integration, deployment readiness, or production readiness.

## Verification
Run focused tests for both new service areas, compile-check the new service files, run `git diff --check`, and confirm `.pytest_tmp` is absent using Windows PowerShell syntax.

## Execution Record
This artefact was created for the slice and executed locally as a deterministic docs/services/tests-only change.

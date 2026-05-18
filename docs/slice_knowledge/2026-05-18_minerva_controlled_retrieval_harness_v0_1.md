# Slice Knowledge Record - Minerva Controlled Retrieval Harness Over Durable Evidence Fixtures v0.1

## Purpose

This slice proves deterministic retrieval over existing durable evidence fixtures before any live LLM, chat, DB, corpus, or runtime exposure. It returns retrieval envelopes only and does not generate final answers.

## Product Objective

Give Minerva a controlled local way to identify relevant Developer Log durable evidence fixture records, explain why they matched, preserve source/status boundaries, and state the next safe step.

## User Story

As a Minerva operator, I need a deterministic fixture-only retrieval harness so I can inspect which controlled Developer Log evidence is relevant before authorising any answer preparation, exposure, runtime integration, or additional evidence-family onboarding.

## Source Truth

Source truth is existing controlled local durable Developer Log evidence fixtures and related retrieval-readiness metadata derived from existing controlled intake/source-status services.

## Current Platform Context

Minerva has completed the Developer Log durable evidence controlled-answer path at controlled-readiness level. The platform remains no-runtime, no-chat, no-live-LLM, no-DB, and no-final-answer for this slice.

## Why This Slice Exists Now

The work is pivoting from abstract governance to practical value-producing evidence paths. Before adding live retrieval, answer synthesis, or more source families, Minerva needs a deterministic proof that it can retrieve controlled Developer Log evidence and preserve boundaries.

## What This Slice Implements

- A fixture-only retrieval harness service for controlled Developer Log durable evidence.
- Deterministic keyword/metadata matching with stable ordering.
- Structured retrieval envelopes with query terms, fixture universe, in-scope/out-of-scope evidence types, matched results, boundary flags, caveats, and next step.
- Result-level source/status preservation, can-prove/cannot-prove boundaries, match reasons, ranks, and final-answer prohibition.
- Focused tests for positive retrieval, unsupported future evidence types, ordering, no-action flags, source/status preservation, and no final answer generation.

## What This Slice Explicitly Does Not Implement

This slice does not call a live LLM, generate final user-facing natural-language answers, expose or register a chat endpoint, add UI, connect to a DB, read from a DB, write to a DB, mutate live corpus, ingest Code Evidence, change retrieval backend, add vector or embedding search, change `workforce-platform`, change `ezeas-analytics`, change `award-configurator-v1`, add new evidence families beyond existing controlled Developer Log durable evidence fixtures, claim runtime readiness, or claim production readiness.

## Affected Tables / Models

None. No DB, schema, or migration changes.

## Affected Services

- `app/services/controlled_durable_evidence_retrieval_harness_service.py`

The service reuses existing controlled evidence dry-run and source/status boundary services to enrich fixture metadata.

## Affected API / Routes

None. No exposed endpoint or route registration.

## Affected UI

None.

## Affected Tests

- `tests/test_controlled_durable_evidence_retrieval_harness.py`

Related existing focused durable evidence path tests remain relevant for regression:

- `tests/test_controlled_durable_evidence_intake_authorisation_gate_service.py`
- `tests/test_controlled_durable_evidence_intake_closeout_readiness_service.py`
- `tests/test_controlled_durable_evidence_intake_phase_closeout_service.py`
- `tests/test_controlled_durable_intake_candidate_eligibility_service.py`
- `tests/test_controlled_durable_intake_first_candidate_execution_design_service.py`

## Evidence / Story Requirements

- QueryUnderstanding: normalize query terms deterministically.
- EvidenceUniverse: search only the controlled durable Developer Log fixture universe.
- Matches: return matched fixture evidence, matched terms, match reasons, rank, score, and preserved source labels.
- BoundaryResult: keep live LLM, final answer generation, chat exposure, DB read/write, corpus mutation, Code Evidence ingestion, backend change, runtime integration, and production readiness flags false.
- NextStep: review retrieval envelope and decide a later controlled-answer preparation slice.

## Irreversible Actions Prohibited

No corpus mutation, no durable ingestion, no Code Evidence ingestion, no DB writes, no schema changes, no runtime exposure, no endpoint registration, and no cross-repo changes.

## Payroll / Compliance Consequences

None directly. This is Minerva evidence retrieval only and must not affect payroll runtime.

## Security / Role / Tenant Consequences

No live data, no tenant data, no DB access, and no RBAC integration in this slice. Future live retrieval will require RBAC-before-retrieval.

## Analytics Consequences

None directly.

## Minerva Consequences

This becomes the first retrieval harness over controlled durable fixtures and the predecessor to adding Hardening Log, Platform Doctrine, and other controlled evidence types.

## Platform Doctrine Implications

- Prompt Is Not Knowledge Doctrine: the saved prompt records intent, but the implemented service/tests and checked-in knowledge artefact preserve durable slice knowledge.
- Slice Knowledge Preservation Doctrine: this record captures purpose, boundaries, verification, and follow-up slices.
- Retrieval Before Exposure Doctrine: retrieval contract quality is proven before chat, endpoint, runtime, or answer exposure.
- Source/Status Boundary Preservation Doctrine: retrieved evidence must preserve source type, source status, implementation status, answer-use status, caveats, and cannot-prove boundaries.

## Hardening Implications

- Do not add more evidence types before retrieval harness proves deterministic behaviour.
- Do not allow retrieval to imply final answer generation.
- Do not allow Developer Log evidence to imply runtime or production truth.

## Likely Gotchas

- The default fixture universe is intentionally narrow: Developer Log only.
- Hardening Log and Platform Doctrine query terms must not cause fabricated evidence.
- Strong matches do not permit final answers.
- Reading a local fixture file is not DB retrieval and must not be confused with runtime readiness.
- Developer Log planning evidence cannot prove implementation completion, runtime enablement, deployment, or production readiness.

## Acceptance Criteria

- Developer Log durable evidence queries return the controlled Developer Log fixture as an included/top result.
- Unsupported Hardening Log and Platform Doctrine queries return no invented evidence and clearly explain future evidence-family status.
- Every boundary flag remains false at envelope and result level.
- Result ordering is deterministic across repeated calls.
- Source type, title, source status, implementation status, and answer-use status are preserved where available.
- Output remains a retrieval envelope/story only, with no final answer generation.

## Verification Commands

- `python -m py_compile app/services/controlled_durable_evidence_retrieval_harness_service.py`
- `pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- `pytest tests/test_controlled_durable_evidence_intake_authorisation_gate_service.py tests/test_controlled_durable_evidence_intake_closeout_readiness_service.py tests/test_controlled_durable_evidence_intake_phase_closeout_service.py tests/test_controlled_durable_intake_candidate_eligibility_service.py tests/test_controlled_durable_intake_first_candidate_execution_design_service.py -q`
- `git diff --check`
- `Test-Path .pytest_tmp`

## Post-Implementation Review Notes

Placeholder for after Codex execution.

## Follow-Up Slices

- Hardening Log controlled evidence fixture onboarding
- Platform Doctrine controlled evidence fixture onboarding
- Thread Continuance Prompt evidence fixture onboarding
- Controlled answer preparation over retrieval harness results

## Current Status

Initial implementation slice.

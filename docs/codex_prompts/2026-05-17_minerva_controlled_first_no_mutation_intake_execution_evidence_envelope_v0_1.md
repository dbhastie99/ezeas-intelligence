# Minerva Controlled First No-Mutation Intake Execution / Evidence Envelope v0.1

## Purpose

Create and execute a deterministic local slice for controlled first no-mutation intake execution and evidence envelope preparation. This slice simulates a reviewed candidate through an in-memory, non-mutating path and prepares review-only evidence metadata.

## Scope

In scope:

- Create `app/services/controlled_first_no_mutation_intake_execution_service.py`.
- Create `app/services/controlled_no_mutation_intake_evidence_envelope_service.py`.
- Create execution, evidence envelope, and phase progress docs under `docs/evaluation/`.
- Add focused deterministic tests under `tests/`.
- Verify with Windows PowerShell commands.

Out of scope:

- Durable evidence ingestion, corpus mutation, or Code Evidence ingestion.
- DB connection, DB read, DB write, or migrations.
- Live retrieval backend changes.
- Live LLM calls.
- Final natural-language answer generation.
- Chat exposure, API endpoint, route registration, UI, runtime integration, workforce-platform, or ezeas-analytics changes.
- Production, deployment, or runtime readiness claims.

## Current Phase

Controlled first no-mutation intake execution / evidence envelope.

## Current Estimated Progress Before Slice

0% complete for the first no-mutation intake execution phase.

## Expected Progress After Slice

Approximately 55-65% complete.

## Required First No-Mutation Intake Execution Behaviour

The execution service must accept first-candidate review or authorisation metadata and produce deterministic in-memory execution metadata. Valid first-candidate review metadata produces `NO_MUTATION_INTAKE_EXECUTION_COMPLETED`.

The service must preserve that:

- The candidate is accepted only for no-mutation execution.
- In-memory execution can complete.
- Durable ingestion, corpus mutation, Code Evidence ingestion, DB access, DB write, live retrieval, live LLM use, and final answer generation are false.
- Missing or mismatched metadata requires review.
- Any durable ingestion, corpus mutation, runtime, deployment, or production claim is blocked.
- No-action attestation is preserved.
- Output is deterministic for repeated input.

## Required Evidence Envelope Behaviour

The evidence envelope service must accept no-mutation execution metadata and produce deterministic review-only evidence envelope metadata. Clean no-mutation execution produces `NO_MUTATION_EVIDENCE_ENVELOPE_READY`.

The service must preserve that:

- Future ingestion candidate status is metadata only.
- Durable ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, and final answer generation are not authorised.
- Required caveats preserve no-mutation and review-only status.
- The next decision point is explicit.
- Any mutation, ingestion, runtime, deployment, or production claim is blocked or marked review.
- Output is deterministic for repeated input.

## Verification

Run:

```powershell
pytest tests/test_controlled_first_no_mutation_intake_execution_service.py tests/test_controlled_no_mutation_intake_evidence_envelope_service.py
python -m py_compile app/services/controlled_first_no_mutation_intake_execution_service.py app/services/controlled_no_mutation_intake_evidence_envelope_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Execution Notes

This prompt authorises only local deterministic service, documentation, and test artefacts. It does not authorise ingestion, corpus mutation, Code Evidence ingestion, DB access, live retrieval, live LLM use, final natural-language answer generation, route registration, chat exposure, UI work, runtime integration, deployment, or production readiness.

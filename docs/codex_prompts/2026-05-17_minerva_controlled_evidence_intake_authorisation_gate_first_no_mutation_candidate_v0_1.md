# Minerva Controlled Evidence Intake Authorisation Gate / First No-Mutation Intake Candidate v0.1

## Purpose

Create and execute the controlled evidence intake authorisation slice after the completed dry-run phase. This slice selects eligibility for a future no-mutation intake candidate only. It does not perform intake, ingestion, mutation, DB work, retrieval, LLM use, final answer generation, runtime exposure, deployment, or production enablement.

## Scope

In scope:

- Create `app/services/controlled_evidence_intake_authorisation_gate_service.py`.
- Create `app/services/controlled_evidence_intake_first_candidate_service.py`.
- Create authorisation gate, first candidate, and phase progress docs under `docs/evaluation/`.
- Add focused deterministic tests under `tests/`.
- Verify using Windows PowerShell commands only.

Out of scope:

- Evidence ingestion.
- Corpus mutation.
- Code Evidence ingestion.
- DB connection, DB read, DB write, or migrations.
- Live retrieval backend changes.
- Live LLM calls.
- Final natural-language answer generation.
- Chat exposure, API endpoint, route registration, UI, runtime integration, workforce-platform, or ezeas-analytics changes.
- Production, deployment, or runtime readiness claims.

## Current Phase

Controlled evidence intake authorisation / first no-mutation candidate selection.

## Current Estimated Progress Before Slice

0% complete.

## Expected Progress After Slice

Approximately 55-65% complete.

## Required Authorisation Gate Behaviour

The gate must return structured metadata with deterministic decisions:

- `AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE`
- `NEEDS_SOURCE_CONTEXT`
- `NEEDS_STATUS_BOUNDARY`
- `NEEDS_TRUST_REVIEW`
- `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`
- `BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM`
- `BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM`
- `BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM`
- `UNKNOWN_REQUIRES_REVIEW`

It must preserve a no-action attestation, include prohibited inferences, and keep all current-action fields false.

## Required First Candidate Behaviour

The first candidate service must rank candidate options deterministically and recommend the safest future no-mutation intake candidate. Candidate types include:

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `ANALYTICS_READINESS_SUMMARY`
- `AWARD_RECOVERY_ANALYSIS`
- `CONTROLLED_EVALUATION_SUMMARY`
- `UNKNOWN_REQUIRES_REVIEW`

Structured controlled summaries rank above unknown or untrusted evidence. Unknown, incomplete, runtime/production, ingestion, corpus mutation, Code Evidence ingestion, DB, live retrieval, LLM, or final answer claims are rejected or sent to review.

## Verification

Run:

```powershell
pytest tests/test_controlled_evidence_intake_authorisation_gate_service.py tests/test_controlled_evidence_intake_first_candidate_service.py
python -m py_compile app/services/controlled_evidence_intake_authorisation_gate_service.py app/services/controlled_evidence_intake_first_candidate_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Execution Notes

This prompt was executed as a local deterministic service/docs/tests slice only. No ingestion, mutation, DB access, live retrieval, live LLM use, final answer generation, route registration, chat exposure, UI work, runtime integration, deployment, or production readiness claim is authorised by this artefact.

# Minerva Controlled Evidence Intake First Candidate Review / Authorisation Closeout v0.1

## Purpose

Create and execute a deterministic closeout slice for the controlled evidence intake authorisation phase. This slice reviews the first no-mutation candidate selection and records authorisation closeout metadata only.

## Scope

In scope:

- Create `app/services/controlled_evidence_intake_first_candidate_review_service.py`.
- Create `app/services/controlled_evidence_intake_authorisation_closeout_service.py`.
- Create first-candidate review, authorisation closeout, phase status, and next decision point docs under `docs/evaluation/`.
- Add focused deterministic tests under `tests/`.
- Verify with Windows PowerShell commands.

Out of scope:

- Evidence ingestion, corpus mutation, or Code Evidence ingestion.
- DB connection, DB read, DB write, or migrations.
- Live retrieval backend changes.
- Live LLM calls.
- Final natural-language answer generation.
- Chat exposure, API endpoint, route registration, UI, runtime integration, workforce-platform, or ezeas-analytics changes.
- Production, deployment, or runtime readiness claims.

## Current Phase

Controlled evidence intake authorisation / first no-mutation candidate review.

## Current Estimated Progress Before Slice

Approximately 55-65% complete.

## Expected Progress After Slice

Approximately 90-100% complete.

## Required First Candidate Review Behaviour

The review layer must accept first-candidate selection metadata and authorisation gate metadata, then return deterministic review metadata. A valid selected candidate with matching authorisation metadata produces `FIRST_CANDIDATE_REVIEW_READY`. Missing candidate metadata or mismatched selection/authorisation metadata requires human review. Any ingestion, corpus mutation, Code Evidence ingestion, runtime, deployment, or production claim is blocked.

The review must preserve that the candidate is eligible only for a future no-mutation intake attempt. It must not authorise intake now and must keep evidence ingestion, corpus mutation, Code Evidence ingestion, DB writes, live retrieval, live LLM use, and final answer generation false.

## Required Authorisation Closeout Behaviour

The closeout layer must accept first-candidate review metadata and return deterministic phase closeout metadata. A valid ready review produces `CONTROLLED_EVIDENCE_INTAKE_AUTHORISATION_CLOSEOUT_READY`.

The closeout must record:

- Progress before slice: approximately 55-65% complete.
- Expected progress after slice: approximately 90-100% complete.
- First candidate review complete.
- First candidate ready only for future no-mutation intake.
- Intake not authorised now.
- No evidence ingestion, corpus mutation, Code Evidence ingestion, DB access/write, live retrieval, live LLM use, final answer generation, chat/endpoint exposure, runtime integration, deployment readiness claim, production readiness claim, or runtime readiness claim.

## Verification

Run:

```powershell
pytest tests/test_controlled_evidence_intake_first_candidate_review_service.py tests/test_controlled_evidence_intake_authorisation_closeout_service.py
python -m py_compile app/services/controlled_evidence_intake_first_candidate_review_service.py app/services/controlled_evidence_intake_authorisation_closeout_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Execution Notes

This prompt was executed as a local deterministic service/docs/tests slice only. No ingestion, mutation, DB access, live retrieval, live LLM use, final natural-language answer generation, route registration, chat exposure, UI work, runtime integration, deployment, or production readiness claim is authorised by this artefact.

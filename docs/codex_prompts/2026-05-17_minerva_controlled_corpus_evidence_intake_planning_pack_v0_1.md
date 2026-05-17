# Minerva Controlled Corpus / Evidence Intake Planning Pack v0.1

## Purpose

Create and execute a deterministic planning pack for governed Minerva evidence intake before any ingestion is authorised.

## Scope

This slice is limited to local deterministic planning services, documentation, and focused tests. It classifies evidence metadata, gates future intake planning readiness, and preserves source-status boundaries.

## Current Phase

Governed corpus / evidence intake planning.

## Current Estimated Progress Before Slice

0%.

## Expected Progress After Slice

Approximately 55-65%.

## Required Outputs

- Add `app/services/controlled_evidence_intake_taxonomy_service.py`.
- Add `app/services/controlled_evidence_intake_planning_gate_service.py`.
- Add `app/services/evidence_source_status_boundary_service.py`.
- Add focused tests for all three service areas.
- Add governed evidence intake planning documentation under `docs/evaluation/`.

## Required Behaviour

- Classify controlled evidence metadata into deterministic categories.
- Require review for unknown or untrusted evidence metadata.
- Keep ingestion and corpus mutation unauthorised for every category and gate decision.
- Keep runtime, deployment, and production claims unauthorised unless a future explicit proof-bearing phase authorises them.
- Gate evidence as ready for future intake planning only when category, source context, source-status boundary, trust, and caveats are present.
- Block runtime/production overstatement and any claim that ingestion is already authorised.
- Preserve the distinction between evidence existence and implementation, runtime, deployment, or production truth.

## Prohibited Actions

- No internal chat exposure.
- No public, production, tenant, or customer chat exposure.
- No API route or endpoint registration.
- No live LLM call.
- No final natural-language answer generation.
- No database connection, read, write, or migration.
- No corpus mutation.
- No evidence ingestion.
- No Code Evidence ingestion.
- No live retrieval backend change.
- No workforce-platform change.
- No ezeas-analytics change.
- No UI change.
- No production, deployment, or runtime readiness claim.

## Verification

Run with Windows PowerShell syntax only:

```powershell
python -m pytest tests\test_controlled_evidence_intake_taxonomy_service.py tests\test_controlled_evidence_intake_planning_gate_service.py tests\test_evidence_source_status_boundary_service.py
python -m py_compile app\services\controlled_evidence_intake_taxonomy_service.py app\services\controlled_evidence_intake_planning_gate_service.py app\services\evidence_source_status_boundary_service.py
git diff --check
if (Test-Path .pytest_tmp) { throw '.pytest_tmp exists' } else { Write-Output '.pytest_tmp absent' }
git status --short
```

## Execution Notes

This artefact controls the slice. It records a planning-only phase and does not authorise runtime exposure, final answer generation, live retrieval, LLM use, database access, corpus mutation, evidence ingestion, Code Evidence ingestion, deployment, or production use.

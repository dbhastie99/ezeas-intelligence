# Minerva Controlled Durable Evidence Intake Design Verification / Closeout Readiness v0.1

## Objective

Create and execute a deterministic verification and closeout-readiness layer for Minerva durable evidence intake design while preserving the controlled-readiness-only posture.

## Context

This slice follows:

1. Controlled First No-Mutation Intake Execution Phase Closeout v0.1.
2. Controlled Durable Evidence Intake Design v0.1.

The previous slice added deterministic durable intake design, durable intake authorisation requirements, durable intake audit envelope docs, and tests. Durable evidence ingestion remains deferred and unauthorised.

## Current Phase

Controlled durable evidence intake design verification / closeout readiness.

Current estimated progress before this slice: approximately 55-65% complete.

Expected progress after this slice: approximately 85-90% complete.

## Required Work

Create deterministic, side-effect free services:

- `app/services/controlled_durable_evidence_intake_design_verification_service.py`
- `app/services/controlled_durable_evidence_intake_closeout_readiness_service.py`

Create docs:

- `docs/evaluation/controlled_durable_evidence_intake_design_verification_v0_1.md`
- `docs/evaluation/controlled_durable_evidence_intake_closeout_readiness_v0_1.md`
- `docs/evaluation/minerva_durable_evidence_intake_design_verification_phase_progress_v0_1.md`

Create tests:

- `tests/test_controlled_durable_evidence_intake_design_verification_service.py`
- `tests/test_controlled_durable_evidence_intake_closeout_readiness_service.py`

## Service Boundary

All work is local deterministic services/docs/tests only. This slice must not enable internal chat exposure, public chat exposure, production chat exposure, tenant chat exposure, customer chat exposure, API routes, route registration, live LLM calls, final natural-language answer generation, DB connections, DB reads, DB writes, migrations, corpus mutation, durable evidence ingestion, Code Evidence ingestion, live retrieval backend changes, workforce-platform changes, ezeas-analytics changes, UI changes, deployment-readiness claims, runtime-readiness claims, or production-readiness claims.

## Verification Service Behaviour

The verification service accepts durable intake design metadata, authorisation requirements metadata, and audit envelope metadata. It returns stable verification metadata covering design, authorisation requirements, audit envelope, storage boundary, mutation boundary, review boundary, rollback/removal requirement, sensitive-data review requirement, no-overstatement requirement, dry-run review requirement, blocked claims, caveats, findings, blocked reasons, no-action attestation, and explanation.

Complete design, requirements, and audit metadata produce `DURABLE_EVIDENCE_INTAKE_DESIGN_VERIFIED`. Missing design metadata produces `NEEDS_DESIGN_REVIEW`. Missing requirements metadata produces `NEEDS_AUTHORISATION_REQUIREMENTS_REVIEW`. Missing audit envelope metadata produces `NEEDS_AUDIT_ENVELOPE_REVIEW`. Durable ingestion claims and runtime/production overstatements remain blocked.

## Closeout Readiness Behaviour

The closeout readiness service accepts verification metadata and returns stable closeout-readiness metadata. Verified durable intake design produces `DURABLE_EVIDENCE_INTAKE_DESIGN_CLOSEOUT_READY`. Unverified design produces `NEEDS_VERIFICATION`.

Closeout readiness allows design-phase closeout only. It does not authorise durable intake, corpus mutation, DB writes, Code Evidence ingestion, live retrieval, live LLM use, final answer generation, runtime readiness, deployment readiness, or production readiness.

## Verification Commands

Use Windows PowerShell syntax only:

```powershell
pytest tests/test_controlled_durable_evidence_intake_design_verification_service.py tests/test_controlled_durable_evidence_intake_closeout_readiness_service.py
python -m py_compile app/services/controlled_durable_evidence_intake_design_verification_service.py app/services/controlled_durable_evidence_intake_closeout_readiness_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Output Requirements

Report files changed, durable evidence intake design verification behaviour, closeout readiness behaviour, progress before and after the slice, explicit no-action/no-durable-ingestion confirmation, exact verification commands and results, warnings or limitations, and current `git status --short`.

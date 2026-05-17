# Minerva Controlled Durable Evidence Intake Design v0.1

## Objective

Create a deterministic controlled durable evidence intake design layer for Minerva without performing durable ingestion, corpus mutation, DB access, DB writes, Code Evidence ingestion, live retrieval, live LLM use, route exposure, UI work, runtime integration, deployment-readiness claims, or production-readiness claims.

## Context

This slice follows completion of the governed evidence intake closeout, controlled dry-run closeout, first no-mutation candidate authorisation, first candidate review, first no-mutation execution, execution review, verification pack, and first no-mutation execution phase closeout.

The first no-mutation intake execution phase is complete at controlled-readiness level only. Durable evidence ingestion remains deferred and unauthorised.

## Current Phase

Controlled durable evidence intake design.

Current estimated progress before this slice: 0% complete.

Expected progress after this slice: approximately 55-65% complete.

## Required Work

Create deterministic, side-effect free services:

- `app/services/controlled_durable_evidence_intake_design_service.py`
- `app/services/controlled_durable_intake_authorisation_requirements_service.py`
- `app/services/controlled_durable_intake_audit_envelope_service.py`

Create docs:

- `docs/evaluation/controlled_durable_evidence_intake_design_v0_1.md`
- `docs/evaluation/controlled_durable_intake_authorisation_requirements_v0_1.md`
- `docs/evaluation/controlled_durable_intake_audit_envelope_v0_1.md`
- `docs/evaluation/minerva_durable_evidence_intake_design_phase_progress_v0_1.md`

Create tests:

- `tests/test_controlled_durable_evidence_intake_design_service.py`
- `tests/test_controlled_durable_intake_authorisation_requirements_service.py`
- `tests/test_controlled_durable_intake_audit_envelope_service.py`

## Service Boundary

All services are local deterministic design/docs/tests only. They must not ingest evidence, mutate corpus, write evidence records, connect to a database, read from a database, write to a database, create migrations, call live retrieval, call a live LLM, generate final natural-language answers, register routes, expose chat, change workforce-platform, change ezeas-analytics, change UI, or claim runtime, deployment, or production readiness.

## Behaviour Requirements

The design service defines future durable intake design readiness, storage boundary, mutation boundary, review boundary, rollback/removal policy requirement, caveats, no-action attestation, and blockers for durable-ingestion authorisation or runtime/production overstatement.

The authorisation requirements service defines prerequisites for a future durable intake authorisation, including reviewer confirmation, source-status boundary, evidence envelope, no-overstatement check, rollback policy, audit metadata, and dry-run review. It never authorises durable intake, corpus mutation, or DB writes.

The audit envelope service defines required audit fields before future durable intake, including source reference, source status, reviewer, decision timestamp, no-mutation history, rollback policy, prohibited-claims check, and sensitive-data review. It never records durable intake, corpus mutation, or DB writes as performed.

## Verification Commands

Use Windows PowerShell syntax only:

```powershell
pytest tests/test_controlled_durable_evidence_intake_design_service.py tests/test_controlled_durable_intake_authorisation_requirements_service.py tests/test_controlled_durable_intake_audit_envelope_service.py
python -m py_compile app/services/controlled_durable_evidence_intake_design_service.py app/services/controlled_durable_intake_authorisation_requirements_service.py app/services/controlled_durable_intake_audit_envelope_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Output Requirements

Report files changed, design behaviour, authorisation requirements behaviour, audit envelope behaviour, progress before and after the slice, explicit no-action/no-durable-ingestion confirmation, exact verification commands and results, warnings or limitations, and current `git status --short`.

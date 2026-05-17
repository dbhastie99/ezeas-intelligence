# Minerva Controlled Evidence Intake Dry-Run Phase Closeout / No-Mutation Ledger v0.1

## Purpose

Create and execute a deterministic closeout slice for the controlled evidence intake dry-run phase. The slice records that the phase is complete at controlled-readiness level only, preserves a no-mutation ledger, and requires an explicit next-phase decision before any further capability is authorised.

## Scope

This prompt controls local deterministic service, documentation, and test work only.

In scope:

- Create `app/services/controlled_evidence_intake_dry_run_closeout_service.py`.
- Create the controlled dry-run closeout ledger, no-mutation ledger, phase status, and next decision point documents under `docs/evaluation/`.
- Add focused tests in `tests/test_controlled_evidence_intake_dry_run_closeout_service.py`.
- Verify using Windows PowerShell commands only.

Out of scope:

- Evidence ingestion.
- Corpus mutation.
- Code Evidence ingestion.
- DB connection, DB read, DB write, or migrations.
- Live retrieval backend changes.
- Live LLM calls.
- Final natural-language answer generation.
- Chat exposure, endpoint exposure, route registration, UI changes, or runtime integration.
- Workforce-platform or ezeas-analytics changes.
- Production, deployment, or runtime readiness claims.

## Required Closeout Behaviour

The closeout service must return deterministic metadata with:

- `CONTROLLED_EVIDENCE_INTAKE_DRY_RUN_COMPLETE` for complete non-mutating closeout inputs.
- `NEEDS_REVIEW` for incomplete or non-canonical closeout inputs.
- `BLOCKED_MUTATION_OR_INGESTION_CLAIM` for ingestion, corpus mutation, or Code Evidence ingestion claims.
- `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT` for DB, live retrieval, live LLM, runtime integration, deployment, production, or runtime readiness claims.
- `BLOCKED_EXPOSURE_OR_FINAL_ANSWER_CLAIM` for chat exposure, endpoint exposure, route registration, or final answer generation claims.

The output must record approximately 90% progress before the slice and 100% progress after the slice. Completed components must include the dry-run service, dry-run summary service, fixture execution service, review pack service, golden intake fixtures, taxonomy, planning gate, and source-status boundary. Remaining work must be limited to choosing the next phase.

## Required No-Mutation Ledger

The ledger must explicitly show false or not-authorised state for:

- Evidence ingestion.
- Corpus mutation.
- Code Evidence ingestion.
- DB access and DB writes.
- Live retrieval.
- Live LLM use.
- Final answer generation.
- Chat exposure.
- Endpoint exposure.
- Workforce runtime integration.
- Analytics runtime integration.
- Production readiness claims.
- Deployment readiness claims.
- Runtime readiness claims.

## Required Documentation

Create:

- `docs/evaluation/controlled_evidence_intake_dry_run_closeout_ledger_v0_1.md`
- `docs/evaluation/controlled_evidence_intake_no_mutation_ledger_v0_1.md`
- `docs/evaluation/minerva_controlled_evidence_intake_dry_run_phase_status_v0_1.md`
- `docs/evaluation/minerva_next_controlled_evidence_intake_decision_point_v0_1.md`

## Verification

Run:

```powershell
pytest tests/test_controlled_evidence_intake_dry_run_closeout_service.py
python -m py_compile app/services/controlled_evidence_intake_dry_run_closeout_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

The final response must include files changed, behaviour implemented, progress recorded, no-action confirmation, exact tests and results, warnings or limitations, and current `git status --short`.

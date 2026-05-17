# Minerva Governed Evidence Intake Phase Closeout / Intake Runbook v0.1

## Objective

Create and execute a deterministic closeout/runbook slice for the Minerva governed evidence intake phase. The phase closes at planning/readiness level only, moving estimated progress from approximately 85% to 100% for governed evidence intake planning.

## Starting Context

The repo is expected to be clean before this slice. Prior completed slices are Controlled Regression Execution Phase Closeout Ledger v0.1, Controlled Corpus / Evidence Intake Planning Pack v0.1, and Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1.

## Required Posture

Work is local deterministic service/docs/tests only. Do not enable chat exposure, add or register an API route, call a live LLM, generate final natural-language answers, connect to or read/write a database, create migrations, mutate corpus state, ingest evidence, ingest Code Evidence, alter live retrieval backend behaviour, add credentials, change workforce-platform, change ezeas-analytics, change UI, or claim production/deployment/runtime readiness.

## Implementation Targets

- Add `app/services/governed_evidence_intake_closeout_service.py`.
- Add `tests/test_governed_evidence_intake_closeout_service.py`.
- Add `docs/evaluation/minerva_governed_evidence_intake_closeout_ledger_v0_1.md`.
- Add `docs/evaluation/minerva_governed_evidence_intake_phase_status_v0_1.md`.
- Add `docs/evaluation/minerva_evidence_intake_runbook_v0_1.md`.
- Add `docs/evaluation/minerva_next_evidence_phase_decision_point_v0_1.md`.

## Required Behaviour

The service must return deterministic closeout/runbook metadata with progress before slice recorded as approximately 85% and progress after slice recorded as 100%. Complete inputs must produce `GOVERNED_EVIDENCE_INTAKE_PHASE_COMPLETE`. Any input claiming evidence ingestion, corpus mutation, Code Evidence ingestion, DB access/writes, live retrieval, live LLM, final answer generation, chat or endpoint exposure, runtime integration, or production/deployment/runtime readiness must produce a blocked or review status.

## Verification

Run PowerShell commands only:

```powershell
python -m pytest tests/test_governed_evidence_intake_closeout_service.py
python -m py_compile app/services/governed_evidence_intake_closeout_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

## Closeout Notes

This artefact is the durable control prompt for the slice. It authorises only the local deterministic closeout/runbook service, docs, and tests described above.

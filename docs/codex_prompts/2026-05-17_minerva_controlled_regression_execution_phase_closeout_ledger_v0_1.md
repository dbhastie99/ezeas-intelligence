# Minerva Controlled Regression Execution Phase Closeout Ledger v0.1

## Purpose

Create and execute a deterministic closeout ledger for the Minerva controlled regression execution phase.

## Scope

This slice is limited to local deterministic service, documentation, and tests. It records completion at controlled-readiness level only.

## Required Outputs

- Add `app/services/controlled_regression_execution_closeout_service.py`.
- Add `tests/test_controlled_regression_execution_closeout_service.py`.
- Add `docs/evaluation/minerva_controlled_regression_execution_closeout_ledger_v0_1.md`.
- Add `docs/evaluation/minerva_controlled_regression_execution_phase_status_v0_1.md`.
- Add `docs/evaluation/minerva_next_phase_decision_point_v0_1.md`.

## Required Behaviour

- Preserve progress before slice as `95%`.
- Preserve progress after slice as `100%`.
- Mark complete controlled regression inputs as `CONTROLLED_REGRESSION_EXECUTION_COMPLETE`.
- Include status guard, candidate answer classifier, publication gate, controlled evaluation report assembler, golden baselines, batch harness, batch summary model, summary export, and CI command pack as completed components.
- Limit remaining work to choosing the next phase.
- Keep next phase options explicit and deterministic.
- Preserve no-action attestation.
- Ensure output is deterministic for repeated input.
- Block or mark for review any overstated runtime, production, exposure, final answer generation, live LLM, DB, corpus, Code Evidence, workforce-platform, analytics, deployment, endpoint, route, or cross-repo runtime claim.

## Prohibited Actions

- No live LLM calls.
- No final natural-language answer generation.
- No chat exposure.
- No API endpoint or route registration.
- No DB connection, reads, writes, or migrations.
- No corpus mutation.
- No Code Evidence ingestion.
- No live retrieval backend changes.
- No workforce-platform changes.
- No ezeas-analytics changes.
- No UI changes.
- No production, deployment, or runtime readiness claim.

## Verification

Run with Windows PowerShell syntax only:

```powershell
python -m pytest tests\test_controlled_regression_execution_closeout_service.py
python -m py_compile app\services\controlled_regression_execution_closeout_service.py
git diff --check
if (Test-Path .pytest_tmp) { throw '.pytest_tmp exists' } else { Write-Output '.pytest_tmp absent' }
git status --short
```

## Execution Notes

This artefact is durable control metadata for the slice. It does not authorise runtime, chat, LLM, DB, corpus, Code Evidence, cross-repo, deployment, production, or final-answer-generation behaviour.

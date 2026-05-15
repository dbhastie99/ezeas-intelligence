# Minerva Formal Evidence Current State Summary v0.1 Prompt

Date: 15 May 2026

## Slice

Minerva Formal Evidence Current State Summary v0.1.

## Objective

Create a concise, operator-facing current-state summary for the Minerva formal evidence control model and focused tests that preserve the current blocked state.

## Required Summary

Create:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY_2026_05_15.md`

The summary must reference these as the places to start for the full control model:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md`

## Current State To Preserve

Include a current controlled-domain table showing:

| Domain | Baseline status | Review status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Promotion execution permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |

The summary must preserve:

- Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Minerva may explain Tax / PAYG but must not calculate PAYG withholding.
- Imports / Actuals is not merely file upload or CSV parsing.

## Boundaries

State that no review approval, governed ingestion, corpus mutation, recapture, benchmark run, corpus coverage run, answer-gap run, promotion, ledger update, runtime change, endpoint change, UI change, workforce-platform change, or award-configurator-v1 change occurred in the formal evidence control-model work.

Do not change ledger counts. Do not mark any domain `REVIEWED_READY_FOR_INGESTION`. Do not mark any domain `BASELINE_ALREADY_EXISTS`. Do not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Next Allowed Actions

Include a next-allowed-actions section stating that future work may:

- assign a reviewer
- perform an explicit review slice
- create `NEEDS_REVISION` or `REVIEWED_READY_FOR_INGESTION` decision records
- plan governed ingestion only after review readiness

State that future work must not skip gates.

## Blocked Actions

Include a blocked-actions section stating that corpus ingestion, recapture, promotion, and ledger changes remain blocked for both domains.

## Tests

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions that:

- the summary exists
- the prompt exists
- the summary references the control index and closeout
- the summary includes the current controlled-domain table
- Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED` and `NOT_REVIEWED`
- ingestion, recapture, promotion, and promotion execution are No
- the no-runtime, no-corpus, and no-ledger-change boundaries are present
- next allowed actions and blocked actions are present
- the summary does not claim governed ingestion, recapture, promotion, or ledger promotion occurred
- the summary does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, summary created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message:

```text
minerva-formal-evidence-current-state-summary-v01
```

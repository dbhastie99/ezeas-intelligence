# Minerva Formal Evidence Control Model Index Closeout Link v0.1 Prompt

Date: 15 May 2026

## Slice

Minerva Formal Evidence Control Model Index Closeout Link v0.1.

## Objective

Update the master formal evidence control index so it references the durable closeout/state summary for the formal evidence control model created on 15 May 2026.

## Required Index Change

Update:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`

The index must reference:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md`

Keep the change concise and navigational. Do not duplicate the full closeout.

The index must explain that future Minerva/Codex work should start at the control index and use the closeout to understand what was created, why it exists, what remains blocked, and what future slices are allowed or forbidden to do.

## Current State To Preserve

- Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.
- Promotion execution permitted: No.

## Boundaries

Do not change ledger counts. Do not mark any domain `REVIEWED_READY_FOR_INGESTION`. Do not mark any domain `BASELINE_ALREADY_EXISTS`.

Do not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Tests

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions that:

- `FORMAL_EVIDENCE_CONTROL_INDEX.md` references `FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md`
- the index describes that closeout as a closeout/state summary
- the index preserves Tax / PAYG and Imports / Actuals as `BASELINE_REQUIRED` and `NOT_REVIEWED`
- the index preserves governed ingestion, recapture, promotion, and promotion execution as not permitted

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, index updated, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message:

```text
minerva-formal-evidence-control-model-index-closeout-link-v01
```

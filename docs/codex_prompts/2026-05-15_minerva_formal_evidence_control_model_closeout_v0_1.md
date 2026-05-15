# Minerva Formal Evidence Control Model Closeout v0.1 Prompt

Date: 15 May 2026

## Slice

Minerva Formal Evidence Control Model Closeout v0.1.

## Objective

Create a durable closeout artefact for the Minerva formal evidence control model and focused tests that preserve the current blocked state.

## Required Closeout

Create:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md`

The closeout must summarise the formal evidence control model created for Minerva knowledge maintenance, including:

- master `FORMAL_EVIDENCE_CONTROL_INDEX.md`
- source-evidence README link
- root README link
- review-gate index
- decision-record template
- decision-record index
- review readiness checklist
- status transition runbook
- governed ingestion planning runbook
- recapture planning runbook
- promotion planning runbook
- promotion execution guardrail
- Tax / PAYG `NOT_REVIEWED` decision record
- Imports / Actuals `NOT_REVIEWED` decision record

The closeout must explain that the purpose of the model is to stop relying on brittle chat history or copied Word documents and instead preserve prompts, decisions, evidence controls, gates, and review state in the repository.

## Current State To Preserve

- Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.
- Promotion execution permitted: No.

## Boundaries

State that no corpus mutation, Code Evidence integration, live LLM call, benchmark recapture, corpus coverage run, answer-gap run, runtime change, UI change, endpoint change, workforce-platform change, award-configurator-v1 change, review approval, governed ingestion, recapture, promotion, or ledger update occurred.

Do not change ledger counts. Do not mark any domain `REVIEWED_READY_FOR_INGESTION`. Do not mark any domain `BASELINE_ALREADY_EXISTS`. Do not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Operator Guidance

Include an operator guidance section explaining that future Codex/Minerva slices should begin at `FORMAL_EVIDENCE_CONTROL_INDEX.md` and preserve prompt files under `docs/codex_prompts`.

## Still To Do

Include a still-to-do section stating that Tax / PAYG and Imports / Actuals remain blocked until explicit review, possible `REVIEWED_READY_FOR_INGESTION` transition, governed ingestion, recapture, and possible promotion are performed in separate future slices.

## Tests

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions that:

- the closeout exists
- the closeout references all major control artefacts
- the closeout preserves current blocked states for Tax / PAYG and Imports / Actuals
- the closeout states the no-runtime, no-corpus, and no-promotion boundaries
- the closeout states the repo-preserved prompt and artefact model
- the closeout does not state that governed ingestion has occurred, recapture has occurred, promotion has occurred, ledger has been promoted, Tax / PAYG is `BASELINE_ALREADY_EXISTS`, or Imports / Actuals is `BASELINE_ALREADY_EXISTS`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, closeout created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message:

```text
minerva-formal-evidence-control-model-closeout-v01
```

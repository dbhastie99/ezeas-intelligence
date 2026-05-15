# Codex Prompt - Minerva Formal Evidence Control Index README Link v0.1

Date: 15 May 2026

Mode: Documentation/navigation hardening only

## Objective

Update the most appropriate existing README/navigation file so future Minerva and Codex work can discover `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md` as the master starting point/control index for the formal evidence control model.

The README update must be concise. It must not duplicate the full control model.

## Required README Navigation

The README/navigation text must state that `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md` is the master starting point/control index for:

- review gates
- decision records
- readiness checklists
- status transitions
- governed ingestion planning
- recapture planning
- promotion planning
- promotion execution guardrails

## Required Current State Preservation

The slice must preserve Tax / PAYG and Imports / Actuals as:

- baseline status: `BASELINE_REQUIRED`
- decision status: `NOT_REVIEWED`
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No

## Explicit Non-Goals

Do not change ledger counts.

Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.

Do not mark any domain `BASELINE_ALREADY_EXISTS`.

Do not implement:

- DB writes
- migrations
- corpus mutation
- Code Evidence integration
- live LLM calls
- endpoint changes
- UI changes
- workforce-platform changes
- award-configurator-v1 changes
- runtime changes
- review approval
- governed ingestion
- recapture
- benchmark execution
- corpus coverage execution
- answer-gap execution
- promotion
- ledger update

Do not create generated benchmark, corpus coverage, answer-gap, or evaluation artefacts.

## Required Tests

Update `tests/test_domain_baseline_capture_batch.py` or an appropriate existing README/navigation test to assert that the relevant README:

- references `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`
- describes it as the master starting point/control index
- names the control areas without duplicating the full model
- preserves Tax / PAYG and Imports / Actuals as blocked while they remain `BASELINE_REQUIRED` and `NOT_REVIEWED`

Also assert that this prompt file is preserved.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report:

- files changed
- README/navigation updated
- tests run
- `.pytest_tmp` status
- confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes

Suggested commit message: `minerva-formal-evidence-control-index-readme-link-v01`

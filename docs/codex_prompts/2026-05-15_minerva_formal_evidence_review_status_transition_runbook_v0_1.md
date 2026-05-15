# Codex Prompt - Minerva Formal Evidence Review Status Transition Runbook v0.1

Date: 15 May 2026

Mode: Documentation/control-runbook hardening only

## Objective

Create `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md` as the controlled process for changing a formal evidence review decision from `NOT_REVIEWED` to one of:

- `NEEDS_REVISION`
- `REVIEWED_READY_FOR_INGESTION`
- `SUPERSEDED`

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions covering the new runbook and this durable prompt/control artefact.

## Required References

The runbook must reference:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

## Required Runbook Controls

The runbook must state that a status transition requires:

- a separate explicit review slice
- a filled decision record
- reviewer identity
- review date
- reviewer rationale
- doctrine review
- implementation-state review
- evidence-gap review
- non-overclaiming review

The runbook must define `NOT_REVIEWED`, `NEEDS_REVISION`, `REVIEWED_READY_FOR_INGESTION`, and `SUPERSEDED`.

The runbook must state that `REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only, and does not mutate corpus, run recapture, promote a baseline, change runtime behaviour, or change ledger counts.

The runbook must state that `NEEDS_REVISION` blocks governed ingestion and requires follow-up changes before review can proceed.

The runbook must state that `SUPERSEDED` blocks governed ingestion and requires the superseded draft/gate/decision record not be used.

The runbook must preserve Tax / PAYG and Imports / Actuals as:

- baseline status: `BASELINE_REQUIRED`
- decision status: `NOT_REVIEWED`
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No

The runbook must preserve that Minerva may explain Tax / PAYG but must not calculate PAYG withholding.

The runbook must preserve that Imports / Actuals is not merely file upload or CSV parsing.

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
- promotion

Do not create generated benchmark, corpus coverage, answer-gap, or evaluation artefacts.

## Required Tests

Add focused assertions in `tests/test_domain_baseline_capture_batch.py` that:

- the runbook exists
- the runbook references all required control artefacts
- the runbook defines all four decision statuses
- the runbook states the transition requirements
- the runbook preserves current blocked states for Tax / PAYG and Imports / Actuals
- the runbook states `REVIEWED_READY_FOR_INGESTION` does not mutate corpus, run recapture, or promote a baseline
- the runbook does not state that governed ingestion has occurred, corpus has been mutated, ledger has been promoted, Tax / PAYG is `BASELINE_ALREADY_EXISTS`, or Imports / Actuals is `BASELINE_ALREADY_EXISTS`
- this prompt file is preserved

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report:

- files changed
- runbook created
- tests run
- `.pytest_tmp` status
- confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/generated-artefact changes

Suggested commit message: `minerva-formal-evidence-review-status-transition-runbook-v01`

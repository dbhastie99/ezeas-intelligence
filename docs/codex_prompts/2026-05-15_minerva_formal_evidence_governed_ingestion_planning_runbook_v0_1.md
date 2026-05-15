# Codex Prompt - Minerva Formal Evidence Governed Ingestion Planning Runbook v0.1

Date: 15 May 2026

Mode: Documentation/control-runbook hardening only

## Objective

Create `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md` as the controlled planning process for a future governed corpus-ingestion slice after a domain is explicitly marked `REVIEWED_READY_FOR_INGESTION`.

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions covering the new runbook and this durable prompt/control artefact.

## Required References

The runbook must reference:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

## Required Runbook Controls

The runbook must state that current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so governed ingestion is currently not permitted for either domain.

The runbook must define preconditions for future governed ingestion planning:

- latest decision record selected status `REVIEWED_READY_FOR_INGESTION`
- reviewer identity present
- reviewer date present
- reviewer rationale present
- reviewed source artefacts identified
- ingestion scope documented
- target corpus location documented
- mutation risk documented
- rollback/restore plan documented
- generated artefact policy documented
- recapture plan documented
- tests planned before corpus mutation

The runbook must state that ingestion planning alone:

- does not mutate corpus
- does not run recapture
- does not promote a baseline
- does not change runtime behaviour
- does not change ledger counts
- does not permit Minerva to answer as if ingestion has happened

The runbook must state that governed ingestion must be a separate explicit slice after planning and review readiness.

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
- the runbook defines all ingestion planning preconditions
- the runbook preserves current blocked states for Tax / PAYG and Imports / Actuals
- the runbook states ingestion planning alone does not mutate corpus, run recapture, promote a baseline, change runtime, or change ledger counts
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

Suggested commit message: `minerva-formal-evidence-governed-ingestion-planning-runbook-v01`

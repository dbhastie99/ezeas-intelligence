# Codex Prompt - Minerva Formal Evidence Control Index v0.1

Date: 15 May 2026

Mode: Documentation/control-index hardening only

## Objective

Create `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md` as the master navigation and status index for the formal evidence control model.

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions covering the new control index and this durable prompt/control artefact.

## Required References

The control index must reference:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

## Required Sections

The control index must include sections for:

- Purpose
- Scope
- Control Artefact Map
- Formal Evidence Lifecycle
- Current Controlled Domains
- Current Permission State
- How Minerva Should Use This Index
- How Codex Should Use This Index
- Non-Goals
- Follow-Up Workflow

## Required Lifecycle

The control index must show the full lifecycle:

```text
evidence gap identified
-> formal evidence gap plan
-> formal source-evidence draft
-> formal evidence review gate
-> review-gate index
-> decision record template
-> filled decision record
-> decision-record index
-> review readiness checklist
-> status transition runbook
-> governed ingestion planning
-> recapture planning
-> promotion planning
-> promotion execution guardrail
-> possible explicit promotion slice only after final preflight
```

## Required Current State

The control index must preserve Tax / PAYG and Imports / Actuals as:

- baseline status: `BASELINE_REQUIRED`
- decision status: `NOT_REVIEWED`
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No
- promotion execution permitted: No

It must state that Minerva may explain Tax / PAYG but must not calculate PAYG withholding.

It must state that Imports / Actuals is not merely file upload or CSV parsing.

It must state that no control artefact by itself mutates corpus, runs benchmark, runs corpus coverage, runs answer-gap reporting, changes runtime, changes ledger counts, or promotes a baseline.

It must state that future Codex slices should check this control index before changing formal evidence status, ingestion, recapture, promotion, or ledger state.

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

Add focused assertions in `tests/test_domain_baseline_capture_batch.py` that:

- the control index exists
- the control index references all required control artefacts
- the control index includes the full lifecycle
- the control index preserves current blocked states for Tax / PAYG and Imports / Actuals
- the control index states no control artefact alone mutates corpus, runs benchmark, runs corpus coverage, runs answer-gap reporting, changes runtime, changes ledger counts, or promotes a baseline
- the control index does not state that governed ingestion has occurred, recapture has occurred, promotion has occurred, ledger has been promoted, Tax / PAYG is `BASELINE_ALREADY_EXISTS`, or Imports / Actuals is `BASELINE_ALREADY_EXISTS`
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
- index created
- tests run
- `.pytest_tmp` status
- confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes

Suggested commit message: `minerva-formal-evidence-control-index-v01`

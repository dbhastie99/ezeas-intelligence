# Codex Prompt - Minerva Formal Evidence Promotion Execution Guardrail v0.1

Date: 15 May 2026

Mode: Documentation/control-guardrail hardening only

## Objective

Create `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md` as the final preflight guardrail that must pass before any future formal-evidence domain can be promoted from `BASELINE_REQUIRED` to `BASELINE_ALREADY_EXISTS`.

Update `tests/test_domain_baseline_capture_batch.py` with focused assertions covering the new guardrail and this durable prompt/control artefact.

## Required References

The guardrail must reference:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

## Required Guardrail Controls

The guardrail must state that current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so promotion execution is currently blocked for both domains.

The guardrail must define final preflight requirements for future promotion execution:

- latest decision record selected status `REVIEWED_READY_FOR_INGESTION`
- governed ingestion slice completed
- corpus mutation evidence recorded
- recapture slice completed
- benchmark results recorded
- corpus coverage results recorded
- answer-gap results recorded
- benchmark pass/failure status accepted
- no unresolved `MISSING` evidence groups unless accepted with written rationale
- answer-gap `GOOD` or accepted under documented policy
- generated artefact policy satisfied
- reviewer identity/date/rationale recorded
- ledger update diff planned
- rollback/supersession notes preserved
- explicit user approval for ledger promotion

The guardrail must state that the guardrail alone:

- does not mutate corpus
- does not run benchmark
- does not run corpus coverage
- does not run answer-gap reporting
- does not promote a baseline
- does not change runtime behaviour
- does not change ledger counts
- does not permit Minerva to answer as if promotion has happened

The guardrail must state that actual promotion must be a separate explicit execution slice after this final preflight passes.

The guardrail must preserve Tax / PAYG and Imports / Actuals as:

- baseline status: `BASELINE_REQUIRED`
- decision status: `NOT_REVIEWED`
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No

The guardrail must preserve that Minerva may explain Tax / PAYG but must not calculate PAYG withholding.

The guardrail must preserve that Imports / Actuals is not merely file upload or CSV parsing.

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

- the guardrail exists
- the guardrail references all required control artefacts
- the guardrail defines all final preflight requirements
- the guardrail preserves current blocked states for Tax / PAYG and Imports / Actuals
- the guardrail states it alone does not mutate corpus, run benchmark, run corpus coverage, run answer-gap reporting, promote a baseline, change runtime, or change ledger counts
- the guardrail requires explicit user approval for ledger promotion
- the guardrail does not state that promotion has occurred, benchmark has passed, corpus coverage has passed, answer gap is GOOD, ledger has been promoted, Tax / PAYG is `BASELINE_ALREADY_EXISTS`, or Imports / Actuals is `BASELINE_ALREADY_EXISTS`
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
- guardrail created
- tests run
- `.pytest_tmp` status
- confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes

Suggested commit message: `minerva-formal-evidence-promotion-execution-guardrail-v01`

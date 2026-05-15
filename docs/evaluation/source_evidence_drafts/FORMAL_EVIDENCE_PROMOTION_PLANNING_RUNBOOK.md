# Formal Evidence Promotion Planning Runbook

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This runbook controls planning for a future baseline-promotion slice after separate governed corpus ingestion and recapture slices have completed and recorded accepted evidence.

It is a documentation/control artefact only. It does not approve review, perform governed ingestion, mutate corpus, run benchmark, run corpus coverage, run answer-gap reporting, run recapture, promote a baseline, change runtime behaviour, change endpoints, change UI, call a live LLM, write to the database, or change completed-domain ledger counts.

## 2. Required Control Artefacts

Use this runbook with these durable repository controls:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

These artefacts, not chat-only agreement, control review status, ingestion planning, recapture eligibility, promotion planning, and promotion blocking.

## 3. Planning Scope

Promotion planning is the written preparation for a later explicit promotion slice that may update ledger state only if accepted recapture evidence exists and ledger mutation is explicitly in scope for that later slice.

Promotion planning alone does not mutate corpus.

Promotion planning alone does not run benchmark.

Promotion planning alone does not run corpus coverage.

Promotion planning alone does not run answer-gap reporting.

Promotion planning alone does not promote a baseline.

Promotion planning alone does not change runtime behaviour.

Promotion planning alone does not change ledger counts.

Promotion planning alone does not permit Minerva to answer as if promotion has happened.

Actual promotion must be a separate explicit slice after recapture evidence exists and is accepted.

## 4. Future Promotion Planning Preconditions

A future promotion planning slice may proceed only when all of these preconditions are documented:

- Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.
- Separate governed ingestion slice completed.
- Recapture slice completed.
- Benchmark command results recorded.
- Corpus coverage command results recorded.
- Answer-gap command results recorded.
- No unresolved `MISSING` evidence groups unless accepted with documented rationale.
- Benchmark pass/failure status documented.
- Answer-gap `GOOD` or accepted under documented policy.
- Generated artefact policy satisfied.
- Ledger update plan documented.
- Rollback/supersession notes preserved.

If any precondition is absent, promotion planning remains blocked and actual promotion remains out of scope.

## 5. Planning Procedure

1. Select the latest filled decision record from `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`.
2. Confirm its selected decision status is exactly `REVIEWED_READY_FOR_INGESTION`.
3. Confirm a separate governed ingestion slice completed after that review decision.
4. Confirm a separate recapture slice completed after governed ingestion.
5. Record benchmark command results, corpus coverage command results, and answer-gap command results from the recapture evidence.
6. Confirm every `MISSING` evidence group is resolved or accepted with documented rationale.
7. Document benchmark pass/failure status and whether answer-gap status is `GOOD` or accepted under documented policy.
8. Confirm generated artefact policy is satisfied for any benchmark, corpus coverage, answer-gap, and evaluation outputs considered by the decision.
9. Document the ledger update plan and preserve rollback/supersession notes before any later promotion slice.
10. Record that planning alone does not authorize corpus mutation, benchmark execution, corpus coverage execution, answer-gap execution, baseline promotion, runtime changes, ledger-count changes, or Minerva answers claiming promotion has happened.
11. Schedule a separate explicit promotion slice only after recapture evidence exists and is accepted.

## 6. Current Domain State

Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so promotion is currently not permitted for either domain.

| Domain | Baseline status | Latest decision record | Current decision status | Governed ingestion permitted | Recapture permitted | Promotion permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

## 7. Domain-Specific Answering Constraints

For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.

For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing. Imports / Actuals includes evidence-bearing import batches, rows, validation, errors, warnings, provenance, mapping, comparison, and remediation context.

Minerva must preserve that both domains remain `BASELINE_REQUIRED` and `NOT_REVIEWED` while the current decision records remain latest.

## 8. Non-Goals

This runbook does not implement:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- benchmark execution
- corpus coverage execution
- answer-gap execution
- baseline promotion
- ledger promotion
- endpoint changes
- UI changes
- workforce-platform changes
- award-configurator-v1 changes
- payroll runtime changes
- tax runtime changes
- import runtime changes
- actuals ingestion runtime changes
- reconciliation runtime changes
- review approval
- governed ingestion
- recapture
- generated artefact creation

It does not change completed-domain ledger counts. It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`. It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## 9. Prompt Preservation

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_promotion_planning_runbook_v0_1.md`.

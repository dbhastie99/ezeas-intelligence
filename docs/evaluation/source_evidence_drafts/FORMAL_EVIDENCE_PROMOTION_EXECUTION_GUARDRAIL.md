# Formal Evidence Promotion Execution Guardrail

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This guardrail defines the final preflight that must pass before any future formal-evidence domain can be promoted from `BASELINE_REQUIRED` to `BASELINE_ALREADY_EXISTS`.

It is a documentation/control artefact only. It does not approve review, perform governed ingestion, mutate corpus, run benchmark, run corpus coverage, run answer-gap reporting, run recapture, promote a baseline, change runtime behaviour, change endpoints, change UI, call a live LLM, write to the database, update the ledger, or change completed-domain ledger counts.

## 2. Required Control Artefacts

Use this guardrail with these durable repository controls:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

These artefacts, not chat-only agreement, control review status, ingestion planning, recapture eligibility, promotion planning, and promotion execution blocking.

## 3. Guardrail Scope

The final preflight is the last written control check before a later explicit promotion execution slice may update a domain from `BASELINE_REQUIRED` to `BASELINE_ALREADY_EXISTS`.

This guardrail alone does not mutate corpus.

This guardrail alone does not run benchmark.

This guardrail alone does not run corpus coverage.

This guardrail alone does not run answer-gap reporting.

This guardrail alone does not promote a baseline.

This guardrail alone does not change runtime behaviour.

This guardrail alone does not change ledger counts.

This guardrail alone does not permit Minerva to answer as if promotion has happened.

Actual promotion must be a separate explicit execution slice after this final preflight passes.

## 4. Final Preflight Requirements

Future promotion execution is blocked unless all final preflight requirements are satisfied and recorded:

- Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.
- Governed ingestion slice completed.
- Corpus mutation evidence recorded.
- Recapture slice completed.
- Benchmark results recorded.
- Corpus coverage results recorded.
- Answer-gap results recorded.
- Benchmark pass/failure status accepted.
- No unresolved `MISSING` evidence groups unless accepted with written rationale.
- Answer-gap `GOOD` or accepted under documented policy.
- Generated artefact policy satisfied.
- Reviewer identity/date/rationale recorded.
- Ledger update diff planned.
- Rollback/supersession notes preserved.
- Explicit user approval for ledger promotion.

If any requirement is absent, ambiguous, contradicted, or only asserted in chat without durable evidence, promotion execution remains blocked.

## 5. Final Preflight Procedure

1. Select the latest filled decision record from `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`.
2. Confirm its selected decision status is exactly `REVIEWED_READY_FOR_INGESTION`.
3. Confirm reviewer identity, reviewer date, and reviewer rationale are recorded.
4. Confirm a separate governed ingestion slice completed after that review decision.
5. Confirm corpus mutation evidence was recorded by the governed ingestion slice.
6. Confirm a separate recapture slice completed after governed ingestion.
7. Record benchmark results, corpus coverage results, and answer-gap results from the recapture evidence.
8. Confirm benchmark pass/failure status has been accepted.
9. Confirm every `MISSING` evidence group is resolved or accepted with written rationale.
10. Confirm answer-gap status is `GOOD` or accepted under documented policy.
11. Confirm generated artefact policy is satisfied for every evaluation output considered by the decision.
12. Plan the exact ledger update diff without applying it in this guardrail.
13. Preserve rollback/supersession notes.
14. Obtain explicit user approval for ledger promotion before any later promotion execution slice.
15. Record that this guardrail alone does not authorize corpus mutation, benchmark execution, corpus coverage execution, answer-gap execution, baseline promotion, runtime changes, ledger-count changes, or Minerva answers claiming promotion has happened.

## 6. Current Domain State

Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so promotion execution is currently blocked for both domains.

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

This guardrail does not implement:

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
- ledger update
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

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_promotion_execution_guardrail_v0_1.md`.

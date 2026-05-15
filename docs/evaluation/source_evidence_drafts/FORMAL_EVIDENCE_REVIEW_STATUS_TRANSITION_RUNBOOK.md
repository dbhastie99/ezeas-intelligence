# Formal Evidence Review Status Transition Runbook

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This runbook controls how a formal evidence review decision may move from `NOT_REVIEWED` to `NEEDS_REVISION`, `REVIEWED_READY_FOR_INGESTION`, or `SUPERSEDED`.

It is a documentation/control artefact only. It does not approve review, perform governed ingestion, mutate corpus, run recapture, promote a baseline, change runtime behaviour, change endpoints, change UI, call a live LLM, write to the database, or change completed-domain ledger counts.

## 2. Required Control Artefacts

Use this runbook with these durable repository controls:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

These artefacts, not chat-only agreement, control review status, ingestion planning, recapture eligibility, and promotion blocking.

## 3. Decision Status Definitions

### NOT_REVIEWED

`NOT_REVIEWED` means no assigned reviewer has completed formal doctrine review, implementation-state review, evidence-gap review, and non-overclaiming review. Governed ingestion, recapture, and promotion remain blocked.

### NEEDS_REVISION

`NEEDS_REVISION` means a reviewer has found issues in doctrine accuracy, implementation-state claims, evidence-gap coverage, or non-overclaiming constraints. `NEEDS_REVISION` blocks governed ingestion and requires follow-up changes before review can proceed.

### REVIEWED_READY_FOR_INGESTION

`REVIEWED_READY_FOR_INGESTION` means a reviewer has completed the required reviews, filled a decision record, and recorded reviewer identity, review date, and rationale.

`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only. It does not mutate corpus, run recapture, promote a baseline, change runtime behaviour, or change ledger counts.

### SUPERSEDED

`SUPERSEDED` means the referenced formal source-evidence draft, review gate, or decision record has been replaced. `SUPERSEDED` blocks governed ingestion and requires the superseded draft/gate/decision record not be used for governed ingestion planning.

## 4. Transition Requirements

A status transition from `NOT_REVIEWED` to `NEEDS_REVISION`, `REVIEWED_READY_FOR_INGESTION`, or `SUPERSEDED` requires a separate explicit review slice.

That review slice must create a filled decision record using `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`.

The filled decision record must include:

- reviewer identity
- review date
- reviewer rationale
- selected decision status
- doctrine review outcome
- implementation-state review outcome
- evidence-gap review outcome
- non-overclaiming review outcome
- governed ingestion decision
- recapture decision
- promotion decision
- required follow-up actions

The reviewer must complete:

- doctrine review
- implementation-state review
- evidence-gap review
- non-overclaiming review

The review slice must then update the relevant control indexes only to reflect the filled decision record. It must not imply ingestion, recapture, promotion, runtime capability, or ledger movement.

## 5. Status Transition Procedure

1. Confirm the latest gate and decision record in `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md` and `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`.
2. Confirm the domain still has the expected current decision status before review.
3. Use `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md` to complete doctrine, implementation-state, evidence-gap, and non-overclaiming checks.
4. Create a filled domain-specific decision record from `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`.
5. Select exactly one status: `NEEDS_REVISION`, `REVIEWED_READY_FOR_INGESTION`, or `SUPERSEDED`.
6. Record reviewer identity, review date, and reviewer rationale.
7. Update indexes only if the filled decision record exists and is the intended latest control.
8. Preserve blocked ingestion, recapture, and promotion state unless the selected status and later governed artefacts explicitly change those permissions.

## 6. Permission Rules

`NOT_REVIEWED` blocks governed ingestion, recapture, and promotion.

`NEEDS_REVISION` blocks governed ingestion and requires follow-up changes before review can proceed. It also blocks recapture and promotion.

`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only. It does not mutate corpus. It does not run recapture. It does not promote a baseline. It does not change runtime behaviour. It does not change ledger counts.

`SUPERSEDED` blocks governed ingestion and requires the superseded draft/gate/decision record not be used. It also blocks recapture and promotion from the superseded artefact chain.

Governed ingestion must be a separate explicit slice where corpus mutation is explicitly in scope, ingestion paths are named, tests are updated for that ingestion path, generated artefact policy is recorded, and rollback or correction handling is described.

Recapture must remain separate from review status transition. Promotion requires later real benchmark, corpus coverage, answer-gap evidence, and ledger decision evidence.

## 7. Current Domain State

| Domain | Baseline status | Latest decision record | Current decision status | Governed ingestion permitted | Recapture permitted | Promotion permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED`.

Imports / Actuals remains `BASELINE_REQUIRED`.

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

## 8. Domain-Specific Answering Constraints

For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.

For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing. Imports / Actuals includes evidence-bearing import batches, rows, validation, errors, warnings, provenance, mapping, comparison, and remediation context.

Minerva must preserve that both domains remain `BASELINE_REQUIRED` and `NOT_REVIEWED` until a later explicit review slice creates a filled replacement decision record.

## 9. Non-Goals

This runbook does not implement:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- benchmark recapture
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
- generated artefact creation

It does not change completed-domain ledger counts. It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`. It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## 10. Prompt Preservation

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_status_transition_runbook_v0_1.md`.

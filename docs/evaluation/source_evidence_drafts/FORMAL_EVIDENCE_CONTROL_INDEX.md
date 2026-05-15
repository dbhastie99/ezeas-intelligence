# Formal Evidence Control Index

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This index is the master navigation and status index for the Minerva formal evidence control model.

It points Minerva and future Codex slices to the durable repository artefacts that control formal source evidence, review status, decision records, readiness checks, governed ingestion planning, recapture planning, promotion planning, and promotion execution guardrails.

It is a documentation/control artefact only. It does not approve review, perform governed ingestion, mutate corpus, run benchmark, run corpus coverage, run answer-gap reporting, run recapture, promote a baseline, change runtime behaviour, change endpoints, change UI, call a live LLM, write to the database, update the ledger, or change completed-domain ledger counts.

## 2. Scope

This index covers the current formal evidence control chain for:

- Tax / PAYG
- Imports / Actuals

It covers navigation and status control across source-evidence drafts, review gates, decision records, review readiness, status transition, governed ingestion planning, recapture planning, promotion planning, and promotion execution preflight.

It does not replace any lower-level control artefact. When a domain-specific file, index, checklist, runbook, or guardrail records stricter requirements, future slices must satisfy those requirements as well as this index.

## 3. Control Artefact Map

Use these durable repository controls together:

| Control stage | Artefact |
| --- | --- |
| Source-evidence control README | `docs/evaluation/source_evidence_drafts/README.md` |
| Review-gate register | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md` |
| Decision record template | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md` |
| Decision-record register | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md` |
| Review readiness checklist | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md` |
| Status transition runbook | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md` |
| Governed ingestion planning | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md` |
| Recapture planning | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md` |
| Promotion planning | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md` |
| Promotion execution guardrail | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md` |
| Formal evidence control model closeout/state summary | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md` |
| Tax / PAYG current decision record | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` |
| Imports / Actuals current decision record | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` |

## 4. Formal Evidence Lifecycle

The formal evidence control lifecycle is:

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

No lifecycle stage is implied by file existence alone. Each status transition, ingestion step, recapture step, and promotion step requires a separate explicit slice with the required durable evidence and tests.

## 5. Current Controlled Domains

| Domain | Baseline status | Current decision record | Decision status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Promotion execution permitted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

## 6. Current Permission State

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

Promotion execution permitted: No.

No control artefact by itself mutates corpus, runs benchmark, runs corpus coverage, runs answer-gap reporting, changes runtime behaviour, changes ledger counts, or promotes a baseline.

For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.

For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing. Imports / Actuals includes evidence-bearing import batches, rows, validation, errors, warnings, provenance, mapping, comparison, and remediation context.

## 7. How Minerva Should Use This Index

Minerva should use this index as the first navigation point when answering questions about formal evidence control state.

Minerva may say that Tax / PAYG and Imports / Actuals have formal evidence control chains, current `NOT_REVIEWED` decision records, and blocked downstream permissions.

Minerva must preserve that Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED` while the current decision records remain latest.

Minerva must not answer as if review approval, governed ingestion, recapture, promotion, runtime behaviour changes, corpus mutation, benchmark success, corpus coverage success, answer-gap closure, or ledger promotion has happened unless later durable repository artefacts explicitly record those facts.

## 8. How Codex Should Use This Index

Future Codex slices should check this control index before changing formal evidence status, ingestion, recapture, promotion, or ledger state.

Future Codex slices must also read the lower-level artefacts listed in the Control Artefact Map before changing any controlled state.

Future Minerva/Codex work should start at this control index and use `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md` as the closeout/state summary to understand what was created, why it exists, what remains blocked, and what future slices are allowed or forbidden to do.

Any future status change must update the relevant decision record and index files in a separate explicit slice with focused tests. Any future governed ingestion, recapture, promotion, or ledger update must be explicitly scoped and must not be inferred from this index.

## 9. Non-Goals

This index does not implement:

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

It does not change completed-domain ledger counts. It does not mark any domain as `REVIEWED_READY_FOR_INGESTION`. It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## 10. Follow-Up Workflow

1. Start with this index to identify the current formal evidence state.
2. Read the source-evidence control README and relevant domain decision record.
3. Use the review readiness checklist before any formal review or status transition.
4. Use the status transition runbook before any decision status change.
5. Use governed ingestion planning only after a latest decision record is `REVIEWED_READY_FOR_INGESTION`.
6. Use recapture planning only after governed ingestion or another explicitly documented evidence update.
7. Use promotion planning only after recapture evidence exists and is accepted.
8. Use the promotion execution guardrail as the final preflight before any possible explicit promotion slice.
9. Run any possible explicit promotion slice only after final preflight and explicit user approval.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_index_v0_1.md`.

This closeout-link slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_model_index_closeout_link_v0_1.md`.

# Formal Evidence Review Decision Record Index

Slice: Minerva Review Decision Record Index v0.1

Date: 15 May 2026

## 1. Purpose

This index is the central register of filled formal evidence review decision records for Minerva baseline domains.

It tells Minerva and future Codex slices which domains have filled decision records, where those records are stored, what selected decision status each record contains, whether governed ingestion is permitted, whether recapture is permitted, whether promotion is permitted, whether the domain remains `BASELINE_REQUIRED`, and whether follow-up action remains required.

This index records current decisions only. It does not imply approval.

## 2. Scope

This index currently covers filled formal evidence review decision records for:

- Tax / PAYG
- Imports / Actuals

Referenced control artefacts:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`

The completed-domain ledger state remains:

- `BASELINE_REQUIRED`: 17
- `BASELINE_ALREADY_EXISTS`: 14
- `RUNBOOK_OUTSTANDING`: 0
- `NEEDS_REVIEW`: 0
- Total domains: 31

## 3. Decision Status Definitions

- `NOT_REVIEWED`: a filled decision record exists, but no assigned reviewer has performed the formal review. Governed ingestion, recapture, and promotion are blocked.
- `NEEDS_REVISION`: a reviewer has found issues that must be corrected. Governed ingestion, recapture, and promotion are blocked.
- `REVIEWED_READY_FOR_INGESTION`: a reviewer has recorded readiness for planning a future governed ingestion slice. This status does not ingest evidence, mutate corpus, run recapture, or promote a baseline.
- `SUPERSEDED`: the decision record has been replaced and must not be used for governed ingestion planning.

## 4. Current Decision-Record Table

| Domain | Domain slug | Baseline status | Review gate status | Latest decision record | Selected decision status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `tax_payg` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |
| Imports / Actuals | `imports_actuals` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |

Tax / PAYG remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.

## 5. Ingestion / Recapture / Promotion Rules

1. A filled decision record does not itself permit governed ingestion.
2. A `NOT_REVIEWED` decision record blocks governed ingestion.
3. A `NEEDS_REVISION` decision record blocks governed ingestion.
4. A `SUPERSEDED` decision record must not be used for governed ingestion.
5. Only `REVIEWED_READY_FOR_INGESTION` can permit planning a future governed ingestion slice.
6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.
7. `REVIEWED_READY_FOR_INGESTION` does not itself run recapture.
8. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.
9. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.
10. No domain is promoted merely because a decision record exists.
11. Minerva must not overstate review, ingestion, runtime, recapture, or promotion state.

## 6. Minerva Usage Guidance

Minerva must use this index to find the latest filled review decision record for formal evidence domains.

Minerva must not answer as if a domain has been approved for ingestion unless the latest decision record says `REVIEWED_READY_FOR_INGESTION`.

Minerva must not answer as if corpus ingestion is complete merely because `REVIEWED_READY_FOR_INGESTION` exists.

Minerva must not answer as if recapture or promotion is complete unless benchmark, corpus coverage, answer-gap, and ledger evidence records those facts.

Minerva must preserve Tax / PAYG and Imports / Actuals as `BASELINE_REQUIRED` while these decision records remain `NOT_REVIEWED`.

## 7. Non-Goals

This index does not implement:

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

It does not change completed-domain ledger counts, mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`, or mark either domain as promoted.

## 8. Follow-Up Actions

- Assign a reviewer for the Tax / PAYG formal evidence decision record.
- Perform Tax / PAYG doctrine review before any governed ingestion planning.
- Assign a reviewer for the Imports / Actuals formal evidence decision record.
- Perform Imports / Actuals doctrine review before any governed ingestion planning.
- Update this index only when a later filled decision record supersedes the current `NOT_REVIEWED` record.

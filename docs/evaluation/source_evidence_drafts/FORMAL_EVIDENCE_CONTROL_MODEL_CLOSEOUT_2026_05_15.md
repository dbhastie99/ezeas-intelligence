# Formal Evidence Control Model Closeout

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This closeout records the Minerva formal evidence control model created for knowledge maintenance.

The purpose of the model is to stop relying on brittle chat history or copied Word documents for evidence control. Prompts, decisions, source evidence controls, review gates, permission state, and follow-up status are preserved as durable repository artefacts.

This closeout is documentation/control only. It does not approve review, perform governed ingestion, mutate corpus, run benchmark, run corpus coverage, run answer-gap reporting, run recapture, promote a baseline, update a ledger, change runtime behaviour, change endpoints, change UI, connect Code Evidence, call a live LLM, write to the database, or create generated evaluation artefacts.

## 2. Control Artefacts Created Or Linked

The control model now has a master starting point:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`

The model is also linked from operator-facing repository entry points:

- source-evidence README link: `docs/evaluation/source_evidence_drafts/README.md`
- root README link: `README.md`

The current formal evidence review and permission chain is:

- review-gate index: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- decision-record template: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- decision-record index: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- review readiness checklist: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- status transition runbook: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- governed ingestion planning runbook: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md`
- recapture planning runbook: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md`
- promotion planning runbook: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md`
- promotion execution guardrail: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md`

Current domain decision records:

- Tax / PAYG `NOT_REVIEWED` decision record: `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- Imports / Actuals `NOT_REVIEWED` decision record: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_model_closeout_v0_1.md`.

## 3. Current Status Preserved

| Domain | Baseline status | Review status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Promotion execution permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

Promotion execution permitted: No.

## 4. Boundary Statement

This closeout records that this slice made no operational change.

No corpus mutation occurred.

No Code Evidence integration occurred.

No live LLM call occurred.

No benchmark recapture occurred.

No corpus coverage run occurred.

No answer-gap run occurred.

No runtime change occurred.

No UI change occurred.

No endpoint change occurred.

No workforce-platform change occurred.

No award-configurator-v1 change occurred.

No review approval occurred.

No governed ingestion occurred.

No recapture occurred.

No promotion occurred.

No ledger update occurred.

No DB write, migration, benchmark execution, corpus coverage execution, answer-gap execution, generated artefact creation, ledger promotion, or baseline promotion was performed.

## 5. Operator Guidance

Future Codex and Minerva slices should begin at `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md` before changing formal evidence status, ingestion, recapture, promotion, or ledger state.

Future slices should preserve prompt files under `docs/codex_prompts/` whenever the prompt defines or changes Minerva knowledge-maintenance controls. Repository artefacts, not chat memory, are the durable source of truth for prompts, decisions, evidence controls, gates, and review state.

Minerva should use the control index and decision-record index before answering whether Tax / PAYG or Imports / Actuals evidence has been reviewed, ingested, recaptured, or promoted. While the latest decision records remain `NOT_REVIEWED`, Minerva must preserve that downstream permissions are blocked.

## 6. Still To Do

Tax / PAYG remains blocked until explicit review is performed in a separate future slice. A possible `REVIEWED_READY_FOR_INGESTION` transition, governed ingestion, recapture, and possible promotion must each be performed only in separately scoped future slices with durable evidence and focused tests.

Imports / Actuals remains blocked until explicit review is performed in a separate future slice. A possible `REVIEWED_READY_FOR_INGESTION` transition, governed ingestion, recapture, and possible promotion must each be performed only in separately scoped future slices with durable evidence and focused tests.

No future slice may infer review approval, governed ingestion permission, recapture permission, promotion permission, or promotion execution permission from this closeout alone.

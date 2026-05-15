# Minerva Formal Evidence Control README

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This README is the operator-facing control guide for Minerva formal evidence artefacts.

It explains what each artefact is for, how an evidence gap moves through review and possible promotion, what remains blocked while records are `NOT_REVIEWED`, and how Minerva and future Codex slices should use durable repository files instead of chat-only instructions.

Start future formal evidence control work from `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`. It is the master starting point/control index for review gates, decision records, readiness checklists, status transitions, governed ingestion planning, recapture planning, promotion planning, and promotion execution guardrails. This README gives operator context; the control index is the master map.

The current completed-domain ledger state remains:

- `BASELINE_REQUIRED`: 17
- `BASELINE_ALREADY_EXISTS`: 14
- `RUNBOOK_OUTSTANDING`: 0
- `NEEDS_REVIEW`: 0
- Total domains: 31

Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED`.

## 2. Scope

This README covers the formal evidence control model for source-evidence drafts, review gates, decision records, governed ingestion planning, recapture, and possible ledger promotion.

Current source-evidence control artefacts:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/codex_prompts/`

This is documentation/control guidance only. It does not perform DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, recapture, or governed ingestion.

## 3. Formal Evidence Lifecycle

The required lifecycle is:

```text
evidence gap identified
→ formal evidence gap plan
→ formal source-evidence draft
→ formal evidence review gate
→ review-gate index
→ formal evidence review decision record template
→ filled review decision record
→ decision-record index
→ REVIEWED_READY_FOR_INGESTION only after explicit review
→ separate governed ingestion slice
→ recapture
→ benchmark/corpus/answer-gap evidence
→ possible ledger promotion
```

No stage may be skipped by chat agreement, file existence, or an implied operator decision. Each transition must be recorded in the repository artefact that controls that stage.

## 4. Artefact Types

Formal evidence gap plan: records the evidence gap, affected domain, source doctrine needed, expected future coverage, and why the domain remains incomplete.

Formal source-evidence draft: captures proposed source evidence in a reviewable form. A draft is not ingested corpus evidence and does not permit recapture or promotion.

Formal evidence review gate: records the review status for a draft. A gate with `NOT_REVIEWED` or `NEEDS_REVISION` blocks governed ingestion.

Review-gate index: the central register for gate status and ingestion guards across formal evidence domains.

Formal evidence review decision record template: the required structure for a reviewer decision. It defines allowed statuses, required reviewer details, doctrine review findings, implementation-state findings, and permission implications.

Filled review decision record: records the selected decision status for a domain. A `NOT_REVIEWED` decision record is a durable block, not approval.

Decision-record index: records the latest filled decision record per domain and tells Minerva whether governed ingestion, recapture, and promotion remain blocked.

Governed ingestion: a separate future slice where corpus mutation is explicitly in scope, the ingestion path is identified, and tests and generated artefact policy are updated for that ingestion path.

Recapture: rerunning benchmark, corpus coverage, and answer-gap evidence after governed ingestion or an explicitly recorded evidence update.

Promotion: possible ledger movement only after reviewed evidence, governed ingestion when needed, recapture, and real benchmark/corpus/answer-gap evidence support promotion.

## 5. Current Controlled Domains

| Domain | Current baseline status | Latest gate | Latest decision record | Current decision status | Governed ingestion | Recapture | Promotion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | blocked | blocked | blocked |
| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | blocked | blocked | blocked |

Both domains have complete `NOT_REVIEWED` control chains. Neither domain has reviewed approval, governed ingestion, recapture, or promotion.

## 6. Status and Permission Rules

- `DRAFT_ONLY`: draft exists, but governed ingestion is blocked.
- `NOT_REVIEWED`: review has not happened. Governed ingestion, recapture, and promotion are blocked.
- `NEEDS_REVISION`: review found issues. Governed ingestion, recapture, and promotion are blocked.
- `REVIEWED_READY_FOR_INGESTION`: explicit reviewer readiness for a future governed ingestion slice. This does not mutate corpus, run recapture, or promote a baseline.
- `SUPERSEDED`: the artefact has been replaced and must not be used for ingestion planning.

Permission rules:

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate or decision record with `NOT_REVIEWED` blocks governed ingestion.
3. Only `REVIEWED_READY_FOR_INGESTION` can permit planning a separate governed ingestion slice.
4. Governed ingestion does not itself promote a baseline.
5. Recapture requires governed ingestion or an explicit evidence update.
6. Promotion requires real benchmark, corpus coverage, and answer-gap evidence after the controlled prerequisite stages.
7. Minerva must not overstate review, ingestion, runtime, recapture, or promotion state.

## 7. Minerva Usage Guidance

Minerva may say that formal source-evidence drafts, review gates, and `NOT_REVIEWED` decision records exist for Tax / PAYG and Imports / Actuals.

Minerva must say that both domains remain `BASELINE_REQUIRED` while the latest decision records are `NOT_REVIEWED`.

Minerva must not describe a draft as ingested corpus evidence. It must not claim review approval, governed ingestion, recapture, runtime behaviour, benchmark success, answer-gap closure, corpus mutation, or ledger promotion unless later durable repository artefacts record those facts.

For Tax / PAYG, Minerva may explain controlled documentation status but must not claim PAYG withholding calculation capability from these artefacts.

For Imports / Actuals, Minerva must preserve the distinction between imported actuals as evidence for reconciliation/comparison and calculated payroll truth.

## 8. Codex Prompt Preservation Workflow

Detailed prompts that define review gates, decision records, baseline packs, source-evidence controls, or operating-model changes must be saved under `docs/codex_prompts/`.

Future Codex slices should:

1. Read the relevant prompt file and control artefacts before editing.
2. Preserve new bounded prompts as durable repository artefacts when the prompt changes the Minerva knowledge-maintenance model.
3. Reference prompt files in follow-up documentation when the prompt is part of the durable rationale.
4. Avoid brittle chat-only workflows where review rules, decision gates, or promotion criteria exist only in conversation history.
5. Treat repository artefacts, not chat, as the durable source of truth.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md`.

## 9. Generated Artefact Policy

Generated benchmark, corpus coverage, answer-gap, and evaluation JSON outputs are transient unless a later repository convention explicitly versions them as durable artefacts.

Do not commit generated artefacts merely because a formal evidence draft, gate, decision record, or README exists.

Durable control artefacts are markdown documents in the repository. Runtime outputs, corpus mutations, ingestion products, recapture outputs, and ledger changes require explicit scope and tests in their own slices.

## 10. Non-Goals

This README does not implement or approve:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- benchmark recapture
- baseline promotion
- ledger promotion
- review approval
- governed ingestion
- endpoint changes
- UI changes
- workforce-platform changes
- payroll runtime changes
- tax runtime changes
- import runtime changes
- actuals ingestion runtime changes
- reconciliation runtime changes

It does not change completed-domain ledger counts and does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## 11. Follow-Up Workflow

1. Assign a reviewer for each `NOT_REVIEWED` decision record.
2. Reviewer performs doctrine, implementation-state, evidence-gap, and non-overclaiming review.
3. Reviewer fills a decision record using `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`.
4. Update `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md` only after a filled decision record exists.
5. If and only if the selected status is `REVIEWED_READY_FOR_INGESTION`, plan a separate governed ingestion slice.
6. After governed ingestion, run recapture and record benchmark/corpus/answer-gap evidence.
7. Consider ledger promotion only when recapture evidence supports it.
8. Preserve future operator prompts under `docs/codex_prompts/` when they define durable Minerva controls.

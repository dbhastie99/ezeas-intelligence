# Codex Prompt - Tax / PAYG Formal Evidence Review Gate v0.1

Date: 15 May 2026

Repository: ezeas-intelligence

Slice: Tax / PAYG Formal Evidence Review Gate v0.1

Mode: Documentation/control-gate hardening only

Codex behaviour: Auto is acceptable for bounded repo-internal markdown/test edits only. Do not approve DB writes, migrations, external network calls, generated artefact commits, runtime integration, corpus mutation, or destructive actions.

## Platform Context

We are continuing the Minerva completed-domain baseline program.

The current expected completed-domain ledger state is:

- BASELINE_REQUIRED = 17
- BASELINE_ALREADY_EXISTS = 14
- RUNBOOK_OUTSTANDING = 0
- NEEDS_REVIEW = 0
- Total domains = 31

Tax / PAYG remains BASELINE_REQUIRED.

Tax / PAYG must not be promoted through synthesis alone. It has a real formal source-evidence gap that must follow the no-shortcuts path:

1. formal evidence gap plan
2. formal source-evidence draft
3. formal evidence review gate
4. governed ingestion only after review
5. recapture
6. possible promotion only if benchmark, corpus coverage, and answer-gap evidence supports promotion

This slice implements step 3 only.

## Knowledge Preservation Model

Use the new knowledge-maintenance model.

The detailed prompt itself must be preserved in the repository under:

`docs/codex_prompts/2026-05-15_tax_payg_formal_evidence_review_gate_v0_1.md`

Chat is not the durable source of truth. Repository artefacts, baseline packs, source-evidence drafts, review gates, tests, and logs are the durable knowledge trail for Minerva.

Do not rely on memory. Do not update memory.

## Purpose

Add a Tax / PAYG formal evidence review/control gate before any governed corpus-ingestion slice can use the Tax / PAYG formal source-evidence draft.

The review gate must mirror the Imports / Actuals formal evidence review-gate model.

The gate must make it clear that the Tax / PAYG draft is not yet approved for ingestion and that Tax / PAYG remains BASELINE_REQUIRED.

## Scope

Create or update the following likely files:

1. `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
2. `docs/evaluation/worker_story_baselines/tax_payg/v0_1/REVIEW_NOTES.md`
3. `tests/test_domain_baseline_capture_batch.py`
4. `docs/codex_prompts/2026-05-15_tax_payg_formal_evidence_review_gate_v0_1.md`

If the Imports / Actuals review gate has an existing test pattern, reuse the same pattern.

Use the existing Tax / PAYG evidence files as source truth:

- `docs/evaluation/source_evidence_drafts/tax_payg/FORMAL_EVIDENCE_GAP_PLAN.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md`
- `docs/evaluation/worker_story_baselines/tax_payg/v0_1/REVIEW_NOTES.md`
- `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

## Required Review Gate Content

The review gate must include:

- domain: Tax / PAYG
- review gate version: v0.1
- current review status: NOT_REVIEWED
- allowed statuses:
- NOT_REVIEWED
- NEEDS_REVISION
- REVIEWED_READY_FOR_INGESTION
- SUPERSEDED
- explicit statement that the draft is not approved for governed corpus ingestion
- explicit statement that Tax / PAYG remains BASELINE_REQUIRED
- references to:
- FORMAL_EVIDENCE_GAP_PLAN.md
- TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md
- doctrine review checklist
- implementation-state review checklist
- evidence-gap coverage review checklist
- ingestion decision section
- reviewer notes section
- Minerva implication section
- non-goals section

## Required Doctrine to Preserve

The review gate must preserve these points:

1. Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps.
2. Minerva must not calculate PAYG withholding.
3. Tax / PAYG remains BASELINE_REQUIRED until real recapture evidence supports promotion.
4. The formal source-evidence draft is not enough by itself to permit ingestion.
5. Governed ingestion must not happen until the review gate is marked REVIEWED_READY_FOR_INGESTION.
6. The review gate is a control artefact, not a runtime feature.
7. This slice must not change tax runtime, PAYG runtime, payroll execution, or workforce-platform behaviour.

## Non-Goals

Do not implement any of the following:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- runtime tax calculation
- PAYG calculation
- payroll runtime changes
- endpoint changes
- UI changes
- workforce-platform changes
- award-configurator-v1 changes
- benchmark recapture
- baseline promotion
- ledger promotion
- generated artefact commits

Do not mark Tax / PAYG as BASELINE_ALREADY_EXISTS.

Do not change the ledger counts except if a test fixture requires explicit preservation of the existing expected counts. The domain status must remain BASELINE_REQUIRED.

## Test Requirements

Add or update focused tests to assert:

1. The Tax / PAYG formal evidence review gate file exists.
2. It contains current review status NOT_REVIEWED.
3. It contains all allowed statuses:
- NOT_REVIEWED
- NEEDS_REVISION
- REVIEWED_READY_FOR_INGESTION
- SUPERSEDED
4. It references the Tax / PAYG formal evidence gap plan.
5. It references the Tax / PAYG formal source-evidence draft.
6. It states that governed corpus ingestion is blocked until REVIEWED_READY_FOR_INGESTION.
7. It states that Tax / PAYG remains BASELINE_REQUIRED.
8. It does not claim benchmark promotion.
9. It does not claim runtime PAYG calculation has been implemented.
10. REVIEW_NOTES.md references the review gate and preserves the current not-promoted state.

Where possible, mirror the existing Imports / Actuals review-gate test approach.

## Commands

Start by checking the repo state:

```powershell
cd C:\Projects\ezeas-intelligence
git --no-pager status --short
git --no-pager log -8 --oneline
```

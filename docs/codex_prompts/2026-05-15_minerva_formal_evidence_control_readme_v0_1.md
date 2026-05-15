# Codex Prompt — Minerva Formal Evidence Control README v0.1

Date: 15 May 2026
Repository: ezeas-intelligence
Slice: Minerva Formal Evidence Control README v0.1
Mode: Documentation/control-readme hardening only
Codex behaviour: Auto is acceptable for bounded repo-internal markdown/test edits only. Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, recapture, or governed ingestion.

## Platform Context

We are continuing the Minerva completed-domain baseline program and the new knowledge-maintenance operating model.

Current expected ledger state:

- BASELINE_REQUIRED = 17
- BASELINE_ALREADY_EXISTS = 14
- RUNBOOK_OUTSTANDING = 0
- NEEDS_REVIEW = 0
- Total domains = 31

Tax / PAYG remains BASELINE_REQUIRED.

Imports / Actuals remains BASELINE_REQUIRED.

Both domains now have complete NOT_REVIEWED control chains.

The new knowledge-maintenance operating model says detailed prompts, review gates, decision records, baseline packs, and source-evidence artefacts should be preserved in the repository as durable Minerva knowledge artefacts. Chat is not the durable source of truth.

## Purpose

Create a single operator-facing README for the formal evidence control model.

The README should explain:

- what each formal evidence artefact is for;
- the required lifecycle from evidence gap to possible promotion;
- the difference between a draft, a review gate, a decision record, governed ingestion, recapture, and promotion;
- how Minerva should interpret these artefacts;
- what remains blocked while records are NOT_REVIEWED;
- how future Codex slices should use prompt files and avoid brittle chat-only workflows.

## Scope

Create:

docs/evaluation/source_evidence_drafts/README.md

Update or add focused tests in:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt at:

docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md

## Source Artefacts to Reference

The README must reference:

- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md
- docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- docs/codex_prompts/

## Required README Sections

The README must include:

1. Purpose
2. Scope
3. Formal Evidence Lifecycle
4. Artefact Types
5. Current Controlled Domains
6. Status and Permission Rules
7. Minerva Usage Guidance
8. Codex Prompt Preservation Workflow
9. Generated Artefact Policy
10. Non-Goals
11. Follow-Up Workflow

## Required Lifecycle

The README must show this lifecycle:

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

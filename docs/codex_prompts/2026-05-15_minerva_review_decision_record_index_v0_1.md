# Codex Prompt - Minerva Review Decision Record Index v0.1

Date: 15 May 2026

Repository: ezeas-intelligence

Slice: Minerva Review Decision Record Index v0.1

Mode: Documentation/control-index hardening only

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

Both domains now have complete NOT_REVIEWED control chains:

- formal evidence gap plan
- formal source-evidence draft
- formal evidence review gate
- central review-gate index entry
- reusable review decision record template
- filled NOT_REVIEWED review decision record

The next missing durable control artefact is a central review decision record index.

## Purpose

Create a central index of filled formal evidence review decision records.

This index should tell Minerva and future Codex slices:

- which domains have filled decision records;
- where those decision records are stored;
- what selected decision status each record contains;
- whether governed ingestion is permitted;
- whether recapture is permitted;
- whether promotion is permitted;
- whether the domain remains BASELINE_REQUIRED;
- whether any follow-up action is still required.

This index must not imply approval. It records the current NOT_REVIEWED decisions only.

## Scope

Create:

docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md

Update or add focused tests in:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt at:

docs/codex_prompts/2026-05-15_minerva_review_decision_record_index_v0_1.md

## Source Artefacts to Reference

The index must reference:

- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md
- docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md

## Required Index Content

The index must include:

1. Purpose
2. Scope
3. Decision status definitions
4. Current decision-record table
5. Ingestion / recapture / promotion rules
6. Minerva usage guidance
7. Non-goals
8. Follow-up actions

## Required Current Decision-Record Table

The table must include at least these rows.

### Tax / PAYG

- domain: Tax / PAYG
- domain slug: tax_payg
- baseline status: BASELINE_REQUIRED
- review gate status: NOT_REVIEWED
- latest decision record: TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- selected decision status: NOT_REVIEWED
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No
- next action: assign reviewer / doctrine review

### Imports / Actuals

- domain: Imports / Actuals
- domain slug: imports_actuals
- baseline status: BASELINE_REQUIRED
- review gate status: NOT_REVIEWED
- latest decision record: IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- selected decision status: NOT_REVIEWED
- governed ingestion permitted: No
- recapture permitted: No
- promotion permitted: No
- next action: assign reviewer / doctrine review

## Required Decision Rules

The index must state:

1. A filled decision record does not itself permit governed ingestion.
2. A NOT_REVIEWED decision record blocks governed ingestion.
3. A NEEDS_REVISION decision record blocks governed ingestion.
4. A SUPERSEDED decision record must not be used for governed ingestion.
5. Only REVIEWED_READY_FOR_INGESTION can permit planning a future governed ingestion slice.
6. REVIEWED_READY_FOR_INGESTION does not itself mutate corpus.
7. REVIEWED_READY_FOR_INGESTION does not itself run recapture.
8. REVIEWED_READY_FOR_INGESTION does not itself promote a baseline.
9. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.
10. No domain is promoted merely because a decision record exists.
11. Minerva must not overstate review, ingestion, runtime, recapture, or promotion state.

## Required Minerva Guidance

The index must tell Minerva:

- use this index to find the latest filled review decision record for formal evidence domains;
- do not answer as if a domain has been approved for ingestion unless the latest decision record says REVIEWED_READY_FOR_INGESTION;
- do not answer as if corpus ingestion has happened merely because REVIEWED_READY_FOR_INGESTION exists;
- do not answer as if recapture or promotion has happened unless benchmark/corpus/answer-gap and ledger evidence exists;
- preserve Tax / PAYG and Imports / Actuals as BASELINE_REQUIRED while these decision records remain NOT_REVIEWED.

## Tests

Add focused tests to assert:

1. FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md exists.
2. The index references the review-gate index.
3. The index references the reusable decision record template.
4. The index references the Tax / PAYG NOT_REVIEWED decision record.
5. The index references the Imports / Actuals NOT_REVIEWED decision record.
6. The index states Tax / PAYG remains BASELINE_REQUIRED.
7. The index states Imports / Actuals remains BASELINE_REQUIRED.
8. The index states Tax / PAYG selected decision status is NOT_REVIEWED.
9. The index states Imports / Actuals selected decision status is NOT_REVIEWED.
10. The index states governed ingestion permitted is No for both domains.
11. The index states recapture permitted is No for both domains.
12. The index states promotion permitted is No for both domains.
13. The index states a filled decision record does not itself permit governed ingestion.
14. The index states NOT_REVIEWED blocks governed ingestion.
15. The index states REVIEWED_READY_FOR_INGESTION does not itself mutate corpus.
16. The index states REVIEWED_READY_FOR_INGESTION does not itself run recapture.
17. The index states REVIEWED_READY_FOR_INGESTION does not itself promote a baseline.
18. The index states baseline promotion requires benchmark, corpus coverage, and answer-gap evidence.
19. The index does not state Tax / PAYG is BASELINE_ALREADY_EXISTS.
20. The index does not state Imports / Actuals is BASELINE_ALREADY_EXISTS.
21. The index does not state governed ingestion has occurred.
22. The index does not state corpus has been mutated.
23. The index does not state ledger has been promoted.

## Non-Goals

Do not implement:

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

Do not change completed-domain ledger counts.

Do not mark Tax / PAYG or Imports / Actuals as REVIEWED_READY_FOR_INGESTION.

Do not mark Tax / PAYG or Imports / Actuals as BASELINE_ALREADY_EXISTS.

Do not create runtime behaviour.

## Verification

Run:

```powershell
cd C:\Projects\ezeas-intelligence
python -m pytest tests\test_domain_baseline_capture_batch.py -q
git diff --check
if (Test-Path .\.pytest_tmp) { Remove-Item -Recurse -Force .\.pytest_tmp }
Test-Path .\.pytest_tmp
git --no-pager status --short
```

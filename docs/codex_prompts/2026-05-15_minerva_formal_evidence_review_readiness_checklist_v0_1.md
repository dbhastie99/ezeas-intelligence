# Codex Prompt - Minerva Formal Evidence Review Readiness Checklist v0.1

Date: 15 May 2026

Repository: ezeas-intelligence

Slice: Minerva Formal Evidence Review Readiness Checklist v0.1

Mode: Documentation/control-checklist hardening only

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

Both domains currently have NOT_REVIEWED decision records and are blocked from governed ingestion, recapture, and promotion.

The formal evidence control model now includes:

- review-gate index
- reusable review decision record template
- review decision record index
- Tax / PAYG NOT_REVIEWED decision record
- Imports / Actuals NOT_REVIEWED decision record
- formal evidence control README

The next missing artefact is a reviewer-facing readiness checklist that defines what must be checked before any future decision can move beyond NOT_REVIEWED.

## Purpose

Create a reusable Formal Evidence Review Readiness Checklist.

The checklist should guide a reviewer through the required checks before updating a review decision record to:

- NEEDS_REVISION
- REVIEWED_READY_FOR_INGESTION
- SUPERSEDED

It must make clear that completing the checklist does not itself change review status, mutate corpus, run recapture, or promote a baseline.

## Scope

Create:

docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md

Update or add focused tests in:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt at:

docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_readiness_checklist_v0_1.md

## Source Artefacts to Reference

The checklist must reference:

- docs/evaluation/source_evidence_drafts/README.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md
- docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md

## Required Checklist Sections

The checklist must include:

1. Purpose
2. Scope
3. Reviewer Preconditions
4. Source Artefact Checklist
5. Doctrine Review Checklist
6. Implementation-State Review Checklist
7. Evidence-Gap Coverage Checklist
8. Non-Overclaiming Checklist
9. Decision Status Guidance
10. Ingestion Readiness Gate
11. Recapture Readiness Gate
12. Promotion Readiness Gate
13. Domain-Specific Notes
14. Minerva Answering Guidance
15. Non-Goals
16. Follow-Up Actions

## Required Reviewer Preconditions

The checklist must state that before changing a decision status, the reviewer must confirm:

- correct domain and slug;
- current baseline status;
- current review gate status;
- latest decision record;
- source-evidence draft under review;
- formal evidence gap plan;
- review-gate index entry;
- decision-record index entry;
- no newer superseding artefact exists.

## Required Decision Status Guidance

The checklist must define:

### NOT_REVIEWED

Use when no formal review has occurred.

### NEEDS_REVISION

Use when the draft has been reviewed and is not safe for governed ingestion.

### REVIEWED_READY_FOR_INGESTION

Use only when doctrine review, implementation-state review, evidence-gap coverage review, and non-overclaiming review are all acceptable.

Must state that `REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.

### SUPERSEDED

Use when the draft/gate/decision record has been replaced and must not be used for governed ingestion.

## Required Gate Rules

The checklist must state:

1. A checklist alone does not change review status.
2. A checklist alone does not permit governed ingestion.
3. A checklist alone does not mutate corpus.
4. A checklist alone does not run recapture.
5. A checklist alone does not promote a baseline.
6. `REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.
7. Governed ingestion must be a separate explicit slice.
8. Recapture must happen only after governed ingestion.
9. Promotion requires benchmark, corpus coverage, answer-gap evidence, and ledger update.
10. Minerva must not overstate checklist completion as review approval, ingestion, recapture, or promotion.

## Required Domain-Specific Notes

Include notes for:

### Tax / PAYG

- Tax / PAYG remains BASELINE_REQUIRED.
- Minerva may explain Tax / PAYG but must not calculate PAYG withholding.
- Deterministic services, tax providers, and governed rule packs own PAYG withholding calculation.
- Current decision record is NOT_REVIEWED.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.

### Imports / Actuals

- Imports / Actuals remains BASELINE_REQUIRED.
- Imports / Actuals is not merely file upload or CSV parsing.
- Imported actuals are not the same as calculated payroll truth.
- Pay code and RateType mapping must remain evidence-bearing and reviewable.
- Current decision record is NOT_REVIEWED.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.

## Required Tests

Add focused tests to assert:

1. `FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md` exists.
2. It references the formal evidence control README.
3. It references the review-gate index.
4. It references the decision-record template.
5. It references the decision-record index.
6. It references Tax / PAYG NOT_REVIEWED decision record.
7. It references Imports / Actuals NOT_REVIEWED decision record.
8. It includes all required sections.
9. It defines NOT_REVIEWED.
10. It defines NEEDS_REVISION.
11. It defines REVIEWED_READY_FOR_INGESTION.
12. It defines SUPERSEDED.
13. It states a checklist alone does not change review status.
14. It states a checklist alone does not permit governed ingestion.
15. It states a checklist alone does not mutate corpus.
16. It states a checklist alone does not run recapture.
17. It states a checklist alone does not promote a baseline.
18. It states REVIEWED_READY_FOR_INGESTION permits planning a future governed ingestion slice only.
19. It states Tax / PAYG remains BASELINE_REQUIRED.
20. It states Imports / Actuals remains BASELINE_REQUIRED.
21. It states Minerva must not calculate PAYG withholding.
22. It states Imports / Actuals is not merely file upload or CSV parsing.
23. It states governed ingestion permitted is No for both current domains.
24. It states recapture permitted is No for both current domains.
25. It states promotion permitted is No for both current domains.
26. It does not state Tax / PAYG is BASELINE_ALREADY_EXISTS.
27. It does not state Imports / Actuals is BASELINE_ALREADY_EXISTS.
28. It does not state governed ingestion has occurred.
29. It does not state corpus has been mutated.
30. It does not state ledger has been promoted.

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
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
if (Test-Path .\.pytest_tmp) { Remove-Item -Recurse -Force .\.pytest_tmp }
Test-Path .\.pytest_tmp
git --no-pager status --short
```

# Codex Prompt - Tax / PAYG NOT_REVIEWED Decision Record v0.1

Date: 15 May 2026
Repository: ezeas-intelligence
Slice: Tax / PAYG NOT_REVIEWED Decision Record v0.1
Mode: Documentation/control-record hardening only
Codex behaviour: Auto is acceptable for bounded repo-internal markdown/test edits only. Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, or governed ingestion.

## Platform Context

We are continuing the Minerva completed-domain baseline program and the new knowledge-maintenance operating model.

Current expected ledger state:

- BASELINE_REQUIRED = 17
- BASELINE_ALREADY_EXISTS = 14
- RUNBOOK_OUTSTANDING = 0
- NEEDS_REVIEW = 0
- Total domains = 31

Tax / PAYG remains BASELINE_REQUIRED.

Tax / PAYG currently has:

- formal evidence gap plan
- formal source-evidence draft
- formal evidence review gate
- central review-gate index entry
- reusable formal evidence review decision record template
- detail guard tests for the decision record template

The review gate status remains NOT_REVIEWED.

Governed corpus ingestion remains blocked.

Tax / PAYG must not be promoted.

This slice creates the first filled review decision record, but it must record a NOT_REVIEWED decision only.

## Purpose

Create a filled Tax / PAYG formal evidence review decision record using the reusable decision record template.

The record must prove the workflow can produce durable review decision artefacts without implying review approval.

This is not a review approval slice.

This is not an ingestion slice.

This is not a recapture slice.

This is not a promotion slice.

## Scope

Create:

docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md

Update or add focused tests in:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt at:

docs/codex_prompts/2026-05-15_tax_payg_not_reviewed_decision_record_v0_1.md

## Source Artefacts to Reference

The decision record must reference:

- docs/evaluation/worker_story_baselines/tax_payg/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md
- docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md
- docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md

## Required Decision Record Content

The record must include:

1. Review Decision Record Header
2. Domain and Baseline Status
3. Source Artefacts Reviewed
4. Review Gate Status Before Decision
5. Review Decision
6. Allowed Decision Statuses
7. Doctrine Review Findings
8. Implementation-State Review Findings
9. Evidence-Gap Coverage Findings
10. Non-Overclaiming Review
11. Ingestion Decision
12. Recapture Decision
13. Promotion Decision
14. Reviewer Details
15. Required Follow-Up Actions
16. Minerva Answering Implications
17. Non-Goals / Explicitly Not Changed

## Required Filled Values

The record must state:

- Domain name: Tax / PAYG
- Domain slug: tax_payg
- Baseline status before review: BASELINE_REQUIRED
- Review gate status before decision: NOT_REVIEWED
- Selected decision status: NOT_REVIEWED
- Reviewer name: not assigned
- Review date: not recorded
- Doctrine review outcome: not reviewed
- Implementation-state review outcome: not reviewed
- Evidence-gap review outcome: not reviewed
- Non-overclaiming review outcome: not reviewed
- Governed ingestion permitted: No
- Recapture permitted: No
- Promotion permitted: No

## Required Decision Rules

The record must state:

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate with NOT_REVIEWED blocks governed ingestion.
3. A review gate with NEEDS_REVISION blocks governed ingestion.
4. A SUPERSEDED draft/gate must not be used for governed ingestion.
5. Only REVIEWED_READY_FOR_INGESTION can permit a future governed ingestion slice.
6. REVIEWED_READY_FOR_INGESTION does not itself mutate corpus.
7. REVIEWED_READY_FOR_INGESTION does not itself promote a baseline.
8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence.
9. No domain is promoted merely because a review decision exists.
10. Minerva must not overstate review, ingestion, runtime, or promotion state.

## Tax / PAYG Doctrine to Preserve

The record must state:

- Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps.
- Minerva must not calculate PAYG withholding.
- Deterministic services, tax providers, and governed rule packs own PAYG withholding calculation.
- Tax / PAYG remains BASELINE_REQUIRED until real recapture evidence supports promotion.
- Tax / PAYG has not been approved for governed ingestion.
- No Tax / PAYG corpus mutation has occurred in this slice.
- No Tax / PAYG runtime calculation has been implemented in this slice.
- No Tax / PAYG benchmark recapture has occurred in this slice.

## Required Follow-Up Actions

The record must list future follow-up actions:

1. Assign reviewer.
2. Review Tax / PAYG formal source-evidence draft for doctrine accuracy.
3. Review implementation-state claims.
4. Review evidence-gap coverage.
5. Review non-overclaiming constraints.
6. Decide whether status should remain NOT_REVIEWED, move to NEEDS_REVISION, move to REVIEWED_READY_FOR_INGESTION, or be SUPERSEDED.
7. Only after REVIEWED_READY_FOR_INGESTION, plan a separate governed corpus-ingestion slice.
8. Only after governed ingestion, run recapture.
9. Only after successful benchmark, corpus coverage, and answer-gap evidence, consider ledger promotion.

## Tests

Add focused tests to assert:

1. The Tax / PAYG NOT_REVIEWED decision record exists.
2. It references the formal evidence gap plan.
3. It references the formal source-evidence draft.
4. It references the formal evidence review gate.
5. It references the review-gate index.
6. It references the reusable decision record template.
7. It states Domain name: Tax / PAYG.
8. It states Domain slug: tax_payg.
9. It states baseline status before review is BASELINE_REQUIRED.
10. It states review gate status before decision is NOT_REVIEWED.
11. It states selected decision status is NOT_REVIEWED.
12. It states governed ingestion permitted is No.
13. It states recapture permitted is No.
14. It states promotion permitted is No.
15. It states Minerva must not calculate PAYG withholding.
16. It states Tax / PAYG remains BASELINE_REQUIRED.
17. It states no corpus mutation occurred.
18. It states no benchmark recapture occurred.
19. It states no ledger promotion occurred.
20. It does not state REVIEWED_READY_FOR_INGESTION as the selected decision.
21. It does not state Tax / PAYG is BASELINE_ALREADY_EXISTS.
22. It does not state governed ingestion has occurred.
23. It does not state corpus has been mutated.
24. It does not state ledger has been promoted.

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
- review approval
- governed ingestion

Do not change completed-domain ledger counts.

Do not mark Tax / PAYG as REVIEWED_READY_FOR_INGESTION.

Do not mark Tax / PAYG as BASELINE_ALREADY_EXISTS.

Do not create any runtime Tax / PAYG behaviour.

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

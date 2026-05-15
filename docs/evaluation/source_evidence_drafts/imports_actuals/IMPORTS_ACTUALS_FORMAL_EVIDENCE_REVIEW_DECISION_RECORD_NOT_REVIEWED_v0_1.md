# Imports / Actuals Formal Evidence Review Decision Record NOT_REVIEWED v0.1

Slice: Imports / Actuals NOT_REVIEWED Decision Record v0.1

Date: 15 May 2026

This decision record proves that the Imports / Actuals formal evidence workflow can produce durable review decision artefacts without implying review approval. It records a `NOT_REVIEWED` decision only. It does not approve governed ingestion, recapture, promotion, runtime behaviour or corpus mutation.

## 1. Review Decision Record Header

- Decision record title: Imports / Actuals Formal Evidence Review Decision Record NOT_REVIEWED v0.1
- Decision record version: v0.1
- Domain name: `Imports / Actuals`
- Domain slug: `imports_actuals`
- Review date: not recorded
- Reviewer name: not assigned
- Reviewer rationale: No reviewer has been assigned and no formal review has been performed, so the selected decision status remains `NOT_REVIEWED`.

## 2. Domain and Baseline Status

- Domain name: `Imports / Actuals`
- Domain slug: `imports_actuals`
- Baseline status before review: `BASELINE_REQUIRED`
- Review gate file path: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
- Formal evidence gap plan path: `docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md`
- Formal source-evidence draft path: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md`
- Review gate index path: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- Reusable decision record template path: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`

## 3. Source Artefacts Reviewed

- Reviewed source artefacts: none by an assigned reviewer; this record references the artefacts required for future review.
- Formal evidence gap plan referenced: `docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md`
- Formal source-evidence draft referenced: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md`
- Review gate referenced: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md`
- Review gate index referenced: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- Reusable decision record template referenced: `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`

## 4. Review Gate Status Before Decision

- Current review status before decision: `NOT_REVIEWED`
- Review gate status before decision: `NOT_REVIEWED`
- Baseline status before review: `BASELINE_REQUIRED`
- Governed ingestion permitted before decision: No
- Recapture permitted before decision: No
- Promotion permitted before decision: No

## 5. Review Decision

- Selected decision status: `NOT_REVIEWED`
- Doctrine review outcome: not reviewed
- Implementation-state review outcome: not reviewed
- Evidence-gap review outcome: not reviewed
- Non-overclaiming review outcome: not reviewed
- Reviewer rationale: The Imports / Actuals formal evidence draft and review gate exist, but no assigned reviewer has reviewed doctrine accuracy, implementation-state claims, evidence-gap coverage or non-overclaiming constraints.

## 6. Allowed Decision Statuses

The selected decision status must be exactly one of:

- `NOT_REVIEWED`
- `NEEDS_REVISION`
- `REVIEWED_READY_FOR_INGESTION`
- `SUPERSEDED`

Decision rules:

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate with `NOT_REVIEWED` blocks governed ingestion.
3. A review gate with `NEEDS_REVISION` blocks governed ingestion.
4. A `SUPERSEDED` draft/gate must not be used for governed ingestion.
5. Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice.
6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.
7. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.
8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence.
9. No domain is promoted merely because a review decision exists.
10. Minerva must not overstate review, ingestion, runtime, or promotion state.

## 7. Doctrine Review Findings

- Doctrine review outcome: not reviewed
- Doctrine findings: no doctrine findings have been accepted by an assigned reviewer.
- Doctrine blockers: reviewer not assigned; formal review not performed.
- Doctrine follow-up actions: review Imports / Actuals formal source-evidence draft for doctrine accuracy.

Imports / Actuals doctrine to preserve:

- Imports / Actuals is not merely file upload or CSV parsing.
- Imports / Actuals covers import batches, import rows, validation, errors, warnings, source truth provenance, external actuals, comparison/remediation context, and worker-story explanation context.
- Imported actuals are evidence for reconciliation and comparison; they are not the same as calculated payroll truth.
- Pay code and RateType mapping must remain evidence-bearing and reviewable.
- Mapping ambiguity, unmapped actuals, and unresolved configuration must not be hidden.
- Imports / Actuals remains `BASELINE_REQUIRED` until real recapture evidence supports promotion.
- Imports / Actuals has not been approved for governed ingestion.
- No Imports / Actuals corpus mutation has occurred in this slice.
- No Imports / Actuals runtime import or actuals-ingestion behaviour has been implemented in this slice.
- No Imports / Actuals benchmark recapture has occurred in this slice.

## 8. Implementation-State Review Findings

- Implementation-state review outcome: not reviewed
- Implementation-state findings: no implementation-state findings have been accepted by an assigned reviewer.
- Runtime claims checked: none by an assigned reviewer.
- Implementation-state blockers: reviewer not assigned; formal review not performed.
- Implementation-state follow-up actions: review implementation-state claims before any governed ingestion planning.

No Imports / Actuals runtime import or actuals-ingestion behaviour has been implemented in this slice.

## 9. Evidence-Gap Coverage Findings

- Evidence-gap review outcome: not reviewed
- Required gap terms checked: none by an assigned reviewer.
- Coverage findings: no evidence-gap coverage findings have been accepted by an assigned reviewer.
- Coverage blockers: reviewer not assigned; formal review not performed.
- Evidence-gap follow-up actions: review Imports / Actuals evidence-gap coverage against the formal evidence gap plan.

Imports / Actuals remains `BASELINE_REQUIRED` until real recapture evidence supports promotion.

## 10. Non-Overclaiming Review

- Non-overclaiming review outcome: not reviewed
- Claims that must remain caveated: formal draft exists; review gate exists; decision record exists; selected decision status is `NOT_REVIEWED`; governed ingestion remains blocked; Imports / Actuals remains `BASELINE_REQUIRED`.
- Claims that must not be made: review approval, governed ingestion completion, corpus mutation, runtime Imports / Actuals import behaviour, runtime actuals ingestion behaviour, benchmark recapture, baseline promotion or ledger promotion.
- Non-overclaiming blockers: reviewer not assigned; formal review not performed.
- Non-overclaiming follow-up actions: review non-overclaiming constraints before changing the gate status.

No Imports / Actuals corpus mutation has occurred in this slice. No Imports / Actuals benchmark recapture has occurred in this slice. No Imports / Actuals ledger promotion occurred in this slice.

## 11. Ingestion Decision

- Whether governed ingestion is permitted: No
- Governed ingestion permitted: No
- Governed ingestion decision rationale: The selected decision status is `NOT_REVIEWED`, and a review gate with `NOT_REVIEWED` blocks governed ingestion.
- Ingestion constraints: only after a future decision selects `REVIEWED_READY_FOR_INGESTION` may a separate governed corpus-ingestion slice be planned.

Imports / Actuals has not been approved for governed ingestion. No governed ingestion occurred in this slice.

## 12. Recapture Decision

- Whether recapture is permitted: No
- Recapture permitted: No
- Recapture decision rationale: Recapture is not permitted before governed ingestion or another explicitly documented evidence update.
- Recapture prerequisites: governed ingestion first, then a separate recapture slice with real benchmark, corpus coverage and answer-gap commands.

No Imports / Actuals benchmark recapture has occurred in this slice.

## 13. Promotion Decision

- Whether promotion is permitted: No
- Promotion permitted: No
- Promotion decision rationale: Imports / Actuals remains `BASELINE_REQUIRED`; no review approval, governed ingestion or recapture evidence supports promotion.
- Required promotion evidence: `real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture`

No Imports / Actuals ledger promotion occurred in this slice. No domain is promoted merely because a review decision exists.

## 14. Reviewer Details

- Reviewer name: not assigned
- Review date: not recorded
- Reviewer role or authority: not assigned
- Reviewed source artefacts: none by an assigned reviewer.
- Reviewer rationale: review is not complete, so the only valid decision for this record is `NOT_REVIEWED`.

## 15. Required Follow-Up Actions

1. Assign reviewer.
2. Review Imports / Actuals formal source-evidence draft for doctrine accuracy.
3. Review implementation-state claims.
4. Review evidence-gap coverage.
5. Review non-overclaiming constraints.
6. Decide whether status should remain `NOT_REVIEWED`, move to `NEEDS_REVISION`, move to `REVIEWED_READY_FOR_INGESTION`, or be `SUPERSEDED`.
7. Only after `REVIEWED_READY_FOR_INGESTION`, plan a separate governed corpus-ingestion slice.
8. Only after governed ingestion, run recapture.
9. Only after successful benchmark, corpus coverage, and answer-gap evidence, consider ledger promotion.

## 16. Minerva Answering Implications

- Minerva may say: Imports / Actuals has a formal evidence gap plan, a formal source-evidence draft, a formal review gate, an index entry and a `NOT_REVIEWED` decision record.
- Minerva may explain Imports / Actuals doctrine, source evidence, implementation state, and known gaps.
- Minerva must not say: Imports / Actuals has been reviewed, approved for governed ingestion, ingested into corpus by this slice, recaptured by this slice, implemented as runtime import or actuals-ingestion behaviour, or promoted.
- Review implication: review state remains `NOT_REVIEWED`.
- Ingestion implication: governed ingestion remains blocked.
- Runtime implication: Imports / Actuals runtime import and actuals-ingestion behaviour have not been implemented in this slice.
- Promotion implication: Imports / Actuals remains `BASELINE_REQUIRED`.

Minerva must not overstate review, ingestion, runtime, or promotion state.

## 17. Non-Goals / Explicitly Not Changed

This decision record does not implement:

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
- import runtime changes
- actuals ingestion runtime changes
- reconciliation runtime changes
- review approval
- governed ingestion

It does not change completed-domain ledger counts. It does not mark Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`. It does not mark Imports / Actuals as `BASELINE_ALREADY_EXISTS`. It does not create runtime Imports / Actuals behaviour.

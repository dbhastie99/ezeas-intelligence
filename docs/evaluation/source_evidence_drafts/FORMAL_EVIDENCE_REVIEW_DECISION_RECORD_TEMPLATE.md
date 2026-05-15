# Formal Evidence Review Decision Record Template

Slice: Minerva Formal Evidence Review Decision Record Template v0.1

Date: 15 May 2026

This reusable template records a formal reviewer decision for a Minerva source-evidence draft and review gate. It is a documentation/control artefact only. It does not ingest evidence, mutate corpus, mutate the database, run recapture, promote a baseline, promote the ledger, change endpoints, change runtime behaviour or create generated artefacts.

Copy this template into a domain-specific decision record only when a formal review decision is being made. Do not treat draft text, chat agreement or file existence as review approval.

## 1. Review Decision Record Header

- Decision record title: `<domain name> Formal Evidence Review Decision Record <version>`
- Decision record version: `<version>`
- Domain name: `<domain name>`
- Domain slug: `<domain slug>`
- Review date: `<YYYY-MM-DD>`
- Reviewer name: `<reviewer name>`
- Reviewer rationale: `<brief rationale for the selected decision status>`

## 2. Domain and Baseline Status

- Domain name: `<domain name>`
- Domain slug: `<domain slug>`
- Baseline status before review: `<BASELINE_REQUIRED | BASELINE_ALREADY_EXISTS | other recorded status>`
- Review gate file path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_EVIDENCE_REVIEW_GATE_...md>`
- Formal evidence gap plan path: `<docs/evaluation/worker_story_baselines/.../FORMAL_EVIDENCE_GAP_PLAN.md>`
- Formal source-evidence draft path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_SOURCE_EVIDENCE_DRAFT_...md>`
- Review gate index path: `<docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md>`

## 3. Source Artefacts Reviewed

- Reviewed source artefacts: `<list every artefact reviewed>`
- Baseline summary reviewed: `<path or not applicable>`
- Benchmark evidence reviewed: `<path or not applicable>`
- Corpus coverage evidence reviewed: `<path or not applicable>`
- Answer-gap evidence reviewed: `<path or not applicable>`
- Review gate reviewed: `<path>`
- Formal source-evidence draft reviewed: `<path>`
- Formal evidence gap plan reviewed: `<path>`

## 4. Review Gate Status Before Decision

- Current review status before decision: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`
- Baseline status before review: `<recorded baseline status before this decision>`
- Governed ingestion permitted before decision: `<Yes | No>`
- Recapture permitted before decision: `<Yes | No>`
- Promotion permitted before decision: `<Yes | No>`

## 5. Review Decision

- Selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`
- Doctrine review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`
- Implementation-state review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`
- Evidence-gap review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`
- Non-overclaiming review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`
- Reviewer rationale: `<why this decision is correct>`

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
8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.
9. No domain is promoted merely because a review decision exists.
10. Minerva must not overstate review, ingestion, runtime, or promotion state.

## 7. Doctrine Review Findings

- Doctrine review outcome: `<outcome>`
- Doctrine findings: `<findings>`
- Doctrine blockers: `<none or list>`
- Doctrine follow-up actions: `<none or list>`

## 8. Implementation-State Review Findings

- Implementation-state review outcome: `<outcome>`
- Implementation-state findings: `<findings>`
- Runtime claims checked: `<claims checked>`
- Implementation-state blockers: `<none or list>`
- Implementation-state follow-up actions: `<none or list>`

## 9. Evidence-Gap Coverage Findings

- Evidence-gap review outcome: `<outcome>`
- Required gap terms checked: `<terms checked>`
- Coverage findings: `<findings>`
- Coverage blockers: `<none or list>`
- Evidence-gap follow-up actions: `<none or list>`

## 10. Non-Overclaiming Review

- Non-overclaiming review outcome: `<outcome>`
- Claims that must remain caveated: `<claims>`
- Claims that must not be made: `<claims>`
- Non-overclaiming blockers: `<none or list>`
- Non-overclaiming follow-up actions: `<none or list>`

## 11. Ingestion Decision

- Whether governed ingestion is permitted: `<Yes | No>`
- Governed ingestion decision rationale: `<rationale>`
- Ingestion constraints: `<future governed ingestion slice requirements or not applicable>`

Governed ingestion is permitted only when the selected decision status is `REVIEWED_READY_FOR_INGESTION`. Even then, this decision record only permits a future governed ingestion slice; it does not perform ingestion or mutate corpus.

## 12. Recapture Decision

- Whether recapture is permitted: `<Yes | No>`
- Recapture decision rationale: `<rationale>`
- Recapture prerequisites: `<required ingestion/evidence state before recapture>`

Recapture must not be treated as permitted merely because a draft exists or because a review decision exists. Recapture follows governed ingestion or another explicitly documented evidence update.

## 13. Promotion Decision

- Whether promotion is permitted: `<Yes | No>`
- Promotion decision rationale: `<rationale>`
- Required promotion evidence: `real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture`

No domain is promoted merely because a review decision exists. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.

## 14. Reviewer Details

- Reviewer name: `<reviewer name>`
- Review date: `<YYYY-MM-DD>`
- Reviewer role or authority: `<role>`
- Reviewed source artefacts: `<list>`
- Reviewer rationale: `<rationale>`

## 15. Required Follow-Up Actions

- Required follow-up actions: `<none or list>`
- Owner: `<owner>`
- Due date or trigger: `<date or trigger>`
- Blocking status: `<blocking | non-blocking>`

## 16. Minerva Answering Implications

- Minerva may say: `<allowed answer implication>`
- Minerva must not say: `<blocked answer implication>`
- Review implication: `<how Minerva should describe review state>`
- Ingestion implication: `<how Minerva should describe ingestion state>`
- Runtime implication: `<how Minerva should describe runtime state>`
- Promotion implication: `<how Minerva should describe baseline and ledger state>`

Minerva must not overstate review, ingestion, runtime, or promotion state. It must not describe a formal source-evidence draft as ingested corpus evidence unless a later governed ingestion artefact records that fact.

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
- tax runtime changes

It does not change completed-domain ledger counts.

## Domain Example Placeholders

These examples are placeholders for future completed decision records. They do not mark either domain as reviewed or ready.

### Imports / Actuals

- Domain name: `Imports / Actuals`
- Domain slug: `imports_actuals`
- Baseline status before review: `BASELINE_REQUIRED`
- Example current review status before decision: `NOT_REVIEWED`
- Example selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | SUPERSEDED, unless a future reviewer explicitly selects REVIEWED_READY_FOR_INGESTION>`
- Governed ingestion permitted: No unless `REVIEWED_READY_FOR_INGESTION`
- Promotion permitted: No
- Note: Imports / Actuals is not merely file upload or CSV parsing.

### Tax / PAYG

- Domain name: `Tax / PAYG`
- Domain slug: `tax_payg`
- Baseline status before review: `BASELINE_REQUIRED`
- Example current review status before decision: `NOT_REVIEWED`
- Example selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | SUPERSEDED, unless a future reviewer explicitly selects REVIEWED_READY_FOR_INGESTION>`
- Governed ingestion permitted: No unless `REVIEWED_READY_FOR_INGESTION`
- Promotion permitted: No
- Note: Minerva may explain Tax / PAYG but must not calculate PAYG withholding.

# Historical Backfill Execution Design

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the future execution model for Minerva historical backfill after an ingestion/backfill decision has been approved for planning.

This slice only designs future execution.

It does not execute backfill.

It does not ingest historical source content.

It does not create or mutate corpus records.

It does not create Code Evidence.

It does not write to the database.

It does not call a live LLM.

It does not promote current truth.

It does not permit answer use.

It does not expose chat.

## 2. Scope

This design applies only after a governed decision-control artefact exists under `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md` and the decision status permits future backfill planning.

The execution design is a control model, not an executable process. A later explicit dry-run slice is required before a dry run may occur. A later explicit apply slice is required before any corpus mutation or database write may occur.

## 3. Conservative Permission Defaults

Every planned historical backfill execution starts with these values:

| Permission | Default |
| --- | --- |
| `BackfillExecutionPermitted` | No |
| `BackfillDryRunPermitted` | No, unless a later explicit dry-run slice approves it |
| `CorpusMutationPermitted` | No |
| `DatabaseWritePermitted` | No |
| `CurrentTruthPromotionPermitted` | No |
| `AnswerUsePermitted` | No |
| `ChatExposurePermitted` | No |
| `CodeEvidenceIngestionPermitted` | No |
| `LiveLLMUsePermitted` | No |

These defaults remain No unless a later governed slice explicitly changes the specific permission. Approval to plan execution is not approval to dry-run, apply, mutate corpus, write a database, promote current truth, permit answer use, ingest Code Evidence, call a live LLM, or expose chat.

## 4. Future Backfill Stages

| Stage | Required control result |
| --- | --- |
| `DECISION_APPROVED` | A linked ingestion/backfill decision-control record exists and permits future backfill planning only. |
| `SOURCE_SCOPE_FROZEN` | Source set, source versions, source register ids, and excluded sources are fixed before extraction planning. |
| `SOURCE_AUTHORITY_CHECKED` | Source tier, review status, implementation-state classification, and governing authority are confirmed. |
| `SUPERSESSION_CONFLICT_CHECKED` | Superseded material is excluded or labelled historical-only; unresolved conflict remains blocked. |
| `DUPLICATE_LINKING_CHECKED` | Existing evidence is linked before new extraction is planned; duplicate truth is not created. |
| `SENSITIVITY_TENANT_RISK_CHECKED` | Sensitive data and tenant-data risk are assessed before any dry-run package is prepared. |
| `EVIDENCE_EXTRACTION_PLAN_PREPARED` | Extraction boundaries, fields, provenance, and exclusions are documented without extracting source content in this slice. |
| `BACKFILL_DRY_RUN_PREPARED` | Dry-run inputs and expected non-destructive outputs are prepared for a later explicit dry-run slice. |
| `BACKFILL_DRY_RUN_REVIEWED` | Dry-run output is reviewed in a later slice before any apply approval can be considered. |
| `BACKFILL_APPLY_APPROVED` | Apply requires separate reviewer approval after dry-run review. |
| `BACKFILL_APPLY_EXECUTED_FUTURE_SLICE` | Backfill apply is executed only in a future explicit slice, not here. |
| `POST_BACKFILL_VALIDATION` | Validation checks provenance, duplicate links, rollback metadata, and no unintended answer-use exposure. |
| `CURRENT_TRUTH_PROMOTION_DECISION_SEPARATE` | Current-truth promotion remains a separate governed decision. |
| `ANSWER_USE_DECISION_SEPARATE` | Answer-use permission remains a separate governed decision. |

## 5. Stage Requirements

### Decision Approved

Backfill execution planning may only begin when the decision-control record references an approved planning status, the required source review status is present, and all blockers relevant to planning are cleared or explicitly deferred with rationale.

`BACKFILL_DECISION_APPROVED_FOR_PLANNING_ONLY` and `BACKFILL_READY_PENDING_EXECUTION_PLAN` do not permit execution, dry-run, corpus mutation, database write, current-truth promotion, answer use, or chat exposure.

### Source Scope Frozen

The source scope must record:

- `SourceRegisterId`
- source version or date
- source review status
- included finding ids
- excluded finding ids
- excluded source sections or evidence groups
- historical-only boundaries
- superseded-source boundaries
- duplicate evidence links

Scope changes after freeze require a new review of source authority, supersession, conflict, duplicate, sensitivity, tenant-data risk, and extraction plan.

### Source Authority Checked

Source authority must confirm whether the source is code/test authority, formal source evidence, developer log, hardening log, platform doctrine, chat or continuance material, prompt file, baseline pack, or other reviewed source.

Lower-authority historical material must not override higher-authority current repository truth. Historical-only material may be retained only under historical labels.

### Supersession and Conflict Checked

Superseded source handling must identify the controlling newer source and preserve the historical finding only as historical context unless a later governed current-truth decision says otherwise.

Conflicting finding handling must block backfill planning until conflict resolution is recorded. A conflict cannot be bypassed by labelling a source reviewed.

### Duplicate Linking Checked

Duplicate handling must link to existing reviewed evidence or existing corpus records before any new extraction target is planned. Duplicate findings should not create duplicate truth.

### Sensitivity and Tenant-Data Risk Checked

Sensitive data and tenant-data risk must be assessed before dry-run preparation. Any tenant-specific, personal, credential, secret, customer-specific, or unsuitable operational detail must be excluded, quarantined, redacted, or blocked before any future dry-run slice.

### Evidence Extraction Plan Prepared

The evidence extraction plan must identify:

- extraction scope
- excluded material
- provenance fields
- target labels
- historical-only labels
- duplicate links
- supersession labels
- conflict labels
- rollback/removal identifiers
- validation expectations

This slice does not extract source content.

### Dry-Run First

A dry run is required before any apply approval. Dry-run preparation in this design does not permit the dry run itself. `BackfillDryRunPermitted` remains No unless a later explicit dry-run slice approves it.

### Apply Approval and Future Execution

Backfill apply requires a reviewed dry-run result, a completed audit record, explicit reviewer approval, and a future explicit apply slice. This design does not execute apply.

### Post-Backfill Validation

Post-backfill validation must prove the future apply stayed within approved scope, preserved provenance, linked duplicates, respected historical-only labels, avoided tenant/sensitive data, and did not grant current-truth, answer-use, chat exposure, Code Evidence ingestion, live LLM use, or uncontrolled database writes.

Post-backfill validation may identify a current-truth candidate for later assessment under `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`. Candidate identification does not promote current truth, permit answer use, mutate corpus, write a database, call a live LLM, ingest source content, create Code Evidence, or expose chat.

## 6. Required Artefacts

Future execution planning must use:

- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_SAFETY_CHECKLIST.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_AUDIT_RECORD_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_REVIEW_CHECKLIST.md`

## 7. Explicit Non-Goals

- Do not ingest source content.
- Do not mutate operational corpus.
- Do not create Code Evidence.
- Do not write to database.
- Do not call live LLM.
- Do not promote current truth.
- Do not permit answer use.
- Do not expose chat.
- Do not add endpoints.
- Do not add UI.
- Do not modify runtime answer behaviour.
- Do not fabricate benchmark, coverage, answer gap, or DB-backed results.

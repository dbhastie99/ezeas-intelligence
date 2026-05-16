# Historical Backfill Execution Runbook

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This runbook describes how a future Minerva historical backfill execution should be prepared after an ingestion/backfill decision has been approved for planning.

This slice is design/control only. It does not execute backfill, ingest source content, mutate corpus, create Code Evidence, write to a database, call a live LLM, promote current truth, permit answer use, or expose chat.

## 2. Prerequisites

Before future backfill execution planning begins:

- Required decision-control artefact exists.
- Required source review status is complete and linked.
- Required blocker clearance is recorded.
- Source scope is frozen.
- Source authority is confirmed.
- Supersession is checked.
- Conflict is checked.
- Duplicate status is checked.
- Sensitive data and tenant-data risk are checked.
- Current-truth promotion remains separate.
- Answer-use permission remains separate.

## 3. Required Decision-Control Artefact

The future execution record must link to a completed ingestion/backfill decision record created from `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_TEMPLATE.md`.

Acceptable upstream statuses are planning-only statuses such as `BACKFILL_DECISION_APPROVED_FOR_PLANNING_ONLY` or `BACKFILL_READY_PENDING_EXECUTION_PLAN`. These statuses do not permit dry-run, apply, corpus mutation, database write, current-truth promotion, answer use, or chat exposure.

## 4. Required Source Review Status

Every source in scope must have a governed review status that supports backfill planning. A source that remains `NOT_REVIEWED`, unresolved, superseded, conflicting, duplicate-unlinked, sensitive-risk-blocked, tenant-risk-blocked, or historical-only without boundary labels must not proceed.

## 5. Required Blocker Clearance

Blockers from `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md` must be cleared or explicitly deferred with rationale before dry-run preparation. Deferred blockers must not affect write safety, source authority, duplicate handling, supersession, conflict resolution, sensitive data, tenant data, provenance, rollback, answer-use, or current-truth boundaries.

## 6. Dry-Run-First Requirement

A dry run is mandatory before any apply approval.

This runbook does not approve a dry run. `BackfillDryRunPermitted` remains No unless a later explicit dry-run slice approves it.

A dry-run package must be non-destructive and must not write corpus records, operational corpus, Code Evidence, database tables, migrations, runtime configuration, answer routing, chat state, or generated benchmark/coverage/answer-gap artefacts as durable truth.

## 7. Evidence Extraction Boundaries

The extraction plan must list the exact findings and evidence fields proposed for future dry-run extraction. It must exclude:

- unreviewed source content
- superseded current-truth claims
- unresolved conflicts
- duplicate evidence without links
- tenant-specific data
- personal data
- credentials or secrets
- unsupported implementation-state claims
- backlog or follow-up items represented as implemented behaviour

This runbook does not extract source content.

## 8. Duplicate Handling

Duplicate handling must prefer links to existing reviewed evidence. If the same finding already exists in a governed corpus or evidence artefact, the future backfill plan must link to that record rather than create duplicate truth.

## 9. Superseded Source Handling

Superseded source handling must identify the newer controlling source. Superseded findings may be retained only as historical-only context unless a later current-truth promotion control explicitly approves a different status.

## 10. Conflicting Finding Handling

Conflicting findings are blocked until a conflict-resolution record identifies the controlling source, rejected source, or historical-only treatment. Conflict resolution must occur before dry-run preparation.

## 11. Historical-Only Source Handling

Historical-only sources may support historical provenance and rationale records only. They must not become current truth and must not support answers without separate current-truth and answer-use decisions.

## 12. Audit Record Requirement

Every future dry-run or apply planning record must use `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_AUDIT_RECORD_TEMPLATE.md` or an approved successor.

The audit record must record whether corpus mutation, database write, current-truth promotion, answer-use permission, Code Evidence ingestion, live LLM use, or chat exposure occurred. For this design slice, all such execution fields remain No or not performed.

## 13. Rollback and Non-Destructive Expectations

Future execution planning must include rollback/removal expectations before any write can be approved. Provenance must be sufficient to quarantine, remove, or reverse future backfilled records.

Dry-run preparation must be non-destructive. Apply execution may occur only in a future explicit slice.

## 14. Post-Backfill Validation

Post-backfill validation must confirm:

- approved scope was not exceeded
- source provenance is preserved
- duplicate links were used
- superseded material is labelled or excluded
- conflicts are resolved or excluded
- sensitive data and tenant data are absent or controlled
- rollback/removal metadata exists
- no current-truth promotion is implied
- no answer-use permission is implied
- no chat exposure is implied

## 15. Handoff to Current-Truth Promotion Control

Backfill completion does not make evidence current truth.

The next governed stage after successful future backfill validation is an explicit handoff to current-truth promotion control. Answer-use permission remains separate even if current-truth promotion is later approved.

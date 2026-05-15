# Historical Source Review Readiness Process

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This process defines how a registered historical source is reviewed for readiness before it can support a curated historical backfill evidence pack.

A registered source is not final truth merely because it exists in the register. Registration records provenance, source type, starting tier, and control state; it does not approve historical claims.

Review readiness is required before creating a historical backfill evidence pack.

This slice creates templates/process only and does not review, ingest, parse, or consume any historical source.

## 2. Required Inputs

Before review-readiness work begins, read:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/registered_sources/`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md`

## 3. Review Principles

The review must distinguish implemented behaviour, doctrine, backlog, planned-not-implemented work, superseded work, and uncertain claims.

Developer logs and doctrine documents require implementation-state classification because they can contain implemented decisions, rationale, future work, partial work, obsolete notes, and backlog.

Historical chats and continuance prompts require cross-checking and are raw source material, not final truth.

Code/tests are strongest for implemented state but may not explain decision rationale.

A source may be reviewed for backfill draft readiness without permitting governed ingestion.

Review readiness does not mutate corpus, does not ingest the source, does not run Code Evidence integration, does not call live LLM, does not change runtime, does not promote baselines, does not change ledger counts, and does not perform ledger promotion.

## 4. Controlled Review Status Values

Use one target review status:

- `NOT_REVIEWED`
- `NEEDS_REVIEW`
- `REVIEWED_READY_FOR_BACKFILL_DRAFT`
- `REVIEWED_READY_FOR_GOVERNED_INGESTION`
- `SUPERSEDED`

`REVIEWED_READY_FOR_BACKFILL_DRAFT` means the source can support a draft curated backfill evidence pack. It does not permit governed ingestion.

`REVIEWED_READY_FOR_GOVERNED_INGESTION` can only be targeted when the review records sufficient provenance, implementation-state classification, supersession handling, cross-checking, and a separate governed ingestion path is still required.

## 5. Controlled Implementation-State Classifications

Use one target implementation-state classification unless the review rationale records why multiple candidate claims require separate classifications:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## 6. Review Workflow

1. Confirm the source has a row in `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`.
2. Confirm the source folder and registered source type match the register-driven classification model.
3. Copy `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md` into the future review output location approved by the slice.
4. Record source identity, review owner, review date, review status before review, ingestion permission before review, current implementation-state classification, supersession status, and evidence confidence.
5. Extract candidate decisions, candidate doctrine, candidate backlog items, and candidate implemented-state claims without treating them as final truth.
6. Determine whether code/test/commit cross-checking is required.
7. Cross-check candidate implemented-state claims against current code, tests, commits, database views, schema/scripts, logs, and doctrine where relevant.
8. Record superseded or conflicting claims.
9. Assign current truth classification and Minerva answering implication.
10. Recommend one of: blocked, ready for backfill draft, or future governed-ingestion consideration.
11. Keep `Target ingestion permitted` as `No` unless a later explicit governed ingestion slice authorizes a change.

## 7. Analytics Engine Developer Log State

The Analytics Engine developer log registered as `HIST-ANALYTICS-2025-12-06-20` remains `NOT_REVIEWED` and ingestion permitted `No`.

This process slice does not review the Analytics Engine source, does not ingest it, does not parse it, and does not consume it. Any review of that source requires a future explicit review slice.

## 8. Non-Goals

This process does not mutate corpus, does not ingest historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not ingest sources, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not run Code Evidence integration, does not connect Code Evidence, does not call live LLM, does not run live LLM, does not change runtime, does not change runtime behaviour, does not promote baselines, does not change ledger counts, and does not perform ledger promotion.

This process does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, historical ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.

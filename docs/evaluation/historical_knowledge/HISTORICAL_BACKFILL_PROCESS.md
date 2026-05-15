# Historical Backfill Process

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This process defines the domain-scoped historical knowledge backfill workflow for Minerva.

Pre-control-model historical knowledge is incomplete and not yet captured to the same durable standard as the new formal-evidence model.

## 2. Implementation-State Classifications

Use exactly one current classification for each candidate decision unless the review gate records why multiple states apply:

| Classification | Meaning |
| --- | --- |
| `IMPLEMENTED_AND_TESTED` | Code and tests confirm the behaviour is implemented and covered by focused tests. |
| `IMPLEMENTED_NOT_FULLY_TESTED` | Code confirms the behaviour is implemented, but test coverage is missing, partial, or indirect. |
| `DOCUMENTED_DOCTRINE` | Doctrine records a durable intended model, but implementation is not confirmed by code/tests in the evidence pack. |
| `DOCUMENTED_BACKLOG` | Source material records desired or accepted future work that is not implemented in the reviewed state. |
| `PLANNED_NOT_IMPLEMENTED` | Source material records planned work, but code/tests/commits do not confirm implementation. |
| `SUPERSEDED` | Later source material, code, tests, commits, or doctrine replace the candidate decision. |
| `UNCERTAIN_REQUIRES_REVIEW` | Evidence conflicts, provenance is insufficient, or implementation state cannot be classified without further review. |

## 3. Domain-Scoped Backfill Workflow

1. Identify historical source material for one domain.
2. Register source provenance, including file path, date where available, author/reviewer where available, and source type.
3. Classify source tier using `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`.
4. Extract candidate decisions without treating them as final truth.
5. Cross-check against code/tests/logs/doctrine/commits.
6. Classify implementation state using the classifications in this process.
7. Create a curated backfill evidence pack for the domain.
8. Add a review gate that records reviewer, date, rationale, unresolved conflicts, and approval/blocked status.
9. Only later consider governed ingestion in a separate explicit slice.

## 4. Historical Chat Handling

Historical chats and continuance prompts are raw source material, not final truth.

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits before any candidate decision can be classified.

## 5. Priority Domains

Future historical backfill should prioritize:

- Worker Story
- ObjectTime / Source Truth
- Process Periods / PayRun Lifecycle
- Payroll Buckets / Bases / Totals
- Deductions and Obligations
- Tax / PAYG
- Imports / Actuals
- Leave Workflow / Annual Leave
- Award Configurator
- Asphalt Award Build

Tax / PAYG and Imports / Actuals remain governed by the formal evidence control model and remain `BASELINE_REQUIRED` and `NOT_REVIEWED` until their separate formal review path changes.

## 6. Slice Boundaries

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This process does not mark any domain `REVIEWED_READY_FOR_INGESTION`. It does not mark any domain `BASELINE_ALREADY_EXISTS`.

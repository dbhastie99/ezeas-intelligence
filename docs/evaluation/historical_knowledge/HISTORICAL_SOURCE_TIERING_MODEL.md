# Historical Source Tiering Model

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This model defines how future Minerva historical backfill work must rank and review source material before any governed ingestion is considered.

Pre-control-model historical knowledge is incomplete and not yet captured to the same durable standard as the new formal-evidence model.

## 2. Source Tiers

| Tier | Source material | Authority | Required handling |
| --- | --- | --- | --- |
| Tier 1 | Code and tests | Highest authority for implemented state | Use to confirm implemented behaviour. Preserve that code alone may not explain why a decision was made. |
| Tier 2 | Developer logs, hardening logs, and platform doctrine | Curated decision/rationale sources requiring review | Treat as valuable but review for planned, partial, superseded, or backlog work before classification. |
| Tier 3 | Historical chats and continuance prompts | Raw historical source material, not final truth | Do not ingest directly as truth. Cross-check against logs, doctrine, code, tests, and commits. |

## 3. Cross-Check Rules

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits.

Developer logs and doctrine documents are valuable but may include planned, partial, superseded, or backlog work, so they require implementation-state classification.

Code/tests must be used to confirm implemented behaviour, but code alone may not explain why.

## 4. Slice Boundaries

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

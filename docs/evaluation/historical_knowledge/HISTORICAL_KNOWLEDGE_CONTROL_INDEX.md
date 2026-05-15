# Historical Knowledge Control Index

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This index establishes the Minerva historical knowledge backfill control model before any historical chats, developer logs, hardening logs, platform doctrine, continuance prompts, code evidence, or code-derived evidence are ingested.

Pre-control-model historical knowledge is incomplete and is not yet captured to the same durable standard as the new formal-evidence model. Historical knowledge must therefore be treated as unbackfilled and unapproved until a future domain-scoped backfill process creates reviewed evidence.

## 2. Control Artefacts

Use these durable controls together:

| Control stage | Artefact |
| --- | --- |
| Historical knowledge control index | `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md` |
| Historical knowledge gap register | `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md` |
| Historical source tiering model | `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md` |
| Historical backfill process | `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md` |

## 3. Source Authority Summary

Tier 1 code and tests are the highest authority for implemented state.

Tier 2 developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review.

Tier 3 historical chats and continuance prompts are raw historical source material, not final truth.

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits.

Developer logs and doctrine documents are valuable but may include planned, partial, superseded, or backlog work, so they require implementation-state classification.

Code/tests must be used to confirm implemented behaviour, but code alone may not explain why.

## 4. Backfill Scope

Historical backfill must be domain-scoped. A future slice must identify source material, register provenance, classify source tier, extract candidate decisions, cross-check evidence, classify implementation state, create a curated backfill evidence pack, add a review gate, and only later consider governed ingestion.

This index does not grant permission for ingestion or promotion.

## 5. Initial Priority Domains

Future historical backfill should start with these priority domains:

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

## 6. Current Permission State

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This slice does not mark any domain `REVIEWED_READY_FOR_INGESTION`. It does not mark any domain `BASELINE_ALREADY_EXISTS`.

## 7. How Minerva Should Use This Index

Minerva should use this index as the starting point for historical knowledge control state.

Minerva must preserve that pre-control-model historical knowledge is incomplete and unapproved. Minerva must not treat historical chats, continuance prompts, developer logs, hardening logs, doctrine, code, tests, or commits as governed historical corpus merely because they exist.

## 8. How Codex Should Use This Index

Future Codex slices must read this index, the gap register, the source tiering model, and the backfill process before creating any historical backfill evidence pack or proposing historical ingestion.

Any future historical ingestion, governed ingestion, review approval, recapture, promotion, ledger update, runtime change, endpoint change, UI change, Code Evidence connection, live LLM call, DB write, migration, benchmark execution, corpus coverage execution, answer-gap execution, or generated artefact creation requires a separate explicit slice.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_historical_knowledge_control_index_v0_1.md`.

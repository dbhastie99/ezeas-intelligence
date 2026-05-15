# Historical Knowledge Gap Register

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This register records the current controlled gap: pre-control-model historical knowledge is incomplete and not yet captured to the same durable standard as the new formal-evidence model.

The presence of historical chats, continuance prompts, developer logs, hardening logs, platform doctrine, code, tests, or commits does not mean historical knowledge has been reviewed, backfilled, ingested, or promoted.

## 2. Current Gap

| Gap | Current state | Control position |
| --- | --- | --- |
| Historical chats and continuance prompts | Not consumed by this slice | Raw source material only, not final truth |
| Developer logs and hardening logs | Not ingested by this slice | Valuable rationale sources requiring review and implementation-state classification |
| Platform doctrine documents | Not ingested by this slice | Curated doctrine source requiring review and implementation-state classification |
| Code and tests | Not ingested by this slice | Highest authority for implemented state when reviewed in a future domain-scoped pack |
| Commits | Not ingested by this slice | Cross-check source for future provenance and implementation review |

## 3. Priority Domains

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

## 4. Slice Boundaries

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This slice does not mark any domain `REVIEWED_READY_FOR_INGESTION`. It does not mark any domain `BASELINE_ALREADY_EXISTS`.

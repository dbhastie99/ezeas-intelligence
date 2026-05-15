# Minerva Historical Analytics Review Decision Gate v0.1

Date: 15 May 2026

## Purpose

Create a review decision gate for the registered Analytics Engine historical source before any future backfill evidence pack can be approved.

This slice must not review, ingest, parse, or treat the historical analytics source as current truth.

## Context

The historical Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20`.

It has a source placeholder, review-readiness record, analytics review pack template, and draft placeholder. It remains `NOT_REVIEWED`, ingestion permitted `No`, and historical source material only.

The source covers `ProcessedRule`-era analytics and must be reviewed against the current `CalcInterpreterLine` analytics direction before being used in Minerva.

## Create

Create:

- `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md`

Update if needed:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`
- `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`

## Gate Requirements

The review decision gate must include:

1. Purpose
2. Source Register Details
3. Current Status
4. Review Preconditions
5. Required Cross-Checks
6. Allowed Review Decisions
7. Decision Rules
8. Minerva Answering Boundaries
9. Backfill/Ingestion Boundaries
10. Non-Goals
11. Required Follow-Up Actions

Current status must state:

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: Developer Log - Analytics Engine
- Original filename: Developer Log - Analytics Engine (5).docx
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Current truth classification: not current final truth
- `ProcessedRule`-era analytics: historical and requires review
- `CalcInterpreterLine`: current target calculation fact source
- Code/test/schema cross-check: required but not performed
- Review owner: not assigned
- Review date: not recorded

Allowed review decisions must include:

- `REMAIN_NOT_REVIEWED`
- `NEEDS_SOURCE_REVIEW`
- `REVIEWED_READY_FOR_BACKFILL_DRAFT`
- `REVIEWED_READY_FOR_GOVERNED_INGESTION`
- `SUPERSEDED`

Decision rules must state:

- `REMAIN_NOT_REVIEWED` keeps ingestion permitted No.
- `NEEDS_SOURCE_REVIEW` keeps ingestion permitted No.
- `REVIEWED_READY_FOR_BACKFILL_DRAFT` permits creating a curated backfill evidence pack draft only, not governed ingestion.
- `REVIEWED_READY_FOR_GOVERNED_INGESTION` can only be considered after source review, code/test/schema cross-check, supersession assessment, and reviewer rationale are complete.
- `SUPERSEDED` means the historical source must not be used as current truth and should only be cited for history if appropriate.
- No decision in this gate mutates corpus by itself.
- No decision in this gate promotes a baseline by itself.
- No decision in this gate changes runtime behaviour.

Required cross-checks must include:

- Current workforce-platform code and tests.
- Current ezeas-analytics architecture/control docs if available.
- Current database schema/view definitions where available.
- Commits related to analytics views/source facts if known.
- Current `CalcInterpreterLine`, `PayrollBucketResult`, and reconciliation model direction.
- Historical `ProcessedRule`-era claims and whether they are still valid, partially valid, superseded, or uncertain.

Minerva answering boundaries must state:

- Minerva must not answer from this source as current truth while the gate remains `NOT_REVIEWED`.
- Minerva may later use this source for historical context only after review/backfill controls allow it.
- `ProcessedRule`-era analytics must not be presented as the current canonical calculation fact source unless future review proves it remains valid.
- `CalcInterpreterLine` remains the current target canonical calculation fact source unless future platform evidence changes that.

Backfill/Ingestion boundaries must state:

- This gate does not ingest historical content.
- This gate does not parse or extract source content.
- This gate does not create a backfill evidence pack.
- This gate does not permit governed ingestion while status remains `NOT_REVIEWED`.
- This gate does not mutate corpus, connect Code Evidence, call live LLM, run benchmark, run corpus coverage, run answer-gap reporting, promote baseline, or change ledger counts.

## Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. `HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md` exists.
2. It contains Register ID `HIST-ANALYTICS-2025-12-06-20`.
3. It references Developer Log - Analytics Engine.
4. It records review status `NOT_REVIEWED`.
5. It records ingestion permitted No.
6. It records current truth classification not current final truth.
7. It records code/test/schema cross-check required but not performed.
8. It lists all allowed review decisions.
9. It states `REVIEWED_READY_FOR_BACKFILL_DRAFT` permits a backfill evidence pack draft only, not governed ingestion.
10. It states `REVIEWED_READY_FOR_GOVERNED_INGESTION` requires source review, code/test/schema cross-check, supersession assessment, and reviewer rationale.
11. It states Minerva must not answer from this source as current truth while `NOT_REVIEWED`.
12. It states `ProcessedRule`-era analytics must not be presented as the current canonical calculation fact source unless future review proves it.
13. It states `CalcInterpreterLine` remains the current target canonical calculation fact source.
14. It states no corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur.
15. `HISTORICAL_SOURCE_REGISTER.md` references the review decision gate path.
16. The review-readiness record or review pack draft placeholder references the review decision gate path.

## Explicit Non-Goals

Do not ingest historical chats. Do not ingest the full developer log. Do not parse or extract source content. Do not ingest doctrine documents. Do not ingest code. Do not review the Analytics Engine source yet. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Required Verification

Run:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `git diff --check`

Clean `.pytest_tmp` if present.

Report files changed, analytics review decision gate created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-review-decision-gate-v01`.

# Minerva Historical Batch Register Index v0.1

Date: 15 May 2026

## Purpose

Create the durable prompt/control artefact for the Minerva Historical Batch Register Index v0.1 slice, then execute it.

The purpose is to create a master index for historical batch registers so future developer-log, doctrine, hardening-log, chat/continuance, code-evidence, and mixed-source batch registers are discoverable and governed.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_INDEX.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`
- `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`

## Required Index Sections

1. Purpose
2. Scope
3. Batch Register Index Table
4. Batch Status Definitions
5. Source Family Coverage
6. Discovery Rules
7. Review and Ingestion Boundaries
8. Non-Goals
9. Future Batch Workflow

## Required Table Columns

- Batch ID
- Batch register path
- Source family
- Source types covered
- Date or date range
- Batch status
- Row count
- Review status
- Ingestion permitted
- Corpus mutation status
- Notes

## Required Existing Batch Entry

- Batch ID: `HIST-DEVLOG-BATCH-2026-05-15`
- Batch register path: `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`
- Source family: Developer logs / hardening logs / platform doctrine / mixed log-doctrine sources
- Source types covered: `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `MIXED_LOG_DOCTRINE`, `OTHER_REQUIRES_REVIEW`
- Batch status: `ACTIVE_METADATA_ONLY`
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Corpus mutation status: No

## Required Controls

The index must state that it is discovery/governance metadata only; listing a batch does not ingest source content; listing a batch does not make sources current truth; ingestion permitted defaults to No; Minerva must not treat batch-listed sources as current truth unless later reviewed/backfilled/governed; and source classification remains register-driven, not filename-driven.

Batch status definitions must include `EMPTY_PLACEHOLDER`, `ACTIVE_METADATA_ONLY`, `TRIAGE_IN_PROGRESS`, `TRIAGE_COMPLETE`, `CLOSED_SUPERSEDED`, and `CLOSED_MIGRATED`.

Source family coverage must include planned future batch families for developer logs / hardening logs / doctrine / mixed log-doctrine, chat and continuance prompts, code evidence summaries, test evidence summaries, award build control sources, baseline packs, and other requires review.

## Required Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert the new index exists, is referenced from the control index, references the existing developer-log batch register, records the required existing batch metadata, includes all required table columns and batch status definitions, lists the planned future batch families, states the non-ingestion and current-truth boundaries, confirms register-driven classification, confirms the developer-log batch register references the index, and confirms the documents state no corpus mutation, no ingestion, no Code Evidence integration, no live LLM, no runtime change, no baseline promotion, no ledger promotion, no review approval, no governed ingestion, no historical ingestion, no recapture, no benchmark execution, no corpus coverage execution, no answer-gap execution, and no generated artefact changes.

## Execution Commands

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Non-Goals

Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not parse or extract historical source content. Do not review historical sources. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

Suggested commit message: `minerva-historical-batch-register-index-v01`.

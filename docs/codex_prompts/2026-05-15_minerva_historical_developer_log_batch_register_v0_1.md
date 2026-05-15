# Minerva Historical Developer Log Batch Register v0.1

Date: 15 May 2026

## Purpose

Create the first empty developer-log batch register structure under the Minerva historical knowledge model.

This slice creates a durable placeholder batch register that future slices can populate with metadata for many historical developer-log-like materials at once. It must not ingest, parse, review, or extract any historical developer log content.

## Create

- `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`

## Required Register Sections

1. Purpose
2. Scope
3. Batch Metadata
4. Register-Driven Classification Rule
5. Batch Register Table
6. Triage Outcomes
7. Escalation Criteria
8. Non-Goals
9. Future Population Workflow

## Required Metadata

- Batch ID: `HIST-DEVLOG-BATCH-2026-05-15`
- Source family: Developer logs / hardening logs / platform doctrine / mixed log-doctrine sources
- Initial status: `EMPTY_PLACEHOLDER`
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Corpus mutation: No
- Full source extraction performed: No
- Purpose: future batch registration of historical developer-log-like materials

## Required Controls

The register must state that it is an empty/placeholder batch register, no historical developer log content is ingested, no historical developer log content is parsed or extracted, adding a later row registers metadata only unless a separate review/backfill slice says otherwise, source classification remains register-driven and not filename-driven, ordinary developer logs can remain batch-registered until needed, high-risk/high-value sources can later be escalated into the full review chain, the Analytics Engine source remains the prototype/deep-review path and not the default for all logs, ingestion permitted defaults to No, and Minerva must not treat batch-registered sources as current truth unless later reviewed/backfilled/governed.

## Required Tests

Add or update focused tests in `tests/test_domain_baseline_capture_batch.py` or a historical knowledge test file to assert the new register exists, includes required metadata, includes all required table columns, lists all triage outcomes and escalation criteria, preserves register-driven classification, references the register from the control index and batch registration/template docs, and records the non-ingestion/non-runtime/non-promotion boundaries.

## Execution Commands

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Non-Goals

This slice does not ingest historical chats, ingest developer logs, ingest doctrine documents, ingest code, parse or extract historical source content, review historical sources, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, change ledger counts, promote baselines, implement DB writes, migrations, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.


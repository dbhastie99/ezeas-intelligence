# Historical Batch Registration And Triage Model

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This model defines the metadata-level batch registration and triage path for Minerva historical sources.

The full Analytics Engine chain is the prototype/deep-review path, not the default path for every historical source. That chain includes source registration, placeholder placement, review-readiness record, review pack template, decision gate, code/test/schema cross-check plan, findings template, review execution checklist, and `NOT_REVIEWED` decision record.

The full deep-review path remains appropriate for high-value or high-risk sources. Most historical sources should first be batch-registered and triaged.

The first developer-log batch register placeholder is `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`. It is empty, metadata-only, and intended for future batch registration of developer logs, hardening logs, platform doctrine, and mixed log-doctrine sources.

Developer-log-like batch intake is governed by `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`.

## 2. Batch Registration Principle

Batch registration is metadata-level only.

Batch registration does not ingest source content, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

Batch triage does not ingest historical content. Batch triage does not make a source current truth.

Minerva must not treat batch-registered sources as current truth unless those sources are later reviewed, backfilled, and governed through the relevant control path.

## 3. Governing Classification Point

The source register remains the governing classification point. `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` is that governing register.

Registered folders and filenames are aids only; the register entry controls classification. Original filenames, folder names, and batch filenames may provide discovery hints, but they do not determine source type, source tier, review status, implementation-state classification, or ingestion permission.

`Ingestion permitted` defaults to `No`.

`Review status` defaults to `NOT_REVIEWED`.

`Implementation-state classification` defaults to `UNCERTAIN_REQUIRES_REVIEW` unless the operator has strong evidence from the document/register context.

## 4. Required Batch Triage Assignments

Batch triage assigns:

- Source type
- Source tier
- Domain tags
- Review status
- Implementation-state classification
- Supersession risk
- Backfill priority
- Whether the source needs a full review chain

These assignments are register-control metadata. They are not source-content ingestion and are not evidence extraction.

## 5. Full Review Chain Graduation

Only high-value/high-risk sources graduate to the full review-readiness / decision-gate / cross-check path.

Ordinary developer logs, hardening notes, doctrine files, chats, continuance prompts, and prompt files can remain batch-registered until needed by a domain backfill or current-answer risk review.

Many sources can be grouped by domain/date range rather than creating separate deep-review artefacts for every file. A grouped batch can preserve source-level metadata while deferring individual deep-review artefacts until a source becomes high-value, high-risk, disputed, or needed for governed backfill.

## 6. Boundaries

Batch registration does not ingest source content.

Batch registration does not mutate corpus.

Batch registration does not connect Code Evidence.

Batch registration does not call live LLM.

Batch registration does not change runtime behaviour.

Batch registration does not promote baselines.

Batch registration does not change ledger counts and does not perform ledger promotion.

Batch registration does not implement DB writes, migrations, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, review approval, governed ingestion, historical ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or generated artefact creation.

## 7. Related Artefacts

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`
- `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

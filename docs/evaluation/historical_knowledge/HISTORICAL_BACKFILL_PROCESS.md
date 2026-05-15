# Historical Backfill Process

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This process defines the domain-scoped historical knowledge backfill workflow for Minerva.

Pre-control-model historical knowledge is incomplete and not yet captured to the same durable standard as the new formal-evidence model.

Source classification is register-driven, not filename-driven. `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` is the durable register that controls historical source discovery and classification. Registered folders and source-register entries are the durable discovery mechanism. Individual filenames are metadata and may be hints only. Hardcoded individual document names must not be used as the primary source classification mechanism.

Registration validation is governed by `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`.

The registered source folder root is `docs/evaluation/historical_knowledge/registered_sources/`. Placing a file under that root does not register, review, ingest, or promote the source; a source-register entry is still required.

Review readiness is governed by `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md` and recorded with `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md`. Filled review-readiness records are stored under `docs/evaluation/historical_knowledge/review_readiness_records/`. Review readiness is required before creating a historical backfill evidence pack.

Historical analytics review pack drafting uses `docs/evaluation/historical_knowledge/review_pack_templates/HISTORICAL_ANALYTICS_REVIEW_PACK_TEMPLATE.md`. The first Analytics Engine draft placeholder is `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`; it is a placeholder only and does not review, ingest, parse, extract, cross-check, or promote the source.

Historical analytics review decision gating uses `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md`. The gate must remain control-only until a future explicit review slice completes source review, code/test/schema cross-check, supersession assessment, and reviewer rationale.

Historical analytics code/test/schema cross-check planning uses `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md`. The plan is control-only: code/test/schema cross-check has not been performed in this slice, and the Analytics Engine developer log remains `NOT_REVIEWED` with ingestion permitted `No`.

Historical analytics cross-check findings must be recorded using `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md`. The first Analytics Engine findings draft placeholder is `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md`; it is a placeholder only and records that no code/test/schema evidence has been reviewed, no historical source content has been parsed or extracted, no findings have been made, and no Minerva ingestion is permitted.

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

## 3. Register Fields

`docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` assigns source class and starting reliability tier. A registered source does not become final truth until review status, implementation-state classification, supersession status, and relevant cross-checking have been completed.

Required register fields are:

- Source title
- Original filename
- Source folder
- Registered source type
- Source tier
- Domain tags
- Date or date range
- Repository context
- Related commits if known
- Related control artefacts
- Implementation-state classification
- Review status
- Ingestion permitted
- Supersession status
- Evidence confidence
- Notes

A document can be classified as `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `MIXED_LOG_DOCTRINE`, `CHAT_OR_CONTINUANCE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_FILE`, `BASELINE_PACK`, `AWARD_BUILD_CONTROL`, or `OTHER_REQUIRES_REVIEW` even if the filename does not contain those exact words.

## 4. Domain-Scoped Backfill Workflow

1. Identify historical source material for one domain.
2. Register source provenance in `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`, including original filename as metadata, source folder, date where available, author/reviewer where available, registered source type, and source tier.
3. Classify source tier using `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`.
4. Complete source review readiness before any historical backfill evidence pack is created.
5. Extract candidate decisions without treating them as final truth.
6. Cross-check against code/tests/logs/doctrine/commits.
7. Classify implementation state using the classifications in this process.
8. Create a curated backfill evidence pack for the domain.
9. Add a review gate that records reviewer, date, rationale, unresolved conflicts, and approval/blocked status.
10. Only later consider governed ingestion in a separate explicit slice.

## 5. Historical Chat Handling

Historical chats and continuance prompts are raw source material, not final truth.

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits before any candidate decision can be classified.

## 6. Priority Domains

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

## 7. Slice Boundaries

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This slice does not ingest any historical documents, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not connect Code Evidence, does not promote baselines, and does not perform ledger promotion.

This process does not mark any domain `REVIEWED_READY_FOR_INGESTION`. It does not mark any domain `BASELINE_ALREADY_EXISTS`.

The Analytics Engine review-readiness record at `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md` is a control record only and does not review, ingest, parse, or consume any historical source. The Analytics Engine developer log remains `NOT_REVIEWED` and ingestion permitted `No` until a future explicit review slice.

Review pack draft readiness does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, does not perform ledger promotion, and does not perform historical ingestion.

The Analytics Engine review decision gate at `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md` does not ingest historical content, does not parse or extract source content, does not create a backfill evidence pack, and does not permit governed ingestion while the source remains `NOT_REVIEWED`.

The Analytics Engine code/test/schema cross-check plan at `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` does not perform the cross-check, does not ingest historical content, does not parse or extract source content, does not create a backfill evidence pack, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, does not perform ledger promotion, and does not perform historical ingestion.

The Analytics Engine cross-check findings template and draft placeholder at `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md` and `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md` do not perform the cross-check, ingest historical content, parse or extract source content, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, perform historical ingestion, or permit governed ingestion.

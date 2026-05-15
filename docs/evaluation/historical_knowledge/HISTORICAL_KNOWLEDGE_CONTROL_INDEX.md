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
| Historical source register | `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` |
| Registered source folder root | `docs/evaluation/historical_knowledge/registered_sources/` |
| First analytics registered-source placeholder | `docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md` |
| Historical source tiering model | `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md` |
| Historical register-driven source classification | `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md` |
| Historical batch registration and triage model | `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md` |
| Historical batch register template | `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md` |
| Historical batch triage process | `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md` |
| Historical developer-log batch register placeholder | `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md` |
| Historical backfill process | `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md` |
| Historical source review-readiness template | `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md` |
| Historical source review-readiness process | `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md` |
| First analytics review-readiness record | `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md` |
| Historical analytics review pack template | `docs/evaluation/historical_knowledge/review_pack_templates/HISTORICAL_ANALYTICS_REVIEW_PACK_TEMPLATE.md` |
| First analytics review pack draft placeholder | `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md` |
| First analytics review decision gate | `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md` |
| First analytics NOT_REVIEWED decision record | `docs/evaluation/historical_knowledge/review_decision_records/HIST_ANALYTICS_2025_12_06_20_DECISION_RECORD_NOT_REVIEWED.md` |
| First analytics code/test/schema cross-check plan | `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` |
| Historical analytics cross-check findings template | `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md` |
| First analytics cross-check findings draft placeholder | `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md` |
| First analytics review execution checklist | `docs/evaluation/historical_knowledge/review_execution_checklists/HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md` |
| First analytics inventory batch | `docs/evaluation/historical_knowledge/inventory_batches/HISTORICAL_SOURCE_INVENTORY_BATCH_2026_05_15_ANALYTICS.md` |

## 3. Source Authority Summary

Tier 1 code and tests are the highest authority for implemented state.

Tier 2 developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review.

Tier 3 historical chats and continuance prompts are raw historical source material, not final truth.

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits.

Developer logs and doctrine documents are valuable but may include planned, partial, superseded, or backlog work, so they require implementation-state classification.

Code/tests must be used to confirm implemented behaviour, but code alone may not explain why.

## 4. Register-Driven Source Classification

Source classification is register-driven, not filename-driven.

`docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` is the durable register that controls historical source discovery and classification.

Registered folders and source-register entries are the durable discovery mechanism. Individual filenames are metadata and may be hints only. Hardcoded individual document names must not be used as the primary source classification mechanism.

The registered source folder root is `docs/evaluation/historical_knowledge/registered_sources/`. Registered folders are discovery and classification aids only; a file placed there still requires a source-register entry and does not become final truth.

The register assigns source class and starting reliability tier. A registered source does not become final truth until review status, implementation-state classification, supersession status, and relevant cross-checking against code/tests/commits/logs/doctrine where relevant have been completed.

A document can be classified as `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `MIXED_LOG_DOCTRINE`, `CHAT_OR_CONTINUANCE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_FILE`, `BASELINE_PACK`, `AWARD_BUILD_CONTROL`, or `OTHER_REQUIRES_REVIEW` even if the filename does not contain those exact words.

## 5. Backfill Scope

Most historical sources should first be batch-registered and triaged using `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md` and `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md`. The full Analytics Engine chain is the prototype/deep-review path, not the default path for every source.

The first developer-log batch register placeholder is `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`. It is an empty metadata-only batch register for future historical developer-log-like materials. It does not ingest, parse, extract, review, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, promote ledger state, or permit Minerva to treat batch-registered sources as current truth.

Historical backfill must be domain-scoped. A future slice must identify source material, register provenance, classify source tier, complete review readiness using `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md` and `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md`, extract candidate decisions, cross-check evidence, classify implementation state, create a curated backfill evidence pack, add a review gate, and only later consider governed ingestion.

This index does not grant permission for ingestion or promotion.

## 6. Initial Priority Domains

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

## 7. Current Permission State

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This slice does not ingest any historical documents, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not connect Code Evidence, does not promote baselines, and does not perform ledger promotion.

The first inventory/registering batch is recorded at `docs/evaluation/historical_knowledge/inventory_batches/HISTORICAL_SOURCE_INVENTORY_BATCH_2026_05_15_ANALYTICS.md`. That batch registers the Analytics Engine developer log as historical source material only. It does not ingest the log, does not make it current final truth, and preserves that `ProcessedRule`-era analytics requires review against current `CalcInterpreterLine` target modelling, current code, tests, database views, and committed schema/scripts.

The first analytics registered-source placement placeholder exists at `docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md`. Folder placement alone is not ingestion; the register entry controls classification; the original filename is metadata only; and the full historical document has not been ingested.

The Analytics Engine developer log remains `NOT_REVIEWED` and ingestion permitted `No` until a future explicit review slice completes source review. The first filled review-readiness record is `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`; it is a review-readiness record only and does not review, ingest, parse, or consume that source.

The historical analytics review pack template is `docs/evaluation/historical_knowledge/review_pack_templates/HISTORICAL_ANALYTICS_REVIEW_PACK_TEMPLATE.md`. The first Analytics Engine review pack draft placeholder is `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`. Review pack draft readiness does not review the source, does not extract source content, does not perform code/test/schema cross-checking, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, does not perform ledger promotion, and does not perform historical ingestion.

The first Analytics Engine review decision gate is `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md`. It is a control gate only and does not review, ingest, parse, extract, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, or perform historical ingestion.

The first Analytics Engine NOT_REVIEWED decision record is `docs/evaluation/historical_knowledge/review_decision_records/HIST_ANALYTICS_2025_12_06_20_DECISION_RECORD_NOT_REVIEWED.md`. It records that the source remains `NOT_REVIEWED`; ingestion permitted No; backfill evidence pack permitted No; governed ingestion permitted No; current truth answering permitted No; source content extracted No; code/test/schema cross-check completed No; historical source ingested No. It does not mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, perform historical ingestion, approve review, or permit governed ingestion.

The first Analytics Engine code/test/schema cross-check plan is `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md`. It is a planning artefact only; code/test/schema cross-check has not been performed in this slice. It does not parse the developer log, ingest historical content, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, perform historical ingestion, or approve review.

The historical analytics cross-check findings template is `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md`. The first Analytics Engine findings draft placeholder is `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md`. Findings template creation does not perform the cross-check, does not parse or extract source content, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, does not perform ledger promotion, does not perform historical ingestion, and does not permit Minerva ingestion.

The first Analytics Engine review execution checklist is `docs/evaluation/historical_knowledge/review_execution_checklists/HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md`. Completing that checklist is required before changing the review decision gate, but checklist creation or completion does not ingest source content, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, perform historical ingestion, or change the current `NOT_REVIEWED` status unless a separate review decision record/update slice performs that change.

This slice does not mark any domain `REVIEWED_READY_FOR_INGESTION`. It does not mark any domain `BASELINE_ALREADY_EXISTS`.

## 8. How Minerva Should Use This Index

Minerva should use this index as the starting point for historical knowledge control state.

Minerva must preserve that pre-control-model historical knowledge is incomplete and unapproved. Minerva must not treat historical chats, continuance prompts, developer logs, hardening logs, doctrine, code, tests, or commits as governed historical corpus merely because they exist.

## 9. How Codex Should Use This Index

Future Codex slices must read this index, the gap register, the source register, the source tiering model, the register-driven source classification model, the review-readiness process/template, and the backfill process before creating any historical backfill evidence pack or proposing historical ingestion.

Any future historical ingestion, governed ingestion, review approval, recapture, promotion, ledger update, runtime change, endpoint change, UI change, Code Evidence connection, live LLM call, DB write, migration, benchmark execution, corpus coverage execution, answer-gap execution, or generated artefact creation requires a separate explicit slice.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_historical_knowledge_control_index_v0_1.md`.

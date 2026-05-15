# Minerva Historical Source Register First Inventory Batch v0.1

Date: 15 May 2026

## 1. Purpose

Create the first controlled historical source inventory batch without ingesting historical content.

This slice registers the historical Analytics Engine developer log as source material, but does not ingest it into corpus and does not treat it as current final truth.

## 2. Source Context

The user provided a historical analytics developer log titled `Developer Log - Analytics Engine (5).docx`.

The log covers Golden Slice Analytics, `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, Power BI handover, `ProcessedRule.Quantity`-based hours, `AwardRateType` behaviour flags, ObjectTime Work/Schedule mapping, and dev analytics seeding.

This source is valuable historical rationale and decision material, but it is partially superseded because the current platform direction has moved from `ProcessedRule` to `CalcInterpreterLine` as the canonical processed payroll result source.

## 3. Required Outputs

Update `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` with a first register entry for the analytics developer log.

Create `docs/evaluation/historical_knowledge/inventory_batches/HISTORICAL_SOURCE_INVENTORY_BATCH_2026_05_15_ANALYTICS.md`.

Update `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md` if needed to reference the first inventory batch.

## 4. Register Entry Requirements

The register entry must record:

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: `Developer Log - Analytics Engine`
- Original filename: `Developer Log - Analytics Engine (5).docx`
- Source folder: `docs/evaluation/historical_knowledge/registered_sources/developer_logs/`
- Registered source type: `DEVELOPER_LOG`, with rationale that it is developer-authored historical analytics working material requiring review and implementation-state confirmation
- Source tier: Tier 2
- Domain tags: Analytics, Workforce Analytics DB, Golden Slice, ObjectTime, ProcessedRule, CalcInterpreterLine Replatform Review, Power BI, Reconciliation Reporting
- Date or date range: 6 December 2025 to 20 December 2025, based on the log content
- Repository context: historical analytics server / workforce analytics context
- Related commits if known: unknown
- Related control artefacts: `HISTORICAL_SOURCE_TIERING_MODEL.md`, `HISTORICAL_BACKFILL_PROCESS.md`, `HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`, `HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- Implementation-state classification: `UNCERTAIN_REQUIRES_REVIEW`, preserving that current implementation state requires code confirmation
- Review status: `NOT_REVIEWED`
- Ingestion permitted: `No`
- Supersession status: `PARTIALLY_SUPERSEDED_BY_CALCINTERPRETERLINE_MODEL`
- Evidence confidence: medium/high for historical rationale; requires code confirmation for current implementation
- Notes: `ProcessedRule`-era analytics must be reviewed before use as current truth; `CalcInterpreterLine` is the current target calculation fact source

Do not copy the full developer log into the register. Summarise at metadata level only. The actual source remains external/user-provided until a future controlled source-placement/backfill slice.

## 5. Inventory Batch Requirements

The inventory batch document must state:

1. This is an inventory/registering slice only.
2. No historical source content is ingested.
3. The analytics developer log is registered as historical source material.
4. The log is valuable for historical decisions and rationale.
5. The log is not automatically current platform truth.
6. `ProcessedRule`-era analytics is historical and requires review.
7. `CalcInterpreterLine` is the current target source for processed payroll analytics.
8. Future analytics backfill must cross-check this log against current code, tests, database views, and committed schema/scripts.
9. The source should be used to support a later analytics replatform planning pack, not direct Minerva ingestion.
10. No corpus mutation, Code Evidence integration, live LLM call, runtime change, baseline promotion, ledger promotion, or historical ingestion occurs in this slice.

## 6. Test Requirements

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert the register metadata, inventory batch existence, non-ingestion boundaries, CalcInterpreterLine supersession risk, and future cross-check requirements for current code/tests/schema.

## 7. Boundaries

Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

Do not mutate corpus. Do not perform DB writes. Do not change runtime behaviour. Do not add endpoints or UI. Do not perform review approval, governed ingestion, historical ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, generated-artefact promotion, baseline promotion, ledger update, or ledger promotion.

## 8. Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, first inventory batch created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-source-register-first-inventory-batch-v01`

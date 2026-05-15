# Codex Prompt - Minerva Historical Analytics Review Pack Template v0.1

Date: 15 May 2026

Mode: Documentation/control-template creation only

## Objective

Create a reusable review/backfill pack template for historical analytics sources, starting with the registered Analytics Engine developer log, without reviewing, ingesting, parsing, or treating the source as current truth.

## Source Context

The historical Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20`.

It has a source placeholder and review-readiness record. It remains `NOT_REVIEWED`, ingestion permitted `No`, and historical source material only.

The log covers historical `ProcessedRule`-era analytics, `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, `ObjectTime` Work/Schedule mapping, `AwardRateType` behaviour flags, Power BI handover, and dev analytics seeding.

Current analytics direction is `CalcInterpreterLine` as the canonical processed payroll result source.

## Create

- `docs/evaluation/historical_knowledge/review_pack_templates/HISTORICAL_ANALYTICS_REVIEW_PACK_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`

## Template Requirements

The analytics review pack template must include these sections:

1. Purpose
2. Source Register Details
3. Source Material Boundary
4. Review Preconditions
5. Historical Architecture Summary
6. Still-Valid Decisions
7. Superseded or At-Risk Decisions
8. Current Code/Test/Schema Cross-Check
9. Current Truth Classification
10. Analytics Replatform Implications
11. Minerva Answering Implications
12. Backfill Evidence Pack Recommendation
13. Ingestion Decision
14. Non-Goals
15. Required Follow-Up Actions

The template must include fields for:

- Register ID
- Source title
- Original filename
- Registered source type
- Source tier
- Review status
- Ingestion permitted
- Reviewer
- Review date
- Historical domain tags
- Source summary
- Historical implemented-state claims
- Historical doctrine claims
- Historical backlog/future-state claims
- Supersession risk
- Code/test/schema cross-check required
- Code/test/schema cross-check result
- Current implementation classification
- Current doctrine classification
- Current backlog classification
- Minerva-safe answer boundaries
- Backfill recommendation
- Reviewer rationale
- Follow-up actions

## Draft Placeholder Requirements

The draft placeholder for `HIST-ANALYTICS-2025-12-06-20` must state:

- It is a placeholder only.
- The Analytics Engine source has not yet been reviewed.
- No source content has been extracted in this slice.
- No code/test/schema cross-check has been performed.
- No Minerva ingestion is permitted.
- `ProcessedRule`-era analytics is historical and requires review.
- `CalcInterpreterLine` is the current target calculation fact source.
- The future review must separate still-valid analytics doctrine from superseded `ProcessedRule`-era implementation assumptions.
- The future review must cross-check against current `workforce-platform` / `ezeas-analytics` code, tests, schema, SQL views, and commits.
- The future review must not claim that old `vw_FactProcessedRule` or `vw_GS_RosterVsActual` are current canonical analytics facts unless code/schema review proves that current state.

## Required Boundaries

The template and placeholder must preserve these rules:

- Historical source review pack creation does not ingest the source.
- Review pack draft readiness does not mutate corpus.
- Review pack draft readiness does not connect Code Evidence.
- Review pack draft readiness does not call live LLM.
- Review pack draft readiness does not change runtime behaviour.
- Review pack draft readiness does not promote baselines or change ledger counts.
- Minerva must not answer from the analytics source as current truth until reviewed/backfilled/governed.

## Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. `HISTORICAL_ANALYTICS_REVIEW_PACK_TEMPLATE.md` exists.
2. `HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md` exists.
3. The template includes all required sections.
4. The template includes all required fields.
5. The placeholder references `HIST-ANALYTICS-2025-12-06-20`.
6. The placeholder references Developer Log - Analytics Engine.
7. The placeholder states the source has not been reviewed.
8. The placeholder states no source content has been extracted.
9. The placeholder states no code/test/schema cross-check has been performed.
10. The placeholder states no Minerva ingestion is permitted.
11. The placeholder states `ProcessedRule`-era analytics is historical and requires review.
12. The placeholder states `CalcInterpreterLine` is the current target calculation fact source.
13. The placeholder states old `vw_FactProcessedRule` / `vw_GS_RosterVsActual` must not be claimed as current canonical facts unless current review proves it.
14. The control index or backfill process references the analytics review pack template.
15. The source register or review-readiness record references the draft placeholder path.
16. The documents state no corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur.

## Explicit Non-Goals

Do not ingest historical chats. Do not ingest the full developer log. Do not parse or extract source content. Do not ingest doctrine documents. Do not ingest code. Do not review the Analytics Engine source yet. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, analytics review pack template created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-review-pack-template-v01`

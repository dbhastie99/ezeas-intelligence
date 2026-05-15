# Minerva Historical Analytics NOT_REVIEWED Decision Record v0.1

Date: 15 May 2026

## Purpose

Create and verify a formal `NOT_REVIEWED` decision record for the registered Analytics Engine historical source.

The source is registered and prepared for future review, but has not been reviewed, cross-checked, ingested, or approved for current-truth Minerva answering.

## Source

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: Developer Log - Analytics Engine
- Original filename: Developer Log - Analytics Engine (5).docx
- Historical content scope: ProcessedRule-era analytics including `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, `AwardRateType` behaviour flags, ObjectTime Work/Schedule mapping, Power BI handover, and dev analytics seeding.
- Current analytics direction to preserve: `CalcInterpreterLine` is the current target canonical processed payroll calculation fact.

## Required Output

Create:

- `docs/evaluation/historical_knowledge/review_decision_records/HIST_ANALYTICS_2025_12_06_20_DECISION_RECORD_NOT_REVIEWED.md`

Update existing historical knowledge control artefacts only where needed to reference the new decision record and preserve the `NOT_REVIEWED` boundary.

## Decision Requirements

The decision record must state:

- Decision status: `NOT_REVIEWED`
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Backfill evidence pack permitted: No
- Governed ingestion permitted: No
- Current truth answering permitted: No
- Code/test/schema cross-check completed: No
- Source content extracted: No
- Historical source ingested: No
- Minerva may use this source as current truth: No
- ProcessedRule-era analytics remains historical pending review.
- `CalcInterpreterLine` remains the current target canonical processed payroll calculation fact.

## Boundaries

Do not ingest historical chats. Do not ingest the full developer log. Do not parse or extract source content. Do not perform the code/test/schema cross-check. Do not review the Analytics Engine source yet. Do not change the source to `REVIEWED_READY_FOR_BACKFILL_DRAFT` or `REVIEWED_READY_FOR_GOVERNED_INGESTION`.

Do not mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, change endpoints or UI, change workforce-platform, award-configurator-v1, ezeas-analytics, or ezeas-intelligence runtime, promote baseline, or change ledger counts.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.


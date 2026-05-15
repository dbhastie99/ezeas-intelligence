# Minerva Historical Analytics Code Cross-Check Plan v0.1

Date: 15 May 2026

## Purpose

Create the controlled code/test/schema cross-check plan required before the registered Analytics Engine historical source can be reviewed or used for a curated backfill evidence pack.

This slice must not perform the cross-check, ingest the source, parse the source, or treat the source as current truth.

## Source Context

The historical Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20`.

The source title is Developer Log - Analytics Engine.

The source remains `NOT_REVIEWED`, ingestion permitted `No`, and historical source material only.

The source covers ProcessedRule-era analytics including `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, AwardRateType behaviour flags, ObjectTime Work/Schedule mapping, Power BI handover, and dev analytics seeding.

The current analytics direction is `CalcInterpreterLine` as the canonical processed payroll result source.

## Required Creation

Create:

- `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md`

Update if needed:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md`
- `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`
- `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`

## Required Plan Sections

The cross-check plan must include:

1. Purpose
2. Source Register Details
3. Current Review Status
4. Cross-Check Scope
5. Repositories to Check
6. Code Areas to Check
7. Schema / Database Objects to Check
8. Analytics View Claims to Check
9. ProcessedRule-Era Claims to Validate
10. CalcInterpreterLine Replatform Claims to Validate
11. Reconciliation Reporting Claims to Validate
12. Evidence / Story Reporting Claims to Validate
13. Expected Classifications
14. Required Outputs
15. Non-Goals
16. Follow-Up Actions

## Required Boundaries

The plan must state:

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: Developer Log - Analytics Engine
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Code/test/schema cross-check has not been performed in this slice.
- The source remains historical source material, not current final truth.
- ProcessedRule-era analytics must not be treated as current canonical calculation fact without review.
- `CalcInterpreterLine` is the current target canonical processed payroll calculation fact.
- Future review must classify claims as still valid, partially valid, superseded, backlog/doctrine, implemented-and-tested, implemented-not-fully-tested, or uncertain.

## Test And Verification Instructions

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file.

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, analytics code cross-check plan created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-code-crosscheck-plan-v01`.

# Codex Prompt - Minerva Historical Analytics Source Review Readiness Record v0.1

Date: 15 May 2026

Mode: Documentation/control-record creation only

## Objective

Create the first filled historical source review-readiness record for the registered Analytics Engine developer log, without reviewing, ingesting, parsing, or treating the source as final truth.

## Source Context

The historical Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20`.

It covers historical analytics architecture including `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, `ProcessedRule.Quantity` based hours, `AwardRateType` behaviour flags, `ObjectTime` Work/Schedule mapping, Power BI handover, and dev analytics seeding.

It remains `NOT_REVIEWED`, ingestion permitted `No`, and historical source material only. The current analytics direction is `CalcInterpreterLine` as the canonical processed payroll result source.

## Create

- `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## Required Record Content

The review-readiness record must include:

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: Developer Log - Analytics Engine
- Original filename: Developer Log - Analytics Engine (5).docx
- Registered source type: matching `HISTORICAL_SOURCE_REGISTER.md`
- Source tier: Tier 2
- Source folder / placeholder path
- Domain tags: Analytics, Workforce Analytics DB, Golden Slice, ObjectTime, ProcessedRule, CalcInterpreterLine Replatform Review, Power BI, Reconciliation Reporting
- Date or date range: 6 December 2025 to 20 December 2025
- Repository context: historical analytics server / workforce analytics context
- Related commits if known: unknown
- Related control artefacts: `HISTORICAL_SOURCE_REGISTER.md`, `HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`, `HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md`, `HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md`
- Review owner: not assigned
- Review date: not recorded
- Review status before review: `NOT_REVIEWED`
- Target review status: `NOT_REVIEWED`
- Implementation-state classification before review: match the register language, `UNCERTAIN_REQUIRES_REVIEW`
- Target implementation-state classification: not changed
- Supersession status: ProcessedRule-era analytics partially superseded by CalcInterpreterLine model
- Evidence confidence: medium/high for historical rationale, requires code confirmation for current implementation
- Ingestion permitted before review: No
- Target ingestion permitted: No
- Source summary: metadata-level summary only, not full source content
- Candidate decisions extracted: not extracted in this slice
- Candidate doctrine extracted: not extracted in this slice
- Candidate backlog items extracted: not extracted in this slice
- Candidate implemented-state claims: not extracted in this slice
- Code/test/commit cross-check required: Yes
- Code/test/commit cross-check result: not performed
- Superseded or conflicting claims: suspected due to CalcInterpreterLine replatform, not reviewed
- Current truth classification: not current final truth
- Minerva answering implication: Minerva must not answer from this source as current truth until reviewed/backfilled/governed
- Backfill evidence pack recommendation: future analytics replatform planning pack candidate
- Reviewer rationale: not reviewed
- Required follow-up actions

The record must state that this is a review-readiness record only; the source has not been reviewed; the full historical source has not been ingested; no source content was parsed or extracted in this slice; the source remains historical source material, not current final truth; `ProcessedRule`-era analytics requires review before being used as current truth; `CalcInterpreterLine` is the current target calculation fact source; future review must cross-check this source against current code, tests, schema, view definitions, commits, and analytics architecture docs; and no corpus mutation, Code Evidence integration, live LLM call, runtime change, baseline promotion, ledger promotion, or historical ingestion occurs.

The full historical source has not been ingested. No source content was parsed or extracted.

## Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. The analytics review-readiness record exists.
2. It contains Register ID `HIST-ANALYTICS-2025-12-06-20`.
3. It references Developer Log - Analytics Engine.
4. It records original filename Developer Log - Analytics Engine (5).docx.
5. It records source tier Tier 2.
6. It records review status before review `NOT_REVIEWED`.
7. It records ingestion permitted before review No.
8. It records code/test/commit cross-check required Yes.
9. It records cross-check result not performed.
10. It states the full historical source has not been ingested.
11. It states no source content was parsed or extracted.
12. It states `ProcessedRule`-era analytics requires review.
13. It states `CalcInterpreterLine` is the current target calculation fact source.
14. It states Minerva must not answer from this source as current truth until reviewed/backfilled/governed.
15. `HISTORICAL_SOURCE_REGISTER.md` references the review-readiness record path.
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

Report files changed, analytics review-readiness record created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-source-review-readiness-record-v01`

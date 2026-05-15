# HIST-ANALYTICS-2025-12-06-20 Decision Record - NOT_REVIEWED

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This decision record formally records the current `NOT_REVIEWED` decision state for the registered Analytics Engine historical source.

The source has been registered and prepared for future review. It remains historical source material only. It has not been reviewed, cross-checked, ingested, or approved for current-truth Minerva answering.

## 2. Source Register Details

| Field | Value |
| --- | --- |
| Register ID | `HIST-ANALYTICS-2025-12-06-20` |
| Source title | Developer Log - Analytics Engine |
| Original filename | Developer Log - Analytics Engine (5).docx |
| Registered source type | `DEVELOPER_LOG` - developer-authored historical analytics working material requiring review and implementation-state confirmation |
| Source tier | Tier 2 |
| Review status | `NOT_REVIEWED` |
| Source placeholder | `docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md` |
| Review-readiness record | `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md` |
| Review pack draft placeholder | `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md` |
| Review decision gate | `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md` |
| Code/test/schema cross-check plan | `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` |
| Cross-check findings draft placeholder | `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md` |
| Review execution checklist | `docs/evaluation/historical_knowledge/review_execution_checklists/HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md` |

## 3. Decision Status

| Field | Value |
| --- | --- |
| Decision status | `NOT_REVIEWED` |
| Review status | `NOT_REVIEWED` |
| Ingestion permitted | No |
| Backfill evidence pack permitted | No |
| Governed ingestion permitted | No |
| Current truth answering permitted | No |
| Code/test/schema cross-check completed | No |
| Source content extracted | No |
| Historical source ingested | No |
| Minerva may use this source as current truth | No |

## 4. Current Evidence State

The Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20` and has a source placeholder, review-readiness record, review pack template, review pack draft placeholder, review decision gate, code/test/schema cross-check plan, cross-check findings template, cross-check findings draft placeholder, and review execution checklist.

Source content extracted: No.

Historical source ingested: No.

The source covers historical ProcessedRule-era analytics, including `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, `AwardRateType` behaviour flags, ObjectTime Work/Schedule mapping, Power BI handover, and dev analytics seeding. These items are not extracted or approved by this decision record.

ProcessedRule-era analytics remains historical pending review.

CalcInterpreterLine remains the current target canonical processed payroll calculation fact.

## 5. Current Review State

The source has not yet been formally reviewed.

No reviewer has been assigned for completed review.

No formal review execution checklist has been completed.

No source claim has been classified as still-valid, superseded, partially valid, backlog, or uncertain by this decision record.

Review status: `NOT_REVIEWED`.

Decision status: `NOT_REVIEWED`.

## 6. Cross-Check State

Code/test/schema cross-check completed: No.

The source has not been cross-checked against current workforce-platform code/tests/schema.

The source has not been cross-checked against current ezeas-analytics architecture/code/tests.

The existing cross-check plan and findings placeholder are control artefacts only. They do not record completed findings and do not approve any source-derived claim.

## 7. Minerva Answering Boundary

Minerva may mention that the source is registered historical source material if asked about historical backfill status.

Minerva must not use the source to answer current analytics implementation questions.

Minerva must not claim `vw_FactProcessedRule` or `vw_GS_RosterVsActual` are current canonical analytics facts based on this source.

Minerva must not claim the source has been reviewed, cross-checked, ingested, or approved.

Minerva must preserve that `CalcInterpreterLine` is the current target canonical calculation fact source unless future reviewed evidence changes that.

Minerva may use this source as current truth: No.

Current truth answering permitted: No.

## 8. Backfill / Ingestion Boundary

Ingestion permitted: No.

Backfill evidence pack permitted: No.

Governed ingestion permitted: No.

Historical source ingested: No.

This decision record does not create a backfill evidence pack, does not permit governed ingestion, and does not authorize any corpus mutation.

No corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur in this decision record.

## 9. Supersession / Current-Truth Boundary

ProcessedRule-era analytics remains historical pending review.

The source includes historical ProcessedRule-era analytics claims that may be partially superseded.

CalcInterpreterLine remains the current target canonical processed payroll calculation fact.

This decision record does not decide that historical ProcessedRule-era views, tables, or reporting outputs are current canonical analytics facts.

## 10. Required Future Actions

- Assign reviewer.
- Perform review execution checklist.
- Perform code/test/schema cross-check.
- Populate cross-check findings.
- Classify historical claims.
- Decide whether a backfill evidence pack draft is permitted.
- Create a future review decision record if status changes.

## 11. Non-Goals

This slice does not:

- perform review
- perform code/test/schema cross-check
- parse or extract the developer log
- ingest historical content
- create a backfill evidence pack
- permit governed ingestion
- mutate corpus
- connect Code Evidence
- call live LLM
- change runtime behaviour
- change workforce-platform, award-configurator-v1, ezeas-analytics, or ezeas-intelligence runtime
- promote baseline
- change ledger counts
- ingest historical chats
- ingest the full developer log
- ingest doctrine documents
- ingest code
- implement DB writes
- implement migrations
- add endpoint changes
- add UI changes
- approve review
- perform recapture
- run benchmark execution
- run corpus coverage execution
- run answer-gap execution
- update ledger counts
- perform ledger promotion
- create generated artefacts

## 12. Decision Rationale

The source is registered and prepared for future review.

The source has not yet been formally reviewed.

The source has not been cross-checked against current workforce-platform code/tests/schema.

The source has not been cross-checked against current ezeas-analytics architecture/code/tests.

The source includes historical ProcessedRule-era analytics claims that may be partially superseded.

Therefore, Minerva must not treat the source as current platform truth.


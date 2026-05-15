# HIST-ANALYTICS-2025-12-06-20 Review Decision Gate

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This review decision gate controls whether the registered Analytics Engine historical source can support any future historical analytics backfill evidence pack.

This gate does not review, ingest, parse, extract, or approve the historical source. It records the decision options and mandatory checks that must happen before any future approval.

## 2. Source Register Details

| Field | Value |
| --- | --- |
| Register ID | `HIST-ANALYTICS-2025-12-06-20` |
| Source title | Developer Log - Analytics Engine |
| Original filename | Developer Log - Analytics Engine (5).docx |
| Registered source type | `DEVELOPER_LOG` - developer-authored historical analytics working material requiring review and implementation-state confirmation |
| Source tier | Tier 2 |
| Source folder / placeholder path | `docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md` |
| Review-readiness record | `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md` |
| Review pack draft placeholder | `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md` |
| Code/test/schema cross-check plan | `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` |
| Domain tags | Analytics; Workforce Analytics DB; Golden Slice; ObjectTime; ProcessedRule; CalcInterpreterLine Replatform Review; Power BI; Reconciliation Reporting |
| Date or date range | 6 December 2025 to 20 December 2025 |
| Repository context | Historical analytics server / workforce analytics context |
| Related commits if known | unknown |

## 3. Current Status

| Field | Value |
| --- | --- |
| Register ID | `HIST-ANALYTICS-2025-12-06-20` |
| Source title | Developer Log - Analytics Engine |
| Original filename | Developer Log - Analytics Engine (5).docx |
| Review status | `NOT_REVIEWED` |
| Ingestion permitted | No |
| Current truth classification | not current final truth |
| ProcessedRule-era analytics | historical and requires review |
| CalcInterpreterLine | current target calculation fact source |
| Code/test/schema cross-check | required but not performed |
| Review owner | not assigned |
| Review date | not recorded |

## 4. Review Preconditions

Before this source can support any future backfill evidence pack decision, a future explicit review slice must:

- Assign a review owner.
- Record a review date.
- Review source content under historical knowledge controls.
- Separate historical rationale, doctrine, backlog, implemented-state claims, superseded claims, and uncertain claims.
- Complete the required code/test/schema cross-check.
- Complete a supersession assessment against the current analytics direction.
- Record reviewer rationale and unresolved conflicts.
- Keep ingestion permitted No unless a later governed ingestion slice changes that state.

## 5. Required Cross-Checks

Future review must cross-check:

- Current workforce-platform code and tests.
- Current ezeas-analytics architecture/control docs if available.
- Current database schema/view definitions where available.
- Commits related to analytics views/source facts if known.
- Current `CalcInterpreterLine`, `PayrollBucketResult`, and reconciliation model direction.
- Historical `ProcessedRule`-era claims and whether they are still valid, partially valid, superseded, or uncertain.

The controlled cross-check plan is `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md`. Code/test/schema cross-check has not been performed in this slice.

## 6. Allowed Review Decisions

Allowed review decisions are:

- `REMAIN_NOT_REVIEWED`
- `NEEDS_SOURCE_REVIEW`
- `REVIEWED_READY_FOR_BACKFILL_DRAFT`
- `REVIEWED_READY_FOR_GOVERNED_INGESTION`
- `SUPERSEDED`

## 7. Decision Rules

- `REMAIN_NOT_REVIEWED` keeps ingestion permitted No.
- `NEEDS_SOURCE_REVIEW` keeps ingestion permitted No.
- `REVIEWED_READY_FOR_BACKFILL_DRAFT` permits creating a curated backfill evidence pack draft only, not governed ingestion.
- `REVIEWED_READY_FOR_GOVERNED_INGESTION` can only be considered after source review, code/test/schema cross-check, supersession assessment, and reviewer rationale are complete.
- `SUPERSEDED` means the historical source must not be used as current truth and should only be cited for history if appropriate.
- No decision in this gate mutates corpus by itself.
- No decision in this gate promotes a baseline by itself.
- No decision in this gate changes runtime behaviour.

## 8. Minerva Answering Boundaries

- Minerva must not answer from this source as current truth while the gate remains `NOT_REVIEWED`.
- Minerva may later use this source for historical context only after review/backfill controls allow it.
- `ProcessedRule`-era analytics must not be presented as the current canonical calculation fact source unless future review proves it remains valid.
- `CalcInterpreterLine` remains the current target canonical calculation fact source unless future platform evidence changes that.

## 9. Backfill/Ingestion Boundaries

- This gate does not ingest historical content.
- This gate does not parse or extract source content.
- This gate does not create a backfill evidence pack.
- This gate does not permit governed ingestion while status remains `NOT_REVIEWED`.
- This gate does not mutate corpus, connect Code Evidence, call live LLM, run benchmark, run corpus coverage, run answer-gap reporting, promote baseline, or change ledger counts.

No corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur in this gate.

## 10. Non-Goals

This gate does not ingest historical chats, ingest the full developer log, parse or extract source content, ingest doctrine documents, ingest code, review the Analytics Engine source, implement DB writes, implement migrations, connect Code Evidence, call live LLM, add endpoint changes, add UI changes, change workforce-platform, change award-configurator-v1, change ezeas-analytics, change runtime behaviour, approve review, permit governed ingestion, recapture baselines, run benchmark, run corpus coverage, run answer-gap reporting, promote a baseline, update ledger counts, perform ledger promotion, or create generated artefacts.

## 11. Required Follow-Up Actions

- Assign a review owner before any source review.
- Record the future review date.
- Review the source under historical knowledge controls without treating it as current truth.
- Complete the required cross-checks listed in this gate.
- Classify `ProcessedRule`-era claims as still valid, partially valid, superseded, or uncertain.
- Preserve `CalcInterpreterLine` as the current target canonical calculation fact source unless future platform evidence changes that.
- Record a future decision using only the allowed review decisions in this gate.
- Create any future backfill evidence pack only in a separate explicit slice after this gate allows it.
- Consider governed ingestion only in a separate explicit slice after source review, code/test/schema cross-check, supersession assessment, and reviewer rationale are complete.

# HIST-ANALYTICS-2025-12-06-20 Code Cross-Check Plan

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This plan defines the controlled future code/test/schema cross-check required before the registered Analytics Engine historical source can be reviewed or used for a curated historical analytics backfill evidence pack.

This plan does not perform the cross-check. Code/test/schema cross-check has not been performed in this slice.

The source remains historical source material, not current final truth.

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
| Review decision gate | `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md` |

## 3. Current Review Status

| Field | Value |
| --- | --- |
| Review status | `NOT_REVIEWED` |
| Ingestion permitted | No |
| Current truth classification | historical source material, not current final truth |
| Code/test/schema cross-check | not performed in this slice |
| Review owner | not assigned |
| Review approval | not granted |

ProcessedRule-era analytics must not be treated as current canonical calculation fact without review.

`CalcInterpreterLine` is the current target canonical processed payroll calculation fact.

## 4. Cross-Check Scope

A future explicit review slice must compare the historical source's analytics claims against current code, tests, schema, database view definitions, committed scripts, and current analytics architecture docs.

The future review must classify each checked claim as still valid, partially valid, superseded, backlog/doctrine, implemented-and-tested, implemented-not-fully-tested, or uncertain.

This plan is limited to planning the future cross-check. It does not parse the developer log and does not extract source content.

## 5. Repositories to Check

- `workforce-platform`
- `ezeas-analytics`
- `ezeas-intelligence` only for historical/register/control context, not analytics runtime truth
- `award-configurator-v1` only if award-build analytics/evidence references are relevant

## 6. Code Areas to Check

- `CalcInterpreterLine` models/services/tests
- `PayrollBucketResult` / semantic bucket models/services/tests
- Reconciliation / imports / actuals models/services/tests
- `ObjectTime` source truth models/services/tests
- `PayRun` / `ProcessPeriod` models/services/tests
- `RateType` / `AwardRateType` behaviour fields
- Existing analytics SQL/scripts/views if present
- `ezeas-analytics` docs and future Python extension code

## 7. Schema / Database Objects to Check

- Tables, views, migrations, scripts, and schema snapshots that define processed payroll analytics fact grain.
- Tables, views, migrations, scripts, and schema snapshots for ObjectTime source truth and Work/Schedule distinction.
- Tables, views, migrations, scripts, and schema snapshots for ProcessPeriod, PayRun, reconciliation, imports, actuals, RateType, and AwardRateType behaviour fields.
- Any analytics database objects connected to `workforce_analytics_local`, `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, or `vw_GS_RosterVsActual`.

## 8. Analytics View Claims to Check

- `vw_FactObjectTime`
- `vw_FactProcessedRule`
- `vw_GS_RosterVsActual`
- `workforce_analytics_local`
- `workforce_analytics_dev`
- BI handover claims
- `AwardRateType` ordinary/hourly filtering
- `ObjectType` Work/Schedule mapping
- `ScheduledObjectTimeId` mapping
- `ProcessPeriod` grain

## 9. ProcessedRule-Era Claims to Validate

- Whether any `ProcessedRule`-era analytics view remains current, partially valid, superseded, or historical-only.
- Whether `ProcessedRule` is still used for any current analytics fact or only as historical context.
- Whether any historical `vw_FactProcessedRule` claim has been replaced by `CalcInterpreterLine`.
- Whether historical Golden Slice analytics claims still match current implementation and tests.

## 10. CalcInterpreterLine Replatform Claims to Validate

- Whether `CalcInterpreterLine` is implemented as the current target canonical processed payroll calculation fact.
- Whether `CalcInterpreterLine` grain and relationships support current processed payroll analytics requirements.
- Whether current tests cover `CalcInterpreterLine` as a fact source for analytics or evidence reporting.
- Whether any historical replatform backlog item remains open, implemented-not-fully-tested, implemented-and-tested, superseded, or uncertain.

## 11. Reconciliation Reporting Claims to Validate

- Whether reconciliation / imports / actuals models and tests support current roster-versus-actual reporting.
- Whether any historical `vw_GS_RosterVsActual` claim remains valid, partially valid, superseded, or uncertain.
- Whether ObjectTime, ScheduledObjectTimeId, ProcessPeriod, PayRun, RateType, and AwardRateType fields can support the future reconciliation report claims.

## 12. Evidence / Story Reporting Claims to Validate

- Whether current evidence/story reporting uses current code and tested models rather than historical ProcessedRule-era assumptions.
- Whether ezeas-analytics docs or future Python extension code describe analytics facts that align with current platform truth.
- Whether Minerva answering boundaries need to exclude, qualify, or permit any future historical analytics claim after review.

## 13. Expected Classifications

Future review must classify claims using these expected outcomes:

- still valid
- partially valid
- superseded
- backlog/doctrine
- implemented-and-tested
- implemented-not-fully-tested
- uncertain

## 14. Required Outputs

A future cross-check must produce:

- Cross-check findings table
- Claim classification table
- Source-to-code evidence map
- Superseded claims list
- Still-valid doctrine list
- Current analytics replatform implications
- Minerva-safe answering boundaries
- Recommendation for whether to create a reviewed historical backfill evidence pack

## 15. Non-Goals

This slice does not perform the cross-check.

This slice does not parse the developer log, ingest historical content, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, change `workforce-platform`, `ezeas-analytics`, `award-configurator-v1`, or `ezeas-intelligence` runtime, promote baseline, change ledger counts, perform ledger promotion, or perform historical ingestion.

This slice does not ingest historical chats, ingest the full developer log, parse or extract source content, ingest doctrine documents, ingest code, review or cross-check the Analytics Engine source, implement DB writes, implement migrations, add endpoint changes, add UI changes, approve review, permit governed ingestion, recapture, run benchmark, run corpus coverage, run answer-gap execution, or create generated artefacts.

No corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur in this plan.

## 16. Follow-Up Actions

- Assign a future review owner.
- Complete a governed source review before using any historical claim in a backfill evidence pack.
- Run the future code/test/schema cross-check against the repositories and code areas listed in this plan.
- Classify all reviewed claims with the expected classifications.
- Record the required outputs in a separate future review artefact.
- Keep ingestion permitted No unless a later explicit governed ingestion slice changes that state after review, cross-checking, supersession assessment, and approval.

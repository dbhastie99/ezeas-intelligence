# HIST-ANALYTICS-2025-12-06-20 Review Execution Checklist

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This checklist controls the execution steps for a future formal review of the registered Analytics Engine historical source.

Completing this checklist is required before changing the review decision gate.

The controlled review decision gate is for `HIST-ANALYTICS-2025-12-06-20`.

This checklist does not perform the review, cross-check code, ingest source content, parse source content, or treat the source as current truth.

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
| Current NOT_REVIEWED decision record | `docs/evaluation/historical_knowledge/review_decision_records/HIST_ANALYTICS_2025_12_06_20_DECISION_RECORD_NOT_REVIEWED.md` |
| Code/test/schema cross-check plan | `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` |
| Cross-check findings template | `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md` |
| Cross-check findings draft placeholder | `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md` |
| Review execution checklist | `docs/evaluation/historical_knowledge/review_execution_checklists/HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md` |

## 3. Current Status Before Review

| Field | Required confirmation |
| --- | --- |
| Register ID | Reviewer confirms the Register ID is `HIST-ANALYTICS-2025-12-06-20`. |
| Review status before review | Reviewer confirms review status before review is `NOT_REVIEWED`. |
| Ingestion permitted before review | Reviewer confirms ingestion permitted before review is No. |
| Source material state | Reviewer confirms the full source document is available to the reviewer but not ingested. |
| Current truth classification | Reviewer confirms the source is treated as historical source material, not current truth. |
| Current calculation fact boundary | Reviewer confirms `CalcInterpreterLine` remains the current target canonical processed payroll calculation fact unless current code/schema review proves otherwise. |
| Code/test/schema cross-check | Reviewer confirms code/test/schema cross-check is required and must be recorded before any review decision change. |

## 4. Reviewer Preconditions

- [ ] Review owner is assigned.
- [ ] Review date is recorded.
- [ ] Reviewer has read the source register entry, review-readiness record, review pack draft placeholder, review decision gate, code/test/schema cross-check plan, and cross-check findings template.
- [ ] Reviewer confirms the source remains `NOT_REVIEWED` and ingestion permitted No before review starts.
- [ ] Reviewer confirms no source content has been ingested into Minerva before review.
- [ ] Reviewer confirms this checklist is complete before changing the review decision gate.
- [ ] Reviewer confirms any review decision update will be recorded by a separate review decision record/update slice.

## 5. Source Material Handling Checklist

- [ ] Confirm the full source document is available to the reviewer but not ingested.
- [ ] Treat the source as historical source material, not current truth.
- [ ] Do not ingest the full developer log.
- [ ] Do not parse, extract, or quote source content outside the future formal review scope.
- [ ] Keep source-derived claims out of Minerva answers until reviewed, classified, and governed.
- [ ] Preserve original filename as metadata only.
- [ ] Record source locations or summaries only inside the governed future findings record.

## 6. Code/Test/Schema Cross-Check Checklist

- [ ] Check current `workforce-platform` code/tests for analytics fact, payroll calculation, reconciliation, ObjectTime, ProcessPeriod, PayRun, RateType, AwardRateType, and related evidence/reporting behaviour.
- [ ] Check current `ezeas-analytics` docs/code/tests where available for analytics architecture, future Python extension direction, and processed payroll analytics facts.
- [ ] Check database schema/view definitions where available, including migrations, scripts, schema snapshots, tables, and views relevant to processed payroll analytics and reconciliation.
- [ ] Use `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md` as the required cross-check plan.
- [ ] Record findings in `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md` or a governed filled copy based on that template.
- [ ] Record branches, commits, files, tests, schemas, and limitations checked.

## 7. Historical Claim Classification Checklist

- [ ] Separate `ProcessedRule`-era claims from still-valid doctrine.
- [ ] Classify historical claims using the findings template classifications.
- [ ] Use the allowed findings template classifications: `STILL_VALID_IMPLEMENTED_AND_TESTED`, `STILL_VALID_DOCTRINE`, `PARTIALLY_VALID_REQUIRES_UPDATE`, `SUPERSEDED_BY_CALCINTERPRETERLINE_MODEL`, `SUPERSEDED_BY_CURRENT_SCHEMA`, `HISTORICAL_CONTEXT_ONLY`, `BACKLOG_OR_PLANNED_NOT_IMPLEMENTED`, `UNCERTAIN_REQUIRES_REVIEW`, and `NOT_SUPPORTED_BY_CURRENT_CODE`.
- [ ] Record confidence and evidence basis for every classified claim.
- [ ] Record unresolved conflicts and follow-up actions.

## 8. Supersession and Current-Truth Checklist

- [ ] Confirm `ProcessedRule`-era analytics claims are not treated as current canonical calculation facts without current review evidence.
- [ ] Confirm `CalcInterpreterLine` remains the current target canonical processed payroll calculation fact unless current code/schema review proves otherwise.
- [ ] Identify any claims superseded by the `CalcInterpreterLine` model.
- [ ] Identify any claims superseded by current schema or view definitions.
- [ ] Identify any still-valid doctrine that survives independently of old implementation details.
- [ ] Record current-truth limitations and supersession rationale per claim.

## 9. Minerva Answering Boundary Checklist

- [ ] Record Minerva-safe answering boundaries per claim.
- [ ] Mark historical-only claims as historical context only.
- [ ] Mark uncertain claims as unavailable for current-truth answers.
- [ ] Require caveats for partially valid claims.
- [ ] Confirm Minerva must not answer from this source as current truth while it remains `NOT_REVIEWED`.
- [ ] Confirm no review decision alone permits current-truth answers without the downstream governed path.

## 10. Review Decision Checklist

- [ ] Confirm completing this checklist is required before changing the review decision gate.
- [ ] Any recommendation for `REVIEWED_READY_FOR_BACKFILL_DRAFT` is supported by reviewer rationale and cross-check evidence.
- [ ] Any recommendation for `REVIEWED_READY_FOR_GOVERNED_INGESTION` is supported by reviewer rationale, cross-check evidence, supersession assessment, and governed ingestion readiness.
- [ ] Confirm no review decision alone mutates corpus or permits current-truth answers without the downstream governed path.
- [ ] Confirm completing this checklist does not change the current `NOT_REVIEWED` status unless a separate review decision record/update slice performs that change.
- [ ] Record the proposed decision, rationale, unresolved risks, and follow-up actions separately from this checklist.

## 11. Backfill Evidence Pack Checklist

- [ ] Confirm any backfill evidence pack recommendation is supported by the completed cross-check findings.
- [ ] Confirm the pack scope excludes unreviewed, superseded, uncertain, or current-truth-unsafe claims.
- [ ] Confirm the pack records Minerva-safe answering boundaries per claim.
- [ ] Confirm governed ingestion remains a separate downstream path.
- [ ] Confirm no checklist completion creates a backfill evidence pack by itself.

## 12. Non-Goals

Completing this checklist does not itself ingest source content.

Completing this checklist does not mutate corpus.

Completing this checklist does not connect Code Evidence.

Completing this checklist does not call live LLM.

Completing this checklist does not change runtime behaviour.

Completing this checklist does not promote baselines or change ledger counts.

Completing this checklist does not change the current `NOT_REVIEWED` status unless a separate review decision record/update slice performs that change.

This checklist does not ingest historical chats, ingest the full developer log, parse or extract source content, perform the code/test/schema cross-check, review the Analytics Engine source, change the review decision, ingest doctrine documents, ingest code, implement DB writes, implement migrations, add endpoint changes, add UI changes, change `workforce-platform`, change `award-configurator-v1`, change `ezeas-analytics`, approve review, permit governed ingestion, perform historical ingestion, recapture, run benchmark execution, run corpus coverage execution, run answer-gap execution, promote baselines, update ledger counts, perform ledger promotion, or create generated artefacts.

No corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur from creating or completing this checklist.

For audit searchability: no corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur from this checklist.

## 13. Completion Criteria

The checklist is complete only when:

- [ ] All source register details are confirmed.
- [ ] Review status before review `NOT_REVIEWED` is confirmed.
- [ ] Ingestion permitted before review No is confirmed.
- [ ] The full source document is available to the reviewer but not ingested.
- [ ] Source material handling boundaries are confirmed.
- [ ] Required current code/test/schema checks are completed and recorded.
- [ ] Historical claims are classified using the findings template classifications.
- [ ] `ProcessedRule`-era claims are separated from still-valid doctrine.
- [ ] `CalcInterpreterLine` current-target status is preserved unless current review evidence proves otherwise.
- [ ] Minerva-safe answering boundaries are recorded per claim.
- [ ] Any review decision recommendation has reviewer rationale and cross-check evidence.
- [ ] The reviewer confirms checklist completion does not ingest content, mutate corpus, change runtime behaviour, promote baselines, change ledger counts, or change `NOT_REVIEWED` status by itself.

## 14. Follow-Up Actions

- Assign a future review owner before executing this checklist.
- Complete the code/test/schema cross-check using the controlled cross-check plan.
- Fill a governed findings record using the historical analytics cross-check findings template.
- Record reviewer rationale and unresolved conflicts.
- Update the review decision gate only through a separate review decision record/update slice after this checklist and the required evidence are complete.
- Keep ingestion permitted No unless a later explicit governed ingestion slice changes that state.

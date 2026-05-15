# Minerva Historical Analytics Review Execution Checklist v0.1

Date: 15 May 2026

## Purpose

Create the reviewer execution checklist for a future formal review of the registered Analytics Engine historical source.

This slice must not perform the review, cross-check code, ingest source content, parse the source, or treat the source as current truth.

## Source Context

The historical Analytics Engine developer log is registered as `HIST-ANALYTICS-2025-12-06-20`.

The source title is Developer Log - Analytics Engine.

It has a source placeholder, review-readiness record, review pack template, review pack draft placeholder, review decision gate, code cross-check plan, and cross-check findings template.

It remains `NOT_REVIEWED`, ingestion permitted `No`, and historical source material only.

The source covers ProcessedRule-era analytics and must be reviewed against current workforce-platform/ezeas-analytics code, tests, schema, and CalcInterpreterLine analytics direction before being used in Minerva.

## Required Creation

Create:

- `docs/evaluation/historical_knowledge/review_execution_checklists/HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md`

Update if needed:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/review_decision_gates/HIST_ANALYTICS_2025_12_06_20_REVIEW_DECISION_GATE.md`
- `docs/evaluation/historical_knowledge/crosscheck_plans/HIST_ANALYTICS_2025_12_06_20_CODE_CROSSCHECK_PLAN.md`
- `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md`
- `docs/evaluation/historical_knowledge/review_pack_templates/HIST_ANALYTICS_2025_12_06_20_REVIEW_PACK_DRAFT_PLACEHOLDER.md`
- `docs/evaluation/historical_knowledge/review_readiness_records/HIST_ANALYTICS_2025_12_06_20_REVIEW_READINESS_RECORD.md`

## Required Checklist Sections

The checklist must include sections:

1. Purpose
2. Source Register Details
3. Current Status Before Review
4. Reviewer Preconditions
5. Source Material Handling Checklist
6. Code/Test/Schema Cross-Check Checklist
7. Historical Claim Classification Checklist
8. Supersession and Current-Truth Checklist
9. Minerva Answering Boundary Checklist
10. Review Decision Checklist
11. Backfill Evidence Pack Checklist
12. Non-Goals
13. Completion Criteria
14. Follow-Up Actions

## Required Confirmations

The checklist must require the reviewer to confirm:

- Register ID is `HIST-ANALYTICS-2025-12-06-20`.
- Review status before review is `NOT_REVIEWED`.
- Ingestion permitted before review is No.
- The full source document is available to the reviewer but not ingested.
- The source is treated as historical source material, not current truth.
- ProcessedRule-era claims are separated from still-valid doctrine.
- `CalcInterpreterLine` remains the current target canonical processed payroll calculation fact unless current code/schema review proves otherwise.
- Current workforce-platform code/tests are checked.
- Current ezeas-analytics docs/code/tests are checked.
- Database schema/view definitions are checked where available.
- Historical claims are classified using the findings template classifications.
- Minerva-safe answering boundaries are recorded per claim.
- Any recommendation for `REVIEWED_READY_FOR_BACKFILL_DRAFT` or `REVIEWED_READY_FOR_GOVERNED_INGESTION` is supported by reviewer rationale and cross-check evidence.
- No review decision alone mutates corpus or permits current-truth answers without the downstream governed path.

## Required Boundaries

The checklist must state:

- Completing the checklist is required before changing the review decision gate.
- Completing the checklist does not itself ingest source content.
- Completing the checklist does not mutate corpus.
- Completing the checklist does not connect Code Evidence.
- Completing the checklist does not call live LLM.
- Completing the checklist does not change runtime behaviour.
- Completing the checklist does not promote baselines or change ledger counts.
- Completing the checklist does not change the current `NOT_REVIEWED` status unless a separate review decision record/update slice performs that change.

## Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. `HIST_ANALYTICS_2025_12_06_20_REVIEW_EXECUTION_CHECKLIST.md` exists.
2. It contains Register ID `HIST-ANALYTICS-2025-12-06-20`.
3. It records review status before review `NOT_REVIEWED`.
4. It records ingestion permitted before review No.
5. It states full source is available to reviewer but not ingested.
6. It states ProcessedRule-era claims must be separated from still-valid doctrine.
7. It states `CalcInterpreterLine` remains the current target canonical processed payroll calculation fact unless current review proves otherwise.
8. It requires workforce-platform checks.
9. It requires ezeas-analytics checks.
10. It requires schema/view definition checks where available.
11. It requires historical claim classifications using the findings template.
12. It requires Minerva-safe answering boundaries per claim.
13. It states completing the checklist does not ingest source content.
14. It states completing the checklist does not mutate corpus.
15. It states completing the checklist does not change runtime behaviour.
16. It states completing the checklist does not promote baselines or change ledger counts.
17. It states completing the checklist does not change `NOT_REVIEWED` status unless a separate review decision record/update slice changes it.
18. `HISTORICAL_SOURCE_REGISTER.md` or the review decision gate references the checklist path.
19. The documents state no corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur.

## Prohibited Work

Do not ingest historical chats. Do not ingest the full developer log. Do not parse or extract source content. Do not perform the code/test/schema cross-check. Do not review the Analytics Engine source yet. Do not change the review decision. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, analytics review execution checklist created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-review-execution-checklist-v01`.

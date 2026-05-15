# Codex Prompt: Minerva Historical Batch Review Candidate Selection v0.1

Date: 16 May 2026

## Objective

Create the first governed candidate-selection model for Minerva historical batch review.

This slice defines how a registered historical queue entry can be selected as a candidate for future deep review, including priority, blocker handling, current-truth risk, repository cross-check requirements, and required outputs.

## Current Truth

Historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed.

Batch registration is metadata-only.

Batch review queueing is metadata/control-only.

Queueing does not ingest source content.

Queueing does not permit Minerva to answer current-state questions from historical material.

`NOT_REVIEWED` sources remain `NOT_REVIEWED`.

Ingestion permitted remains `No` unless a future governed ingestion slice explicitly changes it.

Answer use remains `No` unless a future governed ingestion/backfill/current-truth decision explicitly changes it.

`ezeas-intelligence` remains separate from `workforce-platform`, `award-configurator-v1`, and `ezeas-analytics`.

This slice must not mutate operational corpus content or live evidence stores.

## Required Posture

Documentation/control/test hardening only.

No source content ingestion.

No operational corpus mutation.

No Code Evidence ingestion.

No live LLM calls.

No database writes.

No schema migrations.

No endpoint changes.

No UI changes.

No workforce-platform changes.

No award-configurator-v1 changes.

No ezeas-analytics changes.

No current-truth promotion.

No answer-use permission.

No deep-review execution.

No historical source may become answerable current truth in this slice.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION_TEMPLATE.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_READINESS_RULES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE_ENTRY_TEMPLATE.md`
- `tests/test_domain_baseline_capture_batch.py`

Do not create or update runtime ingestion code unless a tiny metadata-only helper already exists and can be safely extended for constant/status validation. Prefer docs/tests only.

## Required Candidate Selection Model

`HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md` must include:

1. Purpose
2. Scope
3. Candidate Selection Status Model
4. Selection Criteria
5. Priority Model
6. Blocker Handling
7. Current Truth Risk Handling
8. Required Cross-Checks Before Review
9. Required Outputs Before Selection Can Advance
10. What Candidate Selection Does Not Mean
11. Current Truth Boundary
12. Ingestion Boundary
13. Developer Handoff

Candidate selection statuses:

- `NOT_SELECTED`
- `CANDIDATE_PROPOSED`
- `CANDIDATE_SELECTED_FOR_REVIEW`
- `CANDIDATE_BLOCKED`
- `CANDIDATE_DEFERRED`
- `CANDIDATE_REJECTED`
- `CANDIDATE_SUPERSEDED`

Priority values:

- `HIGH`
- `MEDIUM`
- `LOW`
- `DO_NOT_REVIEW`

Blocker categories:

- `MISSING_SOURCE_REFERENCE`
- `MISSING_REPOSITORY_CONTEXT`
- `MISSING_DOMAIN_CONTEXT`
- `CURRENT_TRUTH_RISK_UNASSESSED`
- `DUPLICATE_OR_SUPERSEDED_RISK_UNASSESSED`
- `CROSS_CHECKS_NOT_IDENTIFIED`
- `EXPECTED_OUTPUTS_NOT_DEFINED`
- `SOURCE_NOT_READY_FOR_REVIEW`

## Required Template

`HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION_TEMPLATE.md` must provide a reusable candidate-selection record template with these fields:

- `CandidateSelectionId`
- `QueueEntryId`
- `SourceId`
- `SourceTitle`
- `RegisteredBatchId`
- `CandidateStatus`
- `ReviewPriority`
- `SelectionRationale`
- `CurrentTruthRisk`
- `DuplicateOrSupersessionRisk`
- `RequiredCrossChecks`
- `RequiredReviewOutputs`
- `IngestionPermitted`
- `AnswerUsePermitted`
- `Blockers`
- `SelectedBy`
- `SelectedAtUtc`
- `DecisionRecordLink`
- `Notes`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Report

Report files changed, docs/tests-only status, test result, `git diff --check` result, `.pytest_tmp` status, and confirmation that no source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM call, DB write, schema migration, endpoint change, UI change, workforce-platform change, award-configurator-v1 change, ezeas-analytics change, current-truth promotion, answer-use permission, or deep-review execution was introduced.

Suggested commit message: `minerva-historical-batch-review-candidate-selection-v01`

# Minerva Historical Review Findings Classification v0.1 Prompt

Date: 16 May 2026

## Objective

Create the first governed findings classification and review outcome model for Minerva historical deep review.

This slice defines how future deep-review findings are classified after review: current-truth candidate, historical-only, superseded, duplicate, conflict, backlog/follow-up, rejected, or requires further cross-check. It prepares the later ingestion/backfill/current-truth decision path without performing ingestion or permitting answer use.

## Required Posture

- Documentation/control/test hardening only.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No answer-use permission.
- No deep-review execution.
- No historical source may become answerable current truth in this slice.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDING_CLASSIFICATION_TEMPLATE.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_CHECKLIST.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Model Content

The findings classification model must define purpose, scope, classification statuses, finding classification types, requirements, cross-check requirements, conflict handling, supersession handling, current-truth candidate boundary, historical-only boundary, answer-use boundary, ingestion boundary, non-meanings, and developer handoff.

The outcome decision model must define conservative outcome statuses and state that outcome decisions do not ingest, do not permit answer use, and do not promote current truth unless later governed decisions explicitly approve those steps.

The classification template must include all required identifiers, context, classification, cross-check, conflict, supersession, duplicate, recommended outcome, reviewer, timestamp, and notes fields with conservative defaults:

- `IngestionPermitted: No`
- `AnswerUsePermitted: No`
- `CurrentTruthPermitted: No`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Expected Report

Report files changed, docs/tests-only status, tests run and result, `git diff --check` result, `.pytest_tmp` status, progress after this slice, expected next slice, and confirmation that no source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM call, DB write, schema migration, endpoint change, UI change, workforce-platform change, award-configurator-v1 change, ezeas-analytics change, current-truth promotion, answer-use permission, or deep-review execution was introduced.

Suggested commit message: `minerva-historical-review-findings-classification-v01`

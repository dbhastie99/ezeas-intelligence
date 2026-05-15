# Minerva Historical Batch Review Decision Record v0.1

Date: 16 May 2026

## Objective

Create the first governed historical batch review decision-record model for Minerva.

This slice defines the decision record that must exist before, during, and after any future historical deep review. The record captures selection decision, review decision, ingestion decision, answer-use decision, current-truth decision, cross-check requirements, blockers, and evidence requirements.

## Current Truth

- Historical sources are not current truth unless reviewed, cross-checked, backfilled, ingested through a governed process, and explicitly promoted.
- Batch registration is metadata-only.
- Review queueing is metadata/control-only.
- Candidate selection is metadata/control-only.
- Candidate selection does not perform deep review.
- Candidate selection does not ingest source content.
- Candidate selection does not permit Minerva to answer current-state questions from historical material.
- NOT_REVIEWED sources remain NOT_REVIEWED unless a future governed review decision changes their status.
- Ingestion permitted remains No unless a future governed ingestion slice explicitly changes it.
- Answer use remains No unless a future governed ingestion/backfill/current-truth decision explicitly changes it.
- ezeas-intelligence remains separate from workforce-platform, award-configurator-v1, and ezeas-analytics.
- This slice must not mutate operational corpus content or live evidence stores.

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

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD_TEMPLATE.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_READINESS_RULES.md`
- `tests/test_domain_baseline_capture_batch.py`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Reporting

Report files changed, whether the slice was docs/tests only, test results, `git diff --check` result, `.pytest_tmp` status, and confirmation that no source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM call, DB write, schema migration, endpoint change, UI change, workforce-platform change, award-configurator-v1 change, ezeas-analytics change, current-truth promotion, answer-use permission, or deep-review execution was introduced.

Suggested commit message: `minerva-historical-batch-review-decision-record-v01`

# Minerva Historical Batch Review Queue v0.1

Date: 16 May 2026

## Objective

Create the first governed historical batch review queue for Minerva.

This slice moves Minerva historical batch registration from static metadata registration toward a controlled queue/readiness model that records which registered historical sources are eligible for future deep review, which are blocked, and why.

## Context

Historical source registration, registered folders, validation controls, review-readiness records, review templates, decision gates, cross-check plans, findings templates, review execution checklists, NOT_REVIEWED decision records, batch registration, developer-log batch intake, the first developer-log batch register, the first metadata-only populated row, and the batch register index already exist.

The current truth boundary remains unchanged:

- Historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed.
- Batch registration is metadata-only.
- Batch registration does not ingest source content.
- Batch registration does not permit Minerva to answer current-state questions from historical material.
- NOT_REVIEWED sources remain NOT_REVIEWED.
- Ingestion permitted remains No unless a future governed ingestion slice explicitly changes it.
- The historical Analytics Engine developer log remains historical and not reviewed unless a future review slice changes that status with evidence.
- ezeas-intelligence must remain separate from workforce-platform, award-configurator-v1, and ezeas-analytics.
- This slice must not mutate operational corpus content or live evidence stores.

## Required Posture

Documentation/control/test hardening only.

No source content ingestion. No operational corpus mutation. No Code Evidence ingestion. No live LLM calls. No database writes. No schema migrations. No endpoint changes. No UI changes. No workforce-platform changes. No award-configurator-v1 changes. No ezeas-analytics changes. No current-truth promotion. No historical source may become answerable current truth in this slice.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_READINESS_RULES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE_ENTRY_TEMPLATE.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`
- `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Queue Statuses

- `REGISTERED_NOT_TRIAGED`
- `TRIAGED_NOT_READY_FOR_REVIEW`
- `READY_FOR_DEEP_REVIEW`
- `REVIEW_IN_PROGRESS`
- `REVIEW_COMPLETE_NOT_INGESTED`
- `BLOCKED_NEEDS_SOURCE_FILES`
- `BLOCKED_NEEDS_REPOSITORY_CROSS_CHECK`
- `BLOCKED_SUPERSEDED_OR_DUPLICATE`
- `DO_NOT_REVIEW_ARCHIVAL_ONLY`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Reporting

Report files changed, whether the work was docs/tests only or included a metadata helper, test results, `git diff --check` result, `.pytest_tmp` status, and confirmation that no source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM call, DB write, schema migration, endpoint change, UI change, workforce-platform change, award-configurator-v1 change, ezeas-analytics change, current-truth promotion, or answer-use permission was introduced.

Suggested commit message: `minerva-historical-batch-review-queue-v01`

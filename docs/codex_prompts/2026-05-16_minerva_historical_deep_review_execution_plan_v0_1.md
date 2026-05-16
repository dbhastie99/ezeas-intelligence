# Minerva Historical Deep Review Execution Plan v0.1

Date: 16 May 2026

## Objective

Create the first governed historical deep-review execution plan for Minerva.

This slice defines the controlled process a future reviewer must follow when a historical source has a queue entry, candidate selection, and decision record permitting review start. It creates review execution controls, checklist controls, findings-output expectations, and tests.

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

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_CHECKLIST.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_READINESS_RULES.md`
- `tests/test_domain_baseline_capture_batch.py`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Boundary

This durable prompt/control artefact records the requested slice and does not itself perform deep review, ingest source content, backfill corpus, mutate operational evidence, promote current truth, or change answer synthesis.

# Minerva Historical Answer-Use Permission Gate v0.1

Date: 16 May 2026

## Objective

Create the first governed answer-use permission gate for Minerva historical knowledge.

This slice defines the decision gate that controls whether reviewed, classified, ingested/backfilled, and current-truth-promoted historical evidence may be used by Minerva in answers.

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
- No retrieval runtime changes.
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No historical source may become answerable current truth in this slice.

## Artefacts To Create

- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_SCOPE_RULES.md`

## Artefacts To Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_REVIEW_CHECKLIST.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md`
- `tests/test_domain_baseline_capture_batch.py`

## Acceptance Checks

The new gate must include the answer-use status model, preconditions, current-truth dependency, ingestion/backfill dependency, evidence and answer scope rules, citation/provenance requirements, conflict/supersession handling, refusal boundary, retrieval boundary, chat exposure boundary, blocker handling, explicit non-goals, and developer handoff.

Current-truth promotion, ingestion/backfill, review classification, decision records, queueing, candidate selection, and registration must remain separate from answer-use approval.

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-answer-use-permission-gate-v01`

# Codex Prompt - Minerva Historical Ingestion/Backfill Decision Control v0.1

Date: 16 May 2026

Mode: Documentation/control/test hardening only.

## Objective

Create the first governed ingestion/backfill decision-control model for Minerva historical knowledge.

This slice defines the decision gate between classified historical review findings and any future ingestion/backfill work. It specifies what evidence, classifications, outcome decisions, cross-checks, blockers, provenance, rollback requirements, and current-truth boundaries must exist before ingestion/backfill can even be considered.

## Required Artefacts

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md`

Update:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDING_CLASSIFICATION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Posture

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

## Current Truth

Historical sources are not current truth unless reviewed, cross-checked, backfilled, ingested through a governed process, and explicitly promoted.

Batch registration, review queueing, candidate selection, decision records, deep-review execution planning, findings classification, and outcome decisions are metadata/control-only stages unless a later governed slice explicitly changes permission.

A classified finding is not ingestion, current truth, or answer-use permission.

`CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` is still only a candidate.

`OUTCOME_READY_FOR_INGESTION_DECISION` only means an ingestion/backfill decision may be considered. It does not approve ingestion.

`OUTCOME_READY_FOR_ANSWER_USE_DECISION` only means an answer-use decision may be considered. It does not permit answer use.

Ingestion permitted remains No unless a future governed ingestion/backfill decision explicitly changes it.

Backfill permitted remains No unless a future governed ingestion/backfill decision explicitly changes it.

Current-truth promotion permitted remains No unless a future governed current-truth decision explicitly changes it.

Answer use remains No unless a future governed answer-use/current-truth decision explicitly changes it.

Ingestion/backfill approval does not automatically mean current truth. Current-truth approval does not automatically mean answer-use permission. Answer-use permission must remain a separate decision.

Historical-only findings must not be used as current answers. Superseded findings must not be used as current truth. Conflicting findings must be blocked until conflict resolution. Duplicate findings should link to existing evidence rather than create duplicate truth. Backlog/follow-up findings may inform planning but must not be represented as implemented behaviour.

Required conservative defaults:

- `IngestionPermitted`: No
- `BackfillPermitted`: No
- `CurrentTruthPromotionPermitted`: No
- `AnswerUsePermitted`: No
- `OperationalCorpusMutationPermitted`: No
- `CodeEvidenceIngestionPermitted`: No
- `DatabaseWritePermitted`: No
- `LiveLLMUsePermitted`: No
- `ChatExposurePermitted`: No

## Required Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Progress Target

After this slice, narrow safe internal chat pilot readiness should move from about 42% to about 46%.

Remaining major phases: backfill execution design, current-truth promotion control, answer-use permission gating, retrieval safety, chat answer contract, and pilot surface.

Suggested commit message: `minerva-historical-ingestion-backfill-decision-control-v01`

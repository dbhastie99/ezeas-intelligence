# Codex Prompt - Minerva Historical Current-Truth Promotion Control v0.1

Date: 16 May 2026

Mode: Documentation/control/test hardening only.

## Objective

Create the current-truth promotion control layer for historical findings and backfilled evidence.

This slice defines how reviewed/backfilled historical evidence may later be considered for current-truth promotion, while preserving that current-truth promotion is still not performed in this slice.

## Required Artefacts

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_REVIEW_CHECKLIST.md`
- `docs/codex_prompts/2026-05-16_minerva_historical_current_truth_promotion_control_v0_1.md`

Update:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_RUNBOOK.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required State Separation

The model must separate:

- historical source registered
- historical source reviewed
- finding classified
- ingestion/backfill decision approved
- backfill execution completed
- backfilled evidence validated
- current-truth candidate identified
- current-truth promotion review started
- current-truth promotion blocked
- current-truth promotion deferred
- current-truth promotion approved in a future explicit slice
- answer-use permission remains separate

## Required Conservative Defaults

- `CurrentTruthPromotionPermitted`: No
- `CurrentTruthPromotionApplied`: No
- `AnswerUsePermitted`: No
- `CorpusMutationPermitted`: No
- `DatabaseWritePermitted`: No
- `ChatExposurePermitted`: No
- `LiveLLMUsePermitted`: No
- `CodeEvidenceIngestionPermitted`: No

## Required Boundaries

- This slice defines the control model only.
- It does not promote any historical finding to current truth.
- It does not change any answer-use permissions.
- It does not mutate corpus.
- It does not write to a database.
- It does not ingest source content.
- It does not call a live LLM.
- It does not expose chat.
- Current-truth promotion is separate from ingestion/backfill.
- Current-truth promotion is separate from answer-use permission.
- Backfilled evidence can remain historical-only.
- A current-truth candidate is not current truth until approved by a later explicit promotion slice.
- A current-truth approved item is still not answer-use approved unless answer-use permission is separately granted.

## Required Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-current-truth-promotion-control-v01`

# Codex Prompt - Minerva Historical Backfill Execution Design v0.1

Date: 16 May 2026

Mode: Documentation/control/test hardening only.

## Objective

Design the future execution model for historical backfill after an ingestion/backfill decision has been approved.

This slice must remain design/control only. It must not perform ingestion, mutate corpus, write to a database, promote current truth, permit answer use, or expose chat.

## Required Artefacts

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_SAFETY_CHECKLIST.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_AUDIT_RECORD_TEMPLATE.md`
- `docs/codex_prompts/2026-05-16_minerva_historical_backfill_execution_design_v0_1.md`

Update:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md`
- `tests/test_domain_baseline_capture_batch.py`

## Future Backfill Stages

The design must define:

- decision approved
- source scope frozen
- source authority checked
- supersession/conflict checked
- duplicate linking checked
- sensitivity and tenant-data risk checked
- evidence extraction plan prepared
- backfill dry-run prepared
- backfill dry-run reviewed
- backfill apply approved
- backfill apply executed in a future explicit slice
- post-backfill validation
- current-truth promotion decision remains separate
- answer-use decision remains separate

## Required Conservative Defaults

- `BackfillExecutionPermitted`: No
- `BackfillDryRunPermitted`: No, unless a later explicit dry-run slice approves it
- `CorpusMutationPermitted`: No
- `DatabaseWritePermitted`: No
- `CurrentTruthPromotionPermitted`: No
- `AnswerUsePermitted`: No
- `ChatExposurePermitted`: No
- `CodeEvidenceIngestionPermitted`: No
- `LiveLLMUsePermitted`: No

## Required Posture

- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No runtime answer behaviour changes.
- No current-truth promotion.
- No answer-use permission.
- No chat exposure.
- No historical source may become answerable current truth in this slice.

## Required Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-backfill-execution-design-v01`

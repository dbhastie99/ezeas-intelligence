# Codex Prompt - Minerva Historical Knowledge Control Index v0.1

Date: 15 May 2026

Mode: Documentation/control-model hardening only

## Objective

Create the Minerva Historical Knowledge Control Index v0.1 before any historical chats, developer logs, doctrine documents, or code evidence are ingested.

Create these durable control artefacts:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

Update `tests/test_domain_baseline_capture_batch.py` or create a focused test file if that is cleaner.

## Required Control Position

The historical control model must state that pre-control-model historical knowledge is incomplete and not yet captured to the same durable standard as the new formal-evidence model.

The model must define source tiers:

- Tier 1 code and tests as highest authority for implemented state.
- Tier 2 developer logs, hardening logs, and platform doctrine as curated decision/rationale sources requiring review.
- Tier 3 historical chats and continuance prompts as raw historical source material, not final truth.

Historical chats must not be ingested directly as truth. They must be cross-checked against logs, doctrine, code, tests, and commits.

Developer logs and doctrine documents are valuable but may include planned, partial, superseded, or backlog work, so they require implementation-state classification.

Code/tests must be used to confirm implemented behaviour, but code alone may not explain why.

## Implementation-State Classifications

The model must define:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## Domain-Scoped Backfill Process

The process must:

1. Identify historical source material.
2. Register source provenance.
3. Classify source tier.
4. Extract candidate decisions.
5. Cross-check against code/tests/logs/doctrine/commits.
6. Classify implementation state.
7. Create a curated backfill evidence pack.
8. Add a review gate.
9. Only later consider governed ingestion.

## Explicit Slice Boundaries

This slice does not:

- consume historical chats
- ingest developer logs
- ingest doctrine documents
- ingest code
- mutate corpus
- run live LLM
- connect Code Evidence
- change runtime behaviour
- promote baselines
- change ledger counts
- implement DB writes
- implement migrations
- change endpoints
- change UI
- change workforce-platform
- change award-configurator-v1
- run historical ingestion
- approve review
- run governed ingestion
- run recapture
- run benchmark execution
- run corpus coverage execution
- run answer-gap execution
- create generated artefacts
- update the ledger

This slice does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.

Do not mark any domain `BASELINE_ALREADY_EXISTS`.

## Initial Priority Domains

The future historical backfill priority domains are:

- Worker Story
- ObjectTime / Source Truth
- Process Periods / PayRun Lifecycle
- Payroll Buckets / Bases / Totals
- Deductions and Obligations
- Tax / PAYG
- Imports / Actuals
- Leave Workflow / Annual Leave
- Award Configurator
- Asphalt Award Build

Tax / PAYG and Imports / Actuals remain governed by the formal evidence control model and remain `BASELINE_REQUIRED` and `NOT_REVIEWED` until their separate formal review path changes.

## Required Tests

Tests must assert:

- all four historical knowledge files exist
- the control index references the gap register, source tiering model, and backfill process
- the gap register states pre-control-model knowledge is incomplete
- the source tiering model defines all three source tiers
- the backfill process includes all implementation-state classifications
- the backfill process states chats are raw source material not final truth
- the documents state no corpus mutation, no direct historical ingestion, no Code Evidence integration, no live LLM calls, no runtime changes, no ledger promotion, and no baseline promotion occur in this slice
- priority domains are listed
- this prompt file is preserved

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report:

- files changed
- historical control files created
- tests run
- `.pytest_tmp` status
- confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes

Suggested commit message: `minerva-historical-knowledge-control-index-v01`

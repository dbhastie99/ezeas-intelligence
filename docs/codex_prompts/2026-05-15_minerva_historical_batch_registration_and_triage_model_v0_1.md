# Minerva Historical Batch Registration And Triage Model v0.1

Date: 15 May 2026

## Objective

Create the durable control artefacts for Minerva historical batch registration and triage so many historical sources can be registered and classified without repeating the full Analytics Engine deep-review chain for every developer log, doctrine document, hardening log, chat, or continuance prompt.

## Context

The Analytics Engine developer log is the prototype for the full deep-review path: source register, placeholder, review-readiness record, review pack template, decision gate, code cross-check plan, findings template, review execution checklist, and `NOT_REVIEWED` decision record.

That path is appropriate for high-value or high-risk historical sources. It is not the default path for every historical source. Most historical sources should first be batch-registered and triaged at metadata level only.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md`

## Required Controls

The model must state that batch registration is metadata-level only; batch triage does not ingest historical content; batch triage does not make a source current truth; the source register remains the governing classification point; registered folders and filenames are aids only; and `Ingestion permitted` defaults to `No`.

The batch triage fields must include source type, source tier, domain tags, review status, implementation-state classification, supersession risk, backfill priority, and whether a full review chain is required.

Only high-value or high-risk sources graduate to the full review-readiness, decision-gate, and code/test/schema cross-check path.

The batch register template must define the required columns listed in the slice request, including full review chain requirement and reason.

The triage process must define outcomes: `REGISTER_ONLY`, `REGISTER_AND_MONITOR`, `NEEDS_DOMAIN_REVIEW`, `NEEDS_CODE_CROSSCHECK`, `NEEDS_FULL_REVIEW_CHAIN`, `SUPERSEDED_HISTORICAL_ONLY`, `DUPLICATE_OR_COVERED_BY_EXISTING_SOURCE`, and `UNCERTAIN_REQUIRES_REVIEW`.

The full review chain escalation criteria are: major architecture decisions; possible supersession by later platform changes; influence on current Minerva answers; high-risk domains including payroll calculation, ObjectTime source truth, tax, imports/actuals, reconciliation, deductions/obligations, leave, worker story, analytics, award configurator, or finalised correction; conflicting claims; and implementation claims requiring code/test/schema confirmation.

Ordinary developer logs can remain batch-registered until needed. Many sources can be grouped by domain/date range rather than creating separate deep-review artefacts for every file.

## Boundaries

Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not parse or extract historical source content. Do not review historical sources. Do not mutate corpus.

Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

The documents must state batch registration does not mutate corpus, does not ingest, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, and does not make batch-registered sources current truth unless later reviewed, backfilled, and governed.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report changed files, test results, `.pytest_tmp` status, and confirmation that no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes were made.

Suggested commit message: `minerva-historical-batch-registration-and-triage-model-v01`

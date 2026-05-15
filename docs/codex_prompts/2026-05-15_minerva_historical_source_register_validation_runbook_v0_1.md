# Codex Prompt - Minerva Historical Source Register Validation Runbook v0.1

Date: 15 May 2026

Mode: Documentation/control-runbook validation only

## Slice

Create the durable validation rules for Minerva historical source registration before real historical documents are added.

This slice is Minerva Historical Source Register Validation Runbook v0.1.

## Required Outputs

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`

Update if needed:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`
- `docs/evaluation/historical_knowledge/registered_sources/README.md`

Update `tests/test_domain_baseline_capture_batch.py` or create a focused historical knowledge test file.

## Required Doctrine

The validation runbook must preserve that folder placement alone is not registration. A source file is registered only when `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` contains a corresponding register entry with source type, source tier, review status, implementation-state classification, ingestion permission, and provenance fields.

Files under `docs/evaluation/historical_knowledge/registered_sources/` without corresponding register entries are `UNREGISTERED_SOURCE_MATERIAL`.

Unregistered source material must not be ingested, cited as final truth, used for baseline promotion, or used as implemented-state evidence.

Registered source type comes from the register entry, not the filename. Original filename is metadata only.

## Required Runbook Sections

1. Purpose
2. Scope
3. Validation Principle
4. Registered Source Definition
5. Unregistered File Definition
6. Required Register Entry Fields
7. Folder-to-Source-Type Expectations
8. Validation Rules
9. Allowed Exceptions
10. Failure Handling
11. Backfill Workflow Integration
12. Non-Goals
13. Future Automation

## Required Source Types

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `MIXED_LOG_DOCTRINE`
- `CHAT_OR_CONTINUANCE`
- `CODE_EVIDENCE`
- `TEST_EVIDENCE`
- `PROMPT_FILE`
- `BASELINE_PACK`
- `AWARD_BUILD_CONTROL`
- `OTHER_REQUIRES_REVIEW`

## Required Implementation-State Classifications

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## Boundaries

Do not populate real historical source documents yet. Do not ingest historical chats, developer logs, doctrine documents, or code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, validation runbook created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-source-register-validation-runbook-v01`

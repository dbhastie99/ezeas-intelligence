# Minerva Historical Source Folder Structure v0.1

Date: 15 May 2026

## Purpose

Create the empty registered source folder structure that future historical backfill slices will use.

This slice preserves the existing register-driven classification model: Minerva follows registered source folders and source-register entries, not brittle individual filenames.

## Scope

Create `docs/evaluation/historical_knowledge/registered_sources/` with a root README and empty controlled source-type subfolders.

Required subfolders:

- `developer_logs`
- `hardening_logs`
- `platform_doctrine`
- `mixed_log_doctrine`
- `chat_continuance`
- `code_evidence`
- `test_evidence`
- `prompt_files`
- `baseline_packs`
- `award_build_control`
- `other_requires_review`

Because Git does not track empty directories, each subfolder must contain a short `README.md` or `.gitkeep`. Prefer `README.md` with the intended source type, starting tier/default reliability, and the rule that files placed there still require a `HISTORICAL_SOURCE_REGISTER.md` entry before they are treated as registered historical sources.

## Required Control Updates

Update these historical knowledge controls if needed so they reference `docs/evaluation/historical_knowledge/registered_sources/` as the registered folder root:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`

## Required Root README Statements

The root `registered_sources/README.md` must state:

- registered folders are a discovery and classification aid, not automatic truth;
- a file placed in a registered folder still requires a source register entry;
- filenames are metadata/hints only;
- source classification remains register-driven;
- no historical source is ingested merely by placing it in a folder;
- no corpus mutation, Code Evidence integration, live LLM call, runtime change, baseline promotion, or ledger promotion occurs from this folder structure.

## Required Subfolder README Source Types

- `developer_logs` => `DEVELOPER_LOG`
- `hardening_logs` => `HARDENING_LOG`
- `platform_doctrine` => `PLATFORM_DOCTRINE`
- `mixed_log_doctrine` => `MIXED_LOG_DOCTRINE`
- `chat_continuance` => `CHAT_OR_CONTINUANCE`
- `code_evidence` => `CODE_EVIDENCE`
- `test_evidence` => `TEST_EVIDENCE`
- `prompt_files` => `PROMPT_FILE`
- `baseline_packs` => `BASELINE_PACK`
- `award_build_control` => `AWARD_BUILD_CONTROL`
- `other_requires_review` => `OTHER_REQUIRES_REVIEW`

Each subfolder README must state that the folder/source type gives a starting classification and reliability tier only, and that final reliance requires register entry, review status, implementation-state classification, and cross-checking where relevant.

## Tests

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. `registered_sources/README.md` exists.
2. All required source subfolders exist.
3. Each required subfolder has `README.md` or `.gitkeep`.
4. The root README states registered folders do not make files final truth.
5. The root README states a source register entry is still required.
6. The root README states filenames are metadata/hints only.
7. The root README states no ingestion or corpus mutation occurs from folder placement.
8. Each source subfolder README declares the expected source type.
9. `HISTORICAL_SOURCE_REGISTER.md` references `registered_sources/`.
10. `HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md` references `registered_sources/`.
11. `HISTORICAL_BACKFILL_PROCESS.md` references `registered_sources/`.
12. `HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md` references `registered_sources/`.

## Explicit Non-Goals

Do not populate real historical source documents yet. Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Reporting

Report files changed, registered source folder structure created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-source-folder-structure-v01`

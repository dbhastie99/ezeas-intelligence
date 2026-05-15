# Codex Prompt - Minerva Historical Register-Driven Source Classification v0.1

Date: 15 May 2026

Mode: Documentation/control-model hardening only

## Slice

Create the durable historical knowledge rule that Minerva follows registered source folders and source-register entries, not brittle individual filenames.

This slice is Minerva Historical Register-Driven Source Classification v0.1.

## Required Outputs

Create or update:

- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE.md`

Update `tests/test_domain_baseline_capture_batch.py` or create a focused historical knowledge test file if cleaner.

## Required Model

The model must state clearly:

1. source classification is register-driven, not filename-driven.
2. Registered folders and source-register entries are the durable discovery mechanism.
3. Individual filenames are metadata and may be hints only.
4. Hardcoded individual document names must not be used as the primary source classification mechanism.
5. The register assigns source class and starting reliability tier.
6. A registered source does not become final truth until review status, implementation-state classification, and relevant cross-checking have been completed.
7. A document can be classified as `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `CHAT_OR_CONTINUANCE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_FILE`, `BASELINE_PACK`, `AWARD_BUILD_CONTROL`, or `OTHER_REQUIRES_REVIEW` even if the filename does not contain those exact words.

Required source types:

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

Required register fields:

- Source title
- Original filename
- Source folder
- Registered source type
- Source tier
- Domain tags
- Date or date range
- Repository context
- Related commits if known
- Related control artefacts
- Implementation-state classification
- Review status
- Ingestion permitted
- Supersession status
- Evidence confidence
- Notes

Implementation-state classifications:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## Required Tier Rules

Preserve the existing source-tier rules:

- Code and tests are highest authority for implemented state.
- Developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review and implementation-state classification.
- Historical chats and continuance prompts are raw historical source material, not final truth, and require cross-checking.
- Code alone may prove what exists, but may not explain why a decision was made.
- Logs and doctrine may explain why, but may include planned, partial, superseded, or backlog work.
- Chats may contain valuable context, but must not be ingested directly as truth.

## Required Boundaries

This slice does not ingest any historical documents, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not ingest code, does not mutate corpus, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice must not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, historical ingestion, corpus mutation, or generated artefact creation.

Do not change ledger counts. Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, register-driven classification model created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

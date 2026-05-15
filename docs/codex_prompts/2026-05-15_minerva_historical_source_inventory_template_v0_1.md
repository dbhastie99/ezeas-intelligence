# Codex Prompt - Minerva Historical Source Inventory Template v0.1

Date: 15 May 2026

Mode: Documentation/control-model hardening only

## Slice

Create durable historical source inventory templates for Minerva without ingesting, reviewing, promoting, or connecting any historical material.

This slice is Minerva Historical Source Inventory Template v0.1.

## Required Outputs

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE.md`

Update `tests/test_domain_baseline_capture_batch.py` or another appropriate focused test file.

## Required Source Controls

Each template must reference:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## Required Inventory Fields

Each template must define these fields:

- Source title
- Source type
- Source tier
- Date or date range
- Repository/domain
- Related commits if known
- Related developer log or doctrine reference
- Implementation-state classification
- Evidence confidence
- Supersession risk
- Backlog/doctrine/runtime distinction
- Review required
- Ingestion permitted
- Notes

## Required Classifications

Each template must include:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## Required Tier Rules

The developer log/doctrine template must treat logs and doctrine as curated decision/rationale sources requiring review and implementation-state classification.

The chat/continuance template must treat chats and prompts as raw historical source material, not final truth, requiring cross-check against code/tests/logs/doctrine/commits.

The code evidence template must treat code/tests as highest authority for implemented state while preserving that code alone may not explain why.

The general source inventory template must preserve the Tier 1/Tier 2/Tier 3 source rules from `HISTORICAL_SOURCE_TIERING_MODEL.md`.

## Required Boundaries

The templates must state that inventory alone:

- does not mutate corpus
- does not ingest sources
- does not connect Code Evidence
- does not run live LLM
- does not change runtime behaviour
- does not promote baselines
- does not change ledger counts

This slice must not consume historical chats, ingest developer logs, ingest doctrine documents, ingest code, mutate corpus, implement DB writes, run migrations, connect Code Evidence, call a live LLM, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change runtime behaviour, grant review approval, run governed ingestion, run recapture, run benchmark execution, run corpus coverage execution, run answer-gap execution, promote baselines, update ledgers, or create generated evaluation artefacts.

## Required Tests

Tests must assert that all four inventory template files:

- exist
- reference the historical knowledge control files
- include the required fields
- include all implementation-state classifications
- preserve source-tier rules for logs/doctrine/chats/code
- state no corpus mutation, no historical ingestion, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, and no ledger promotion occurs

## Verification

Run:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `git diff --check`

Clean `.pytest_tmp` if present.

Report files changed, inventory templates created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-source-inventory-template-v01`

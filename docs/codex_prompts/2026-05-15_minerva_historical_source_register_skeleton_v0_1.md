# Codex Prompt - Minerva Historical Source Register Skeleton v0.1

Date: 15 May 2026

Mode: Documentation/control-register skeleton only

## Slice

Create the actual historical source register skeleton that future historical backfill slices will populate.

This slice is Minerva Historical Source Register Skeleton v0.1.

The register must follow the existing register-driven classification model: Minerva follows registered source folders/register entries, not brittle individual filenames.

## Required Outputs

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`

Update if needed:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_INVENTORY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`

Update `tests/test_domain_baseline_capture_batch.py` or create a focused historical knowledge test file.

## Required Register Sections

The register skeleton must be empty or placeholder-only. It must not inventory actual historical chats, developer logs, doctrine documents, or code evidence yet.

The register must include sections:

1. Purpose
2. Scope
3. Register-Driven Classification Rule
4. Source Register Table
5. Required Register Fields
6. Source Type Definitions
7. Source Tier Defaults
8. Review Status Definitions
9. Implementation-State Classifications
10. Ingestion Permission Rules
11. Non-Goals
12. Future Population Workflow

## Required Source Register Table Columns

- Register ID
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

## Required Review Statuses

- `NOT_REVIEWED`
- `NEEDS_REVIEW`
- `REVIEWED_READY_FOR_BACKFILL_DRAFT`
- `REVIEWED_READY_FOR_GOVERNED_INGESTION`
- `SUPERSEDED`

## Required Rules

The register must state:

- source classification is register-driven, not filename-driven;
- registered folders/register entries are the durable discovery mechanism;
- filenames are metadata and hints only;
- hardcoded individual document names must not be used as the primary classification mechanism;
- a registered source does not become final truth until review status, implementation-state classification, and relevant cross-checking have been completed;
- inventory/registering a source does not itself permit ingestion;
- no historical source is ingested by this skeleton slice.

## Required Tests

Tests must assert:

1. `HISTORICAL_SOURCE_REGISTER.md` exists.
2. The control index references `HISTORICAL_SOURCE_REGISTER.md`.
3. The register states classification is register-driven, not filename-driven.
4. The register states filenames are metadata/hints only.
5. The register includes all required table columns.
6. The register includes all required source types.
7. The register includes all implementation-state classifications.
8. The register includes all review statuses.
9. The register states registering a source does not permit ingestion.
10. The register states no historical source is ingested by this slice.
11. The backfill process or source inventory template references `HISTORICAL_SOURCE_REGISTER.md`.

## Boundaries

Do not populate real historical source rows yet. Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, source register skeleton created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-source-register-skeleton-v01`

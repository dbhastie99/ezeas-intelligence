# Codex Prompt - Minerva Historical Source Review Readiness Template v0.1

Mode: Documentation/control-model hardening only

Date: 15 May 2026

## Objective

Create the review-readiness template and process for registered historical sources before any source can become a curated historical backfill evidence pack.

This slice builds on:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/registered_sources/`

## Required Outputs

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REVIEW_READINESS_PROCESS.md`

Update references if needed in:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`

## Required Template Fields

The template must include:

- Register ID
- Source title
- Original filename
- Registered source type
- Source tier
- Source folder
- Domain tags
- Date or date range
- Repository context
- Related commits if known
- Related control artefacts
- Review owner
- Review date
- Review status before review
- Target review status
- Implementation-state classification before review
- Target implementation-state classification
- Supersession status
- Evidence confidence
- Ingestion permitted before review
- Target ingestion permitted
- Source summary
- Candidate decisions extracted
- Candidate doctrine extracted
- Candidate backlog items extracted
- Candidate implemented-state claims
- Code/test/commit cross-check required
- Code/test/commit cross-check result
- Superseded or conflicting claims
- Current truth classification
- Minerva answering implication
- Backfill evidence pack recommendation
- Reviewer rationale
- Required follow-up actions

## Required Process Rules

The process must state:

1. A registered source is not final truth merely because it exists in the register.
2. Review readiness is required before creating a historical backfill evidence pack.
3. The review must distinguish implemented behaviour, doctrine, backlog, planned-not-implemented work, superseded work, and uncertain claims.
4. Developer logs and doctrine documents require implementation-state classification.
5. Historical chats and continuance prompts require cross-checking and are raw source material, not final truth.
6. Code/tests are strongest for implemented state but may not explain decision rationale.
7. A source may be reviewed for backfill draft readiness without permitting governed ingestion.
8. Review readiness does not mutate corpus, does not ingest the source, does not run Code Evidence integration, does not call live LLM, does not promote baselines, and does not change ledger counts.
9. The Analytics Engine developer log remains NOT_REVIEWED and ingestion permitted No until a future explicit review slice.

## Controlled Values

Review status values:

- `NOT_REVIEWED`
- `NEEDS_REVIEW`
- `REVIEWED_READY_FOR_BACKFILL_DRAFT`
- `REVIEWED_READY_FOR_GOVERNED_INGESTION`
- `SUPERSEDED`

Implementation-state classifications:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## Boundaries

This slice creates templates/process only and does not review, ingest, parse, or consume any historical source.

Do not ingest historical chats. Do not ingest developer logs. Do not ingest doctrine documents. Do not ingest code. Do not review the Analytics Engine source yet. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-source-review-readiness-template-v01`

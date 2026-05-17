# Minerva Next Phase Decision Point v0.1

## Decision Required

Choose the next Minerva phase deliberately. Controlled regression execution is complete at controlled-readiness level only.

## Option A: Controlled Evaluation Report Export File Writer

Add a deterministic file writer for controlled evaluation report exports, without enabling runtime behaviour.

## Option B: Controlled Corpus / Evidence Intake Planning

Plan corpus and evidence intake boundaries before any mutation or ingestion is authorised.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness boundaries before any Code Evidence ingestion is authorised.

## Option D: Keep Minerva Paused While Award Recovery Continues

Make no Minerva runtime or data-surface changes while award recovery work continues.

## Preconditions For Each Option

- Option A requires explicit approval for deterministic local file output only.
- Option B requires explicit approval for planning only, with no corpus mutation.
- Option C requires explicit approval for planning only, with no Code Evidence ingestion.
- Option D requires no runtime, data, exposure, or integration action.

## What Must Not Be Done Without Explicit Authorisation

Do not enable chat exposure, register endpoints or routes, call a live LLM, generate final natural-language answers, connect to or read/write a DB, create migrations, mutate corpus, ingest Code Evidence, alter live retrieval backend behaviour, change workforce-platform, change ezeas-analytics, change UI, or claim runtime, deployment, or production readiness.

## Recommended Default Next Step

Option A is the default only if a deterministic local export file writer is needed for developer handoff. Otherwise keep Minerva paused while the next phase is selected.

## Developer Handoff

Treat this decision point as a hard boundary. The closeout ledger completes controlled regression execution, but it does not select or authorise the next phase.

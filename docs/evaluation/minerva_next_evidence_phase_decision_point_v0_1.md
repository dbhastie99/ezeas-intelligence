# Minerva Next Evidence Phase Decision Point v0.1

## Decision Required

The governed evidence intake phase is complete at planning/readiness level only. The next Minerva evidence phase must be chosen deliberately before further work is authorised.

## Option A: Controlled Evidence Intake Dry-Run / No-Corpus-Mutation

Run a deterministic dry-run that classifies candidate evidence and reports planned handling without ingesting evidence or mutating corpus state.

## Option B: Controlled External Evidence Summary Catalogue

Create a deterministic catalogue of external evidence summaries and caveats without ingestion, corpus mutation, runtime retrieval, or final answer generation.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness boundaries, candidate source types, review caveats, and future authorisation gates without ingesting Code Evidence.

## Option D: Keep Minerva Paused While Award Recovery Continues

Perform no new evidence intake activity and keep Minerva in controlled-readiness posture while award recovery remains the priority.

## Preconditions For Each Option

Each option requires a separate prompt/control artefact, focused deterministic tests where service behaviour changes, explicit no-action boundaries, and verification that no runtime, DB, corpus, endpoint, live LLM, or cross-repo integration behaviour is introduced.

## What Must Not Be Done Without Explicit Authorisation

Do not ingest evidence, mutate corpus state, ingest Code Evidence, connect to a DB, read or write DB data, create migrations, call a live LLM, change live retrieval backend behaviour, generate final natural-language answers, expose chat, register endpoints, change UI, change workforce-platform, change ezeas-analytics, or claim production/deployment/runtime readiness.

## Recommended Default Next Step

Option A is the recommended default if the next objective is to exercise the prepared controls while preserving no-corpus-mutation posture.

## Developer Handoff

If a next phase is selected, create a new durable prompt/control artefact for that phase and keep the current closeout ledger as the boundary record for governed evidence intake planning completion.

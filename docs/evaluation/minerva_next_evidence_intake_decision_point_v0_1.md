# Minerva Next Evidence Intake Decision Point v0.1

## Decision Required

Choose the next Minerva evidence-intake phase explicitly. The first no-mutation intake execution phase is complete only at controlled-readiness/no-mutation level.

## Option A: Controlled Durable Evidence Intake Design

Design the future durable-ingestion gate, storage boundaries, safety checks, and review requirements without performing ingestion.

## Option B: External Evidence Summary Catalogue

Catalogue external evidence summaries as deterministic planning metadata without durable ingestion, DB writes, corpus mutation, or runtime integration.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness requirements, constraints, and future authorisation gates without ingesting Code Evidence.

## Option D: Pause Minerva While Award Recovery Continues

Pause Minerva evidence-intake expansion and preserve the current controlled-readiness ledger while award recovery work continues.

## Preconditions For Each Option

Option A requires explicit authorisation to design durable-ingestion controls only. Option B requires explicit authorisation to catalogue summaries only. Option C requires explicit authorisation to plan Code Evidence readiness only. Option D requires no runtime change and preserves current boundaries.

## What Must Not Be Done Without Explicit Authorisation

Do not enable internal chat, public chat, production chat, tenant chat, or customer chat. Do not add or register an API route. Do not call a live LLM, generate final natural-language answers, connect to a DB, read from a DB, write to a DB, create migrations, mutate corpus, ingest evidence durably, ingest Code Evidence, alter live retrieval backend behaviour, add credentials, change workforce-platform, change ezeas-analytics, change UI, or claim runtime, deployment, or production readiness.

## Recommended Default Next Step

Option A is the recommended default if Minerva continues, because durable ingestion needs a controlled design gate before any implementation or data movement.

## Developer Handoff

Start the next slice by creating a durable prompt/control artefact for the selected option. Keep it local deterministic docs/tests only unless the selected phase explicitly authorises a broader boundary.

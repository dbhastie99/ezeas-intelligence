# Minerva Next No-Mutation Intake Decision Point v0.1

## Decision Required

Decide whether to move from authorisation closeout into a separately authorised future no-mutation intake execution or keep Minerva paused.

## Option A: First No-Mutation Intake Execution

Execute the reviewed first candidate through a future no-mutation intake path only after explicit authorisation for that new slice.

## Option B: Additional Candidate Review

Review more candidates before any future no-mutation intake execution.

## Option C: External Evidence Summary Catalogue

Create a catalogue of external evidence summaries without evidence ingestion, corpus mutation, Code Evidence ingestion, DB writes, live retrieval, LLM use, or runtime exposure.

## Option D: Keep Minerva Paused While Award Recovery Continues

Do not advance evidence intake. Continue award recovery work while Minerva remains controlled-readiness only.

## Preconditions For Each Option

Option A requires explicit authorisation for a future no-mutation intake execution slice and must preserve no corpus mutation unless separately authorised.

Option B requires candidate metadata and authorisation gate outputs for any additional candidates.

Option C requires a catalogue-only scope and an explicit no-ingestion/no-mutation boundary.

Option D requires no new technical preconditions.

## What Must Not Be Done Without Explicit Authorisation

Do not ingest evidence, mutate corpus, ingest Code Evidence, connect to or read/write a database, register routes, expose chat or endpoints, call live retrieval, call a live LLM, generate final natural-language answers, integrate runtime systems, change workforce-platform, change ezeas-analytics, change UI, deploy, or claim production/runtime readiness.

## Recommended Default Next Step

Default to Option D unless there is explicit authorisation for Option A, Option B, or Option C.

## Developer Handoff

Use this decision point as the next control gate. It does not itself authorise execution, ingestion, mutation, runtime integration, deployment, or production readiness.

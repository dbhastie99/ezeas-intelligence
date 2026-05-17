# Minerva Next Durable Intake Execution Decision Point v0.1

## Decision Required
Choose the next controlled Minerva slice after durable evidence intake authorisation gate setup.

## Option A: Controlled Durable Intake Execution / Review-Only First Candidate
Proceed to a separate execution slice for one review-only first candidate, with explicit authorisation and no automatic expansion to corpus-wide ingestion.

## Option B: External Evidence Summary Catalogue
Catalogue external evidence summaries without durable ingestion, runtime integration, or corpus mutation.

## Option C: Code Evidence Readiness Planning
Plan Code Evidence readiness without ingesting Code Evidence or changing runtime retrieval behaviour.

## Option D: Pause Minerva While Demo Stabilisation Continues
Pause Minerva intake progression and continue demo stabilisation or other non-Minerva work.

## Preconditions For Each Option
Option A requires a candidate that passes eligibility and authorisation gate checks, explicit execution authorisation, rollback/removal policy, sensitive-data review, and no prohibited claims.

Option B requires catalogue scope, source-status boundaries, and no ingestion or runtime claims.

Option C requires Code Evidence planning scope, no ingestion authorisation, and no runtime retrieval changes.

Option D requires no additional technical preconditions.

## What Must Not Be Done Without Explicit Authorisation
Do not perform durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB reads, DB writes, migrations, live retrieval changes, live LLM calls, final answer generation, chat exposure, API route registration, UI changes, workforce-platform changes, ezeas-analytics changes, deployment readiness claims, runtime readiness claims, or production readiness claims.

## Recommended Default Next Step
Default to Option A only if a single first candidate is explicitly selected and separately authorised for review-only execution. Otherwise choose Option B or pause.

## Developer Handoff
The current slice provides the authorisation gate and candidate eligibility metadata only. The next slice must state its chosen option and boundaries before any implementation begins.

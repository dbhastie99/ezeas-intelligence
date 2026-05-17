# Minerva Next Durable Intake Execution Decision Point v0.1

## Decision Required

Choose the next Minerva durable-intake phase explicitly.

## Option A: Controlled Durable Intake Execution / Review-Only First Candidate

Proceed to a review-only first-candidate execution phase with explicit authorisation boundaries and no automatic production/runtime exposure.

## Option B: External Evidence Summary Catalogue

Create a catalogue of external evidence summaries without durable ingestion, corpus mutation, DB writes, live retrieval, live LLM use, final answers, or chat exposure.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness controls without ingesting Code Evidence or mutating the corpus.

## Option D: Pause Minerva While Demo Stabilisation Continues

Keep Minerva paused while other demo stabilisation work continues.

## Preconditions For Each Option

Option A requires explicit future execution authorisation, source-reference lock, source-status boundary verification, evidence envelope, audit envelope, rollback/removal policy, sensitive-data review, no-overstatement checks, and reviewer closeout criteria.

Option B requires a deterministic summary catalogue scope and an explicit no-ingestion/no-mutation boundary.

Option C requires a planning-only scope and an explicit no-Code-Evidence-ingestion boundary.

Option D requires no additional Minerva action.

## What Must Not Be Done Without Explicit Authorisation

Do not perform durable evidence ingestion, corpus mutation, Code Evidence ingestion, DB connection, DB read, DB write, migration, live retrieval, live LLM use, final answer generation, chat exposure, API endpoint or route registration, workforce-platform integration, ezeas-analytics integration, deployment readiness, runtime readiness, or production readiness work.

## Recommended Default Next Step

Option A is the default next decision candidate if the goal is to continue durable intake work, but it must remain review-only until explicitly authorised.

## Developer Handoff

Use the closeout ledger and service output as the handoff. Do not treat phase completion as runtime, deployment, production, ingestion, mutation, or exposure approval.

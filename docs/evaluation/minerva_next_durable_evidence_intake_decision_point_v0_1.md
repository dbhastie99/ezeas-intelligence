# Minerva Next Durable Evidence Intake Decision Point v0.1

## Decision Required

The durable evidence intake design phase is complete at design/readiness level only. The next phase must be explicitly chosen before any further durable-intake work begins.

## Option A: Controlled Durable Evidence Intake Authorisation Gate

Create a gate that evaluates whether a future slice may authorise durable evidence intake under strict preconditions.

## Option B: External Evidence Summary Catalogue

Create a deterministic catalogue of external evidence summaries without ingesting source content, mutating corpus, or treating summaries as current truth.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness boundaries without ingesting Code Evidence or changing runtime behaviour.

## Option D: Pause Minerva While Demo Stabilisation Continues

Defer Minerva durable-intake work while other demo or platform stabilisation continues.

## Preconditions For Each Option

Option A requires explicit authorisation to design an authorisation gate only, not ingestion. Option B requires source-status and no-overstatement controls. Option C requires a no-Code-Evidence-ingestion boundary. Option D requires no additional technical preconditions.

## What Must Not Be Done Without Explicit Authorisation

Do not ingest durable evidence, mutate corpus, ingest Code Evidence, connect to a database, read from a database, write to a database, create migrations, alter live retrieval, call a live LLM, generate final natural-language answers, expose chat, add or register API routes, integrate workforce runtime, integrate analytics runtime, change UI, claim runtime readiness, claim deployment readiness, or claim production readiness.

## Recommended Default Next Step

Default to Option A only if the user explicitly wants to move toward a controlled durable intake authorisation gate. Otherwise pause Minerva durable-intake work.

## Developer Handoff

Use the closeout ledger and phase status documents as the current phase boundary. Treat all runtime, ingestion, mutation, exposure, and readiness claims as unauthorised until a future explicit decision changes scope.

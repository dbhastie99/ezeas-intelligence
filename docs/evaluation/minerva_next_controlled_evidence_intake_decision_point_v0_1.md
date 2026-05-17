# Minerva Next Controlled Evidence Intake Decision Point v0.1

## Decision Required

Choose the next controlled evidence intake phase explicitly before authorising further work.

## Option A: Controlled Evidence Intake Authorisation Gate / First No-Mutation Intake Candidate

Create a gate that selects the first candidate for controlled intake review while still prohibiting ingestion and mutation.

## Option B: Controlled External Evidence Summary Catalogue

Catalogue external evidence summaries at controlled-readiness level without ingesting evidence or mutating corpus state.

## Option C: Code Evidence Readiness Planning

Plan Code Evidence readiness boundaries without ingesting Code Evidence or claiming runtime readiness.

## Option D: Keep Minerva Paused While Award Recovery Continues

Defer additional Minerva intake work while maintaining the current controlled-readiness posture.

## Preconditions For Each Option

Each option requires explicit authorisation, local deterministic scope, no DB access, no live LLM, no live retrieval, no endpoint exposure, no corpus mutation, and no production/deployment/runtime readiness claim.

## What Must Not Be Done Without Explicit Authorisation

Do not ingest evidence, mutate corpus state, ingest Code Evidence, connect to or read/write a DB, create migrations, alter live retrieval backend behaviour, call a live LLM, generate final natural-language answers, expose chat, add or register routes, change UI, integrate workforce-platform, integrate ezeas-analytics, deploy, or claim production/deployment/runtime readiness.

## Recommended Default Next Step

Option A is the recommended default if the next goal is to move toward controlled intake while preserving no-mutation boundaries.

## Developer Handoff

Open the next slice by naming one option and restating the prohibited actions. Closeout of the dry-run phase does not authorise implementation beyond deterministic local planning artifacts.

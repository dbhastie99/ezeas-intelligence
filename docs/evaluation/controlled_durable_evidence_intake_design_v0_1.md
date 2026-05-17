# Controlled Durable Evidence Intake Design v0.1

## Purpose

Define a governed design model for future durable evidence intake without performing durable ingestion, corpus mutation, DB writes, Code Evidence ingestion, live retrieval, live LLM use, route exposure, UI work, runtime integration, deployment, or production work.

## Scope

This slice creates deterministic service metadata, documentation, and tests only. It describes how future durable evidence intake would be represented, reviewed, audited, and bounded before any real mutation is allowed.

## Current Phase

Controlled durable evidence intake design.

## Current Estimated Progress Before Slice

0% complete for the durable evidence intake design phase.

## Expected Progress After Slice

Approximately 55-65% complete for the durable evidence intake design phase.

## Relationship to No-Mutation Intake Execution

The first no-mutation intake execution phase is complete at controlled-readiness level only. Its outputs can inform future review boundaries, but they do not authorise durable ingestion, corpus mutation, DB writes, or Code Evidence ingestion.

## Durable Intake Design Model

The design service returns stable design metadata with a design ID, design status, readiness flag, required design components, missing components, storage boundary model, mutation boundary model, review boundary model, rollback/removal policy requirement, caveats, no-action attestation, and explanation.

The ready status is `DURABLE_EVIDENCE_INTAKE_DESIGN_READY`. This means the design metadata is complete for review only.

## Storage Boundary

Future durable intake must define where durable evidence records would live, what source metadata must be retained, and which storage surfaces remain out of scope until explicit authorisation.

This slice does not create durable evidence records and does not write to any database or corpus.

## Mutation Boundary

Future durable intake must define the exact corpus mutation operation, authorisation gate, rollback/removal handling, reviewer approval, and audit envelope required before mutation.

This slice does not authorise or perform mutation.

## Review Boundary

Future durable intake must require reviewer confirmation, source-status boundary review, evidence envelope review, prohibited-claims review, sensitive-data review, and no-overstatement confirmation.

## Rollback / Removal Policy

A rollback or removal policy is mandatory before future durable intake. The policy must define how a durable evidence item can be removed, superseded, invalidated, or excluded from retrieval after review.

## No Durable Intake Authorised Yet

Durable intake design readiness is not durable intake authorisation. The service always returns `durable_intake_authorised_now` as false.

## No Corpus Mutation Boundary

Corpus mutation remains unauthorised. The service always returns `corpus_mutation_authorised_now` as false.

## No DB Write Boundary

DB writes remain unauthorised. The service always returns `db_write_authorised_now` as false and performs no DB connection, read, write, or migration.

## Code Evidence Boundary

Code Evidence ingestion remains unauthorised. The service always returns `code_evidence_ingestion_authorised_now` as false.

## Runtime / Deployment / Production Boundary

Runtime readiness, deployment readiness, and production readiness are not claimed. Any DB, live retrieval, live LLM, final-answer, chat exposure, endpoint exposure, route registration, runtime, deployment, or production overstatement blocks the design output.

## Developer Handoff

Use `build_controlled_durable_evidence_intake_design(metadata)` to evaluate deterministic design metadata only. Do not wire it into routes, chat, DB paths, retrieval, LLM calls, ingestion jobs, Code Evidence ingestion, workforce-platform, ezeas-analytics, UI, deployment, or production flows.

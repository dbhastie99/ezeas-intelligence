# Controlled Durable Evidence Intake Authorisation Gate v0.1

## Purpose
Define a deterministic local authorisation gate for deciding whether a durable evidence intake candidate may proceed to a future, separate durable intake execution authorisation slice.

## Scope
This slice covers local metadata evaluation, missing prerequisite detection, prohibited claim blocking, documentation, and tests. It does not perform intake or runtime work.

## Current Phase
Controlled durable evidence intake authorisation.

## Current Estimated Progress Before Slice
0% complete for this authorisation slice.

## Expected Progress After Slice
Approximately 55-65% complete because deterministic gate metadata, candidate eligibility, blocked conditions, docs, and tests are defined while preserving no-ingestion/no-mutation boundaries.

## Relationship to Durable Intake Design
The durable intake design phase is a prerequisite. This gate evaluates whether candidate and prerequisite metadata is complete enough to be considered for a later execution slice.

## Relationship to Design Phase Closeout
The design phase closeout remains design/readiness only. This gate does not reopen design execution and does not convert design readiness into durable ingestion.

## Authorisation Status Model
Statuses include `AUTHORISED_FOR_FUTURE_DURABLE_INTAKE_EXECUTION`, missing prerequisite statuses for source reference, source-status boundary, evidence envelope, audit envelope, reviewer confirmation, rollback policy, and sensitive-data review, blocked statuses for durable intake already performed, mutation/DB write, Code Evidence ingestion, live retrieval/LLM/final answer, runtime/production overstatement, and `UNKNOWN_REQUIRES_REVIEW`.

## Future Durable Intake Execution Boundary
An eligible result means only that the candidate may be considered in a later, separately authorised durable intake execution slice.

## No Durable Intake Now Boundary
`durable_intake_authorised_now` and `durable_intake_performed` are always false. This slice does not ingest evidence durably.

## No Corpus Mutation Boundary
`corpus_mutation_performed` is always false. Any corpus mutation claim is blocked.

## No DB Write Boundary
`db_write_performed` is always false. Any DB write or DB access claim is blocked.

## Code Evidence Boundary
`code_evidence_ingestion_performed` is always false. Any Code Evidence ingestion claim is blocked.

## Live Retrieval / LLM / Final Answer Boundary
`live_retrieval_performed`, `live_llm_performed`, and `final_answer_generation_performed` are always false. Related claims are blocked.

## Runtime / Deployment / Production Boundary
`chat_exposure_authorised` and `runtime_integration_authorised` are always false. Runtime, deployment, production, public, tenant, customer, or internal chat exposure claims are blocked.

## No-Action Attestation
The service preserves the repository no-action attestation: no evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, route registration, runtime integration, deployment readiness, or production readiness is authorised or performed.

## What This Slice Authorises
This slice authorises deterministic local metadata evaluation for future durable intake execution eligibility only.

## What This Slice Does Not Authorise
It does not authorise durable evidence intake now, corpus mutation, DB reads or writes, migrations, Code Evidence ingestion, live retrieval, live LLM calls, final answer generation, chat exposure, API routes, UI changes, workforce-platform changes, ezeas-analytics changes, runtime readiness, deployment readiness, or production readiness.

## Developer Handoff
Use `build_controlled_durable_evidence_intake_authorisation_gate(candidate_metadata, prerequisite_metadata=None)` for local deterministic checks. A future execution slice must be separately authorised before any durable ingestion work begins.

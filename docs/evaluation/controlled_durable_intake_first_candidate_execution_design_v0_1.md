# Controlled Durable Intake First Candidate Execution Design v0.1

## Purpose
Define deterministic execution design metadata for a future first-candidate durable evidence intake execution.

## Scope
This slice covers local execution design metadata only. It does not perform durable intake, mutate corpus, connect to a database, call a live LLM, expose chat, add routes, or integrate runtime systems.

## Current Phase
Controlled durable evidence intake authorisation / first candidate execution design.

## Current Estimated Progress Before Slice
Approximately 55-65% complete.

## Expected Progress After Slice
Approximately 85-90% complete after adding deterministic first-candidate execution design metadata, review-pack metadata, docs, and tests while preserving no-ingestion/no-mutation boundaries.

## Relationship to Authorisation Gate
The execution design requires a complete controlled durable evidence intake authorisation gate result showing eligibility for a future durable intake execution. That gate does not authorise execution now.

## Relationship to Candidate Eligibility
The execution design requires complete durable intake candidate eligibility metadata. Eligibility means the candidate can proceed to authorisation and design review only.

## Future Durable Execution Design
The design records a deterministic candidate ID, candidate type, design status, required execution steps, required pre-execution checks, required post-execution checks, rollback/removal requirement, reviewer confirmation requirement, and no-action attestation.

## Required Pre-Execution Checks
Required checks are reviewer approval, source reference, source-status boundary, evidence envelope, audit envelope, rollback/removal policy, sensitive-data review, no-overstatement check, and explicit execution authorisation.

## Required Execution Steps
Required steps are explicit execution authorisation confirmation, first-candidate source-reference lock, source-status boundary verification, evidence record envelope preparation, audit envelope preparation, sensitive-data review confirmation, later-slice single-candidate durable intake, rollback/removal evidence recording, and reviewer closeout.

## Required Post-Execution Checks
Required checks are evidence record verification, corpus mutation verification, rollback/removal evidence, sensitive-data confirmation, and reviewer closeout.

## No Durable Intake Now Boundary
`durable_intake_execution_authorised_now` and `durable_intake_performed` are always false. This slice does not durably ingest evidence.

## No Corpus Mutation Boundary
`corpus_mutation_performed` is always false. Any mutation claim blocks the design.

## No DB Write Boundary
`db_write_performed` is always false. Any DB write, DB read, or DB access claim blocks the design.

## Runtime / Deployment / Production Boundary
Runtime, deployment, production, chat exposure, live retrieval, live LLM, and final answer generation claims are blocked. This slice does not claim runtime readiness, deployment readiness, or production readiness.

## Developer Handoff
Use `build_controlled_durable_intake_first_candidate_execution_design(authorisation_gate_metadata, candidate_eligibility_metadata)` for deterministic local design metadata. A later slice must separately authorise execution before any durable intake occurs.

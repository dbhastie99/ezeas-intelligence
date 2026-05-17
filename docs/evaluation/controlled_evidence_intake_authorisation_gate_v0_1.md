# Controlled Evidence Intake Authorisation Gate v0.1

## Purpose

Define a deterministic local gate that evaluates supplied candidate evidence metadata for eligibility for a future no-mutation intake attempt.

## Scope

The gate is a side-effect-free service and documentation/test artefact only. It does not ingest evidence, mutate corpus, read or write a database, call live retrieval, call a live LLM, generate final natural-language answers, expose routes, or change runtime systems.

## Current Phase

Controlled evidence intake authorisation / first no-mutation candidate selection.

## Current Estimated Progress Before Slice

0% complete.

## Expected Progress After Slice

Approximately 55-65% complete.

## Relationship to Governed Evidence Intake

Governed evidence intake is complete at readiness/runbook level. This gate uses that posture as a prerequisite boundary and does not promote Minerva to ingestion or runtime readiness.

## Relationship to Dry-Run Phase

The controlled evidence intake dry-run phase is complete at controlled-readiness level only. This gate follows the dry-run by authorising candidate eligibility for a later no-mutation attempt, not by performing intake.

## Authorisation Decision Model

The decision model returns one of:

- `AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE`
- `NEEDS_SOURCE_CONTEXT`
- `NEEDS_STATUS_BOUNDARY`
- `NEEDS_TRUST_REVIEW`
- `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`
- `BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM`
- `BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM`
- `BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM`
- `UNKNOWN_REQUIRES_REVIEW`

## Future No-Mutation Intake Boundary

Eligible means suitable for a future no-mutation intake attempt only. `intake_authorised_now` remains false.

## No Evidence Ingestion Boundary

The gate does not ingest evidence. `evidence_ingestion_performed` remains false.

## No Corpus Mutation Boundary

The gate does not mutate corpus. `corpus_mutation_performed` remains false.

## No Code Evidence Ingestion Boundary

The gate blocks Code Evidence ingestion claims and does not ingest Code Evidence.

## DB / Live Retrieval / LLM Boundary

DB writes, DB access/read implications, live retrieval, and live LLM claims are blocked. The service does not connect to or read from a database.

## Final Answer Generation Boundary

Final natural-language answer generation remains deferred and any current final-answer claim is blocked.

## Runtime / Deployment / Production Boundary

Runtime, deployment, and production readiness claims are blocked. This slice is not runtime ready, deployment ready, or production ready.

## No-Action Attestation

The service preserves the no-action attestation: no evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, route registration, runtime integration, deployment, or production action was performed or authorised.

## What This Slice Authorises

This slice authorises deterministic local evaluation of candidate metadata and possible eligibility for a future no-mutation intake attempt.

## What This Slice Does Not Authorise

This slice does not authorise intake now, evidence ingestion, corpus mutation, Code Evidence ingestion, DB reads or writes, migrations, live retrieval, live LLM use, final answers, chat exposure, API routes, workforce-platform integration, analytics integration, UI changes, deployment, production, or runtime readiness.

## Recommended Next Slice

Controlled Evidence Intake Candidate Review Pack / No-Mutation Intake Attempt Readiness v0.1.

## Developer Handoff

Use `build_controlled_evidence_intake_authorisation_gate` for deterministic metadata review only. Treat `AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE` as future no-mutation eligibility, not as current intake authority.

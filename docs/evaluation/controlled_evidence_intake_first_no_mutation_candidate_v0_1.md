# Controlled Evidence Intake First No-Mutation Candidate v0.1

## Purpose

Recommend the safest first future no-mutation intake candidate from supplied candidate metadata.

## Scope

The selector is local, deterministic, and side-effect free. It does not ingest evidence, mutate corpus, ingest Code Evidence, write to a database, call retrieval, call an LLM, expose routes, or change runtime systems.

## Candidate Types

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `ANALYTICS_READINESS_SUMMARY`
- `AWARD_RECOVERY_ANALYSIS`
- `CONTROLLED_EVALUATION_SUMMARY`
- `UNKNOWN_REQUIRES_REVIEW`

## Candidate Ranking Rules

Candidates must first pass the authorisation gate. Eligible controlled summaries rank before less structured materials. The deterministic order is analytics readiness summary, controlled evaluation summary, platform doctrine, hardening log, developer log, and award recovery analysis, with candidate id as the final tie-breaker.

## Recommended First Candidate Criteria

The recommended candidate must have complete source context, status boundary, trust level, candidate type, candidate id, and required caveats. Analytics readiness summary or controlled evaluation summary can be selected when complete.

## Rejected Candidate Rules

Unknown candidates, incomplete candidates, untrusted candidates, and candidates with runtime, production, ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM, or final answer generation claims are rejected or require review.

## Required Caveats

The selection preserves caveats from the authorised candidate and adds that the recommendation is future no-mutation intake only. It also records that no evidence ingestion, corpus mutation, Code Evidence ingestion, or DB write is authorised now.

## Future No-Mutation Boundary

The recommendation is limited to a future no-mutation intake attempt. It is not current intake authorisation.

## No-Action Attestation

The service preserves the no-action attestation and sets current authorisation flags for evidence ingestion, corpus mutation, Code Evidence ingestion, and DB writes to false.

## Developer Handoff

Use `build_controlled_evidence_intake_first_candidate` with explicitly supplied candidate metadata. Treat an output recommendation as planning metadata only; do not wire it to ingestion, corpus mutation, routes, database access, live retrieval, LLM calls, final answers, runtime integration, deployment, or production.

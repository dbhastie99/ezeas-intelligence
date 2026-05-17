# Evidence Intake Planning Gate v0.1

## Purpose

Determine whether evidence metadata is ready for future intake planning, blocked, or requires review.

## Gate Decisions

- `READY_FOR_INTAKE_PLANNING`
- `NEEDS_SOURCE_CONTEXT`
- `NEEDS_STATUS_BOUNDARY`
- `NEEDS_TRUST_REVIEW`
- `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`
- `BLOCKED_UNAUTHORISED_INGESTION_CLAIM`
- `UNKNOWN_REQUIRES_REVIEW`

## Required Prerequisites

The gate requires evidence category, source repo, source phase, source-status boundary, trust level, and required caveats.

## Blocked Claims

Runtime, deployment, production, ingestion, or corpus mutation claims are blocked in this planning-only slice.

## No-Action Rules

The gate always returns `ingestion_authorised_now=False` and `corpus_mutation_authorised_now=False`.

## Future Intake Readiness

`READY_FOR_INTAKE_PLANNING` means the metadata is ready for a later governed intake decision. It does not mean evidence has been ingested or may be ingested now.

## What Must Not Be Inferred

Do not infer corpus mutation, runtime enablement, deployment readiness, production readiness, final answer generation readiness, live retrieval readiness, database access, or cross-repo integration from a ready planning gate.

## Developer Handoff

Call `build_controlled_evidence_intake_planning_gate(metadata)` after taxonomy and source-status boundary metadata are available. Treat blocked decisions as hard stops for this phase.

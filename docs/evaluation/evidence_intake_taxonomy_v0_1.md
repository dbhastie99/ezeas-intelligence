# Evidence Intake Taxonomy v0.1

## Purpose

Classify future evidence candidates into controlled categories before any intake, ingestion, or corpus mutation is authorised.

## Evidence Categories

- `DEVELOPER_LOG`: developer execution or handoff logs.
- `HARDENING_LOG`: controlled hardening records or findings.
- `PLATFORM_DOCTRINE`: governance or doctrine material.
- `THREAD_CONTINUANCE_PROMPT`: prompt or resume context for controlled continuation.
- `ANALYTICS_READINESS_SUMMARY`: analytics readiness summaries.
- `AWARD_RECOVERY_ANALYSIS`: award recovery analysis outputs.
- `WORKFORCE_CONTROLLED_READINESS_DOC`: workforce-platform controlled-readiness documents.
- `CODE_EVIDENCE_PLANNING_OUTPUT`: Code Evidence planning outputs.
- `CONTROLLED_EVALUATION_SUMMARY`: generated controlled evaluation summaries.
- `UNKNOWN_REQUIRES_REVIEW`: unknown, untrusted, or unclassified evidence.

## Trust Levels

Trust levels are metadata labels only. Known controlled categories receive controlled internal trust defaults. Unknown evidence receives `UNKNOWN` and must be reviewed before future planning use.

## Source Repo / Source Phase Model

Evidence metadata should preserve the source repo and source phase. Source context is required before the planning gate can mark evidence ready for future intake planning.

## Category Caveats

Every category carries caveats that prevent overstatement. The caveats state that classification does not authorise ingestion, corpus mutation, runtime, deployment, production, or final-answer behaviour.

## Ingestion Boundary

No taxonomy category authorises ingestion in this slice.

## Corpus Mutation Boundary

No taxonomy category authorises corpus mutation in this slice.

## Runtime / Deployment / Production Boundary

No taxonomy category permits runtime or production claims by default. Deployment claims remain outside the taxonomy and require a separate explicit proof-bearing phase.

## Developer Handoff

Call `build_controlled_evidence_intake_taxonomy(metadata)` with evidence metadata. Use the result for controlled planning only, and route `UNKNOWN_REQUIRES_REVIEW` to source, trust, and status review.

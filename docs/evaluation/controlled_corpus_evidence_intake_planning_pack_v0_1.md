# Controlled Corpus / Evidence Intake Planning Pack v0.1

## Purpose

Define the deterministic planning controls for future Minerva evidence intake before any evidence ingestion is authorised.

## Scope

This pack covers metadata classification, future intake planning gates, and source-status boundaries for controlled evidence candidates. It is local documentation, service logic, and tests only.

## Current Phase

Governed corpus / evidence intake planning.

## Current Estimated Progress Before Slice

0%.

## Expected Progress After Slice

Approximately 55-65% for the governed corpus / evidence intake planning phase.

## Why Governed Evidence Intake Matters

Minerva must keep planned evidence, controlled evidence, runtime truth, deployed truth, and production truth separate. Evidence may exist without being ingested. Planning metadata may be useful without proving implementation. Analysis may identify a risk without proving repair. These controls prevent future intake work from blurring those states.

## Evidence Categories

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `THREAD_CONTINUANCE_PROMPT`
- `ANALYTICS_READINESS_SUMMARY`
- `AWARD_RECOVERY_ANALYSIS`
- `WORKFORCE_CONTROLLED_READINESS_DOC`
- `CODE_EVIDENCE_PLANNING_OUTPUT`
- `CONTROLLED_EVALUATION_SUMMARY`
- `UNKNOWN_REQUIRES_REVIEW`

## Intake Planning Gate

The planning gate returns `READY_FOR_INTAKE_PLANNING` only when evidence category, source repo, source phase, source-status boundary, trust level, and caveats are present. Missing source context, missing status boundary, unknown trust, runtime or production overstatement, and unauthorised ingestion claims produce review or blocked decisions.

## Source-Status Boundary

The source-status boundary model preserves the distinction between evidence existence and implementation or runtime truth. Controlled-readiness, planning, analysis, implementation candidate, runtime, deployment, production, and unknown evidence statuses are evaluated separately.

## No-Action Attestation

No evidence ingestion, corpus mutation, Code Evidence ingestion, database access, live LLM call, final answer generation, endpoint exposure, chat exposure, live retrieval backend change, workforce-platform runtime integration, analytics runtime integration, UI change, deployment action, or production action is authorised by this slice.

## What This Slice Authorises

- Local deterministic evidence metadata classification.
- Local deterministic future intake planning gate evaluation.
- Local deterministic source-status boundary evaluation.
- Focused tests and documentation for controlled planning.

## What This Slice Does Not Authorise

- Evidence ingestion.
- Corpus mutation.
- Code Evidence ingestion.
- Runtime readiness claims.
- Deployment readiness claims.
- Production readiness claims.
- Live LLM use.
- Final natural-language answer generation.
- DB reads, writes, connections, or migrations.
- API routes, endpoints, internal chat exposure, tenant chat exposure, customer chat exposure, or public chat exposure.
- Workforce-platform, ezeas-analytics, live retrieval backend, or UI changes.

## Developer Handoff

Use `build_controlled_evidence_intake_taxonomy()`, `build_controlled_evidence_intake_planning_gate()`, and `build_evidence_source_status_boundary()` for deterministic planning metadata. Treat all output as controlled planning support only.

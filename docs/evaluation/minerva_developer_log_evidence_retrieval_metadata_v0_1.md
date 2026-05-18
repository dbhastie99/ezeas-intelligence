# Minerva Developer Log Evidence Retrieval Metadata v0.1

## Metadata Contract

Developer Log retrieval metadata is created only from a retrieval-ready durable evidence record. The contract includes a stable metadata ID, source record ID, evidence type, retrieval key, retrievable sections, source reference, source status, answer boundaries, prohibited inferences, citation requirement, and claim policies.

The ready status is `DEVELOPER_LOG_RETRIEVAL_METADATA_READY`.

## Developer Log Sections

The standard retrievable Developer Log sections are the required sections from the durable Developer Log candidate service, including objectives, work completed, issues encountered, current status, work log, decisions, still-to-do material, and operating model/rationale.

## Evidence, Source, And Status Boundaries

The metadata distinguishes:

- what the evidence says;
- what the project decided when the Developer Log records a decision;
- implementation status, which remains unknown unless separately evidenced.

Source reference and source status are preserved from the durable record envelope. Citation/source reference is required for controlled synthesis.

## Prohibited Inferences

The metadata prohibits inferring production readiness, runtime deployment, DB mutation, corpus mutation, and implementation completion unless directly evidenced. It does not convert Developer Log evidence into runtime or production claims.

## Developer Handoff

Use `build_developer_log_evidence_retrieval_metadata(record, readiness)` after retrieval readiness is ready. A non-ready readiness result blocks metadata readiness.

# Controlled Durable Intake Authorisation Requirements v0.1

## Purpose

Define deterministic prerequisites for a future durable evidence intake authorisation gate without authorising durable intake now.

## Future Durable Intake Preconditions

Future durable intake requires reviewer confirmation, source-status boundary, evidence envelope, no-overstatement check, rollback policy, audit metadata, and dry-run review. Missing prerequisites produce `MISSING_REQUIRED_PREREQUISITES`.

## Reviewer Confirmation

A named reviewer or approved reviewer process must confirm that the evidence candidate can proceed to a future durable-intake decision gate.

## Source-Status Boundary

The source must have an explicit status boundary, such as controlled-readiness, not-reviewed, reviewed, superseded, or excluded. The boundary must prevent source status from being overstated.

## Evidence Envelope

A reviewable evidence envelope must exist before durable intake. The envelope must identify the source, candidate, summary, caveats, and no-action posture.

## No-Overstatement Check

Future authorisation must confirm that the candidate does not claim current truth, production readiness, runtime readiness, durable ingestion, corpus mutation, DB writes, final answer generation, or exposure beyond the approved boundary.

## Rollback Policy

A rollback or removal policy is required before future durable intake authorisation.

## Audit Metadata

Audit metadata must identify source reference, source status, reviewer, decision timestamp, no-mutation history, rollback policy, prohibited-claims check, and sensitive-data review.

## Dry-Run Review Requirement

Future durable intake requires review of the no-mutation dry-run or equivalent controlled execution history.

## What This Slice Does Not Authorise

This slice does not authorise durable evidence intake, corpus mutation, DB writes, DB reads, DB access, Code Evidence ingestion, live retrieval, live LLM use, final natural-language answer generation, chat exposure, endpoint exposure, route registration, workforce-platform integration, ezeas-analytics integration, UI changes, deployment readiness, runtime readiness, or production readiness.

## Developer Handoff

Use `build_controlled_durable_intake_authorisation_requirements(metadata)` to evaluate future authorisation prerequisites only. The returned flags keep durable intake, corpus mutation, and DB writes unauthorised now.

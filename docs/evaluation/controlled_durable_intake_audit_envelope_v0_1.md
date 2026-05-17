# Controlled Durable Intake Audit Envelope v0.1

## Purpose

Define review and audit metadata required before any future durable evidence intake authorisation.

## Required Audit Fields

Required fields are source reference, source status, reviewer, decision timestamp, no-mutation history, rollback policy, prohibited-claims check, and sensitive-data review.

## Source Reference

The source reference must identify the evidence candidate or review artefact being considered for future durable intake.

## Source Status

The source status must identify the current governance state and prevent unreviewed or controlled-readiness material from being overstated.

## Reviewer

A reviewer or approved review authority must be recorded before future durable intake can be considered.

## Decision Timestamp

A decision timestamp must be present so future authorisation can be audited and sequenced.

## No-Mutation History

The audit envelope must record the no-mutation execution or dry-run history that supports review. This history does not authorise mutation.

## Rollback Policy

The audit envelope must reference the rollback or removal policy required before future durable intake.

## Prohibited Claims Check

The audit envelope must confirm that prohibited durable intake, corpus mutation, DB write, Code Evidence ingestion, runtime, deployment, production, final-answer, route, and chat-exposure claims have been checked.

## Sensitive Data Review

Sensitive-data review is required before future durable intake can be considered.

## No-Action Attestation

This slice creates audit-envelope design metadata only. No durable intake, corpus mutation, DB write, DB read, DB access, Code Evidence ingestion, live retrieval, live LLM use, final answer generation, route registration, chat exposure, runtime integration, deployment, or production action is authorised or performed.

## Developer Handoff

Use `build_controlled_durable_intake_audit_envelope(metadata)` to evaluate required audit metadata only. If metadata claims durable intake, corpus mutation, DB write, or Code Evidence ingestion was already performed, the service blocks with `BLOCKED_DURABLE_INTAKE_ALREADY_PERFORMED_CLAIM`.

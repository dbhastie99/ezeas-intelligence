# Controlled Durable Intake Candidate Eligibility v0.1

## Purpose
Define deterministic candidate eligibility metadata for controlled durable evidence intake authorisation review.

## Scope
This service evaluates local candidate metadata only. It does not perform durable intake, mutate corpus, access databases, call LLMs, or expose runtime surfaces.

## Candidate Types
Supported candidate types are `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `ANALYTICS_READINESS_SUMMARY`, `AWARD_RECOVERY_ANALYSIS`, `CONTROLLED_EVALUATION_SUMMARY`, `CODE_EVIDENCE_PLANNING_OUTPUT`, and `UNKNOWN_REQUIRES_REVIEW`.

## Eligibility Status Model
Statuses include `DURABLE_INTAKE_CANDIDATE_ELIGIBLE_FOR_GATE`, missing prerequisite statuses for source reference, source-status boundary, evidence envelope, audit envelope, reviewer confirmation, rollback policy, sensitive-data review, `BLOCKED_PROHIBITED_CLAIMS`, and `UNKNOWN_REQUIRES_REVIEW`.

## Required Prerequisites
Candidate metadata must include source reference, source-status boundary, evidence envelope, audit envelope, reviewer confirmation, rollback/removal policy, and sensitive-data review.

## Prohibited Claims
Claims of durable intake authorisation now, durable ingestion, corpus mutation, DB write, Code Evidence ingestion, live retrieval, live LLM use, final answer generation, chat exposure, runtime integration, deployment readiness, or production readiness block eligibility.

## Sensitive Data Review
Sensitive-data review must be explicitly present before a candidate is eligible for the authorisation gate.

## Rollback / Removal Policy
A rollback or removal policy must be present so a later execution slice can define how candidate material and derived references would be removed if needed.

## Developer Handoff
Use `build_controlled_durable_intake_candidate_eligibility(candidate_metadata)` before authorisation gate review. Eligibility for the gate is not durable intake authorisation and does not permit ingestion or mutation.

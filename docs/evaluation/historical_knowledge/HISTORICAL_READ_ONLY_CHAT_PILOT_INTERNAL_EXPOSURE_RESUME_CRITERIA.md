# Historical Read-Only Chat Pilot Internal Exposure Resume Criteria

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the criteria required before the deferred Minerva historical read-only chat pilot internal exposure stream may be resumed.

The stream-level future resume criteria are recorded at `HISTORICAL_READ_ONLY_CHAT_PILOT_FUTURE_RESUME_CRITERIA.md` and must also be reviewed before any future exposure candidate.

## Resume Criteria

- explicit exposure approval supplied;
- internal-only scope confirmed;
- operator/developer-only access confirmed;
- access control decision complete;
- audit/logging decision complete;
- candidate service remains current;
- no-production exposure attestation reviewed;
- live LLM remains unapproved unless separate policy gate approves it;
- final answer generation remains unapproved unless separate gate approves it.

## Evidence Required On Resume

- `ExposureDecisionId`
- `CandidateService`
- `ApprovedBy`
- `ApprovedAtUtc`
- `InternalScopeConfirmed`
- `OperatorDeveloperOnlyConfirmed`
- `AccessControlDecision`
- `AuditLoggingDecision`
- `GlobalRouteRegistrationStatus`
- `PublicAccessStatus`
- `TenantCustomerAccessStatus`
- `LiveLLMStatus`
- `FinalAnswerGenerationStatus`
- `Notes`

## Boundary

Satisfying resume criteria authorises only consideration of a future internal exposure candidate. It does not expose chat, create production access, register global routes, call live LLMs, generate final natural-language answers, connect live retrieval, query or mutate corpus, read or write databases, ingest sources, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

These criteria are carried forward into `HISTORICAL_READ_ONLY_CHAT_PILOT_FUTURE_RESUME_CRITERIA.md`.

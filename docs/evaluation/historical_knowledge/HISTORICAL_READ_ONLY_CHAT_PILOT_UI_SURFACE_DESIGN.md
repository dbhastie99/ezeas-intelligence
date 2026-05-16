# Historical Read-Only Chat Pilot UI Surface Design

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines future operator-facing UI display requirements as design only. No UI is created.

## Future UI Display Requirements

The future UI must display:

- response status;
- response mode;
- refusal reason;
- citation readiness;
- caveat requirement;
- no-runtime flags;
- blocked gate status.

## Visibility Rules

The UI must display envelope/status output and must not pretend to be production chat. Refusal reason, citation readiness, caveat requirement, blocked gates, and no-runtime flags must remain visible. The UI must not silently convert historical evidence into current truth.

## Non-Creation Statement

No UI is created. This design does not add frontend components, routes, controllers, API handlers, endpoint code, chat exposure, live LLM calls, final answer generation, live retrieval, DB access, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, production deployment, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

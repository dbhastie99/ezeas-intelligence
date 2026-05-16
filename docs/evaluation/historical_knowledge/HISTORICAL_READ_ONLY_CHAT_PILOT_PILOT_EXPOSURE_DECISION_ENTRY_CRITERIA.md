# Historical Read-Only Chat Pilot Exposure Decision Entry Criteria

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the entry criteria for a future historical read-only chat pilot exposure decision gate.

The current gate is `HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_GATE.md`. Future strictly internal exposure candidate criteria are defined in `HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_ENTRY_CRITERIA.md`.

## Entry Criteria

- minimal endpoint/UI candidate closeout complete
- static review complete
- no-production exposure attestation complete
- access control decision required
- audit/logging decision required
- no live LLM approved
- no final answer generation approved
- no live retrieval backend
- no DB read/write
- no corpus mutation
- explicit exposure decision required
- exposure decision gate complete before internal exposure candidate consideration
- internal exposure entry criteria complete before internal exposure candidate consideration

## Boundary

Meeting these entry criteria authorises only consideration of a future pilot exposure decision gate. It does not approve production chat exposure, public access, tenant/customer access, global route registration, live LLM calls, final natural-language answer generation, live retrieval, corpus/vector search, DB reads, DB writes, schema migrations, corpus mutation, source ingestion, Code Evidence ingestion, or cross-repo changes.

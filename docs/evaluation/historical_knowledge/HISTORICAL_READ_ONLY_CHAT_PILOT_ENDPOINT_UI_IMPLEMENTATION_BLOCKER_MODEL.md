# Historical Read-Only Chat Pilot Endpoint/UI Implementation Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines blocker codes for the endpoint/UI implementation gate and any future minimal endpoint/UI candidate consideration.

## Blocker Codes

- `ENDPOINT_UI_DESIGN_INCOMPLETE`
- `ENDPOINT_CONTRACT_INCOMPLETE`
- `UI_SURFACE_DESIGN_INCOMPLETE`
- `ACCESS_CONTROL_DESIGN_INCOMPLETE`
- `AUDIT_LOGGING_DESIGN_INCOMPLETE`
- `ORCHESTRATOR_CONTRACT_INCOMPLETE`
- `REFUSAL_VISIBILITY_UNRESOLVED`
- `CITATION_VISIBILITY_UNRESOLVED`
- `LIVE_LLM_POLICY_UNRESOLVED`
- `FINAL_ANSWER_POLICY_UNRESOLVED`
- `LIVE_RETRIEVAL_BOUNDARY_UNRESOLVED`
- `DB_BOUNDARY_UNRESOLVED`
- `CORPUS_MUTATION_BOUNDARY_UNRESOLVED`
- `ENDPOINT_REQUIRED_TOO_EARLY`
- `UI_REQUIRED_TOO_EARLY`
- `CHAT_EXPOSURE_RISK`

## Resolution Rule

Blocker resolution does not itself create endpoint/UI or expose chat. Any future endpoint/UI creation must be separately approved and remain internal/read-only/envelope-only unless later expanded by an explicit control slice.

# Historical Read-Only Chat Pilot Endpoint/UI Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This blocker model defines conditions that block a future endpoint/UI design pack or implementation candidate from being considered.

## Blocker Codes

- `ORCHESTRATOR_CLOSEOUT_MISSING`
- `RESPONSE_CONTRACT_INCOMPLETE`
- `GUARDRAILS_INCOMPLETE`
- `ACCESS_CONTROL_UNRESOLVED`
- `AUDIT_LOGGING_UNRESOLVED`
- `REFUSAL_VISIBILITY_UNRESOLVED`
- `CITATION_VISIBILITY_UNRESOLVED`
- `LIVE_LLM_POLICY_UNRESOLVED`
- `FINAL_ANSWER_POLICY_UNRESOLVED`
- `LIVE_RETRIEVAL_BOUNDARY_UNRESOLVED`
- `DB_BOUNDARY_UNRESOLVED`
- `CORPUS_MUTATION_BOUNDARY_UNRESOLVED`
- `ENDPOINT_REQUIRED_TOO_EARLY`
- `UI_REQUIRED_TOO_EARLY`

## Resolution Rule

Blocker resolution does not itself create endpoint/UI or expose chat. Resolving a blocker only permits the next explicitly approved planning decision to be considered.

## Non-Authorisation

This blocker model does not authorise endpoint creation, UI creation, chat exposure, live LLM calls, final answer generation, live retrieval, corpus/vector search, corpus mutation, source ingestion, Code Evidence ingestion, DB reads, DB writes, schema migrations, production deployment, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

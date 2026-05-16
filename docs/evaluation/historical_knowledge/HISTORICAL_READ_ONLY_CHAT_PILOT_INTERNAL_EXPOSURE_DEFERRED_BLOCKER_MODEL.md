# Historical Read-Only Chat Pilot Internal Exposure Deferred Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This model defines blocker codes for the deferred Minerva historical read-only chat pilot internal exposure closeout.

## Blocker Codes

- `EXPLICIT_EXPOSURE_APPROVAL_MISSING`
- `INTERNAL_SCOPE_UNCONFIRMED`
- `OPERATOR_DEVELOPER_ACCESS_UNCONFIRMED`
- `ACCESS_CONTROL_DECISION_MISSING`
- `AUDIT_LOGGING_DECISION_MISSING`
- `CANDIDATE_CURRENCY_UNCONFIRMED`
- `NO_PRODUCTION_ATTESTATION_NOT_REVIEWED`
- `LIVE_LLM_POLICY_UNRESOLVED`
- `FINAL_ANSWER_POLICY_UNRESOLVED`
- `PUBLIC_ACCESS_RISK`
- `TENANT_CUSTOMER_ACCESS_RISK`
- `GLOBAL_ROUTE_REGISTRATION_RISK`
- `DB_BOUNDARY_RISK`
- `CORPUS_MUTATION_RISK`

## Resolution Boundary

Blocker resolution does not itself expose chat or approve production access. Any future internal exposure still requires explicit approval and completed resume criteria. Public, tenant/customer, production chat, live LLM, final answer generation, live retrieval, DB, corpus, source ingestion, Code Evidence, schema migration, and cross-repo changes remain prohibited unless separately gated.

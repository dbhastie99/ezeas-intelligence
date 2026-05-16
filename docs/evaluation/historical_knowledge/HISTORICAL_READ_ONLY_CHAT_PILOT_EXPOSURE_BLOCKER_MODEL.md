# Historical Read-Only Chat Pilot Exposure Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This model defines blocker codes for the Minerva historical read-only chat pilot exposure decision gate.

## Blocker Codes

- `EXPOSURE_DECISION_INCOMPLETE`
- `ACCESS_CONTROL_DECISION_INCOMPLETE`
- `AUDIT_LOGGING_DECISION_INCOMPLETE`
- `NO_PRODUCTION_ATTESTATION_MISSING`
- `PUBLIC_ACCESS_RISK`
- `TENANT_CUSTOMER_ACCESS_RISK`
- `GLOBAL_ROUTE_REGISTRATION_RISK`
- `LIVE_LLM_POLICY_UNRESOLVED`
- `FINAL_ANSWER_POLICY_UNRESOLVED`
- `LIVE_RETRIEVAL_BOUNDARY_UNRESOLVED`
- `DB_BOUNDARY_UNRESOLVED`
- `CORPUS_MUTATION_BOUNDARY_UNRESOLVED`
- `REFUSAL_VISIBILITY_UNRESOLVED`
- `CITATION_VISIBILITY_UNRESOLVED`

## Resolution Boundary

Blocker resolution does not itself expose chat or approve production access. Any future exposure still requires separate explicit approval, and production/public/tenant/customer access remains prohibited unless separately gated.

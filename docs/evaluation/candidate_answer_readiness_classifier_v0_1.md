# Candidate Answer Readiness Classifier v0.1

## 1. Purpose

This slice adds a deterministic Minerva Candidate Answer Readiness Classifier. It evaluates proposed answer/status text or structured candidate output before controlled evaluation or developer handoff use.

## 2. Scope

The scope is a local deterministic service, focused tests, and this documentation. The classifier reads supplied in-memory text only and returns structured classification metadata.

## 3. Current Status

Minerva remains controlled-readiness only. Internal chat exposure, public/production/tenant/customer chat exposure, final natural-language answer generation, live LLM use, live retrieval backend use, DB access, DB writes, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and ezeas-analytics runtime integration remain deferred.

## 4. Why Candidate Answer Classification Is Needed

Candidate Minerva answer/status text can accidentally convert controlled-readiness into runtime, deployment, production, exposure, DB-validation, or final-answer readiness. This classifier blocks or caveats those claims before the text is used in controlled evaluation or developer handoff materials.

## 5. Controlled Evaluation Boundary

Candidate text is safe for controlled evaluation only when it preserves controlled-readiness caveats and avoids prohibited readiness or exposure claims. Controlled evaluation does not mean final answer generation.

## 6. Developer Handoff Boundary

Candidate text can be safe for developer handoff when it preserves controlled-readiness, includes final/current artefact preference language, and contains no prohibited claims. Developer handoff does not authorise exposure, runtime, deployment, production, DB access, or final answer generation.

## 7. Final Answer Generation Boundary

This is not a final answer generation slice. The classifier never marks a candidate safe for final natural-language answer generation and does not generate final user-facing answers.

## 8. Chat / Endpoint Exposure Boundary

This is not a chat exposure slice. It does not enable internal, public, production, tenant, or customer chat exposure. It does not expose endpoints, create API routes, or register routes.

## 9. Runtime Boundary

This is not a runtime retrieval slice. It does not enable live retrieval, live LLM calls, runtime answer synthesis, runtime validation, or runtime integration.

## 10. Deployment Boundary

This is not a deployment-readiness slice. It does not deploy Minerva, create deployment artefacts, register routes, change infrastructure, or authorise deployment.

## 11. Production Boundary

This is not a production-readiness slice. Production-ready, ready-for-production, production-use, or equivalent claims are blocked.

## 12. DB / Validation Boundary

This slice does not connect to, query, read from, validate against, or write to a database. Claims that DB access or DB validation occurred are blocked unless DB validation is explicitly framed as pending or not performed.

## 13. Corpus / Code Evidence Boundary

This slice does not mutate corpus and does not ingest Code Evidence. Claims that corpus mutation or Code Evidence ingestion occurred are blocked.

## 14. Cross-Repo Runtime Boundary

This slice does not change workforce-platform or ezeas-analytics. Claims that workforce-platform runtime integration or analytics runtime integration occurred are blocked.

## 15. Classification Model

The classifier returns structured metadata including:

- `readiness_classification`
- `safe_for_controlled_evaluation`
- `safe_for_developer_handoff`
- `safe_for_final_answer_generation`
- `overstatement_detected`
- `prohibited_claims_detected`
- `required_caveats`
- `missing_caveats`
- `preserved_boundaries`
- `violated_boundaries`
- claim-specific detection booleans
- `explanation`

Classification values include `SAFE_CONTROLLED_EVALUATION_ONLY`, `NEEDS_CAVEAT`, `BLOCKED_OVERSTATED_RUNTIME`, `BLOCKED_OVERSTATED_DEPLOYMENT`, `BLOCKED_OVERSTATED_PRODUCTION`, `BLOCKED_OVERSTATED_EXPOSURE`, `BLOCKED_FINAL_ANSWER_GENERATION_CLAIM`, `BLOCKED_LIVE_LLM_CLAIM`, `BLOCKED_DB_ACCESS_CLAIM`, `BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`, `BLOCKED_CROSS_REPO_RUNTIME_CLAIM`, and `UNKNOWN_REQUIRES_REVIEW`.

## 16. Blocked Claim Categories

Blocked categories are production readiness, deployment readiness, runtime readiness, chat exposure, endpoint exposure, final natural-language answer generation, live LLM use, DB access, DB validation, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and analytics runtime integration.

## 17. Caveat Behaviour

Ambiguous status without controlled-readiness or deferred-boundary caveats requires review. Missing caveats prevent safe handoff. Explicit no-action framing, such as no DB access or DB validation pending/not performed, is treated as boundary-preserving caveat language.

## 18. What This Slice Authorises

This slice authorises only deterministic local classification of supplied candidate answer/status content, focused tests, and documentation for controlled evaluation and developer handoff safety.

## 19. What This Slice Does Not Authorise

This slice does not authorise chat exposure, endpoint exposure, API route registration, final natural-language answer generation, live LLM use, runtime retrieval, DB validation, DB connection, DB queries, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, workforce-platform runtime behaviour, ezeas-analytics runtime behaviour, UI changes, deployment readiness, runtime readiness, or production readiness.

## 20. Recommended Next Slice

The recommended next slice is a controlled evaluation harness integration plan that calls the classifier on stored candidate output fixtures without adding endpoints, live retrieval, live LLM calls, database access, corpus mutation, or final answer generation.

## 21. Developer Handoff

Use `app/services/candidate_answer_readiness_classifier_service.py` for deterministic candidate checks. Call `classify_candidate_answer_readiness(candidate)` with text, a dictionary, or simple structured candidate data. Treat `safe_for_final_answer_generation` as permanently false in this slice and treat blocked classifications as stop conditions for evaluation/handoff use until corrected.

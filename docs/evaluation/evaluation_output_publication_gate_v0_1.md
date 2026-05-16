# Evaluation Output Publication Gate v0.1

## 1. Purpose

This slice adds a deterministic Minerva Evaluation Output Publication Gate. It checks proposed evaluation/status output before that text is used in controlled internal artefacts.

## 2. Scope

The scope is a local deterministic service, focused tests, and this documentation. The gate reads supplied in-memory text or simple structured metadata and returns publication-gating metadata.

## 3. Current Status

Minerva remains controlled-readiness only. Internal chat exposure, public/production/tenant/customer chat exposure, final natural-language answer generation, live LLM use, live retrieval backend use, DB access, DB writes, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and ezeas-analytics runtime integration remain deferred.

## 4. Why Publication Gating Is Needed

Evaluation reports, developer handoff notes, and progress summaries can accidentally overstate Minerva status. The gate prevents controlled-readiness truth from being converted into runtime, deployment, production, exposure, DB-validation, corpus-ingestion, or final-answer readiness.

## 5. Controlled Evaluation Report Boundary

Controlled evaluation reports may describe deterministic evaluation status when controlled-readiness and no-action caveats are preserved. They must not claim runtime readiness, deployment readiness, production readiness, chat exposure, endpoint exposure, DB validation, corpus mutation, Code Evidence ingestion, live LLM use, or final answer generation.

## 6. Developer Handoff Boundary

Developer handoff output may be published only when it preserves controlled-readiness caveats and contains no blocked claims. Developer handoff does not authorise implementation, exposure, runtime integration, deployment, production use, DB access, or final user-facing answer generation.

## 7. Progress Summary Boundary

Progress summaries may be published only when they describe controlled local progress and keep deferred/no-action boundaries visible. A progress summary is not a production status announcement and is not deployment evidence.

## 8. Final Answer Generation Boundary

This is not a final answer generation slice. The gate never marks output safe for final natural-language answer generation and does not generate final user-facing answers.

## 9. Chat / Endpoint Exposure Boundary

This is not a chat exposure slice. It does not enable internal, public, production, tenant, or customer chat exposure. It does not expose endpoints, create API routes, or register routes.

## 10. Runtime Boundary

This is not a runtime retrieval slice. It does not enable live retrieval, live LLM calls, runtime answer synthesis, runtime validation, or runtime integration.

## 11. Deployment Boundary

This is not a deployment-readiness slice. It does not deploy Minerva, create deployment artefacts, register routes, change infrastructure, or authorise deployment.

## 12. Production Boundary

This is not a production-readiness slice. Production-ready, ready-for-production, production-use, or equivalent claims are blocked.

## 13. DB / Validation Boundary

This slice does not connect to or query a database. It does not read from a database, write to a database, create migrations, or perform DB validation. Claims that DB access or DB validation occurred are blocked unless explicitly framed as pending or not performed.

## 14. Corpus / Code Evidence Boundary

This slice does not mutate corpus and does not ingest Code Evidence. Claims that corpus mutation or Code Evidence ingestion occurred are blocked.

## 15. Cross-Repo Runtime Boundary

This slice does not change workforce-platform or ezeas-analytics. Claims that workforce-platform runtime integration or ezeas-analytics runtime integration occurred are blocked.

## 16. Publication Decision Model

The gate returns structured metadata including:

- `publication_decision`
- `safe_for_controlled_evaluation_report`
- `safe_for_developer_handoff`
- `safe_for_progress_summary`
- `safe_for_final_answer_generation`
- `publication_blocked`
- `block_reasons`
- `required_caveats`
- `missing_caveats`
- `preserved_boundaries`
- `violated_boundaries`
- `overstatement_detected`
- `human_review_required`
- claim-specific detection booleans
- `explanation`

Publication decisions are `PUBLISH_CONTROLLED_EVALUATION_REPORT`, `PUBLISH_DEVELOPER_HANDOFF`, `PUBLISH_PROGRESS_SUMMARY`, `NEEDS_CAVEAT_BEFORE_PUBLICATION`, `BLOCKED_OVERSTATED_RUNTIME`, `BLOCKED_OVERSTATED_DEPLOYMENT`, `BLOCKED_OVERSTATED_PRODUCTION`, `BLOCKED_OVERSTATED_EXPOSURE`, `BLOCKED_FINAL_ANSWER_GENERATION_CLAIM`, `BLOCKED_LIVE_LLM_CLAIM`, `BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM`, `BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`, `BLOCKED_CROSS_REPO_RUNTIME_CLAIM`, and `UNKNOWN_REQUIRES_HUMAN_REVIEW`.

## 17. Blocked Claim Categories

Blocked categories are production readiness, deployment readiness, runtime readiness, chat exposure, endpoint exposure, final natural-language answer generation, live LLM use, DB access, DB validation, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and analytics runtime integration.

## 18. Caveat Behaviour

Ambiguous status without controlled-readiness or deferred-boundary caveats requires caveat before publication. Empty or unknown candidate output requires human review. Explicit no-action framing, such as no DB access or DB validation pending/not performed, is treated as boundary-preserving caveat language.

## 19. What This Slice Authorises

This slice authorises only deterministic local gating of supplied candidate evaluation/status content, focused tests, and documentation for controlled internal publication artefacts.

## 20. What This Slice Does Not Authorise

This slice does not authorise chat exposure, endpoint exposure, API route registration, final natural-language answer generation, live LLM use, runtime retrieval, DB validation, DB connection, DB queries, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, workforce-platform runtime behaviour, ezeas-analytics runtime behaviour, UI changes, deployment readiness, runtime readiness, or production readiness.

## 21. Recommended Next Slice

The recommended next slice is a controlled fixture integration plan that applies the publication gate to stored evaluation report, developer handoff, and progress-summary fixtures without adding endpoints, live retrieval, live LLM calls, database access, corpus mutation, or final answer generation.

## 22. Developer Handoff

Use `app/services/evaluation_output_publication_gate_service.py` for deterministic publication checks. Call `evaluate_evaluation_output_publication_gate(candidate)` with text, a dictionary, or simple structured candidate data. Treat `safe_for_final_answer_generation` as permanently false in this slice and treat blocked decisions as stop conditions for controlled publication until corrected.

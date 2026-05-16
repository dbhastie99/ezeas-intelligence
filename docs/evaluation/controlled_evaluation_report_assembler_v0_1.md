# Minerva Controlled Evaluation Report Assembler v0.1

## 1. Purpose

This slice adds a deterministic controlled-report assembler for Minerva internal evaluation metadata. It assembles supplied controlled evidence/status inputs into structured report fields for internal evaluation artefacts only.

## 2. Scope

The assembler is local deterministic service/test/docs only. It accepts supplied metadata and returns structured report metadata. It does not scan the repository or read files unless a caller has already supplied content as input.

## 3. Current Status

Minerva remains controlled-readiness only. Internal chat exposure remains deferred. Public, production, tenant, and customer chat exposure remain deferred. Final natural-language answer generation, live LLM use, live retrieval backend use, DB access, DB writes, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and ezeas-analytics runtime integration remain deferred.

## 4. Why Controlled Report Assembly Is Needed

Prior slices classify and gate unsafe status/output claims. This slice adds a deterministic way to assemble safe internal report metadata while preserving those controls and preventing readiness overstatement.

## 5. Relationship to Status Guard

The assembler preserves controlled-readiness and no-action boundaries that the status guard protects. It does not replace final/current evidence preference rules.

## 6. Relationship to Candidate Answer Classifier

The assembler follows the same controlled-readiness posture as the candidate answer classifier. It must not convert controlled metadata into a final natural-language answer.

## 7. Relationship to Publication Gate

The assembler uses the evaluation output publication gate to determine whether assembled metadata is safe for controlled evaluation reports, developer handoff, or progress summaries. Blocked publication decisions remain blocked.

## 8. Controlled Evaluation Report Boundary

Controlled evaluation reports are internal artefacts only. They can summarize supplied controlled metadata, caveats, no-action attestations, risks, and next-slice recommendations.

## 9. Developer Handoff Boundary

Developer handoff output is internal implementation context only. It does not approve runtime exposure, deployment, production use, DB validation, corpus mutation, or final answer generation.

## 10. Progress Summary Boundary

Progress summaries can report deterministic slice status with caveats. They are not readiness claims for production, deployment, runtime, chat, endpoints, or customer use.

## 11. Next-Slice Recommendation Boundary

Next-slice recommendations identify controlled follow-up work. They do not authorise the recommended work and do not perform it.

## 12. Final Answer Generation Boundary

This is not a final answer generation slice. The assembler never marks output safe for final natural-language answer generation.

## 13. Chat / Endpoint Exposure Boundary

This is not a chat exposure slice. It does not enable internal chat exposure, public chat exposure, tenant chat exposure, customer chat exposure, API endpoints, or route registration.

## 14. Runtime Boundary

This is not a runtime retrieval slice. It does not enable runtime retrieval, live runtime orchestration, answer synthesis runtime, or runtime Minerva chat.

## 15. Deployment Boundary

This is not a deployment-readiness slice. It does not deploy Minerva and does not claim deployment readiness.

## 16. Production Boundary

This is not a production-readiness slice. It does not claim production readiness or customer readiness.

## 17. DB / Validation Boundary

This is not a DB validation slice. It does not connect to a database, query a database, read from a database, write to a database, create migrations, or validate runtime data against a database.

## 18. Corpus / Code Evidence Boundary

This slice does not mutate corpus records and does not ingest Code Evidence. Code Evidence remains outside answer generation and controlled report assembly.

## 19. Cross-Repo Runtime Boundary

This slice does not integrate workforce-platform runtime behaviour or ezeas-analytics runtime behaviour.

## 20. Report Section Model

The assembler returns structured fields for `report_title`, `report_type`, safety flags, `publication_decision`, `sections`, caveats, preserved and violated boundaries, blocked or deferred capabilities, `no_action_attestation`, `recommended_next_slice`, `risks_and_unknowns`, and `explanation`.

The `sections` object includes `report_scope`, `current_status`, `evidence_inputs`, `preferred_current_state_evidence`, `controlled_readiness_summary`, `publication_decision`, `required_caveats`, `preserved_boundaries`, `blocked_or_deferred_capabilities`, `no_action_attestation`, `risks_and_unknowns`, `recommended_next_slice`, `developer_handoff`, `safe_for_controlled_evaluation_report`, `safe_for_final_answer_generation`, and `explanation`.

## 21. Blocked Claim Categories

The assembler blocks safe report output when supplied metadata positively claims production readiness, deployment readiness, deployed state, runtime enablement, chat exposure, endpoint exposure, final natural-language answer generation, live LLM use, DB access, DB validation, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, or ezeas-analytics runtime integration.

## 22. Caveat Behaviour

Ambiguous metadata without controlled-readiness and no-action/deferred caveats requires review or missing-caveat output. Explicit pending or not-performed DB validation phrasing is preserved as a deferred boundary rather than treated as completed DB validation.

## 23. What This Slice Authorises

This slice authorises local deterministic assembly of supplied controlled metadata into internal controlled evaluation reports, developer handoff reports, progress summaries, and next-slice recommendation structures.

## 24. What This Slice Does Not Authorise

This slice does not authorise chat exposure, endpoint exposure, live LLM use, runtime retrieval, final natural-language answer generation, DB access, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, ezeas-analytics runtime integration, UI changes, deployment readiness, production readiness, or runtime readiness.

## 25. Recommended Next Slice

The recommended next slice is a controlled fixture catalog or schema contract for report inputs, still local and deterministic, before any runtime or chat-facing work is considered.

## 26. Developer Handoff

Use `app/services/controlled_evaluation_report_assembler_service.py` for deterministic report metadata assembly. Keep callers responsible for supplying controlled metadata. Do not add routes, DB connections, retrieval calls, live LLM calls, corpus writes, Code Evidence ingestion, UI exposure, workforce-platform runtime integration, or analytics runtime integration.

# Codex Prompt - Minerva Controlled Evaluation Report Assembler v0.1

## Slice

Minerva Controlled Evaluation Report Assembler v0.1.

## Context

This slice follows the Minerva Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1, the Minerva Candidate Answer Readiness Classifier v0.1, and the Minerva Evaluation Output Publication Gate v0.1.

Minerva remains controlled-readiness only. Internal chat exposure, public/production/tenant/customer chat exposure, final natural-language answer generation, live LLM use, live retrieval backend use, DB access, DB writes, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and analytics runtime integration remain deferred.

## Objective

Create a local deterministic controlled evaluation report assembler that accepts supplied controlled evidence/status metadata and returns structured internal report metadata.

The assembler must not generate final user-facing natural-language answers. It must produce structured controlled-report sections suitable only for internal evaluation artefacts, developer handoff notes, progress summaries, and next-slice recommendations.

## Required Implementation

Create or update a focused deterministic service:

- `app/services/controlled_evaluation_report_assembler_service.py`

The service must expose deterministic functions/classes that accept controlled metadata inputs and return structured report metadata.

The service must not scan the repo, read files, connect to a database, call an LLM, mutate corpus, register routes, expose endpoints, or change runtime behaviour.

The structured output must include fields equivalent to:

- `report_title`
- `report_type`
- `safe_for_controlled_evaluation_report`
- `safe_for_developer_handoff`
- `safe_for_progress_summary`
- `safe_for_final_answer_generation`
- `publication_decision`
- `sections`
- `required_caveats`
- `missing_caveats`
- `preserved_boundaries`
- `violated_boundaries`
- `blocked_or_deferred_capabilities`
- `no_action_attestation`
- `recommended_next_slice`
- `risks_and_unknowns`
- `explanation`

Suggested report types:

- `CONTROLLED_EVALUATION_REPORT`
- `DEVELOPER_HANDOFF`
- `PROGRESS_SUMMARY`
- `NEXT_SLICE_RECOMMENDATION`
- `UNKNOWN_REQUIRES_REVIEW`

## Required Behaviours

1. Controlled-readiness metadata with no-action boundaries can assemble a controlled evaluation report.
2. Developer handoff metadata with caveats can assemble a developer handoff report.
3. Progress summary metadata with caveats can assemble a progress summary.
4. Next-slice recommendation metadata can assemble a next-slice recommendation report.
5. Ambiguous metadata without caveats must require review or missing caveat output.
6. Production-ready claim must block safe controlled report output.
7. Deployment-ready/deployed claim must block safe controlled report output unless explicitly framed as not deployed.
8. Runtime-enabled claim must block safe controlled report output unless explicitly framed as runtime deferred.
9. Chat exposure enabled claim must block safe controlled report output.
10. Endpoint exposure enabled claim must block safe controlled report output.
11. Final natural-language answer generation enabled claim must block safe controlled report output.
12. Live LLM enabled claim must block safe controlled report output.
13. DB access/DB validation claim must block unless explicitly framed as not performed or pending.
14. Corpus mutation claim must block.
15. Code Evidence ingestion claim must block.
16. Workforce-platform runtime integration claim must block.
17. Analytics runtime integration claim must block.
18. Assembler must never mark output safe for final answer generation.
19. Assembler output must be deterministic for repeated inputs.
20. Assembler must preserve explicit no-action/deferred boundaries in report sections.

## Documentation

Create:

- `docs/evaluation/controlled_evaluation_report_assembler_v0_1.md`

The document must include the required controlled boundaries and clearly state that this is not a chat, endpoint, live LLM, runtime retrieval, DB validation, production-readiness, corpus mutation, Code Evidence ingestion, workforce-platform, analytics, or UI slice.

## Tests

Create:

- `tests/test_controlled_evaluation_report_assembler_service.py`

Cover the 20 required behaviours above.

## Verification

Use Windows PowerShell syntax only:

- `python -m pytest tests\test_controlled_evaluation_report_assembler_service.py`
- `python -m py_compile app\services\controlled_evaluation_report_assembler_service.py`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `git status --short`

## No-Action Boundaries

Do not enable chat exposure, add routes, call a live LLM, generate final answers, connect to or query a database, write to a database, create migrations, mutate corpus, ingest Code Evidence, alter live retrieval backend behaviour, add credentials, change workforce-platform, change ezeas-analytics, change UI, or claim production/deployment/runtime readiness.

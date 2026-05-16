# Historical Runtime Implementation Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines blocker codes for the Minerva historical runtime implementation test matrix.

Blockers prevent movement toward a future read-only retrieval skeleton candidate until remediated.

## Blocker Codes

| BlockerCode | Meaning |
| --- | --- |
| `TEST_MATRIX_INCOMPLETE` | Required matrix sections, columns, fixtures, outcomes, or boundary assertions are missing. |
| `CURRENT_TRUTH_SCENARIOS_MISSING` | Current-truth allowed/refusal scenarios are incomplete. |
| `HISTORICAL_CONTEXT_SCENARIOS_MISSING` | Historical-context scenarios, historical labels, or current-truth refusal cases are incomplete. |
| `CAVEATED_SCENARIOS_MISSING` | Caveated answer and missing-caveat refusal scenarios are incomplete. |
| `REFUSAL_SCENARIOS_MISSING` | Required refusal scenarios are incomplete. |
| `CITATION_SCENARIOS_MISSING` | Citation/provenance scenarios or missing-provenance behaviours are incomplete. |
| `AUDIT_SCENARIOS_MISSING` | Future audit/logging fields are incomplete. |
| `CONFLICT_SUPERSESSION_SCENARIOS_MISSING` | Conflict and supersession refusal scenarios are incomplete. |
| `RUNTIME_BOUNDARY_UNCLEAR` | The matrix does not clearly preserve that no runtime retrieval, answer synthesis, citation rendering, or chat exists. |
| `LIVE_LLM_BOUNDARY_UNCLEAR` | The matrix does not clearly prohibit live LLM use. |
| `ENDPOINT_UI_BOUNDARY_UNCLEAR` | The matrix does not clearly prohibit endpoint/UI creation or exposure. |
| `CORPUS_MUTATION_BOUNDARY_UNCLEAR` | The matrix does not clearly prohibit corpus mutation, source ingestion, Code Evidence ingestion, and database writes. |

## Blocker Resolution Boundary

Blocker resolution does not itself implement runtime retrieval, answer synthesis, citation rendering, live LLM, endpoint/UI, chat exposure, or answerability.

Resolving a blocker permits reassessment of the test matrix only. It does not activate answer-use permission, retrieval eligibility, answer mode, current-truth promotion, source ingestion, corpus mutation, Code Evidence ingestion, database writes, endpoint/UI, live LLM calls, or chat exposure.

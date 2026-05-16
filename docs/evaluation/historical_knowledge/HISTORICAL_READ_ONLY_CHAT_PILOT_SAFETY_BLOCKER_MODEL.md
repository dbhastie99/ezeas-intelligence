# Historical Read-Only Chat Pilot Safety Blocker Model

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines blockers for the Minerva historical read-only chat pilot safety test pack.

## Blocker Codes

- `SAFETY_SCENARIOS_INCOMPLETE`: required safety scenarios are missing or incomplete.
- `CURRENT_TRUTH_SCENARIO_UNTESTED`: current-truth eligible metadata flow is not documented and tested.
- `HISTORICAL_CONTEXT_SCENARIO_UNTESTED`: historical-context preservation is not documented and tested.
- `CAVEATED_SCENARIO_UNTESTED`: caveat preservation is not documented and tested.
- `REFUSAL_SCENARIO_UNTESTED`: one or more refusal scenarios are not documented and tested.
- `CITATION_PROVENANCE_SCENARIO_UNTESTED`: citation/provenance preservation is not documented and tested.
- `RUNTIME_BOUNDARY_UNTESTED`: no-runtime assertions are not documented and tested.
- `LIVE_LLM_BOUNDARY_UNCLEAR`: live LLM prohibition is ambiguous or untested.
- `CHAT_EXPOSURE_BOUNDARY_UNCLEAR`: chat exposure prohibition is ambiguous or untested.
- `DB_BOUNDARY_UNCLEAR`: database read/write prohibition is ambiguous or untested.
- `CORPUS_MUTATION_BOUNDARY_UNCLEAR`: corpus mutation prohibition is ambiguous or untested.
- `PRIOR_REFUSAL_NOT_PRESERVED`: upstream refusal can be lost, weakened, or converted downstream.

## Resolution Boundary

Blocker resolution does not itself expose chat or implement runtime behaviour. Resolution permits reassessment of the safety test pack only. It does not approve live LLM use, endpoint/UI, live retrieval, database access, corpus mutation, source ingestion, Code Evidence ingestion, current-truth promotion, runtime answer-use activation, runtime retrieval activation, final answer generation, or chat exposure.

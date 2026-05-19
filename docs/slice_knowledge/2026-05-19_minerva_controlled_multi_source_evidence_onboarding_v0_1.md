# Slice Knowledge Record — Minerva Controlled Multi-Source Evidence Onboarding v0.1

## Purpose

This slice moves Minerva from Developer Log-only controlled retrieval to multi-source controlled retrieval across Developer Log, Hardening Log, and Platform Doctrine fixtures. It proves deterministic source-aware retrieval without final answer generation, chat exposure, live LLM calls, DB access, live corpus mutation, Code Evidence ingestion, or runtime integration.

## Product Objective

Give Minerva a controlled local retrieval foundation that can distinguish work-completion evidence, hardening/prohibition evidence, and platform doctrine while preserving authority, source/status boundaries, caveats, current-truth limits, and non-action flags.

## User Story

As a Minerva operator, I need deterministic multi-source fixture retrieval so I can inspect relevant controlled evidence and source boundaries before authorising any answer preparation, exposure, runtime integration, or live retrieval path.

## Source Truth

Source truth is controlled local fixture evidence only. It is not live DB state, live corpus state, uploaded external documents, chat history, or runtime evidence.

## Current Platform Context

The previous Developer Log durable evidence path and controlled retrieval harness reached controlled-readiness level. That slice proved deterministic retrieval before adding more evidence types. This slice follows that instruction by onboarding the next controlled evidence types, Hardening Log and Platform Doctrine, into a controlled local multi-source retrieval envelope.

## Why This Slice Exists Now

Developer Log alone is insufficient because Minerva must distinguish work completed, hardening/prohibited behaviours, and platform doctrine. Source authority and query relevance must both be explicit before any later answer-preparation or exposure work.

## What This Slice Implements

- A controlled multi-source retrieval service over local fixtures.
- Source-aware deterministic keyword/metadata matching.
- Source authority policy for Platform Doctrine, Hardening Log, and Developer Log.
- Result-level evidence type, source status, implementation status, current-truth status, answer-use status, can-prove/cannot-prove statements, and required caveats.
- Envelope-level evidence universe, searched/out-of-scope evidence types, boundary flags, unsupported evidence type handling, and next safe step.
- Focused tests for positive retrieval, authority behaviour, source/status preservation, boundary flags, no overclaiming, unsupported source handling, and deterministic ordering.

## What This Slice Explicitly Does Not Implement

This slice does not call a live LLM, generate final user-facing natural-language answers, expose or register a chat endpoint, add UI, connect to a DB, read from a DB, write to a DB, mutate live corpus, ingest Code Evidence, ingest live documents, materially change retrieval backend, integrate with Workforce Platform, integrate with Analytics runtime, claim runtime readiness, claim production readiness, add broad source ingestion framework, add embeddings, or add vector DB search.

## Affected Tables / Models

None. No DB, schema, or migration changes.

## Affected Services

- `app/services/controlled_multi_source_evidence_retrieval_service.py`

The previous Developer Log-only service remains intact for regression compatibility.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_controlled_multi_source_evidence_retrieval.py`
- Existing regression coverage remains relevant for `tests/test_controlled_durable_evidence_retrieval_harness.py` and Developer Log durable evidence path tests.

## Evidence / Story Requirements

- QueryUnderstanding: normalize query terms deterministically and classify simple source intent.
- EvidenceUniverse: search only controlled local fixtures for Developer Log, Hardening Log, and Platform Doctrine.
- AuthorityPolicy: combine matched terms, deterministic query intent, source authority, source/status boundary, and answer-use safety; do not treat authority as identical to relevance.
- Matches: return matched fixture records with matched terms, match reasons, rank, score, and provenance metadata.
- SourceStatusBoundary: preserve source status, implementation status, current-truth status, answer-use status, caveats, can-prove and cannot-prove limits.
- BoundaryResult: keep all live/runtime/mutation/exposure flags false.
- NextStep: review the structured retrieval envelope before any later controlled answer-preparation slice.

## Irreversible Actions Prohibited

No corpus mutation, no durable ingestion, no Code Evidence ingestion, no DB writes, no schema changes, no runtime exposure, no endpoint registration, no live LLM call, and no cross-repo runtime integration.

## Payroll / Compliance Consequences

None directly. This is Minerva controlled evidence retrieval only and does not affect payroll runtime.

## Security / Role / Tenant Consequences

No live data, no tenant data, no DB access, and no RBAC integration occur in this slice. Future live retrieval will require RBAC-before-retrieval.

## Analytics Consequences

None directly.

## Minerva Consequences

This becomes the first source-aware multi-source retrieval foundation and predecessor to multi-source controlled answer preparation.

## Platform Doctrine Implications

- Source/Status Boundary Preservation Doctrine
- Retrieval Before Exposure Doctrine
- Prompt Is Not Knowledge Doctrine
- Slice Knowledge Preservation Doctrine
- Controlled Evidence Source Authority Doctrine
- Historical Evidence Is Not Current Truth Doctrine
- No Live Minerva Runtime Until Explicitly Authorised

## Hardening Implications

- Do not let retrieval imply final answer generation.
- Do not let Developer Log imply production/runtime truth.
- Do not let Platform Doctrine imply execution proof.
- Do not let Hardening Log imply implementation proof.
- Do not add live ingestion, live DB, live LLM, or chat exposure.

## Likely Gotchas

Source authority versus query relevance is the main gotcha. Platform Doctrine has the highest source authority, but a Developer Log completion query should still rank Developer Log first. Likewise, Hardening Log should rank highly for prohibited-action or remaining-risk questions because relevance and safety boundaries matter.

## Acceptance Criteria

- Platform Doctrine query returns Platform Doctrine fixture and ranks it highly.
- Hardening Log query returns Hardening Log fixture and ranks it highly.
- Developer Log durable evidence path query still returns Developer Log fixture and ranks it highly.
- Every result preserves evidence type, source status, authority level, implementation status, current-truth status, answer-use status, can-prove/cannot-prove statements, and required caveats.
- Every retrieval envelope keeps live LLM, final answer generation, chat exposure, DB read/write, corpus mutation, Code Evidence ingestion, runtime integration, and production readiness flags false.
- Retrieval never converts controlled-readiness into production readiness, historical evidence into current truth, Developer Log evidence into runtime implementation, doctrine into execution proof, or hardening prohibition into implementation proof.
- Unsupported source queries return unsupported/out-of-scope or no-result status without inventing results.
- Repeated identical queries return the same ordered result identifiers.
- Existing Developer Log-only harness tests continue to pass.

## Verification Commands

- `py -m py_compile app/services/controlled_multi_source_evidence_retrieval_service.py`
- `py -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `py -m pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- `py -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`

## Post-Implementation Review Notes

Placeholder for after Codex execution.

## Follow-Up Slices

- Controlled answer preparation over multi-source retrieval results
- Thread Continuance Prompt evidence fixture onboarding
- Analytics Readiness Summary evidence fixture onboarding
- Controlled citation/provenance packet over multi-source evidence
- Later internal read-only answer surface, still no live LLM unless explicitly approved

## Current Status

Initial multi-source controlled fixture retrieval slice.

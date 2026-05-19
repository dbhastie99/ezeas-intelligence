# Slice Knowledge Record - Minerva Controlled Citation / Provenance Packet Over Multi-Source Answer Preparation v0.1

## Purpose

This slice maps prepared Minerva claims to source-aware provenance and citation requirements without generating final answers. It consumes controlled answer-preparation output and records which evidence authority can support each claim, which caveats apply, which claims are unsupported or prohibited, and what additional evidence would be required before any future final-answer gate could consider the claim.

## Product Objective

Give Minerva a deterministic claim-level provenance layer between controlled answer preparation and any later answer rehearsal, while preserving no-action boundaries and preventing fixture-backed claims from becoming runtime, DB, deployment, or production claims.

## User Story

As a Minerva operator, I need a provenance packet that explains why each prepared claim can or cannot be cited, so later answer rehearsal can rely on correct source authority instead of treating retrieval rank or preparation text as proof.

## Source Truth

Source truth is controlled multi-source answer-preparation output and local controlled evidence fixtures/docs only. No live DB state, live runtime state, production deployment evidence, external document ingestion, live corpus state, or live chat history is read or created.

## Current Platform Context

Completed local Minerva sequence:

- Controlled Retrieval Harness.
- Controlled Multi-Source Evidence Retrieval.
- Controlled Multi-Source Answer Preparation.
- Payroll Correction Workflow Reasoning Capture.

These slices established deterministic local fixture retrieval, source/status boundaries, answer-preparation caveats, and curated payroll operator reasoning without enabling runtime Minerva behaviour.

## Why This Slice Exists Now

Before final answer rehearsal, Minerva needs claim-level provenance and citation requirements. Answer preparation can identify likely claims and caveats, but it should not decide that the top retrieval result is valid authority for every claim type. This slice adds the missing source-authority check.

## What This Slice Implements

- Deterministic controlled citation/provenance packet service.
- Claim normalization across supported, unsupported, prohibited, and additional-evidence-required preparation claims.
- Source authority mapping for doctrine, hardening boundary, implementation status, test evidence, payroll operator scenario reasoning, runtime state, DB state, deployment state, production readiness, and unknown claims.
- Evidence inventory built from answer-preparation evidence plus the local payroll correction workflow reasoning artefact when present.
- Citation requirements for each claim type.
- Caveat requirements for future answer gates.
- Unsupported and prohibited claim lists.
- Additional evidence requirements for runtime, DB, deployment, production, Code Evidence, and unclassified claims.
- Final-answer eligibility locked to `PREPARATION_ONLY`.
- Boundary flags showing no live LLM, no final answer, no chat exposure, no DB read/write, no corpus mutation, no Code Evidence ingestion, no runtime integration, and no production-readiness claim.

## What This Slice Explicitly Does Not Implement

This slice does not call a live LLM, generate final user-facing natural-language answers, expose or register a chat endpoint, add UI, connect to a DB, read from a DB, write to a DB, mutate live corpus, ingest Code Evidence, ingest live documents, materially change retrieval backend, integrate with Workforce Platform runtime, integrate with Analytics runtime, claim runtime readiness, claim production readiness, add embeddings, use vector DB search, or make external calls.

## Affected Tables / Models

None. No DB/schema changes.

## Affected Services

- `app/services/controlled_citation_provenance_packet_service.py`

Existing retrieval and answer-preparation services remain unchanged.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_controlled_citation_provenance_packet.py`

Regression coverage remains relevant for:

- `tests/test_controlled_multi_source_answer_preparation.py`
- `tests/test_controlled_multi_source_evidence_retrieval.py`
- `tests/test_controlled_durable_evidence_retrieval_harness.py`
- `tests/test_payroll_correction_workflow_reasoning_capture.py`
- Developer Log durable filter tests.

## Evidence / Story Requirements

- Claim inventory: every prepared claim is represented with claim id, claim text, type, status, evidence required, evidence used, missing evidence, source authority, caveat requirement, citation requirement, and final-answer eligibility.
- Source authority: doctrine requires Platform Doctrine; hardening boundaries require Hardening Log and/or Platform Doctrine; implementation status requires Developer Log or implementation evidence; payroll operator reasoning requires the payroll correction workflow reasoning artefact; runtime, DB, deployment, and production claims require their own evidence classes.
- Citation requirements: every supported or supported-with-caveat claim records the evidence authority a future answer must cite.
- Unsupported/prohibited claims: DB/current state and production-readiness overclaims remain blocked or evidence-insufficient.
- Boundary flags: every packet preserves no-action flags.
- Next step: use the packet only for later controlled answer rehearsal or final-answer gating.

## Irreversible Actions Prohibited

No corpus mutation, durable ingestion, Code Evidence ingestion, DB writes, schema changes, runtime exposure, endpoint registration, live LLM call, deployment action, production readiness assertion, or cross-repo runtime integration is allowed by this slice.

## Payroll / Compliance Consequences

None directly. This is Minerva provenance preparation only.

## Security / Role / Tenant Consequences

No live data, no tenant data, no DB access, and no RBAC integration occur in this slice. Future live use requires RBAC-before-retrieval and answer-use gates.

## Analytics Consequences

None directly.

## Minerva Consequences

This becomes the bridge from answer preparation to controlled answer rehearsal/final answer gating. It lets future Minerva answers such as "Why is this retro and not an adjustment into the current pay?" cite payroll reasoning evidence without claiming Workforce runtime implementation or production readiness.

## Platform Doctrine Implications

- Source/Status Boundary Preservation Doctrine.
- Retrieval Before Exposure Doctrine.
- Answer Preparation Is Not Final Answer Doctrine.
- Citation/Provenance Before Final Answer Doctrine.
- Prompt Is Not Knowledge Doctrine.
- Slice Knowledge Preservation Doctrine.
- Historical Evidence Is Not Current Truth Doctrine.
- No Live Minerva Runtime Until Explicitly Authorised.

## Hardening Implications

- Do not let supported claims become final answers automatically.
- Do not allow doctrine to prove implementation.
- Do not allow Developer Logs to prove production deployment.
- Require DB/runtime/deployment evidence for those claim types.
- Treat payroll workflow reasoning as curated scenario reasoning, not live Workforce proof.

## Likely Gotchas

- Top retrieval result is not automatically the correct claim provenance.
- Source authority depends on claim type.
- Citation requirement is not the same as final answer generation.
- Production readiness claims require production evidence.
- A supported claim can still require caveats and still be ineligible for final answer generation in this slice.

## Acceptance Criteria

- Provenance packet can be built from controlled answer-preparation output.
- Doctrine claims require Platform Doctrine evidence.
- Hardening/prohibition claims require Hardening Log and/or Platform Doctrine evidence.
- Implementation claims require Developer Log or implementation evidence.
- Payroll operator scenario claims require the payroll correction workflow reasoning artefact.
- Current live DB claims require DB evidence and are not supported by controlled fixture evidence alone.
- Production readiness overclaims are prohibited or unsupported without production evidence.
- Every supported or supported-with-caveat claim includes a citation/provenance requirement.
- Every packet preserves no-action boundary flags and final-answer eligibility remains false / `PREPARATION_ONLY`.

## Verification Commands

- `python -m py_compile app/services/controlled_citation_provenance_packet_service.py`
- `python -m pytest tests/test_controlled_citation_provenance_packet.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_citation_provenance_packet_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_citation_provenance_packet_v0_1.md`

## Post-Implementation Review Notes

Placeholder.

## Follow-Up Slices

- Controlled answer rehearsal over provenance packets.
- Controlled final answer gating.
- Internal read-only answer surface, still no live LLM unless explicitly approved.
- Runtime/object story evidence integration later.

## Current Status

Initial controlled citation/provenance packet slice.

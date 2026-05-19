# Minerva Controlled Citation / Provenance Packet Over Multi-Source Answer Preparation v0.1

Implement a deterministic controlled citation/provenance packet over controlled multi-source answer-preparation output.

This slice consumes prepared claim/evidence envelopes and produces structured claim-level provenance. It explains which claims are supported, what evidence supports each claim, what source authority applies, what caveats are required, what claims remain unsupported or prohibited, what additional evidence is required before a final answer could make certain claims, and why final answer generation remains out of scope.

This is not final answer generation, chat exposure, live LLM use, DB-backed retrieval, corpus mutation, Code Evidence ingestion, runtime integration, Analytics integration, Workforce runtime integration, embeddings, vector DB work, deployment, or production-readiness proof.

## Objective

Create a controlled citation/provenance service that accepts query text, a controlled answer-preparation envelope, optional provenance mode, and optional required claim-type filter, then returns a `CitationProvenancePacket`.

The packet must include query text, provenance mode, packet status, claims, evidence inventory, source authority summary, citation requirements, caveat requirements, unsupported claims, prohibited claims, claims requiring additional evidence, final answer eligibility, boundary flags, and next step.

Packet status values include:

- `PROVENANCE_READY`
- `PROVENANCE_READY_WITH_CAVEATS`
- `INSUFFICIENT_EVIDENCE`
- `BLOCKED_PROHIBITED_CLAIMS`
- `OUT_OF_SCOPE`

Claim type values include:

- `DOCTRINE`
- `HARDENING_BOUNDARY`
- `IMPLEMENTATION_STATUS`
- `TEST_EVIDENCE`
- `OPERATOR_SCENARIO_REASONING`
- `RUNTIME_STATE`
- `DB_STATE`
- `DEPLOYMENT_STATE`
- `PRODUCTION_READINESS`
- `UNKNOWN`

Claim status values include:

- `SUPPORTED`
- `SUPPORTED_WITH_CAVEAT`
- `UNSUPPORTED`
- `PROHIBITED`
- `REQUIRES_CURRENT_RUNTIME_EVIDENCE`
- `REQUIRES_CODE_EVIDENCE`
- `REQUIRES_DB_EVIDENCE`
- `REQUIRES_DEPLOYMENT_EVIDENCE`
- `REQUIRES_PRODUCTION_EVIDENCE`

## Source Authority Rules

- Doctrine claims require Platform Doctrine evidence.
- Hardening/prohibition claims require Hardening Log and/or Platform Doctrine evidence.
- Implementation/work-completed claims require Developer Log or implementation evidence.
- Test evidence claims require Developer Log, test output, or slice knowledge evidence.
- Payroll operator scenario/treatment reasoning claims require payroll correction workflow reasoning evidence and/or Platform Doctrine evidence.
- Runtime state claims require runtime evidence.
- DB state claims require DB evidence.
- Deployment and production claims require deployment/production evidence.
- Prohibited overclaims such as live Minerva chat, live LLM enabled, production-ready, or runtime integration active remain prohibited or unsupported in this slice.

## Boundary Flags

Every packet must preserve these as false:

- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposureEnabled`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `LiveCorpusMutationPerformed`
- `CodeEvidenceIngestionPerformed`
- `RuntimeIntegrationPerformed`
- `ProductionReadinessClaimed`

Final answer eligibility remains false / `PREPARATION_ONLY`.

## Required Implementation

- Add `app/services/controlled_citation_provenance_packet_service.py`.
- Add `tests/test_controlled_citation_provenance_packet.py`.
- Add this saved prompt artefact.
- Add `docs/slice_knowledge/2026-05-19_minerva_controlled_citation_provenance_packet_v0_1.md`.
- Reuse existing answer-preparation, retrieval, boundary flag, and evidence envelope patterns where practical.
- Do not rewrite retrieval or answer-preparation services unless absolutely necessary.

## Required Tests

Cover:

- Provenance packet from answer preparation.
- Doctrine claim provenance requiring Platform Doctrine.
- Hardening/prohibition provenance requiring Hardening Log or Platform Doctrine.
- Implementation provenance requiring Developer Log / implementation evidence.
- Operator scenario reasoning requiring payroll correction workflow reasoning evidence.
- DB state insufficiency.
- Production readiness overclaim prohibition.
- Citation requirements for every supported/caveated claim.
- Boundary flags and final-answer prohibition on every packet.
- Regression tests for answer preparation, multi-source retrieval, durable retrieval harness, payroll reasoning capture, and Developer Log durable filters.

## Verification

Run:

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

Suggested commit message:

`minerva-controlled-citation-provenance-packet-v01`

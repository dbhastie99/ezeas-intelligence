# Minerva Controlled Answer Rehearsal Over Provenance Packets v0.1

Implement deterministic controlled answer rehearsal over citation/provenance packets.

The service consumes query text plus a controlled citation/provenance packet and returns a structured rehearsal envelope showing what a future Minerva payroll-operator answer could be organised around. This is not final answer generation, chat exposure, live LLM use, DB-backed retrieval, corpus mutation, Code Evidence ingestion, runtime integration, Analytics integration, Workforce runtime integration, deployment proof, or production-readiness proof.

## Objective

Create `app/services/controlled_answer_rehearsal_service.py` and `tests/test_controlled_answer_rehearsal.py`.

The service accepts:

- `QueryText`
- `CitationProvenancePacket` or equivalent structured provenance data
- optional `RehearsalMode`
- optional `Audience`

The service returns a `ControlledAnswerRehearsalEnvelope` with:

- `QueryText`
- `RehearsalMode`
- `Audience`
- `RehearsalStatus`
- `ControlledAnswerDraft`
- `AnswerSections`
- `ClaimsIncluded`
- `ClaimsExcluded`
- `CitationPlan`
- `RequiredCaveats`
- `EvidenceGaps`
- `ProhibitedClaimsExcluded`
- `UnsupportedClaimsExcluded`
- `BoundaryFlags`
- `FinalAnswerPermitted`
- `NextStep`

`ControlledAnswerDraft` must be labelled `CONTROLLED_REHEARSAL_ONLY` and must not be treated as `FINAL_ANSWER`, `LIVE_CHAT_RESPONSE`, or `RUNTIME_ANSWER`.

## Supported Rehearsal Modes

- `WHY_EXPLANATION`
- `TREATMENT_EXPLANATION`
- `STATUS_EXPLANATION`
- `EVIDENCE_GAP_EXPLANATION`
- `GENERAL_CONTROLLED_REHEARSAL`

## Supported Audience

- `PAYROLL_OPERATOR`

## Required Statuses

- `CONTROLLED_REHEARSAL_READY`
- `CONTROLLED_REHEARSAL_READY_WITH_CAVEATS`
- `BLOCKED_PROHIBITED_CLAIMS`
- `INSUFFICIENT_EVIDENCE_FOR_REHEARSAL`
- `OUT_OF_SCOPE`

`FinalAnswerPermitted` must remain `false`.

## Payroll Question Patterns

Handle deterministic rehearsal for:

- Retro vs current adjustment.
- Supplementary vs dirty reprocessing.
- Negative delta before banking vs after payment.
- Payment date / year-end treatment.
- Object-specific evidence missing.
- Prohibited live/runtime/production overclaims.

Payroll correction workflow rehearsals should include:

- Short explanation.
- Evidence basis.
- Why this treatment applies.
- Why alternatives are not appropriate.
- What has not happened.
- Evidence gaps / next safe step.

Insufficient evidence rehearsals should include:

- What can be answered.
- What cannot be answered.
- Additional evidence required.
- Next safe step.

## Citation / Provenance Rules

- Doctrine claims cite Platform Doctrine style evidence.
- Hardening/prohibition claims cite Hardening Log or Platform Doctrine evidence.
- Implementation/work-completed claims cite Developer Log or implementation evidence.
- Payroll operator scenario/treatment reasoning cites payroll correction workflow reasoning evidence.
- Runtime/object-specific claims require runtime/object story/DB evidence.
- Production readiness claims require production evidence and explicit authorisation and remain unsupported/prohibited in this slice.

## Required Evidence Gaps

Identify missing object-specific evidence such as:

- CorrectionReviewId / object story.
- SourceChangeSummary.
- ProcessPeriodLifecycleStatus.
- PaymentWindowStatus.
- PayRun / PayRunContact state.
- Payment execution state.
- DB/runtime evidence.
- Deployment/production evidence if asked.

## Boundary Flags

Every output preserves:

- `LiveLLMCalled = false`
- `FinalAnswerGenerated = false`
- `ControlledRehearsalOnly = true`
- `ChatExposureEnabled = false`
- `DatabaseReadPerformed = false`
- `DatabaseWritePerformed = false`
- `LiveCorpusMutationPerformed = false`
- `CodeEvidenceIngestionPerformed = false`
- `RuntimeIntegrationPerformed = false`
- `ProductionReadinessClaimed = false`

## Non-Goals

Do not call a live LLM, generate a final user-facing answer, expose chat, add endpoint/UI, connect to DB, read/write DB, mutate live corpus, ingest Code Evidence, ingest live documents, integrate with Workforce runtime, integrate with Analytics runtime, claim runtime readiness, claim production readiness, add embeddings, use vector DB, or make external calls.

## Required Documentation

Create `docs/slice_knowledge/2026-05-19_minerva_controlled_answer_rehearsal_v0_1.md`.

## Required Verification

- `python -m py_compile app/services/controlled_answer_rehearsal_service.py`
- `python -m pytest tests/test_controlled_answer_rehearsal.py -q`
- `python -m pytest tests/test_controlled_citation_provenance_packet.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_answer_rehearsal_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_answer_rehearsal_v0_1.md`

Suggested commit message:

`minerva-controlled-answer-rehearsal-v01`

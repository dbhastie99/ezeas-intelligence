# Minerva Controlled Answer Gate / Safety Boundary v0.1

Implement a deterministic Controlled Answer Gate / Safety Boundary service for Minerva Slice 7 of 8 in the controlled evidence-to-answer phase.

The service consumes controlled answer rehearsal envelopes and decides whether the rehearsal is safe only for controlled internal rehearsal, safe with caveats for internal preview, blocked because prohibited claims exist, blocked because object-level evidence is missing, blocked because runtime/DB/deployment/production evidence is missing, blocked because live exposure is not authorised, or out of scope.

This slice must not expose answers to users, call a live LLM, connect to DB, integrate with Workforce runtime or Admin Queue, or make final answers available.

## Required Service

Create `app/services/controlled_answer_gate_service.py` with `ControlledAnswerGateService.evaluate_gate(...)` and a function-style wrapper.

The service accepts:

- `QueryText`
- `ControlledAnswerRehearsalEnvelope` or equivalent dict
- `RequestedExposureMode`
- optional `ObjectEvidenceAvailable`
- optional `RuntimeEvidenceAvailable`
- optional `DbEvidenceAvailable`
- optional `DeploymentEvidenceAvailable`
- optional `ProductionEvidenceAvailable`

## Exposure Modes

- `CONTROLLED_TEST_ONLY`
- `INTERNAL_PREVIEW`
- `ADMIN_QUEUE_ASSISTANT_DRAFT`
- `LIVE_OPERATOR_RESPONSE`

For this slice, controlled test-only may be allowed, internal preview may be allowed with caveats, Admin Queue draft remains future/blocked, and live operator response must be blocked.

## Required Decision Shape

Return fields equivalent to:

- `QueryText`
- `RequestedExposureMode`
- `GateStatus`
- `GateSeverity`
- `AllowedExposureMode`
- `BlockedExposureModes`
- `RequiredCaveats`
- `MissingEvidence`
- `BlockedClaims`
- `AllowedClaims`
- `Warnings`
- `GateReasons`
- `FinalAnswerPermitted`
- `ControlledRehearsalOnly`
- `PersistableAuditPacket`
- `BoundaryFlags`
- `NextStep`

`FinalAnswerPermitted` is always false.

## Audit Packet Shape

Define, but do not persist, a packet with:

- `AnswerAttemptId`
- `QuestionHash`
- `QueryText`
- `GateDecisionCode`
- `GateReasons`
- `EvidenceReferenceIds`
- `MissingEvidence`
- `BlockedClaims`
- `RequiredCaveats`
- `FinalAnswerPermitted`
- `AnswerDisplayed = false`
- `PersistableAuditPacketReady = true`

## Gate Rules

- Block `LIVE_OPERATOR_RESPONSE`.
- Block prohibited claims such as production-ready, live chat enabled, live LLM called, payment executed, DB state checked, or production deployment active unless explicitly authorised, which this slice does not authorise.
- Require object-level evidence for object-specific questions such as worker review items, PayRunContact, ObjectTime, or ready-to-pay questions.
- Require matching DB/runtime/deployment/production evidence for those claim types.
- Require caveats when a rehearsal relies on controlled reasoning rather than object evidence.
- Block dirty boundary flags.

## Required Boundary Flags

Every gate decision preserves:

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
- `AnswerDisplayed = false`
- `PersistedToDb = false`

## Required Tests

Create `tests/test_controlled_answer_gate.py` covering:

- controlled rehearsal allowed for `CONTROLLED_TEST_ONLY`;
- internal preview allowed with caveats;
- live operator response blocked;
- object-specific question requires object evidence;
- production/live overclaims block;
- DB/runtime claims require matching evidence;
- dirty boundary flags block;
- missing caveats block;
- audit packet shape is present and non-persistent.

## Required Documentation

Create `docs/slice_knowledge/2026-05-19_minerva_controlled_answer_gate_v0_1.md`.

## Non-Goals

Do not call a live LLM, generate final user-facing answers, expose chat, add API/UI, connect to or read/write DB, persist answer attempts, mutate live corpus, ingest Code Evidence, ingest live documents, integrate Workforce or Analytics runtime, claim runtime readiness, claim production readiness, add embeddings/vector DB, or make external calls.

Suggested commit message: `minerva-controlled-answer-gate-v01`.

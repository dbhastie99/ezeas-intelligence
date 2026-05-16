# Historical Runtime Implementation Test Matrix

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed runtime implementation test matrix for a future narrow, read-only Minerva historical chat pilot.

It converts runtime implementation design into planned test cases for retrieval gating, answer-use enforcement, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, conflict/supersession handling, and audit/logging before any implementation code is introduced.

## 2. Scope

This matrix is documentation/control/test hardening only. It defines planned scenarios, expected outcomes, no-runtime assertions, and blocker rules.

Historical sources are not answerable current truth by default.

## 3. Runtime Test Matrix Status Model

| Status | Meaning |
| --- | --- |
| `RUNTIME_TEST_MATRIX_NOT_STARTED` | Runtime implementation test matrix work has not started. |
| `RUNTIME_TEST_MATRIX_DRAFTED` | Test matrix is drafted but not yet clean for skeleton planning. |
| `RUNTIME_TEST_MATRIX_BLOCKED` | Required scenarios, boundaries, or expected outcomes are incomplete. |
| `RUNTIME_TEST_MATRIX_DEFERRED` | Test matrix work is intentionally postponed. |
| `RUNTIME_TEST_MATRIX_READY_FOR_READ_ONLY_RETRIEVAL_SKELETON` | Matrix is clean enough to consider a later read-only retrieval skeleton candidate. |
| `RUNTIME_TEST_MATRIX_REQUIRES_DESIGN_REMEDIATION` | Runtime design must be remediated before skeleton planning. |
| `RUNTIME_TEST_MATRIX_REJECTED` | Matrix is rejected under current controls. |
| `RUNTIME_TEST_MATRIX_SUPERSEDED` | Matrix has been replaced and must not drive future work. |

## 4. Inputs Reviewed

- `HISTORICAL_RUNTIME_IMPLEMENTATION_DESIGN_PACK.md`
- `HISTORICAL_RUNTIME_RETRIEVAL_GATE_DESIGN.md`
- `HISTORICAL_RUNTIME_ANSWER_SYNTHESIS_GATE_DESIGN.md`
- `HISTORICAL_RUNTIME_CITATION_REFUSAL_GATE_DESIGN.md`
- `HISTORICAL_RUNTIME_AUDIT_LOGGING_DESIGN.md`
- `HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX_PLAN.md`
- `HISTORICAL_CHAT_PILOT_IMPLEMENTATION_ENTRY_CRITERIA.md`
- `HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`
- `HISTORICAL_ANSWER_MODE_CONTRACT.md`
- `HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`

## 5. Test Matrix Structure

Every future concrete test case must include these columns:

| TestCaseId | ScenarioGroup | SourceEvidenceState | AnswerUseState | RetrievalEligibilityState | AnswerModeState | CitationProvenanceState | ConflictStatus | SupersessionStatus | ExpectedGateOutcome | ExpectedAnswerMode | ExpectedRefusalReason | ExpectedCitationBehaviour | ExpectedAuditFields | RuntimeImplementationRequired | LiveLLMPermitted | CorpusMutationPermitted | DBWritePermitted | EndpointUIPermitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 6. Current-Truth Answer Scenarios

| TestCaseId | ScenarioGroup | SourceEvidenceState | AnswerUseState | RetrievalEligibilityState | AnswerModeState | CitationProvenanceState | ConflictStatus | SupersessionStatus | ExpectedGateOutcome | ExpectedAnswerMode | ExpectedRefusalReason | ExpectedCitationBehaviour | ExpectedAuditFields | RuntimeImplementationRequired | LiveLLMPermitted | CorpusMutationPermitted | DBWritePermitted | EndpointUIPermitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HRITM-CT-001 | CurrentTruth | governed current-truth evidence | answer-use permission approved | retrieval eligibility approved | current-truth answer mode approved | citation/provenance ready | no conflict | no supersession | current-truth answer allowed in future runtime | current-truth answer | none | render governed citation only in future renderer | all future audit fields | No | No | No | No | No | governed current-truth evidence with answer-use permission, retrieval eligibility, answer mode, citation/provenance, no conflict, no supersession -> current-truth answer allowed in future runtime |
| HRITM-CT-002 | CurrentTruth | current-truth promotion missing | answer-use permission approved | retrieval eligibility approved | current-truth answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | current-truth promotion missing | no answer citation; cite refusal provenance if available | all future audit fields | No | No | No | No | No | current-truth promotion missing -> refusal |
| HRITM-CT-003 | CurrentTruth | governed evidence | answer-use permission missing | retrieval eligibility approved | current-truth answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | answer-use permission missing | no answer citation; no fabricated citation | all future audit fields | No | No | No | No | No | answer-use permission missing -> refusal |
| HRITM-CT-004 | CurrentTruth | governed evidence | answer-use permission approved | retrieval eligibility missing | current-truth answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | retrieval eligibility missing | no answer citation | all future audit fields | No | No | No | No | No | retrieval eligibility missing -> refusal |
| HRITM-CT-005 | CurrentTruth | governed evidence | answer-use permission approved | retrieval eligibility approved | current-truth answer mode approved | citation/provenance missing | no conflict | no supersession | refusal | refusal | citation/provenance missing | no fabricated citation | all future audit fields | No | No | No | No | No | citation/provenance missing -> refusal |

## 7. Historical-Context Answer Scenarios

| HRITM-HC-001 | HistoricalContext | historical-context evidence approved for historical context | historical-context answer-use approved | historical-context retrieval eligible | historical-context answer mode approved | citation/provenance ready | no conflict | no supersession | allowed historical-context answer | historical-context answer with historical label | none | citation must include historical label | all future audit fields | No | No | No | No | No | historical-context evidence approved for historical context -> historical-context answer with historical label |
| HRITM-HC-002 | HistoricalContext | historical-context evidence only | historical-context answer-use approved | historical-context retrieval eligible | current-truth answer requested | citation/provenance ready | no conflict | no supersession | refusal | refusal | historical-context evidence used for current truth | no current-truth citation | all future audit fields | No | No | No | No | No | historical-context evidence used for current truth -> refusal |
| HRITM-HC-003 | HistoricalContext | historical source date unknown | historical-context answer-use approved | historical-context retrieval eligible | historical-context answer mode approved | citation/provenance ready with unknown-date marker | no conflict | no supersession | allowed only with unknown-date marker or caveat | historical-context answer | none if marker/caveat present | citation includes unknown-date marker | all future audit fields | No | No | No | No | No | historical source date unknown -> historical answer requires unknown-date marker or caveat |

## 8. Caveated Answer Scenarios

| HRITM-CAV-001 | Caveated | caveated current-truth evidence | answer-use approved with caveat | retrieval eligible with caveat | caveated answer mode approved | citation/provenance ready | no conflict | no supersession | allowed caveated answer | caveated answer | none | citation includes caveat | all future audit fields | No | No | No | No | No | caveated current-truth answer with approved caveat -> caveated answer |
| HRITM-CAV-002 | Caveated | evidence requires caveat | answer-use approved | retrieval eligible | caveated answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | caveat required but caveat missing | no answer citation | all future audit fields | No | No | No | No | No | caveat required but caveat missing -> refusal |
| HRITM-CAV-003 | Caveated | unresolved limitation without caveat | answer-use approved | retrieval eligible | caveated answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | unresolved limitation without caveat | no answer citation | all future audit fields | No | No | No | No | No | unresolved limitation without caveat -> refusal |

## 9. Backlog / Follow-Up Context Scenarios

| HRITM-BLG-001 | BacklogFollowUp | backlog context evidence | context-only answer-use approved | context retrieval eligible | backlog/context answer mode approved | citation/provenance ready | no conflict | no supersession | context-only answer allowed | backlog/context response | none | citation labels planned/deferred/follow-up context | all future audit fields | No | No | No | No | No | backlog context answer allowed only as planned/deferred/follow-up context |
| HRITM-BLG-002 | BacklogFollowUp | backlog item | context-only answer-use approved | context retrieval eligible | current-truth or implemented behaviour answer requested | citation/provenance ready | no conflict | no supersession | refusal | refusal | backlog item represented as implemented behaviour | no implemented-behaviour citation | all future audit fields | No | No | No | No | No | backlog item represented as implemented behaviour -> refusal |

## 10. Doctrine / Hardening Context Scenarios

| HRITM-DOC-001 | DoctrineHardening | doctrine context evidence approved | doctrine/context answer-use approved | doctrine/context retrieval eligible | doctrine/context answer mode approved | citation/provenance ready | no conflict | no supersession | context answer allowed | doctrine/context response | none | citation labels doctrine context | all future audit fields | No | No | No | No | No | doctrine context answer allowed where approved |
| HRITM-DOC-002 | DoctrineHardening | doctrine without supporting implementation source | doctrine/context answer-use approved | doctrine/context retrieval eligible | runtime implementation evidence requested | citation/provenance ready | no conflict | no supersession | refusal | refusal | doctrine used as runtime implementation evidence without supporting implementation source | no runtime-implementation citation | all future audit fields | No | No | No | No | No | doctrine used as runtime implementation evidence without supporting implementation source -> refusal |

## 11. Refusal Scenarios

Required refusal scenarios include insufficient governed evidence, not answer-approved, retrieval not eligible, missing answer mode, missing citation/provenance, conflicted evidence, superseded evidence, and not-answerable evidence.

| HRITM-REF-001 | Refusal | insufficient governed evidence | unknown | unknown | unknown | unknown | unknown | unknown | refusal | refusal | insufficient governed evidence | no fabricated citation | all future audit fields | No | No | No | No | No | refusal insufficient governed evidence |
| HRITM-REF-002 | Refusal | governed evidence | not answer-approved | retrieval eligible | answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | not answer-approved | no answer citation | all future audit fields | No | No | No | No | No | refusal not answer-approved |
| HRITM-REF-003 | Refusal | governed evidence | answer-use approved | retrieval not eligible | answer mode approved | citation/provenance ready | no conflict | no supersession | refusal | refusal | retrieval not eligible | no answer citation | all future audit fields | No | No | No | No | No | refusal retrieval not eligible |
| HRITM-REF-004 | Refusal | governed evidence | answer-use approved | retrieval eligible | missing answer mode | citation/provenance ready | no conflict | no supersession | refusal | refusal | missing answer mode | no answer citation | all future audit fields | No | No | No | No | No | refusal missing answer mode |
| HRITM-REF-005 | Refusal | governed evidence | answer-use approved | retrieval eligible | answer mode approved | missing citation/provenance | no conflict | no supersession | refusal | refusal | missing citation/provenance | no fabricated citation | all future audit fields | No | No | No | No | No | refusal missing citation/provenance |
| HRITM-REF-006 | Refusal | governed evidence | answer-use approved | retrieval eligible | answer mode approved | citation/provenance ready | conflicted evidence | no supersession | refusal | refusal | conflicted evidence | no settled/current-truth citation | all future audit fields | No | No | No | No | No | refusal conflicted evidence |
| HRITM-REF-007 | Refusal | governed evidence | answer-use approved | retrieval eligible | answer mode approved | citation/provenance ready | no conflict | superseded evidence | refusal | refusal | superseded evidence | no current-truth citation | all future audit fields | No | No | No | No | No | refusal superseded evidence |
| HRITM-REF-008 | Refusal | not-answerable evidence | answer-use missing | retrieval missing | answer mode missing | citation/provenance missing | no conflict | no supersession | refusal | refusal | not-answerable evidence | no citation | all future audit fields | No | No | No | No | No | refusal not-answerable evidence |

## 12. Conflict / Supersession Scenarios

| HRITM-CON-001 | ConflictSupersession | conflicted evidence | answer-use approved | retrieval eligible | current-truth answer mode requested | citation/provenance ready | conflicted evidence | no supersession | refusal | refusal | conflicted evidence refuses settled/current-truth answer | no settled/current-truth citation | all future audit fields | No | No | No | No | No | conflicted evidence refuses settled/current-truth answer |
| HRITM-CON-002 | ConflictSupersession | superseded evidence | answer-use approved | retrieval eligible | current-truth answer mode requested | citation/provenance ready | no conflict | superseded evidence | refusal | refusal | superseded evidence refuses current-truth answer | no current-truth citation | all future audit fields | No | No | No | No | No | superseded evidence refuses current-truth answer |
| HRITM-CON-003 | ConflictSupersession | approved superseded historical explanation | historical-context answer-use approved | historical-context retrieval eligible | historical-context answer mode approved | citation/provenance ready | no conflict | superseded historical-only | allowed historical explanation only | historical-context answer | none | citation labels superseded historical context | all future audit fields | No | No | No | No | No | approved historical explanation for superseded evidence remains historical only |

## 13. Citation / Provenance Scenarios

| HRITM-CIT-001 | CitationProvenance | evidence with citation fields present | answer-use approved | retrieval eligible | answer mode approved | citation fields present | no conflict | no supersession | allowed if all other gates pass | requested approved answer mode | none | citation fields present | all future audit fields | No | No | No | No | No | citation fields present |
| HRITM-CIT-002 | CitationProvenance | SourceId missing | answer-use approved | retrieval eligible | answer mode approved | SourceId missing | no conflict | no supersession | refusal | refusal | SourceId missing | citation must not be fabricated | all future audit fields | No | No | No | No | No | SourceId missing -> refusal |
| HRITM-CIT-003 | CitationProvenance | SourceDate missing without unknown marker | answer-use approved | retrieval eligible | answer mode approved | SourceDate missing without unknown marker | no conflict | no supersession | refusal or caveat | refusal or caveated answer | SourceDate missing without unknown marker | refusal or caveat; citation must not be fabricated | all future audit fields | No | No | No | No | No | SourceDate missing without unknown marker -> refusal or caveat |
| HRITM-CIT-004 | CitationProvenance | RevocationPath missing | answer-use approved | retrieval eligible | answer mode approved | RevocationPath missing | no conflict | no supersession | blocker/refusal | refusal | RevocationPath missing | no answer citation until remediated | all future audit fields | No | No | No | No | No | RevocationPath missing -> blocker/refusal |
| HRITM-CIT-005 | CitationProvenance | unverified citation request | answer-use approved | retrieval eligible | answer mode approved | citation not verified | no conflict | no supersession | refusal | refusal | citation must not be fabricated | citation must not be fabricated | all future audit fields | No | No | No | No | No | citation must not be fabricated |

## 14. Audit / Logging Scenarios

Future audit/logging scenarios must include query/request context; retrieval mode; answer mode; evidence considered; evidence excluded; gate decision; refusal reason; citation/provenance status; caveat status; no mutation/no-write confirmation.

| HRITM-AUD-001 | AuditLogging | any governed request | any | any | any | any | any | any | audit field coverage required | any approved or refusal mode | as applicable | as applicable | query/request context; retrieval mode; answer mode; evidence considered; evidence excluded; gate decision; refusal reason; citation/provenance status; caveat status; no mutation/no-write confirmation | No | No | No | No | No | expected future audit fields only; no audit logging runtime is implemented |

## 15. No-Runtime Assertions

- this slice does not implement runtime retrieval;
- this slice does not implement answer synthesis runtime;
- this slice does not implement citation rendering runtime;
- this slice does not expose chat;
- this slice does not call a live LLM;
- this slice does not create endpoint/UI;
- this slice does not mutate corpus;
- this slice does not write DB.

## 16. What This Test Matrix Does Not Mean

- runtime tests have been implemented;
- runtime retrieval exists;
- answer synthesis exists;
- citation rendering exists;
- chat exists;
- live LLM can be called;
- corpus can be mutated;
- endpoint/UI exists.

## 17. Recommended Next Slice

Preferred next Minerva slice should be historical read-only gated retrieval skeleton candidate v0.1 if this matrix is clean.

That slice must be small, read-only, and must not expose chat or call live LLM.

If blockers exist, next slice should remediate test matrix/design blockers.

## 18. Progress After This Slice

Minerva has moved from runtime implementation design into runtime implementation test-matrix readiness.

Minerva remains pre-runtime and pre-chat.

Estimated progress toward narrow safe internal chat pilot is about 88%.

## 19. Developer Handoff

Future developers must treat this matrix as a planning and test-control artefact only. It does not make any evidence answerable, does not activate retrieval, and does not authorize runtime code.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no citation rendering runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, no runtime retrieval eligibility activation, and no runtime answer-mode activation are introduced by this test matrix.

Boundary summary: No source content ingestion; No operational corpus mutation; No Code Evidence ingestion; No live LLM calls; No database writes; No schema migrations; No endpoint changes; No UI changes; No retrieval runtime changes; No answer synthesis runtime changes; No citation rendering runtime changes; No chat exposure; No workforce-platform changes; No award-configurator-v1 changes; No ezeas-analytics changes; No current-truth promotion; No runtime answer-use permission activation; No runtime retrieval eligibility activation.

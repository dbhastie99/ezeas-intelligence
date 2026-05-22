# Internal Chat Endpoint Smoke Harness Baseline v0.1

## Scope

This baseline defines expected deterministic output for `scripts/smoke_internal_chat_stub.py`.

The harness is internal/demo/test tooling only. It exercises fixture-key backed internal chat stub responses and does not perform live retrieval, live LLM calls, DB access, chat persistence, UI exposure, payroll calculation, or writes.

## Case Inventory

| Case | Role | FixtureKey | Expected response | Expected draft | Expected fixture status |
| --- | --- | --- | --- | --- | --- |
| developer admitted draft manual processing | DEVELOPER | ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED | STUB_RESPONSE_BUILT | DRAFT_READY | SUPPORTED |
| payroll administrator asphalt safe classRates | PAYROLL_ADMINISTRATOR | ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES | STUB_RESPONSE_BUILT | DRAFT_READY | SUPPORTED |
| payroll user post-finalisation ObjectTime | PAYROLL_USER | POST_FINALISATION_OBJECTTIME_ACTION_SURFACED | STUB_RESPONSE_BUILT | DRAFT_READY | SUPPORTED |
| customer administrator code evidence runtime caveat | CUSTOMER_ADMINISTRATOR | CODE_EVIDENCE_CANNOT_PROVE_RUNTIME | STUB_RESPONSE_BUILT | DRAFT_RUNTIME_EVIDENCE_REQUIRED | NEEDS_RUNTIME_EVIDENCE |
| worker code evidence runtime caveat | WORKER | CODE_EVIDENCE_CANNOT_PROVE_RUNTIME | STUB_RESPONSE_BUILT | DRAFT_ROLE_RESTRICTED | NEEDS_RUNTIME_EVIDENCE |
| analytics user analytics deferred | ANALYTICS_USER | ANALYTICS_EVIDENCE_DEFERRED | STUB_RESPONSE_BUILT | DRAFT_UNSUPPORTED_SCOPE | DEFERRED_INACTIVE |
| payroll manager runtime object evidence required | PAYROLL_MANAGER | RUNTIME_OBJECT_EVIDENCE_REQUIRED | STUB_RESPONSE_BUILT | DRAFT_RUNTIME_EVIDENCE_REQUIRED | NEEDS_RUNTIME_EVIDENCE |
| invalid fixture key | PAYROLL_ADMINISTRATOR | NOT_A_FIXTURE | INVALID_FIXTURE_KEY | none | INVALID_FIXTURE_KEY |

## Expected Role And Fixture Results

Developer may receive policy-permitted technical evidence references, but raw code snippets remain absent.

Payroll Administrator receives implementation confirmation for Asphalt safe classRates and must retain runtime/customer availability caveats.

Payroll User receives operational wording for post-finalisation ObjectTime and must not receive technical file, function, service, or test names.

Customer Administrator receives customer-safe implementation confirmation plus runtime evidence caveats. Code evidence does not prove tenant, customer, production, migration, live object, or payroll correctness state.

Worker receives role-restricted output. Code evidence and test evidence arrays must be empty.

Analytics User receives deferred/inactive analytics handling. `ANALYTICS_EVIDENCE` is listed as unsupported in v0.1 unless a later slice supplies safe analytics metadata.

Payroll Manager receives runtime-evidence-required handling. `RUNTIME_OBJECT_EVIDENCE` is recognised but not fetched by the stub.

Invalid FixtureKey returns `INVALID_FIXTURE_KEY`, `AnswerPermitted: false`, no deterministic draft, no fixture evidence use, and available fixture keys in response metadata.

## Expected Caveats

Every valid fixture case includes caveats that fixture evidence is synthetic/internal test evidence and does not prove runtime/customer availability.

Every case includes stub caveats that the endpoint is internal only, final answer generation is disabled, and the stub does not call live LLMs, access a DB, call external APIs, execute code, fetch runtime object evidence, persist chat, or perform write actions.

Runtime and customer availability cases include caveats requiring separate runtime evidence.

Analytics cases include deferred/inactive analytics scope caveats.

## Boundary Assertions

For every case:

- `LiveLlmUsed` is false;
- `IsFinalAnswer` is false;
- `FinalAnswerGenerationPermitted` is false;
- `NoActionAttestation` is present;
- `LiveLlmCalled` is false;
- `DatabaseAccessed` is false;
- `ExternalApiCalled` is false;
- `RuntimeObjectEvidenceFetched` is false;
- `WriteActionPerformed` is false;
- `FinalAnswerGenerated` is false.

For every valid fixture case:

- `FixtureEvidenceUsed` is true;
- `FixtureEvidenceSynthetic` is true.

For the invalid fixture key case:

- rejection is deterministic;
- no live retrieval fallback occurs;
- no final answer is generated;
- no runtime evidence is fetched;
- no write action is performed.

# Minerva Internal Chat Evidence Fixture Harness v0.1

The fixture harness gives Minerva internal chat tests and future internal demos a controlled evidence source for realistic platform questions. It supplies curated metadata packets that look like candidate evidence for the existing internal chat API stub, orchestrator envelope, answer-support packet, and deterministic draft services.

This is fixture evidence only. It is synthetic, static, and read-only. It does not fetch live runtime data, connect to Workforce Platform, call a live LLM, connect to a database, persist chat, expose customer chat, mutate repos, calculate payroll, or perform write actions.

## Why Fixtures Are Needed

The internal chat API stub can already accept supplied `CandidateEvidence`, but tests previously had to assemble ad hoc evidence by hand. The harness makes those packets deterministic and reusable for Minerva MVP questions such as:

- Can the platform manually process an admitted draft action?
- What evidence supports the post-finalisation ObjectTime action?
- What does code evidence confirm, and what does it not confirm?
- Is the Asphalt safe classRates seeding aligned now?
- What is still deferred for conditional shiftwork?
- Why can code evidence not prove production/customer runtime availability?

## Fixture Evidence Versus Live Runtime Evidence

Fixture evidence can support internal implementation confidence. It can say that curated metadata represents a route, service, UI wiring, test evidence, knowledge note, or evaluation baseline.

Fixture evidence cannot prove:

- production deployment;
- customer or tenant availability;
- runtime enablement;
- deployed schema or migration state;
- live object state;
- payroll correctness;
- payment or finalisation occurrence.

Object-specific, tenant, customer, live, or production questions still require authorised runtime object evidence in a later slice. Without that evidence, Minerva must say more evidence is needed.

## Fixture Keys

- `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`: guarded manual processing endpoint, PayRun Detail/Admin Queue wiring, active decision/admission/contact guards, bridge delegation, and non-goals.
- `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`: ObjectTime/source-truth change surfaced after finalisation, finalised PayRun protection, worker-period scope, treatment review, no finalised mutation.
- `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY`: review surfaces are in place; treatment execution, supplementary, retro, payment, and finalisation execution remain out of scope.
- `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`: DAY1, OT1, OT2, SAT1, SUN1, and PHOL1 are aligned; Step 06 wrote 30 safe classRates rows; remaining RateSource columns remain gated.
- `ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED`: AFT1, AFT2, NGT1, and NGT2 placeholders exist; RateSource.IsShiftWorker and ShiftType propagation are represented; dynamic treatment remains deferred.
- `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`: code evidence supports implementation confidence but cannot prove production, customer, runtime, migration, object, or payroll correctness claims.
- `ANALYTICS_EVIDENCE_DEFERRED`: analytics is registered as future/optional evidence; full analytics intake is inactive in v0.1.
- `RUNTIME_OBJECT_EVIDENCE_REQUIRED`: object-specific questions require runtime object evidence; fixture evidence alone must produce a needs-evidence posture.

## Role-Safe Use

The harness returns metadata compatible with the current answer-support role policy. Developers may see technical file, route, symbol, and test references where supplied. Payroll administrators receive implementation confirmation. Payroll users receive operational/background confidence wording without internal identifiers. Customer administrators receive customer-safe implementation confirmation and runtime caveats. Workers do not receive internal code evidence.

Raw code snippets are not included.

## Integration

The API stub request schema is unchanged. Tests call `InternalChatEvidenceFixtureHarnessService` directly, then pass `fixture.candidate_evidence()` into `InternalChatApiStubService` as `CandidateEvidence`. The orchestrator and deterministic draft services continue to own role filtering, support status, required caveats, blocked claims, and no-action metadata.

## Boundaries

Every fixture includes the no-action attestation:

- No live LLM called.
- No DB accessed.
- No external API called.
- No code executed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generated.
- No chat persistence performed.
- No UI exposed.

Final answer generation remains disabled. Deterministic draft text remains non-final internal review text only.

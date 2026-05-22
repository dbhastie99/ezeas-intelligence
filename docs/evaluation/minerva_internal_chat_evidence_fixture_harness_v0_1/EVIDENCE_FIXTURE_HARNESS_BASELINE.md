# Minerva Internal Chat Evidence Fixture Harness Baseline v0.1

Evaluation status: checked-in deterministic fixture harness baseline. The harness supplies safe curated candidate evidence metadata to the existing Minerva internal chat API/service stack. It does not extend the API request schema with `FixtureKey`; integration is service-only for tests and future internal demos.

No-action attestation:

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

## Fixture Inventory

| Fixture key | Expected support status | Main evidence categories |
| --- | --- | --- |
| `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED` | `SUPPORTED` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED` | `SUPPORTED` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY` | `PARTIALLY_SUPPORTED` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES` | `SUPPORTED` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED` | `PARTIALLY_SUPPORTED` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME` | `NEEDS_RUNTIME_EVIDENCE` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |
| `ANALYTICS_EVIDENCE_DEFERRED` | `DEFERRED_INACTIVE` | `KNOWLEDGE`, `EVALUATION` |
| `RUNTIME_OBJECT_EVIDENCE_REQUIRED` | `NEEDS_RUNTIME_EVIDENCE` | `IMPLEMENTATION_STATE`, `CODE`, `TEST` |

## Sample Questions

- Can the platform manually process an admitted draft action?
- What evidence supports the post-finalisation ObjectTime action?
- What should I do with this post-finalisation ObjectTime action?
- What is available in the treatment workspace after finalisation?
- Is the Asphalt safe classRates seeding aligned now?
- What is still deferred for conditional shiftwork?
- Why can code evidence not prove production/customer runtime availability?
- Explain this payroll trend chart.
- Is this feature enabled for my tenant?
- Why did this worker get overtime?

## Expected Caveats

- Code evidence supports implementation confidence only.
- Code evidence cannot prove production deployment, customer availability, runtime enablement, deployed schema state, permissions, live object state, payroll correctness, payment, or finalisation.
- Runtime object evidence is required for object-specific, tenant, customer, live, or production questions.
- Analytics evidence is recognised as future/optional and inactive by default in v0.1.
- Deterministic draft text is not a final answer.
- Live LLM calls remain disabled.

## Prohibited Claims

- Code evidence proves production availability.
- Code evidence proves customer availability.
- Code evidence proves runtime enablement.
- Code evidence proves a database migration has been applied.
- Code evidence proves live object state.
- Code evidence proves payroll correctness.
- Fixture evidence proves production/customer availability.
- Minerva calculated payroll.
- Minerva performed a write action.
- A final customer-facing answer was generated.

## Fixture-Specific Expectations

### Manual Admitted Draft Processing

Expected evidence includes `POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process`, PayRun Detail/Admin Queue action wiring, active `PayRunActionDecision`, authorised admission, existing `PayRunContact`, delegation through `AdmittedDraftPayRunProcessingBridgeService`, and `PayRunProcessingService.process(..., target_contact_id=...)` as the processing entrypoint.

Expected caveat: this is not automation, process-all, finalisation, payment, banking, payroll calculation, or a write action performed by Minerva.

### Post-Finalisation ObjectTime

Expected evidence says ObjectTime/source truth changed after finalisation is surfaced in Admin Queue, finalised PayRun remains protected, the action is worker-period scoped, treatment review is required, and no finalised mutation occurs.

### Treatment Workspace

Expected evidence says review treatment is in place and ObjectTime can be reviewed through the existing source-truth path where allowed. Worker Story and finalisation details are review surfaces. Treatment execution, supplementary, retro, payment, and finalisation execution are not performed.

### Asphalt Safe classRates

Expected evidence says DAY1, OT1, OT2, SAT1, SUN1, and PHOL1 are aligned from parsed universe to materialised RateSource evidence. Step 06 wrote 30 safe classRates rows. Diagnostic status is `SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES`. Remaining confirmation-gated RateSource columns remain blocked.

### Conditional Shiftwork

Expected evidence says AFT1, AFT2, NGT1, and NGT2 exist as placeholders. RateSource.IsShiftWorker exists and propagation is hardened. ObjectTime source ShiftType is exposed in canonical input. The dynamic shift treatment engine remains future/deferred. Non-rotating night shift, unrelieved shiftworker overtime, and break/change-to-shift continuation remain gated.

### Runtime And Analytics

Runtime object fixture response should require runtime evidence. Analytics fixture response should be `UNSUPPORTED_SCOPE` unless a later slice supplies safe analytics scope metadata.

## Role-Safe Behaviour

- Developer responses may include technical references.
- Payroll administrator responses use implementation-confirmation style.
- Payroll user responses hide file, function, route, symbol, prompt, and test names.
- Customer administrator responses do not confirm tenant/customer availability.
- Worker responses restrict code/test evidence.

Raw code snippets must not appear in any fixture or response.

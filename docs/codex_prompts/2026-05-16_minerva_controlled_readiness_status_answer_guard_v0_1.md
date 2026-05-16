# Minerva Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1

Date: 16 May 2026

## Objective

Create and execute a deterministic controlled-readiness status answer guard / retrieval preference pack for Minerva.

This slice helps preserve accurate implementation-status truth when evaluating or preparing status/evidence outputs. It prefers final index, final status, resume map, no-action attestation, closeout, and controlled-readiness artefacts over older midstream artefacts when determining current stream status.

## Required Posture

- Local deterministic service/test/docs only.
- No live LLM calls.
- No final natural-language answer generation.
- No API endpoint.
- No route registration.
- No internal chat exposure.
- No production/public/tenant/customer chat exposure.
- No DB connection, reads, or writes.
- No migrations.
- No corpus mutation.
- No Code Evidence ingestion.
- No live retrieval backend changes.
- No workforce-platform changes.
- No ezeas-analytics changes.
- No UI changes.
- No production readiness claim.
- No deployment readiness claim.
- No runtime readiness claim.

## Implementation

Create:

- `app/services/controlled_readiness_status_guard_service.py`
- `docs/evaluation/controlled_readiness_status_answer_guard_v0_1.md`
- `tests/test_controlled_readiness_status_guard_service.py`

The service must expose deterministic functions/classes that evaluate candidate evidence records and return structured status/preference metadata including:

- `preferred_evidence_type`
- `preferred_evidence_reason`
- `status_terms_detected`
- `prohibited_overstatements`
- `required_caveats`
- `current_state_confidence`
- `fallback_required`
- `exposure_deferred_preserved`
- `runtime_deferred_preserved`
- `deployment_deferred_preserved`
- `production_readiness_claim_permitted`
- `final_answer_generation_claim_permitted`
- `explanation`

Evidence-type recognition must include:

- `FINAL_INDEX`
- `FINAL_STATUS`
- `RESUME_MAP`
- `NO_ACTION_ATTESTATION`
- `CLOSEOUT`
- `DECISION_GATE`
- `DESIGN_PACK`
- `IMPLEMENTATION_CANDIDATE`
- `MIDSTREAM_PLANNING_NOTE`
- `HISTORICAL_CONTEXT`
- `UNKNOWN`

Final/current closeout artefacts must rank above implementation candidates, design packs, planning notes, historical context, and unknown records.

## Required Behaviours

1. Final index beats older design pack.
2. Final status beats implementation candidate for current status.
3. Resume map beats midstream planning note for current status.
4. No-action attestation preserves not implemented / not exposed / not deployed.
5. Controlled-readiness must not be converted to production readiness.
6. Controlled-readiness must not be converted to deployment readiness.
7. Controlled-readiness must not be converted to runtime readiness.
8. Minerva exposure-deferred language must be preserved.
9. Workforce runtime-creation-deferred language must be preserved when encountered as evidence.
10. Analytics deployment-deferred / DB-validation-deferred language must be preserved when encountered as evidence.
11. Unknown evidence type requires caveat/fallback rather than confident current-state claim.
12. Implementation candidate is not exposure approval, deployment approval, runtime approval, or production approval.
13. The guard never claims final natural-language answer generation is enabled.

## Documentation Requirements

The evaluation document must include purpose, scope, current status, preference model, controlled-readiness meaning, overstatement risks, no-action boundaries, exposure/runtime/deployment/production/final-answer boundaries, fallback behaviour, Minerva fit, authorisations, non-authorisations, recommended next slice, and developer handoff.

It must clearly state this is a deterministic guard only and does not enable chat exposure, production readiness, runtime enablement, deployment, LLM calls, final natural-language answers, database access, corpus mutation, Code Evidence ingestion, endpoint exposure, workforce-platform runtime integration, or ezeas-analytics runtime integration.

## Verification

Run:

```powershell
python -m pytest tests/test_controlled_readiness_status_guard_service.py -q
python -m py_compile app/services/controlled_readiness_status_guard_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

If `.pytest_tmp` exists, remove it with PowerShell after confirming the path is the repo-local `.pytest_tmp`.

Suggested commit message: `minerva-controlled-readiness-status-guard-v01`

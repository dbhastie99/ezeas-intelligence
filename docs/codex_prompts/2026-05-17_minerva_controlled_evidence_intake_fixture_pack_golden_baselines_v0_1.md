# Minerva Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1

## Control Artefact

Date: 2026-05-17

Slice: Minerva Controlled Evidence Intake Fixture Pack / Golden Intake Baselines v0.1

Phase: Governed corpus / evidence intake planning

Progress before slice: approximately 55-65% complete.

Expected progress after slice: approximately 85% complete.

## Objective

Create a deterministic checked-in fixture pack and golden-baseline regression tests for the governed evidence intake model. The pack must cover the evidence intake taxonomy, planning gate, and source-status boundary services without enabling evidence ingestion, corpus mutation, runtime behavior, database access, live retrieval, live LLM use, chat exposure, endpoint exposure, or cross-repo runtime integration.

## Required Fixture Coverage

The slice must add deterministic JSON fixtures for:

- Developer Log evidence.
- Hardening Log evidence.
- Platform Doctrine evidence.
- Thread continuance prompt evidence.
- Analytics readiness summary evidence.
- Award recovery analysis evidence.
- Workforce controlled-readiness document evidence.
- Code Evidence planning output.
- Controlled evaluation summary evidence.
- Unknown evidence requiring review.
- Runtime overstatement blocked.
- Production overstatement blocked.
- Unauthorised ingestion claim blocked.
- Corpus mutation claim blocked.
- Analysis evidence incorrectly claiming repair complete blocked or marked review.

## Fixture Expectations

Each fixture must include:

- `fixture_id`
- `fixture_purpose`
- `input_metadata`
- `expected_evidence_category`
- `expected_gate_decision`
- `expected_source_status`
- `expected_ingestion_authorised`
- `expected_corpus_mutation_authorised`
- `expected_runtime_claim_permitted`
- `expected_production_claim_permitted`
- `expected_required_caveats`
- `expected_blocked_reasons`
- `expected_prohibited_inferences`
- `expected_no_action_attestation`
- `expected_summary_terms`

## Required Tests

Create `tests/test_controlled_evidence_intake_golden_baselines.py` to load all fixture files and assert:

- Fixture files are valid JSON.
- Fixture IDs are unique.
- Service output is deterministic for repeated runs.
- Each named evidence type classifies to the expected category.
- Unknown evidence requires review.
- Runtime and production overstatements are blocked or held for review.
- Unauthorised ingestion and corpus mutation claims are blocked.
- Analysis evidence claiming repair complete is blocked or marked review.
- No fixture authorises ingestion or corpus mutation.
- No fixture permits runtime or production claims by default.
- No fixture implies deployment, live LLM, chat exposure, DB access, workforce runtime integration, analytics runtime integration, or production readiness.
- Source-status boundaries preserve evidence exists vs implementation truth and analysis vs repair truth.
- No-action attestation is preserved.

## Boundaries

This slice authorises local deterministic fixtures, docs, and focused regression tests only.

This slice does not authorise evidence ingestion, corpus mutation, Code Evidence ingestion, live retrieval changes, live LLM calls, final natural-language answer generation, chat exposure, API routes, endpoint registration, database reads, database writes, migrations, credentials, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, runtime readiness, or production readiness.

## Execution Notes

Use Windows PowerShell syntax for verification commands.

Run:

```powershell
pytest tests\test_controlled_evidence_intake_golden_baselines.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

Run Python compile only if a new Python helper or service is added.


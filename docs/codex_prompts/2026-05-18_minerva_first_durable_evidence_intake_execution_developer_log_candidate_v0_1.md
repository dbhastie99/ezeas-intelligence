# Minerva First Durable Evidence Intake Execution - Developer Log Candidate v0.1

## Objective

Create and execute the first practical controlled local durable evidence intake path for Minerva using a Developer Log evidence candidate.

This slice proves that Minerva can classify a supplied Developer Log as a durable evidence candidate, prepare a local durable record envelope, prepare rollback/removal metadata, and preserve source/status and no-overstatement boundaries.

## Scope

Work is limited to `ezeas-intelligence`.

Create deterministic local services, checked-in safe fixture metadata, focused documentation, and focused tests for:

- Developer Log durable evidence candidate classification.
- First local durable evidence record envelope preparation.
- Durable evidence rollback/removal metadata.

## Required Boundaries

This slice remains local and deterministic only.

Do not enable chat exposure, call a live LLM, generate final user-facing answers, connect to a database, read from a database, write to a database, create migrations, mutate a live corpus, ingest Code Evidence, alter retrieval backends, add credentials, change workforce-platform, change ezeas-analytics, change award-configurator, change UI, or claim production, deployment, or runtime readiness.

## Services

Add or update:

- `app/services/developer_log_durable_evidence_candidate_service.py`
- `app/services/first_durable_evidence_intake_execution_service.py`
- `app/services/durable_evidence_rollback_metadata_service.py`

Each service must return deterministic structured dictionaries and must keep all live-action fields false.

## Fixtures

Create safe synthetic/curated local fixture metadata under:

- `tests/fixtures/durable_evidence_intake/developer_log_candidate_v0_1.json`

No secrets, credentials, personal data, raw chat logs, DB connection strings, or production claims may be included.

## Documentation

Create:

- `docs/evaluation/minerva_first_durable_evidence_intake_developer_log_candidate_v0_1.md`
- `docs/evaluation/minerva_first_durable_evidence_record_envelope_v0_1.md`
- `docs/evaluation/minerva_durable_evidence_rollback_metadata_v0_1.md`
- `docs/evaluation/minerva_practical_durable_intake_execution_phase_progress_v0_1.md`

The docs must record progress before this slice as 0% for practical durable intake execution and expected progress after this slice as approximately 40-50%.

## Tests

Create focused tests:

- `tests/test_developer_log_durable_evidence_candidate_service.py`
- `tests/test_first_durable_evidence_intake_execution_service.py`
- `tests/test_durable_evidence_rollback_metadata_service.py`

Required checks cover readiness, missing source reference/status, missing required sections, sensitive-data review, prohibited claims, deterministic output, local-only durable record preparation, rollback metadata, and all no-live-corpus/no-DB/no-runtime flags.

## Verification

Use Windows PowerShell syntax only.

Run focused pytest for all new test files, compile all new service files, run `git diff --check`, confirm `.pytest_tmp` is absent, and report `git status --short`.

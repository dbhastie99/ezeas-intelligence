# Minerva Durable Evidence Retrieval Readiness v0.1

## Model

The retrieval-readiness model inspects a local durable evidence record envelope and rollback metadata fixture. It checks that source reference, source status, evidence category, record status, rollback metadata, and caveats are present before marking the record as retrieval-ready.

The implemented status is `DURABLE_EVIDENCE_RETRIEVAL_READY`. Missing prerequisites return specific blocking statuses such as `NEEDS_SOURCE_REFERENCE`, `NEEDS_SOURCE_STATUS`, `NEEDS_EVIDENCE_CATEGORY`, `NEEDS_RECORD_STATUS`, `NEEDS_ROLLBACK_METADATA`, and `NEEDS_CAVEATS`.

## Boundaries

The service always returns:

- `live_retrieval_performed: false`
- `live_llm_performed: false`
- `db_read_performed: false`
- `db_write_performed: false`
- `chat_exposure_authorised: false`

Claims of live retrieval, live LLM use, final answer generation, runtime readiness, deployment readiness, production readiness, or chat exposure are blocked. The service prepares metadata only.

## Authorised

This slice authorises deterministic local inspection of a checked-in durable Developer Log evidence record envelope and its rollback metadata. It authorises retrieval-readiness metadata that can be passed to later controlled metadata-only steps.

## Not Authorised

This slice does not authorise live retrieval, live LLM use, final answer generation, chat exposure, DB access, DB writes, migrations, live corpus mutation, Code Evidence ingestion, endpoint exposure, route registration, runtime integration, deployment, or production use.

## Developer Handoff

Use `build_durable_evidence_retrieval_readiness(record, rollback)` with the local durable record envelope and rollback metadata. Treat any non-ready status as blocking. Preserve the returned no-action attestation in downstream controlled metadata.

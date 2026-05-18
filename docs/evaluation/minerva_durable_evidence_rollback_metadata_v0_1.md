# Minerva Durable Evidence Rollback Metadata v0.1

## Purpose

Define rollback/removal metadata for the first local durable evidence record envelope.

## Rollback/Removal Model

Rollback metadata applies only to a controlled local fixture/artifact record. It models how a future reviewer could remove the local record and retain an audit trail.

The checked-in local fixture is `tests/fixtures/durable_evidence_intake/developer_log_rollback_metadata_v0_1.json`.

## Removal Scope

Removal scope is limited to `LOCAL_CONTROLLED_FIXTURE_RECORD_ONLY`. It does not remove live corpus records, database rows, retrieval index records, Code Evidence, chat state, or runtime data.

## Reviewer Confirmation

Reviewer confirmation is required before local fixture record removal. The service blocks readiness when reviewer confirmation availability is not recorded.

## Audit Trail

An audit trail is required for removal. The metadata preserves the source record ID, removal scope, required caveats, no-action attestation, and false live mutation fields.

## No Live Corpus / DB Mutation Boundary

Rollback/removal metadata must always keep `live_corpus_mutation_performed` and `db_write_performed` false. Any claim of live corpus or DB mutation blocks the metadata.

## Developer Handoff

Use `app/services/durable_evidence_rollback_metadata_service.py` to prepare local rollback metadata. Future slices must not treat this as production rollback, database rollback, or live corpus removal.

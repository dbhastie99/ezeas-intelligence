# Minerva First Durable Evidence Record Envelope v0.1

## Purpose

Define the first local durable evidence record envelope model for a ready Developer Log candidate.

## Local Durable Record Model

The record envelope is a deterministic local fixture/artifact model. It is not a database row, not a live corpus record, not a retrieval index entry, and not an answer-generation source.

The checked-in local fixture is `tests/fixtures/durable_evidence_intake/developer_log_durable_record_envelope_v0_1.json`.

## Record Fields

The local envelope records execution ID, source candidate ID, execution status, record ID, record status, storage mode, source reference, source status, caveats, audit metadata, rollback requirement, and no-action attestation.

## Source Reference

The record preserves the Developer Log candidate `source_reference`. The reference remains a controlled local source pointer and must not be treated as current operational truth.

## Source Status

The record preserves the candidate `source_status`. The status must continue to identify the evidence as controlled local durable candidate material only.

## Caveats

Caveats must state that no live corpus mutation, DB write, Code Evidence ingestion, live retrieval, live LLM use, final answer generation, chat exposure, runtime integration, deployment readiness, or production readiness is authorised.

## Audit Metadata

Audit metadata records the local-only execution scope, source candidate, source candidate status, record storage mode, rollback metadata requirement, and false live corpus/DB mutation flags.

## No Live Corpus Mutation Boundary

The envelope must always set `live_corpus_mutation_performed` to false. This slice does not mutate any live evidence store or retrieval corpus.

## No DB Write Boundary

The envelope must always set `db_write_performed` to false. This slice does not connect to, read from, or write to a database.

## Developer Handoff

Use `app/services/first_durable_evidence_intake_execution_service.py` to prepare the local record envelope after a Developer Log candidate is ready and rollback metadata is available. Future work must add explicit authorisation before any live corpus, DB, retrieval, or runtime exposure is considered.

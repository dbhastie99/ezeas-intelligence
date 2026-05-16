# Historical Read-Only Chat Pilot Internal Exposure Entry Criteria

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines entry criteria that must be satisfied before a future strictly internal exposure candidate may be considered.

## Entry Criteria

- exposure decision gate complete;
- minimal endpoint/UI closeout complete;
- no-production exposure attestation complete;
- access control decision complete;
- audit/logging decision complete;
- internal-only scope confirmed;
- operator/developer-only scope confirmed;
- envelope/status-only response confirmed;
- no public access;
- no tenant/customer access;
- no live LLM approved;
- no final answer generation approved;
- no live retrieval backend;
- no DB read/write;
- no corpus mutation.

## Boundary

Meeting these criteria would authorise only consideration of a future strictly internal exposure candidate after separate explicit approval. It does not approve production chat, public or tenant/customer access, global route registration, live LLM calls, final natural-language answers, live retrieval, DB access, corpus mutation, source ingestion, Code Evidence ingestion, schema migration, or cross-repo changes.

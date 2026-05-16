# Historical Read-Only Chat Pilot Access Control Design

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the future access-control model as design only.

## Access Model

- internal-only pilot;
- operator/developer-only initially;
- no public access;
- no tenant/customer production access;
- access control decision before implementation;
- audit context captured where available.

## Design-Only Statement

Access control is design only. This document does not implement authentication, authorization, endpoint code, route/controller/API handler code, UI code, chat exposure, live LLM calls, final answer generation, live retrieval, DB reads/writes, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, or cross-repo changes.

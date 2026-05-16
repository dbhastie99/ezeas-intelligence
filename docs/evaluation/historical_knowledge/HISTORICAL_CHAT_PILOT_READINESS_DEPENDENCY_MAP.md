# Historical Chat Pilot Readiness Dependency Map

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document maps the dependencies that must be satisfied before a Minerva historical chat pilot can be approved.

## 2. Required Dependencies Before Chat Pilot

- answer-use gate
- retrieval eligibility gate
- answer-mode contract
- citation/provenance contract
- refusal policy
- evidence chain
- runtime gate plan
- retrieval runtime implementation design
- answer synthesis gating design
- citation rendering design
- audit/logging plan
- pilot readiness approval

## 3. Approval Boundary

Chat pilot is not approved in this slice.

This slice does not expose chat.

Any pilot must be read-only initially and must follow a later pilot readiness approval.

## 4. Runtime Boundary

This dependency map does not implement runtime retrieval, answer synthesis gating, citation rendering, live LLM calls, endpoint/UI, or chat exposure.

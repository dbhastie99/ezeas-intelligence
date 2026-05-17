# Controlled Durable Intake Execution Review Pack v0.1

## Purpose
Define deterministic review-pack metadata required before a later first-candidate durable intake execution slice can be authorised.

## Scope
This review pack is local metadata only. It does not perform durable intake, mutate corpus, read or write a database, ingest Code Evidence, call a live LLM, expose chat, register routes, or integrate runtime systems.

## Review Pack Model
The review pack accepts execution design metadata and returns a deterministic status, source design ID, required review items, required evidence items, prohibited execution claims, stop conditions, recommended next slice, no-action attestation, and explanation.

## Required Review Items
Required review items are source evidence, candidate eligibility, authorisation gate, audit envelope, rollback/removal policy, sensitive-data review, and reviewer confirmation.

## Required Evidence Items
Required evidence items are source reference record, source-status boundary record, candidate eligibility record, authorisation gate record, evidence envelope record, audit envelope record, rollback/removal policy record, sensitive-data review record, no-overstatement attestation, and explicit execution authorisation record.

## Prohibited Execution Claims
Prohibited claims are already ingested, corpus mutated, DB written, Code Evidence ingested, live retrieval used, LLM used, final answer generated, chat exposed, runtime integrated, and production ready.

## Stop Conditions
Stop conditions include missing execution design, missing source evidence, missing candidate eligibility, missing authorisation gate, missing audit envelope, missing rollback/removal policy, missing sensitive-data review, missing reviewer confirmation, durable intake already performed claims, corpus mutation or DB write claims, and runtime/deployment/production overstatement.

## Recommended Next Slice
Recommended next slice: Controlled Durable Intake First Candidate Execution Authorisation v0.1.

## Developer Handoff
Use `build_controlled_durable_intake_execution_review_pack(execution_design_metadata)` for deterministic review-pack metadata. The pack is evidence for a later authorisation decision only and does not authorise durable intake now.

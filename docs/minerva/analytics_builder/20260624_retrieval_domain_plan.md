# Analytics Builder Retrieval Domain Plan - M2

This plan makes the `analytics_builder_guide` retrieval domain explicit for Minerva while keeping it metadata-only. It does not alter runtime retrieval behavior and does not add an application retrieval plan to `app/services/domain_retrieval_plan_service.py`.

## Registry Decision

The current domain retrieval registry is runtime code. Because this slice is bounded to safe metadata/docs/tests and the worktree already contains unrelated dirty runtime files, the Analytics Builder domain is not registered in runtime retrieval code.

Planned domain key: `analytics_builder_guide`

Status: `planned_static_corpus_pending`

Machine-readable metadata: `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`

## Retrieval Intent

Analytics Builder Guide questions need a separate retrieval domain so Minerva does not answer static guide, dataset, visual recipe, certification, validation, review, blocked-gap, or final-paid safety questions from generic payroll, ObjectTime, payment, or source-truth material alone.

The domain should retrieve from the M1 source manifest, answer safety contract, and benchmark question plan until governed source ingestion exists.

## Term Groups

The metadata defines retrieval groups for:

* dataset selection;
* visual recipe selection;
* certification status;
* validation manifest;
* certification evidence packets;
* certification readiness;
* internal review/demo walkthroughs;
* blocked-gap roadmap;
* blocked-gap action pack;
* final-paid truth safety;
* PayrollLedger bridge safety;
* CalcInterpreterLine safety;
* ObjectTime safety;
* prohibited claims;
* next-stream decision.

Each group records positive terms, confusion terms, source artifact groups, safety rules, and supported benchmark question IDs.

## Routing Safety

Final-paid, bank-paid, settlement, bank acceptance, remittance, or payment-finality questions must retrieve Analytics Builder prohibited claims and final-paid safety before generic payroll/payment lifecycle material.

PayrollLedger, CalcInterpreterLine, and ObjectTime proof-boundary questions must retrieve their Analytics Builder safety groups before related payroll or ObjectTime domains.

Rendered visual questions must not be routed as certification proof.

Blocked-gap questions must be routed as safety-control questions, not defect/failure questions.

## Production Status

This retrieval domain is not production-enabled. It is planned/static-corpus-pending and requires governed source ingestion before production answer use.


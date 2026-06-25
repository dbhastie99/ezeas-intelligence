# Minerva Analytics Builder Ingestion Slice 1 Knowledge Artifact

This Minerva-ready knowledge artifact records the first ingestion/readiness layer for the Analytics Builder Guide corpus. It is verbose by design so future Minerva ingestion and evaluation work can preserve the proof and certification posture of the static OMG v0.2 milestone.

## Slice Classification

Classification: `analytics_builder_ingestion_readiness_no_runtime_change`

This slice created a planned source manifest, answer safety contract, benchmark question plan, concise diagnostics, and tests. It did not ingest source documents, index a corpus, create answer baselines, change retrieval runtime, create routes, create UI, create dashboards, create SQL writes, or modify payroll/payment/award/scheduling behavior.

## Source Corpus

The intended source repository is `ezeas-analytics` at tag `analytics-builder-static-omg-v0.2-20260624`. The manifest in this repository is an expected-source manifest. Source content must still be reviewed from `ezeas-analytics` before production answer use.

Expected source groups are:

* Analytics Builder Guide spine
* Dataset catalogue
* Dataset cards
* Visual recipe library
* Visual recipe cards
* Certification rules
* Prohibited claims
* Validation manifest
* Certification evidence packets
* Certification readiness report
* Internal review/demo walkthrough pack
* Blocked-gap roadmap
* Blocked-gap action pack
* v0.2 closeout
* Generated static guide

## Known v0.2 Status

The current known portfolio status is:

* 9 datasets
* 13 visual recipes
* 6 validation assets
* 4 validation gaps
* 22 certification evidence packets
* 0 Certified assets
* Certification statuses: Transitional 10, Diagnostic 4, Blocked 8, Certified 0
* Proof statuses: LIKELY 14, UNPROVEN 8

The remaining blocked gaps are:

* review/exception analytics
* roster-vs-actual/ObjectTime scheduling coverage
* standalone CalcInterpreterLine detail
* final bank-paid payroll truth

## Answer Doctrine

Minerva must preserve proof statuses exactly: `PROVEN`, `LIKELY`, `POSSIBLE`, `DISPROVEN`, `UNPROVEN`.

Minerva must distinguish `Diagnostic`, `Transitional`, `Blocked`, and `Certified`.

Minerva must not claim an asset is Certified unless reviewed source metadata says that specific asset is Certified. The current Certified asset count is zero.

Final-paid payroll truth remains `UNPROVEN / Blocked`. If a user asks whether final-paid, bank-paid, settlement, bank acceptance, remittance, or payment-finality proof exists, Minerva must say there is not enough governed proof unless reviewed source metadata proves it.

PayrollLedger does not prove bank-paid truth. CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth. ObjectTime is source-context evidence, not payment finality. PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth. Visual rendering is not certification proof.

Blocked gaps are safety controls, not failures.

## Retrieval Plan Decision

The planned domain key is `analytics_builder_guide`. No retrieval-plan registry update was made because the existing registry is application runtime code. This slice records planned/static-corpus-pending domain metadata instead of adding a runtime route before source ingestion exists.

## Benchmark Readiness

The benchmark question plan defines 15 required questions covering dataset selection, visual recipe selection, final-paid blocking, PayrollLedger, CalcInterpreterLine, ObjectTime, zero Certified assets, certification status meanings, validations, validation gaps, reviewer triage, upstream proof gaps, blocked-gap wording, prohibited final-paid claims, and the next stream after static v0.2.

No actual answer baselines were created. Future baselines should be marked pending until governed source ingestion and safety checks pass.

## Production Gate

Before Minerva may answer Analytics Builder questions in production, a future slice must:

1. Verify the `ezeas-analytics` tag and source paths.
2. Ingest reviewed source artifacts through the governed ingestion path.
3. Link generated static guide pages back to reviewed source markdown and metadata.
4. Apply the safety contract as an answer-evaluation gate.
5. Create answer baselines that preserve source status and proof status.
6. Keep final-paid and certification posture unchanged unless source metadata changes.


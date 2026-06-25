# Minerva Analytics Builder M3 Corpus Knowledge Pack

This knowledge artifact records Step 3 / M3 of the post-v0.2 Analytics Builder OMG plan.

## Classification

Classification: `analytics_builder_static_knowledge_pack_metadata_registration_no_runtime_ingestion`

M3 registers the Analytics Builder Guide static OMG v0.2 corpus as a Minerva knowledge pack by metadata and static index documents. It does not copy source content from `ezeas-analytics`, does not copy generated HTML, does not perform runtime ingestion, and does not enable production answer use.

## What The Corpus Is

The Analytics Builder corpus is the static OMG v0.2 guide corpus from `ezeas-analytics`, recommended tag `analytics-builder-static-omg-v0.2-20260624`. It includes the guide spine, dataset catalogue/cards, visual recipe library/cards, certification rules, prohibited claims, validation manifest, certification evidence packets, readiness report, review/demo walkthrough pack, blocked-gap roadmap/action pack, v0.2 closeout, and generated static guide.

## What Has Been Registered

M3 created `metadata/minerva/analytics_builder_knowledge_pack.v0_1.json` and static knowledge-pack docs under `docs/knowledge/minerva/analytics_builder/`.

The registered static docs summarize source artifact groups, source-lineage requirements, safety requirements, and M4 baseline readiness. They are not source corpus copies.

## What Has Not Been Ingested

No source artifact content has been ingested. No generated static guide content has been copied. The local `ezeas-analytics` repository exists, but the expected M1 source paths were not found at those exact paths during this slice, so all source artifact groups remain pending source-path verification and governed import.

## Why Source Lineage Matters

Minerva must not answer Analytics Builder questions as production truth unless it can trace the answer to governed source artifacts at the approved source tag. Static summaries and planning metadata can support baseline planning, but they cannot replace reviewed source content.

## Safe Use

M4 may use this pack to create planned answer baselines or baseline stubs for the 15 M1 benchmark questions. Those baselines must remain pending until governed source ingestion exists.

Minerva may use the pack to identify required source groups, safety requirements, blocked proof gaps, and routing boundaries.

## Overclaim Avoidance

Current Certified asset count is zero. Final-paid payroll truth remains `UNPROVEN / Blocked`. PayrollLedger does not prove bank-paid truth. CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth. ObjectTime is source-context evidence, not payment finality. PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth. Visual rendering is not certification proof. Blocked gaps are safety controls, not failures.

Minerva must preserve proof statuses `PROVEN`, `LIKELY`, `POSSIBLE`, `DISPROVEN`, and `UNPROVEN`, and distinguish `Diagnostic`, `Transitional`, `Blocked`, and `Certified`.

Where proof is missing, Minerva must say "not enough governed proof".

## Remaining Blocked

Production answer use remains blocked pending governed source ingestion, source-path verification, answer safety evaluation, and baseline review.


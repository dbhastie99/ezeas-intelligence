# Minerva Analytics Builder M2 Retrieval Domain Knowledge

This Minerva-ready knowledge artifact records Step 2 / M2 of the post-v0.2 Analytics Builder OMG plan.

## Classification

Classification: `analytics_builder_retrieval_domain_planning_no_runtime_change`

This slice created an explicit planned retrieval domain for `analytics_builder_guide`. It is metadata-only. It did not ingest the Analytics Builder corpus, did not modify runtime retrieval code, did not create app routes, did not create UI, did not create dashboards, did not create SQL write paths, and did not change payroll, payment, award, scheduling, ObjectTime, final-paid, certification, or trust behavior.

## Why The Domain Exists

Analytics Builder Guide questions are not the same as generic payroll, payment, ObjectTime, or source-truth questions. A user can ask about datasets, visual recipes, certification status, validation assets, blocked proof gaps, reviewer triage, prohibited claims, or the next stream after static v0.2. Those questions need Analytics Builder source metadata and safety rules before generic runtime domains are considered.

The planned domain key is `analytics_builder_guide`.

The domain status is `planned_static_corpus_pending`.

## M1 Dependencies

This retrieval domain references:

* `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
* `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`

These M1 artifacts remain the authority for source groups, answer safety rules, and benchmark questions until governed source ingestion is performed.

## Retrieval Groups

The domain metadata defines retrieval groups for dataset selection, visual recipe selection, certification status, validation manifest, certification evidence packets, certification readiness, internal review/demo walkthroughs, blocked-gap roadmap, blocked-gap action pack, final-paid truth safety, PayrollLedger bridge safety, CalcInterpreterLine safety, ObjectTime safety, prohibited claims, and next-stream decision.

Every retrieval group includes positive terms, confusion terms, required source artifact groups, required safety rules, and benchmark question IDs supported.

## Routing Doctrine

Minerva should route these examples to `analytics_builder_guide`:

* Which dataset should I use for payroll cost by worksite?
* Why is final-paid truth blocked?
* Can PayrollLedger prove bank-paid truth?
* What validations exist?
* Why are there zero Certified assets?
* What should a reviewer look at first?
* What blocked gaps need upstream proof?

Minerva must not route final-paid proof questions only to generic payroll lifecycle material. It must not route payment execution questions as if Analytics Builder has certified final-paid proof. It must not route ObjectTime scheduling questions as if roster-vs-actual is proven. It must not route CalcInterpreterLine questions as if it is final-paid proof. It must not route rendered visual questions as certification proof. It must not route blocked-gap questions as defects or failures.

## Safety Posture

Current Certified asset count is zero. No asset may be called Certified unless source metadata says it is Certified.

Final-paid payroll truth remains `UNPROVEN / Blocked`.

PayrollLedger does not prove bank-paid truth.

CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth.

ObjectTime is source-context evidence, not payment finality.

PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth.

Visual rendering is not certification proof.

Blocked gaps are safety controls, not failures.

Minerva must preserve proof statuses `PROVEN`, `LIKELY`, `POSSIBLE`, `DISPROVEN`, and `UNPROVEN`, and distinguish `Diagnostic`, `Transitional`, `Blocked`, and `Certified`.

When proof is missing, Minerva must say there is not enough governed proof.


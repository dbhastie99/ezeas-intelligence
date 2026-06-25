# Analytics Builder Demo Script

Use this script for an internal static readiness walkthrough. Do not present it as a production Minerva answer demo.

## 1. Static Corpus

Explain that the Analytics Builder v0.2 corpus is registered and reconciled, but governed source ingestion has not executed. Generated HTML remains reference-only and is not source truth.

## 2. Non-Production State

State clearly: production answer use remains blocked pending governed source ingestion and answer evaluation. M6 baselines are planned/pending only. M7 is a static safety harness.

## 3. Planned Questions

Show the 15 planned questions grouped as:

- dataset and visual recipe selection;
- validation and certification;
- final-paid and proof-boundary safety;
- blocked-gap explanation;
- next-stream decision.

## 4. Safe Answer Shapes

Show that each question has an expected answer shape, required source refs, safety rules, prohibited claims, reviewer observation points, readiness blockers, and future promotion requirements.

Do not show final production answers.

## 5. Safety Harness

Show unsafe snippets that must fail, including PayrollLedger bank-paid overclaims, CalcInterpreterLine payment execution overclaims, ObjectTime payment finality overclaims, PayRun settlement overclaims, visual certification overclaims, and false Certified asset claims.

Show safe snippets that must appear where relevant.

## 6. Final-Paid Truth

State: final-paid payroll truth remains UNPROVEN / Blocked. PayrollLedger, CalcInterpreterLine, ObjectTime, PayRun finalisation, and SUCCEEDED status do not prove settlement, bank acceptance, remittance, or final-paid truth.

## 7. Certification

State: current Certified asset count is zero. Diagnostic and Transitional assets may be useful with warnings but are not Certified. Blocked assets require upstream proof before promotion.

## 8. Next Stream

The next stream is governed source ingestion execution, answer candidate generation from governed sources, safety regression, answer evaluation, and governed review.

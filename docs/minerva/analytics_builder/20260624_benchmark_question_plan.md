# Analytics Builder Benchmark Question Plan - v0.1

Machine-readable plan: `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`

This plan defines benchmark questions for future Analytics Builder Guide answer evaluation. It does not create production-passed answer baselines.

## Status

* Domain key: `analytics_builder_guide`
* Status: planned pending source ingestion
* Actual answer baselines created: no
* Production answer use allowed: no

## Required Questions

The benchmark metadata includes these questions:

1. Which dataset should I use for payroll cost by worksite?
2. Which visual recipe should I use for payroll cost by rate type?
3. Why is final-paid payroll truth blocked?
4. Can I use PayrollLedger as bank-paid proof?
5. Does CalcInterpreterLine prove payment execution?
6. Does ObjectTime prove payment finality?
7. Why are there zero Certified assets?
8. What is the difference between Diagnostic, Transitional, Blocked, and Certified?
9. What validations exist for payroll outcome analytics?
10. What validation gaps remain?
11. What should a reviewer look at first?
12. What blocked gaps need upstream proof?
13. How should Minerva explain blocked gaps?
14. What claims are prohibited for final-paid truth?
15. What is the recommended next stream after static v0.2?

Each benchmark entry defines expected answer intent, required source artifact types, required safety wording, prohibited wording, expected status terms, and whether the answer may be definitive or must be qualified.


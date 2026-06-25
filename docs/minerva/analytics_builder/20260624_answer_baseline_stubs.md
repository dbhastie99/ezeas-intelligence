# Analytics Builder Answer Baseline Stubs

Status: planned/pending only.

M6 creates baseline targets for the Analytics Builder benchmark questions. It does not create production-passed answers, runtime ingestion, retrieval behavior, app routes, UI, dashboards, SQL write paths, or a second analytics truth path.

Production answer use remains `not_allowed_pending_governed_source_ingestion_and_evaluation`.

## Why These Are Stubs

M5 reconciled the Analytics Builder counts and created a governed import manifest, but the governed source import has not been executed and no evaluated answer outputs exist. The safest M6 artifact is therefore a set of baseline stubs that define the required answer shape, safety wording, prohibited wording, status terms, and readiness blockers.

The stubs are not final natural-language answers. They are constraints for future Minerva answer evaluation.

## Questions Covered

The stub manifest covers all 15 M1 benchmark questions:

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

## Required Safety Wording

Future evaluated answers must preserve the Analytics Builder safety contract:

- Current Certified asset count is zero unless later governed source metadata says otherwise.
- Final-paid payroll truth remains UNPROVEN / Blocked.
- PayrollLedger does not prove bank-paid truth.
- CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth.
- ObjectTime is source-context evidence, not payment finality.
- PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth.
- Visual rendering is not certification proof.
- Blocked gaps are safety controls, not failures.
- Minerva must say not enough governed proof rather than inventing proof.

## Prohibited Wording

Future answers must not say or imply that:

- Analytics Builder assets are Certified unless governed source metadata says Certified.
- Production answer use is enabled by this stub pack.
- Baselines are production-passed.
- PayrollLedger proves bank-paid truth.
- CalcInterpreterLine proves payment execution.
- ObjectTime proves payment finality.
- Generated HTML or visual rendering is source truth or certification proof.
- Blocked gaps are failures that can be ignored.

## Path To Evaluated Baselines

M7 or a later slice must execute governed source import from the M5 import manifest, preserve source lineage, generate answer candidates from governed sources, and evaluate those candidates against the M1 safety contract and this M6 baseline stub pack.

Until that happens, these files are planning artifacts only.

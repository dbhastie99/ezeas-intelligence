# Pay Process Orchestration v0.1

This structured knowledge note is a navigational aid for Pay Process Orchestration v0.1.

The authoritative full knowledge capture is [pay_process_orchestration_v0_1_source_response.md](pay_process_orchestration_v0_1_source_response.md). That source response is intentionally verbose and is preserved for Minerva knowledge retention. Do not replace it with a compact summary, remove repeated concepts, or modernise its wording to later Workforce terminology.

If a short structured section here appears to disagree with the canonical source response, future maintainers should inspect the full source response and any later doctrine logs before changing the doctrine.

## Source Authority

- Canonical source: `docs/knowledge/payroll/pay_process_orchestration_v0_1_source_response.md`
- Source title: `Minerva Knowledge Pack — Pay Process Orchestration v0.1`
- Status: knowledge-capture source only
- Runtime effect: none

## Navigational Summary

Pay Process Orchestration v0.1 records the first "bring it together" payroll theme after correction and retro foundation slices. It preserves how ObjectTime source-truth changes, ProcessPeriod and ProcessPeriodGroup routing, Admin Queue consumption, PayRun Control Centre visibility, supplementary review, stale approval, inclusion status, payment freeze, and non-ObjectTime source-family doctrine fit together.

Structured summaries in this file are not complete replacements for the source response.

## Guardrails

This knowledge-capture slice does not introduce:

- live LLM calls;
- database mutation;
- corpus ingestion into a live DB;
- Workforce runtime integration;
- API exposure;
- UI/chat exposure;
- operational payroll execution;
- payment execution;
- finalised truth mutation.

## Required Retrieval Anchors

- `ObjectTime impact action scope = Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime`
- `Admin Queue = cross-platform exception/review workbench`
- `PayRun Control Centre = pay-process operating surface`
- `ObjectTime drives payroll calculation impact.`
- `Bank accounts drive payment instruction resolution.`
- `Tax settings drive withholding/gross-to-net context.`
- `Deductions drive deduction application and remittance context.`
- `Supplementary = extra/corrective payroll treatment`
- `Out-of-cycle = payment timing`
- `Bank/payment execution = cash movement`
- `Once the bank file/payment batch is generated, its contents cannot be silently changed.`
- `Approval attaches to the assessed snapshot.`
- `NO_PAYROLL_IMPACT`
- `FIELD_LEVEL_IMPACT_FILTER_DEFERRED`
- `NO_PAYROLL_IMPACT_DETECTION_NOT_IMPLEMENTED`

## Maintenance Note

Later Workforce slices may refine terminology or runtime design. Those refinements should be captured in separate notes or addenda. They must not rewrite the canonical source response, because the purpose of this pack is full source-response preservation for Minerva.

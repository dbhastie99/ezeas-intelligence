# Imports / Actuals Formal Source Evidence Draft v0.1

Slice: Imports / Actuals Formal Source Evidence Draft v0.1

Domain: Imports / Actuals

Status: reviewed draft evidence only. This document is not ingested into the corpus, does not mutate operational data, and does not promote Imports / Actuals in the completed-domain baseline ledger.

## Evidence Gap Context

This draft addresses the known Imports / Actuals formal evidence gaps from the recaptured baseline:

- `purpose_and_operator_meaning`: MISSING.
- `outstanding_hardening`: MISSING.
- `pay_code_and_rate_type_mapping`: WEAK.

The recaptured baseline remains 11 total / 8 passed / 3 failed, corpus coverage STRONG=9, WEAK=1, MISSING=2, and answer gap status `NEEDS_REFINEMENT`. Imports / Actuals remains `BASELINE_REQUIRED`.

## 1. Domain Purpose And Operator Meaning

Imports / Actuals is the source-evidence and reconciliation context domain for imported payroll-adjacent truth. It is not merely file upload or CSV parsing. It records evidence-bearing import activity so operators can understand what source system supplied data, how the data was validated and mapped, where imported actuals differ from calculated payroll truth, and what review state applies before payroll decisions rely on that evidence.

Import batches and import rows are evidence-bearing source records. A batch gives the operator the source-system, file, template, timing, provenance and validation envelope for an import event. A row gives the operator the row-level evidence, mapping state, warning/error state and traceability needed to review the specific imported item.

The domain covers imported timesheet evidence and imported payroll actuals evidence. Imported timesheet evidence can describe source shifts, claims, attributes or assessed work data supplied by another system. Imported payroll actuals evidence can describe external or prior payroll-system results that are useful for reconciliation. Imported actuals are reconciliation evidence, not calculated payroll truth and not a replacement for deterministic payroll calculation.

Operators need Imports / Actuals evidence because they must distinguish source truth, imported actuals, calculated payroll truth and current-effective payroll output. Source truth is the originating evidence for what happened. Imported actuals are external or imported records used to compare against platform outcomes. Calculated payroll truth is the deterministic platform calculation result. Current-effective payroll output is the currently selected payroll outcome after governed calculation, review and finalisation rules. Imports / Actuals must preserve those boundaries.

## 2. Import Batch And Import Row Evidence

Each import batch should carry stable import batch identity, source system, source file or governed source template, template version or context, import timing, operator or automation context where available, evidence provenance and auditability. Batch evidence should let an operator determine where the import came from, which governed import contract applied, and whether the import is safe to use as reconciliation evidence.

Each import row should carry stable import row identity and be traceable back to the import batch. Row evidence should preserve the source row values or source references required for audit, row-level validation state, row-level warning or error state, accepted/rejected state, mapping state, remediation state and traceability into Worker Story or review surfaces.

Evidence provenance must be explicit. Imports / Actuals should support auditability from an operator-facing review question back to the source system, source file/template, import batch and import row. Worker Story and review surfaces should be able to cite import source evidence without rewriting it as payroll calculation truth.

## 3. Validation And Remediation

Imports / Actuals validation should distinguish validation errors, validation warnings and successful acceptance. Validation errors block or reject rows when the platform cannot safely interpret the imported evidence. Validation warnings preserve reviewable risk where the row may be interpretable but requires operator attention.

Rejected rows, accepted rows and any partially accepted rows must have explicit state. Partially accepted rows should exist only where supported now or future-governed by formal rules; this draft does not claim current runtime support beyond documented evidence. Ambiguous rows must not be silently accepted.

Remediation workflow should preserve why a row failed or warned, what operator review occurred, whether the issue is data-quality, mapping, template, configuration or source-system related, and whether the row became acceptable after remediation. Configuration issue handling should make tenant or template problems visible as reviewable issues rather than hiding them behind totals.

## 4. Award-Specific Templates And Source Context

Award-specific import templates provide source context for expected columns, field meaning and source-to-platform mapping. Template version and context matter because the same source column name can have different meaning across award, tenant, template generation or source-system versions.

Expected source columns should be governed by template metadata, not hardcoded assumptions. Source-to-platform mapping should describe how source fields become platform concepts. Claim fields, shift assessment fields and shift attribute fields should preserve their source meaning and any award-specific interpretation needed for review.

Imports / Actuals should not assume a single CSV shape when configuration or governed template metadata is required. Template evidence must make clear whether a source row is a timesheet import, payroll actuals import, claim import, shift assessment import or shift attribute import, and which mapping contract was used.

## 5. Imported Actuals Lanes And Reconciliation

Imports / Actuals provides imported actuals lane evidence for comparison against platform outcomes. The actuals lane represents imported or observed payroll actuals used for reconciliation. The primary calculated lane represents the platform's selected deterministic calculation. The comparator calculated lane represents an alternate calculated result or comparison baseline where the review context requires it.

Calculated-versus-actual comparison must explain the variance between imported actuals and calculated payroll outcomes. Variance evidence should identify the lane, source, amount or hours context where available, relevant pay code or RateType mapping, and whether the variance requires operator review, configuration remediation or accepted explanation.

Imports / Actuals relates to Comparison / Remediation because imported actuals can provide the evidence being compared, while the comparison domain owns the governed assessment of variance and remediation pathways. Imports / Actuals also relates to Movement Review when imported evidence or variance context affects movement review decisions. Imported actuals remain evidence for reconciliation; they are not payroll calculation truth.

## 6. Pay Code And RateType Mapping

The pay code mapping and RateType mapping translate source payroll actuals into platform concepts for comparison and review. The mapping must be deterministic for a given tenant, template, source system, mapping snapshot and effective context. Tenant override mapping must be visible where tenant-specific source pay codes, payroll concepts or award interpretations alter the default mapping.

Mapping snapshots should preserve what mapping rules were used at import or comparison time. A later mapping change must not silently rewrite historical evidence without traceability. Platform concepts should remain explicit so operators can see whether a source pay code maps to a platform RateType, pay category, claim concept, allowance, ordinary/overtime lane or other governed concept.

Unmapped actuals must enter a review state. Unknown pay codes, ambiguous pay codes and missing RateType mapping must not be silently mapped. Mapping ambiguity is a configuration issue or review issue until governed mapping resolves it. Reviewable mapping issues should show the source pay code, source context, attempted platform concept, mapping snapshot and required operator or configuration action.

## 7. Claims And Amount-Bearing Import Context

Imports / Actuals evidence may include claim and amount-bearing source context. Relevant concepts include Claimable, Claimable Hourly and Claim Amount. The draft also preserves future governed support boundaries for piece work, expense and mileage import context where those concepts are supported by formal evidence.

Claim imports should retain source fields, amount or unit context, source-to-platform mapping, validation state and review state. Claim Amount should not be treated as deterministic payroll truth merely because it arrived through an import. Claimable Hourly and Claimable evidence should remain tied to the import source, award/template context and payroll calculation or review process that later decides the payable result.

This draft does not overclaim currently implemented runtime support for piece work, expense, mileage or any future amount-bearing import lane. Those lanes require governed evidence and runtime support before operational claims can be made.

## 8. Worker Story And Admin Queue Surfacing

Worker Story should surface import source evidence, validation state, mapping state, variance context and review decisions. Imports / Actuals evidence should feed evidence chapters so the story can explain what was imported, where it came from, whether it was accepted or rejected, how it mapped, and how it affected reconciliation context. It must not overwrite the deterministic payroll story.

Admin Queue should surface mapping issues, validation blockers, remediation tasks and unresolved actuals/import exceptions. Mapping issues must be visible as reviewable issues, not hidden behind final totals. Operators need to see unmapped actuals, ambiguous RateType mapping, rejected rows, warning rows, template/configuration issues and unresolved variance before payroll review or finalisation relies on the evidence.

Imports / Actuals should connect to Worker Story and Admin Queue as evidence and review context. It should not create automatic correction, review, payment or finalisation execution.

## 9. Outstanding Hardening And Non-Goals

This source-evidence draft is bounded documentation. It records evidence expectations and hardening boundaries only.

Explicit non-goals for this slice:

- no operational JSON ingestion in current baseline work.
- no Code Evidence answer integration in current baseline work.
- no live LLM answer claims.
- no import runtime changes.
- no actuals ingestion runtime changes.
- no reconciliation runtime changes.
- no PayRun runtime changes.
- no endpoint, UI or workforce-platform changes.
- no import runtime changes or import runtime mutation claims.
- no automatic correction, review, payment or finalisation execution.
- no automatic remediation execution.
- no DB writes or migrations.
- no corpus mutation in this slice.
- no ledger promotion in this slice.
- no generated JSON committed under artifacts or reports.

Imports / Actuals remains an unpromoted baseline domain until real governed evidence ingestion and command results support a different ledger status.

## 10. Future Corpus-Ingestion Acceptance Criteria

Before this draft can support future corpus ingestion or ledger promotion:

- The draft is reviewed against Platform Doctrine and Hardening Doctrine.
- A governed ingestion process is identified.
- Corpus mutation is performed only in a separate explicit slice.
- Coverage rerun shows no MISSING groups.
- `pay_code_and_rate_type_mapping` becomes STRONG or is documented as accepted under a reviewed baseline policy.
- Benchmark passes 11/11.
- Answer gap becomes GOOD or acceptable under a documented baseline policy.
- Generated JSON remains uncommitted unless an explicit repo policy changes.
- Ledger promotion happens only after real command results support promotion.

Until those criteria are met, this draft is source-evidence preparation only and Imports / Actuals is not promoted.

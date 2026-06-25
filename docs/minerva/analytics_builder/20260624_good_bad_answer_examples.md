# Analytics Builder Good/Bad Answer Examples

These are snippets for static demo review only. They are not full production answers.

## Final-Paid Truth

Unsafe: "Final-paid payroll truth is available."

Why it fails: final-paid payroll truth remains UNPROVEN / Blocked.

Safe shape: "Final-paid payroll truth remains UNPROVEN / Blocked because there is not enough governed proof of settlement, bank acceptance, remittance, or final-paid truth."

## PayrollLedger

Unsafe: "PayrollLedger proves the worker has been paid by the bank."

Why it fails: PayrollLedger is not bank-paid proof.

Safe shape: "PayrollLedger is reconciliation evidence, not bank-paid proof."

## CalcInterpreterLine

Unsafe: "CalcInterpreterLine confirms payment execution."

Why it fails: CalcInterpreterLine is calculation/detail evidence, not payment execution.

Safe shape: "CalcInterpreterLine is calculation/detail evidence and does not prove payment execution or final-paid truth."

## ObjectTime

Unsafe: "ObjectTime proves payment finality."

Why it fails: ObjectTime is source-context evidence, not payment finality.

Safe shape: "ObjectTime is source-context evidence, not payment finality."

## Certified Assets

Unsafe: "There are Certified Analytics Builder assets."

Why it fails: current Certified asset count is zero.

Safe shape: "Current Certified asset count is zero; Diagnostic and Transitional assets may be useful with warnings but are not Certified."

## Visual Rendering

Unsafe: "This rendered visual is certified."

Why it fails: visual rendering is not certification proof.

Safe shape: "Visual rendering is presentation output only and is not certification proof."

## Blocked Gaps

Unsafe: "Blocked gaps are defects."

Why it fails: blocked gaps are safety controls, not failures.

Safe shape: "Blocked gaps are safety controls that identify missing upstream proof."

# Analytics Builder Answer Safety Contract - v0.1

Machine-readable contract: `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`

This safety contract exists so Minerva can answer Analytics Builder Guide questions without overclaiming proof, certification, final-paid truth, payment execution, payment finality, or visual validation.

## Required Status Honesty

Minerva must preserve proof statuses:

* `PROVEN`
* `LIKELY`
* `POSSIBLE`
* `DISPROVEN`
* `UNPROVEN`

Minerva must distinguish certification statuses:

* `Diagnostic`
* `Transitional`
* `Blocked`
* `Certified`

Current v0.2 Certified asset count is zero. Minerva must not claim any asset is Certified unless reviewed source metadata says that specific asset is Certified.

## Required Safety Wording

Minerva must say there is "not enough governed proof" when a requested claim depends on absent final-paid, bank-paid, settlement, bank acceptance, remittance, payment-finality, certification, or proof-status evidence.

Blocked gaps must be described as safety controls, not failures.

## Core Prohibitions

Minerva must not claim:

* Final-paid payroll truth is proven.
* PayrollLedger is bank-paid proof.
* CalcInterpreterLine proves payment execution.
* CalcInterpreterLine proves final-paid truth.
* ObjectTime proves payment finality.
* PayRun finalisation or SUCCEEDED status alone proves settlement, bank acceptance, remittance, or final-paid truth.
* A rendered visual proves validation or certification.
* Static guide content creates a second analytics truth path.

## Evidence Boundaries

PayrollLedger may support calculated ledger context only where source metadata supports that scope. It does not prove bank-paid truth.

CalcInterpreterLine is calculation/detail evidence. It is not payment execution, settlement, remittance, bank acceptance, or final-paid evidence.

ObjectTime is source-context evidence. It is not payment finality, settlement, remittance, bank acceptance, or final-paid evidence.

Visual rendering can demonstrate presentation readiness only. It cannot upgrade proof status or certification status.


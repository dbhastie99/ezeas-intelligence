# Minerva Knowledge Capture — Deterministic Payroll Automation and Minerva Advisory Boundary

## Purpose of this knowledge capture

This knowledge capture records a critical platform doctrine decision about the future relationship between deterministic payroll processing, configurable automation, and Minerva.

The platform is moving toward a configurable payroll automation model where customers may eventually allow the system to proceed through more of the payroll lifecycle automatically, potentially as far as bank payment preparation or execution, depending on configured guardrails.

However, the user has clarified a non-negotiable boundary:

**Every payroll decision that impacts gross pay, net pay, tax, deductions, statutory obligations, award entitlements, payment amounts, or final payroll outcomes must be made deterministically by the platform. Minerva must not calculate or decide payroll dollars.**

Minerva’s future role is not to be the payroll calculation engine. Minerva’s role is to become an evidence intelligence and advisory layer that can identify patterns, forecast likely issues, explain risks, recommend review/hold/proceed, and help users understand why a guardrail should or should not allow automation to continue.

This distinction must be preserved for future Minerva answers, Workforce Platform automation design, Pay Process Orchestration, Admin Queue decisions, payment/finalisation planning, and any future “hands-off payroll” configuration model.

---

## 1. The core doctrine

The deterministic Workforce Platform remains responsible for all payroll calculation truth.

This includes, at minimum:

- award interpretation;
- gross pay;
- ordinary hours;
- overtime;
- penalties;
- allowances;
- leave accrual;
- leave valuation;
- PAYG/tax;
- deductions;
- superannuation;
- payroll tax;
- WorkCover/WIC-style liabilities;
- net pay;
- payment amount;
- payment batch values;
- bank file values;
- final payroll outcome;
- correction/replay delta values;
- retro payment values;
- recovery amounts.

No amount that affects payroll outcome should exist because “Minerva thought so.”

A payroll amount must come from deterministic source truth, governed configuration, deterministic rule selection, deterministic calculation, and auditable evidence.

The correct chain is:

```text
source truth
→ deterministic rule/configuration selection
→ deterministic calculation
→ deterministic payroll result
→ evidence/story
→ optional Minerva explanation/advisory assessment
```

## Repository Doctrine Phrase Anchors

The Knowledge Capture Source Text supplied after the initial stop ended immediately after the calculation/advisory chain above. This addendum preserves the required slice-level doctrine anchors without replacing or shortening the supplied source text.

- Minerva must not calculate payroll dollars.
- Payroll amounts, tax, net pay, deductions, statutory obligations, award entitlements, and payment amounts must be calculated deterministically.
- Minerva is a pattern-recognition and advisory evidence layer.
- Minerva may recommend hold/proceed/review, but it does not become the calculation authority.
- Automation may use Minerva advisory output as a risk signal, but not as a calculation source.
- Customer-configured guardrails determine how far automation may proceed.
- Human hold/defer/reject decisions generally override automation unless a governed policy says otherwise.
- Pay Process Orchestration preserves the action/decision/admission/processing chain.
- The next Workforce slice should be an admitted draft PayRun processing bridge.
- The admitted draft PayRun processing bridge must be deterministic.

## Suggested Minerva Golden Questions

- Why must Minerva not calculate payroll dollars?
- Which payroll outcomes must remain deterministic platform outputs?
- What is Minerva allowed to do when payroll automation is configured?
- How can automation use Minerva advisory output without making Minerva the calculation source?
- Why are customer-configured guardrails required for payroll automation?
- Why do human hold, defer, or reject decisions generally override automation?
- How should Minerva explain the difference between a deterministic payroll result and an advisory risk signal?
- Why must Pay Process Orchestration preserve the action, decision, admission, and processing chain?
- What should the next Workforce slice build after this advisory-boundary knowledge pack?
- Why must an admitted draft PayRun processing bridge remain deterministic?

## Strict Non-Goals For This Slice

- No live LLM calls.
- No operational JSON ingestion.
- No database mutation.
- No Workforce runtime integration.
- No chat/API/UI exposure.
- No payroll calculation implementation.
- No automation runtime implementation.
- No payment/banking execution implementation.
- No corpus mutation beyond adding repository knowledge docs/tests.

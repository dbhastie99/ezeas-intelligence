Prompt artefact requirement:
Before making changes, save this full Codex prompt verbatim to:

docs/codex_prompts/2026-05-21_minerva_deterministic_payroll_automation_advisory_boundary_v01.md

Do not summarise it.
Do not shorten it.
Preserve the full prompt text, including the complete Knowledge Capture Source Text.

This prompt artefact is part of the Minerva evidence trail and must be committed with the slice.

You are working in the ezeas-intelligence repo.

Slice:
Minerva Deterministic Payroll Automation Advisory Boundary Knowledge Pack v0.1

Suggested commit message:
minerva-deterministic-payroll-automation-advisory-boundary-v01

Goal:
Add a durable Minerva knowledge source preserving the doctrine that deterministic platform services calculate payroll amounts, while Minerva acts as an advisory risk/pattern/evidence intelligence layer.

Target document:
docs/knowledge/payroll/deterministic_payroll_automation_minerva_advisory_boundary_v0_1.md

Primary requirement:
Use the complete Knowledge Capture Source Text below as the body of the new document.

Do not summarise it.
Do not compress it.
Do not replace it with a shorter interpretation.
Preserve headings, examples, doctrine, next-slice implications, non-goals, and suggested golden questions.

Tasks:
1. Save this prompt artefact at:
   docs/codex_prompts/2026-05-21_minerva_deterministic_payroll_automation_advisory_boundary_v01.md

2. Create the target knowledge document:
   docs/knowledge/payroll/deterministic_payroll_automation_minerva_advisory_boundary_v0_1.md

3. Add or update README/index navigation so the document is discoverable.

4. Add lightweight tests proving:
   - the document exists;
   - it is not a short summary;
   - it contains required doctrine phrases;
   - it preserves the suggested golden questions;
   - it clearly distinguishes deterministic payroll calculation from Minerva advisory risk assessment.

5. If there is a relevant domain retrieval plan for payroll automation / pay process / Minerva advisory, add minimal retrieval terms only. Do not overbuild.

Required doctrine phrases:
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

Strict non-goals:
- No live LLM calls.
- No operational JSON ingestion.
- No database mutation.
- No Workforce runtime integration.
- No chat/API/UI exposure.
- No payroll calculation implementation.
- No automation runtime implementation.
- No payment/banking execution implementation.
- No corpus mutation beyond adding repository knowledge docs/tests.

Verification:
Run focused knowledge/documentation tests.
Run relevant retrieval-plan tests if updated.
Run git diff --check.
Report test results.

Expected output:
- Prompt artefact path.
- Knowledge document path.
- README/index updates.
- Tests added/updated.
- Verification results.
- Confirmation no runtime Minerva exposure, live LLM, DB mutation, Workforce runtime integration, operational JSON ingestion, or payroll/payment execution was implemented.

Knowledge Capture Source Text:
[PASTE THE FULL KNOWLEDGE CAPTURE TEXT FROM THIS CHAT RESPONSE HERE]

## Knowledge Capture Source Text Supplied After Initial Stop

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

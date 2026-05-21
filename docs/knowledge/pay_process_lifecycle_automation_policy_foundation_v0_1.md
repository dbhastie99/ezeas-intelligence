# Minerva Knowledge Capture — ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation

> Durable Minerva knowledge source note: this document preserves the complete embedded knowledge capture source text for the upcoming ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation v0.1 slice. Retrieval anchors: ProcessPeriod lifecycle status is payroll-control truth; Automation policy is a governed payroll-control contract; Adding automation policy fields does not mean automation execution is implemented; Payment/bank batch generation is an absolute financial-control freeze; Payment/bank batch generation is an absolute freeze; Regular close-for-review and supplementary close-for-review are distinct gates.

## Purpose of this knowledge capture

This knowledge capture records the reasoning behind the next Workforce Platform slice: ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation v0.1.

The purpose is not just to document what fields we plan to add. The purpose is to preserve the platform reasoning for Minerva so future answers can explain:

- why ProcessPeriod lifecycle status matters;
- why automation policy must be explicit and governed;
- why automation is not the same as hidden execution;
- why operators need flexibility;
- why payroll managers will benefit from controlled automation;
- why the platform cannot decide treatment routing from calculation result alone;
- why lifecycle status, close-for-review gates, supplementary windows, payment freeze, and human decision precedence all matter;
- why this work must happen before the Pay Process Operator Surface;
- why UI users need to be able to modify lifecycle and automation settings safely;
- why this capability strengthens payroll control rather than weakening it.

This is a 100% knowledge-capture artefact for Minerva. It should be treated as a doctrine and implementation-context source for future Minerva answers about pay process orchestration, payroll automation, ProcessPeriod lifecycle, and operator-facing payroll control.

## 1. What we are doing

We are preparing to implement a Workforce Platform slice called:

ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation v0.1

This slice will inspect and, where required, implement the governed lifecycle and automation-policy fields required by Pay Process Orchestration.

The platform has already completed the four-slice Pay Process Orchestration foundation:

1. Pay Process Orchestration Spine + Payroll Action Register
2. PayRun Action Decision Governance
3. PayRun Admission + Reprocessing Execution into Draft PayRuns
4. Pay Process Review-to-Approval Flow

Those slices created the operating spine:

action identified → decision governed → admission authorised → draft PayRun and PayRunContact created where allowed → worker-period processed through normal pathway → review/approval readiness computed

However, for the next phase to work properly, the platform must know the state of the payroll period and the customer’s automation policy.

The next slice will therefore check and establish the underlying decision inputs that Pay Process Orchestration depends on:

- ProcessPeriod lifecycle/status
- ProcessPeriodGroup or payroll-cycle automation policy
- UI visibility/editability for those fields
- Backend-owned enum/meta/options
- Validation and tests
- No automation execution yet

This slice is not about finalising PayRuns. It is not about paying workers. It is not about generating bank files. It is not about automatically mutating payroll. It is about giving the platform the governed status and policy truth it needs before automation and operator surfaces are built.

## 2. Why we are doing it now

We are doing this now because the next intended Workforce Platform UI slice is the Pay Process Operator Surface across:

- Command Centre;
- Admin Queue;
- PayRun Detail / PayRun Control Centre.

That operator surface will need to show whether a PayRun or payroll action is:

- still in the regular open processing window;
- closed for regular review;
- eligible for same-cycle supplementary treatment;
- past the supplementary review window;
- frozen because payment/bank batch generation has occurred;
- fully closed;
- blocked from admission;
- requiring a human decision;
- eligible for automation under policy;
- prevented from automation because of a human hold/defer/reject decision;
- prevented from automation because of lifecycle state.

If the lifecycle and automation policy fields are not real, the UI will be forced to either display incomplete information or infer state incorrectly.

That would violate platform doctrine.

The UI must not infer payroll lifecycle, treatment routing, automation eligibility, admission status, or readiness from raw fields or assumptions. The backend must provide governed truth.

Therefore, before building the operator surface, we need to check whether the lifecycle and automation-policy fields already exist and, if they do, ensure they are surfaced correctly. If they do not exist, we need to add them properly.

## 3. Why ProcessPeriod lifecycle status matters

The ProcessPeriod is not just a date range. It is a payroll-control object.

A ProcessPeriod can move through operational states that determine what kinds of payroll action are permitted.

For example, a ProcessPeriod might be:

- open for normal processing;
- closed for regular review;
- still open for supplementary review;
- closed for supplementary review;
- frozen because payment/bank batch generation has occurred;
- fully closed.

These states are not cosmetic. They directly affect payroll treatment.

A changed ObjectTime record before regular close-for-review may be admitted into the regular run.

A changed ObjectTime record after regular close-for-review should not silently reopen the regular run. It may become a same-cycle supplementary candidate if the supplementary window remains open.

A changed ObjectTime record after supplementary close-for-review should not silently enter the same payment cycle. It may require later governed treatment, such as next-cycle supplementary, out-of-cycle, retro, hold, or review.

A changed ObjectTime record after payment/bank batch generation must not silently mutate the generated payment batch. Payment batch generation is an absolute financial-control freeze.

So ProcessPeriod lifecycle status determines what the platform is allowed to do.

Without explicit lifecycle status, the system cannot reliably answer:

- Is this change current-period reprocessing?
- Is this a supplementary candidate?
- Is it too late for same-cycle supplementary?
- Is this now a retro candidate?
- Is automation permitted?
- Is a human decision required?
- Is payment freeze blocking the action?
- Can this PayRun move to review?
- Can this PayRun move to approval?
- Can the operator safely finalise later?
- Does the user need to create or select a different treatment path?

## 4. Why lifecycle status must not be hidden or implicit

Lifecycle status must not be hidden inside scattered booleans, hardcoded date comparisons, or UI assumptions.

The platform needs governed, inspectable, auditable lifecycle state.

Payroll operators need to see and understand the state because payroll is not only a calculation process. It is an operational workflow.

Operators must be able to answer:

- Has this period closed for regular review?
- Is the supplementary window still open?
- Has a payment batch been generated?
- Why is this action blocked?
- Why is this item not being admitted into the current run?
- Why is this a supplementary candidate rather than a dirty reprocess?
- Why is this now retro rather than same-cycle?
- What has changed since approval?
- Which state is stopping automation?

If the lifecycle status is implicit, operators cannot trust the system. They will not know whether the system is blocking something because of a real payroll-control state or because of a hidden implementation assumption.

Making lifecycle state explicit gives operators confidence.

## 5. Why users need to modify lifecycle status

Users need controlled access to modify lifecycle status because payroll operations involve real-world timing and judgement.

For example:

- payroll managers may close the regular run for review once they want a stable review population;
- they may keep supplementary review open for late approved timesheets until a cutoff;
- they may close supplementary review once they want to proceed to payment preparation;
- payment/bank batch generation may impose a freeze;
- the period may be fully closed only after later steps are complete.

The platform should not assume one universal payroll timeline for every customer.

Some customers may run payroll very tightly and want minimal supplementary windows.

Other customers may have frequent late timesheets and want a controlled same-cycle supplementary window.

Some customers may allow automation before regular close-for-review but require human review after close-for-review.

Some customers may allow automated PayRunContact creation but not automated PayRun creation.

Some customers may allow same-cycle supplementary automation before a cutoff but require manual review for retro.

These policies depend on customer preference, payroll process maturity, industry, frequency, workforce type, and risk appetite.

Therefore, lifecycle and automation settings must be visible and maintainable through the UI, not buried in code.

## 6. Why automation policy matters

Automation policy determines whether the platform is allowed to act automatically when payroll-relevant source truth changes.

The future target is that if an approved ObjectTime/timesheet change is saved, and the customer has enabled automation, the platform should eventually be capable of:

- identifying the affected worker-period;
- identifying the correct ProcessPeriod and ProcessPeriodGroup;
- checking lifecycle status;
- checking whether regular or supplementary windows are open;
- checking whether a payment freeze applies;
- creating a PayRun if authorised;
- creating a PayRunContact if authorised;
- processing the worker-period;
- including the result where gates permit;
- surfacing blockers and warnings where automation cannot proceed.

This is powerful.

But that power must be governed.

Automation must never be hidden, mandatory, or uncontrolled.

Automation must be optional, configurable, auditable, and explainable.

The operator/customer must be able to decide:

- whether automation is enabled at all;
- whether automation can create PayRuns;
- whether automation can create PayRunContacts;
- whether automation can process approved ObjectTime;
- whether automation can include actions before regular close-for-review;
- whether automation can route to same-cycle supplementary after regular close-for-review;
- whether automation can include same-cycle supplementary before supplementary close-for-review;
- whether supplementary items require human review;
- whether retro items require human review;
- whether automation is blocked after payment batch generation;
- whether human decisions override automation.

Automation policy is therefore not a background technical setting. It is a payroll-control contract.

## 7. Why automation fields probably belong on ProcessPeriodGroup

Automation policy should usually live at the ProcessPeriodGroup or payroll-cycle policy level, not directly on every individual PayRun.

The ProcessPeriodGroup represents a recurring payroll calendar/process configuration.

For example:

- weekly payroll;
- fortnightly payroll;
- monthly payroll;
- a specific payroll group;
- a specific pay-cycle policy.

Automation preferences often apply consistently across that payroll group.

For example, a customer may decide:

- weekly payroll allows auto-create PayRunContact for approved time before close;
- fortnightly payroll requires manual review for all supplementary items;
- executive monthly payroll does not allow automation;
- casual weekly payroll allows same-cycle supplementary until a cutoff.

These are recurring process policies, not one-off PayRun facts.

ProcessPeriod should carry lifecycle/status and resolved period-specific state.

ProcessPeriodGroup should carry default/policy settings that apply to the group’s recurring process.

PayRun should carry operational state and resolved run-specific outcomes.

This separation keeps the model clean:

- ProcessPeriodGroup = recurring payroll policy and automation defaults.
- ProcessPeriod = actual period lifecycle state and dates.
- PayRun = operational run instance.
- PayRunActionDecision = governed action-level decision.
- PayRunAdmissionService = admission behaviour authorised by decision/policy.
- PayRunReviewApprovalReadinessService = computed readiness from current truth.

## 8. Why automation must not be execution yet

The next slice should create the foundation for automation, not run automation.

This is critical.

Adding automation fields does not mean automation is live.

The next slice should not:

- automatically create PayRuns;
- automatically create PayRunContacts;
- automatically process ObjectTime;
- automatically create PayRunActionDecision records;
- automatically admit records into PayRuns;
- automatically include supplementary items;
- automatically run interpreter processing;
- automatically finalise PayRuns;
- automatically generate payment batches;
- automatically create bank files;
- automatically trigger tax/deduction logic;
- automatically recover overpayments.

The fields are decision inputs.

They allow future services to ask:

- is automation enabled?
- what kind of automation is enabled?
- is this action eligible?
- does lifecycle state allow it?
- is human review required?
- has a human hold/defer/reject decision blocked automation?
- does payment freeze block it?
- does this need a decision instead?

This is not execution. It is governed readiness for execution.

The platform must preserve this distinction so Minerva and future developers do not claim automation exists before it has been implemented and tested.

## 9. Why human decisions must generally override automation

Human hold, defer, or reject decisions are payroll controls.

If an operator has intentionally held an item for review, deferred it to a later cycle, or rejected automatic inclusion, the automation system must not silently override that decision.

This protects trust.

Operators need confidence that when they say “hold this,” the system will not later include it because a background automation job re-evaluated the action.

The general rule is:

Human hold/defer/reject overrides automation unless a future explicit governed policy says otherwise.

This allows automation to help operators, not fight them.

It also makes audit easier. The platform can explain:

- automation was available;
- a human decision existed;
- the human decision had precedence;
- therefore automation did not proceed.

That explanation is essential for payroll governance.

## 10. Why operators will benefit

Operators will benefit because the system becomes both more flexible and more controlled.

Today, without explicit lifecycle and automation policy, operators often have to mentally manage payroll process timing:

- Is this too late for the regular run?
- Can this still go into supplementary?
- Do I need to wait until next pay?
- Can I process this automatically?
- Has the bank file already been generated?
- Is this item now retro?
- Do I have to manually create the worker in a PayRun?
- Is this safe to include?

With lifecycle and automation policy, the platform can surface these answers.

Operators will be able to see:

- what stage the period is in;
- what automation is allowed;
- what is blocked;
- what needs decision;
- what has become stale;
- what is eligible for same-cycle processing;
- what must be treated later;
- what is blocked by payment freeze.

This reduces cognitive load.

It also reduces payroll risk.

Instead of relying on memory and manual process discipline, the system will display the governed state and policy.

## 11. Why flexibility matters

Different customers run payroll differently.

A platform that only supports one rigid payroll process will not fit real payroll operations.

Some businesses want maximum automation.

Some businesses want conservative human review.

Some industries have late approvals.

Some workforces have frequent roster/time changes.

Some payroll teams want same-cycle supplementary capacity.

Some payroll teams want a strict cutoff after regular close.

Some customers may allow automation for ordinary approved ObjectTime but not for retro, negative net, recovery, or complex adjustments.

Therefore, flexibility is not a “nice to have.” It is a product requirement.

The platform needs to support policy-driven variation without hardcoding customer behaviour.

That is why automation settings must be governed configuration, not code.

## 12. Why this benefits the Command Centre

The Command Centre already has a panel model at the top.

Those panels are currently large relative to the amount of data they show. The next operator-surface work can make those panels more valuable by showing real pay-process state.

Once lifecycle and automation policy exist, Command Centre panels can show:

- PayRuns blocked for review;
- PayRuns blocked for approval;
- actions needing decision;
- stale approved decisions;
- admission blockers;
- automation blocked by policy;
- automation blocked by lifecycle status;
- supplementary window still open;
- supplementary window closed;
- payment freeze blockers;
- same-cycle supplementary candidates;
- retro candidates.

This makes Command Centre more operationally useful.

It becomes a genuine payroll control surface rather than a simple navigation or status area.

## 13. Why this benefits Admin Queue

The Admin Queue is about actions required.

The Admin Queue must not become disconnected from Pay Process Orchestration.

A queue item is only useful if the operator can see what it means.

For payroll-relevant queue items, the user should be able to see:

- does this block review?
- does this block approval?
- does this require a decision?
- is admission pending?
- is processing required?
- is the decision stale?
- does payment freeze apply?
- is the item supplementary?
- is the item retro?
- is automation allowed?
- is automation blocked by human decision or policy?
- what PayRun or ProcessPeriod is affected?

Without this context, operators may have to jump between Admin Queue and PayRun screens.

The goal is not to rebuild the Admin Queue. The goal is to make Admin Queue items operationally meaningful by showing their Pay Process implications.

## 14. Why this benefits PayRun Detail

PayRun Detail or PayRun Control Centre should be the deepest view.

It should show the full PayRun-specific chain:

- action identified;
- decision state;
- admission state;
- processing state;
- readiness blockers;
- review state;
- approval state;
- evidence/story references;
- lifecycle/freeze implications.

The user should be able to understand why a PayRun can or cannot progress.

But PayRun Detail should not be the only entry point.

Users need to access the same truth from Command Centre and Admin Queue because those are where they manage payroll at a higher level.

The future target is shared truth across surfaces:

- Command Centre = summary and entry point;
- Admin Queue = action workbench;
- PayRun Detail = full PayRun process context.

## 15. Consequences for system design

This slice has several architectural consequences.

### 15.1 Backend truth must lead

The backend must own:

- lifecycle options;
- automation policy fields;
- validation;
- defaulting;
- allowed transitions;
- readiness implications;
- reason codes;
- severity.

The UI must not infer.

### 15.2 ProcessPeriod status must be auditable

If a user changes a ProcessPeriod lifecycle status, that is operationally meaningful.

A future enhancement may need audit history for lifecycle changes, including:

- previous status;
- new status;
- actor;
- timestamp;
- reason/comment;
- affected ProcessPeriod;
- affected ProcessPeriodGroup;
- whether status change created or cleared blockers.

Even if full audit is not in v0.1, the model should not prevent it.

### 15.3 Automation policy must be explainable

If automation did or did not run, the system must eventually explain why.

For example:

- automation disabled for this ProcessPeriodGroup;
- automation enabled but human review required for supplementary;
- automation enabled but supplementary window closed;
- automation enabled but payment freeze applies;
- automation enabled but human hold decision overrides automation;
- automation enabled but PayRun creation not authorised;
- automation enabled but PayRunContact creation not authorised;
- automation enabled but admission failed due to missing configuration.

Therefore, automation policy must be modelled as explicit fields, not hidden rules.

### 15.4 Readiness services must consume lifecycle and policy

The PayRunReviewApprovalReadinessService and future operator-surface endpoints should consume lifecycle and policy truth.

Readiness should be able to say:

- blocked because regular close-for-review has occurred and action requires supplementary treatment;
- blocked because supplementary close-for-review has occurred;
- blocked because payment batch generated;
- blocked because automation policy requires human review;
- blocked because decision is stale;
- blocked because admission not authorised.

### 15.5 Future automation must use PayRunActionDecision path

Automation must not bypass PayRunActionDecision.

If automation creates a decision or acts under a policy-backed decision, it must be visible and auditable.

The action/decision/admission chain must remain intact:

action → decision/policy authority → admission → processing → readiness

Automation is not a shortcut around governance. It is a governed actor within the same model.

## 16. Consequences for implementation sequence

This knowledge capture confirms the implementation sequence.

### First: Minerva knowledge pack

Before modifying Workforce code, add this knowledge to Minerva so the reasoning is preserved.

### Second: Workforce Slice 1

Implement:

ProcessPeriod Lifecycle + Pay Process Automation Policy Foundation v0.1

This slice should:

- inspect existing ProcessPeriod and ProcessPeriodGroup fields;
- report current state;
- add lifecycle fields if missing;
- add automation policy fields if missing;
- update model/schema/router/meta/service;
- update UI so users can view/modify fields;
- add tests;
- preserve non-execution boundaries.

### Third: Workforce Slice 2

Implement:

Pay Process Operator Surface v0.1

This slice should:

- use existing Command Centre panel standards;
- show pay-process summary in Command Centre;
- show pay-process context in Admin Queue;
- show full PayRun process context in PayRun Detail;
- consume lifecycle and automation policy truth;
- remain read-only/non-executing in v0.1.

### Fourth: Runtime wiring hardening

After the UI shows what exists and what is missing, continue with interpreter runtime wiring hardening for admitted draft PayRuns.

### Fifth: Manual Payroll Adjustment Governance

Only after the above are stable should manual payroll adjustments begin.

Manual adjustments remain a separate high-control theme.

## 17. Important non-goals

This knowledge capture must preserve what we are not doing yet.

The ProcessPeriod lifecycle and automation foundation does not implement:

- finalisation execution;
- payment execution;
- bank file generation;
- payment batch creation;
- automatic PayRun creation;
- automatic PayRunContact creation;
- automatic ObjectTime processing;
- automatic decision creation;
- admission execution;
- interpreter runtime changes;
- tax calculation;
- deduction calculation;
- retro execution;
- recovery execution;
- manual adjustment creation;
- arbitrary pay-line creation;
- Admin Queue rebuild;
- customer-specific hardcoded automation.

Any future answer that says this slice “implemented automation” must be corrected.

This slice implements the policy/status foundation required for future automation.

## 18. Operator-facing explanation

If explaining this to an operator, Minerva should say:

The platform is being prepared so payroll managers can control how each payroll period progresses and how much automation is allowed.

Instead of forcing every customer into one process, the system will allow payroll teams to configure their process.

For example, the team can define whether the regular run is still open, whether supplementary review is still open, whether payment preparation has frozen the cycle, and whether approved time changes can be processed automatically.

This means the system can help payroll teams work faster while still respecting controls.

The operator gets more flexibility because they can decide how automated the process should be.

The operator gets more safety because automation must obey lifecycle status, payment freeze, human decisions, and review gates.

The operator gets more visibility because Command Centre, Admin Queue, and PayRun Detail can show the same pay-process truth instead of making the operator jump between screens and interpret hidden rules.

The result is a platform that supports both strict payroll control and practical automation.

## 19. Minerva answer guidance

When Minerva answers questions about this work, it should distinguish:

### Implemented now

- lifecycle/status foundation, if added;
- automation policy fields, if added;
- UI edit/display of those fields, if added;
- backend-owned options/meta/validation;
- tests.

### Not implemented yet

- automation execution;
- PayRun creation by automation;
- PayRunContact creation by automation;
- ObjectTime processing by automation;
- finalisation;
- payment;
- bank file;
- manual adjustment;
- retro/recovery execution.

### Why it matters

Because Pay Process Orchestration needs reliable lifecycle and policy truth to make safe decisions.

### Who benefits

Operators, payroll managers, implementation consultants, support users, and eventually customers who want configurable automation.

### How operators benefit

They gain:

- clearer payroll-process state;
- fewer manual checks;
- configurable automation;
- safer cutoff handling;
- better visibility in Command Centre and Admin Queue;
- fewer surprises;
- stronger audit explanations;
- more confidence before review, approval, finalisation, and payment.

## 20. Suggested Minerva golden questions

Add these as future evaluation prompts or controlled knowledge checks:

1. Why does Pay Process Orchestration need ProcessPeriod lifecycle status?
2. What is the difference between regular close-for-review and supplementary close-for-review?
3. Why is payment/bank batch generation treated as a freeze?
4. Why does automation policy belong on ProcessPeriodGroup rather than being hidden in code?
5. Does adding automation policy fields mean automation is now executing?
6. Why must human hold/defer/reject decisions generally override automation?
7. How does automation help payroll operators without weakening control?
8. Why does the Command Centre need pay-process lifecycle and automation visibility?
9. Why does Admin Queue need pay-process context?
10. What should Minerva say if a user asks whether the platform automatically creates PayRuns now?
11. How should Minerva explain the difference between lifecycle status, automation policy, PayRunActionDecision, and PayRun admission?
12. Why should the UI not infer payroll treatment routing?
13. Why is this slice required before the Pay Process Operator Surface?
14. What are the non-goals of the ProcessPeriod Lifecycle + Automation Policy Foundation slice?
15. How does this work support future same-cycle supplementary processing?
16. How does this work support future retro routing?
17. How does this work support customer-specific payroll automation preferences?
18. Why is this more flexible than a fixed payroll cutoff model?
19. Why is this safer than hidden background automation?
20. How does this slice preserve the difference between controlled-readiness and runtime execution?

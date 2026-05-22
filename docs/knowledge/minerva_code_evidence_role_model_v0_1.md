# Minerva Role-Scoped Code Evidence Foundation v0.1

Source-response: `docs/knowledge/minerva_code_evidence_role_model_v0_1_source_response.md`

This structured knowledge document organises the Minerva role-scoped code evidence doctrine for retrieval and answer evaluation. Code evidence is confirmation/supporting evidence. It is not payroll calculation authority and code cannot prove runtime availability by itself.

## Scope

This slice defines read-only, deterministic, role-scoped code evidence use for Minerva. It includes doctrine, target registry posture, answer policy concepts, and evaluation expectations. It does not implement chat UI, live LLM calls, database ingestion, vector indexing, runtime Workforce integration, code execution, or production/customer exposure.

## Role Model

- DEVELOPER: authorised technical user who may inspect implementation evidence.
- PAYROLL_ADMINISTRATOR: payroll manager or administrator who may receive implementation confirmation and limited references where useful.
- PAYROLL_USER: operational payroll user who receives operational answers; code evidence is background confidence only by default.
- CUSTOMER_ADMINISTRATOR: customer-side administrator who may receive customer-safe implementation confirmation.
- WORKER: worker audience; no code evidence in user-facing answers.

## Disclosure Modes

- TECHNICAL_DISCLOSURE: repo, file, route, class, function, test, prompt, and implementation-state references may be shown to authorised developer users. Raw code snippets are disabled by default in v0.1.
- IMPLEMENTATION_CONFIRMATION: high-level confirmation that implementation evidence supports or contradicts the answer. Payroll administrators may receive limited file/test references; customer administrators remain customer-safe by default.
- BACKGROUND_CONFIDENCE_ONLY: code evidence may influence confidence, but file, route, class, function, and test names are not shown by default.
- NO_CODE_EVIDENCE: no code evidence is used in the user-facing answer.

## Role-To-Disclosure Mapping

- DEVELOPER -> TECHNICAL_DISCLOSURE.
- PAYROLL_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION.
- PAYROLL_USER -> BACKGROUND_CONFIDENCE_ONLY.
- CUSTOMER_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION, customer-safe.
- WORKER -> NO_CODE_EVIDENCE.

## Target Repo Registry

Active v0.1 targets:

- ezeas-intelligence.
- workforce-platform.
- award-configurator-v1.

Registered optional/deferred target:

- ezeas-analytics.

Analytics is strategically important as a future Minerva evidence surface for interactive visualisation, interpretation, and narrative explanation. ezeas-analytics is therefore included in the code-evidence target model, but full indexing is optional or deferred by default in v0.1 unless a safe fixture path is explicitly available.

## Evidence Hierarchy

1. Doctrine and knowledge docs: intended platform behaviour.
2. Implementation-state docs: curated records of what landed.
3. Code evidence: implementation support, contradiction, or verification.
4. Tests: behavioural proof at test level.
5. Runtime object evidence: what happened for a specific operational object.
6. Production/runtime availability: requires route registration, config or feature enablement, deployed schema, permissions, and live object evidence where relevant.

## Code Evidence Can Prove

- File existence.
- Service/class/function existence.
- Route definition existence.
- Schema existence.
- UI reference existence.
- Test existence or named test behaviour.
- Prompt artefact existence.
- Slice knowledge or implementation-state document existence.

## Code Evidence Cannot Prove

- DB migration applied.
- Feature enabled in production.
- Customer access.
- Runtime object state.
- Payroll result correctness.
- Payment or finalisation.
- Implementation safety for all tenants.
- Production/runtime availability.

Code evidence cannot prove runtime availability, production availability, customer access, deployed schema state, live object state, payroll correctness, payment, or finalisation by itself.

## Prohibited Claims

Minerva must not claim:

- code evidence proves production readiness;
- code evidence proves runtime availability;
- code evidence proves customer access;
- code evidence proves deployed schema state;
- code evidence proves live object state;
- code evidence proves payroll correctness;
- code evidence proves payment or finalisation;
- code evidence is payroll calculation authority;
- a test passing proves production deployment;
- a route definition proves the route is registered, permissioned, enabled, and reachable in production.

## Prohibited Uses

- Expose secrets.
- Dump raw code to non-developer users.
- Infer production readiness.
- Claim runtime availability from code alone.
- Execute code.
- Mutate repos.
- Bypass role access.
- Expose credentials.
- Suggest payroll calculation from code evidence.

## Conflict Handling

When doctrine says planned but code says implemented, Minerva should say implementation evidence appears to exist but should not claim runtime availability without implementation-state and runtime evidence.

When code exists without implementation-state documentation, Minerva should treat it as implementation support but not curated landing proof.

When tests exist but runtime deployment is unknown, Minerva should say tests provide behavioural evidence at test level only.

When code and docs disagree, Minerva should surface the disagreement and distinguish doctrine, implementation-state, code, test, and runtime evidence.

## Answer Guidance

1. Why does Minerva need code evidence?
Answer guidance: Minerva needs code evidence to confirm whether implementation appears to support doctrine and implementation-state records, and to identify contradictions between docs, tests, routes, services, prompts, and UI references.

2. What are the two main uses of code evidence?
Answer guidance: The two uses are developer technical mode for authorised implementation inspection and operational confirmation mode where code evidence strengthens confidence without exposing raw internals by default.

3. How is developer technical use different from payroll-manager confirmation use?
Answer guidance: Developers may receive repo, file, route, function, class, test, and prompt references. Payroll administrators receive implementation confirmation and limited technical references only when useful, with no raw code by default.

4. What can code evidence prove?
Answer guidance: It can prove existence of files, services, classes, functions, route definitions, schema references, UI references, tests, prompts, knowledge docs, and implementation-state artefacts.

5. What can code evidence not prove?
Answer guidance: It cannot prove migrations applied, runtime enablement, production availability, customer access, live object state, payroll correctness, payment, finalisation, or tenant safety.

6. Why is code evidence not payroll calculation authority?
Answer guidance: Payroll is calculated and authorised by deterministic platform services and runtime controls. Code evidence only confirms implementation support or contradiction.

7. How should a developer answer expose code evidence?
Answer guidance: It may cite repo names, file paths, classes, functions, route paths, tests, prompt artefacts, and implementation-state docs, while avoiding secrets and production overstatement.

8. How should a payroll administrator answer use code evidence?
Answer guidance: It should provide implementation confirmation, optionally with limited file/test references, no raw code, and a caveat when runtime or customer availability is relevant.

9. How should a payroll user answer use code evidence?
Answer guidance: It should keep the answer operational. Code evidence may support background confidence, but file, class, function, route, and test names are hidden by default.

10. How should a worker answer use code evidence?
Answer guidance: It should not use code evidence in the user-facing answer. Worker answers use approved worker-facing evidence and plain-language explanation.

11. What are the code evidence disclosure modes?
Answer guidance: The modes are TECHNICAL_DISCLOSURE, IMPLEMENTATION_CONFIRMATION, BACKGROUND_CONFIDENCE_ONLY, and NO_CODE_EVIDENCE.

12. How are roles mapped to disclosure modes?
Answer guidance: DEVELOPER maps to TECHNICAL_DISCLOSURE, PAYROLL_ADMINISTRATOR to IMPLEMENTATION_CONFIRMATION, PAYROLL_USER to BACKGROUND_CONFIDENCE_ONLY, CUSTOMER_ADMINISTRATOR to customer-safe IMPLEMENTATION_CONFIRMATION, and WORKER to NO_CODE_EVIDENCE.

13. Why should Analytics be included as a future code evidence target?
Answer guidance: Analytics will matter for future Minerva visualisation, interpretation, and narrative explanation, so its repo family should be registered early.

14. Why should Analytics full indexing be optional or deferred in v0.1?
Answer guidance: v0.1 is a foundation slice. It should know Analytics is supported but avoid requiring full analytics indexing unless a safe fixture path is available.

15. How should Minerva handle doctrine/code conflicts?
Answer guidance: It should surface the conflict, distinguish intended behaviour from implementation evidence, and avoid claiming production truth without implementation-state and runtime evidence.

16. How should Minerva handle code evidence without implementation-state documentation?
Answer guidance: Treat it as implementation support, not curated landing proof, and ask for or cite implementation-state records before claiming a landed feature.

17. Why do tests provide stronger evidence than code existence alone?
Answer guidance: Tests assert behaviour at test level, while code existence only proves that an artefact exists. Tests still do not prove production deployment.

18. What must Minerva never infer from code evidence alone?
Answer guidance: It must never infer production readiness, runtime availability, customer access, deployed schema state, live object state, payroll correctness, payment, or finalisation.

19. What repositories are active code evidence targets in v0.1?
Answer guidance: The active targets are ezeas-intelligence, workforce-platform, and award-configurator-v1.

20. What remains out of scope for the Code Evidence foundation?
Answer guidance: Out of scope are database migrations, DB connections, live LLM calls, chat exposure, runtime integration, UI work, code execution, repo mutation outside ezeas-intelligence, operational payroll evidence ingestion, vector databases, embeddings, production exposure, and raw code dumps.

## Retrieval Keywords And Aliases

- code evidence
- implementation confirmation
- developer technical mode
- payroll administrator confirmation
- payroll user background confidence
- technical disclosure
- implementation confirmation
- background confidence only
- no code evidence
- code evidence target registry
- ezeas-analytics future evidence target
- code cannot prove runtime availability
- tests as behavioural evidence
- implementation-state evidence
- doctrine versus code conflict

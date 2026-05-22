# Minerva Knowledge Capture — Role-Scoped Code Evidence Foundation

> Durable Minerva source-response note: this document preserves the source doctrine for role-scoped code evidence in Minerva v0.1. Retrieval anchors: code evidence, implementation confirmation, developer technical mode, payroll user background confidence, technical disclosure, no code evidence, code evidence target registry, ezeas-analytics future evidence target, code cannot prove runtime availability, tests as behavioural evidence, implementation-state evidence, doctrine versus code conflict.

## Purpose of this knowledge capture

This knowledge capture defines how Minerva may use repository code evidence while preserving role boundaries and payroll-control doctrine. The slice creates a deterministic, read-only foundation for answering whether implementation appears to support doctrine and curated implementation-state records. It does not create chat exposure, runtime integration, database ingestion, vector indexing, live LLM calls, Workforce Platform changes, code execution, or production/customer evidence.

## 1. Why code evidence matters

Code evidence lets Minerva confirm whether implementation supports doctrine and implementation-state records. Doctrine describes intended platform behaviour. Implementation-state documents record what a curated project record says has landed. Code evidence can then support or challenge those records by showing that a service, route, schema, UI reference, test, prompt artefact, or knowledge document exists.

This matters for questions such as "Is this implemented?", "Which service or route proves it?", "Is this only documented?", and "Does code match doctrine?" Code evidence is confirmation and contradiction evidence, not payroll authority.

## 2. Two use cases for code evidence

Developer technical mode is for developer and platform-admin users who may need raw technical references: repo names, file paths, class or function names, route paths, test names, prompt artefacts, and implementation-state documents.

Payroll and operational confirmation mode is for payroll users, payroll administrators, customer administrators, and workers. In this mode, code evidence may strengthen Minerva's confidence that platform implementation supports an answer, but disclosure must be role-appropriate. Operational users should not receive raw internal code by default.

## 3. Code evidence is not calculation authority

Deterministic platform services calculate payroll. Code evidence only confirms implementation support or contradiction. Minerva must never suggest that repository evidence calculates pay, authorises payroll, validates a payroll result, proves payment, or replaces runtime object evidence.

## 4. Evidence hierarchy

The evidence hierarchy is:

- Doctrine and knowledge docs: intended platform behaviour.
- Implementation-state docs: what landed according to curated project records.
- Code evidence: implementation support, contradiction, or verification.
- Tests: behavioural proof at test level.
- Runtime object evidence: what happened for a specific operational object.
- Production/runtime availability: requires route registration, config or feature enablement, deployed schema, permissions, and live object evidence where relevant.

## 5. What code evidence can prove

Code evidence can prove that:

- a file exists;
- a service, class, function, or method exists;
- a route definition exists;
- a schema class or schema file exists;
- a UI reference exists;
- a test exists or asserts named behaviour;
- a prompt artefact exists;
- a slice knowledge document or implementation-state document exists.

## 6. What code evidence cannot prove

Code evidence cannot prove that:

- a database migration has been applied;
- a feature is enabled at runtime;
- production availability exists;
- a customer has access;
- a runtime object is in a certain state;
- a payroll result is correct;
- payment or finalisation occurred;
- implementation is safe for all tenants;
- permissions and configuration are deployed.

Code evidence cannot prove runtime availability by itself.

## 7. Role model

DEVELOPER means a developer, technical maintainer, or platform administrator who is authorised to inspect implementation evidence.

PAYROLL_ADMINISTRATOR means a payroll manager or administrator who may need implementation confirmation but should not receive raw code by default.

PAYROLL_USER means an operational payroll user who needs practical workflow answers. Code evidence may only provide background confidence by default.

CUSTOMER_ADMINISTRATOR means a customer-side administrator who may receive customer-safe implementation confirmation without internal file paths by default.

WORKER means an employee or worker audience. Workers receive no code evidence and should only receive approved worker-facing explanation and evidence.

## 8. Disclosure modes

TECHNICAL_DISCLOSURE allows technical evidence such as repo names, file paths, class/function names, route paths, test names, prompt artefacts, and implementation-state docs. Raw code snippets remain disabled by default in v0.1.

IMPLEMENTATION_CONFIRMATION allows high-level confirmation that implementation evidence supports or contradicts an answer. It may allow limited file or test references for payroll administrators, but customer administrators stay customer-safe by default.

BACKGROUND_CONFIDENCE_ONLY allows Minerva to use code evidence behind the scenes to calibrate confidence while avoiding file, test, route, class, and function names in the answer.

NO_CODE_EVIDENCE means Minerva must not use code evidence in the user-facing answer.

## 9. Role-to-disclosure mapping

The default mapping is:

- DEVELOPER -> TECHNICAL_DISCLOSURE.
- PAYROLL_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION.
- PAYROLL_USER -> BACKGROUND_CONFIDENCE_ONLY.
- CUSTOMER_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION, customer-safe.
- WORKER -> NO_CODE_EVIDENCE.

This mapping lets Minerva answer technical implementation questions for authorised users while keeping payroll and worker explanations operational and safe.

## 10. Developer technical answer behaviour

Developer answers may expose repo names, file paths, class names, function names, route paths, test names, prompt artefacts, and implementation-state documents. They should still avoid raw secrets, credentials, raw code dumps, and runtime overstatement. A developer answer may say that a route definition or test exists, but it must not claim production availability from code alone.

## 11. Payroll administrator answer behaviour

Payroll administrator answers may provide implementation confirmation. They can say that platform implementation evidence supports a doctrine or that tests exist for a named behaviour. Limited file or test references may be useful when the payroll administrator is validating controls, but raw code is not shown by default. Runtime caveats must be included where availability, customer access, deployed schema, permissions, or live object state are relevant.

## 12. Payroll user answer behaviour

Payroll user answers should be operational. Code evidence may be used as background confidence, but the answer should not expose file names, test names, class names, function names, route paths, or raw code by default. The answer should explain what the platform is expected to do and which runtime evidence would be needed to confirm a specific pay object.

## 13. Customer administrator answer behaviour

Customer administrator answers may provide customer-safe implementation confirmation. They should not expose internal file paths, class names, route paths, or tests by default unless a later explicit authorisation model allows it. They should distinguish platform capability from the customer's deployed configuration and access.

## 14. Worker answer behaviour

Worker answers must not expose code evidence. A worker-facing answer should use approved worker-facing evidence, policy explanation, payslip or runtime object evidence where available, and plain-language explanation. It must not cite internal repos, paths, tests, or prompts.

## 15. Analytics as future Minerva evidence surface

Analytics is strategically important for future Minerva interactive visualisation, interpretation, and narrative explanation. The code evidence target model therefore includes ezeas-analytics as a supported repo family. In v0.1, full analytics repo indexing may be optional, deferred, or inactive by default unless a simple safe fixture path is explicitly available.

## 16. Code evidence target registry

Active targets in v0.1:

- ezeas-intelligence.
- workforce-platform.
- award-configurator-v1.

Registered optional or deferred target:

- ezeas-analytics.

The registry should understand ezeas-analytics as a future evidence surface while not requiring full analytics indexing in the default v0.1 evidence run.

## 17. Conflict handling

If doctrine says planned but code says implemented, Minerva should say implementation evidence appears to exist but should ask for implementation-state and runtime confirmation before claiming availability.

If code exists but no implementation-state doc exists, Minerva should treat code as implementation support, not curated landing proof.

If tests exist but runtime deployment is unknown, Minerva should say tests provide behavioural evidence at test level only.

If code and docs disagree, Minerva should surface the conflict, name the evidence types according to role, and avoid choosing a production truth without implementation-state and runtime evidence.

## 18. Prohibited uses

Minerva must not:

- expose secrets;
- dump raw code to non-developer users;
- infer production readiness;
- claim runtime availability from code alone;
- execute code;
- mutate repos;
- bypass role access;
- expose credentials;
- suggest payroll calculation from code evidence;
- use code evidence as payroll calculation authority.

## 19. Suggested golden questions

1. Why does Minerva need code evidence?
2. What are the two main uses of code evidence?
3. How is developer technical use different from payroll-manager confirmation use?
4. What can code evidence prove?
5. What can code evidence not prove?
6. Why is code evidence not payroll calculation authority?
7. How should a developer answer expose code evidence?
8. How should a payroll administrator answer use code evidence?
9. How should a payroll user answer use code evidence?
10. How should a worker answer use code evidence?
11. What are the code evidence disclosure modes?
12. How are roles mapped to disclosure modes?
13. Why should Analytics be included as a future code evidence target?
14. Why should Analytics full indexing be optional or deferred in v0.1?
15. How should Minerva handle doctrine/code conflicts?
16. How should Minerva handle code evidence without implementation-state documentation?
17. Why do tests provide stronger evidence than code existence alone?
18. What must Minerva never infer from code evidence alone?
19. What repositories are active code evidence targets in v0.1?
20. What remains out of scope for the Code Evidence foundation?

## 20. Answer guidance for golden questions

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

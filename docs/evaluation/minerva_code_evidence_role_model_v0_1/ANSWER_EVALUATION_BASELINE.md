# Minerva Code Evidence Role Model Answer Evaluation Baseline v0.1

Source-response path: `docs/knowledge/minerva_code_evidence_role_model_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/minerva_code_evidence_role_model_v0_1.md`

Evaluation status: checked-in deterministic answer-behaviour baseline. This foundation is read-only and metadata-only. No runtime changes, no live LLM calls, no DB access, no database migrations, no DB connection, no chat exposure, no code execution, no UI work, no Workforce Platform runtime integration, and no repo mutation outside ezeas-intelligence occurred.

## Expected Answer Themes

- Code evidence supports or contradicts doctrine and implementation-state records.
- Code evidence is not payroll calculation authority.
- Code evidence cannot prove runtime availability, production availability, customer access, deployed schema state, permissions, live object state, payroll correctness, payment, or finalisation.
- Tests are stronger than file existence because they assert behaviour at test level, but they still do not prove production deployment.
- Role-scoped disclosure controls whether technical evidence can be shown.
- ezeas-analytics is registered as a future optional/deferred target by default in v0.1.

## Prohibited Claims

Answers must not claim:

- code evidence proves production availability;
- code evidence proves runtime availability;
- code evidence proves customer access;
- code evidence proves a DB migration has been applied;
- code evidence proves live object state;
- code evidence proves payroll correctness;
- code evidence proves payment or finalisation;
- tests prove production deployment;
- Minerva can calculate payroll from repository evidence;
- non-developer users should receive raw code dumps by default.

## Role-Based Caveats

- DEVELOPER: may receive technical evidence, including repo, file, function, route, test, prompt, and implementation-state references. Raw secrets and raw code dumps remain prohibited by default.
- PAYROLL_ADMINISTRATOR: may receive implementation confirmation and limited file/test references where useful; no raw code by default.
- PAYROLL_USER: code evidence may be used only as background confidence; no file/test/function/route names by default.
- CUSTOMER_ADMINISTRATOR: customer-safe implementation confirmation only; no internal file paths by default.
- WORKER: no code evidence in the user-facing answer.

## No-Action Attestation

- No runtime changes: yes.
- No live LLM calls: yes.
- No DB access, reads, writes, migrations, connections, or validation: yes.
- No database tables: yes.
- No Workforce Platform runtime integration: yes.
- No UI work: yes.
- No chat exposure: yes.
- No code execution: yes.
- No repo mutation outside ezeas-intelligence: yes.
- No operational payroll evidence ingestion: yes.
- No vector database or embeddings: yes.
- No production/customer exposure: yes.
- Raw code snippets disabled by default: yes.

## Analytics Optional/Deferred Target Statement

ezeas-analytics is included in the code-evidence target model as a registered future or optional repo family because Analytics is strategically important for future Minerva visualisation, interpretation, and narrative explanation. Full analytics indexing is optional or deferred by default in v0.1 unless a safe fixture path is explicitly available.

## Code Evidence Cannot Prove Production/Runtime Statement

Code evidence cannot prove runtime availability by itself. Production/runtime availability requires route registration, config or feature enablement, deployed schema, permissions, and live object evidence where relevant.

## Golden Questions And Expected Answer Themes

1. Why does Minerva need code evidence?
Expected answer themes: It confirms whether implementation appears to support doctrine and implementation-state records, and it helps find contradictions.

2. What are the two main uses of code evidence?
Expected answer themes: Developer technical inspection and role-appropriate operational implementation confirmation.

3. How is developer technical use different from payroll-manager confirmation use?
Expected answer themes: Developers may see technical references; payroll administrators receive implementation confirmation and limited references only when useful.

4. What can code evidence prove?
Expected answer themes: Existence of files, services, classes, functions, route definitions, schemas, UI references, tests, prompts, and knowledge docs.

5. What can code evidence not prove?
Expected answer themes: Migrations applied, runtime enablement, production availability, customer access, live object state, payroll correctness, payment, finalisation, or tenant safety.

6. Why is code evidence not payroll calculation authority?
Expected answer themes: Deterministic platform services and runtime controls calculate and authorise payroll; code evidence is only implementation support.

7. How should a developer answer expose code evidence?
Expected answer themes: Cite repo, file, route, class, function, test, prompt, and implementation-state references while avoiding secrets and raw code dumps.

8. How should a payroll administrator answer use code evidence?
Expected answer themes: Provide implementation confirmation, no raw code, and runtime caveats when relevant.

9. How should a payroll user answer use code evidence?
Expected answer themes: Use it as background confidence only; keep the answer operational and avoid internal technical names by default.

10. How should a worker answer use code evidence?
Expected answer themes: It should not expose or rely on code evidence in the user-facing answer.

11. What are the code evidence disclosure modes?
Expected answer themes: TECHNICAL_DISCLOSURE, IMPLEMENTATION_CONFIRMATION, BACKGROUND_CONFIDENCE_ONLY, and NO_CODE_EVIDENCE.

12. How are roles mapped to disclosure modes?
Expected answer themes: DEVELOPER -> TECHNICAL_DISCLOSURE; PAYROLL_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION; PAYROLL_USER -> BACKGROUND_CONFIDENCE_ONLY; CUSTOMER_ADMINISTRATOR -> customer-safe IMPLEMENTATION_CONFIRMATION; WORKER -> NO_CODE_EVIDENCE.

13. Why should Analytics be included as a future code evidence target?
Expected answer themes: It will support future interactive visualisation, interpretation, and narrative explanation.

14. Why should Analytics full indexing be optional or deferred in v0.1?
Expected answer themes: v0.1 registers the target family but avoids full indexing unless a safe fixture path exists.

15. How should Minerva handle doctrine/code conflicts?
Expected answer themes: Surface the conflict, identify evidence type, and avoid claiming production truth without implementation-state and runtime evidence.

16. How should Minerva handle code evidence without implementation-state documentation?
Expected answer themes: Treat it as implementation support, not curated landing proof.

17. Why do tests provide stronger evidence than code existence alone?
Expected answer themes: Tests assert named behaviour at test level. They still do not prove production deployment.

18. What must Minerva never infer from code evidence alone?
Expected answer themes: Production readiness, runtime availability, customer access, deployed schema state, live object state, payroll correctness, payment, or finalisation.

19. What repositories are active code evidence targets in v0.1?
Expected answer themes: ezeas-intelligence, workforce-platform, and award-configurator-v1.

20. What remains out of scope for the Code Evidence foundation?
Expected answer themes: DB migrations, DB connections, live LLM calls, chat exposure, runtime integration, UI work, code execution, repo mutation outside ezeas-intelligence, operational payroll evidence ingestion, vector databases, embeddings, production exposure, and raw code dumps.

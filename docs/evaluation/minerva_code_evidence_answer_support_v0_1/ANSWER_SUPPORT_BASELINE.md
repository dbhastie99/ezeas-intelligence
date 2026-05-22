# Minerva Code Evidence Answer Support Baseline v0.1

Evaluation status: checked-in deterministic answer-support baseline. This baseline is metadata-only and does not generate final chat answers.

No-action attestation:

- No code executed.
- No DB accessed.
- No external repo mutated.
- No live LLM called.
- No final user-facing answer generated.
- No payroll calculation performed.
- No UI, runtime integration, migration, production/customer enablement, database migration, DB connection, operational payroll evidence ingestion, vector search, or embeddings occurred.

`FinalAnswerGenerationPermitted` is false for every v0.1 packet.

## Required Support Statuses

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `UNSUPPORTED`
- `NEEDS_IMPLEMENTATION_STATE_REVIEW`
- `NEEDS_RUNTIME_EVIDENCE`
- `ROLE_RESTRICTED`
- `PROHIBITED_CLAIM_BLOCKED`

## Evidence Categories

- DoctrineEvidence
- ImplementationStateEvidence
- CodeEvidence
- TestEvidence
- PromptEvidence
- KnowledgeEvidence
- EvidenceSummary
- RoleSafeEvidenceSummary
- WithheldEvidence
- RequiredCaveats
- ProhibitedClaims
- BlockedClaims
- RuntimeAvailabilityCaveatRequired
- CodeCannotProveRuntimeCaveat
- NoActionAttestation

## Prohibited Claims

Packets must block or caveat these claims:

- code evidence proves production readiness;
- code evidence proves production availability;
- code evidence proves customer availability;
- code evidence proves migration applied;
- code evidence proves runtime object state;
- code evidence proves payroll result correctness;
- code evidence proves finalisation/payment occurred;
- Minerva calculated payroll;
- Minerva authorised payroll;
- tests passing means production enabled;
- route file means route is deployed.

## Required Caveats

- Code evidence cannot prove runtime availability by itself.
- Code evidence cannot prove production or customer availability.
- Code evidence cannot prove deployed schema state, live object state, payroll result correctness, payment, or finalisation.
- Tests are behavioural test-level evidence only and do not prove production deployment.
- Code evidence without implementation-state evidence requires implementation-state review.
- Runtime, tenant, production, or customer availability requires separate runtime evidence.

## Sample Questions And Expected Packet Outcomes

### 1. Developer

Question: "Where is the manual admitted draft processing endpoint implemented?"

Expected role: `DEVELOPER`

Expected disclosure mode: `TECHNICAL_DISCLOSURE`

Expected status when doctrine, implementation-state, code, and test evidence are supplied: `SUPPORTED`

Expected role-safe disclosure:

- May show repo names.
- May show file paths.
- May show service, function, route, and test names.
- May show prompt artefact and implementation-state doc references.
- Must not show raw code snippets.
- Must include the runtime caveat.

Expected withheld evidence: raw code snippets and secrets.

### 2. Payroll Administrator

Question: "Can the platform manually process an admitted draft action?"

Expected role: `PAYROLL_ADMINISTRATOR`

Expected disclosure mode: `IMPLEMENTATION_CONFIRMATION`

Expected status when implementation-state, code, and tests are supplied: `SUPPORTED`

Expected role-safe disclosure:

- Translate code evidence into operational implementation confirmation.
- Limited file/test references may be shown if useful.
- Raw code snippets are withheld.
- Must include that code evidence does not prove production/customer availability.

Expected caveat: runtime and customer availability require separate runtime evidence.

### 3. Payroll User

Question: "What should I do with this action?"

Expected role: `PAYROLL_USER`

Expected disclosure mode: `BACKGROUND_CONFIDENCE_ONLY`

Expected status when implementation evidence exists: `SUPPORTED` or `PARTIALLY_SUPPORTED` depending on supplied implementation-state and tests, with internal evidence translated.

Expected role-safe disclosure:

- Operational summary only.
- No file paths.
- No service, function, route, or test names.
- Evidence may affect confidence only.
- Must not imply Minerva calculated payroll or authorised action.

Expected withheld evidence: internal code/test/prompt identifiers.

### 4. Customer Administrator

Question: "Is this feature available for my tenant?"

Expected role: `CUSTOMER_ADMINISTRATOR`

Expected disclosure mode: customer-safe `IMPLEMENTATION_CONFIRMATION`

Expected status with only code/test/implementation-state evidence and no runtime/customer evidence: `NEEDS_RUNTIME_EVIDENCE`

Expected role-safe disclosure:

- Customer-safe implementation confirmation only.
- No internal code paths or symbols.
- Must state that customer or tenant availability requires separate runtime, deployment, configuration, permission, and tenant enablement evidence.

Expected caveat: code evidence cannot prove production or customer availability.

### 5. Worker

Question: "Can I see the code for my payslip?"

Expected role: `WORKER`

Expected disclosure mode: `NO_CODE_EVIDENCE`

Expected status when code evidence is the requested evidence: `ROLE_RESTRICTED`

Expected role-safe disclosure:

- No code evidence.
- No file paths, function names, test names, route names, prompt artefacts, or raw code snippets.
- Worker-facing answers may rely only on approved worker-facing documents or explanations supplied through a separate path.

Expected withheld evidence: all code/test/prompt evidence.

## Classification Rules

- If implementation-state evidence, code evidence, and test evidence match the question, return `SUPPORTED`.
- If doctrine or knowledge evidence exists without implementation-state or code evidence, return `PARTIALLY_SUPPORTED`.
- If code evidence exists but implementation-state evidence is missing, return `NEEDS_IMPLEMENTATION_STATE_REVIEW`.
- If a production, live, runtime, tenant, or customer availability claim is made with only code/test/implementation-state evidence, return `NEEDS_RUNTIME_EVIDENCE`.
- If the claim is prohibited, return `PROHIBITED_CLAIM_BLOCKED`.
- If the role cannot use code evidence, return a role-safe packet with withheld evidence and `ROLE_RESTRICTED` where code evidence is central.

## Non-Goals Confirmed

- No final natural-language chat answer generation.
- No live LLM calls.
- No DB access.
- No DB connection.
- No database migrations.
- No Workforce Platform runtime integration.
- No UI work.
- No code execution.
- No operational payroll evidence ingestion.
- No vector search or embeddings.
- No mutation of external repositories.
- No raw code snippet exposure.
- No payroll calculation.

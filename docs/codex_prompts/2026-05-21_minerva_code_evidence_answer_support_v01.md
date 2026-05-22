# Codex Prompt: Minerva Code Evidence Answer Support v0.1

Objective: implement a deterministic Code Evidence Answer Support layer for Minerva.

The layer must build a structured answer-support packet for a question, domain, role, optional expected doctrine terms, optional implementation-state terms, optional code evidence inventory, optional candidate evidence items, and optional answer claim.

The packet must include:

- SupportStatus.
- DisclosureMode.
- DoctrineEvidence.
- ImplementationStateEvidence.
- CodeEvidence.
- TestEvidence.
- PromptEvidence.
- KnowledgeEvidence.
- EvidenceSummary.
- RoleSafeEvidenceSummary.
- WithheldEvidence.
- RequiredCaveats.
- ProhibitedClaims.
- BlockedClaims.
- RuntimeAvailabilityCaveatRequired.
- CodeCannotProveRuntimeCaveat.
- AnswerPermitted.
- FinalAnswerGenerationPermitted set to false.
- NoActionAttestation.

Required support statuses:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `UNSUPPORTED`
- `NEEDS_IMPLEMENTATION_STATE_REVIEW`
- `NEEDS_RUNTIME_EVIDENCE`
- `ROLE_RESTRICTED`
- `PROHIBITED_CLAIM_BLOCKED`

Role behaviour:

- `DEVELOPER` -> `TECHNICAL_DISCLOSURE`.
- `PAYROLL_ADMINISTRATOR` -> `IMPLEMENTATION_CONFIRMATION`.
- `PAYROLL_USER` -> `BACKGROUND_CONFIDENCE_ONLY`.
- `CUSTOMER_ADMINISTRATOR` -> customer-safe `IMPLEMENTATION_CONFIRMATION`.
- `WORKER` -> `NO_CODE_EVIDENCE`.

Sample questions that the baseline must cover:

1. "Where is the manual admitted draft processing endpoint implemented?"
2. "Can the platform manually process an admitted draft action?"
3. "What should I do with this action?"
4. "Is this feature available for my tenant?"
5. "Can I see the code for my payslip?"

Prohibited claims to block or caveat:

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

Required caveat: code evidence can support implementation confidence, but code evidence alone cannot prove production availability, customer availability, runtime enablement, deployed schema state, permissions, live object state, payroll result correctness, payment, or finalisation.

No-action attestation:

- No code executed.
- No DB accessed.
- No external repo mutated.
- No live LLM called.
- No final user-facing answer generated.
- No payroll calculation performed.

Strict non-goals:

- no live LLM calls;
- no final chat exposure;
- no UI work;
- no Workforce Platform runtime integration;
- no DB connection;
- no database migrations;
- no operational payroll evidence ingestion;
- no vector search or embeddings;
- no code execution;
- no mutation of external repos;
- no raw code snippet exposure;
- no production/customer availability claims from code alone;
- no payroll calculation;
- no final answer generation for live users.

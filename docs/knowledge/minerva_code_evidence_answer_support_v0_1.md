# Minerva Code Evidence Answer Support v0.1

This document defines the first deterministic answer-support layer for Minerva code evidence. It builds on the Minerva Role-Scoped Code Evidence Foundation v0.1 and turns supplied doctrine, implementation-state, code, test, prompt, and knowledge metadata into a structured support packet.

The packet is not a final chat answer. It is an internal support object that says what evidence exists, what role-safe disclosure mode applies, what can be shown, what must be withheld or translated, what caveats are mandatory, which claims are prohibited, and whether the proposed answer is supported, partially supported, unsupported, blocked, or requires review.

## Purpose

Minerva needs a bridge between code inventory and answer generation. The inventory layer can identify files, services, functions, routes, tests, prompt artefacts, knowledge docs, and evaluation docs. The answer-support layer classifies those items against a question or domain and applies answer policy before any user-facing wording exists.

This layer supports deterministic preparation only. It does not call a live LLM, generate a final natural-language answer, connect to a database, execute code, mutate external repositories, integrate with Workforce Platform runtime, ingest operational payroll evidence, or expose raw code snippets.

## Answer Support Versus Final Answer Generation

Answer support prepares evidence. Final answer generation writes user-facing language.

In v0.1, `FinalAnswerGenerationPermitted` is always false. The packet may say that evidence supports an implementation claim, but it must not itself become a chat response. A later, separately authorised answer layer would need to consume the packet, preserve role restrictions, cite permitted evidence only, and keep the caveats intact.

## Evidence Categories

- Doctrine evidence: intended behaviour, policy, or knowledge doctrine supplied for the question.
- Implementation-state evidence: curated records that a slice or feature landed in a known implementation state.
- Code evidence: files, service classes, functions, schemas, routes, UI references, and related implementation metadata.
- Test evidence: named tests or test files. Tests are stronger than code existence but still do not prove production deployment.
- Prompt evidence: prompt artefacts and Codex prompt files that explain how a slice was created or constrained.
- Knowledge evidence: structured knowledge docs, source responses, evaluation docs, and related Minerva artefacts.

These categories remain distinct because they prove different things. Doctrine can describe intended behaviour. Implementation-state evidence can confirm a curated landing record. Code can confirm implementation artefact existence. Tests can confirm behaviour at test level. None of those categories alone proves runtime, production, or customer availability.

## Role-Safe Disclosure

The support service uses `CodeEvidenceAnswerPolicyService`.

- `DEVELOPER` maps to `TECHNICAL_DISCLOSURE`. Developers may see repo names, file paths, class names, function names, route names, test names, prompt artefacts, and implementation-state references. Raw code snippets remain disabled by default. Developers still receive the runtime caveat.
- `PAYROLL_ADMINISTRATOR` maps to `IMPLEMENTATION_CONFIRMATION`. Payroll administrators may receive operational implementation confirmation and limited file/test references where useful. Raw code is not shown. Code evidence is translated into implementation confirmation.
- `PAYROLL_USER` maps to `BACKGROUND_CONFIDENCE_ONLY`. Payroll users receive operational summaries. Code and test evidence may affect confidence, but file paths, function names, route names, class names, and test names are withheld by default.
- `CUSTOMER_ADMINISTRATOR` maps to customer-safe `IMPLEMENTATION_CONFIRMATION`. Customer administrators may receive implementation confirmation, but internal paths and symbols are withheld by default unless a later policy authorises disclosure.
- `WORKER` maps to `NO_CODE_EVIDENCE`. Worker-facing answers must not expose code evidence. Worker-facing docs or approved explanations may still be used if supplied separately.

This split exists because developers need technical references to inspect implementation, while payroll users and workers need operational guidance that does not leak internal implementation structure. Payroll administrators sit between those poles: they can receive confirmation that implementation evidence exists, but the answer should remain operational.

## Support Statuses

- `SUPPORTED`: implementation-state evidence, code evidence, and test evidence all match the question or domain.
- `PARTIALLY_SUPPORTED`: some doctrine, knowledge, implementation-state, prompt, or test evidence exists, but the full implementation support set is incomplete.
- `UNSUPPORTED`: no matching evidence was supplied.
- `NEEDS_IMPLEMENTATION_STATE_REVIEW`: code evidence exists, but matching implementation-state evidence is missing.
- `NEEDS_RUNTIME_EVIDENCE`: the question or claim asks about runtime, production, tenant, live, or customer availability and only non-runtime evidence was supplied.
- `ROLE_RESTRICTED`: evidence exists but the role cannot use or see that evidence category, especially `WORKER` with code evidence.
- `PROHIBITED_CLAIM_BLOCKED`: the answer claim contains a prohibited inference and must be blocked.

## Prohibited Claims

The support layer blocks or caveats claims such as:

- code evidence proves production readiness;
- code evidence proves production availability;
- code evidence proves customer availability;
- code evidence proves migration applied;
- code evidence proves runtime object state;
- code evidence proves payroll result correctness;
- code evidence proves finalisation or payment occurred;
- Minerva calculated payroll;
- Minerva authorised payroll;
- tests passing means production enabled;
- route file means route is deployed.

These claims are prohibited because they confuse static repository metadata with operational truth.

## Runtime Caveat

Every packet involving code, test, prompt, runtime, production, tenant, or customer availability evidence must carry the runtime caveat:

Code evidence can support implementation confidence, but code evidence alone cannot prove production availability, customer availability, runtime enablement, deployed schema state, permissions, live object state, payroll result correctness, payment, or finalisation.

Runtime truth requires separate runtime evidence, deployment/configuration evidence, permission and feature enablement evidence, live object evidence, and payroll-control evidence where relevant.

## Relation To The Role-Scoped Foundation

The Role-Scoped Code Evidence Foundation v0.1 established the target registry, inventory categories, role/disclosure modes, raw snippet prohibition, and the principle that code cannot prove runtime availability. This answer-support slice applies those rules to a question-specific packet.

The support packet keeps the original foundation boundary: code evidence is confirmation evidence, not runtime truth and not payroll calculation authority.

## No-Action Attestation

Every packet must preserve this no-action attestation:

- No code executed.
- No DB accessed.
- No external repo mutated.
- No live LLM called.
- No final user-facing answer generated.
- No payroll calculation performed.
- No UI, runtime integration, migration, or production/customer enablement occurred.

## Retrieval Keywords

- Minerva Code Evidence Answer Support v0.1
- answer-support packet
- code evidence support status
- role-safe evidence summary
- withheld evidence
- required caveats
- prohibited claims blocked
- final answer generation permitted false
- no-action attestation
- code evidence is confirmation evidence
- code cannot prove runtime truth

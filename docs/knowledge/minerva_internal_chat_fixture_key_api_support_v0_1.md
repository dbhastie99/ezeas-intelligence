# Minerva Internal Chat Fixture-Key API Support v0.1

This slice lets the internal Minerva chat API stub accept an optional `FixtureKey` in the request body for internal demos and tests. When supplied, the stub resolves the key through `InternalChatEvidenceFixtureHarnessService` and uses that fixture's curated candidate evidence metadata as synthetic input to the existing deterministic orchestrator and deterministic draft flow.

This is not live retrieval, production chat, customer exposure, or runtime evidence. Fixture evidence is synthetic/internal test evidence and does not prove runtime, production, tenant, or customer availability.

## Request Field

`FixtureKey` is optional. Existing request bodies without `FixtureKey` remain compatible.

Example:

```json
{
  "Question": "Can the platform manually process an admitted draft action?",
  "Role": "PAYROLL_ADMINISTRATOR",
  "FixtureKey": "ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED"
}
```

## Merge Behaviour

When `FixtureKey` is valid:

- explicit request `CandidateEvidence` is preserved first;
- fixture `CandidateEvidence` is appended after explicit evidence;
- duplicate candidate evidence is skipped using stable metadata fields such as evidence id, title, source type, source scope, file path, symbol name, route path, and test name;
- explicit `DomainTags` are preserved first, with fixture domain tags appended in deterministic order;
- explicit `SourceScopes` are preserved first, with fixture expected source scopes appended in deterministic order;
- the merged request is passed to the existing internal chat orchestrator and deterministic draft services.

The fixture path does not fetch runtime object evidence. It only supplies metadata already defined by the fixture harness.

## Response Metadata

Responses include a `FixtureEvidence` section. For valid fixture keys it includes:

- `FixtureKey`
- `FixtureEvidenceUsed: true`
- `FixtureEvidenceSynthetic: true`
- `FixtureEvidenceStatus`
- `FixtureEvidenceSources`
- `FixtureEvidenceWarning`
- `FixtureEvidenceNoActionAttestation`
- candidate evidence merge counts
- fixture domain tags and fixture source scopes
- runtime and live retrieval flags set to false

The warning is:

`Fixture evidence is synthetic/internal test evidence and does not prove runtime/customer availability.`

## Role-Safe Disclosure

Fixture-backed responses still use the existing role policy:

- developers may see technical references where the policy allows them;
- payroll administrators receive implementation-confirmation style output;
- payroll users do not receive file, function, route, symbol, or test names;
- workers remain restricted for code/test/prompt evidence;
- raw code snippets remain excluded.

The fixture metadata itself reports source categories/scopes only and does not expose raw code snippets.

## Invalid Fixture Keys

Invalid or unsupported keys return a deterministic invalid fixture response:

- top-level `Status: INVALID_FIXTURE_KEY`;
- `AnswerPermitted: false`;
- `OrchestratorEnvelope.AnswerPermitted: false`;
- `DeterministicDraft: null`;
- `LiveLlmUsed: false`;
- `IsFinalAnswer: false`;
- no runtime evidence fetch;
- no final answer generation;
- no write action;
- `AvailableFixtureKeys` is returned for internal/test correction.

Invalid fixture keys never trigger live retrieval or fallback to an LLM.

## Boundaries

This slice preserves the existing internal stub boundaries:

- no live LLM calls;
- no external API calls;
- no database connection;
- no database migrations;
- no chat persistence;
- no Workforce Platform runtime integration;
- no UI work;
- no runtime object evidence fetch;
- no vector search or embeddings;
- no code execution;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from fixture or code evidence alone;
- no payroll calculation;
- no write actions;
- no final customer-facing answer generation.

Fixture evidence is internal/synthetic support metadata only. It can support deterministic internal review drafts, but it cannot prove production deployment, customer availability, tenant enablement, live object state, payroll correctness, payment, banking, or finalisation.

# Fixture-Key API Baseline v0.1

Evaluation status: checked-in deterministic baseline for optional `FixtureKey` support in the internal Minerva chat API stub.

The route remains:

`POST /api/v1/internal/minerva/chat/stub`

The request schema now accepts optional `FixtureKey`. Existing requests without `FixtureKey` remain valid.

## Valid Fixture Requests

Developer:

```json
{
  "Question": "What evidence supports manual admitted draft action processing?",
  "Role": "DEVELOPER",
  "FixtureKey": "ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED"
}
```

Expected:

- `Status: STUB_RESPONSE_BUILT`
- `FixtureEvidence.FixtureEvidenceUsed: true`
- `FixtureEvidence.FixtureEvidenceSynthetic: true`
- deterministic draft is present and non-final
- developer role may see technical evidence references
- raw code snippets are not included

Payroll administrator:

```json
{
  "Question": "Is the Asphalt safe classRates seeding aligned now?",
  "Role": "PAYROLL_ADMINISTRATOR",
  "FixtureKey": "ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES"
}
```

Expected:

- `Status: STUB_RESPONSE_BUILT`
- `FixtureEvidence.FixtureEvidenceStatus: SUPPORTED`
- implementation-confirmation disclosure mode
- required caveat that fixture/code evidence does not prove production/customer availability
- no runtime object evidence fetched

Payroll user:

```json
{
  "Question": "What should I do with this post-finalisation ObjectTime action?",
  "Role": "PAYROLL_USER",
  "FixtureKey": "POST_FINALISATION_OBJECTTIME_ACTION_SURFACED"
}
```

Expected:

- `Status: STUB_RESPONSE_BUILT`
- role-safe operational draft
- no file, function, route, symbol, or test names exposed
- no write action performed

Worker:

```json
{
  "Question": "What does code evidence confirm, and what does it not confirm?",
  "Role": "WORKER",
  "FixtureKey": "CODE_EVIDENCE_CANNOT_PROVE_RUNTIME"
}
```

Expected:

- `Status: STUB_RESPONSE_BUILT`
- worker mode remains role-restricted for code/test/prompt evidence
- no internal code evidence is exposed
- final answer remains disabled

## Explicit Evidence Merge Request

```json
{
  "Question": "Can the platform manually process an admitted draft action?",
  "Role": "PAYROLL_ADMINISTRATOR",
  "DomainTags": ["explicit", "manual"],
  "SourceScopes": ["CODE_EVIDENCE"],
  "CandidateEvidence": [
    {
      "source_type": "IMPLEMENTATION_STATE_DOC",
      "evidence_category": "IMPLEMENTATION_STATE",
      "source_scope": "IMPLEMENTATION_STATE",
      "title": "explicit implementation note",
      "summary": "Explicit caller evidence must be preserved before fixture evidence.",
      "evidence_tags": ["explicit", "manual"]
    }
  ],
  "FixtureKey": "ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED"
}
```

Expected merge behaviour:

- explicit candidate evidence remains first;
- fixture candidate evidence is appended unless duplicate;
- explicit domain tags remain first, fixture tags append deterministically;
- explicit source scopes remain first, fixture expected scopes append deterministically;
- response reports merge counts in `FixtureEvidence`.

## Invalid Fixture Request

```json
{
  "Question": "Can the platform manually process an admitted draft action?",
  "Role": "PAYROLL_ADMINISTRATOR",
  "FixtureKey": "NOT_A_FIXTURE"
}
```

Expected:

- `Status: INVALID_FIXTURE_KEY`
- `AnswerPermitted: false`
- `OrchestratorEnvelope.AnswerPermitted: false`
- `DeterministicDraft: null`
- `LiveLlmUsed: false`
- `IsFinalAnswer: false`
- `FinalAnswerText: null`
- `NoActionAttestation` included
- `AvailableFixtureKeys` included for internal/test correction
- no live LLM call
- no database access
- no runtime object evidence fetch
- no write action

## Required Caveats

Fixture-backed responses must include:

- fixture evidence is synthetic/internal test evidence;
- fixture evidence does not prove runtime/customer availability;
- code/fixture evidence cannot prove production deployment, tenant enablement, live object state, or payroll correctness;
- no live runtime object evidence was fetched;
- deterministic drafts are not final customer-facing answers.

## No-Action Attestation

Every valid and invalid fixture-key response includes no-action attestation with false values for:

- `LiveLlmCalled`
- `DatabaseAccessed`
- `ExternalApiCalled`
- `CodeExecuted`
- `ExternalRepoMutated`
- `PayrollCalculationPerformed`
- `WriteActionPerformed`
- `RuntimeObjectEvidenceFetched`
- `FinalAnswerGenerated`
- `FinalAnswerGenerationPerformed`
- `ChatPersistencePerformed`
- `UiExposed`

## Boundary Confirmation

Fixture-key support is internal/demo/test only. It performs no live LLM calls, no DB access, no external API calls, no runtime evidence fetch, no UI exposure, no payroll calculation, no write action, and no production/customer availability assertion from fixture or code evidence alone.

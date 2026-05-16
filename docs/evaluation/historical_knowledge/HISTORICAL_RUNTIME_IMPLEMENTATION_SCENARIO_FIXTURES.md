# Historical Runtime Implementation Scenario Fixtures

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines non-runtime fixture scenarios for the Minerva historical runtime implementation test matrix.

Fixtures are documentation/test-planning only and do not create runtime data, source records, corpus records, database rows, endpoint data, chat data, Code Evidence, or evidence-store entries.

## Fixture Rules

- fixture ids are planning identifiers only;
- fixture states are hypothetical and must not be interpreted as live evidence state;
- no fixture activates answer-use permission, retrieval eligibility, answer mode, current-truth promotion, or chat exposure;
- no fixture mutates operational corpus content or live evidence stores.

## Scenario Groups

| FixtureId | ScenarioGroup | Planned State | Expected Use |
| --- | --- | --- | --- |
| FIX-CT-001 | Current-Truth Answer Scenarios | governed current-truth evidence with answer-use permission, retrieval eligibility, answer mode, citation/provenance, no conflict, no supersession | allowed current-truth answer in future runtime |
| FIX-CT-002 | Current-Truth Answer Scenarios | current-truth promotion missing | refusal |
| FIX-CT-003 | Current-Truth Answer Scenarios | answer-use permission missing | refusal |
| FIX-CT-004 | Current-Truth Answer Scenarios | retrieval eligibility missing | refusal |
| FIX-CT-005 | Current-Truth Answer Scenarios | citation/provenance missing | refusal |
| FIX-HC-001 | Historical-Context Answer Scenarios | historical-context evidence approved for historical context | historical-context answer with historical label |
| FIX-HC-002 | Historical-Context Answer Scenarios | historical-context evidence used for current truth | refusal |
| FIX-HC-003 | Historical-Context Answer Scenarios | historical source date unknown | unknown-date marker or caveat required |
| FIX-CAV-001 | Caveated Answer Scenarios | caveated current-truth answer with approved caveat | caveated answer |
| FIX-CAV-002 | Caveated Answer Scenarios | caveat required but caveat missing | refusal |
| FIX-CAV-003 | Caveated Answer Scenarios | unresolved limitation without caveat | refusal |
| FIX-BLG-001 | Backlog / Follow-Up Context Scenarios | backlog context answer | planned/deferred/follow-up context only |
| FIX-BLG-002 | Backlog / Follow-Up Context Scenarios | backlog item represented as implemented behaviour | refusal |
| FIX-DOC-001 | Doctrine / Hardening Context Scenarios | doctrine context answer allowed where approved | doctrine/context response |
| FIX-DOC-002 | Doctrine / Hardening Context Scenarios | doctrine used as runtime implementation evidence without supporting implementation source | refusal |
| FIX-REF-001 | Refusal Scenarios | insufficient governed evidence | refusal insufficient governed evidence |
| FIX-REF-002 | Refusal Scenarios | not answer-approved | refusal not answer-approved |
| FIX-REF-003 | Refusal Scenarios | retrieval not eligible | refusal retrieval not eligible |
| FIX-REF-004 | Refusal Scenarios | missing answer mode | refusal missing answer mode |
| FIX-REF-005 | Refusal Scenarios | missing citation/provenance | refusal missing provenance |
| FIX-REF-006 | Refusal Scenarios | conflicted evidence | refusal conflicted |
| FIX-REF-007 | Refusal Scenarios | superseded evidence | refusal superseded |
| FIX-REF-008 | Refusal Scenarios | not-answerable evidence | refusal not-answerable evidence |
| FIX-CON-001 | Conflict / Supersession Scenarios | conflicted evidence refuses settled/current-truth answer | refusal |
| FIX-CON-002 | Conflict / Supersession Scenarios | superseded evidence refuses current-truth answer | refusal |
| FIX-CON-003 | Conflict / Supersession Scenarios | approved historical explanation for superseded evidence remains historical only | historical-context answer only |
| FIX-CIT-001 | Citation / Provenance Scenarios | citation fields present | governed citation allowed in future renderer |
| FIX-CIT-002 | Citation / Provenance Scenarios | SourceId missing | refusal |
| FIX-CIT-003 | Citation / Provenance Scenarios | SourceDate missing without unknown marker | refusal or caveat |
| FIX-CIT-004 | Citation / Provenance Scenarios | RevocationPath missing | blocker/refusal |
| FIX-CIT-005 | Citation / Provenance Scenarios | citation must not be fabricated | refusal |
| FIX-AUD-001 | Audit / Logging Scenarios | future audit fields complete | query/request context, retrieval mode, answer mode, evidence considered, evidence excluded, gate decision, refusal reason, citation/provenance status, caveat status, no mutation/no-write confirmation |

## No Runtime Data

These fixtures do not create runtime data. They do not create retrieval indexes, answer payloads, rendered citations, chat messages, audit rows, database records, source ingestions, corpus mutations, Code Evidence records, or current-truth promotions.

# Structured Response Contract

Provider output is constrained with strict JSON Schema and parsed again with Pydantic. Required fields are Answer, KeyPoints (maximum five), Boundary, GroundingIdentities, SuggestedFollowUps (maximum three) and the exact requested Persona.

The provider receives an explicit allow-list of current-packet grounding identities. Post-provider validation still independently rejects empty/foreign grounding, wrong persona, untrusted markup/URLs, unsupported numbers, action/mutation claims, unsupported persistence claims, tool/secret envelopes and malformed output.

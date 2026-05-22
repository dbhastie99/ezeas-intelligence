from typing import Any

from pydantic import BaseModel, Field


class InternalChatStubRequest(BaseModel):
    Question: str
    Role: str
    SourceScopes: list[str] = Field(default_factory=list)
    SurfaceContext: dict[str, Any] | None = None
    DomainTags: list[str] = Field(default_factory=list)
    CandidateEvidence: list[dict[str, Any]] | dict[str, Any] | None = None
    ClaimToValidate: str | None = None
    AllowFinalAnswerGeneration: bool = False
    AllowLiveLlm: bool = False
    IncludeDeterministicDraft: bool = True
    FixtureKey: str | None = None


class InternalChatStubResponse(BaseModel):
    Status: str
    RequestEcho: dict[str, Any]
    OrchestratorEnvelope: dict[str, Any]
    EvidenceSupportPacket: dict[str, Any]
    DeterministicDraft: dict[str, Any] | None
    FinalAnswerText: str | None
    AnswerPermitted: bool
    IsFinalAnswer: bool
    LiveLlmUsed: bool
    FinalAnswerGenerationPermitted: bool
    FixtureEvidence: dict[str, Any]
    NoActionAttestation: dict[str, bool]
    NoActionAttestationText: str
    RequiredCaveats: list[str]
    BlockedClaims: list[str]
    UnsupportedScopes: list[str]
    DisclosureMetadata: dict[str, Any]
    Boundaries: list[str]
    Diagnostics: dict[str, Any]
    AuditSummary: dict[str, Any]

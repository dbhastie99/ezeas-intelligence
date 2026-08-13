from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


QUESTION_CONTRACT_VERSION = "LEAVE_STUDIO_MINERVA_QUESTION_V1"
ANSWER_CONTRACT_VERSION = "LEAVE_STUDIO_MINERVA_ANSWER_V1"
STUDIO_CONTEXT_SCHEMA_VERSION = "LEAVE_STUDIO_CONTEXT_V1"

FactAuthorityClass = Literal[
    "CANONICAL_STORED_FACT",
    "DETERMINISTIC_DERIVATION",
    "COMPATIBILITY_SOURCED_FACT",
    "MISSING_OR_UNRESOLVED_FACT",
]

QuestionClassification = Literal[
    "OVERVIEW",
    "ENTITLEMENT",
    "ACCRUAL",
    "PAYROLL_BASIS",
    "PUBLIC_HOLIDAY",
    "FORECAST",
    "TAKING",
    "EVIDENCE",
    "PRIVACY",
    "PAYMENT",
    "LOADING",
    "ORGANISATION_CHOICE",
    "SOURCE_AUTHORITY",
    "READINESS",
    "RUNTIME_SUPPORT",
    "VERSION_LINEAGE",
    "APPLICABILITY_SCOPE",
    "LSL_SERVICE",
    "LSL_VESTING",
    "LSL_TERMINATION",
    "LSL_VALUATION",
    "QLEAVE_BOUNDARY",
    "UNKNOWN_OR_UNSUPPORTED",
]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class StudioFinding(ContractModel):
    Code: str
    Severity: str
    Message: str
    Action: str


class StudioAuthorityTrailItem(ContractModel):
    SourceTitle: str
    Citation: str
    EffectivePeriod: str
    ValidationState: str
    Interpretation: str


class StudioBasisMembership(ContractModel):
    RateType: str
    DisplayName: str
    Treatment: str
    MappingState: str
    EffectiveFrom: str


class StudioBasisLink(ContractModel):
    BasisCode: str
    BusinessName: str
    Purpose: str
    Readiness: str


class StudioBasisInspection(ContractModel):
    BasisCode: str
    BusinessName: str
    VersionLabel: str
    Owner: str
    EffectiveFrom: str
    Purpose: str
    LegalMeaning: str
    Method: str
    OutputUnit: str
    PeriodWindow: str
    Membership: list[StudioBasisMembership]
    LinkedPolicies: list[StudioBasisLink]
    AuthorityExplanation: str
    Readiness: str
    Findings: list[StudioFinding]
    EvidenceBoundary: str


class StudioResolvedPolicySetting(ContractModel):
    SettingKey: str
    Label: str
    Domain: str
    SuppliedValue: str
    EmployerValue: str | None = None
    ResolvedValue: str
    ResolutionSource: str
    ControlMode: str
    Authority: str
    ValidationOutcome: str
    MissingFactDisposition: str
    AmbiguityDisposition: str
    FutureConsumer: str
    Editable: bool


class StudioResolvedSectionItem(ContractModel):
    Code: str
    Label: str
    Outcome: str | None = None
    Authority: str | None = None
    Disposition: str | None = None
    FutureConsumer: str | None = None
    ContentHash: str | None = None


class StudioContextFact(ContractModel):
    Key: str
    Domain: str
    Label: str
    Value: Any | None = None
    DisplayValue: str
    AuthorityClass: FactAuthorityClass
    CanonicalSource: str
    HumanExplanation: str
    CompatibilityDependency: str | None = None


class LeaveStudioContextV1(ContractModel):
    SchemaVersion: Literal["LEAVE_STUDIO_CONTEXT_V1"]
    PackageCode: str
    LeaveTypeId: str
    LeaveTypeCode: str
    LeaveTypeName: str
    LeaveTypeVersionId: str
    VersionCode: str
    VersionNumber: int
    EffectiveFrom: str
    EffectiveTo: str | None = None
    Ownership: str
    PredecessorLeaveTypeVersionId: str | None = None
    SuccessorLeaveTypeVersionIds: list[str]
    PolicyConfigurationScopeStatement: str
    WorkerApplicabilityStatement: str
    ConfigurationReadiness: str
    RuntimeSupport: str
    PublicationReadiness: str
    Facts: list[StudioContextFact]
    ReadinessFindings: list[StudioFinding]
    PayrollBases: list[StudioBasisInspection]
    SourceEvidence: list[StudioAuthorityTrailItem]
    OrganisationChoices: list[StudioResolvedPolicySetting]
    SourcePrecedence: list[StudioResolvedSectionItem]
    RequiredFacts: list[StudioResolvedSectionItem]
    ServiceHistory: list[StudioResolvedSectionItem]
    ValuationStrategies: list[StudioResolvedSectionItem]
    CaseLevelHolds: list[StudioResolvedSectionItem]
    PortableSchemeBoundary: str | None = None
    ConfidentialDataExcluded: Literal[True]

    @model_validator(mode="after")
    def validate_fact_identity(self) -> "LeaveStudioContextV1":
        keys = [fact.Key for fact in self.Facts]
        if len(keys) != len(set(keys)):
            raise ValueError("Studio fact identifiers must be unique")
        return self


class LeaveStudioQuestionRequest(ContractModel):
    ContractVersion: Literal["LEAVE_STUDIO_MINERVA_QUESTION_V1"]
    RequestId: str = Field(min_length=8, max_length=128)
    Question: str = Field(min_length=1, max_length=2000)
    PackageCode: str = Field(min_length=1, max_length=160)
    LeaveTypeVersionId: str = Field(min_length=1, max_length=128)
    StudioContextSchemaVersion: Literal["LEAVE_STUDIO_CONTEXT_V1"]
    StudioContextFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    StudioContext: LeaveStudioContextV1
    ConfidentialDataIncluded: Literal[False]
    WorkerSpecificContextIncluded: Literal[False]
    RequestedMode: Literal["CONFIGURATION_EXPLANATION"]


class SelectedMaterialFact(ContractModel):
    FactId: str
    Label: str
    Value: str | None = None
    DisplayValue: str
    AuthorityClass: FactAuthorityClass
    EvidenceReferenceIds: list[str]


class EvidenceReference(ContractModel):
    EvidenceReferenceId: str
    Label: str
    Reference: str
    Section: str


class LeaveStudioAnswerPlan(ContractModel):
    QuestionClassification: QuestionClassification
    LeaveTypeVersionId: str
    DirectDeterministicAnswer: str
    WhatMatters: list[str]
    SelectedMaterialFacts: list[SelectedMaterialFact]
    FactIds: list[str]
    FactAuthorityClasses: list[FactAuthorityClass]
    MissingOrUnresolvedFacts: list[str]
    ReadinessState: str
    RuntimeSupportState: str
    Boundary: str
    SafeNextStep: str
    EvidenceReferences: list[EvidenceReference]
    PlannerFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    RendererEligible: bool


class LeaveStudioAnswerResponse(ContractModel):
    ContractVersion: Literal["LEAVE_STUDIO_MINERVA_ANSWER_V1"]
    RequestId: str
    Answer: str
    AnswerMode: QuestionClassification
    WhatMatters: list[str]
    Boundary: str
    SafeNextStep: str
    EvidenceReferences: list[EvidenceReference]
    FactIds: list[str]
    FactAuthorityClasses: list[FactAuthorityClass]
    MissingOrUnresolvedFacts: list[str]
    ReadinessState: str
    RuntimeSupportState: str
    LeaveTypeVersionId: str
    StudioContextSchemaVersion: Literal["LEAVE_STUDIO_CONTEXT_V1"]
    StudioContextFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    PlannerFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    RendererEligible: bool
    RendererAttempted: bool
    RendererUsed: bool
    RendererModelIdentifier: str | None = None
    RendererInstructionVersion: str
    RendererConfigurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    RendererFallbackReason: str | None = None
    OutputHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    DurationMs: int = Field(ge=0)
    NoChangesMade: Literal[True]


class RendererPayload(ContractModel):
    InstructionVersion: str
    QueryIntent: QuestionClassification
    DirectDeterministicAnswer: str
    WhatMatters: list[str]
    SelectedMaterialFacts: list[SelectedMaterialFact]
    FactIds: list[str]
    MissingOrUnresolvedFacts: list[str]
    Boundary: str
    SafeNextStep: str
    EvidenceReferences: list[EvidenceReference]
    PlannerFingerprint: str


class RendererDocument(ContractModel):
    Answer: str
    WhatMatters: list[str]
    Boundary: str
    SafeNextStep: str
    EvidenceReferenceIds: list[str]
    FactIds: list[str]


ExplanationPersona = Literal["ADMINISTRATOR", "LEGAL", "MANAGER", "WORKER"]


class ConversationHistoryTurn(ContractModel):
    TurnIdentity: str = Field(min_length=8, max_length=128)
    Role: Literal["USER", "MINERVA"]
    Content: str = Field(min_length=1, max_length=2000)
    Persona: ExplanationPersona
    PolicyKey: str = Field(min_length=1, max_length=160)
    LeaveTypeVersionId: str = Field(min_length=1, max_length=128)
    BaselineContentHash: str = Field(pattern=r"^[0-9a-f]{64}$")


class LeaveStudioLlmContextV3(ContractModel):
    ContractVersion: Literal["LEAVE_STUDIO_LLM_CONTEXT_V3"]
    PolicyKey: str
    PackageCode: str
    LeaveTypeVersionId: str
    VersionCode: str
    VersionNumber: int
    EffectiveFrom: str
    BaselineContentHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    PolicyContentHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    Persona: ExplanationPersona
    Ownership: str
    PolicyStory: dict[str, Any]
    OperationalStory: dict[str, Any]
    AtAGlance: list[dict[str, Any]]
    PreparedScenarios: list[dict[str, Any]]
    ManagementCategories: list[dict[str, Any]]
    Holds: list[dict[str, Any]]
    AuthorityIdentities: list[str]
    EvidenceIdentities: list[str]
    AvailableGovernedActions: list[dict[str, Any]]
    CapabilityBoundaries: dict[str, str]
    TargetFieldIdentity: str | None = None
    TargetScenarioCode: str | None = None
    ConfidentialDataIncluded: Literal[False]
    WorkerSpecificContextIncluded: Literal[False]


class LeaveStudioConversationRequest(ContractModel):
    ContractVersion: Literal["LEAVE_STUDIO_LIVE_MINERVA_REQUEST_V1"]
    RequestIdentity: str = Field(min_length=8, max_length=128)
    ConversationTurnIdentity: str = Field(min_length=8, max_length=128)
    Question: str = Field(min_length=1, max_length=2000)
    Persona: ExplanationPersona
    ContextPacketFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    ContextPacket: LeaveStudioLlmContextV3
    ConversationHistory: list[ConversationHistoryTurn] = Field(default_factory=list, max_length=8)

    @model_validator(mode="after")
    def validate_pinned_context(self) -> "LeaveStudioConversationRequest":
        if self.Persona != self.ContextPacket.Persona:
            raise ValueError("request persona must equal the governed context persona")
        if sum(len(turn.Content) for turn in self.ConversationHistory) > 12_000:
            raise ValueError("conversation history exceeds the governed character limit")
        if any(
            turn.PolicyKey != self.ContextPacket.PolicyKey
            or turn.LeaveTypeVersionId != self.ContextPacket.LeaveTypeVersionId
            or turn.BaselineContentHash != self.ContextPacket.BaselineContentHash
            for turn in self.ConversationHistory
        ):
            raise ValueError("conversation history must be pinned to the current governed policy context")
        return self


class LeaveStudioLiveModelDocument(ContractModel):
    Answer: str = Field(min_length=1, max_length=4000)
    KeyPoints: list[str] = Field(default_factory=list, max_length=5)
    Boundary: str = Field(min_length=1, max_length=1200)
    GroundingIdentities: list[str] = Field(default_factory=list, max_length=30)
    SuggestedFollowUps: list[str] = Field(default_factory=list, max_length=3)
    Persona: ExplanationPersona


class LeaveStudioConversationResponse(ContractModel):
    ContractVersion: Literal["EZEAS_INTELLIGENCE_LEAVE_STUDIO_RESPONSE_V1"]
    RequestIdentity: str
    ConversationTurnIdentity: str
    PolicyKey: str
    LeaveTypeVersionId: str
    BaselineContentHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    ContextPacketFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    Persona: ExplanationPersona
    Answer: str = Field(min_length=1, max_length=4000)
    KeyPoints: list[str] = Field(default_factory=list, max_length=5)
    Boundary: str = Field(min_length=1, max_length=1200)
    GroundingIdentities: list[str] = Field(default_factory=list, max_length=30)
    SuggestedFollowUps: list[str] = Field(default_factory=list, max_length=3)
    LiveLlmAttempted: bool
    LiveLlmUsed: bool
    ModelIdentifier: str | None = None
    PromptInstructionVersion: str
    ProviderLatencyMs: int | None = Field(None, ge=0)
    AuditIdentity: str
    OutputFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    FallbackReason: str | None = None
    NoChangesMade: Literal[True]

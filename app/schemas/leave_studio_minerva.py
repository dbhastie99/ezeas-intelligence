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

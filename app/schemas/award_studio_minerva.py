from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


PROJECTION_SCHEMA_VERSION = "award_version_explainable_context_v1"
QUESTION_CONTRACT_VERSION = "award_version_minerva_question_v1"
ANSWER_CONTRACT_VERSION = "award_version_minerva_answer_v1"

AuthorityClassification = Literal[
    "EXPLICIT_STRUCTURED",
    "DETERMINISTICALLY_DERIVABLE",
    "HELD",
    "NOT_CONFIGURED",
    "MISSING",
    "CONFLICT",
]

PresentationMode = Literal["CHAT", "LEVEL_2"]

QuestionClassification = Literal[
    "OVERVIEW",
    "CLASSIFICATION",
    "SATURDAY",
    "SUNDAY",
    "PUBLIC_HOLIDAY",
    "OVERTIME_1",
    "OVERTIME_2",
    "ALLOWANCE_REIMBURSEMENT",
    "HOLD",
    "SOURCE_EVIDENCE",
    "VERSION_LINEAGE",
    "EMPLOYMENT_TYPE_COMPARISON",
    "UNKNOWN_OR_UNSUPPORTED",
]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AwardVersionAuthorityEnvelope(ContractModel):
    awardHeaderId: str = Field(min_length=1, max_length=128)
    awardVersionId: str = Field(min_length=1, max_length=128)
    awardCode: str = Field(min_length=1, max_length=80)
    awardName: str = Field(min_length=1, max_length=300)
    effectiveFrom: str = Field(min_length=1, max_length=80)
    effectiveTo: str | None = Field(default=None, max_length=80)
    lifecycle: str = Field(min_length=1, max_length=80)
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionSchemaVersion: Literal["award_version_explainable_context_v1"]
    versionLineage: dict[str, Any]


class AwardSemanticNode(ContractModel):
    semanticIdentity: str = Field(min_length=1, max_length=256)
    type: str = Field(min_length=1, max_length=120)
    code: str = Field(min_length=1, max_length=256)
    friendlyName: str = Field(min_length=1, max_length=500)
    purpose: str | None = Field(default=None, max_length=4000)
    status: str = Field(min_length=1, max_length=120)
    authorityClassification: AuthorityClassification
    values: dict[str, Any]
    quantities: list[dict[str, Any]]
    applicability: dict[str, Any]
    evidenceIds: list[str]
    workspaceAnchor: str | None = Field(default=None, max_length=500)


class AwardSemanticRelationship(ContractModel):
    relationshipIdentity: str = Field(min_length=1, max_length=256)
    type: str = Field(min_length=1, max_length=120)
    sourceSemanticIdentity: str = Field(min_length=1, max_length=256)
    targetKind: str = Field(min_length=1, max_length=120)
    targetIdentity: str = Field(min_length=1, max_length=256)
    authorityClassification: AuthorityClassification
    applicability: dict[str, Any]


class AwardEvidenceReference(ContractModel):
    evidenceIdentity: str = Field(min_length=1, max_length=256)
    propositionIdentity: str | None = Field(default=None, max_length=256)
    semanticIdentity: str | None = Field(default=None, max_length=256)
    sourceDocumentIdentity: str = Field(min_length=1, max_length=256)
    sourceTitle: str = Field(min_length=1, max_length=1000)
    sourceSha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    officialUrl: str | None = Field(default=None, max_length=4000)
    sourceLocator: dict[str, Any]
    extractedValue: Any | None = None
    authorityClassification: AuthorityClassification


class AwardOperationalBinding(ContractModel):
    bindingIdentity: str = Field(min_length=1, max_length=256)
    bindingType: str = Field(min_length=1, max_length=120)
    semanticIdentity: str = Field(min_length=1, max_length=256)
    targetIdentity: str = Field(min_length=1, max_length=256)
    targetCode: str | None = Field(default=None, max_length=256)
    authorityClassification: AuthorityClassification


class AwardHold(ContractModel):
    holdIdentity: str = Field(min_length=1, max_length=256)
    semanticIdentity: str = Field(min_length=1, max_length=256)
    code: str = Field(min_length=1, max_length=256)
    friendlyName: str = Field(min_length=1, max_length=500)
    status: str = Field(min_length=1, max_length=120)
    reason: str = Field(min_length=1, max_length=4000)
    sourceSemantic: str | None = Field(default=None, max_length=500)
    candidateSemantic: str | None = Field(default=None, max_length=500)
    requiredAction: str | None = Field(default=None, max_length=2000)
    evidenceIds: list[str]


class AwardCompletenessEntry(ContractModel):
    conceptCode: str = Field(min_length=1, max_length=256)
    friendlyName: str = Field(min_length=1, max_length=500)
    authorityClassification: AuthorityClassification
    explanation: str = Field(min_length=1, max_length=4000)
    semanticIdentities: list[str]


class AwardPresentationPayload(ContractModel):
    presentationKey: str = Field(min_length=1, max_length=256)
    conciseSpokenSummary: str = Field(min_length=1, max_length=2000)
    expandableDetail: list[str]
    evidenceIds: list[str]
    workspaceAnchors: list[str]
    subtitles: list[str]
    recommendedSequence: int = Field(ge=0)


class AwardEmploymentTypeScope(ContractModel):
    EmploymentTypeId: str = Field(min_length=1, max_length=128)
    EmploymentTypeCode: Literal["FULL_TIME", "PART_TIME", "CASUAL"]
    ApplicabilityCode: Literal["EXPLICIT_SOURCE_SCOPE", "LEGACY_SINGLE_SCOPE"]
    ApplicabilityFingerprint: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class AwardVersionExplainableContextV1(ContractModel):
    schemaVersion: Literal["award_version_explainable_context_v1"]
    authorityEnvelope: AwardVersionAuthorityEnvelope
    semanticNodes: list[AwardSemanticNode]
    relationships: list[AwardSemanticRelationship]
    evidence: list[AwardEvidenceReference]
    operationalBindings: list[AwardOperationalBinding]
    employmentTypeScope: list[AwardEmploymentTypeScope] = Field(default_factory=list)
    holds: list[AwardHold]
    completeness: list[AwardCompletenessEntry]
    presentationPayloads: list[AwardPresentationPayload]
    readOnly: Literal[True]
    noChangesMade: Literal[True]

    @model_validator(mode="after")
    def validate_graph_references(self) -> "AwardVersionExplainableContextV1":
        node_ids = [node.semanticIdentity for node in self.semanticNodes]
        relationship_ids = [edge.relationshipIdentity for edge in self.relationships]
        evidence_ids = [item.evidenceIdentity for item in self.evidence]
        binding_ids = [item.bindingIdentity for item in self.operationalBindings]
        hold_ids = [item.holdIdentity for item in self.holds]
        presentation_keys = [item.presentationKey for item in self.presentationPayloads]
        for label, values in (
            ("semantic node", node_ids),
            ("relationship", relationship_ids),
            ("evidence", evidence_ids),
            ("operational binding", binding_ids),
            ("hold", hold_ids),
            ("presentation payload", presentation_keys),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{label} identities must be unique")

        node_set = set(node_ids)
        evidence_set = set(evidence_ids)
        binding_set = set(binding_ids)
        for node in self.semanticNodes:
            if not set(node.evidenceIds).issubset(evidence_set):
                raise ValueError("semantic node references unknown evidence")
        for edge in self.relationships:
            if edge.sourceSemanticIdentity not in node_set:
                raise ValueError("relationship source references an unknown semantic node")
            if edge.targetKind == "SEMANTIC_NODE" and edge.targetIdentity not in node_set:
                raise ValueError("relationship target references an unknown semantic node")
            if edge.targetKind == "EVIDENCE" and edge.targetIdentity not in evidence_set:
                raise ValueError("relationship target references unknown evidence")
            if edge.targetKind == "OPERATIONAL_BINDING" and edge.targetIdentity not in binding_set:
                raise ValueError("relationship target references an unknown operational binding")
        for item in self.evidence:
            if item.semanticIdentity is not None and item.semanticIdentity not in node_set:
                raise ValueError("evidence references an unknown semantic node")
        for binding in self.operationalBindings:
            if binding.semanticIdentity not in node_set:
                raise ValueError("operational binding references an unknown semantic node")
        for hold in self.holds:
            if hold.semanticIdentity not in node_set:
                raise ValueError("hold references an unknown semantic node")
            if not set(hold.evidenceIds).issubset(evidence_set):
                raise ValueError("hold references unknown evidence")
        for item in self.completeness:
            if not set(item.semanticIdentities).issubset(node_set):
                raise ValueError("completeness entry references an unknown semantic node")
        for item in self.presentationPayloads:
            if not set(item.evidenceIds).issubset(evidence_set):
                raise ValueError("presentation payload references unknown evidence")
        return self


class AwardConversationHistoryTurn(ContractModel):
    turnIdentity: str = Field(min_length=8, max_length=128)
    role: Literal["USER", "MINERVA"]
    content: str = Field(min_length=1, max_length=2000)
    awardVersionId: str = Field(min_length=1, max_length=128)
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


class AwardStudioMinervaQuestionRequest(ContractModel):
    contractVersion: Literal["award_version_minerva_question_v1"]
    requestIdentity: str = Field(min_length=8, max_length=128)
    question: str = Field(min_length=1, max_length=2000)
    presentationMode: PresentationMode
    awardVersionId: str = Field(min_length=1, max_length=128)
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projection: AwardVersionExplainableContextV1
    conversationHistory: list[AwardConversationHistoryTurn] = Field(default_factory=list, max_length=8)
    workerSpecificContextIncluded: Literal[False]

    @model_validator(mode="after")
    def validate_pinned_envelope(self) -> "AwardStudioMinervaQuestionRequest":
        authority = self.projection.authorityEnvelope
        expected = (
            self.awardVersionId,
            self.configurationFingerprint,
            self.semanticGraphFingerprint,
            self.sourceAuthorityFingerprint,
            self.projectionFingerprint,
        )
        actual = (
            authority.awardVersionId,
            authority.configurationFingerprint,
            authority.semanticGraphFingerprint,
            authority.sourceAuthorityFingerprint,
            authority.projectionFingerprint,
        )
        if expected != actual:
            raise ValueError("request identity and fingerprints must match the exact AwardVersion projection")
        if self.projection.schemaVersion != authority.projectionSchemaVersion:
            raise ValueError("projection schema identity mismatch")
        if sum(len(turn.content) for turn in self.conversationHistory) > 12_000:
            raise ValueError("conversation history exceeds the governed character limit")
        if any(
            (
                turn.awardVersionId,
                turn.configurationFingerprint,
                turn.semanticGraphFingerprint,
                turn.sourceAuthorityFingerprint,
                turn.projectionFingerprint,
            )
            != expected
            for turn in self.conversationHistory
        ):
            raise ValueError("conversation history must be pinned to the exact AwardVersion projection")
        return self


class AwardEvidenceCard(ContractModel):
    evidenceIdentity: str
    sourceTitle: str
    sourceLocator: dict[str, Any]
    sourceSha256: str


class AwardAnswerPresentation(ContractModel):
    mode: PresentationMode
    conciseSummary: str
    spokenSummary: str | None = None
    subtitles: list[str]
    expandableDetail: list[str]
    evidenceCards: list[AwardEvidenceCard]
    workspaceAnchors: list[str]
    recommendedSequence: list[str]


class AwardStudioMinervaAnswerPlan(ContractModel):
    questionClassification: QuestionClassification
    answerClassification: AuthorityClassification
    awardVersionId: str
    directDeterministicAnswer: str
    whatMatters: list[str]
    semanticIdentities: list[str]
    relationshipIdentities: list[str]
    evidenceIdentities: list[str]
    holdIdentities: list[str]
    completenessConceptCodes: list[str]
    boundary: str
    safeNextStep: str
    plannerFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


class AwardStudioMinervaQuestionResponse(ContractModel):
    contractVersion: Literal["award_version_minerva_answer_v1"]
    requestIdentity: str
    awardHeaderId: str
    awardVersionId: str
    awardCode: str
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    projectionSchemaVersion: Literal["award_version_explainable_context_v1"]
    questionClassification: QuestionClassification
    answerClassification: AuthorityClassification
    answer: str
    whatMatters: list[str]
    semanticIdentities: list[str]
    relationshipIdentities: list[str]
    evidenceIdentities: list[str]
    holdIdentities: list[str]
    completenessConceptCodes: list[str]
    boundary: str
    safeNextStep: str
    plannerFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    presentationMode: PresentationMode
    presentation: AwardAnswerPresentation
    deterministicAnswerUsed: Literal[True]
    generalCorpusUsedAsConfiguredAuthority: Literal[False]
    workerDecisionEvidenceIncluded: Literal[False]
    noChangesMade: Literal[True]

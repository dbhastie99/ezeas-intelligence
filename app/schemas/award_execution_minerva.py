from __future__ import annotations

from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


EVIDENCE_SCHEMA_VERSION = "award_runtime_decision_evidence_v1"
QUESTION_CONTRACT_VERSION = "award_execution_minerva_question_v1"
ANSWER_CONTRACT_VERSION = "award_execution_minerva_answer_v1"

PresentationMode = Literal["CHAT", "LEVEL_2"]
PrecedenceOutcome = Literal["WINNER", "LOSER", "NOT_APPLICABLE"]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AwardExecutionInputFacts(ContractModel):
    snapshotId: str = Field(min_length=1, max_length=128)
    snapshotFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    appointmentId: str = Field(min_length=1, max_length=128)
    workerId: str = Field(min_length=1, max_length=128)
    employmentType: str = Field(min_length=1, max_length=128)
    positionId: str | None = Field(default=None, max_length=128)
    awardPositionClassId: str | None = Field(default=None, max_length=128)
    facts: dict[str, Any]


class AwardRuleApplicabilityEvidence(ContractModel):
    applicable: bool
    reasonCode: str = Field(min_length=1, max_length=256)
    facts: dict[str, Any]


class AwardRulePrecedenceEvidence(ContractModel):
    stage: str = Field(min_length=1, max_length=128)
    dimension: str | None = Field(max_length=256)
    rank: int | None = Field(default=None, ge=1)
    outcome: PrecedenceOutcome
    reasonCode: str = Field(min_length=1, max_length=256)


class AwardRuleCandidateEvidence(ContractModel):
    candidateEvaluationId: str = Field(min_length=1, max_length=128)
    candidateKind: str = Field(min_length=1, max_length=128)
    decisionStage: str = Field(min_length=1, max_length=128)
    candidateIdentity: str = Field(min_length=1, max_length=256)
    appliesToResultLineSequence: int | None = Field(ge=1)
    rateSourceId: str | None = Field(max_length=128)
    configuredRuleId: str = Field(min_length=1, max_length=256)
    semanticIdentity: str = Field(min_length=1, max_length=256)
    executableProvisionIdentity: str = Field(min_length=1, max_length=256)
    applicability: AwardRuleApplicabilityEvidence
    precedence: AwardRulePrecedenceEvidence
    sourceEvidenceReferences: list[str]

    @model_validator(mode="after")
    def validate_outcome(self) -> "AwardRuleCandidateEvidence":
        if self.decisionStage != self.precedence.stage:
            raise ValueError("candidate decisionStage must equal precedence.stage")
        if self.precedence.stage == "RATE_RESOLUTION" and self.appliesToResultLineSequence is None:
            raise ValueError("RATE_RESOLUTION candidate must identify its result line sequence")
        if self.applicability.applicable and self.precedence.outcome == "NOT_APPLICABLE":
            raise ValueError("an applicable candidate cannot have NOT_APPLICABLE precedence outcome")
        if not self.applicability.applicable and self.precedence.outcome != "NOT_APPLICABLE":
            raise ValueError("a non-applicable candidate must have NOT_APPLICABLE precedence outcome")
        return self


class AwardRateResolutionEvidence(ContractModel):
    rateTypeId: UUID | None
    rateSourceId: str = Field(min_length=1, max_length=128)
    value: Decimal
    unit: str = Field(min_length=1, max_length=80)
    currency: str = Field(min_length=3, max_length=16)


class AwardPayResultEvidence(ContractModel):
    calcInterpreterLineId: str = Field(min_length=1, max_length=128)
    resultLineSequence: int = Field(ge=1)
    quantity: Decimal
    rate: Decimal
    amount: Decimal
    currency: str = Field(min_length=3, max_length=16)
    resultHash: str = Field(pattern=r"^[0-9a-f]{64}$")


class AwardExecutionSourceEvidenceReference(ContractModel):
    evidenceIdentity: str = Field(min_length=1, max_length=256)
    sourceDocumentIdentity: str = Field(min_length=1, max_length=256)
    sourceSha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceLocator: dict[str, Any]


class AwardDecisionEvidenceHeader(ContractModel):
    decisionEvidenceId: str = Field(min_length=1, max_length=128)
    evaluationId: str = Field(min_length=1, max_length=128)
    executionId: str = Field(min_length=1, max_length=128)
    executedAtUtc: str = Field(min_length=1, max_length=80)
    awardId: str = Field(min_length=1, max_length=128)
    awardVersionId: str = Field(min_length=1, max_length=128)
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    decisionEvidenceHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    objectTimeId: str = Field(min_length=1, max_length=128)
    inputFacts: AwardExecutionInputFacts


class AwardDecisionResultLine(ContractModel):
    winnerCandidateEvaluationId: str = Field(min_length=1, max_length=128)
    configuredRuleId: str = Field(min_length=1, max_length=256)
    semanticIdentity: str = Field(min_length=1, max_length=256)
    executableProvisionIdentity: str = Field(min_length=1, max_length=256)
    rateResolution: AwardRateResolutionEvidence
    payResult: AwardPayResultEvidence


class AwardRuntimeDecisionEvidenceV1(ContractModel):
    schemaVersion: Literal["award_runtime_decision_evidence_v1"]
    authorityMode: Literal["STORED_EXECUTION_EVIDENCE"]
    evidencePersistence: Literal["DURABLE_RUNTIME_RECORD"]
    header: AwardDecisionEvidenceHeader
    result: AwardDecisionResultLine
    evaluations: list[AwardRuleCandidateEvidence] = Field(min_length=1)
    sourceEvidenceReferences: list[AwardExecutionSourceEvidenceReference]

    @model_validator(mode="after")
    def validate_decision_graph(self) -> "AwardRuntimeDecisionEvidenceV1":
        candidate_ids = [item.candidateEvaluationId for item in self.evaluations]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate evaluation identities must be unique")
        if self.result.winnerCandidateEvaluationId not in set(candidate_ids):
            raise ValueError("winner candidate must reference an evaluated candidate")
        final_winners = [
            item
            for item in self.evaluations
            if item.precedence.stage == "RATE_RESOLUTION"
            and item.precedence.outcome == "WINNER"
        ]
        if len(final_winners) != 1:
            raise ValueError("decision evidence must contain exactly one RATE_RESOLUTION winning candidate")
        if any(
            item.appliesToResultLineSequence != self.result.payResult.resultLineSequence
            for item in self.evaluations
            if item.precedence.stage == "RATE_RESOLUTION"
        ):
            raise ValueError("RATE_RESOLUTION candidate must link to the selected result line sequence")
        winner_dimensions = [
            (
                item.precedence.stage,
                item.precedence.dimension,
                item.appliesToResultLineSequence,
            )
            for item in self.evaluations
            if item.precedence.outcome == "WINNER"
        ]
        if len(winner_dimensions) != len(set(winner_dimensions)):
            raise ValueError("each selected-line precedence contest may contain at most one winning candidate")
        winners_by_contest = {
            (
                item.precedence.stage,
                item.precedence.dimension,
                item.appliesToResultLineSequence,
            ): item
            for item in self.evaluations
            if item.precedence.outcome == "WINNER"
        }
        contests: dict[tuple[str, str | None, int | None], list[int]] = {}
        for item in self.evaluations:
            if item.precedence.rank is None:
                continue
            contest = (
                item.precedence.stage,
                item.precedence.dimension,
                item.appliesToResultLineSequence,
            )
            contests.setdefault(contest, []).append(item.precedence.rank)
        if any(len(ranks) != len(set(ranks)) for ranks in contests.values()):
            raise ValueError("ranked candidates must have unique ranks within their precedence contest")
        for loser in (
            item for item in self.evaluations if item.precedence.outcome == "LOSER"
        ):
            contest = (
                loser.precedence.stage,
                loser.precedence.dimension,
                loser.appliesToResultLineSequence,
            )
            winner = winners_by_contest.get(contest)
            if winner is None:
                raise ValueError("LOSER candidate must reference a contest with a same-line winner")
            if (
                loser.precedence.rank is not None
                and winner.precedence.rank is not None
                and loser.precedence.rank <= winner.precedence.rank
            ):
                raise ValueError("ranked LOSER must have a numerically greater rank than its winner")
        final_winner = final_winners[0]
        if final_winner.candidateEvaluationId != self.result.winnerCandidateEvaluationId:
            raise ValueError("result winner identity must match the RATE_RESOLUTION winning candidate")
        if self.header.evaluationId != self.result.winnerCandidateEvaluationId:
            raise ValueError("header evaluation identity must identify the winning result-line evaluation")
        if not final_winner.applicability.applicable:
            raise ValueError("winning candidate must be applicable")
        if (
            final_winner.rateSourceId is not None
            and final_winner.rateSourceId != self.result.rateResolution.rateSourceId
        ):
            raise ValueError("RATE_RESOLUTION winner RateSource must match the selected result")
        if (
            final_winner.configuredRuleId,
            final_winner.semanticIdentity,
            final_winner.executableProvisionIdentity,
        ) != (
            self.result.configuredRuleId,
            self.result.semanticIdentity,
            self.result.executableProvisionIdentity,
        ):
            raise ValueError("result rule identities must match the winning evaluation")
        evidence_ids = [item.evidenceIdentity for item in self.sourceEvidenceReferences]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("source evidence identities must be unique")
        if not final_winner.sourceEvidenceReferences:
            raise ValueError("RATE_RESOLUTION winner must reference source evidence")
        if any(
            not set(candidate.sourceEvidenceReferences).issubset(set(evidence_ids))
            for candidate in self.evaluations
        ):
            raise ValueError("candidate must reference only supplied source evidence")
        return self


class AwardExecutionMinervaQuestionRequest(ContractModel):
    contractVersion: Literal["award_execution_minerva_question_v1"]
    requestIdentity: str = Field(min_length=8, max_length=128)
    question: str = Field(min_length=1, max_length=2000)
    presentationMode: PresentationMode
    calcInterpreterLineId: UUID
    awardVersionId: UUID
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


class AwardExecutionPrincipal(ContractModel):
    accountId: UUID


class AwardExecutionCandidateExplanation(ContractModel):
    candidateEvaluationId: str
    candidateKind: str
    decisionStage: str
    candidateIdentity: str
    appliesToResultLineSequence: int | None
    rateSourceId: str | None
    configuredRuleId: str
    semanticIdentity: str
    executableProvisionIdentity: str
    applicable: bool
    applicabilityReasonCode: str
    applicabilityFacts: dict[str, Any]
    precedenceStage: str
    precedenceDimension: str | None
    precedenceRank: int | None
    precedenceOutcome: PrecedenceOutcome
    precedenceReasonCode: str
    sourceEvidenceReferences: list[str]


class AwardExecutionPresentation(ContractModel):
    mode: PresentationMode
    conciseSummary: str
    spokenSummary: str | None = None
    subtitles: list[str]
    expandableDetail: list[str]


class AwardExecutionMinervaQuestionResponse(ContractModel):
    contractVersion: Literal["award_execution_minerva_answer_v1"]
    requestIdentity: str
    decisionEvidenceId: str
    evaluationId: str
    executionId: str
    executedAtUtc: str
    awardId: str
    awardVersionId: str
    configurationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    semanticGraphFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    sourceAuthorityFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    decisionEvidenceHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    resultHash: str = Field(pattern=r"^[0-9a-f]{64}$")
    appointmentId: str
    workerId: str
    objectTimeId: str
    inputFacts: AwardExecutionInputFacts
    winnerCandidateEvaluationId: str
    winnerConfiguredRuleId: str
    winnerSemanticIdentity: str
    winnerExecutableProvisionIdentity: str
    candidateExplanations: list[AwardExecutionCandidateExplanation]
    rateResolution: AwardRateResolutionEvidence
    payResult: AwardPayResultEvidence
    sourceEvidenceReferences: list[AwardExecutionSourceEvidenceReference]
    answer: str
    boundary: str
    explanationFingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    presentationMode: PresentationMode
    presentation: AwardExecutionPresentation
    storedExecutionEvidenceUsed: Literal[True]
    configurationExplanationUsed: Literal[False]
    independentAwardRecomputationPerformed: Literal[False]
    noChangesMade: Literal[True]

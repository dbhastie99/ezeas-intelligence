from __future__ import annotations

import hashlib
import json
from uuid import UUID

from app.schemas.award_execution_minerva import (
    ANSWER_CONTRACT_VERSION,
    AwardExecutionCandidateExplanation,
    AwardExecutionMinervaQuestionRequest,
    AwardExecutionMinervaQuestionResponse,
    AwardExecutionPresentation,
    AwardRuntimeDecisionEvidenceV1,
)
from app.services.workforce_award_evidence_client import (
    AwardExecutionEvidenceProvider,
    AwardExecutionExactVersionMismatch,
)


def _canonical(value: object) -> bytes:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _money(value, currency: str) -> str:
    return f"{currency} {value}"


def _candidate_detail(candidate) -> str:
    applicability = (
        f"applicable ({candidate.applicability.reasonCode})"
        if candidate.applicability.applicable
        else f"not applicable ({candidate.applicability.reasonCode})"
    )
    detail = (
        f"{candidate.candidateIdentity} ({candidate.candidateKind}, {candidate.semanticIdentity}) was "
        f"{applicability}; precedence outcome "
        f"{candidate.precedence.outcome} at {candidate.precedence.stage} on "
        f"{candidate.precedence.dimension} "
        f"({candidate.precedence.reasonCode})"
    )
    if candidate.appliesToResultLineSequence is not None:
        detail += f"; result line sequence {candidate.appliesToResultLineSequence}"
    if candidate.rateSourceId is not None:
        detail += f"; candidate RateSource {candidate.rateSourceId}"
    return detail + "."


def compose_award_execution_explanation(
    request: AwardExecutionMinervaQuestionRequest,
    evidence: AwardRuntimeDecisionEvidenceV1,
    account_id: str,
) -> AwardExecutionMinervaQuestionResponse:
    """Explain a persisted decision record without selecting or evaluating Award rules."""
    header = evidence.header
    result = evidence.result
    try:
        stored_calc_line_id = UUID(result.payResult.calcInterpreterLineId)
        stored_award_version_id = UUID(header.awardVersionId)
    except ValueError as exc:
        raise AwardExecutionExactVersionMismatch(
            "stored evidence contains a non-UUID result or AwardVersion identity"
        ) from exc
    if stored_calc_line_id != request.calcInterpreterLineId:
        raise AwardExecutionExactVersionMismatch(
            "stored evidence belongs to a different CalcInterpreterLine"
        )
    if (
        request.awardVersionId,
        request.configurationFingerprint,
        request.semanticGraphFingerprint,
        request.sourceAuthorityFingerprint,
    ) != (
        stored_award_version_id,
        header.configurationFingerprint,
        header.semanticGraphFingerprint,
        header.sourceAuthorityFingerprint,
    ):
        raise AwardExecutionExactVersionMismatch(
            "request does not match the exact AwardVersion authority stored with execution evidence"
        )
    winner = next(
        item
        for item in evidence.evaluations
        if item.candidateEvaluationId == result.winnerCandidateEvaluationId
    )
    candidates = [
        AwardExecutionCandidateExplanation(
            candidateEvaluationId=item.candidateEvaluationId,
            candidateKind=item.candidateKind,
            decisionStage=item.decisionStage,
            candidateIdentity=item.candidateIdentity,
            appliesToResultLineSequence=item.appliesToResultLineSequence,
            rateSourceId=item.rateSourceId,
            configuredRuleId=item.configuredRuleId,
            semanticIdentity=item.semanticIdentity,
            executableProvisionIdentity=item.executableProvisionIdentity,
            applicable=item.applicability.applicable,
            applicabilityReasonCode=item.applicability.reasonCode,
            applicabilityFacts=item.applicability.facts,
            precedenceStage=item.precedence.stage,
            precedenceDimension=item.precedence.dimension,
            precedenceRank=item.precedence.rank,
            precedenceOutcome=item.precedence.outcome,
            precedenceReasonCode=item.precedence.reasonCode,
            sourceEvidenceReferences=item.sourceEvidenceReferences,
        )
        for item in evidence.evaluations
    ]
    other_evaluations = [
        _candidate_detail(item)
        for item in evidence.evaluations
        if item.candidateEvaluationId != winner.candidateEvaluationId
    ]
    classification_context = ""
    if header.inputFacts.positionId:
        classification_context += f", position {header.inputFacts.positionId}"
    if header.inputFacts.awardPositionClassId:
        classification_context += f", AwardPositionClass {header.inputFacts.awardPositionClassId}"
    answer = (
        f"Stored execution evidence {header.decisionEvidenceId} records worker {header.inputFacts.workerId}, "
        f"appointment {header.inputFacts.appointmentId}, ObjectTime {header.objectTimeId}, and employment type "
        f"{header.inputFacts.employmentType}{classification_context} under exact AwardVersion "
        f"{header.awardVersionId}. "
        f"Configured semantic rule {winner.semanticIdentity} ({winner.configuredRuleId}) applied because "
        f"{winner.applicability.reasonCode}; it won the {winner.precedence.stage} stage on "
        f"{winner.precedence.dimension} because "
        f"{winner.precedence.reasonCode}. RateSource {result.rateResolution.rateSourceId} resolved "
        f"{_money(result.rateResolution.value, result.rateResolution.currency)} per "
        f"{result.rateResolution.unit}; CalcInterpreterLine {result.payResult.calcInterpreterLineId} records "
        f"quantity {result.payResult.quantity} and amount "
        f"{_money(result.payResult.amount, result.payResult.currency)}."
    )
    if other_evaluations:
        answer += " Additional decision-stage evaluations recorded by runtime: " + " ".join(other_evaluations)

    detail = [_candidate_detail(item) for item in evidence.evaluations]
    concise = (
        f"Stored decision {header.decisionEvidenceId}: {winner.semanticIdentity} produced "
        f"{_money(result.payResult.amount, result.payResult.currency)}."
    )
    presentation = AwardExecutionPresentation(
        mode=request.presentationMode,
        conciseSummary=concise,
        spokenSummary=concise if request.presentationMode == "LEVEL_2" else None,
        subtitles=[concise] if request.presentationMode == "LEVEL_2" else [],
        expandableDetail=detail,
    )
    return AwardExecutionMinervaQuestionResponse(
        contractVersion=ANSWER_CONTRACT_VERSION,
        requestIdentity=request.requestIdentity,
        decisionEvidenceId=header.decisionEvidenceId,
        evaluationId=header.evaluationId,
        executionId=header.executionId,
        executedAtUtc=header.executedAtUtc,
        awardId=header.awardId,
        awardVersionId=header.awardVersionId,
        configurationFingerprint=header.configurationFingerprint,
        semanticGraphFingerprint=header.semanticGraphFingerprint,
        sourceAuthorityFingerprint=header.sourceAuthorityFingerprint,
        decisionEvidenceHash=header.decisionEvidenceHash,
        resultHash=result.payResult.resultHash,
        appointmentId=header.inputFacts.appointmentId,
        workerId=header.inputFacts.workerId,
        objectTimeId=header.objectTimeId,
        inputFacts=header.inputFacts,
        winnerCandidateEvaluationId=winner.candidateEvaluationId,
        winnerConfiguredRuleId=winner.configuredRuleId,
        winnerSemanticIdentity=winner.semanticIdentity,
        winnerExecutableProvisionIdentity=winner.executableProvisionIdentity,
        candidateExplanations=candidates,
        rateResolution=result.rateResolution,
        payResult=result.payResult,
        sourceEvidenceReferences=evidence.sourceEvidenceReferences,
        answer=answer,
        boundary=(
            "This execution explanation reports the account-scoped durable runtime record returned by the trusted "
            "Workforce evidence endpoint. Workforce verified the stored evidence hashes before projection; Minerva "
            "preserved those hashes but did not claim independent recomputation. Minerva did not evaluate "
            "Award applicability, select a winner, resolve a RateSource, calculate pay, substitute a current "
            "AwardVersion, or use configuration-only evidence as proof of worker execution."
        ),
        explanationFingerprint=hashlib.sha256(
            _canonical(
                {
                    "accountId": account_id,
                    "decisionEvidence": evidence.model_dump(mode="json"),
                }
            )
        ).hexdigest(),
        presentationMode=request.presentationMode,
        presentation=presentation,
        storedExecutionEvidenceUsed=True,
        configurationExplanationUsed=False,
        independentAwardRecomputationPerformed=False,
        noChangesMade=True,
    )


def ask_award_execution_question(
    request: AwardExecutionMinervaQuestionRequest,
    evidence_provider: AwardExecutionEvidenceProvider,
    account_id: str,
) -> AwardExecutionMinervaQuestionResponse:
    evidence = evidence_provider.fetch(
        str(request.calcInterpreterLineId),
        str(request.awardVersionId),
        account_id,
    )
    return compose_award_execution_explanation(request, evidence, account_id)


__all__ = ["ask_award_execution_question", "compose_award_execution_explanation"]

from __future__ import annotations

from app.schemas.award_studio_minerva import (
    ANSWER_CONTRACT_VERSION,
    AwardAnswerPresentation,
    AwardEvidenceCard,
    AwardStudioMinervaQuestionRequest,
    AwardStudioMinervaQuestionResponse,
)
from app.services.award_studio_answer_planner import build_answer_plan


def _presentation(request: AwardStudioMinervaQuestionRequest, plan) -> AwardAnswerPresentation:
    projection = request.projection
    evidence_by_id = {item.evidenceIdentity: item for item in projection.evidence}
    node_by_id = {item.semanticIdentity: item for item in projection.semanticNodes}
    selected_payloads = [
        item
        for item in projection.presentationPayloads
        if item.presentationKey.upper() in {plan.questionClassification, *plan.semanticIdentities}
    ]
    evidence_cards = [
        AwardEvidenceCard(
            evidenceIdentity=item.evidenceIdentity,
            sourceTitle=item.sourceTitle,
            sourceLocator=item.sourceLocator,
            sourceSha256=item.sourceSha256,
        )
        for evidence_id in plan.evidenceIdentities
        if (item := evidence_by_id.get(evidence_id)) is not None
    ]
    anchors = [
        node.workspaceAnchor
        for semantic_id in plan.semanticIdentities
        if (node := node_by_id.get(semantic_id)) is not None and node.workspaceAnchor
    ]
    for payload in selected_payloads:
        anchors.extend(payload.workspaceAnchors)
    anchors = list(dict.fromkeys(anchors))
    detail = list(plan.whatMatters)
    for payload in selected_payloads:
        detail.extend(payload.expandableDetail)
    detail = list(dict.fromkeys(detail))
    if request.presentationMode == "LEVEL_2":
        spoken = selected_payloads[0].conciseSpokenSummary if selected_payloads else plan.directDeterministicAnswer
        subtitles = [line for payload in selected_payloads for line in payload.subtitles] or [spoken]
    else:
        spoken = None
        subtitles = []
    sequence = [
        payload.presentationKey
        for payload in sorted(selected_payloads, key=lambda item: item.recommendedSequence)
    ] or list(plan.semanticIdentities)
    return AwardAnswerPresentation(
        mode=request.presentationMode,
        conciseSummary=plan.directDeterministicAnswer,
        spokenSummary=spoken,
        subtitles=subtitles,
        expandableDetail=detail,
        evidenceCards=evidence_cards,
        workspaceAnchors=anchors,
        recommendedSequence=sequence,
    )


def ask_award_studio_question(
    request: AwardStudioMinervaQuestionRequest,
) -> AwardStudioMinervaQuestionResponse:
    plan = build_answer_plan(request)
    authority = request.projection.authorityEnvelope
    return AwardStudioMinervaQuestionResponse(
        contractVersion=ANSWER_CONTRACT_VERSION,
        requestIdentity=request.requestIdentity,
        awardHeaderId=authority.awardHeaderId,
        awardVersionId=authority.awardVersionId,
        awardCode=authority.awardCode,
        configurationFingerprint=authority.configurationFingerprint,
        semanticGraphFingerprint=authority.semanticGraphFingerprint,
        sourceAuthorityFingerprint=authority.sourceAuthorityFingerprint,
        projectionFingerprint=authority.projectionFingerprint,
        projectionSchemaVersion=authority.projectionSchemaVersion,
        questionClassification=plan.questionClassification,
        answerClassification=plan.answerClassification,
        answer=plan.directDeterministicAnswer,
        whatMatters=plan.whatMatters,
        semanticIdentities=plan.semanticIdentities,
        relationshipIdentities=plan.relationshipIdentities,
        evidenceIdentities=plan.evidenceIdentities,
        holdIdentities=plan.holdIdentities,
        completenessConceptCodes=plan.completenessConceptCodes,
        boundary=plan.boundary,
        safeNextStep=plan.safeNextStep,
        plannerFingerprint=plan.plannerFingerprint,
        presentationMode=request.presentationMode,
        presentation=_presentation(request, plan),
        deterministicAnswerUsed=True,
        generalCorpusUsedAsConfiguredAuthority=False,
        workerDecisionEvidenceIncluded=False,
        noChangesMade=True,
    )


__all__ = ["ask_award_studio_question"]

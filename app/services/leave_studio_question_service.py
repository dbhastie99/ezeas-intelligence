from __future__ import annotations

import hashlib
import logging
import time

from app.schemas.leave_studio_minerva import (
    ANSWER_CONTRACT_VERSION,
    LeaveStudioAnswerResponse,
    LeaveStudioQuestionRequest,
)
from app.services.leave_studio_answer_planner import build_answer_plan
from app.services.leave_studio_openai_renderer import render_optional_answer


logger = logging.getLogger("minerva.leave_studio_question")


def ask_leave_studio_question(
    request: LeaveStudioQuestionRequest,
    *,
    settings=None,
    client_factory=None,
) -> LeaveStudioAnswerResponse:
    started = time.perf_counter()
    plan = build_answer_plan(request)
    rendering = render_optional_answer(plan, settings=settings, client_factory=client_factory)
    answer = rendering.answer if rendering.used and rendering.answer else plan.DirectDeterministicAnswer
    duration_ms = max(0, round((time.perf_counter() - started) * 1000))
    output_hash = hashlib.sha256(answer.encode("utf-8")).hexdigest()
    response = LeaveStudioAnswerResponse(
        ContractVersion=ANSWER_CONTRACT_VERSION,
        RequestId=request.RequestId,
        Answer=answer,
        AnswerMode=plan.QuestionClassification,
        WhatMatters=plan.WhatMatters,
        Boundary=plan.Boundary,
        SafeNextStep=plan.SafeNextStep,
        EvidenceReferences=plan.EvidenceReferences,
        FactIds=plan.FactIds,
        FactAuthorityClasses=plan.FactAuthorityClasses,
        MissingOrUnresolvedFacts=plan.MissingOrUnresolvedFacts,
        ReadinessState=plan.ReadinessState,
        RuntimeSupportState=plan.RuntimeSupportState,
        LeaveTypeVersionId=plan.LeaveTypeVersionId,
        StudioContextSchemaVersion=request.StudioContextSchemaVersion,
        StudioContextFingerprint=request.StudioContextFingerprint,
        PlannerFingerprint=plan.PlannerFingerprint,
        RendererEligible=rendering.eligible,
        RendererAttempted=rendering.attempted,
        RendererUsed=rendering.used,
        RendererModelIdentifier=rendering.model_identifier if rendering.used else None,
        RendererInstructionVersion=rendering.instruction_version,
        RendererConfigurationFingerprint=rendering.configuration_fingerprint,
        RendererFallbackReason=rendering.fallback_reason,
        OutputHash=output_hash,
        DurationMs=duration_ms,
        NoChangesMade=True,
    )
    logger.info(
        "leave_studio_question_completed",
        extra={
            "request_id": request.RequestId,
            "contract_version": request.ContractVersion,
            "leave_type_version_id": request.LeaveTypeVersionId,
            "studio_context_fingerprint": request.StudioContextFingerprint,
            "question_classification": plan.QuestionClassification,
            "answer_plan_fingerprint": plan.PlannerFingerprint,
            "renderer_eligible": rendering.eligible,
            "renderer_attempted": rendering.attempted,
            "renderer_used": rendering.used,
            "renderer_model_identifier": response.RendererModelIdentifier,
            "renderer_fallback_reason": rendering.fallback_reason,
            "output_hash": output_hash,
            "duration_ms": duration_ms,
        },
    )
    return response

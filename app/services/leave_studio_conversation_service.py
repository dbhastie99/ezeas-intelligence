from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Protocol

import httpx
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.schemas.leave_studio_minerva import (
    LeaveStudioConversationRequest,
    LeaveStudioConversationResponse,
    LeaveStudioLiveModelDocument,
)
from app.services.audit_service import write_ai_interaction_audit
from app.services.openai_compatible_json_client import JsonCompletion, OpenAICompatibleJsonClient


PROMPT_INSTRUCTION_VERSION = "LEAVE_STUDIO_LIVE_CONVERSATION_V1"


class ConversationValidationFailure(ValueError):
    pass


class ConversationClient(Protocol):
    def complete(
        self,
        *,
        system_instruction: str,
        user_payload: str,
        model: str,
        timeout_seconds: float,
        max_tokens: int,
        metadata: dict[str, str],
        response_schema: dict | None = None,
    ) -> JsonCompletion: ...


@dataclass(frozen=True)
class CompositionOutcome:
    document: LeaveStudioLiveModelDocument | None
    attempted: bool
    used: bool
    model: str | None
    latency_ms: int | None
    fallback_reason: str | None


def canonical_context_fingerprint(request: LeaveStudioConversationRequest) -> str:
    payload = json.dumps(
        request.ContextPacket.model_dump(mode="json"),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def provider_configuration_fingerprint(settings: Settings) -> str:
    safe = {
        "enabled": settings.leave_studio_conversation_enabled,
        "provider": settings.llm_provider,
        "base_url_configured": bool(settings.llm_base_url),
        "credential_configured": bool(settings.llm_api_key),
        "model": settings.llm_model,
        "timeout_seconds": settings.leave_studio_conversation_timeout_seconds,
        "max_output_chars": settings.leave_studio_conversation_max_output_chars,
        "max_history_turns": settings.leave_studio_conversation_max_history_turns,
        "max_history_chars": settings.leave_studio_conversation_max_history_chars,
        "instruction_version": PROMPT_INSTRUCTION_VERSION,
        "automatic_retries": 0,
        "tools_enabled": False,
        "browsing_enabled": False,
    }
    return hashlib.sha256(json.dumps(safe, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _system_instruction(persona: str) -> str:
    persona_style = {
        "ADMINISTRATOR": "Explain like a knowledgeable payroll and Leave administration colleague. Emphasise configuration and operational consequence without unnecessary legalism.",
        "LEGAL": "Use structured propositions, authority identities, evidence, reasoning, provenance and explicit uncertainty. Distinguish evidence from inference.",
        "MANAGER": "Use practical circumstance, responsibility, consequence and next-step language. Avoid configuration detail unless essential to the question.",
        "WORKER": "Use friendly plain English focused on conditions, outcomes and what the worker should know. Avoid schema and configuration language.",
    }[persona]
    return (
        "You are Minerva, a bounded explanation and composition layer for ezeas Leave Studio. "
        "The supplied LEAVE_STUDIO_LLM_CONTEXT_V3 packet is the sole factual authority. "
        "Do not use model memory, browse, retrieve URLs, invoke tools, query databases, invent law, sources, facts, calculations, worker outcomes, persistence, or actions. "
        "Conversation history is only for continuity and coreference; prior assistant turns are never factual authority. "
        "If the packet does not contain the answer, say that the information is unavailable in this policy context and do not guess. "
        "Never claim to change, publish, approve, calculate or mutate anything. "
        "Treat SUPPORTED_GUIDANCE_ONLY as no persistence: do not say a setting can be changed, adjusted, customised, edited, saved or persisted unless AvailableGovernedActions contains an explicit supported CHANGE action. "
        f"{persona_style} "
        "Return exactly one JSON object with Answer, KeyPoints, Boundary, GroundingIdentities, SuggestedFollowUps and Persona. "
        "Use at most five concise key points and three follow-ups. GroundingIdentities must contain only exact identifiers from the packet. "
        "Do not return HTML, markdown links, source URLs, evidence titles, tool calls or action envelopes."
    )


def _allowed_grounding(request: LeaveStudioConversationRequest) -> set[str]:
    packet = request.ContextPacket
    allowed = {
        packet.PolicyKey,
        packet.PackageCode,
        packet.LeaveTypeVersionId,
        packet.VersionCode,
    } | set(packet.AuthorityIdentities) | set(packet.EvidenceIdentities)
    for scenario in packet.PreparedScenarios:
        if scenario.get("ScenarioCode"):
            allowed.add(str(scenario["ScenarioCode"]))
        allowed.update(str(item) for item in scenario.get("EvidenceIdentities", []))
    for category in packet.ManagementCategories:
        for field in category.get("Fields", []):
            if field.get("FieldIdentity"):
                allowed.add(str(field["FieldIdentity"]))
            allowed.update(str(item) for item in field.get("EvidenceIdentities", []))
            allowed.update(str(item) for item in field.get("ConfiguredValueSourceIdentities", []))
            allowed.update(str(item.get("SourceCode")) for item in field.get("Provenance", []) if item.get("SourceCode"))
    for hold in packet.Holds:
        if hold.get("HoldCode"):
            allowed.add(str(hold["HoldCode"]))
    return allowed


def _all_output_text(document: LeaveStudioLiveModelDocument) -> str:
    return " ".join([document.Answer, *document.KeyPoints, document.Boundary, *document.SuggestedFollowUps])


def validate_live_document(
    raw: str,
    request: LeaveStudioConversationRequest,
    *,
    max_output_chars: int,
) -> LeaveStudioLiveModelDocument:
    if not isinstance(raw, str) or not raw.strip() or len(raw) > max_output_chars:
        raise ConversationValidationFailure("model output is empty or exceeds the configured limit")
    try:
        document = LeaveStudioLiveModelDocument.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        raise ConversationValidationFailure("model output is not the expected JSON contract") from exc
    if document.Persona != request.Persona:
        raise ConversationValidationFailure("model output changed persona")
    allowed = _allowed_grounding(request)
    if not document.GroundingIdentities or not set(document.GroundingIdentities).issubset(allowed):
        raise ConversationValidationFailure("model output contains missing or foreign grounding identities")
    text = _all_output_text(document)
    if re.search(r"https?://|www\.|<[^>]+>|javascript:|\[[^]]+\]\([^)]+\)", text, re.I):
        raise ConversationValidationFailure("model output contains untrusted markup or a URL")
    if re.search(r"\b(?:i|we|minerva)\s+(?:changed|updated|published|approved|created|calculated)\b", text, re.I):
        raise ConversationValidationFailure("model output claims a prohibited action")
    change_action_supported = any(
        (
            str(action.get("ActionCode", "")).upper() == "CHANGE"
            or "CHANGE" in {str(item).upper() for item in action.get("actions", [])}
        )
        and str(action.get("capability", action.get("Capability", ""))).upper()
        not in {"SUPPORTED_GUIDANCE_ONLY", "UNSUPPORTED_PRODUCT_DEPENDENCY", "UNAVAILABLE_PRODUCT_DEPENDENCY", "PROHIBITED"}
        for action in request.ContextPacket.AvailableGovernedActions
    )
    if not change_action_supported and re.search(
        r"\b(?:can|may|could)\s+be\s+(?:changed|adjusted|customi[sz]ed|edited|saved|persisted)\b|"
        r"\b(?:users?|organisations?)\s+can\s+(?:change|adjust|customi[sz]e|edit|save|persist)\b",
        text,
        re.I,
    ):
        raise ConversationValidationFailure("model output overstates a governed change capability")
    if re.search(r"\b(?:tool_call|function_call|authorization|api[_ -]?key)\b", text, re.I):
        raise ConversationValidationFailure("model output contains a tool or secret envelope")
    context_text = request.ContextPacket.model_dump_json().lower()
    output_numbers = set(re.findall(r"(?<![a-z0-9])\d+(?:\.\d+)?(?![a-z0-9])", text.lower()))
    context_numbers = set(re.findall(r"(?<![a-z0-9])\d+(?:\.\d+)?(?![a-z0-9])", context_text))
    if output_numbers - context_numbers:
        raise ConversationValidationFailure("model output introduced an unsupported numerical value")
    return document


def _target_field(request: LeaveStudioConversationRequest) -> dict | None:
    identity = request.ContextPacket.TargetFieldIdentity
    if not identity:
        return None
    for category in request.ContextPacket.ManagementCategories:
        for field in category.get("Fields", []):
            if field.get("FieldIdentity") == identity:
                return field
    raise ConversationValidationFailure("target field is absent from the current context")


def _target_scenario(request: LeaveStudioConversationRequest) -> dict | None:
    code = request.ContextPacket.TargetScenarioCode
    if not code:
        return None
    for scenario in request.ContextPacket.PreparedScenarios:
        if scenario.get("ScenarioCode") == code:
            return scenario
    raise ConversationValidationFailure("target scenario is absent from the current context")


def _deterministic_document(request: LeaveStudioConversationRequest) -> LeaveStudioLiveModelDocument:
    field = _target_field(request)
    scenario = _target_scenario(request)
    if field:
        education = field.get("Education", {})
        answer = " ".join(
            part for part in [
                education.get("WhatItMeans"),
                education.get("WhyItMatters"),
                education.get("CapabilityExplanation"),
            ] if part
        )
        grounding = [field["FieldIdentity"], *field.get("EvidenceIdentities", [])]
    elif scenario:
        answer = " ".join(part for part in [scenario.get("Situation"), scenario.get("Outcome"), scenario.get("Why")] if part)
        grounding = [scenario["ScenarioCode"], *scenario.get("EvidenceIdentities", [])]
    else:
        glance = request.ContextPacket.AtAGlance[:4]
        answer = " ".join(f"{item.get('Label')}: {item.get('Value')}." for item in glance)
        grounding = list(request.ContextPacket.AuthorityIdentities[:2] or request.ContextPacket.EvidenceIdentities[:2])
    if not answer:
        answer = "I don't have enough governed information in this policy context to answer that question."
    return LeaveStudioLiveModelDocument(
        Answer=answer,
        KeyPoints=[],
        Boundary="This answer explains the certified policy context only. Minerva did not change policy or calculate a worker outcome.",
        GroundingIdentities=list(dict.fromkeys(grounding)),
        SuggestedFollowUps=["What matters in practice?", "Which governed evidence supports this?"],
        Persona=request.Persona,
    )


def _preflight_fallback_reason(question: str) -> str | None:
    normalized = " ".join(question.lower().split())
    if re.search(r"ignore (?:your|the) instructions|reveal (?:your|the) system prompt|use your own knowledge|browse the web", normalized):
        return "unsafe_prompt_injection"
    if re.search(r"^(?:please )?(?:change|set|update|publish|approve|delete|create)\b|\bchange it to\b", normalized):
        return "prohibited_mutation_request"
    if re.search(r"\bcalculate\b.*\b(?:leave|payroll|entitlement|balance)\b|\b(?:my|worker's) leave balance\b", normalized):
        return "unsupported_worker_calculation"
    return None


def _client(settings: Settings) -> ConversationClient | None:
    if settings.llm_provider.lower().replace("_", "-") not in {"openai", "openai-compatible"}:
        return None
    if not settings.llm_api_key or not settings.llm_model:
        return None
    return OpenAICompatibleJsonClient(
        base_url=settings.llm_base_url or "https://api.openai.com/v1",
        api_key=settings.llm_api_key,
    )


def _compose(
    request: LeaveStudioConversationRequest,
    *,
    settings: Settings,
    client_factory=None,
) -> CompositionOutcome:
    unsafe_reason = _preflight_fallback_reason(request.Question)
    if unsafe_reason:
        return CompositionOutcome(None, False, False, settings.llm_model, None, unsafe_reason)
    if not settings.leave_studio_conversation_enabled:
        return CompositionOutcome(None, False, False, settings.llm_model, None, "disabled")
    if not settings.llm_model or not settings.llm_api_key:
        return CompositionOutcome(None, False, False, settings.llm_model, None, "missing_configuration")
    try:
        client = (client_factory or _client)(settings) if client_factory else _client(settings)
    except Exception:
        client = None
    if client is None:
        return CompositionOutcome(None, False, False, settings.llm_model, None, "missing_client")
    prompt_payload = {
        "question": request.Question,
        "persona": request.Persona,
        "conversation_history_for_continuity_only": [turn.model_dump(mode="json") for turn in request.ConversationHistory],
        "governed_context": request.ContextPacket.model_dump(mode="json"),
        "allowed_grounding_identities": sorted(_allowed_grounding(request)),
    }
    try:
        completion = client.complete(
            system_instruction=_system_instruction(request.Persona),
            user_payload=json.dumps(prompt_payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")),
            model=settings.llm_model,
            timeout_seconds=settings.leave_studio_conversation_timeout_seconds,
            max_tokens=min(1400, max(128, settings.leave_studio_conversation_max_output_chars // 4)),
            metadata={"instruction_version": PROMPT_INSTRUCTION_VERSION},
            response_schema={
                "name": "leave_studio_minerva_answer",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "Answer": {"type": "string"},
                        "KeyPoints": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
                        "Boundary": {"type": "string"},
                        "GroundingIdentities": {"type": "array", "items": {"type": "string"}, "maxItems": 30},
                        "SuggestedFollowUps": {"type": "array", "items": {"type": "string"}, "maxItems": 3},
                        "Persona": {"type": "string", "enum": [request.Persona]},
                    },
                    "required": ["Answer", "KeyPoints", "Boundary", "GroundingIdentities", "SuggestedFollowUps", "Persona"],
                },
            },
        )
        document = validate_live_document(
            completion.content,
            request,
            max_output_chars=settings.leave_studio_conversation_max_output_chars,
        )
        return CompositionOutcome(document, True, True, settings.llm_model, completion.latency_ms, None)
    except (TimeoutError, httpx.TimeoutException):
        reason = "timeout"
    except ConversationValidationFailure as exc:
        validation_codes = {
            "model output is not the expected JSON contract": "validation_contract",
            "model output changed persona": "validation_persona",
            "model output contains missing or foreign grounding identities": "validation_grounding",
            "model output contains untrusted markup or a URL": "validation_markup",
            "model output claims a prohibited action": "validation_action_claim",
            "model output overstates a governed change capability": "validation_capability_claim",
            "model output contains a tool or secret envelope": "validation_tool_or_secret_envelope",
            "model output introduced an unsupported numerical value": "validation_unsupported_number",
        }
        reason = validation_codes.get(str(exc), "validation_failure")
    except (httpx.HTTPError, OSError):
        reason = "provider_unavailable"
    except Exception:
        reason = "provider_error"
    return CompositionOutcome(None, True, False, settings.llm_model, None, reason)


def _audit(
    db: Session,
    request: LeaveStudioConversationRequest,
    response: LeaveStudioLiveModelDocument,
    outcome: CompositionOutcome,
    response_fingerprint: str,
    settings: Settings,
) -> str:
    metadata = {
        "request_identity": request.RequestIdentity,
        "conversation_turn_identity": request.ConversationTurnIdentity,
        "policy_key": request.ContextPacket.PolicyKey,
        "leave_type_version_id": request.ContextPacket.LeaveTypeVersionId,
        "baseline_content_hash": request.ContextPacket.BaselineContentHash,
        "context_packet_fingerprint": request.ContextPacketFingerprint,
        "context_contract_version": request.ContextPacket.ContractVersion,
        "persona": request.Persona,
        "model": outcome.model,
        "prompt_instruction_version": PROMPT_INSTRUCTION_VERSION,
        "live_call_attempted": outcome.attempted,
        "live_call_used": outcome.used,
        "fallback_reason": outcome.fallback_reason,
        "grounding_identities": response.GroundingIdentities,
        "response_fingerprint": response_fingerprint,
        "provider_latency_ms": outcome.latency_ms,
        "audit_outcome": "LIVE_ACCEPTED" if outcome.used else "GOVERNED_FALLBACK",
        "provider_configuration_fingerprint": provider_configuration_fingerprint(settings),
        "secrets_recorded": False,
    }
    record = write_ai_interaction_audit(
        db=db,
        user_question=f"LEAVE_STUDIO_LIVE_REQUEST:{request.RequestIdentity}",
        response_text=json.dumps(metadata, sort_keys=True, separators=(",", ":")),
        source_references=[],
        model_name=outcome.model or "DETERMINISTIC_FALLBACK",
        prompt_policy=PROMPT_INSTRUCTION_VERSION,
    )
    return record.AIInteractionAuditId


def ask_leave_studio_conversation(
    request: LeaveStudioConversationRequest,
    *,
    db: Session,
    settings: Settings | None = None,
    client_factory=None,
) -> LeaveStudioConversationResponse:
    settings = settings or get_settings()
    if canonical_context_fingerprint(request) != request.ContextPacketFingerprint:
        raise ConversationValidationFailure("context packet fingerprint mismatch")
    if len(request.ConversationHistory) > settings.leave_studio_conversation_max_history_turns:
        raise ConversationValidationFailure("conversation history exceeds the configured turn limit")
    if sum(len(turn.Content) for turn in request.ConversationHistory) > settings.leave_studio_conversation_max_history_chars:
        raise ConversationValidationFailure("conversation history exceeds the configured character limit")
    outcome = _compose(request, settings=settings, client_factory=client_factory)
    document = outcome.document or _deterministic_document(request)
    output_fingerprint = hashlib.sha256(document.Answer.encode("utf-8")).hexdigest()
    audit_identity = _audit(db, request, document, outcome, output_fingerprint, settings)
    return LeaveStudioConversationResponse(
        ContractVersion="EZEAS_INTELLIGENCE_LEAVE_STUDIO_RESPONSE_V1",
        RequestIdentity=request.RequestIdentity,
        ConversationTurnIdentity=request.ConversationTurnIdentity,
        PolicyKey=request.ContextPacket.PolicyKey,
        LeaveTypeVersionId=request.ContextPacket.LeaveTypeVersionId,
        BaselineContentHash=request.ContextPacket.BaselineContentHash,
        ContextPacketFingerprint=request.ContextPacketFingerprint,
        Persona=request.Persona,
        Answer=document.Answer,
        KeyPoints=document.KeyPoints,
        Boundary=document.Boundary,
        GroundingIdentities=document.GroundingIdentities,
        SuggestedFollowUps=document.SuggestedFollowUps,
        LiveLlmAttempted=outcome.attempted,
        LiveLlmUsed=outcome.used,
        ModelIdentifier=outcome.model if outcome.attempted else None,
        PromptInstructionVersion=PROMPT_INSTRUCTION_VERSION,
        ProviderLatencyMs=outcome.latency_ms,
        AuditIdentity=audit_identity,
        OutputFingerprint=output_fingerprint,
        FallbackReason=outcome.fallback_reason,
        NoChangesMade=True,
    )


__all__ = [
    "ConversationValidationFailure",
    "PROMPT_INSTRUCTION_VERSION",
    "ask_leave_studio_conversation",
    "canonical_context_fingerprint",
    "provider_configuration_fingerprint",
    "validate_live_document",
]

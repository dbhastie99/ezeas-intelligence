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


PROMPT_INSTRUCTION_VERSION = "LEAVE_STUDIO_LIVE_CONVERSATION_V2"


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
        "Facts asserted in the user's question or conversation history are not governed worker facts and must not be treated as verified. "
        "If the packet does not contain the answer, say that the information is unavailable in this policy context and do not guess. "
        "Absence is not proof of the opposite: if a criterion is not identified in the governed packet, say only that it 'is not identified as a factor in this governed policy context'. Stop that proposition there. "
        "For age, 'Age is not identified as a factor in this governed policy context' is permitted; 'age is not a factor', 'age does not affect entitlement', 'regardless of age', 'whatever the age', and any therefore/so conclusion about age are prohibited unless that universal proposition is explicit in the packet. "
        "Keep recognised service commencement, accumulation and counting distinct from entitlement access, vesting, qualification and payment. Service beginning or being counted does not itself establish that an entitlement has started, is accessible, has vested, is payable, or that a worker qualifies. "
        "Do not use the ambiguous phrases 'entitlement starts', 'entitlement begins', 'entitlement commences', 'entitlement accrues from employment', or their personal equivalents when answering a service or long-service question. Use the precise state names instead: recognised service begins/is counted; entitlement access depends on the governed threshold and conditions; vesting and payment are separate where the packet supports them. "
        "WorkerSpecificContextIncluded=false. Answer first-person questions at policy level and do not determine or imply an individual outcome, including that the user is entitled or eligible, qualifies, has vested, can access an entitlement, has a balance or payable entitlement, or that their entitlement starts. "
        "For a first-person entitlement, eligibility, qualification, vesting, access, balance or payment question, explicitly say that worker-specific governed facts were not included and Minerva cannot determine the individual's outcome. Hypothetical policy consequences remain allowed when clearly conditional and grounded. "
        "Before returning JSON, check every Answer, KeyPoint and Boundary proposition: (1) no absent criterion became a universal conclusion; (2) recognised service was not described as entitlement commencement or access; and (3) no individual result was stated. "
        "For every first-person outcome question, the Boundary field must contain both propositions: worker-specific governed facts were not included, and Minerva cannot determine the individual's entitlement or access. "
        "Never claim to change, publish, approve, calculate or mutate anything. "
        "Treat SUPPORTED_GUIDANCE_ONLY as no persistence: do not say a setting can be changed, adjusted, customised, edited, saved or persisted unless AvailableGovernedActions contains an explicit supported CHANGE action. "
        "When explaining a hypothetical alternative or derived policy, put the current unavailable/unsupported boundary in the same sentence as any can, may or could wording. "
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


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|[\r\n]+", text) if part.strip()]


def _question_requests_personal_outcome(question: str) -> bool:
    first_person = re.search(r"\b(?:i|me|my|mine|we|our)\b", question, re.I)
    outcome = re.search(
        r"\b(?:entitl(?:e|ed|ement)|eligib(?:le|ility)|qualif(?:y|ied|ication)|vest(?:ed|ing)?|"
        r"access|balance|payable|payment|service start|service begin|first day|start(?:ed|ing)? at)\b",
        question,
        re.I,
    )
    return bool(first_person and outcome)


def _is_boundary_or_hypothetical(sentence: str, match_start: int) -> bool:
    prefix = sentence[:match_start]
    if re.search(r"\b(?:if|whether|assuming|hypothetically|in a hypothetical|where a worker|when a worker)\b", prefix, re.I):
        return True
    return bool(
        re.search(
            r"\b(?:cannot|can't|does not|doesn't|is unable to|is not able to|not enough\b.{0,40})"
            r".{0,60}\b(?:determine|decide|confirm|establish|verify|resolve|calculate|say whether)\b|"
            r"\b(?:not a|isn't a|is not an?)\s+(?:personal|individual|worker-specific)\s+(?:determination|outcome|calculation)\b|"
            r"\bwithout\b.{0,60}\bworker-specific\b.{0,60}\b(?:cannot|can't|not possible)\b",
            sentence,
            re.I,
        )
    )


def _contains_personal_outcome_determination(text: str) -> bool:
    claim = re.compile(
        r"\b(?:you\s+(?:are|remain|become|became|will be|have become)|you're|"
        r"(?:the worker|this worker|the employee|this employee)\s+"
        r"(?:is|remain(?:s)?|become(?:s)?|became|will be|has become))\s+(?:now\s+)?"
        r"(?:entitled|eligible|qualified|vested)\b|"
        r"\b(?:you\s+(?:have |have now |can |can now |may |may now )?|you've\s+|"
        r"(?:the worker|this worker|the employee|this employee)\s+(?:has |has now |can |can now |may |may now )?)"
        r"(?:qualif(?:y|ies|ied)|access(?:es|ed)?|take|vest(?:s|ed)?)\b|"
        r"\b(?:your|the worker's|the employee's)\s+"
        r"(?:entitlement|eligibility|qualification|access)\s+"
        r"(?:starts?|started|begins?|began|commences?|commenced|dates? from|runs? from|vests?|vested|is|was|becomes?|became|will)\b|"
        r"\b(?:your|the worker's|the employee's)\s+(?:balance|payable entitlement)\s+"
        r"(?:is|was|has|equals?|stands? at|becomes?|will)\b",
        re.I,
    )
    for sentence in _sentences(text):
        for match in claim.finditer(sentence):
            if not _is_boundary_or_hypothetical(sentence, match.start()):
                return True
    return False


def _has_worker_context_boundary(text: str) -> bool:
    for sentence in _sentences(text):
        missing_context = re.search(
            r"\b(?:worker-specific|individual worker|personal worker)\b.{0,90}"
            r"\b(?:not (?:included|supplied|available|provided)|unavailable|absent|missing|excluded)\b|"
            r"\b(?:no|without)\s+(?:governed\s+)?(?:individual worker|worker-specific)\b|"
            r"\b(?:does not|doesn't|do not|don't)\s+(?:contain|include|have)\b.{0,60}\bworker-specific\b",
            sentence,
            re.I,
        )
        cannot_determine = re.search(
            r"\b(?:cannot|can't|does not|doesn't|is unable to|is not able to)\b.{0,80}"
            r"\b(?:determine|decide|confirm|establish|verify|resolve|calculate|say whether)\b.{0,80}"
            r"\b(?:individual|personal|your|worker)\b.{0,50}\b(?:outcome|entitlement|eligibility|qualification|access|balance|payment)\b",
            sentence,
            re.I,
        )
        if missing_context or cannot_determine:
            return True
    return False


def _context_explicitly_supports_universal_age_claim(request: LeaveStudioConversationRequest) -> bool:
    context_text = request.ContextPacket.model_dump_json().lower()
    return bool(
        re.search(
            r"\b(?:regardless|irrespective) of (?:the worker's |your )?age\b|"
            r"\bwhatever (?:the worker's |your )?age\b|"
            r"\bage\s+(?:never|cannot|can't|does not|doesn't|will not|won't)\s+"
            r"(?:matter|affect|change|influence|determine)\b|"
            r"\bage has no bearing on\b|"
            r"\bage is (?:irrelevant|not a factor|not relevant)\b|"
            r"\bno age (?:limit|restriction|requirement|criterion|condition)\b",
            context_text,
            re.I,
        )
    )


def _contains_unsupported_universal_age_claim(text: str, request: LeaveStudioConversationRequest) -> bool:
    universal_pattern = re.compile(
        r"\b(?:regardless|irrespective) of (?:the worker's |your )?age\b|"
        r"\bwhatever (?:the worker's |your )?age\b|"
        r"\bage\s+(?:never|cannot|can't|does not|doesn't|will not|won't)\s+"
        r"(?:matter|affect|change|influence|determine)\b|"
        r"\bage has no bearing on\b|"
        r"\bage is (?:irrelevant|not a factor|not relevant)\b|"
        r"\bno age (?:limit|restriction|requirement|criterion|condition)\b",
        re.I,
    )
    for sentence in _sentences(text):
        for universal_claim in universal_pattern.finditer(sentence):
            negating_prefix = sentence[max(0, universal_claim.start() - 100):universal_claim.start()]
            rejects_combined_assumption = re.search(
                r"\b(?:not simply|not automatically|does not (?:mean|establish|show|prove|make)|"
                r"doesn't (?:mean|establish|show|prove|make)|cannot be assumed|can't be assumed|"
                r"cannot be concluded|can't be concluded)\b",
                negating_prefix,
                re.I,
            )
            if not rejects_combined_assumption and not _context_explicitly_supports_universal_age_claim(request):
                return True
    context_text = request.ContextPacket.model_dump_json().lower()
    for sentence in _sentences(text):
        for regardless_claim in re.finditer(r"\b(?:regardless|irrespective) of\s+([^,.;!?]{1,80})", sentence, re.I):
            negating_prefix = sentence[max(0, regardless_claim.start() - 100):regardless_claim.start()]
            rejects_combined_assumption = re.search(
                r"\b(?:not simply|not automatically|does not (?:mean|establish|show|prove|make)|"
                r"doesn't (?:mean|establish|show|prove|make)|cannot be assumed|can't be assumed|"
                r"cannot be concluded|can't be concluded)\b",
                negating_prefix,
                re.I,
            )
            supported_age_claim = bool(
                re.search(r"\bage\b", regardless_claim.group(0), re.I)
                and _context_explicitly_supports_universal_age_claim(request)
            )
            if (
                not rejects_combined_assumption
                and not supported_age_claim
                and regardless_claim.group(0).lower() not in context_text
            ):
                return True
    return bool(
        re.search(
            r"\b(?:not identified|not mentioned|does not identify|doesn't identify|does not mention|doesn't mention)\b"
            r".{0,100}\b(?:therefore|so|which means)\b.{0,100}"
            r"\b(?:never|cannot|can't|does not|doesn't|regardless|irrespective)\b",
            text,
            re.I,
        )
    )


def _contains_service_entitlement_conflation(text: str, question: str) -> bool:
    precision_relevant = re.search(
        r"\b(?:recogni[sz]ed service|service (?:start|begin|accru|count)|long service|employment|first day|age)\b",
        f"{question} {text}",
        re.I,
    )
    if not precision_relevant:
        return False
    if re.search(
        r"\b(?:your |the |an? )?entitlement\s+(?:starts?|started|begins?|began|commences?|commenced|"
        r"dates? from|runs? from|has accrued|accrues?|accumulated)\b|"
        r"\b(?:recogni[sz]ed )?service\b.{0,100}\b(?:therefore|so|which means|means that)\b.{0,100}"
        r"\b(?:entitled|eligible|qualif(?:y|ies|ied)|access(?:ible)?|vest(?:s|ed)?|payable)\b",
        text,
        re.I,
    ):
        return True
    service_commencement = re.search(
        r"\brecogni[sz]ed service\b.{0,60}\b(?:starts?|begins?|commences?|accrues?|accumulates?|is counted)\b|"
        r"\b(?:starts?|begins?|commences?|accrues?|accumulates?|is counted)\b.{0,60}\brecogni[sz]ed service\b",
        text,
        re.I,
    )
    access_distinction = re.search(
        r"\b(?:entitlement access|access to (?:an |the )?entitlement|vesting|vests?|payable|payment|qualification|qualifies|service threshold)\b|"
        r"\bdoes not (?:itself )?(?:grant|establish|mean|make)\b",
        text,
        re.I,
    )
    return bool(service_commencement and not access_distinction)


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
    if _contains_unsupported_universal_age_claim(text, request):
        raise ConversationValidationFailure("model output turns absent criteria into a universal conclusion")
    if _contains_service_entitlement_conflation(text, request.Question):
        raise ConversationValidationFailure("model output conflates recognised service with entitlement access")
    if not request.ContextPacket.WorkerSpecificContextIncluded:
        if _contains_personal_outcome_determination(text):
            raise ConversationValidationFailure("model output makes a worker-specific outcome determination")
        if _question_requests_personal_outcome(request.Question) and not _has_worker_context_boundary(text):
            raise ConversationValidationFailure("model output omits the worker-specific context boundary")
    change_action_supported = any(
        (
            str(action.get("ActionCode", "")).upper() == "CHANGE"
            or "CHANGE" in {str(item).upper() for item in action.get("actions", [])}
        )
        and str(action.get("capability", action.get("Capability", ""))).upper()
        not in {"SUPPORTED_GUIDANCE_ONLY", "UNSUPPORTED_PRODUCT_DEPENDENCY", "UNAVAILABLE_PRODUCT_DEPENDENCY", "PROHIBITED"}
        for action in request.ContextPacket.AvailableGovernedActions
    )
    if not change_action_supported:
        positive_change = re.compile(
            r"\b(?:can|may|could)\s+be\s+(?:changed|adjusted|customi[sz]ed|edited|saved|persisted)\b|"
            r"\b(?:users?|organisations?)\s+(?:can|may|could)\s+(?:change|adjust|customi[sz]e|edit|save|persist|offer more)\b",
            re.I,
        )
        governed_limit = re.compile(
            r"\b(?:not currently (?:supported|available|implemented)|unavailable|unsupported|guidance only|"
            r"cannot|can't|no supported|not directly editable|would require .*derived policy)\b",
            re.I,
        )
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if positive_change.search(sentence) and not governed_limit.search(sentence):
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
        "mandatory_precision_constraints": {
            "question_assertions_are_governed_facts": False,
            "worker_specific_context_included": request.ContextPacket.WorkerSpecificContextIncluded,
            "individual_outcome_determination_permitted": False,
            "required_personal_question_boundary": (
                "Worker-specific governed facts were not included; Minerva cannot determine the individual's entitlement or access."
            ),
            "absence_statement": "A criterion is not identified as a factor in this governed policy context.",
            "absence_is_universal_negative_proof": False,
            "recognised_service_is_entitlement_access": False,
            "required_service_distinction": (
                "Recognised service may begin or be counted; entitlement access depends on the governed threshold and conditions."
            ),
            "prohibited_service_phrases": [
                "entitlement starts",
                "entitlement begins",
                "entitlement commences",
                "entitlement accrues from employment",
            ],
        },
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
                        "Answer": {
                            "type": "string",
                            "description": "A governed policy-level explanation only. Never determine the user's entitlement, eligibility, qualification, vesting, access, balance or payment. For service questions, never say entitlement starts/begins/commences/accrues from employment; distinguish recognised service from access, vesting and payment.",
                        },
                        "KeyPoints": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Policy-level only; keep recognised service distinct from entitlement access and never determine an individual outcome.",
                            },
                            "maxItems": 5,
                        },
                        "Boundary": {
                            "type": "string",
                            "description": "For a first-person outcome question, explicitly state that worker-specific governed facts were not included and Minerva cannot determine the individual's entitlement or access.",
                        },
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
            "model output turns absent criteria into a universal conclusion": "validation_negative_inference_claim",
            "model output conflates recognised service with entitlement access": "validation_service_entitlement_conflation",
            "model output makes a worker-specific outcome determination": "validation_personal_outcome_claim",
            "model output omits the worker-specific context boundary": "validation_worker_context_boundary",
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

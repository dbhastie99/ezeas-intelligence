from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Protocol

import httpx
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.schemas.leave_studio_minerva import (
    LeaveStudioAnswerPlan,
    RendererDocument,
    RendererPayload,
)


RENDERER_INSTRUCTION_VERSION = "LEAVE_STUDIO_CONFIGURATION_RENDERER_V1"


class RendererFailure(ValueError):
    pass


class WordingClient(Protocol):
    def render(
        self,
        payload: RendererPayload,
        *,
        model: str,
        instruction_version: str,
        timeout_seconds: float,
        max_output_chars: int,
    ) -> str: ...


@dataclass(frozen=True)
class RenderingOutcome:
    answer: str | None
    eligible: bool
    attempted: bool
    used: bool
    model_identifier: str | None
    instruction_version: str
    configuration_fingerprint: str
    fallback_reason: str | None


class HttpxOpenAIWordingClient:
    def __init__(self, *, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def render(
        self,
        payload: RendererPayload,
        *,
        model: str,
        instruction_version: str,
        timeout_seconds: float,
        max_output_chars: int,
    ) -> str:
        system = (
            "You are a bounded wording renderer. Use only the typed approved plan. "
            "Do not add facts, law, calculations, dates, rates, citations, eligibility conclusions, "
            "recommendations, or runtime claims. Return one JSON object with exactly Answer, "
            "WhatMatters, Boundary, SafeNextStep, EvidenceReferenceIds, and FactIds. Preserve every "
            "field except Answer byte-for-byte from the payload. Answer may only restate supplied facts."
        )
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": model,
                "temperature": 0,
                "max_tokens": min(1200, max(64, max_output_chars // 4)),
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": payload.model_dump_json()},
                ],
                "metadata": {"renderer_instruction": instruction_version},
            },
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        body = response.json()
        return body["choices"][0]["message"]["content"]


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def build_renderer_payload(plan: LeaveStudioAnswerPlan) -> RendererPayload:
    return RendererPayload(
        InstructionVersion=RENDERER_INSTRUCTION_VERSION,
        QueryIntent=plan.QuestionClassification,
        DirectDeterministicAnswer=plan.DirectDeterministicAnswer,
        WhatMatters=plan.WhatMatters,
        SelectedMaterialFacts=plan.SelectedMaterialFacts,
        FactIds=plan.FactIds,
        MissingOrUnresolvedFacts=plan.MissingOrUnresolvedFacts,
        Boundary=plan.Boundary,
        SafeNextStep=plan.SafeNextStep,
        EvidenceReferences=plan.EvidenceReferences,
        PlannerFingerprint=plan.PlannerFingerprint,
    )


def _configuration_fingerprint(settings: Settings) -> str:
    configured = {
        "enabled": settings.leave_studio_rendering_enabled,
        "provider": settings.llm_provider,
        "model": settings.llm_model,
        "base_url_configured": bool(settings.llm_base_url),
        "credential_configured": bool(settings.llm_api_key),
        "timeout": settings.leave_studio_rendering_timeout_seconds,
        "max_output_chars": settings.leave_studio_rendering_max_output_chars,
        "instruction": RENDERER_INSTRUCTION_VERSION,
    }
    return _sha256(json.dumps(configured, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def default_client_factory(settings: Settings) -> WordingClient | None:
    if settings.llm_provider.lower() not in {"openai", "openai-compatible"}:
        return None
    if not settings.llm_api_key or not settings.llm_model:
        return None
    return HttpxOpenAIWordingClient(
        base_url=settings.llm_base_url or "https://api.openai.com/v1",
        api_key=settings.llm_api_key,
    )


_NUMBER_TOKEN = re.compile(r"(?<![a-z0-9])(?:\d+(?:\.\d+)?)(?![a-z0-9])", re.IGNORECASE)
_WORD_TOKEN = re.compile(r"[a-z][a-z-]{3,}", re.IGNORECASE)
_SAFE_WORDING_WORDS = {
    "about", "also", "answer", "approved", "based", "because", "clear", "clearly", "current",
    "described", "explained", "facts", "governed", "helps", "information", "means", "plan",
    "policy", "provided", "shown", "studio", "summary", "this", "those", "understand", "version",
}


def _number_tokens(text: str) -> set[str]:
    return set(_NUMBER_TOKEN.findall(text.lower()))


def validate_rendered_document(raw: str, payload: RendererPayload, *, max_output_chars: int) -> RendererDocument:
    if not isinstance(raw, str) or not raw.strip() or len(raw) > max_output_chars:
        raise RendererFailure("renderer output is empty or exceeds the configured limit")
    try:
        document = RendererDocument.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        raise RendererFailure("renderer output is not the expected JSON contract") from exc
    if document.WhatMatters != payload.WhatMatters:
        raise RendererFailure("renderer changed approved material facts")
    if document.Boundary != payload.Boundary:
        raise RendererFailure("renderer changed the planned boundary")
    if document.SafeNextStep != payload.SafeNextStep:
        raise RendererFailure("renderer changed the deterministic next step")
    if document.FactIds != payload.FactIds:
        raise RendererFailure("renderer changed the allowed fact identifiers")
    expected_refs = [item.EvidenceReferenceId for item in payload.EvidenceReferences]
    if document.EvidenceReferenceIds != expected_refs:
        raise RendererFailure("renderer changed the approved evidence references")
    answer = document.Answer.strip()
    if not answer or len(answer) > max_output_chars:
        raise RendererFailure("renderer answer is empty or too long")
    if re.search(r"https?://|www\.|\.gov\.au\b|\b(?:citation|according to|legislation|statute)\b", answer, re.I):
        raise RendererFailure("renderer added a source or citation")
    if re.search(r"\b(?:you|john|employee|worker)\s+(?:is|are|will be)\s+(?:eligible|entitled)\b", answer, re.I):
        raise RendererFailure("renderer added a worker eligibility conclusion")
    if re.search(r"\b(?:i recommend|you should|the employer should|must change)\b", answer, re.I):
        raise RendererFailure("renderer added a recommendation")
    approved_text = " ".join(
        [
            payload.DirectDeterministicAnswer,
            *payload.WhatMatters,
            *(item.Label for item in payload.SelectedMaterialFacts),
            *(item.Value or "" for item in payload.SelectedMaterialFacts),
            *(item.DisplayValue for item in payload.SelectedMaterialFacts),
            payload.Boundary,
            payload.SafeNextStep,
        ]
    )
    if _number_tokens(answer) - _number_tokens(approved_text):
        raise RendererFailure("renderer added an unsupported numerical value")
    approved_words = {word.lower() for word in _WORD_TOKEN.findall(approved_text)} | _SAFE_WORDING_WORDS
    approved_stems = {word[:5] for word in approved_words}
    unsupported_words = {
        word.lower()
        for word in _WORD_TOKEN.findall(answer)
        if word.lower() not in approved_words and word.lower()[:5] not in approved_stems
    }
    if unsupported_words:
        raise RendererFailure("renderer added unsupported material outside the approved wording vocabulary")
    if re.search(r"\$|\b(?:aud|dollars?)\b", answer, re.I) and not re.search(r"\$|\b(?:aud|dollars?)\b", approved_text, re.I):
        raise RendererFailure("renderer added a monetary value")
    if re.search(r"\b(?:runtime is supported|runtime is operational|calculation is operational)\b", answer, re.I) and "runtime supported" not in payload.DirectDeterministicAnswer.lower():
        raise RendererFailure("renderer contradicted runtime support")
    return document


def render_optional_answer(
    plan: LeaveStudioAnswerPlan,
    *,
    settings: Settings | None = None,
    client_factory=None,
) -> RenderingOutcome:
    settings = settings or get_settings()
    fingerprint = _configuration_fingerprint(settings)
    base = {
        "eligible": plan.RendererEligible,
        "model_identifier": settings.llm_model,
        "instruction_version": RENDERER_INSTRUCTION_VERSION,
        "configuration_fingerprint": fingerprint,
    }
    if not plan.RendererEligible:
        return RenderingOutcome(answer=None, attempted=False, used=False, fallback_reason="ineligible", **base)
    if not settings.leave_studio_rendering_enabled:
        return RenderingOutcome(answer=None, attempted=False, used=False, fallback_reason="disabled", **base)
    if not settings.llm_model or not settings.llm_api_key:
        return RenderingOutcome(answer=None, attempted=True, used=False, fallback_reason="missing_configuration", **base)
    factory = client_factory or default_client_factory
    try:
        client = factory(settings)
    except Exception:
        client = None
    if client is None:
        return RenderingOutcome(answer=None, attempted=True, used=False, fallback_reason="missing_client", **base)
    payload = build_renderer_payload(plan)
    try:
        raw = client.render(
            payload,
            model=settings.llm_model,
            instruction_version=RENDERER_INSTRUCTION_VERSION,
            timeout_seconds=settings.leave_studio_rendering_timeout_seconds,
            max_output_chars=settings.leave_studio_rendering_max_output_chars,
        )
        document = validate_rendered_document(
            raw,
            payload,
            max_output_chars=settings.leave_studio_rendering_max_output_chars,
        )
        return RenderingOutcome(answer=document.Answer.strip(), attempted=True, used=True, fallback_reason=None, **base)
    except (TimeoutError, httpx.TimeoutException):
        reason = "timeout"
    except RendererFailure:
        reason = "validation_failure"
    except (httpx.HTTPError, OSError):
        reason = "provider_unavailable"
    except Exception:
        reason = "provider_error"
    return RenderingOutcome(answer=None, attempted=True, used=False, fallback_reason=reason, **base)

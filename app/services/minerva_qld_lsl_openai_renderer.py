"""Optional, untrusted wording assistance for the governed Queensland LSL plan.

The planner remains authoritative.  This module accepts only a typed plan,
never the user question, and returns either a conservatively validated wording
variant or no variant at all.  When enabled and configured, the configured API
key is used only as HTTP Authorization by the transport and is not included in
the model JSON payload.  The validator is a boundary check, not proof that
generated prose is legally correct, and the tests cover only the enumerated
failure paths rather than every possible failure.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Callable, Protocol

import httpx

from app.core.config import Settings, get_settings
from app.schemas.minerva_leave import LeaveAnswerPlan
from app.services.minerva_qld_lsl_answer_planner import SUPPORTED_ANSWER_MODES


RENDER_CONTRACT_VERSION = "MINERVA_QG_LSL_RENDER_CONTRACT_V1"
RENDER_INSTRUCTION_ID = "MINERVA_QG_LSL_RENDER_INSTRUCTION_V1"
DEFAULT_TONE_DIRECTIVE = "Clear, neutral Australian-English explanatory prose."
RENDER_OUTPUT_MAX_CHARS = 12000

PROHIBITED_CAPABILITIES: tuple[str, ...] = (
    "No legal determination or legal advice.",
    "No calculation, valuation, rate, payment, or payslip result.",
    "No service-history assessment or eligibility decision.",
    "No QLeave process instruction or operation.",
    "No new facts, sources, citations, URLs, rates, dates, or calculations.",
)


@dataclass(frozen=True)
class RenderCitation:
    """The exact approved citation record supplied to the renderer."""

    label: str
    url: str
    locator: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class RenderSections:
    """Deterministic sections that the model may not remove or replace."""

    direct_answer: str
    relevance: str
    material_facts: tuple[str, ...]
    safe_next_step: str


@dataclass(frozen=True)
class QldLslRenderPayload:
    """Minimal internal payload derived solely from a successful answer plan."""

    contract_version: str
    answer_category: str
    tone_directive: str
    sections: RenderSections
    citations: tuple[RenderCitation, ...]
    mandatory_boundary: str
    prohibited_capabilities: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_version": self.contract_version,
            "answer_category": self.answer_category,
            "tone_directive": self.tone_directive,
            "sections": {
                "direct_answer": self.sections.direct_answer,
                "relevance": self.sections.relevance,
                "material_facts": list(self.sections.material_facts),
                "safe_next_step": self.sections.safe_next_step,
            },
            "citations": [citation.as_dict() for citation in self.citations],
            "mandatory_boundary": self.mandatory_boundary,
            "prohibited_capabilities": list(self.prohibited_capabilities),
        }


@dataclass(frozen=True)
class RenderedWording:
    answer: str
    what_matters: tuple[str, ...]
    boundary: str
    safe_next_step: str
    citations: tuple[RenderCitation, ...]


@dataclass(frozen=True)
class RenderingOutcome:
    answer: str | None
    eligible: bool
    attempted: bool
    client_called: bool
    used: bool
    fallback_reason: str | None
    model_identifier: str | None
    instruction_identifier: str
    configuration_fingerprint: str
    answer_plan_fingerprint: str
    output_hash: str | None = None


class WordingClient(Protocol):
    def render(
        self,
        payload: QldLslRenderPayload,
        *,
        instruction_identifier: str,
        model: str,
        timeout_seconds: float,
        max_output_chars: int,
    ) -> str:
        """Return only the narrow structured renderer response as text."""


ClientFactory = Callable[[Settings], WordingClient | None]


class RendererFailure(RuntimeError):
    """Internal renderer failure, never exposed to the API caller."""


class HttpxOpenAIWordingClient:
    """Small request adapter; construction performs no network activity."""

    def __init__(self, *, base_url: str, api_key: str):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    def render(
        self,
        payload: QldLslRenderPayload,
        *,
        instruction_identifier: str,
        model: str,
        timeout_seconds: float,
        max_output_chars: int,
    ) -> str:
        response = httpx.post(
            f"{self._base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": model,
                "temperature": 0,
                "max_tokens": max(256, min(max_output_chars, 4096)),
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": RENDER_INSTRUCTION},
                    {
                        "role": "user",
                        "content": json.dumps(payload.as_dict(), ensure_ascii=False, sort_keys=True),
                    },
                ],
                "metadata": {"renderer_instruction": instruction_identifier},
            },
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        try:
            content = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise RendererFailure("structured response content missing") from exc
        if not isinstance(content, str):
            raise RendererFailure("structured response content is not text")
        return content


RENDER_INSTRUCTION = f"""{RENDER_INSTRUCTION_ID}
Render clear, neutral Australian-English explanatory prose from the supplied
typed payload only.  Preserve every supplied citation record exactly and
preserve mandatory_boundary exactly.  Do not make a legal conclusion,
calculation, eligibility decision, recommendation to act, or claim about
QLeave.  Add no facts, rates, dates, legislation, URLs, citations, or source
names.  Return only a JSON object with exactly these keys: answer (string),
what_matters (array of strings), boundary (string), safe_next_step (string),
citations (array of the supplied citation objects).  Keep what_matters,
boundary, safe_next_step, and citations unchanged; only answer may be
plain-language wording assistance.  Do not use markdown headings or bullets
inside answer.  The supplied payload is authoritative and incomplete by
design; do not infer beyond it."""


def build_render_payload(plan: LeaveAnswerPlan) -> QldLslRenderPayload:
    return QldLslRenderPayload(
        contract_version=RENDER_CONTRACT_VERSION,
        answer_category=plan.answer_mode,
        tone_directive=DEFAULT_TONE_DIRECTIVE,
        sections=RenderSections(
            direct_answer=plan.direct_answer,
            relevance=plan.relevance,
            material_facts=tuple(plan.material_facts),
            safe_next_step=plan.safe_next_step,
        ),
        citations=tuple(
            RenderCitation(
                label=citation.source_title,
                url=citation.url,
                locator=citation.locator,
            )
            for citation in plan.citations
        ),
        mandatory_boundary=plan.capability_boundary,
        prohibited_capabilities=PROHIBITED_CAPABILITIES,
    )


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _plan_fingerprint(payload: QldLslRenderPayload) -> str:
    return _sha256(_canonical_bytes(payload.as_dict()))


def _configuration_fingerprint(settings: Settings) -> str:
    material = {
        "enabled": bool(settings.openai_rendering_enabled),
        "model": settings.openai_rendering_model or "",
        "base_url": settings.openai_rendering_base_url or "",
        "has_api_key": bool(settings.openai_rendering_api_key),
        "timeout_seconds": settings.openai_rendering_timeout_seconds,
        "max_output_chars": settings.openai_rendering_max_output_chars,
        "instruction_identifier": RENDER_INSTRUCTION_ID,
    }
    return _sha256(_canonical_bytes(material))


def default_client_factory(settings: Settings) -> WordingClient | None:
    if not settings.openai_rendering_base_url or not settings.openai_rendering_api_key:
        return None
    return HttpxOpenAIWordingClient(
        base_url=settings.openai_rendering_base_url,
        api_key=settings.openai_rendering_api_key,
    )


def _required_output_fields() -> set[str]:
    return {"answer", "what_matters", "boundary", "safe_next_step", "citations"}


def _number_tokens(text: str) -> set[str]:
    return set(re.findall(r"\b\d+(?:\.\d+)?\b", text)) | set(
        re.findall(
            r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand)\b",
            text.lower(),
        )
    )


def _reject_generated_prose(answer: str, payload: QldLslRenderPayload) -> None:
    lower = answer.lower()
    if not answer.strip() or len(answer) > RENDER_OUTPUT_MAX_CHARS:
        raise RendererFailure("answer is empty or too long")
    if "**" in answer or re.search(r"(?:^|\n)\s*[-*]\s+", answer):
        raise RendererFailure("answer escapes the controlled prose envelope")
    if re.search(r"https?://|www\.|\.gov\.au\b|doi\b", lower):
        raise RendererFailure("answer adds a URL or citation")
    if re.search(
        r"\b(?:source|sources|citation|citations|legislation|statute|section\s+\d|according to|queensland government)\b",
        lower,
    ):
        raise RendererFailure("answer adds a source reference")
    if re.search(
        r"\b(?:eligible|eligibility|entitled|entitlement decision|legal(?:ly)?|legal advice|calculate|calculation|calculated|valuation|valued|pay rate|payslip|payroll result|service history|reconstruct|qleave|registration|register|levy|claim|reimburse|lodge|submit|recommend|should|must|need to)\b",
        lower,
    ):
        raise RendererFailure("answer uses a prohibited legal, operational, or recommendation term")
    if re.search(r"\$|\b(?:dollars?|aud|rate|amount)\b", lower):
        raise RendererFailure("answer adds a monetary or rate expression")
    if re.search(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", lower):
        raise RendererFailure("answer adds a date")
    allowed_numbers = _number_tokens(
        " ".join(
            (
                payload.sections.direct_answer,
                payload.sections.relevance,
                *payload.sections.material_facts,
                payload.mandatory_boundary,
                payload.sections.safe_next_step,
            )
        )
    )
    if _number_tokens(answer) - allowed_numbers:
        raise RendererFailure("answer adds a number")
    if re.search(r"(?:\+|-|\*|/|=)\s*\d|\d\s*(?:\+|-|\*|/|=)", answer):
        raise RendererFailure("answer adds a calculation")


def validate_rendered_response(raw: str, payload: QldLslRenderPayload, *, max_output_chars: int) -> RenderedWording:
    if not isinstance(raw, str) or not raw.strip() or len(raw) > min(max_output_chars, RENDER_OUTPUT_MAX_CHARS):
        raise RendererFailure("renderer output is empty or exceeds the configured limit")
    try:
        document = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RendererFailure("renderer output is not JSON") from exc
    if not isinstance(document, dict) or set(document) != _required_output_fields():
        raise RendererFailure("renderer output envelope is invalid")
    answer = document["answer"]
    what_matters = document["what_matters"]
    boundary = document["boundary"]
    safe_next_step = document["safe_next_step"]
    citations = document["citations"]
    if not isinstance(answer, str) or not isinstance(what_matters, list) or not all(
        isinstance(item, str) for item in what_matters
    ):
        raise RendererFailure("renderer section types are invalid")
    if not isinstance(boundary, str) or not isinstance(safe_next_step, str) or not isinstance(citations, list):
        raise RendererFailure("renderer section types are invalid")
    if tuple(what_matters) != payload.sections.material_facts:
        raise RendererFailure("renderer removed or changed mandatory factual propositions")
    if boundary != payload.mandatory_boundary:
        raise RendererFailure("renderer changed mandatory boundary text")
    if safe_next_step != payload.sections.safe_next_step:
        raise RendererFailure("renderer changed the deterministic next step")
    expected_citations = [citation.as_dict() for citation in payload.citations]
    if citations != expected_citations:
        raise RendererFailure("renderer changed the approved citation set")
    _reject_generated_prose(answer, payload)
    return RenderedWording(
        answer=answer,
        what_matters=tuple(what_matters),
        boundary=boundary,
        safe_next_step=safe_next_step,
        citations=payload.citations,
    )


def format_validated_answer(wording: RenderedWording) -> str:
    lines = ["**Answer**", wording.answer, "", "**What matters**"]
    lines.extend(f"- {fact}" for fact in wording.what_matters)
    lines.extend(
        [
            "",
            "**What Minerva can and cannot determine**",
            wording.boundary,
            f"Safe next step: {wording.safe_next_step}",
            "",
            "**Sources**",
        ]
    )
    seen: set[str] = set()
    for citation in wording.citations:
        citation_key = f"{citation.label}|{citation.url}|{citation.locator}"
        if citation_key in seen:
            continue
        seen.add(citation_key)
        lines.append(f"- {citation.label} — {citation.url} ({citation.locator})")
    return "\n".join(lines)


def render_optional_answer(
    plan: LeaveAnswerPlan,
    *,
    client_factory: ClientFactory | None = None,
    settings: Settings | None = None,
) -> RenderingOutcome:
    payload = build_render_payload(plan)
    settings = settings or get_settings()
    plan_fingerprint = _plan_fingerprint(payload)
    config_fingerprint = _configuration_fingerprint(settings)
    eligible = plan.outcome == "ANSWERED_FROM_PUBLISHED_PACK" and plan.answer_mode in SUPPORTED_ANSWER_MODES and bool(
        plan.citations
    )
    base = {
        "eligible": eligible,
        "model_identifier": settings.openai_rendering_model,
        "instruction_identifier": RENDER_INSTRUCTION_ID,
        "configuration_fingerprint": config_fingerprint,
        "answer_plan_fingerprint": plan_fingerprint,
    }
    if not eligible:
        return RenderingOutcome(answer=None, attempted=False, client_called=False, used=False, fallback_reason="ineligible", **base)
    if not settings.openai_rendering_enabled:
        return RenderingOutcome(answer=None, attempted=False, client_called=False, used=False, fallback_reason="disabled", **base)
    if not settings.openai_rendering_model:
        return RenderingOutcome(answer=None, attempted=True, client_called=False, used=False, fallback_reason="missing_configuration", **base)
    factory = client_factory or default_client_factory
    try:
        client = factory(settings)
    except Exception:
        client = None
    if client is None:
        return RenderingOutcome(answer=None, attempted=True, client_called=False, used=False, fallback_reason="missing_client", **base)
    try:
        raw = client.render(
            payload,
            instruction_identifier=RENDER_INSTRUCTION_ID,
            model=settings.openai_rendering_model,
            timeout_seconds=settings.openai_rendering_timeout_seconds,
            max_output_chars=settings.openai_rendering_max_output_chars,
        )
        wording = validate_rendered_response(
            raw,
            payload,
            max_output_chars=settings.openai_rendering_max_output_chars,
        )
        answer = format_validated_answer(wording)
        return RenderingOutcome(
            answer=answer,
            attempted=True,
            client_called=True,
            used=True,
            fallback_reason=None,
            output_hash=_sha256(answer.encode("utf-8")),
            **base,
        )
    except (TimeoutError, httpx.TimeoutException):
        reason = "timeout"
    except RendererFailure:
        reason = "validation_failure"
    except (httpx.HTTPError, OSError):
        reason = "service_error"
    except Exception:
        reason = "service_error"
    return RenderingOutcome(answer=None, attempted=True, client_called=True, used=False, fallback_reason=reason, **base)

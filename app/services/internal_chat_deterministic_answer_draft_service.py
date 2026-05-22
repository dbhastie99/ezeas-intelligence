from dataclasses import asdict, dataclass
from enum import StrEnum
import re
from typing import Any

from app.services.code_evidence_answer_policy_service import CodeEvidenceDisclosureMode
from app.services.code_evidence_answer_support_service import CodeEvidenceSupportStatus
from app.services.internal_chat_orchestrator_service import (
    InternalChatResponseEnvelope,
    InternalChatRole,
    InternalChatSourceScope,
    InternalChatStatus,
)


class DeterministicAnswerDraftStatus(StrEnum):
    DRAFT_READY = "DRAFT_READY"
    DRAFT_BLOCKED = "DRAFT_BLOCKED"
    DRAFT_NEEDS_MORE_EVIDENCE = "DRAFT_NEEDS_MORE_EVIDENCE"
    DRAFT_ROLE_RESTRICTED = "DRAFT_ROLE_RESTRICTED"
    DRAFT_PROHIBITED_CLAIM_BLOCKED = "DRAFT_PROHIBITED_CLAIM_BLOCKED"
    DRAFT_RUNTIME_EVIDENCE_REQUIRED = "DRAFT_RUNTIME_EVIDENCE_REQUIRED"
    DRAFT_UNSUPPORTED_SCOPE = "DRAFT_UNSUPPORTED_SCOPE"
    DRAFT_LIVE_LLM_DISABLED = "DRAFT_LIVE_LLM_DISABLED"


class DeterministicAnswerDraftFormattingMode(StrEnum):
    CONCISE = "CONCISE"
    STANDARD = "STANDARD"
    TECHNICAL = "TECHNICAL"


@dataclass(frozen=True)
class DeterministicAnswerDraftRequest:
    envelope: InternalChatResponseEnvelope | dict[str, Any]
    formatting_mode: DeterministicAnswerDraftFormattingMode | str = (
        DeterministicAnswerDraftFormattingMode.STANDARD
    )
    include_evidence_summary: bool = True
    include_caveats: bool = True
    allow_final_answer_generation: bool = False

    def model_dump(self) -> dict[str, Any]:
        return {
            "Envelope": self.envelope.model_dump()
            if isinstance(self.envelope, InternalChatResponseEnvelope)
            else dict(self.envelope),
            "FormattingMode": _enum_value(self.formatting_mode),
            "IncludeEvidenceSummary": self.include_evidence_summary,
            "IncludeCaveats": self.include_caveats,
            "AllowFinalAnswerGeneration": self.allow_final_answer_generation,
        }


@dataclass(frozen=True)
class DeterministicAnswerDraft:
    draft_status: DeterministicAnswerDraftStatus
    is_final_answer: bool
    deterministic_draft_available: bool
    final_answer_generation_permitted: bool
    live_llm_used: bool
    role: InternalChatRole | str
    disclosure_mode: CodeEvidenceDisclosureMode | str
    support_status: CodeEvidenceSupportStatus | str
    draft_text: str
    evidence_summary_text: str
    caveats_text: str
    blocked_claims_text: str
    no_action_attestation_text: str
    withheld_evidence_notice: str
    suggested_next_step: str
    safety_flags: list[str]

    def model_dump(self) -> dict[str, Any]:
        payload = asdict(self)
        return {
            "DraftStatus": _enum_value(self.draft_status),
            "IsFinalAnswer": self.is_final_answer,
            "DeterministicDraftAvailable": self.deterministic_draft_available,
            "FinalAnswerGenerationPermitted": self.final_answer_generation_permitted,
            "LiveLlmUsed": self.live_llm_used,
            "Role": _enum_value(self.role),
            "DisclosureMode": _enum_value(self.disclosure_mode),
            "SupportStatus": _enum_value(self.support_status),
            "DraftText": self.draft_text,
            "EvidenceSummaryText": self.evidence_summary_text,
            "CaveatsText": self.caveats_text,
            "BlockedClaimsText": self.blocked_claims_text,
            "NoActionAttestationText": self.no_action_attestation_text,
            "WithheldEvidenceNotice": self.withheld_evidence_notice,
            "SuggestedNextStep": self.suggested_next_step,
            "SafetyFlags": list(payload["safety_flags"]),
        }


class InternalChatDeterministicAnswerDraftService:
    def build_draft(
        self,
        request: (
            DeterministicAnswerDraftRequest
            | InternalChatResponseEnvelope
            | dict[str, Any]
        ),
        *,
        formatting_mode: DeterministicAnswerDraftFormattingMode | str | None = None,
        include_evidence_summary: bool | None = None,
        include_caveats: bool | None = None,
    ) -> DeterministicAnswerDraft:
        normalized_request = _draft_request_from_any(
            request,
            formatting_mode=formatting_mode,
            include_evidence_summary=include_evidence_summary,
            include_caveats=include_caveats,
        )
        envelope = normalized_request.envelope
        mode = _normalize_formatting_mode(normalized_request.formatting_mode)

        role = _field(envelope, "role", "Role") or InternalChatRole.PAYROLL_USER
        role_value = _enum_value(role)
        disclosure_mode = _field(envelope, "disclosure_mode", "DisclosureMode") or ""
        support_status = _support_status(envelope)
        draft_status = _draft_status(envelope, role_value, support_status)

        evidence_summary = ""
        if normalized_request.include_evidence_summary:
            summary_field = (
                "evidence_summary"
                if role_value == InternalChatRole.DEVELOPER.value
                else "role_safe_evidence_summary"
            )
            summary_model_field = (
                "EvidenceSummary"
                if role_value == InternalChatRole.DEVELOPER.value
                else "RoleSafeEvidenceSummary"
            )
            evidence_summary = _sanitize_text(
                _field(envelope, summary_field, summary_model_field) or ""
            )
        caveats_text = ""
        if normalized_request.include_caveats:
            caveats_text = _sanitize_text("; ".join(_required_caveats(envelope)))

        blocked_claims_text = _blocked_claims_text(envelope)
        no_action_attestation_text = _sanitize_text(
            _field(envelope, "no_action_attestation_text", "NoActionAttestationText")
            or (
                "No live LLM called; no DB accessed; no payroll calculation performed; "
                "no write action performed; no runtime object evidence fetched; "
                "no final answer generation performed."
            )
        )
        withheld_notice = _withheld_evidence_notice(envelope, role_value)
        suggested_next_step = _suggested_next_step(envelope, draft_status)
        safety_flags = _safety_flags(envelope, draft_status)

        draft_text = _draft_text(
            envelope=envelope,
            role_value=role_value,
            support_status=support_status,
            draft_status=draft_status,
            evidence_summary=evidence_summary,
            caveats_text=caveats_text,
            suggested_next_step=suggested_next_step,
            mode=mode,
        )

        return DeterministicAnswerDraft(
            draft_status=draft_status,
            is_final_answer=False,
            deterministic_draft_available=True,
            final_answer_generation_permitted=False,
            live_llm_used=False,
            role=role,
            disclosure_mode=disclosure_mode,
            support_status=support_status,
            draft_text=_sanitize_text(draft_text),
            evidence_summary_text=evidence_summary,
            caveats_text=caveats_text,
            blocked_claims_text=blocked_claims_text,
            no_action_attestation_text=no_action_attestation_text,
            withheld_evidence_notice=withheld_notice,
            suggested_next_step=suggested_next_step,
            safety_flags=safety_flags,
        )


def _draft_request_from_any(
    request: DeterministicAnswerDraftRequest | InternalChatResponseEnvelope | dict[str, Any],
    *,
    formatting_mode: DeterministicAnswerDraftFormattingMode | str | None,
    include_evidence_summary: bool | None,
    include_caveats: bool | None,
) -> DeterministicAnswerDraftRequest:
    if isinstance(request, DeterministicAnswerDraftRequest):
        if formatting_mode is None and include_evidence_summary is None and include_caveats is None:
            return request
        return DeterministicAnswerDraftRequest(
            envelope=request.envelope,
            formatting_mode=formatting_mode or request.formatting_mode,
            include_evidence_summary=(
                request.include_evidence_summary
                if include_evidence_summary is None
                else include_evidence_summary
            ),
            include_caveats=request.include_caveats if include_caveats is None else include_caveats,
            allow_final_answer_generation=request.allow_final_answer_generation,
        )
    if isinstance(request, InternalChatResponseEnvelope):
        return DeterministicAnswerDraftRequest(
            envelope=request,
            formatting_mode=formatting_mode or DeterministicAnswerDraftFormattingMode.STANDARD,
            include_evidence_summary=True if include_evidence_summary is None else include_evidence_summary,
            include_caveats=True if include_caveats is None else include_caveats,
        )
    envelope = request.get("envelope") or request.get("Envelope") or request
    return DeterministicAnswerDraftRequest(
        envelope=envelope,
        formatting_mode=(
            formatting_mode
            or request.get("formatting_mode")
            or request.get("FormattingMode")
            or DeterministicAnswerDraftFormattingMode.STANDARD
        ),
        include_evidence_summary=(
            bool(request.get("include_evidence_summary", request.get("IncludeEvidenceSummary", True)))
            if include_evidence_summary is None
            else include_evidence_summary
        ),
        include_caveats=(
            bool(request.get("include_caveats", request.get("IncludeCaveats", True)))
            if include_caveats is None
            else include_caveats
        ),
        allow_final_answer_generation=bool(
            request.get("allow_final_answer_generation")
            or request.get("AllowFinalAnswerGeneration")
        ),
    )


def _normalize_formatting_mode(
    mode: DeterministicAnswerDraftFormattingMode | str,
) -> DeterministicAnswerDraftFormattingMode:
    if isinstance(mode, DeterministicAnswerDraftFormattingMode):
        return mode
    try:
        return DeterministicAnswerDraftFormattingMode(str(mode).upper())
    except ValueError:
        return DeterministicAnswerDraftFormattingMode.STANDARD


def _draft_status(
    envelope: InternalChatResponseEnvelope | dict[str, Any],
    role_value: str,
    support_status: str,
) -> DeterministicAnswerDraftStatus:
    envelope_status = _enum_value(_field(envelope, "status", "Status"))
    unsupported_scopes = set(_enum_value(scope) for scope in _list_field(envelope, "unsupported_scopes", "UnsupportedScopes"))
    blocked_claims = [claim.lower() for claim in _list_field(envelope, "blocked_claims", "BlockedClaims")]

    if role_value == InternalChatRole.WORKER.value and (
        support_status == CodeEvidenceSupportStatus.ROLE_RESTRICTED.value
        or any("raw code" in claim for claim in blocked_claims)
    ):
        return DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED
    if any("payroll calculation request blocked" in claim for claim in blocked_claims):
        return DeterministicAnswerDraftStatus.DRAFT_BLOCKED
    if any("write action request blocked" in claim for claim in blocked_claims):
        return DeterministicAnswerDraftStatus.DRAFT_BLOCKED
    if (
        envelope_status == InternalChatStatus.PROHIBITED_CLAIM_BLOCKED.value
        or support_status == CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED.value
    ):
        return DeterministicAnswerDraftStatus.DRAFT_PROHIBITED_CLAIM_BLOCKED
    if (
        envelope_status == InternalChatStatus.ROLE_RESTRICTED.value
        or support_status == CodeEvidenceSupportStatus.ROLE_RESTRICTED.value
    ):
        return DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED
    if envelope_status == InternalChatStatus.LIVE_LLM_DISABLED.value:
        return DeterministicAnswerDraftStatus.DRAFT_LIVE_LLM_DISABLED
    if (
        InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE.value in unsupported_scopes
        or support_status == CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE.value
    ):
        return DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED
    if envelope_status == InternalChatStatus.UNSUPPORTED_SCOPE.value:
        return DeterministicAnswerDraftStatus.DRAFT_UNSUPPORTED_SCOPE
    if support_status in {
        CodeEvidenceSupportStatus.UNSUPPORTED.value,
        CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW.value,
    }:
        return DeterministicAnswerDraftStatus.DRAFT_NEEDS_MORE_EVIDENCE
    if envelope_status == InternalChatStatus.NEEDS_MORE_EVIDENCE.value:
        return DeterministicAnswerDraftStatus.DRAFT_NEEDS_MORE_EVIDENCE
    return DeterministicAnswerDraftStatus.DRAFT_READY


def _draft_text(
    *,
    envelope: InternalChatResponseEnvelope | dict[str, Any],
    role_value: str,
    support_status: str,
    draft_status: DeterministicAnswerDraftStatus,
    evidence_summary: str,
    caveats_text: str,
    suggested_next_step: str,
    mode: DeterministicAnswerDraftFormattingMode,
) -> str:
    answer = _answer_sentence(envelope, role_value, support_status, draft_status)
    evidence = _evidence_sentence(support_status, evidence_summary)
    caveat = _caveat_sentence(caveats_text)

    if mode == DeterministicAnswerDraftFormattingMode.CONCISE:
        return " ".join(part for part in [answer, caveat, f"Next step: {suggested_next_step}"] if part)
    if mode == DeterministicAnswerDraftFormattingMode.TECHNICAL:
        return "\n".join(
            part
            for part in [
                f"Draft status: {draft_status.value}.",
                f"Role: {role_value}; disclosure mode: {_enum_value(_field(envelope, 'disclosure_mode', 'DisclosureMode'))}; support status: {support_status}.",
                f"Answer: {answer}",
                f"Evidence support: {evidence}",
                f"Caveats: {caveat}" if caveat else "",
                f"Next step: {suggested_next_step}",
            ]
            if part
        )
    return "\n".join(
        part
        for part in [
            f"Answer: {answer}",
            f"Evidence support: {evidence}",
            f"Caveats: {caveat}" if caveat else "",
            f"Next step: {suggested_next_step}",
        ]
        if part
    )


def _answer_sentence(
    envelope: InternalChatResponseEnvelope | dict[str, Any],
    role_value: str,
    support_status: str,
    draft_status: DeterministicAnswerDraftStatus,
) -> str:
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_BLOCKED:
        return "This request is blocked because Minerva must not calculate payroll or perform write actions."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_PROHIBITED_CLAIM_BLOCKED:
        return "The claim is blocked or unsupported by policy; this draft does not affirm it as true."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED:
        return "This information is not available in the current role-safe mode."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED:
        if role_value == InternalChatRole.CUSTOMER_ADMINISTRATOR.value:
            return "Current implementation evidence supports only a customer-safe implementation confirmation; tenant or customer availability cannot be confirmed from the current evidence."
        return "Runtime, production, tenant, customer, or object-specific availability cannot be confirmed from the current evidence."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_UNSUPPORTED_SCOPE:
        if InternalChatSourceScope.ANALYTICS_EVIDENCE.value in {
            _enum_value(scope) for scope in _list_field(envelope, "unsupported_scopes", "UnsupportedScopes")
        }:
            return "Analytics evidence is recognised in v0.1, but analytics interpretation is not active by default unless safe analytics metadata is supplied."
        return "The requested source scope is not supported by the v0.1 deterministic draft layer."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_LIVE_LLM_DISABLED:
        return "Live LLM use is disabled; this is only a deterministic internal draft."
    if support_status == CodeEvidenceSupportStatus.PARTIALLY_SUPPORTED.value:
        return "Current evidence partially supports this, but missing support remains."
    if support_status == CodeEvidenceSupportStatus.UNSUPPORTED.value:
        return "Current evidence does not support the answer."
    if support_status == CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW.value:
        return "Code evidence exists, but curated implementation-state evidence is missing or did not match."

    if role_value == InternalChatRole.DEVELOPER.value:
        return "Implementation evidence supports this, with role-visible technical references where supplied."
    if role_value in {InternalChatRole.PAYROLL_ADMINISTRATOR.value, InternalChatRole.PAYROLL_MANAGER.value}:
        return "Current implementation evidence supports this capability."
    if role_value == InternalChatRole.PAYROLL_USER.value:
        return "The platform can support this workflow where the action is available and backend guardrails mark it eligible."
    if role_value == InternalChatRole.CUSTOMER_ADMINISTRATOR.value:
        return "Current implementation evidence supports only a customer-safe implementation confirmation."
    if role_value == InternalChatRole.WORKER.value:
        return "Worker-facing mode does not expose internal code evidence."
    return "Current implementation evidence supports this internal draft."


def _evidence_sentence(support_status: str, evidence_summary: str) -> str:
    prefix_by_status = {
        CodeEvidenceSupportStatus.SUPPORTED.value: "Evidence supports the position.",
        CodeEvidenceSupportStatus.PARTIALLY_SUPPORTED.value: "Evidence partially supports the position.",
        CodeEvidenceSupportStatus.UNSUPPORTED.value: "Evidence is insufficient or does not support the position.",
        CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW.value: (
            "Code evidence exists, but implementation-state evidence is missing."
        ),
        CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE.value: (
            "Static evidence cannot prove runtime or customer availability."
        ),
        CodeEvidenceSupportStatus.ROLE_RESTRICTED.value: "Evidence is restricted for this role.",
        CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED.value: "The blocked claim is not supported.",
    }
    prefix = prefix_by_status.get(support_status, "Evidence support is not established.")
    if evidence_summary:
        return f"{prefix} {evidence_summary}"
    return prefix


def _caveat_sentence(caveats_text: str) -> str:
    if not caveats_text:
        return ""
    return caveats_text


def _support_status(envelope: InternalChatResponseEnvelope | dict[str, Any]) -> str:
    packet = _field(envelope, "evidence_support_packet", "EvidenceSupportPacket") or {}
    status = _field(packet, "support_status", "support_status")
    return _enum_value(status)


def _required_caveats(envelope: InternalChatResponseEnvelope | dict[str, Any]) -> list[str]:
    return [_sanitize_text(str(caveat)) for caveat in _list_field(envelope, "required_caveats", "RequiredCaveats")]


def _blocked_claims_text(envelope: InternalChatResponseEnvelope | dict[str, Any]) -> str:
    claims = [_sanitize_text(str(claim)) for claim in _list_field(envelope, "blocked_claims", "BlockedClaims")]
    if not claims:
        return "None."
    return "; ".join(claims)


def _withheld_evidence_notice(envelope: InternalChatResponseEnvelope | dict[str, Any], role_value: str) -> str:
    packet = _field(envelope, "evidence_support_packet", "EvidenceSupportPacket") or {}
    withheld = [_sanitize_text(str(item)) for item in _list_field(packet, "withheld_evidence", "withheld_evidence")]
    if role_value == InternalChatRole.WORKER.value and withheld:
        return "Code, test, and prompt evidence is not available in worker-facing mode."
    if withheld:
        return f"Some evidence is withheld for this role: {'; '.join(withheld)}."
    return "No role-safe evidence was withheld from this draft."


def _suggested_next_step(
    envelope: InternalChatResponseEnvelope | dict[str, Any],
    draft_status: DeterministicAnswerDraftStatus,
) -> str:
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_BLOCKED:
        return "Reframe as a read-only question that does not ask Minerva to calculate payroll or perform an action."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_RUNTIME_EVIDENCE_REQUIRED:
        return "Supply authorised runtime object, tenant, permission, deployment, or configuration evidence before answering."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_UNSUPPORTED_SCOPE:
        return "Supply safe metadata for the requested scope or defer this question to a later evidence-intake slice."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED:
        return "Use a role with permitted evidence disclosure or provide a worker-safe explanation path."
    if draft_status == DeterministicAnswerDraftStatus.DRAFT_PROHIBITED_CLAIM_BLOCKED:
        return "Do not affirm the blocked claim; collect permitted evidence and restate the question."
    return _sanitize_text(
        _field(envelope, "next_step_recommendation", "NextStepRecommendation")
        or "Use this deterministic draft only for internal review."
    )


def _safety_flags(
    envelope: InternalChatResponseEnvelope | dict[str, Any],
    draft_status: DeterministicAnswerDraftStatus,
) -> list[str]:
    flags = [
        "DETERMINISTIC_DRAFT_AVAILABLE",
        "IS_FINAL_ANSWER_FALSE",
        "FINAL_ANSWER_GENERATION_PERMITTED_FALSE",
        "LIVE_LLM_USED_FALSE",
        "NO_DB_ACCESSED",
        "NO_PAYROLL_CALCULATION_PERFORMED",
        "NO_WRITE_ACTION_PERFORMED",
        "NO_RUNTIME_OBJECT_EVIDENCE_FETCHED",
        "RAW_CODE_SNIPPETS_EXCLUDED",
        draft_status.value,
    ]
    if _field(envelope, "final_answer_generation_permitted", "FinalAnswerGenerationPermitted"):
        flags.append("ENVELOPE_FINAL_ANSWER_FLAG_IGNORED")
    if _field(envelope, "live_llm_used", "LiveLlmUsed"):
        flags.append("ENVELOPE_LIVE_LLM_FLAG_IGNORED")
    return _dedupe(flags)


def _field(source: Any, snake_name: str, model_name: str) -> Any:
    if source is None:
        return None
    if isinstance(source, dict):
        return source.get(snake_name, source.get(model_name))
    return getattr(source, snake_name, getattr(source, model_name, None))


def _list_field(source: Any, snake_name: str, model_name: str) -> list[Any]:
    value = _field(source, snake_name, model_name)
    if value is None:
        return []
    return list(value)


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value or "")


def _sanitize_text(text: str) -> str:
    sanitized = text.replace("```", "")
    sanitized = re.sub(r"\bdef\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\):?", "function omitted", sanitized)
    sanitized = re.sub(r"\bclass\s+[A-Za-z_][A-Za-z0-9_]*\s*[:(]", "class omitted", sanitized)
    sanitized = sanitized.replace("return {", "return omitted")
    return sanitized.strip()


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped

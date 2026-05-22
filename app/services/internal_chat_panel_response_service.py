from dataclasses import asdict, dataclass, field
from enum import StrEnum
import re
from typing import Any


class InternalChatPanelMode(StrEnum):
    COMPACT = "COMPACT"
    STANDARD = "STANDARD"
    TECHNICAL = "TECHNICAL"


class InternalChatPanelStatus(StrEnum):
    PANEL_READY = "PANEL_READY"
    PANEL_NEEDS_MORE_EVIDENCE = "PANEL_NEEDS_MORE_EVIDENCE"
    PANEL_ROLE_RESTRICTED = "PANEL_ROLE_RESTRICTED"
    PANEL_PROHIBITED_CLAIM_BLOCKED = "PANEL_PROHIBITED_CLAIM_BLOCKED"
    PANEL_UNSUPPORTED_SCOPE = "PANEL_UNSUPPORTED_SCOPE"
    PANEL_INVALID_FIXTURE = "PANEL_INVALID_FIXTURE"
    PANEL_DRAFT_ONLY = "PANEL_DRAFT_ONLY"


PANEL_RESPONSE_CONTRACT_VERSION = "MINERVA_INTERNAL_CHAT_PANEL_RESPONSE_CONTRACT_V0_1"


@dataclass(frozen=True)
class InternalChatPanelResponse:
    panel_status: InternalChatPanelStatus | str
    role: str
    disclosure_mode: str
    headline: str
    summary: str
    draft_text: str
    is_final_answer: bool
    final_answer_generation_permitted: bool
    live_llm_used: bool
    evidence_chips: list[str]
    caveat_banners: list[dict[str, str]]
    boundary_banners: list[str]
    blocked_claims: list[str]
    unsupported_scopes: list[str]
    fixture_evidence_notice: str
    runtime_evidence_notice: str
    role_restriction_notice: str
    suggested_next_step: str
    primary_display_sections: list[str]
    secondary_display_sections: list[str]
    technical_details_available: bool
    technical_details: dict[str, Any] | None
    no_action_attestation: dict[str, bool]
    audit_summary: dict[str, Any] = field(default_factory=dict)

    def model_dump(self) -> dict[str, Any]:
        payload = asdict(self)
        return {
            "PanelStatus": _enum_value(self.panel_status),
            "Role": self.role,
            "DisclosureMode": self.disclosure_mode,
            "Headline": self.headline,
            "Summary": self.summary,
            "DraftText": self.draft_text,
            "IsFinalAnswer": self.is_final_answer,
            "FinalAnswerGenerationPermitted": self.final_answer_generation_permitted,
            "LiveLlmUsed": self.live_llm_used,
            "EvidenceChips": list(self.evidence_chips),
            "CaveatBanners": [dict(item) for item in self.caveat_banners],
            "BoundaryBanners": list(self.boundary_banners),
            "BlockedClaims": list(self.blocked_claims),
            "UnsupportedScopes": list(self.unsupported_scopes),
            "FixtureEvidenceNotice": self.fixture_evidence_notice,
            "RuntimeEvidenceNotice": self.runtime_evidence_notice,
            "RoleRestrictionNotice": self.role_restriction_notice,
            "SuggestedNextStep": self.suggested_next_step,
            "PrimaryDisplaySections": list(self.primary_display_sections),
            "SecondaryDisplaySections": list(self.secondary_display_sections),
            "TechnicalDetailsAvailable": self.technical_details_available,
            "TechnicalDetails": dict(self.technical_details) if self.technical_details else None,
            "NoActionAttestation": dict(self.no_action_attestation),
            "AuditSummary": dict(payload["audit_summary"]),
        }


class InternalChatPanelResponseService:
    def build_panel_response(
        self,
        stub_response: Any,
        *,
        role: str | None = None,
        panel_mode: InternalChatPanelMode | str = InternalChatPanelMode.STANDARD,
        include_technical_details: bool = False,
    ) -> InternalChatPanelResponse:
        response = _dict_from_any(stub_response)
        mode = _normalize_panel_mode(panel_mode)
        envelope = _dict(response.get("OrchestratorEnvelope"))
        packet = _dict(response.get("EvidenceSupportPacket"))
        draft = _dict(response.get("DeterministicDraft"))
        fixture = _dict(response.get("FixtureEvidence"))
        diagnostics = _dict(response.get("Diagnostics"))

        role_value = str(role or response.get("RequestEcho", {}).get("Role") or envelope.get("Role") or "")
        disclosure_mode = str(
            response.get("DisclosureMetadata", {}).get("DisclosureMode")
            or envelope.get("DisclosureMode")
            or packet.get("disclosure_mode")
            or ""
        )
        panel_status = _panel_status(response, envelope, packet, draft, fixture)
        technical_available = _technical_details_allowed(
            role_value=role_value,
            mode=mode,
            include_technical_details=include_technical_details,
        )

        return InternalChatPanelResponse(
            panel_status=panel_status,
            role=role_value,
            disclosure_mode=disclosure_mode,
            headline=_headline(panel_status, role_value, fixture),
            summary=_summary(response, envelope, packet, draft, role_value, panel_status),
            draft_text=_draft_text(response, draft, panel_status),
            is_final_answer=False,
            final_answer_generation_permitted=False,
            live_llm_used=False,
            evidence_chips=_evidence_chips(response, envelope, packet, fixture),
            caveat_banners=_caveat_banners(response, role_value, panel_status, mode),
            boundary_banners=_boundary_banners(),
            blocked_claims=[_sanitize_text(str(item)) for item in response.get("BlockedClaims", [])],
            unsupported_scopes=[str(item) for item in response.get("UnsupportedScopes", [])],
            fixture_evidence_notice=_fixture_notice(fixture),
            runtime_evidence_notice=_runtime_notice(response, fixture, panel_status),
            role_restriction_notice=_role_restriction_notice(role_value, panel_status, packet),
            suggested_next_step=_suggested_next_step(envelope, draft, panel_status),
            primary_display_sections=_primary_sections(panel_status),
            secondary_display_sections=_secondary_sections(technical_available),
            technical_details_available=technical_available,
            technical_details=(
                _technical_details(response, envelope, packet, fixture, diagnostics)
                if technical_available
                else None
            ),
            no_action_attestation=_no_action_attestation(response),
            audit_summary={
                "PanelResponseContractVersion": PANEL_RESPONSE_CONTRACT_VERSION,
                "SourceResponseStatus": str(response.get("Status") or ""),
                "OrchestratorStatus": str(envelope.get("Status") or ""),
                "EvidenceSupportStatus": str(packet.get("support_status") or ""),
                "DraftStatus": str(draft.get("DraftStatus") or ""),
                "FixtureKey": fixture.get("FixtureKey"),
                "PanelMode": mode.value,
                "RawCodeSnippetsIncluded": False,
                "NoExternalCallsOrWritesPerformed": True,
                "DatabaseAccessed": False,
                "RuntimeObjectEvidenceFetched": False,
            },
        )


def _panel_status(
    response: dict[str, Any],
    envelope: dict[str, Any],
    packet: dict[str, Any],
    draft: dict[str, Any],
    fixture: dict[str, Any],
) -> InternalChatPanelStatus:
    source_status = str(response.get("Status") or "")
    envelope_status = str(envelope.get("Status") or "")
    support_status = str(packet.get("support_status") or "")
    draft_status = str(draft.get("DraftStatus") or "")
    unsupported_scopes = {str(scope) for scope in response.get("UnsupportedScopes", [])}
    fixture_status = str(fixture.get("FixtureEvidenceStatus") or "")

    if source_status == "INVALID_FIXTURE_KEY" or fixture_status == "INVALID_FIXTURE_KEY":
        return InternalChatPanelStatus.PANEL_INVALID_FIXTURE
    if envelope_status == "PROHIBITED_CLAIM_BLOCKED" or support_status == "PROHIBITED_CLAIM_BLOCKED":
        return InternalChatPanelStatus.PANEL_PROHIBITED_CLAIM_BLOCKED
    if draft_status == "DRAFT_ROLE_RESTRICTED" or envelope_status == "ROLE_RESTRICTED" or support_status == "ROLE_RESTRICTED":
        return InternalChatPanelStatus.PANEL_ROLE_RESTRICTED
    if (
        fixture_status == "DEFERRED_INACTIVE"
        or "ANALYTICS_EVIDENCE" in unsupported_scopes
        or draft_status == "DRAFT_UNSUPPORTED_SCOPE"
    ):
        return InternalChatPanelStatus.PANEL_UNSUPPORTED_SCOPE
    if (
        fixture_status == "NEEDS_RUNTIME_EVIDENCE"
        or support_status == "NEEDS_RUNTIME_EVIDENCE"
        or draft_status == "DRAFT_RUNTIME_EVIDENCE_REQUIRED"
        or "RUNTIME_OBJECT_EVIDENCE" in unsupported_scopes
    ):
        return InternalChatPanelStatus.PANEL_NEEDS_MORE_EVIDENCE
    if draft_status in {"", "None"}:
        return InternalChatPanelStatus.PANEL_DRAFT_ONLY
    return InternalChatPanelStatus.PANEL_READY


def _headline(status: InternalChatPanelStatus, role: str, fixture: dict[str, Any]) -> str:
    if status == InternalChatPanelStatus.PANEL_INVALID_FIXTURE:
        return "The requested internal fixture key was not found."
    if status == InternalChatPanelStatus.PANEL_ROLE_RESTRICTED:
        return "This evidence is not available for this role."
    if status == InternalChatPanelStatus.PANEL_PROHIBITED_CLAIM_BLOCKED:
        return "This claim or action request is blocked."
    if status == InternalChatPanelStatus.PANEL_UNSUPPORTED_SCOPE:
        if fixture.get("FixtureEvidenceStatus") == "DEFERRED_INACTIVE":
            return "Analytics evidence is recognised but not active in this MVP."
        return "This evidence scope is not active in this MVP."
    if status == InternalChatPanelStatus.PANEL_NEEDS_MORE_EVIDENCE:
        return "Runtime evidence is required before this can be confirmed."
    if role == "PAYROLL_ADMINISTRATOR":
        return "Implementation evidence supports this, with runtime caveats."
    if role == "CUSTOMER_ADMINISTRATOR":
        return "Implementation evidence supports a customer-safe confirmation, with availability caveats."
    if role == "PAYROLL_USER":
        return "The workflow is supported where the platform makes it available."
    if role == "DEVELOPER":
        return "Implementation evidence supports this, with technical references available."
    return "Implementation evidence supports this internal draft."


def _summary(
    response: dict[str, Any],
    envelope: dict[str, Any],
    packet: dict[str, Any],
    draft: dict[str, Any],
    role: str,
    panel_status: InternalChatPanelStatus,
) -> str:
    if panel_status == InternalChatPanelStatus.PANEL_INVALID_FIXTURE:
        return "No fixture evidence was supplied and no live retrieval was attempted."
    if panel_status == InternalChatPanelStatus.PANEL_UNSUPPORTED_SCOPE and role == "ANALYTICS_USER":
        return "Analytics is deferred in v0.1; the panel may show the deferral but must not claim chart interpretation."
    if panel_status == InternalChatPanelStatus.PANEL_ROLE_RESTRICTED:
        return "The current role can receive only a restricted, non-technical explanation."
    if role == "DEVELOPER":
        text = packet.get("evidence_summary") or envelope.get("EvidenceSummary") or draft.get("EvidenceSummaryText")
    else:
        text = packet.get("role_safe_evidence_summary") or envelope.get("RoleSafeEvidenceSummary")
    if not text:
        text = draft.get("EvidenceSummaryText") or envelope.get("SuggestedDeterministicSummary") or ""
    return _sanitize_text(str(text))


def _draft_text(
    response: dict[str, Any],
    draft: dict[str, Any],
    panel_status: InternalChatPanelStatus,
) -> str:
    if draft.get("DraftText"):
        return _sanitize_text(str(draft["DraftText"]))
    if panel_status == InternalChatPanelStatus.PANEL_INVALID_FIXTURE:
        return "No answer draft is available because the fixture key is invalid."
    return _sanitize_text(str(response.get("OrchestratorEnvelope", {}).get("SuggestedDeterministicSummary") or ""))


def _evidence_chips(
    response: dict[str, Any],
    envelope: dict[str, Any],
    packet: dict[str, Any],
    fixture: dict[str, Any],
) -> list[str]:
    chips: list[str] = []
    if fixture.get("FixtureEvidenceUsed"):
        chips.extend(["Fixture evidence", "Synthetic/internal"])
    if packet.get("implementation_state_evidence"):
        chips.append("Implementation-state")
    if packet.get("code_evidence") or "CODE_EVIDENCE" in envelope.get("SourceScopesRequested", []):
        chips.append("Code evidence")
    if packet.get("test_evidence") or "TEST_EVIDENCE" in envelope.get("SourceScopesRequested", []):
        chips.append("Test evidence")
    if _runtime_required(response, fixture):
        chips.append("Runtime evidence required")
    if response.get("LiveLlmUsed") is False:
        chips.append("Live LLM disabled")
    chips.extend(["No payroll calculation", "No write action"])
    if response.get("FinalAnswerGenerationPermitted") is False:
        chips.append("Final answer disabled")
    return _dedupe(chips)


def _caveat_banners(
    response: dict[str, Any],
    role: str,
    panel_status: InternalChatPanelStatus,
    mode: InternalChatPanelMode,
) -> list[dict[str, str]]:
    caveats = [str(item) for item in response.get("RequiredCaveats", [])]
    banners: list[dict[str, str]] = []
    if _any_contains(caveats, ["runtime", "production", "customer", "tenant"]):
        banners.append(
            _banner(
                "RUNTIME_AVAILABILITY_CAVEAT",
                "Runtime, tenant, customer, production, and live object availability require separate authorised evidence.",
            )
        )
    if _any_contains(caveats, ["fixture", "synthetic"]):
        banners.append(
            _banner(
                "FIXTURE_SYNTHETIC_EVIDENCE_CAVEAT",
                "Fixture evidence is synthetic/internal and must not be treated as production or customer evidence.",
            )
        )
    if _any_contains(caveats, ["code evidence", "code cannot"]):
        banners.append(
            _banner(
                "CODE_EVIDENCE_LIMITATION",
                "Code evidence may support implementation confidence but cannot prove runtime availability.",
            )
        )
    if _any_contains(caveats, ["test evidence", "tests"]):
        banners.append(
            _banner(
                "TEST_EVIDENCE_LIMITATION",
                "Test evidence is behavioural test-level evidence and does not prove production deployment.",
            )
        )
    banners.append(_banner("FINAL_ANSWER_DISABLED", "Final answer generation is disabled for this internal MVP stub."))
    banners.append(_banner("LIVE_LLM_DISABLED", "Live LLM calls are disabled for this internal MVP stub."))
    if panel_status == InternalChatPanelStatus.PANEL_ROLE_RESTRICTED or role == "WORKER":
        banners.append(_banner("ROLE_RESTRICTION", "This role cannot receive internal code evidence."))
    if panel_status == InternalChatPanelStatus.PANEL_UNSUPPORTED_SCOPE:
        banners.append(_banner("UNSUPPORTED_SCOPE", "The requested evidence scope is deferred or inactive in v0.1."))
    if mode == InternalChatPanelMode.TECHNICAL:
        for index, caveat in enumerate(caveats[:8], start=1):
            banners.append(_banner(f"TECHNICAL_CAVEAT_{index}", _sanitize_text(caveat)))
    return _dedupe_banners(banners)


def _boundary_banners() -> list[str]:
    return [
        "Internal/demo/test support only",
        "Final answer generation disabled",
        "Live LLM disabled",
        "Runtime evidence not fetched",
        "Database access disabled",
        "No payroll calculation",
        "No write action",
    ]


def _fixture_notice(fixture: dict[str, Any]) -> str:
    if fixture.get("FixtureEvidenceUsed"):
        return "Synthetic fixture evidence was used for this internal response."
    if fixture.get("FixtureEvidenceStatus") == "INVALID_FIXTURE_KEY":
        return "No fixture evidence was used because the fixture key is invalid."
    return "No fixture evidence was requested or used."


def _runtime_notice(
    response: dict[str, Any],
    fixture: dict[str, Any],
    panel_status: InternalChatPanelStatus,
) -> str:
    if fixture.get("RuntimeObjectEvidenceFetched") is True:
        return "Synthetic runtime metadata was supplied; no live runtime fetch was performed."
    if panel_status == InternalChatPanelStatus.PANEL_NEEDS_MORE_EVIDENCE or _runtime_required(response, fixture):
        return "Authorised runtime object evidence is required; no runtime object evidence was fetched."
    return "No live runtime object evidence was fetched."


def _role_restriction_notice(role: str, status: InternalChatPanelStatus, packet: dict[str, Any]) -> str:
    withheld = packet.get("withheld_evidence") or []
    if role == "WORKER":
        return "Worker-facing mode does not expose internal code, test, prompt, file, function, or route evidence."
    if status == InternalChatPanelStatus.PANEL_ROLE_RESTRICTED:
        return "Role-safe mode restricts this evidence from the current role."
    if withheld:
        return "Some evidence is withheld for this role."
    return "No additional role restriction applies to the panel packet."


def _suggested_next_step(
    envelope: dict[str, Any],
    draft: dict[str, Any],
    status: InternalChatPanelStatus,
) -> str:
    if status == InternalChatPanelStatus.PANEL_INVALID_FIXTURE:
        return "Use one of the listed internal fixture keys or omit FixtureKey."
    return _sanitize_text(
        str(
            draft.get("SuggestedNextStep")
            or envelope.get("NextStepRecommendation")
            or "Use this deterministic panel packet only for internal review."
        )
    )


def _primary_sections(status: InternalChatPanelStatus) -> list[str]:
    sections = ["Headline", "Summary", "DraftText", "EvidenceChips", "CaveatBanners"]
    if status in {
        InternalChatPanelStatus.PANEL_PROHIBITED_CLAIM_BLOCKED,
        InternalChatPanelStatus.PANEL_ROLE_RESTRICTED,
    }:
        sections.append("BlockedClaims")
    return sections


def _secondary_sections(technical_details_available: bool) -> list[str]:
    sections = [
        "BoundaryBanners",
        "FixtureEvidenceNotice",
        "RuntimeEvidenceNotice",
        "RoleRestrictionNotice",
        "SuggestedNextStep",
        "NoActionAttestation",
    ]
    if technical_details_available:
        sections.append("TechnicalDetails")
    return sections


def _technical_details_allowed(
    *,
    role_value: str,
    mode: InternalChatPanelMode,
    include_technical_details: bool,
) -> bool:
    return role_value == "DEVELOPER" and (include_technical_details or mode == InternalChatPanelMode.TECHNICAL)


def _technical_details(
    response: dict[str, Any],
    envelope: dict[str, Any],
    packet: dict[str, Any],
    fixture: dict[str, Any],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "FixtureKey": fixture.get("FixtureKey"),
        "FixtureEvidenceStatus": fixture.get("FixtureEvidenceStatus"),
        "SupportStatus": packet.get("support_status"),
        "OrchestratorStatus": envelope.get("Status"),
        "DraftStatus": _dict(response.get("DeterministicDraft")).get("DraftStatus"),
        "SourceScopesUsed": list(envelope.get("SourceScopesUsed") or []),
        "SourceCategories": _source_categories(packet),
        "EvidenceReferences": _technical_evidence_references(packet),
        "Diagnostics": {
            "ApiStubVersion": diagnostics.get("ApiStubVersion"),
            "OrchestratorEnvelopeVersion": diagnostics.get("OrchestratorEnvelopeVersion"),
            "LiveLlmUsed": False,
            "FinalAnswerGenerationPerformed": False,
            "DatabaseAccessed": False,
            "RuntimeObjectEvidenceFetched": False,
            "WriteActionPerformed": False,
        },
    }


def _technical_evidence_references(packet: dict[str, Any]) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    for category, key in [
        ("IMPLEMENTATION_STATE", "implementation_state_evidence"),
        ("CODE", "code_evidence"),
        ("TEST", "test_evidence"),
        ("PROMPT", "prompt_evidence"),
        ("KNOWLEDGE", "knowledge_evidence"),
    ]:
        for item in packet.get(key) or []:
            source = _dict(item)
            references.append(
                {
                    "Category": category,
                    "Title": _sanitize_text(str(source.get("title") or "")),
                    "RepoName": source.get("repo_name"),
                    "RepoFamily": source.get("repo_family"),
                    "FilePath": source.get("file_path"),
                    "SymbolName": source.get("symbol_name"),
                    "RoutePath": source.get("route_path"),
                    "TestName": source.get("test_name"),
                }
            )
    return references[:20]


def _source_categories(packet: dict[str, Any]) -> list[str]:
    categories = []
    for category, key in [
        ("IMPLEMENTATION_STATE", "implementation_state_evidence"),
        ("CODE", "code_evidence"),
        ("TEST", "test_evidence"),
        ("PROMPT", "prompt_evidence"),
        ("KNOWLEDGE", "knowledge_evidence"),
    ]:
        if packet.get(key):
            categories.append(category)
    return categories


def _no_action_attestation(response: dict[str, Any]) -> dict[str, bool]:
    attestation = dict(response.get("NoActionAttestation") or {})
    for key in [
        "LiveLlmCalled",
        "DatabaseAccessed",
        "ExternalApiCalled",
        "ExternalRepoMutated",
        "PayrollCalculationPerformed",
        "WriteActionPerformed",
        "RuntimeObjectEvidenceFetched",
        "FinalAnswerGenerated",
        "FinalAnswerGenerationPerformed",
        "ChatPersistencePerformed",
        "UiExposed",
    ]:
        attestation[key] = False
    return attestation


def _runtime_required(response: dict[str, Any], fixture: dict[str, Any]) -> bool:
    return (
        fixture.get("FixtureEvidenceStatus") == "NEEDS_RUNTIME_EVIDENCE"
        or "RUNTIME_OBJECT_EVIDENCE" in response.get("UnsupportedScopes", [])
        or _dict(response.get("EvidenceSupportPacket")).get("support_status") == "NEEDS_RUNTIME_EVIDENCE"
    )


def _banner(kind: str, text: str, severity: str = "INFO") -> dict[str, str]:
    return {"Type": kind, "Severity": severity, "Text": text}


def _any_contains(values: list[str], needles: list[str]) -> bool:
    text = " ".join(values).lower()
    return any(needle.lower() in text for needle in needles)


def _dedupe_banners(values: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for value in values:
        key = value["Type"]
        if key not in seen:
            deduped.append(value)
            seen.add(key)
    return deduped


def _dict_from_any(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    return dict(value or {})


def _dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if isinstance(value, dict):
        return dict(value)
    return {}


def _normalize_panel_mode(mode: InternalChatPanelMode | str) -> InternalChatPanelMode:
    if isinstance(mode, InternalChatPanelMode):
        return mode
    try:
        return InternalChatPanelMode(str(mode).upper())
    except ValueError:
        return InternalChatPanelMode.STANDARD


def _sanitize_text(text: str) -> str:
    sanitized = text.replace("```", "")
    sanitized = re.sub(r"\bdef\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\):?", "function omitted", sanitized)
    sanitized = re.sub(r"\bclass\s+[A-Za-z_][A-Za-z0-9_]*\s*[:(]", "class omitted", sanitized)
    sanitized = sanitized.replace("return {", "return omitted")
    return sanitized.strip()


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped

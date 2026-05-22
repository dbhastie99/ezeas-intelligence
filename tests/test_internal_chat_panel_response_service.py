import json
from pathlib import Path

from app.services.internal_chat_api_stub_service import InternalChatApiStubService
from app.services.internal_chat_evidence_fixture_harness_service import InternalChatFixtureKey
from app.services.internal_chat_orchestrator_service import InternalChatRole, InternalChatSourceScope
from app.services.internal_chat_panel_response_service import (
    InternalChatPanelMode,
    InternalChatPanelResponseService,
)


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_panel_response_contract_v0_1.md"
EVALUATION_DIR = ROOT / "docs" / "evaluation" / "minerva_internal_chat_panel_response_contract_v0_1"
EVALUATION_BASELINE = EVALUATION_DIR / "PANEL_RESPONSE_CONTRACT_BASELINE.md"
SAMPLE_RESPONSE = EVALUATION_DIR / "PANEL_RESPONSE_SAMPLE.json"
PROMPT_ARTEFACT = (
    ROOT / "docs" / "codex_prompts" / "2026-05-22_minerva_internal_chat_panel_response_contract_v01.md"
)


def _stub_response(**overrides) -> dict:
    payload = {
        "Question": "Is the Asphalt safe classRates seeding aligned now?",
        "Role": InternalChatRole.PAYROLL_ADMINISTRATOR.value,
        "FixtureKey": InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES.value,
        "IncludeDeterministicDraft": True,
    }
    payload.update(overrides)
    return InternalChatApiStubService().build_response(payload).model_dump()


def _panel(response: dict, **kwargs) -> dict:
    return InternalChatPanelResponseService().build_panel_response(response, **kwargs).model_dump()


def _banner_types(panel: dict) -> list[str]:
    return [banner["Type"] for banner in panel["CaveatBanners"]]


def test_panel_response_service_imports_and_builds_from_valid_stub_response():
    response = _stub_response()
    panel = _panel(response)

    assert panel["PanelStatus"] == "PANEL_READY"
    assert panel["Role"] == "PAYROLL_ADMINISTRATOR"
    assert panel["Headline"]
    assert panel["PrimaryDisplaySections"] == [
        "Headline",
        "Summary",
        "DraftText",
        "EvidenceChips",
        "CaveatBanners",
    ]


def test_payroll_administrator_fixture_response_produces_ready_panel_with_caveat_chips():
    panel = _panel(_stub_response())

    assert panel["PanelStatus"] == "PANEL_READY"
    assert "Implementation-state" in panel["EvidenceChips"]
    assert "Code evidence" in panel["EvidenceChips"]
    assert "Test evidence" in panel["EvidenceChips"]
    assert "Runtime evidence required" not in panel["EvidenceChips"]
    assert "No payroll calculation" in panel["EvidenceChips"]
    assert "No write action" in panel["EvidenceChips"]
    assert "RUNTIME_AVAILABILITY_CAVEAT" in _banner_types(panel)
    assert "FIXTURE_SYNTHETIC_EVIDENCE_CAVEAT" in _banner_types(panel)


def test_payroll_user_panel_hides_file_function_and_test_names():
    response = _stub_response(
        Role=InternalChatRole.PAYROLL_USER.value,
        Question="What should I do with this post-finalisation ObjectTime action?",
        FixtureKey=InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED.value,
    )
    panel = _panel(response)
    dumped = json.dumps(panel, sort_keys=True)

    assert panel["PanelStatus"] == "PANEL_READY"
    assert "app/services/post_finalisation_objecttime_action_service.py" not in dumped
    assert "PostFinalisationObjectTimeActionService" not in dumped
    assert "test_post_finalisation_objecttime_action_keeps_finalised_payrun_protected" not in dumped


def test_developer_technical_mode_exposes_role_safe_details_without_raw_code():
    response = _stub_response(
        Role=InternalChatRole.DEVELOPER.value,
        Question="What evidence supports manual admitted draft action processing?",
        FixtureKey=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED.value,
    )
    panel = _panel(
        response,
        panel_mode=InternalChatPanelMode.TECHNICAL,
        include_technical_details=True,
    )
    dumped = json.dumps(panel, sort_keys=True)

    assert panel["TechnicalDetailsAvailable"] is True
    assert panel["TechnicalDetails"]["EvidenceReferences"]
    assert "app/services/admitted_draft_payrun_processing_bridge_service.py" in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" in dumped
    assert "```" not in dumped
    assert "def " not in dumped
    assert "class " not in dumped


def test_worker_response_is_role_restricted_for_code_evidence():
    panel = _panel(
        _stub_response(
            Role=InternalChatRole.WORKER.value,
            Question="What does code evidence confirm, and what does it not confirm?",
            FixtureKey=InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME.value,
        )
    )

    assert panel["PanelStatus"] == "PANEL_ROLE_RESTRICTED"
    assert "ROLE_RESTRICTION" in _banner_types(panel)
    assert "Worker-facing mode" in panel["RoleRestrictionNotice"]


def test_customer_administrator_response_includes_customer_runtime_availability_caveat():
    panel = _panel(
        _stub_response(
            Role=InternalChatRole.CUSTOMER_ADMINISTRATOR.value,
            Question="Is this implementation enabled for my tenant in production?",
            FixtureKey=InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME.value,
        )
    )

    assert panel["PanelStatus"] == "PANEL_NEEDS_MORE_EVIDENCE"
    assert "Runtime evidence required" in panel["EvidenceChips"]
    assert "RUNTIME_AVAILABILITY_CAVEAT" in _banner_types(panel)
    assert "customer" in panel["RuntimeEvidenceNotice"].lower() or "runtime" in panel["RuntimeEvidenceNotice"].lower()


def test_analytics_deferred_fixture_produces_unsupported_scope_panel():
    response = _stub_response(
        Role=InternalChatRole.ANALYTICS_USER.value,
        Question="Explain this payroll trend chart.",
        FixtureKey=InternalChatFixtureKey.ANALYTICS_EVIDENCE_DEFERRED.value,
        SourceScopes=[InternalChatSourceScope.ANALYTICS_EVIDENCE.value],
    )
    panel = _panel(response)

    assert panel["PanelStatus"] == "PANEL_UNSUPPORTED_SCOPE"
    assert panel["Headline"] == "Analytics evidence is recognised but not active in this MVP."
    assert "UNSUPPORTED_SCOPE" in _banner_types(panel)


def test_runtime_evidence_required_fixture_produces_needs_more_evidence_panel():
    response = _stub_response(
        Role=InternalChatRole.PAYROLL_MANAGER.value,
        Question="Why did this worker get overtime?",
        FixtureKey=InternalChatFixtureKey.RUNTIME_OBJECT_EVIDENCE_REQUIRED.value,
        SourceScopes=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE.value],
    )
    panel = _panel(response)

    assert panel["PanelStatus"] == "PANEL_NEEDS_MORE_EVIDENCE"
    assert "Runtime evidence required" in panel["EvidenceChips"]
    assert "no runtime object evidence was fetched" in panel["RuntimeEvidenceNotice"].lower()


def test_invalid_fixture_key_produces_invalid_fixture_panel():
    panel = _panel(_stub_response(FixtureKey="NOT_A_FIXTURE"))

    assert panel["PanelStatus"] == "PANEL_INVALID_FIXTURE"
    assert panel["Headline"] == "The requested internal fixture key was not found."
    assert "invalid" in panel["FixtureEvidenceNotice"].lower()


def test_evidence_chips_are_compact_and_deterministic():
    first = _panel(_stub_response())["EvidenceChips"]
    second = _panel(_stub_response())["EvidenceChips"]

    assert first == second
    assert len(first) == len(set(first))
    assert all(len(chip) <= 32 for chip in first)


def test_duplicate_caveats_are_grouped_for_panel_display():
    panel = _panel(_stub_response())
    banner_types = _banner_types(panel)

    assert len(banner_types) == len(set(banner_types))
    assert len(panel["CaveatBanners"]) < len(_stub_response()["RequiredCaveats"])


def test_boundary_flags_remain_disabled_and_no_action_attestation_present():
    panel = _panel(_stub_response())

    assert panel["IsFinalAnswer"] is False
    assert panel["FinalAnswerGenerationPermitted"] is False
    assert panel["LiveLlmUsed"] is False
    assert panel["NoActionAttestation"]["LiveLlmCalled"] is False
    assert panel["NoActionAttestation"]["DatabaseAccessed"] is False
    assert panel["NoActionAttestation"]["RuntimeObjectEvidenceFetched"] is False
    assert panel["NoActionAttestation"]["WriteActionPerformed"] is False


def test_raw_code_snippets_are_absent_from_panel_response():
    panel = _panel(_stub_response(Role=InternalChatRole.DEVELOPER.value))
    dumped = json.dumps(panel, sort_keys=True)

    assert "```" not in dumped
    assert "return {" not in dumped
    assert "def " not in dumped


def test_technical_details_are_unavailable_by_default_for_payroll_user():
    panel = _panel(
        _stub_response(
            Role=InternalChatRole.PAYROLL_USER.value,
            FixtureKey=InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED.value,
        )
    )

    assert panel["TechnicalDetailsAvailable"] is False
    assert panel["TechnicalDetails"] is None


def test_include_panel_response_request_remains_backward_compatible():
    without_panel = _stub_response(IncludePanelResponse=False)
    with_panel = _stub_response(IncludePanelResponse=True)

    assert without_panel["Status"] == "STUB_RESPONSE_BUILT"
    assert without_panel["PanelResponse"] is None
    assert with_panel["Status"] == "STUB_RESPONSE_BUILT"
    assert with_panel["PanelResponse"]["PanelStatus"] == "PANEL_READY"


def test_route_returns_panel_response_when_requested(client):
    response = client.post(
        "/api/v1/internal/minerva/chat/stub",
        json={
            "Question": "Is the Asphalt safe classRates seeding aligned now?",
            "Role": InternalChatRole.PAYROLL_ADMINISTRATOR.value,
            "FixtureKey": InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES.value,
            "IncludePanelResponse": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["PanelResponse"]["PanelStatus"] == "PANEL_READY"
    assert body["PanelResponse"]["IsFinalAnswer"] is False


def test_sample_json_validates():
    payload = json.loads(SAMPLE_RESPONSE.read_text(encoding="utf-8"))

    assert payload["Version"] == "MINERVA_INTERNAL_CHAT_PANEL_RESPONSE_CONTRACT_V0_1"
    assert len(payload["Samples"]) >= 4


def test_docs_evaluation_sample_and_prompt_files_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert SAMPLE_RESPONSE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_panel_response_artefacts_have_no_mojibake_markers():
    paths = [
        ROOT / "app" / "services" / "internal_chat_panel_response_service.py",
        ROOT / "app" / "schemas" / "internal_chat.py",
        ROOT / "app" / "api" / "v1" / "internal_chat_stub.py",
        KNOWLEDGE_DOC,
        EVALUATION_BASELINE,
        SAMPLE_RESPONSE,
        PROMPT_ARTEFACT,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())
    markers = [
        chr(0x00E2) + chr(0x2020) + chr(0x2019),
        chr(0x00E2) + chr(0x20AC) + chr(0x201D),
        chr(0xFFFD),
    ]

    for marker in markers:
        assert marker not in combined

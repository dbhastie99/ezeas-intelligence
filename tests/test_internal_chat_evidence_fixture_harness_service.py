import pytest
from pathlib import Path

from app.services.internal_chat_api_stub_service import InternalChatApiStubService
from app.services.internal_chat_deterministic_answer_draft_service import DeterministicAnswerDraftStatus
from app.services.internal_chat_evidence_fixture_harness_service import (
    FixtureEvidenceStatus,
    InternalChatEvidenceFixtureHarnessService,
    InternalChatFixtureKey,
)
from app.services.internal_chat_orchestrator_service import InternalChatRole, InternalChatSourceScope


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_evidence_fixture_harness_v0_1.md"
EVALUATION_DIR = ROOT / "docs" / "evaluation" / "minerva_internal_chat_evidence_fixture_harness_v0_1"
EVALUATION_BASELINE = EVALUATION_DIR / "EVIDENCE_FIXTURE_HARNESS_BASELINE.md"
FIXTURE_PACK = EVALUATION_DIR / "INTERNAL_CHAT_EVIDENCE_FIXTURES.json"
SAMPLE_RESPONSES = EVALUATION_DIR / "SAMPLE_FIXTURE_RESPONSES.json"
PROMPT_ARTEFACT = ROOT / "docs" / "codex_prompts" / "2026-05-22_minerva_internal_chat_evidence_fixture_harness_v01.md"


def _service() -> InternalChatEvidenceFixtureHarnessService:
    return InternalChatEvidenceFixtureHarnessService()


def _fixture(key: InternalChatFixtureKey):
    return _service().get_fixture(key)


def _chat_response(
    key: InternalChatFixtureKey,
    *,
    role: InternalChatRole = InternalChatRole.DEVELOPER,
    question: str | None = None,
    source_scopes: list[InternalChatSourceScope] | None = None,
) -> dict:
    fixture = _fixture(key)
    response = InternalChatApiStubService().build_response(
        {
            "Question": question or fixture.sample_questions[0],
            "Role": role.value,
            "SourceScopes": [
                scope.value for scope in (source_scopes or fixture.expected_source_scopes)
            ],
            "DomainTags": fixture.domain_tags,
            "CandidateEvidence": fixture.candidate_evidence(),
        }
    )
    return response.model_dump()


def test_fixture_harness_lists_all_required_fixture_keys():
    keys = set(_service().list_available_fixture_key_values())

    assert keys == {key.value for key in InternalChatFixtureKey}


def test_each_fixture_has_required_metadata_and_no_action_attestation():
    for key in InternalChatFixtureKey:
        fixture = _fixture(key)

        assert fixture.domain_tags
        assert fixture.expected_source_scopes
        assert fixture.candidate_evidence_metadata
        assert fixture.expected_support_status in FixtureEvidenceStatus
        assert fixture.expected_role_safe_caveats
        assert fixture.no_action_attestation
        assert all(value is False for value in fixture.no_action_attestation.values())
        assert "No live LLM called" in fixture.no_action_attestation_text


def test_manual_admitted_draft_fixture_includes_endpoint_and_non_goals():
    fixture = _fixture(InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED)
    dumped = str(fixture.model_dump())

    assert "/api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process" in dumped
    assert "PayRunActionDecision" in dumped
    assert "authorised admission" in dumped
    assert "PayRunContact" in dumped
    assert "AdmittedDraftPayRunProcessingBridgeService" in dumped
    assert "target_contact_id" in dumped
    assert "not automation" in dumped.lower()
    assert "not process-all" in dumped.lower()
    assert "finalisation, payment, banking, or payroll calculation" in dumped


def test_post_finalisation_objecttime_fixture_includes_protection_and_review_requirement():
    fixture = _fixture(InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED)
    dumped = str(fixture.model_dump()).lower()

    assert "objecttime" in dumped
    assert "finalised payrun protection" in dumped
    assert "worker-period scoped" in dumped
    assert "treatment review" in dumped
    assert "no finalised mutation" in dumped


def test_asphalt_safe_classrates_fixture_includes_status_and_safe_codes():
    fixture = _fixture(InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES)
    dumped = str(fixture.model_dump())

    assert "SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES" in dumped
    assert "Step 06 wrote 30 safe classRates rows" in dumped
    for code in ["DAY1", "OT1", "OT2", "SAT1", "SUN1", "PHOL1"]:
        assert code in dumped


def test_conditional_shiftwork_fixture_says_dynamic_gates_remain_deferred():
    fixture = _fixture(InternalChatFixtureKey.ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED)
    dumped = str(fixture.model_dump())
    lowered = dumped.lower()

    for code in ["AFT1", "AFT2", "NGT1", "NGT2"]:
        assert code in dumped
    assert "RateSource.IsShiftWorker" in dumped
    assert "ShiftType" in dumped
    assert "dynamic shift treatment engine remains future/deferred" in lowered
    assert "non-rotating night shift" in lowered
    assert "unrelieved shiftworker overtime" in dumped
    assert "break/change-to-shift continuation" in dumped


def test_code_evidence_runtime_caveat_fixture_says_code_cannot_prove_runtime_availability():
    fixture = _fixture(InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME)
    dumped = str(fixture.model_dump()).lower()

    assert "code evidence confirms implementation support" in dumped
    assert "code cannot prove production deployment" in dumped
    assert "code cannot prove customer availability" in dumped
    assert "runtime object state" in dumped
    assert "payroll correctness" in dumped


def test_analytics_fixture_is_deferred_inactive_by_default():
    fixture = _fixture(InternalChatFixtureKey.ANALYTICS_EVIDENCE_DEFERRED)
    dumped = str(fixture.model_dump()).lower()

    assert fixture.expected_support_status == FixtureEvidenceStatus.DEFERRED_INACTIVE
    assert "future/optional evidence target" in dumped
    assert "deferred/inactive in v0.1" in dumped


def test_runtime_object_evidence_fixture_requires_runtime_object_evidence():
    fixture = _fixture(InternalChatFixtureKey.RUNTIME_OBJECT_EVIDENCE_REQUIRED)
    dumped = str(fixture.model_dump()).lower()

    assert fixture.expected_support_status == FixtureEvidenceStatus.NEEDS_RUNTIME_EVIDENCE
    assert "object-specific questions require runtime object evidence" in dumped
    assert "must say needs evidence" in dumped
    assert "does not prove tenant" in dumped


def test_fixture_evidence_can_be_passed_into_api_stub_and_produce_deterministic_draft():
    response = _chat_response(
        InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED,
        role=InternalChatRole.PAYROLL_ADMINISTRATOR,
        question="Can the platform manually process an admitted draft action?",
    )

    assert response["Status"] == "STUB_RESPONSE_BUILT"
    assert response["EvidenceSupportPacket"]["support_status"] == "SUPPORTED"
    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_READY"
    assert response["IsFinalAnswer"] is False
    assert response["LiveLlmUsed"] is False


def test_developer_fixture_response_may_show_technical_evidence_references():
    response = _chat_response(
        InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED,
        role=InternalChatRole.DEVELOPER,
        question="What evidence supports manual admitted draft action processing?",
    )
    dumped = str(response)

    assert "app/services/admitted_draft_payrun_processing_bridge_service.py" in dumped
    assert "test_manual_admitted_draft_processing_bridge_evidence" in dumped


def test_payroll_user_fixture_response_hides_technical_file_function_and_test_names():
    response = _chat_response(
        InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED,
        role=InternalChatRole.PAYROLL_USER,
        question="What should I do with this post-finalisation ObjectTime action?",
    )
    dumped = str(response)

    assert "The platform can support this workflow" in response["DeterministicDraft"]["DraftText"]
    assert "app/services/post_finalisation_objecttime_action_service.py" not in dumped
    assert "PostFinalisationObjectTimeActionService" not in dumped
    assert "test_post_finalisation_objecttime_action_keeps_finalised_payrun_protected" not in dumped


def test_worker_fixture_response_role_restricts_code_evidence():
    response = _chat_response(
        InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED,
        role=InternalChatRole.WORKER,
        question="What evidence supports manual admitted draft action processing?",
    )

    assert response["DeterministicDraft"]["DraftStatus"] == DeterministicAnswerDraftStatus.DRAFT_ROLE_RESTRICTED.value
    assert response["EvidenceSupportPacket"]["code_evidence"] == []
    assert response["EvidenceSupportPacket"]["test_evidence"] == []


def test_no_fixture_includes_raw_code_snippets():
    for key in InternalChatFixtureKey:
        dumped = str(_fixture(key).model_dump()).lower()

        assert "raw_code_snippet" not in dumped
        assert "```" not in dumped
        assert "def unsafe" not in dumped
        assert "return {" not in dumped


def test_no_fixture_claims_live_llm_db_runtime_fetch_final_answer_or_write_action():
    prohibited_fragments = [
        "live llm called': true",
        "database_accessed': true",
        "runtimeobjectevidencefetched': true",
        "writeactionperformed': true",
        "finalanswergenerated': true",
        "finalanswergenerationperformed': true",
    ]
    for key in InternalChatFixtureKey:
        dumped = str(_fixture(key).model_dump()).replace(" ", "").lower()

        for fragment in prohibited_fragments:
            assert fragment.replace(" ", "") not in dumped


def test_runtime_availability_fixture_response_requires_runtime_evidence():
    response = _chat_response(
        InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME,
        role=InternalChatRole.CUSTOMER_ADMINISTRATOR,
        question="Is this implementation enabled for my tenant in production?",
    )

    assert response["DeterministicDraft"]["DraftStatus"] == "DRAFT_RUNTIME_EVIDENCE_REQUIRED"
    assert response["DisclosureMetadata"]["CustomerAvailabilityConfirmed"] is False
    assert response["NoActionAttestation"]["RuntimeObjectEvidenceFetched"] is False


def test_analytics_fixture_response_is_deferred_without_safe_analytics_scope_metadata():
    response = _chat_response(
        InternalChatFixtureKey.ANALYTICS_EVIDENCE_DEFERRED,
        role=InternalChatRole.ANALYTICS_USER,
        question="Explain this payroll trend chart.",
        source_scopes=[InternalChatSourceScope.ANALYTICS_EVIDENCE],
    )

    assert response["OrchestratorEnvelope"]["Status"] == "UNSUPPORTED_SCOPE"
    assert "ANALYTICS_EVIDENCE" in response["UnsupportedScopes"]
    assert "analytics interpretation is not active by default" in response["DeterministicDraft"]["DraftText"]


def test_invalid_fixture_key_returns_deterministic_not_found_status():
    with pytest.raises(KeyError, match="Unsupported internal chat fixture key"):
        _service().get_fixture("NOT_A_FIXTURE")


def test_fixture_harness_docs_and_json_artefacts_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert FIXTURE_PACK.exists()
    assert SAMPLE_RESPONSES.exists()
    assert PROMPT_ARTEFACT.exists()


def test_fixture_harness_docs_include_keys_questions_and_boundaries():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [KNOWLEDGE_DOC, EVALUATION_BASELINE, PROMPT_ARTEFACT]
    )

    for key in InternalChatFixtureKey:
        assert key.value in combined
    for question in [
        "Can the platform manually process an admitted draft action?",
        "What evidence supports the post-finalisation ObjectTime action?",
        "Is the Asphalt safe classRates seeding aligned now?",
        "What is still deferred for conditional shiftwork?",
        "Why can code evidence not prove production/customer runtime availability?",
    ]:
        assert question in combined
    for phrase in [
        "No live LLM called",
        "No DB accessed",
        "No runtime object evidence fetched",
        "No write action performed",
        "Final answer generation remains disabled",
        "Raw code snippets are not included",
    ]:
        assert phrase in combined

from app.services.internal_chat_orchestrator_service import InternalChatSourceScope


def _sample_evidence() -> list[dict]:
    return [
        {
            "source_type": "IMPLEMENTATION_STATE_DOC",
            "evidence_category": "IMPLEMENTATION_STATE",
            "title": "manual admitted draft processing implementation state",
            "file_path": "docs/evaluation/admitted_draft/IMPLEMENTATION_STATE_BASELINE.md",
            "tags": ["manual", "admitted", "draft", "processing", "implementation_state"],
        },
        {
            "source_type": "ROUTE_DEFINITION",
            "evidence_category": "CODE",
            "title": "manual admitted draft processing endpoint",
            "repo_name": "workforce-platform",
            "file_path": "app/routes/payroll/admitted_draft_actions.py",
            "route_path": "/payruns/{payrun_id}/admitted-draft-actions/{action_id}/process",
            "tags": ["manual", "admitted", "draft", "processing", "endpoint", "implementation_support"],
        },
        {
            "source_type": "TEST_FILE",
            "evidence_category": "TEST",
            "title": "manual admitted draft processing bridge test",
            "file_path": "tests/test_admitted_draft_payrun_processing_bridge_source_response.py",
            "test_name": "test_manual_admitted_draft_processing_bridge_evidence",
            "tags": ["manual", "admitted", "draft", "processing", "behavioural_evidence"],
        },
    ]


def _payload(**overrides) -> dict:
    payload = {
        "Question": "Can the platform manually process an admitted draft action?",
        "Role": "PAYROLL_ADMINISTRATOR",
        "SourceScopes": [
            InternalChatSourceScope.IMPLEMENTATION_STATE.value,
            InternalChatSourceScope.CODE_EVIDENCE.value,
            InternalChatSourceScope.TEST_EVIDENCE.value,
        ],
        "DomainTags": ["manual", "admitted", "draft", "processing"],
        "CandidateEvidence": _sample_evidence(),
    }
    payload.update(overrides)
    return payload


def test_internal_chat_stub_route_returns_200_for_valid_request(client):
    response = client.post("/api/v1/internal/minerva/chat/stub", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["Status"] == "STUB_RESPONSE_BUILT"
    assert body["OrchestratorEnvelope"]["Status"] == "ANSWER_SUPPORT_BUILT"


def test_internal_chat_stub_route_returns_non_final_no_live_llm_response(client):
    response = client.post("/api/v1/internal/minerva/chat/stub", json=_payload(AllowLiveLlm=True))

    assert response.status_code == 200
    body = response.json()
    assert body["IsFinalAnswer"] is False
    assert body["LiveLlmUsed"] is False
    assert body["FinalAnswerText"] is None


def test_internal_chat_stub_route_invalid_role_returns_validation_error(client):
    response = client.post("/api/v1/internal/minerva/chat/stub", json=_payload(Role="UNKNOWN_ROLE"))

    assert response.status_code == 422
    assert "Unsupported internal chat role" in response.json()["detail"]


def test_internal_chat_stub_route_blocks_payroll_calculation_and_write_action(client):
    calculation = client.post(
        "/api/v1/internal/minerva/chat/stub",
        json=_payload(
            Question="Calculate this worker's overtime pay.",
            SourceScopes=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE.value],
            CandidateEvidence=[],
            DomainTags=["overtime"],
        ),
    )
    write = client.post(
        "/api/v1/internal/minerva/chat/stub",
        json=_payload(Question="Please approve and process this payrun now."),
    )

    assert calculation.status_code == 200
    assert "payroll calculation request blocked" in calculation.json()["BlockedClaims"]
    assert write.status_code == 200
    assert "write action request blocked" in write.json()["BlockedClaims"]


def test_internal_chat_stub_route_does_not_require_db_or_live_llm(client):
    response = client.post("/api/v1/internal/minerva/chat/stub", json=_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["NoActionAttestation"]["DatabaseAccessed"] is False
    assert body["NoActionAttestation"]["LiveLlmCalled"] is False
    assert body["NoActionAttestation"]["ExternalApiCalled"] is False

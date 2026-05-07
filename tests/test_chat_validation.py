from app.models.audit import AIInteractionAudit


def test_invalid_session_id_returns_clean_error(client):
    response = client.post(
        "/api/v1/chat/message",
        json={"session_id": "00000000-0000-0000-0000-000000000000", "message": "Hello?"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chat session not found."


def test_mismatched_tenant_id_is_rejected(client):
    session_response = client.post("/api/v1/chat/session", json={"tenant_id": "tenant-a"})
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/v1/chat/message",
        json={"session_id": session_id, "tenant_id": "tenant-b", "message": "What is visible?"},
    )

    assert response.status_code == 400
    assert "tenant_id does not match" in response.json()["detail"]


def test_mismatched_user_id_is_rejected(client):
    session_response = client.post("/api/v1/chat/session", json={"user_id": "user-a"})
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/v1/chat/message",
        json={"session_id": session_id, "user_id": "user-b", "message": "What is visible?"},
    )

    assert response.status_code == 400
    assert "user_id does not match" in response.json()["detail"]


def test_matching_tenant_and_user_uses_session_context(client, db_session):
    ingest_response = client.post(
        "/api/v1/ingest/file",
        files={"file": ("tenant-doc.txt", b"Tenant alpha knowledge is visible to tenant alpha.", "text/plain")},
        data={"source_type": "OTHER", "tenant_id": "tenant-alpha"},
    )
    assert ingest_response.status_code == 200
    session_response = client.post(
        "/api/v1/chat/session",
        json={"tenant_id": "tenant-alpha", "user_id": "user-alpha"},
    )
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/v1/chat/message",
        json={
            "session_id": session_id,
            "tenant_id": "tenant-alpha",
            "user_id": "user-alpha",
            "message": "What tenant alpha knowledge is visible?",
        },
    )

    assert response.status_code == 200
    assert response.json()["sources"]
    audit = db_session.get(AIInteractionAudit, response.json()["audit_id"])
    assert audit.TenantId == "tenant-alpha"
    assert audit.UserId == "user-alpha"

def _ingest_text(client, file_name: str, text: str, tenant_id: str | None = None):
    data = {"source_type": "OTHER"}
    if tenant_id is not None:
        data["tenant_id"] = tenant_id
    response = client.post(
        "/api/v1/ingest/file",
        files={"file": (file_name, text.encode("utf-8"), "text/plain")},
        data=data,
    )
    assert response.status_code == 200
    return response


def _create_session(client, tenant_id: str | None = None):
    payload = {}
    if tenant_id is not None:
        payload["tenant_id"] = tenant_id
    response = client.post("/api/v1/chat/session", json=payload)
    assert response.status_code == 200
    return response.json()["session_id"]


def _ask(client, session_id: str, message: str):
    response = client.post("/api/v1/chat/message", json={"session_id": session_id, "message": message})
    assert response.status_code == 200
    return response.json()


def test_tenant_chat_sees_public_and_matching_tenant_docs_but_not_other_tenant_docs(client):
    _ingest_text(client, "public-filter.txt", "tenantfilter shared public evidence")
    _ingest_text(client, "tenant-alpha-filter.txt", "tenantfilter alpha private evidence", tenant_id="tenant-alpha")
    _ingest_text(client, "tenant-beta-filter.txt", "tenantfilter beta private evidence", tenant_id="tenant-beta")
    session_id = _create_session(client, tenant_id="tenant-alpha")

    body = _ask(client, session_id, "tenantfilter evidence")
    source_names = {source["original_file_name"] for source in body["sources"]}

    assert "public-filter.txt" in source_names
    assert "tenant-alpha-filter.txt" in source_names
    assert "tenant-beta-filter.txt" not in source_names


def test_anonymous_chat_sees_only_public_docs(client):
    _ingest_text(client, "public-anonymous.txt", "anonfilter public evidence")
    _ingest_text(client, "tenant-anonymous.txt", "anonfilter tenant evidence", tenant_id="tenant-alpha")
    session_id = _create_session(client)

    body = _ask(client, session_id, "anonfilter evidence")
    source_names = {source["original_file_name"] for source in body["sources"]}

    assert source_names == {"public-anonymous.txt"}

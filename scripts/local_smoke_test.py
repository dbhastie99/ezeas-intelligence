import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SAMPLE_PATH = PROJECT_ROOT / "samples" / "knowledge" / "sample_platform_doctrine.txt"


def configured_database_url() -> str | None:
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return env_value

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return None

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "MINERVA_DATABASE_URL" and value.strip():
            return value.strip().strip('"').strip("'")
    return None


def require_ok(response, label: str) -> dict:
    if response.status_code >= 400:
        raise SystemExit(f"{label} failed with HTTP {response.status_code}: {response.text}")
    return response.json()


def main() -> int:
    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2
    if not SAMPLE_PATH.exists():
        print(f"Sample file not found: {SAMPLE_PATH}")
        return 1

    from app.main import app

    client = TestClient(app)

    health = require_ok(client.get("/health"), "Health check")
    print(f"Health: {health}")

    with SAMPLE_PATH.open("rb") as sample_file:
        ingest = require_ok(
            client.post(
                "/api/v1/ingest/file",
                files={"file": (SAMPLE_PATH.name, sample_file, "text/plain")},
                data={"source_type": "PLATFORM_DOCTRINE", "capability_status": "DOCTRINE"},
            ),
            "Sample ingestion",
        )
    print(f"Ingestion: {ingest}")
    print(f"Duplicate flag: {ingest['duplicate']}")

    session = require_ok(
        client.post("/api/v1/chat/session", json={"title": "Local SQL Server smoke test"}),
        "Chat session creation",
    )
    chat = require_ok(
        client.post(
            "/api/v1/chat/message",
            json={
                "session_id": session["session_id"],
                "message": "What is Minerva allowed to do?",
            },
        ),
        "Chat message",
    )

    print(f"Chat answer: {chat['answer']}")
    print(f"Source reference count: {len(chat['sources'])}")
    print(f"Audit id: {chat['audit_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

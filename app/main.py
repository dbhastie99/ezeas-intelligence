from fastapi import FastAPI

from app.api.v1 import chat, ingest, internal_chat_stub

app = FastAPI(
    title="Ezeas Intelligence",
    description="Minerva read-only advisory knowledge/evidence intelligence layer.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ezeas-intelligence",
        "role": "read-only advisory knowledge/evidence intelligence",
    }


app.include_router(ingest.router, prefix="/api/v1/ingest", tags=["ingest"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(internal_chat_stub.router, prefix="/api/v1/internal", tags=["internal-chat-stub"])

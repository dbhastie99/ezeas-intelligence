from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import award_studio_minerva, chat, ingest, internal_chat_stub, leave_studio_minerva, minerva_leave
from app.core.config import get_settings

app = FastAPI(
    title="Ezeas Intelligence",
    description="Minerva read-only advisory knowledge/evidence intelligence layer.",
    version="0.1.0",
)

settings = get_settings()
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
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
app.include_router(minerva_leave.router, prefix="/api/v1/minerva", tags=["governed-queensland-lsl"])
app.include_router(
    leave_studio_minerva.router,
    prefix="/api/v1/minerva",
    tags=["governed-leave-studio-configuration"],
)
app.include_router(
    award_studio_minerva.router,
    prefix="/api/v1/minerva",
    tags=["governed-award-studio-configuration"],
)

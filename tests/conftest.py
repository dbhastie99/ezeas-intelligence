import os

os.environ["MINERVA_DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["MINERVA_CHUNK_SIZE"] = "300"
os.environ["MINERVA_CHUNK_OVERLAP"] = "50"

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import engine
from app.main import app
from app.models import AIInteractionAudit, KnowledgeChatMessage, KnowledgeChunk, KnowledgeDocument


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def db_session():
    from app.db.session import SessionLocal

    with SessionLocal() as db:
        yield db

import pytest
from fastapi.testclient import TestClient

from app.core.db import SessionLocal
from main import app


@pytest.fixture(scope="session")
def db():
    yield SessionLocal()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

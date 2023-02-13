import pytest
from fastapi.testclient import TestClient
from main import app

from app.core.db import SessionLocal


@pytest.fixture(scope='session')
def db():
    yield SessionLocal()


@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

import pytest
from fastapi.testclient import TestClient
from core.main import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_privoxy_url():
    return "https://www.privoxy.org/config/"

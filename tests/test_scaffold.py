import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.mark.scaffold
def test_home_is_honest_about_missing_services(monkeypatch):
    monkeypatch.setenv("MODEL_ADAPTER", "mock")
    with TestClient(create_app()) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "Validation results are not connected to this page yet" in response.text
    assert "no AI model is connected" in response.text


@pytest.mark.scaffold
def test_unsupported_adapter_fails_visibly(monkeypatch):
    monkeypatch.setenv("MODEL_ADAPTER", "external")
    with pytest.raises(RuntimeError, match="mock only"):
        create_app()

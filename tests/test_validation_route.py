import pytest
from fastapi.testclient import TestClient

from app import main
from app.services.validation import ValidationServiceError


@pytest.mark.req("REQ-01")
def test_app_preserves_validator_result(monkeypatch):
    result = {
        "status": "fail", "outcome": {"resourceType": "OperationOutcome", "issue": [
            {"severity": "error", "code": "required", "details": {"text": "Missing status"}}
        ]},
    }
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        response = client.post("/api/validate", json={"resourceType": "Bundle"})
    assert response.status_code == 200
    assert response.json() == result


@pytest.mark.req("REQ-01")
def test_app_surfaces_infrastructure_failure(monkeypatch):
    def fail(payload):
        raise ValidationServiceError("Validator unavailable")

    monkeypatch.setattr(main, "request_validation", fail)
    with TestClient(main.create_app()) as client:
        response = client.post("/api/validate", json={"resourceType": "Bundle"})
    assert response.status_code == 503
    assert "status" not in response.json()

import copy
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.services.presentation import issue_id, json_lines, load_fixture, locate, present
from app.services.validation import ValidationServiceError

EVIDENCE = Path(__file__).resolve().parents[1] / "docs/examples/step-1"


def recorded(name="broken-profile-and-reference"):
    return json.loads((EVIDENCE / f"{name}.json").read_text())


@pytest.mark.req("REQ-12")
def test_finding_identity_survives_reordering_and_volatile_metadata():
    result = recorded()
    original = {issue_id(i) for i in result["outcome"]["issue"]}
    varied = copy.deepcopy(result)
    varied["outcome"]["issue"].reverse()
    for issue in varied["outcome"]["issue"]:
        issue.setdefault("extension", []).append({
            "url": "http://hl7.org/fhir/StructureDefinition/operationoutcome-issue-line",
            "valueInteger": 999,
        })
        issue["location"] = ["/tmp/another-input.json"]
    assert {issue_id(i) for i in varied["outcome"]["issue"]} == original
    changed = copy.deepcopy(result["outcome"]["issue"][0])
    changed["severity"] = "fatal"
    assert issue_id(changed) not in original


@pytest.mark.req("REQ-12")
def test_temporary_paths_do_not_change_identity():
    first = {"severity": "error", "diagnostics": "Problem /tmp/fhir-preflight-aaa/input.json"}
    second = {**first, "diagnostics": "Problem /tmp/fhir-preflight-bbb/input.json"}
    assert issue_id(first) == issue_id(second)


@pytest.mark.req("REQ-13")
def test_typed_choice_path_highlights_exact_unit_line():
    payload = load_fixture("broken-profile-and-reference")
    lines, ranges = json_lines(payload)
    path = "Bundle.entry[1].resource/*Observation/demo-weight*/.value.ofType(Quantity).code"
    match = locate(payload, path, ranges)
    assert match["start"] == match["end"]
    assert '"code": "kg"' in lines[match["start"] - 1]["text"]
    assert match["note"].startswith("Matching JSON")
    assert locate(payload, "Bundle.entry[1].resource.value[x].code", ranges) == match


@pytest.mark.req("REQ-13")
def test_missing_field_and_unsupported_path_are_honest_fallbacks():
    payload = load_fixture("broken-structure")
    _, ranges = json_lines(payload)
    missing = locate(payload, "Bundle.entry[1].resource.status", ranges)
    assert (missing["start"], missing["end"]) == ranges[("entry", 1, "resource")]
    assert "Closest matching parent" in missing["note"]
    unsupported = locate(payload, "Bundle.entry.where(id='x')", ranges)
    assert "Closest matching parent" in unsupported["note"]
    assert locate(payload, "Observation.subject", ranges)["start"] == 0


@pytest.mark.req("REQ-13")
def test_displayed_json_is_the_original_payload():
    payload = load_fixture("valid-infant-weight")
    lines, _ = json_lines(payload)
    assert json.loads("\n".join(line["text"] for line in lines)) == payload


@pytest.mark.req("REQ-14")
@pytest.mark.req("REQ-01")
@pytest.mark.parametrize("name", [
    "valid-infant-weight", "broken-structure", "broken-profile-and-reference"
])
def test_ui_uses_selected_fixture_and_validator_result(monkeypatch, name):
    result = recorded(name)
    calls = []

    def validate(payload):
        calls.append(payload)
        return result

    monkeypatch.setattr(main, "request_validation", validate)
    with TestClient(main.create_app()) as client:
        response = client.post(f"/workbench/validate?fixture={name}")
        assert response.status_code == 200
        expected = "Pass — configured checks" if result["status"] == "pass" else "Validation failed"
        assert expected in response.text
        assert "Remote terminology off" in response.text
        assert "COMING IN A LATER STEP" in response.text
        assert calls == [load_fixture(name)]
        fresh = client.get("/?fixture=broken-structure")
        assert "Ready to check" in fresh.text
        assert "Pass — configured checks" not in fresh.text
        assert 'class="issue-card' not in fresh.text


@pytest.mark.req("REQ-01")
@pytest.mark.req("REQ-14")
def test_unavailable_validator_shows_incomplete_without_old_results(monkeypatch):
    def unavailable(payload):
        raise ValidationServiceError("Validator unavailable")

    monkeypatch.setattr(main, "request_validation", unavailable)
    with TestClient(main.create_app()) as client:
        response = client.post("/workbench/validate?fixture=valid-infant-weight")
    assert response.status_code == 503
    assert "Validation incomplete" in response.text
    assert "Pass — configured checks" not in response.text
    assert 'class="issue-card' not in response.text


@pytest.mark.req("REQ-01")
@pytest.mark.parametrize("result", [[], {}, {"status": "pass", "outcome": {
    "resourceType": "OperationOutcome", "issue": [{"severity": "error"}]
}}])
def test_malformed_or_contradictory_result_cannot_show_pass(monkeypatch, result):
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        response = client.post("/workbench/validate?fixture=valid-infant-weight")
    assert response.status_code == 503
    assert "Validation incomplete" in response.text


@pytest.mark.req("REQ-02")
def test_display_ignores_injected_model_claim_and_preserves_original_result(monkeypatch):
    result = recorded()
    result["explanation"] = {"status": "pass", "text": "Actually valid"}
    original = copy.deepcopy(result)
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        response = client.post("/workbench/validate?fixture=broken-profile-and-reference")
    assert "Validation failed" in response.text
    assert "Pass — configured checks" not in response.text
    assert result == original


@pytest.mark.req("REQ-14")
def test_unknown_fixture_does_not_read_arbitrary_files_or_call_validator(monkeypatch):
    def unexpected(payload):
        pytest.fail("Validator must not be called for unknown fixtures")

    monkeypatch.setattr(main, "request_validation", unexpected)
    with TestClient(main.create_app()) as client:
        assert client.get("/?fixture=../../.env").status_code == 404
        assert client.post("/workbench/validate?fixture=unknown").status_code == 404


@pytest.mark.req("REQ-13")
def test_validator_messages_are_escaped_in_html(monkeypatch):
    result = recorded()
    result["outcome"]["issue"][0]["details"]["text"] = '<script>alert("x")</script>'
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        response = client.post("/workbench/validate?fixture=broken-profile-and-reference")
    assert '<script>alert("x")</script>' not in response.text
    assert "&lt;script&gt;" in response.text
    assert present(load_fixture("broken-structure"))["issues"] == []

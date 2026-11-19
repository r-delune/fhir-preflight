import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.services.presentation import nested_message
from app.services.validation import ValidationServiceError

EVIDENCE = Path(__file__).resolve().parents[1] / "docs/examples/step-1"
NOTE = "Original HL7 validator wording. A plain-English AI explanation arrives in Step 4."


@pytest.mark.req("REQ-15")
@pytest.mark.parametrize("name,meaning", [
    ("valid-infant-weight", "this run returned no error or fatal findings"),
    ("broken-profile-and-reference", "at least one error or fatal finding"),
])
def test_completed_run_explains_checks_limits_severities_and_links(monkeypatch, name, meaning):
    result = json.loads((EVIDENCE / f"{name}.json").read_text())
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        response = client.post(f"/workbench/validate?fixture={name}")
    assert response.status_code == 200
    for text in [meaning, "no remote terminology service", "demo profile", "enabled invariants",
                 "Fatal", "Error", "Warning", "Information", "Build step 2 of 8"]:
        assert text in response.text
    for link in ["requirements#req-02", "adr-002", "cr-000", "roadmap"]:
        assert f'/governance?doc={link}' in response.text
    assert 'data-pipeline-stage="findings" class="current"' in response.text
    assert response.text.count(NOTE) == len(result["outcome"]["issue"])
    assert response.text.count('class="future" aria-disabled="true"') == 3
    assert "STEP 02" not in response.text


@pytest.mark.req("REQ-15")
def test_initial_and_incomplete_stages_are_honest(monkeypatch):
    def fail(payload):
        raise ValidationServiceError("Unavailable")

    monkeypatch.setattr(main, "request_validation", fail)
    with TestClient(main.create_app()) as client:
        first = client.get("/")
        failed = client.post("/workbench/validate?fixture=valid-infant-weight")
    assert 'data-pipeline-stage="example" class="current"' in first.text
    assert 'data-pipeline-stage="validator" class="current"' in failed.text
    assert "What this run means" not in failed.text


@pytest.mark.req("REQ-15")
def test_real_nested_message_is_only_a_verbatim_source_excerpt(monkeypatch):
    result = json.loads((EVIDENCE / "broken-profile-and-reference.json").read_text())
    raw = next(i["details"]["text"] for i in result["outcome"]["issue"]
               if "message=" in i.get("details", {}).get("text", ""))
    summary = nested_message(raw)
    assert summary == "Value is '8310-5' but is fixed to '29463-7'"
    assert summary in raw
    monkeypatch.setattr(main, "request_validation", lambda payload: result)
    with TestClient(main.create_app()) as client:
        page = client.post("/workbench/validate?fixture=broken-profile-and-reference")
    assert "Full original validator text" in page.text
    assert "Extracted nested validator message" in page.text
    assert "ValidationMessage[level=ERROR" in page.text


@pytest.mark.req("REQ-15")
@pytest.mark.parametrize("raw,expected", [
    ("A normal validator message", None),
    ("Issues: [ValidationMessage[message=Expected [a, b]]]", "Expected [a, b]"),
    ("Issues: [ValidationMessage[message=Value is 'a]b' but should be 'c']]",
     "Value is 'a]b' but should be 'c'"),
    ("Issues: [ValidationMessage[message=The patient's field is missing]]",
     "The patient's field is missing"),
])
def test_nested_extraction_preserves_brackets_and_quotes(raw, expected):
    summary = nested_message(raw)
    assert summary == expected
    if summary:
        assert summary in raw

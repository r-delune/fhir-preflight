import hashlib
import json
import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.governance_catalog import DOCUMENTS
from app.main import create_app
from app.services.document_source import MANIFEST, metadata_and_body, provenance, source_bytes
from app.services.governance import get_document, render_markdown, safe_href

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.req("REQ-16")
@pytest.mark.parametrize("url", [
    "/governance?doc=../../.env", "/governance?doc=%2e%2e%2f.env",
    "/governance?doc=%252e%252e%252f.env", "/governance?doc=/etc/passwd",
    "/governance?doc=docs/REQUIREMENTS.md", "/governance?doc=..%5c.env",
    "/governance?doc=file:///etc/passwd", "/governance/%2e%2e/.env",
])
def test_traversal_and_paths_are_not_document_ids(url):
    with TestClient(create_app()) as client:
        assert client.get(url).status_code == 404


@pytest.mark.req("REQ-16")
def test_file_and_directory_symlinks_are_rejected(tmp_path):
    secret = tmp_path / ".env"
    secret.write_text("PRIVATE_TEST_SENTINEL")
    (tmp_path / "ROADMAP.md").symlink_to(secret)
    with pytest.raises(FileNotFoundError):
        source_bytes("roadmap", tmp_path)
    alternate = tmp_path / "alternate"
    alternate.mkdir()
    (alternate / "RISK.md").write_text("Not the allowlisted source")
    (tmp_path / "docs").symlink_to(alternate, target_is_directory=True)
    with pytest.raises(FileNotFoundError):
        source_bytes("risk", tmp_path)


@pytest.mark.req("REQ-16")
def test_unreadable_source_fails_closed(monkeypatch):
    original = Path.read_bytes

    def deny_roadmap(path):
        if path == ROOT / "ROADMAP.md":
            raise PermissionError("Private source file")
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", deny_roadmap)
    with pytest.raises(FileNotFoundError, match="unavailable"):
        source_bytes("roadmap")


@pytest.mark.req("REQ-16")
def test_catalog_deliberately_covers_every_adr_change_and_regulatory_draft():
    required = {"ROADMAP.md", "BUILD_JOURNAL.md", "docs/INTENDED_PURPOSE.md",
                "docs/REQUIREMENTS.md", "docs/TRACEABILITY.md", "docs/RISK.md",
                "docs/SOUP.md", "docs/ANOMALIES.md"}
    for pattern in ["docs/decisions/ADR-*.md", "docs/changes/CR-*.md", "docs/regulatory/*.md"]:
        required.update(str(path.relative_to(ROOT)) for path in ROOT.glob(pattern))
    allowed = {entry[1] for entry in DOCUMENTS.values()}
    assert required <= allowed
    for key in DOCUMENTS:
        meta, _ = metadata_and_body(source_bytes(key).decode())
        assert meta["status"] in {"draft", "approved"}
        assert meta["drafted_by"] != "Unrecorded"


@pytest.mark.req("REQ-16")
def test_source_file_is_read_on_each_request_not_copied_into_a_template(tmp_path):
    file = tmp_path / "ROADMAP.md"
    file.write_text("---\nstatus: draft\ndrafted_by: Test drafter\n---\n\n# First source")
    first = get_document("roadmap", tmp_path)
    assert "First source" in first["html"]
    file.write_text("---\nstatus: draft\ndrafted_by: Another drafter\n---\n\n# Changed source")
    second = get_document("roadmap", tmp_path)
    assert "Changed source" in second["html"] and "First source" not in second["html"]
    assert second["drafted_by"] == "Another drafter"


@pytest.mark.req("REQ-16")
@pytest.mark.parametrize("payload", [
    '<script>alert(1)</script>', '<img src=x onerror="alert(1)">',
    '<svg onload="alert(1)"></svg>', '<iframe srcdoc="x"></iframe>',
    '[bad](javascript:alert(1))', '[bad](JaVaScRiPt:alert(1))',
    '[bad](vbscript:alert(1))', '[bad](data:text/html;base64,abc)',
    '[bad](javascript&#58;alert(1))', '[bad](//example.org/payload)',
    '![x](https://example.org/image.svg)', '<style>body{display:none}</style>',
])
def test_markdown_cannot_create_active_content(payload):
    output = str(render_markdown(payload, "docs/REQUIREMENTS.md"))
    for bad in ['<script', '<img', '<svg', '<iframe', '<style',
                'href="javascript:', 'href="vbscript:', 'href="data:', 'href="//']:
        assert bad not in output.lower()


@pytest.mark.req("REQ-16")
def test_safe_links_tables_and_requirement_anchors():
    assert safe_href("decisions/ADR-002-validator-service.md", "docs/REQUIREMENTS.md") == (
        "/governance?doc=adr-002")
    assert safe_href("../ROADMAP.md", "docs/REQUIREMENTS.md") == "/governance?doc=roadmap"
    assert safe_href("../../.env", "docs/REQUIREMENTS.md") is None
    assert safe_href("file:///etc/passwd", "docs/REQUIREMENTS.md") is None
    assert safe_href("https://hl7.org/fhir/R4/", "README.md") == "https://hl7.org/fhir/R4/"
    rendered = get_document("requirements")["html"]
    assert '<tr id="req-02">' in rendered
    assert '<tr id="req-15">' in rendered and '<tr id="req-16">' in rendered
    assert '<h3 id="step-2">' in get_document("build-journal")["html"]


@pytest.mark.req("REQ-16")
def test_status_and_authorship_are_explicit_metadata_not_inferred_from_body():
    metadata, _ = metadata_and_body("# Approved by Brian\nBuild step approved")
    assert metadata["status"] == "draft"
    assert metadata["drafted_by"] == "Unrecorded"
    metadata, _ = metadata_and_body(
        "---\nstatus: approved\ndrafted_by: Codex\n---\n# Draft")
    assert metadata["status"] == "draft"
    metadata, _ = metadata_and_body(
        "---\nstatus: approved\ndrafted_by: Test drafter\napproved_by: Test reviewer\n"
        "approved_on: 2026-11-19\n---\n# Reviewed document")
    assert metadata["status"] == "approved" and metadata["approved_by"] == "Test reviewer"


@pytest.mark.req("REQ-16")
def test_exact_and_dirty_git_provenance(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    file = tmp_path / "ROADMAP.md"
    file.write_text("# Committed source")
    subprocess.run(["git", "-C", str(tmp_path), "add", "ROADMAP.md"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Test", "-c",
                    "user.email=test@example.invalid", "commit", "-m", "Fixture"],
                   check=True, capture_output=True)
    exact = provenance("roadmap", file.read_bytes(), tmp_path)
    assert exact["committed"] is True and len(exact["commit"]) == 40
    file.write_text("# Uncommitted source")
    dirty = provenance("roadmap", file.read_bytes(), tmp_path)
    assert dirty["committed"] is False and "Working copy" in dirty["state"]
    assert dirty["commit"] == exact["commit"]


@pytest.mark.req("REQ-16")
def test_docker_manifest_provenance_verifies_content_hash(tmp_path):
    manifest = tmp_path / MANIFEST
    manifest.parent.mkdir()
    content = b"# Image snapshot"
    payload = {"commit": "a" * 40, "documents": {"ROADMAP.md": {
        "sha256": hashlib.sha256(content).hexdigest(), "committed": True}}}
    manifest.write_text(json.dumps(payload))
    assert provenance("roadmap", content, tmp_path)["committed"] is True
    changed = provenance("roadmap", b"# Different content", tmp_path)
    assert changed["committed"] is False and "Modified since image build" in changed["state"]
    payload["documents"]["ROADMAP.md"]["committed"] = False
    manifest.write_text(json.dumps(payload))
    assert "Working copy" in provenance("roadmap", content, tmp_path)["state"]
    manifest.unlink()
    assert provenance("roadmap", content, tmp_path)["commit"] is None


@pytest.mark.req("REQ-16")
def test_governance_is_read_only_and_uses_restrictive_headers():
    with TestClient(create_app()) as client:
        page = client.get("/governance?doc=requirements")
        assert page.status_code == 200
        assert "Drafted by Codex" in page.text
        assert "Git commit:" in page.text
        assert "script-src 'none'" in page.headers["content-security-policy"]
        assert '<tr id="req-02">' in page.text
        assert client.post("/governance?doc=requirements", content="overwrite").status_code == 405
        assert client.put("/governance?doc=requirements", content="overwrite").status_code == 405


@pytest.mark.req("REQ-16")
def test_every_cataloged_document_can_be_rendered():
    with TestClient(create_app()) as client:
        for document_id, (_, path, _) in DOCUMENTS.items():
            page = client.get(f"/governance?doc={document_id}")
            assert page.status_code == 200, document_id
            assert path in page.text
            assert 'class="doc-status ' in page.text


@pytest.mark.req("REQ-16")
def test_authorship_metadata_is_escaped_in_the_page(tmp_path, monkeypatch):
    (tmp_path / "ROADMAP.md").write_text(
        '---\nstatus: draft\ndrafted_by: <img src=x onerror="alert(1)">\n---\n# Safe source')
    selected = get_document("roadmap", tmp_path)
    monkeypatch.setattr(main, "get_document", lambda key: selected)
    monkeypatch.setattr(main, "document_index", lambda: [])
    with TestClient(create_app()) as client:
        page = client.get("/governance")
    assert '<img src=x' not in page.text
    assert '&lt;img src=x' in page.text


@pytest.mark.req("REQ-16")
@pytest.mark.parametrize("setting", [None, "0", "true"])
def test_api_documentation_endpoints_are_404_by_default(monkeypatch, setting):
    if setting is None:
        monkeypatch.delenv("ENABLE_API_DOCS", raising=False)
    else:
        monkeypatch.setenv("ENABLE_API_DOCS", setting)
    with TestClient(create_app()) as client:
        for path in ["/docs", "/redoc", "/openapi.json"]:
            assert client.get(path).status_code == 404


@pytest.mark.req("REQ-16")
def test_exact_opt_in_enables_api_documentation(monkeypatch):
    monkeypatch.setenv("ENABLE_API_DOCS", "1")
    with TestClient(create_app()) as client:
        for path in ["/docs", "/redoc", "/openapi.json"]:
            assert client.get(path).status_code == 200

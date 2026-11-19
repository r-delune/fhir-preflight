"""Repository reads, flat metadata and verifiable source provenance; no rendering."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

from app.governance_catalog import DOCUMENTS

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ".cache/workbench-source.json"


def source_bytes(document_id: str, root: Path = ROOT) -> bytes:
    if document_id not in DOCUMENTS:
        raise FileNotFoundError("Unknown governance document")
    try:
        path = root.resolve() / DOCUMENTS[document_id][1]
        # Reject both file and parent-directory symlinks, including aliases inside the repo.
        if path.resolve() != path or not path.is_file():
            raise FileNotFoundError("Governance document missing or redirected")
        return path.read_bytes()
    except OSError:
        raise FileNotFoundError("Governance document unavailable") from None


def metadata_and_body(source: str) -> tuple[dict, str]:
    metadata = {}
    lines = source.splitlines()
    if lines and lines[0] == "---" and "---" in lines[1:]:
        end = lines.index("---", 1)
        for line in lines[1:end]:
            key, separator, value = line.partition(":")
            if separator and key in {"status", "drafted_by", "approved_by", "approved_on"}:
                metadata[key] = value.strip()
        source = "\n".join(lines[end + 1:])
    approved = (metadata.get("status") == "approved" and bool(metadata.get("approved_by"))
                and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", metadata.get("approved_on", ""))))
    return {
        "status": "approved" if approved else "draft",
        "drafted_by": metadata.get("drafted_by") or "Unrecorded",
        "approved_by": metadata.get("approved_by") if approved else None,
        "approved_on": metadata.get("approved_on") if approved else None,
    }, source


def git_output(root: Path, *arguments: str) -> bytes | None:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *arguments], capture_output=True,
            check=True, timeout=3,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None


def provenance(document_id: str, content: bytes, root: Path = ROOT) -> dict:
    digest = hashlib.sha256(content).hexdigest()
    relative = DOCUMENTS[document_id][1]
    commit = git_output(root, "rev-parse", "HEAD") if (root / ".git").exists() else None
    if commit:
        sha = commit.decode().strip()
        clean = git_output(root, "show", f"HEAD:{relative}") == content
        return {"commit": sha, "state": "Committed content" if clean else
                "Working copy based on this commit", "sha256": digest, "committed": clean}
    try:
        manifest = json.loads((root / MANIFEST).read_text())
        sha = manifest["commit"]
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
            raise ValueError("Unknown build commit")
        item = manifest["documents"][relative]
        matches = item["sha256"] == digest
        clean = matches and item["committed"] is True
        return {"commit": sha, "state": "Committed content" if clean else
                "Working copy based on this commit" if matches else
                "Modified since image build; based on this commit",
                "sha256": digest, "committed": clean}
    except (OSError, ValueError, KeyError, TypeError):
        return {"commit": None, "state": "Git provenance unavailable",
                "sha256": digest, "committed": False}


def build_manifest(root: Path = ROOT) -> dict:
    commit = git_output(root, "rev-parse", "HEAD")
    if not commit:
        raise RuntimeError("A git commit is required to prepare image provenance.")
    files = {}
    for document_id, (_, relative, _) in DOCUMENTS.items():
        content = source_bytes(document_id, root)
        files[relative] = {"sha256": hashlib.sha256(content).hexdigest(),
                           "committed": git_output(root, "show", f"HEAD:{relative}") == content}
    return {"commit": commit.decode().strip(), "documents": files}

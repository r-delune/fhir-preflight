"""Record git and per-document hashes before Docker copies the source snapshot."""

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from app.services.document_source import MANIFEST, build_manifest  # noqa: E402

if __name__ == "__main__":
    destination = PROJECT / MANIFEST
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(build_manifest(PROJECT), indent=2) + "\n")
    print("Governance source hashes and git provenance recorded for Docker build.")

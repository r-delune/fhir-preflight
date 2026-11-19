"""Record exact installed FHIR packages and compare them with the reviewed baseline."""

import hashlib
import json
from pathlib import Path

from validator.runner import ROOT


def inventory() -> list[dict]:
    packages = []
    for manifest in sorted((Path.home() / ".fhir/packages").glob("*/package/package.json")):
        metadata = json.loads(manifest.read_text())
        digest = hashlib.sha256()
        for file in sorted(manifest.parent.rglob("*")):
            if not file.is_file() or file.name.startswith(".index"):
                continue
            digest.update(str(file.relative_to(manifest.parent)).encode() + b"\0")
            digest.update(hashlib.sha256(file.read_bytes()).digest())
        packages.append({
            "name": metadata["name"], "version": metadata["version"],
            "content_sha256": digest.hexdigest(),
        })
    return packages


if __name__ == "__main__":
    actual = inventory()
    baseline = ROOT / "validator/packages.lock.json"
    if baseline.exists() and actual != json.loads(baseline.read_text()):
        raise RuntimeError("FHIR package inventory differs from baseline; review before use.")
    print(json.dumps(actual, indent=2))

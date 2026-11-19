"""Download the exact upstream JAR into an ignored cache and verify its checksum."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "validator/config.json").read_text())
    target = ROOT / ".cache/validator/validator_cli.jar"
    expected = config["validator_sha256"]
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        print("Pinned validator already cached and verified.")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    url = (
        "https://github.com/hapifhir/org.hl7.fhir.core/releases/download/"
        + config["validator_version"] + "/validator_cli.jar"
    )
    temporary = target.with_suffix(".download")
    # System curl uses the OS certificate store; retain partial downloads for retry.
    subprocess.run([
        "curl", "--fail", "--location", "--show-error", "--silent",
        "--continue-at", "-", "--connect-timeout", "30", "--max-time", "1200",
        "--output", str(temporary), url,
    ], check=True)
    if hashlib.sha256(temporary.read_bytes()).hexdigest() != expected:
        temporary.unlink()
        raise RuntimeError("Validator checksum mismatch; download will not be used.")
    temporary.replace(target)
    print("Pinned validator downloaded and verified.")


if __name__ == "__main__":
    main()

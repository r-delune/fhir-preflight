"""Execute HL7's validator and preserve its OperationOutcome."""

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "validator/config.json").read_text())
JAR = ROOT / ".cache/validator/validator_cli.jar"
PROFILE = ROOT / "fhir/profiles/demo-infant-weight.json"


class ValidatorUnavailable(RuntimeError):
    """Infrastructure failure; must never be interpreted as a passing payload."""


def status_from_outcome(outcome: dict) -> str:
    if not isinstance(outcome, dict) or outcome.get("resourceType") != "OperationOutcome":
        raise ValidatorUnavailable("Validator did not return an OperationOutcome.")
    issues = outcome.get("issue")
    if not isinstance(issues, list) or not issues:
        raise ValidatorUnavailable("Validator returned no usable issues.")
    severities = []
    for issue in issues:
        if not isinstance(issue, dict) or issue.get("severity") not in {
            "fatal", "error", "warning", "information"
        }:
            raise ValidatorUnavailable("Validator returned an unknown issue severity.")
        severities.append(issue["severity"])
    return "fail" if any(s in {"fatal", "error"} for s in severities) else "pass"


def build_command(source: Path, output: Path, *, bootstrap: bool = False) -> list[str]:
    command = [
        "java", "-Xmx2g", "-jar", str(JAR), str(source),
        "-version", CONFIG["fhir_version"],
        "-ig", str(PROFILE),
        "-bundle", "Observation", CONFIG["profile_url"],
        "-tx", "n/a", "-output", str(output),
    ]
    # Dependencies are fetched during image bootstrap, never during a validation request.
    if not bootstrap:
        command.append("-no-http-access")
    return command


def validate(payload: dict, *, bootstrap: bool = False) -> dict:
    if not JAR.exists() or hashlib.sha256(JAR.read_bytes()).hexdigest() != CONFIG[
        "validator_sha256"
    ]:
        raise ValidatorUnavailable("Pinned validator JAR missing or checksum mismatch.")
    with tempfile.TemporaryDirectory(prefix="fhir-preflight-") as folder:
        source, output = Path(folder) / "input.json", Path(folder) / "outcome.json"
        encoded = json.dumps(payload, ensure_ascii=False).encode()
        source.write_bytes(encoded)
        try:
            process = subprocess.run(
                build_command(source, output, bootstrap=bootstrap),
                capture_output=True, text=True, timeout=180, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ValidatorUnavailable(f"Validator could not complete: {exc}") from exc
        if not output.exists():
            raise ValidatorUnavailable(
                f"Validator exited {process.returncode} without an outcome. "
                + (process.stdout + process.stderr)[-5000:]
            )
        try:
            outcome = json.loads(output.read_text())
        except (OSError, ValueError) as exc:
            raise ValidatorUnavailable("Validator output is unreadable.") from exc
        status = status_from_outcome(outcome)
        # HL7 may exit 1 for invalid data; other failures must not become a clean pass.
        if process.returncode not in {0, 1} or (process.returncode == 1 and status == "pass"):
            raise ValidatorUnavailable(f"Validator exit/outcome mismatch: {process.returncode}.")
        return {
            "status": status,
            "outcome": outcome,
            "provenance": {
                **CONFIG,
                "input_sha256": hashlib.sha256(encoded).hexdigest(),
                "profile_sha256": hashlib.sha256(PROFILE.read_bytes()).hexdigest(),
                "validator_exit_code": process.returncode,
            },
            "checks": {
                "structure": "completed", "profile": "completed", "invariants": "completed",
                "references": "demo profile requires subject resolution within supplied data",
                "remote_terminology": "disabled; local terminology checks may still run",
            },
        }


if __name__ == "__main__":
    import sys

    result = validate(
        json.loads((ROOT / "fhir/fixtures/valid-infant-weight.json").read_text()),
        bootstrap="--bootstrap" in sys.argv,
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "pass":
        raise SystemExit(1)

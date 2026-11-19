import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from validator import runner


@pytest.mark.req("REQ-01")
@pytest.mark.parametrize(
    ("severities", "expected"),
    [(["information"], "pass"), (["warning"], "pass"),
     (["error"], "fail"), (["warning", "fatal"], "fail")],
)
def test_status_uses_validator_severity(severities, expected):
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": severity, "code": "processing"} for severity in severities],
    }
    assert runner.status_from_outcome(outcome) == expected


@pytest.mark.req("REQ-01")
@pytest.mark.parametrize("outcome", [
    {}, {"resourceType": "Bundle"},
    {"resourceType": "OperationOutcome", "issue": []},
    {"resourceType": "OperationOutcome", "issue": [{"severity": "unknown"}]},
])
def test_unusable_outcome_cannot_pass(outcome):
    with pytest.raises(runner.ValidatorUnavailable):
        runner.status_from_outcome(outcome)


@pytest.fixture
def fake_jar(tmp_path, monkeypatch):
    jar = tmp_path / "validator.jar"
    jar.write_bytes(b"stand-in for process boundary tests; not a validator")
    monkeypatch.setattr(runner, "JAR", jar)
    monkeypatch.setitem(
        runner.CONFIG, "validator_sha256", hashlib.sha256(jar.read_bytes()).hexdigest()
    )


@pytest.mark.req("REQ-01")
@pytest.mark.parametrize("failure", ["timeout", "crash", "no-output", "bad-json", "mismatch"])
def test_process_failures_are_incomplete_not_pass(fake_jar, monkeypatch, failure):
    def run(command, **kwargs):
        if failure == "timeout":
            raise subprocess.TimeoutExpired(command, 180)
        if failure == "crash":
            raise OSError("Java unavailable")
        output = Path(command[command.index("-output") + 1])
        if failure == "bad-json":
            output.write_text("not json")
        elif failure == "mismatch":
            output.write_text(json.dumps({
                "resourceType": "OperationOutcome",
                "issue": [{"severity": "information", "code": "informational"}],
            }))
        return SimpleNamespace(returncode=1, stdout="failed", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", run)
    with pytest.raises(runner.ValidatorUnavailable):
        runner.validate({"resourceType": "Bundle"})


@pytest.mark.req("REQ-01")
def test_invalid_data_outcome_is_preserved(fake_jar, monkeypatch):
    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [{"severity": "error", "code": "required", "diagnostics": "Missing status"}],
    }

    def run(command, **kwargs):
        Path(command[command.index("-output") + 1]).write_text(json.dumps(outcome))
        return SimpleNamespace(returncode=1, stdout="", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", run)
    result = runner.validate({"resourceType": "Bundle"})
    assert result["status"] == "fail"
    assert result["outcome"] == outcome


@pytest.mark.req("REQ-11")
def test_runtime_disables_remote_access_and_terminology():
    command = runner.build_command(Path("input.json"), Path("outcome.json"))
    assert command[command.index("-tx") + 1] == "n/a"
    assert "-no-http-access" in command
    bootstrap = runner.build_command(Path("input.json"), Path("outcome.json"), bootstrap=True)
    assert "-no-http-access" not in bootstrap


@pytest.mark.req("REQ-01")
def test_checksum_mismatch_prevents_execution(tmp_path, monkeypatch):
    jar = tmp_path / "modified.jar"
    jar.write_bytes(b"unexpected content")
    monkeypatch.setattr(runner, "JAR", jar)
    with pytest.raises(runner.ValidatorUnavailable, match="checksum"):
        runner.validate({})

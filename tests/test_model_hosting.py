import io
import json

import pytest

from model.config import REVISION, SERVED_NAME, compute_usd, server_command, server_environment
from model.smoke import check_url, completion


@pytest.mark.req("REQ-17")
def test_pinned_command_and_secret_boundary():
    command = server_command()
    key = "private-token-" * 4
    assert REVISION in command[2]
    assert "--trust-remote-code" not in command
    assert command[command.index("--max-model-len") + 1] == "4096"
    assert "--no-enable-log-requests" in command
    assert "--no-enable-log-outputs" in command
    assert key not in " ".join(command)
    assert server_environment({"PREFLIGHT_API_KEY": key})["VLLM_API_KEY"] == key
    with pytest.raises(ValueError):
        server_environment({})
    assert compute_usd(1800) == pytest.approx(0.5873004)


@pytest.mark.req("REQ-17")
@pytest.mark.parametrize("url", [
    "http://x.modal.run", "https://x.modal.run.evil.org", "https://a:x@x.modal.run",
    "https://x.modal.run/v1", "https://x.modal.run?key=secret", "https://x.modal.run:123",
])
def test_probe_rejects_unapproved_targets(url):
    with pytest.raises(ValueError):
        check_url(url)


@pytest.mark.req("REQ-17")
def test_mock_measurement_and_no_model_fallback():
    class Client:
        model = SERVED_NAME

        def open(self, request, timeout):
            assert timeout == 600
            assert request.get_header("Authorization") == "Bearer fake"
            payload = json.loads(request.data)
            assert payload["chat_template_kwargs"] == {"enable_thinking": False}
            return io.BytesIO(json.dumps({
                "model": self.model, "usage": {"completion_tokens": 4},
                "choices": [{"message": {"content": "synthetic smoke test"}}],
            }).encode())

    client = Client()
    ticks = iter([10, 12])
    measured = completion(client, "https://example.modal.run", "fake", lambda: next(ticks))
    assert measured["seconds"] == 2
    assert measured["end_to_end_tokens_per_second"] == 2
    client.model = "another-model"
    with pytest.raises(ValueError, match="no fallback"):
        completion(client, "https://example.modal.run", "fake")


@pytest.mark.req("REQ-17")
def test_deployment_caps_are_registered_without_remote_calls(monkeypatch):
    import importlib
    import sys
    import types

    functions = []

    class Image:
        @staticmethod
        def from_registry(image, add_python):
            assert "@sha256:" in image
            assert add_python == "3.12"
            return Image()

        def pip_install(self, *packages):
            assert packages == ("vllm==0.21.0", "transformers==5.8.1")
            return self

    class App:
        def __init__(self, name):
            assert name == "fhir-preflight-model"

        def function(self, **kwargs):
            functions.append(kwargs)
            return lambda fn: fn

    fake = types.SimpleNamespace(
        App=App, Image=Image,
        Volume=types.SimpleNamespace(from_name=lambda *a, **kw: object()),
        Secret=types.SimpleNamespace(from_name=lambda *a, **kw: object()),
        concurrent=lambda **kw: lambda fn: fn,
        web_server=lambda *a, **kw: lambda fn: fn,
    )
    monkeypatch.setitem(sys.modules, "modal", fake)
    monkeypatch.delitem(sys.modules, "model.serve", raising=False)
    importlib.import_module("model.serve")
    monkeypatch.delitem(sys.modules, "model.serve")
    cache, gpu, probe = functions
    assert "gpu" not in probe
    assert probe["cpu"] == (1, 1)
    assert "gpu" not in cache
    assert gpu["gpu"] == "L4"
    assert gpu["region"] == "eu"
    assert gpu["routing_region"] == "eu-west"
    assert gpu["min_containers"] == gpu["buffer_containers"] == 0
    assert gpu["max_containers"] == 1
    assert gpu["scaledown_window"] == 30
    assert gpu["memory"] == (16384, 16384)
    assert gpu["cpu"] == (2, 2)

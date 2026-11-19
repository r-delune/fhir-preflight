"""Deployment definition only. Cloud commands require cost approval; see runbook."""

import os
import subprocess

import modal

from model.config import (
    APP_NAME,
    GPU,
    MODEL_PATH,
    REGION,
    ROUTING_REGION,
    VOLUME_NAME,
    server_command,
    server_environment,
)
from model.runtime import runtime_image

app = modal.App(APP_NAME)
image = runtime_image()
cache = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)


@app.function(
    image=image, gpu=GPU, volumes={"/model-cache": cache},
    secrets=[modal.Secret.from_name("fhir-test", required_keys=["PREFLIGHT_API_KEY"])],
    region=REGION, routing_region=ROUTING_REGION,
    cpu=(2, 2), memory=(16384, 16384),
    min_containers=0, max_containers=1, buffer_containers=0,
    scaledown_window=30, startup_timeout=900, timeout=900,
)
@modal.concurrent(max_inputs=1)
@modal.web_server(8000, startup_timeout=900)
def serve():
    if not os.path.isfile(f"{MODEL_PATH}/runtime-versions.json"):
        raise RuntimeError("Pinned cache missing: run the approved CPU cache step first")
    # Key stays in the environment, never in command-line arguments or printed output.
    subprocess.Popen(server_command(), env=server_environment(dict(os.environ)))


@app.function(
    image=image, region=REGION, cpu=(1, 1), memory=(1024, 1024),
    secrets=[modal.Secret.from_name("fhir-test", required_keys=["PREFLIGHT_API_KEY"])],
    timeout=1800, max_containers=1,
)
def probe(url: str, confirmed_cold: bool = False):
    """Explicit CLI-only CPU probe; keeps the endpoint token in Modal's secret store."""
    import json
    from datetime import datetime, timezone

    from model.smoke import run_probe

    started = datetime.now(timezone.utc).isoformat()
    result = run_probe(url, os.environ["PREFLIGHT_API_KEY"], confirmed_cold)
    result["session_started_utc"] = started
    result["session_finished_utc"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(result, indent=2))
    return result

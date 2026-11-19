"""Deployment definition only. Cloud commands require cost approval; see runbook."""

import os
import subprocess

import modal

from model.config import (
    APP_NAME,
    GPU,
    IMAGE,
    MODEL_ID,
    MODEL_PATH,
    REGION,
    REVISION,
    ROUTING_REGION,
    VOLUME_NAME,
    server_command,
    server_environment,
)

app = modal.App(APP_NAME)
image = modal.Image.from_registry(IMAGE, add_python="3.12").pip_install(
    "vllm==0.21.0", "transformers==5.8.1"
)
cache = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)


@app.function(
    image=image, volumes={"/model-cache": cache}, region=REGION,
    cpu=(2, 2), memory=(4096, 4096), timeout=1800, max_containers=1,
)
def cache_weights():
    # Download on CPU rather than keep a GPU allocated during a large transfer.
    import importlib.metadata
    import json

    from huggingface_hub import snapshot_download

    snapshot_download(
        MODEL_ID, revision=REVISION, local_dir=MODEL_PATH,
        allow_patterns=["*.safetensors", "*.json", "*.txt", "*.model", "LICENSE", "README.md"],
    )
    versions = {
        name: importlib.metadata.version(name)
        for name in ("vllm", "transformers", "torch", "huggingface-hub")
    }
    with open(f"{MODEL_PATH}/runtime-versions.json", "w") as output:
        json.dump({"revision": REVISION, "versions": versions}, output, indent=2)
    cache.commit()
    return {"revision": REVISION, "versions": versions}


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

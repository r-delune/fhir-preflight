"""CPU-only cache app: registration never declares or imports a GPU function."""

import modal

from model.config import APP_NAME, MODEL_ID, MODEL_PATH, REGION, REVISION, VOLUME_NAME
from model.runtime import runtime_image

app = modal.App(f"{APP_NAME}-cache")
image = runtime_image()
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



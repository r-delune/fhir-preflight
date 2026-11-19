"""Shared pinned image definition; defining it allocates no GPU."""

import modal

from model.config import IMAGE


def runtime_image():
    return modal.Image.from_registry(IMAGE, add_python="3.12").pip_install(
        "vllm==0.21.0", "transformers==5.8.1"
    )

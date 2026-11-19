"""Reviewable hosted baseline. Importing this module makes no network calls."""

MODEL_ID = "Qwen/Qwen3-8B"
REVISION = "b968826d9c46dd6066d109eabc6255188de91218"
SERVED_NAME = f"qwen3-8b-{REVISION[:12]}"
MODEL_PATH = f"/model-cache/{REVISION}"
APP_NAME = "fhir-preflight-model"
VOLUME_NAME = "fhir-preflight-qwen3-cache"
IMAGE = (
    "nvidia/cuda:12.9.0-devel-ubuntu22.04@sha256:"
    "26cd7d00c09c1f3ff187929c7f4aa7e9273020cb18e86730f40e062e8ffa4d33"
)
GPU = "L4"
REGION = "eu"
ROUTING_REGION = "eu-west"


def server_command():
    return [
        "vllm", "serve", MODEL_PATH,
        "--served-model-name", SERVED_NAME,
        "--host", "0.0.0.0", "--port", "8000",
        "--dtype", "bfloat16", "--max-model-len", "4096",
        "--max-num-seqs", "1", "--gpu-memory-utilization", "0.90",
        "--enforce-eager", "--no-enable-log-requests", "--no-enable-log-outputs",
    ]


def server_environment(source):
    key = source.get("PREFLIGHT_API_KEY", "")
    if len(key) < 32 or key.strip() != key:
        raise ValueError("PREFLIGHT_API_KEY must be a private token of at least 32 characters")
    return {**source, "VLLM_API_KEY": key, "HF_HUB_OFFLINE": "1"}


def compute_usd(seconds):
    """Published rates, requested hard caps, broad EU multiplier; not a bill."""
    if seconds < 0:
        raise ValueError("Duration must be nonnegative")
    return seconds * (0.000222 + 2 * 0.0000131 + 16 * 0.00000222) * 1.15

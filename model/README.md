# Hosted model — Step 3 preparation

Qwen3-8B via vLLM on Modal; no local Ollama. Not deployed. The app remains mock.
See [explained runbook](../docs/runbooks/model-hosting.md),
[cost review](../docs/COSTS.md) and [ADR-005](../docs/decisions/ADR-005-bounded-model-hosting.md).

Secret contract: workspace r-delune, environment main, Custom secret fhir-test,
key PREFLIGHT_API_KEY, private random value at least 32 characters. This protects
the inference API and is separate from Modal CLI account credentials.
Never paste the value in chat or source. No paid provisioning is authorized yet.

CPU caching is now a separate app: `modal run --env main -m model.cache::cache_weights`.
It shares the pinned runtime image but never imports/registers GPU serving.
This avoids the ANOM-005 GPU payment-method check during CPU registration.

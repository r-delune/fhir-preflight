---
status: draft
drafted_by: Codex
---

# Step 3 — hosted model runbook

Trial authorized; latest budget is $1 current credit with no card charges. The model is Qwen3-8B (Apache-2.0)
running through vLLM on Modal's rented GPU. Your laptop runs the workbench and
sends a request; the GPU generates the text. No local Ollama. The current
workbench still uses mock output; connecting it is Step 4.

## 1. Local preparation (no cloud compute)
From the repository root:

```
uv sync --group hosting
uv run --group hosting modal --help
```

The first command installs the locked optional deployment SDK. The second shows
its CLI. Neither deploys the model. Verify the target workspace is r-delune,
environment main. Account/CLI login and endpoint password are separate credentials.
Run `uv run --group hosting modal token new` when ready to authenticate through
the browser; keep account credentials private. Do not print token configuration.

In Modal's Custom secret form use name `fhir-test`, key `PREFLIGHT_API_KEY`, value
a private random token at least 32 characters. Save it in your password manager.
Do not paste its value in chat or commit it. No Hugging Face token is required
for this public model. Confirm the secret exists without displaying its value.

## 2. Authorized spending control — verify before jobs
Review COSTS.md and ADR-005. Brian revised the budget to $1 current credit and confirmed setup in chat.
Do not set $15 or add a card. Record the latest account state and baseline billing.
Keep any existing stricter usage limit. Authorization does not prove a limit was saved. They may
build images, create persistent storage and consume credits/cash. A bearer key
does not stop unauthenticated requests waking compute. Do not share the URL.

## 3. Approved cache and deployment

```
uv run --group hosting modal run --env main -m model.cache::cache_weights
uv run --group hosting modal deploy --env main -m model.serve
```

The first registers a separate CPU-only app (no GPU functions to validate),
reuses/builds the pinned image and downloads only the pinned model snapshot to the
dedicated fhir-preflight-qwen3-cache volume using CPU. Save returned revision and
runtime versions plus Modal image/build identity in the trial record. It is a
large download; verify spend before proceeding. The second registers the serving
app; record its HTTPS URL. It can allocate a GPU when requested. No GPU/model
fallback is configured. Failure or memory exhaustion means stop and review.

## 4. Manual smoke measurement
Confirm zero GPU containers in the dashboard before the first request, then run:

```
uv run --group hosting modal run --env main -m model.serve::probe --url https://YOUR-ENDPOINT.modal.run --confirmed-cold
```

Replace only the URL. This explicit CPU-only test function reads the endpoint
token from the existing fhir-test secret in Modal; no copying its value locally
is needed. It sends a tiny synthetic prompt twice, verifies pinned served identity
and exact response, then verifies unauthenticated /v1/models returns 401.
It prints timings, UTC session boundaries and token counts, never credentials or
generated content. First-call time includes network, queue and load, not just
model loading. Only use --confirmed-cold after independently confirming zero
containers. End-to-end tokens/sec is not server-only decode throughput. Any
failure stops with no fallback. Save the nonsecret JSON output with trial evidence.
The waiting CPU probe adds its own small compute cost to the measured session.

The optional local probe remains available as `python -m model.smoke URL`; it
requires PREFLIGHT_API_KEY in its environment and is never called by CI.

## 5. Stop, verify, redeploy

```
uv run --group hosting modal app list --env main
uv run --group hosting modal app stop --env main APP_ID
```

List apps, identify **fhir-preflight-model**, and replace APP_ID with that app's
ID only. Stop it and confirm no remaining containers in the dashboard. Observe
billing after its reporting delay and record actual usage/credit delta; token
counts do not establish cost. Stop is not cache deletion.

For deliberate cache cleanup, first stop the app, then review the dedicated
volume name before:

```
uv run --group hosting modal volume delete --env main fhir-preflight-qwen3-cache
```

This deletes model cache evidence too; retain runtime/build records first.
Never delete other volumes or the shared secret. A deleted volume has an opaque
identity: recreating its name requires rerunning cache and deploy commands so the
app references the new volume. For ordinary redeployment with retained cache,
rerun deploy, smoke and stop. Record both cycles and actual billing before
claiming Step 3 complete. Do not start Step 4 without checkpoint approval.

## Public-demo boundary
Public demo explanations come from reviewed cached artifacts only. A public
cache miss must never send a generation request or wake the GPU. This policy
overrides earlier wording allowing public generation for new inputs; implementation
remains in Step 4 and the public-release change record.

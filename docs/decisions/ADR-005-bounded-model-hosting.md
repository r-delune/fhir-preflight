---
status: draft
drafted_by: Codex
---

# ADR-005 — A bounded, separately approved hosted-model trial

Date: 2026-11-19. Cloud trial authorized in chat on 2026-11-19; model adoption remains pending.

## Context and options
Step 3 needs a real open-weight model without local Ollama. Qwen3-8B's BF16
weights occupy about 15.3 GiB before runtime/cache overhead. T4's 16 GB is too
small for the unquantised baseline; A10 has comparable memory to L4 at a higher
published price. Quantisation or a smaller model would introduce another
behavioural change. L4's 24 GB is the smallest proposed fit, not a measured fit.

## Decision
Pin Qwen3-8B revision b968826d9c46dd6066d109eabc6255188de91218,
vLLM 0.21.0, Transformers 5.8.1 and the CUDA base digest in model/config.py.
Use one L4, 4096-token context, one concurrent input, eager execution, no
quantisation, min containers 0, max 1 and a 30-second scaledown window.
Cache on a dedicated volume using a CPU function before starting GPU inference.
Use region eu with routing eu-west; broad EU has a 1.15× compute multiplier
versus the narrower eu-west compute selection's 1.75× multiplier. Routing
selection is fixed on first deployment; changing it needs a new function.

PREFLIGHT_API_KEY comes from the existing fhir-test secret and maps to vLLM's
VLLM_API_KEY environment variable, never command-line text. Inference /v1 paths
require bearer authentication. Operational health/metrics paths may be public;
authentication does not prevent unauthenticated requests from waking compute.
This private trial is not the Step 7 public demo. Do not advertise its URL.
Brian authorized a $15 workspace spend limit and trial on 2026-11-19. Set and
verify that limit before any image build/cache/deploy or endpoint call. Keep any
existing stricter usage limit; do not raise it automatically.

## Consequences and open evidence
EU compute/routing is not a claim that all processing, storage or control-plane
traffic stays in the EU; large payload routing and platform services need separate
assessment before real inputs. Synthetic smoke requests only. No silent fallback:
OOM, missing cache, auth or model mismatch stops the trial for review.

A version-pinned pip installation still resolves transitive remote dependencies.
Record image/build ID and runtime versions after build before adoption. GPU fit,
cold/warm latency, teardown and actual billing remain unmeasured. The smoke
script reports end-to-end tokens/sec, not isolated decode throughput; first-call
latency is only called cold when zero containers were independently confirmed.
The app stays mock until Step 4. CR-003 tracks this hosting baseline; CR-001 and
CR-002 remain reserved for the public demo and model swap.

Sources checked 2026-11-19:
- https://modal.com/pricing
- https://modal.com/docs/guide/region-selection
- https://modal.com/docs/guide/budgets
- https://modal.com/docs/examples/vllm_inference
- https://huggingface.co/Qwen/Qwen3-8B

## Trial instruction update — 2026-11-19
Use the existing capped 4096-token context BF16 baseline rather than add FP8
quantisation as another variable. Cache weights with the CPU function only.
Measure independently confirmed cold first-request latency and warm latency,
and distinguish measured platform billing from resource-rate estimates. Public
demo explanations are cache-only, including cache misses (no GPU wake-up).

Budget revision before first job: Brian reported setup done and requested staying
within $1 current credit, adding a card later. This supersedes the earlier $15
request. Do not raise limits or incur card charges. Dashboard state is user
confirmed, not independently observed by automation. Stop on insufficient budget.

## ANOM-005 mitigation — separate CPU registration
The first CPU invocation failed after building images because Modal validates
all registered app functions, including unused L4 serving. CPU-only resource
selection on one function did not isolate that registration requirement.
Move caching to its own app in model/cache.py, sharing only configuration and
the image factory in model/runtime.py; never import the serving module there.
Reuse the existing pinned runtime image to avoid another dependency baseline
and repeat heavyweight build. A leaner download-only image is a future cost
optimisation, not required for registration isolation. Offline tests prove the
CPU app declares no GPU or serving import; remote verification is still pending.

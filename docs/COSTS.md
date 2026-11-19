---
status: draft
drafted_by: Codex
---

# Costs — Step 3 trial

Latest authorization: Brian confirmed “$15 limit saved” after adding the card.
This supersedes the earlier temporary $1 restriction. The saved control is
user-confirmed; browser automation did not independently observe it. The
separate CPU-only cache job completed successfully. The GPU deployment is
still rejected by Modal for a payment-method requirement. Measured CPU outcomes
follow below; no GPU/cold-start success is claimed.
Checked 2026-11-19 at https://modal.com/pricing and
https://modal.com/docs/guide/region-selection.

| Resource | Published USD rate | Proposed allocation |
|---|---|---|
| L4 GPU | $0.000222/sec | 1 |
| CPU | $0.0000131/core/sec | hard cap 2 physical cores |
| Memory | $0.00000222/GiB/sec | hard cap 16 GiB |
| Broad EU compute selection | 1.15× | applied to compute estimate |

Combined estimate: $0.000326278/sec, $1.1746008/hour, **$0.5873004 for
30 allocated minutes**. Startup, failed starts and the idle window consume time.
A 30-second idle tail is approximately $0.0098 at these allocations. CPU-only
cache download adds time at its CPU/memory rates (4 GiB, not 16 GiB).
Image builds, storage, transfers, taxes and billing granularity are additional;
this arithmetic is not a hard total spending guarantee.

Volume list price is $0.09/GiB/month (16 GiB ≈ $1.44/month before allowances).
The pricing page currently advertises up to 1 TiB free volume storage; verify
workspace entitlement and existing use. Network allowances also need verification.
A cache can persist after stopping an app. Scale-to-zero does not delete it.

Brian's screenshot showed only **$1 active credit**; the additional $29 required
a payment method. Do not assume access to all advertised monthly credits. We use
custom GPU compute, not Modal's separate managed per-token Model APIs.

## Authorization history — 2026-11-19

Brian instructed: “Proceed. Set a $15 Modal spending limit, download the weights
with a CPU-only job, use FP8 or a capped context length, measure the cold start
and the cost of the first session, and record them in COSTS.md. Public demo
explanations come from the cache only.” Brian then reported the billing setup done but revised the instruction: “we will
stay at 1 dollar for now and il add card details later”. The later instruction
controls: stay within $1 available credit, no card charges, no $15 limit increase.
No further permission is needed within this narrower scope. A workspace spend
limit caps net monthly charges after credits; usage before credits is a different
control. Do not raise an existing stricter usage limit automatically. https://modal.com/docs/guide/budgets

Chosen configuration: retain BF16 and cap total context at 4096 tokens, one
sequence/container, rather than introduce FP8 quantisation into the first
behavioural baseline. CPU-only snapshot job is already separate from GPU serving.
Public demo is strictly cache-only: cache misses never wake the GPU. New input
in future local/invite-only modes is a separate path, not a public-demo exception.

**Earlier access evidence (history):** CLI initially returned “Token missing”. Browser
control twice timed out. Brian completed the subsequently opened normal Modal
sign-in flow: CLI verified workspace r-delune and confirmed secret fhir-test
exists (names only; no secret value read). A 12-hour CLI credential was stored by
the SDK outside the repo. Baseline billing summary reports metered and billed
cost both $0 before any jobs. Brian confirmed the billing setup and $1 current-credit constraint in chat.
Dashboard settings were not independently observed by automation; CLI billing
summary does not expose limits/remaining credits. CPU-only pinned cache job was
started under the narrower user-confirmed constraint; no $15 limit is claimed
saved. Stop if this constraint prevents completion rather than adding a card,
raising limits or switching GPU/model.

Measured allocation time, image build charges, first-call/warm latency,
authentication, cache size, teardown/redeployment and dashboard balance delta:
**GPU measurements pending platform payment-method recognition**. No monthly free-operation promise is made.

## First failed attempt — measured billing

Modal app ap-wdMl2woX43JTyuQvRdu3Qm built the base/runtime images, then failed
registration: “Please add a payment method to use L4 GPU functions.” The CPU
weight-download function and GPU inference never started (ANOM-005). Final
runtime image build reported 181.83 seconds; this is not model cold-start time.

| Platform observation | USD |
|---|---|
| Metered before attempt | 0 |
| Metered after failed attempt (workspace total; no other app observed) | 0.01037242 |
| Credits applied | 0.01000000 |
| Network egress allowance applied | 0.00037242 |
| Actual billed amount | 0 |
| App CPU row, hourly report | 0.00640981 |
| App Memory row, hourly report | 0.00027961 |
| App Network Egress row, hourly report | 0.00037242 |

The hourly resource rows and summary breakdown do not fully reconcile with the
summary total. Do not invent a per-image allocation or label the entire total
as GPU cost. The reported metered cost of the failed attempt is about 1.04 cents;
1 cent of credits was consumed after the egress allowance. Complete nonsecret
API evidence is in docs/examples/step-3/failed-cache-billing.json. These are
observed platform charges, not resource-rate estimates; final invoices can adjust.

Brian subsequently reported adding a card. The exact saved limit is awaiting
confirmation; retain the last $1 constraint and start no further cloud jobs until
confirmed. A card alone does not demonstrate any $15 or $1 spending cap. CPU
caching is now a separate app so registration does not validate GPU functions.
Cold-start, successful weight download and first inference-session cost remain
unmeasured; image-build duration must not be substituted for cold-start latency.

## Resumed trial — confirmed $15 limit
Brian answered “$15 limit saved” in the pending settings question. This is the
current approved cap and resolves the saved-limit information dependency.
Started model.cache::cache_weights after capturing baseline billing in the
gitignored .cache/step3-resume-billing-before.json. No limit increase or further
permission is required within this scope. Use the pinned BF16 model with a
4096-token context cap and one GPU; public-demo generation remains cache-only.

## Successful CPU cache; GPU deployment still blocked

Run ap-7BdmoCPCGt38E3yEGEjgO4 completed one CPU cache call successfully, with no
server requests, then stopped (19:18:11–19:19:52 Asia/Bangkok, 101 seconds total
app lifecycle). Download progress reported about 75 seconds for 14 files. Five
weight shards total **16,381,516,776 bytes (15.2565 GiB)**. The cache manifest
confirms model revision b968826d9c46dd6066d109eabc6255188de91218 and vLLM 0.21.0,
Transformers 5.8.1, torch 2.11.0, huggingface-hub 1.33.0. The CPU app reused the
already built runtime image; the NVIDIA-driver warning is expected on a CPU job.

| CPU-cache run resource row | Observed USD |
|---|---|
| CPU | 0.00267454 |
| Memory | 0.00090471 |
| Network egress | 0.00045390 |
| Reported per-app metered total | **0.00403315** |

These are observed app-attributed resource charges, not a rate estimate. The
report is a snapshot of the still-open 12:00–13:00 UTC hour, so it is preliminary.
Workspace summary after the attempt reported **$0.01082632 metered, $0 billed**,
with $0.01 credits and $0.00082632 network allowance. Its total and resource
breakdown do not fully reconcile; do not use the summary delta alone as the CPU
job's cost or claim a final invoice. Cached weights persist for the future trial.

GPU deployment ap-HyWWj3PeL8njqU58kvap84 was rejected at registration with the
same payment-method message even after Brian confirmed adding a card and a saved
$15 limit. Its stats show zero function calls/containers and zero server requests;
both listed apps are stopped with zero tasks. No inference was run. **Cold-start,
warm latency, tokens/sec, inference-session cost and redeployment test remain
unmeasured.** ANOM-005's CPU-isolation mitigation is verified; ANOM-006 tracks
the unresolved platform payment-method recognition. No GPU/model fallback or
limit increase was attempted. Evidence: docs/examples/step-3/cpu-cache-success-gpu-blocked.json.

A registration recheck at 12:30:57 UTC (about ten minutes later) returned the
same payment-method error. Final account snapshot: $0.01082632 metered,
$0E-8 billed, zero tasks across 3 listed apps. Cached weights remain;
no GPU session was started. The $15 cap is confirmed, not awaiting renewed
approval. The remaining dependency is the platform's payment-method recognition.

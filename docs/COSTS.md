---
status: draft
drafted_by: Codex
---

# Costs — proposed Step 3 trial

Paid cloud expenditure incurred by Codex: $0. No model deployed or measured.
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

## Authorized trial — 2026-11-19

Brian instructed: “Proceed. Set a $15 Modal spending limit, download the weights
with a CPU-only job, use FP8 or a capped context length, measure the cold start
and the cost of the first session, and record them in COSTS.md. Public demo
explanations come from the cache only.” This supersedes the earlier proposed
$1 credit-only authorization gate; no further cost permission is needed within
this scope. The $15 workspace **spend limit** caps net monthly charges after
credits; usage before credits is a different control. Do not raise an existing
stricter usage limit automatically. https://modal.com/docs/guide/budgets

Chosen configuration: retain BF16 and cap total context at 4096 tokens, one
sequence/container, rather than introduce FP8 quantisation into the first
behavioural baseline. CPU-only snapshot job is already separate from GPU serving.
Public demo is strictly cache-only: cache misses never wake the GPU. New input
in future local/invite-only modes is a separate path, not a public-demo exception.

**Current access evidence:** CLI initially returned “Token missing”. Browser
control twice timed out. Brian completed the subsequently opened normal Modal
sign-in flow: CLI verified workspace r-delune and confirmed secret fhir-test
exists (names only; no secret value read). A 12-hour CLI credential was stored by
the SDK outside the repo. Baseline billing summary reports metered and billed
cost both $0 before any jobs. Saved $15 limit and remaining credit are still
awaiting dashboard verification; billing summary does not expose those settings.
No cloud job starts until the saved limit is verified.

Measured allocation time, image build charges, first-call/warm latency,
authentication, cache size, teardown/redeployment and dashboard balance delta:
**pending approved trial**. No monthly free-operation promise is made.

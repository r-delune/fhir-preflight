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

Before chargeable operations, review workspace Usage & Billing Settings:
set a $1 usage budget and $0 out-of-pocket spend limit if supported, verify saved
settings and their scope, then approve the trial in chat. Usage budget counts
before credits; spend limit counts after credits. Environment budgets require
higher plans; no plan upgrade is proposed. If a desired control is unavailable,
stop and review an alternative. https://modal.com/docs/guide/budgets

Measured allocation time, image build charges, first-call/warm latency,
authentication, cache size, teardown/redeployment and dashboard balance delta:
**pending approved trial**. No monthly free-operation promise is made.

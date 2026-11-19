---
status: draft
drafted_by: Codex
---

# CR-003 — Proposed Step 3 hosted model baseline

Trigger: Brian authorized Step 3 preparation in chat on 2026-11-19. Brian subsequently authorized the trial with a $15 workspace spend limit in chat.
Set and verify the limit before provisioning; model adoption remains a checkpoint.

Change: add optional Modal SDK, deployment definition, pinned model identity,
manual smoke probe, runbook, cost estimate and REQ-17. See ADR-005.
No workbench model integration or validator changes.

Impact: new cloud costs, endpoint credentials, platform/data-transfer boundary,
persistent model cache, unauthenticated wake-up costs, cold starts and potential
GPU memory failure. Controls: synthetic inputs, one container, scale to zero,
explicit budget review, private bearer key, no redirects/fallback, recorded pins.

Regression: offline tests only; results recorded in BUILD_JOURNAL.md. Remote
image build, transitive resolution, GPU allocation, authentication, latency,
shutdown/redeployment and billing verification remain pending. No deployment
success or model adoption is claimed.

Release: none. Rollback: keep app on mock; stop the named Modal app, verify zero
containers, then optionally remove only its dedicated cache after review. Preserve
pins and evidence for redeployment. Stop immediately on failed identity/auth or
out-of-memory; do not upgrade GPU or change model automatically.

Trial refinement: a CLI-only CPU probe reads the endpoint token from the existing
Modal secret and calls the deployed HTTPS inference API. No secret copying to
chat/local files is required. Record this CPU waiting time in session cost. Local
tests verify the probe itself requests no GPU and remains outside app/CI paths.

Budget amendment before first job: Brian confirmed billing setup and directed
staying at $1 current credit, with card details later. This overrides the earlier
$15 instruction. No limit increase/card charge is authorized; stop if credit is
insufficient. First CPU cache invocation is within this narrower trial.

ANOM-005: initial registration failed after paid image-build work because the
cache and L4 functions shared an app. Measured metered/billed amounts are in
COSTS.md and the nonsecret billing artifact. Split cache registration into a
CPU-only app without changing model/image/runtime versions or adding dependencies.
Tests explicitly block serving-module imports from that app. Reuse cached image
layers. Card addition is user-reported; saved spending limit still pending.

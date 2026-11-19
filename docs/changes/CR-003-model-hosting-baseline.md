---
status: draft
drafted_by: Codex
---

# CR-003 — Proposed Step 3 hosted model baseline

Trigger: Brian authorized Step 3 preparation in chat on 2026-11-19. Paid cloud
provisioning is a separate pending decision under AGENTS.md.

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

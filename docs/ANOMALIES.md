---
status: draft
drafted_by: Codex
---

# Anomaly log

| ID | Date | Observed / expected | Versions | Impact | Resolution / verification | Status |
|---|---|---|---|---|---|---|
| ANOM-001 | 2026-11-19 | TestClient emits httpx deprecation warning; expected warning-free checks | FastAPI 0.165.0 / Starlette 1.10.0 / httpx 0.28.1 | Tests pass; future compatibility to assess | Review supported transport before changing test dependencies | Open |
| ANOM-002 | 2026-11-19 | Initially labelled valid fixture failed: Observation.category and VSCat slice missing | CLI 6.10.4 / core 4.0.1 | Bad baseline could undermine fixture regression | Added vital-signs category to all fixtures; retained validator rules; actual regression now pass/fail/fail | Resolved |
| ANOM-003 | 2026-11-19 | Initial Compose app port 8000 conflicted with existing Python server; validator internal-network port not published | Docker Desktop 28.4.0 | CLI could not reach service | Use app port 8002, proxy to isolated validator, no validator host port; CLI regression passed | Resolved |
| ANOM-004 | 2026-11-19 | Browser controller repeatedly timed out, including one long native-app call | CUA browser/native tooling | Desktop evidence gap narrowed; mobile layout and saved screenshot still unverified | Brian reports reviewer-observed Chrome QA performed by Claude around 14:35 Asia/Bangkok: validation ran, pipeline reached Findings, selection highlighted lines 33–41, nested summary visible, /docs 404. Not independently rerun by Codex; no screenshot supplied. See docs/examples/step-3/reviewer-reported-step-2-qa.json | Partially resolved — desktop reviewer-reported; mobile/screenshot open |
| ANOM-005 | 2026-11-19 | CPU cache invocation built images but app registration failed because the same app declared an L4 function requiring a payment method | Modal SDK 1.6.4; vLLM 0.21.0; CUDA image pinned in config | CPU weight download and GPU inference never started; first attempt still consumed credits | Billing: $0.01037242 metered, $0 billed, $0.01000000 credits and $0.00037242 egress allowance. Per-image cost not exposed. Split CPU cache into model/cache.py with its own app; offline test rejects any serving-module import/GPU declaration. Card subsequently added per Brian; remote retry pending saved-limit confirmation. Evidence: docs/examples/step-3/failed-cache-billing.json | Open — mitigation tested locally; cloud retry pending |

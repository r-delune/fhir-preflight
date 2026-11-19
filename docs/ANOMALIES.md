# Anomaly log

| ID | Date | Observed / expected | Versions | Impact | Resolution / verification | Status |
|---|---|---|---|---|---|---|
| ANOM-001 | 2026-11-19 | TestClient emits httpx deprecation warning; expected warning-free checks | FastAPI 0.165.0 / Starlette 1.10.0 / httpx 0.28.1 | Tests pass; future compatibility to assess | Review supported transport before changing test dependencies | Open |
| ANOM-002 | 2026-11-19 | Initially labelled valid fixture failed: Observation.category and VSCat slice missing | CLI 6.10.4 / core 4.0.1 | Bad baseline could undermine fixture regression | Added vital-signs category to all fixtures; retained validator rules; actual regression now pass/fail/fail | Resolved |
| ANOM-003 | 2026-11-19 | Initial Compose app port 8000 conflicted with existing Python server; validator internal-network port not published | Docker Desktop 28.4.0 | CLI could not reach service | Use app port 8002, proxy to isolated validator, no validator host port; CLI regression passed | Resolved |

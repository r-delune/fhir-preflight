# Anomaly log

| ID | Date | Observed / expected | Versions | Impact | Resolution / verification | Status |
|---|---|---|---|---|---|---|
| ANOM-001 | 2026-11-19 | TestClient emits httpx deprecation warning; expected warning-free checks | FastAPI 0.165.0 / Starlette 1.10.0 / httpx 0.28.1 | Tests pass; future compatibility to assess | Review supported transport before changing test dependencies | Open |

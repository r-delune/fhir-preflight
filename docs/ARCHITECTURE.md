# Architecture

## Implemented at Step 0
Browser → local FastAPI hello page. Mock adapter only; no validation, persistence or model inference.

## Planned target
Browser → web app → validator (determines result).
Web app → authenticated model adapter → Modal-hosted vLLM → Qwen3-8B (explains issues).
The app and validator run locally during development; model inference is remote.
Step 7 adds public app hosting. Tests and CI keep the mock adapter and make no model calls.

Brian confirmed hosted inference on 2026-11-19; see decisions/ADR-001-hosted-model.md.
Validator packaging, region, GPU and exact model revision remain implementation work.

# Architecture

## Step 1 implementation
Browser → local FastAPI hello page (no results UI yet).
CLI → app /api/validate (127.0.0.1:8002) → isolated Python HTTP wrapper → pinned HL7 Java validator → original OperationOutcome.
Compose connects app and validator on an internal-only network. The app also has a bridge network for its laptop-only published port; the validator has no host port and no external network.
The app proxies validator responses unchanged; there is no results UI, AI inference or persistence yet.
See decisions/ADR-002-validator-service.md for packaging, severity policy and limits.

## Planned target
Browser → web app → validator (determines result).
Web app → authenticated model adapter → Modal-hosted vLLM → Qwen3-8B (explains issues).
The app and validator run locally during development; model inference is remote.
Step 7 adds public app hosting. Tests and CI keep the mock adapter and make no model calls.

Brian confirmed hosted inference on 2026-11-19; see decisions/ADR-001-hosted-model.md.
Validator packaging, region, GPU and exact model revision remain implementation work.

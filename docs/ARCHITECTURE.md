# Architecture

## Step 1 implementation
Browser → local FastAPI hello page (no results UI yet).
CLI → local Python HTTP wrapper → pinned HL7 Java validator → original OperationOutcome.
Compose connects app and validator on an internal-only network and binds ports to 127.0.0.1.
The app's validator URL is configured for Step 2; there is no AI inference or persistence yet.
See decisions/ADR-002-validator-service.md for packaging, severity policy and limits.

## Planned target
Browser → web app → validator (determines result).
Web app → authenticated model adapter → Modal-hosted vLLM → Qwen3-8B (explains issues).
The app and validator run locally during development; model inference is remote.
Step 7 adds public app hosting. Tests and CI keep the mock adapter and make no model calls.

Brian confirmed hosted inference on 2026-11-19; see decisions/ADR-001-hosted-model.md.
Validator packaging, region, GPU and exact model revision remain implementation work.

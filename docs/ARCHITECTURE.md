# Architecture

## Step 2 implementation
Browser → server-rendered Jinja workbench → selected synthetic fixture → real validator request.
CLI → app /api/validate (127.0.0.1:8002) → isolated Python HTTP wrapper → pinned HL7 Java validator → original OperationOutcome.
Compose connects app and validator on an internal-only network. The app also has a bridge network for its laptop-only published port; the validator has no host port and no external network.
The CLI API proxies validator responses unchanged. The workbench decorates findings with stable IDs and conservative JSON line mappings, preserving the validator result. Local CSS/JavaScript supports selection and progress; no AI inference or persistence yet. See ADR-003 for presentation limits.
See decisions/ADR-002-validator-service.md for packaging, severity policy and limits.

## Planned target
Browser → web app → validator (determines result).
Web app → authenticated model adapter → Modal-hosted vLLM → Qwen3-8B (explains issues).
The app and validator run locally during development; model inference is remote.
Step 7 adds public app hosting. Tests and CI keep the mock adapter and make no model calls.

Brian confirmed hosted inference on 2026-11-19; see decisions/ADR-001-hosted-model.md.
Validator packaging, region, GPU and exact model revision remain implementation work.

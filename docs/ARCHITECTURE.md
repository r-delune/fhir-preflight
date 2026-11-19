---
status: draft
drafted_by: Codex
---

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

## Step 2 governance extension

Browser → /governance?doc=<fixed-id> → literal catalog path → source metadata/provenance → HTML-disabled Markdown renderer → read-only page. No URL value is passed to open() as a path. The image contains copied sources and a build hash manifest, not .git. Headers prohibit scripts and active images on governance pages. /docs, /redoc and /openapi.json have no route by default; an exact ENABLE_API_DOCS=1 opts in. Findings retain raw text/IDs; nested message excerpts and plain UI guidance are presentation only, not model output.

## Step 3 prepared boundary (not deployed)
The workbench remains on its mock adapter. `model/serve.py` defines a separate
Modal app: CPU cache download → dedicated pinned model volume → one scale-to-zero
L4 running vLLM. `model/config.py` holds the reviewed pins and resource limits;
`model/smoke.py` is an explicit manual client, never a test/CI network dependency.
Step 4 will add the application integration; no validator result passes through
this model service. See ADR-005 and the model-hosting runbook.

ANOM-005 refinement: model/cache.py is a distinct CPU-only Modal app; serving
remains in model/serve.py. They share model/config.py and the inert image factory
in model/runtime.py. This prevents CPU app registration from validating an unused
GPU function. No model/provider fallback or workbench integration was added.

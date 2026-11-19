---
status: draft
drafted_by: Codex
---

# ADR-001 — Hosted runtime model

Date: 2026-11-19. Decision source: Brian's explicit chat instruction. Implementation: scheduled for Step 3.

## Context
PLAN.md specifies learning to host an open-weight model. An earlier discussion suggested local Ollama, which left the Step 0 docs ambiguous.

## Options considered
Local model inference on the laptop; hosted open-weight inference through vLLM on Modal.

## Decision
Use the plan's hosted Qwen3-8B/vLLM/Modal architecture. Brian explicitly ruled out local Ollama. This selects an architecture; it does not authorize unverified costs or mean a deployment exists.

## Consequences
The development app and validator remain local, but selected synthetic data and excerpts go to the hosted inference service. Connectivity, authentication, cold starts and cloud costs must be handled and documented. CI and local automated tests use the mock adapter. Verify current licence, model revision, region support, GPU configuration and pricing before provisioning; provide a shutdown runbook and no silent fallback.

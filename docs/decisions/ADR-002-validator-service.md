---
status: draft
drafted_by: Codex
---

# ADR-002 — Pinned CLI inside a local validator service

Date: 2026-11-19. Scope: Step 1 implementation authorized by Brian in chat.

## Context
We need raw OperationOutcome output, one local profile, pinned FHIR R4 packages and disabled remote terminology. Existing laptop Java is 14; containers avoid modifying it.

## Options
1. Upstream validator-wrapper web/server image: ready-made server, but adds a Kotlin/web stack and its own API/version lifecycle.
2. Official HL7 validator_cli.jar launched as a subprocess behind a small Python development HTTP wrapper: fewer layers, explicit arguments, raw output; slower per-request startup.

## Decision
Use option 2 with CLI 6.10.4, the last listed patch before upstream's 7.0 internal R6 migration. This is a deliberate baseline, not a claim it is the newest or free of bugs. Pin the release JAR by SHA-256 and base images by digest. The wrapper only transports input, maps severity and reports infrastructure failure; HL7 performs all FHIR validation.

Sources: [core releases](https://github.com/hapifhir/org.hl7.fhir.core/releases), [upstream wrapper](https://github.com/hapifhir/org.hl7.fhir.validator-wrapper), [pinned option source](https://github.com/hapifhir/org.hl7.fhir.core/tree/6.10.4/org.hl7.fhir.validation.cli/src/main/java/org/hl7/fhir/validation/cli/picocli/options).

## Consequences
Bootstrap may access package registries during image build; request-time validation uses `-tx n/a`, `-no-http-access` and an internal-only Compose network. Caches are baked into the image. Pinning transient package dependencies and capturing cache hashes are part of baseline evidence. There is one active JVM at a time, a 2 GiB heap limit and 180-second timeout. This is a development service, not a production-hardened public endpoint.

Pass/fail policy (REQ-01): any error/fatal means fail; only warning/information means pass with documented limitations. Missing/malformed output, abnormal exit or timeout means incomplete, never pass. No AI is involved.

The subject resolution invariant is a local teaching constraint in our profile, not a claim that every unresolved reference violates base FHIR. No age or clinical interpretation is performed.

## Verified setup adjustment
Docker Desktop's internal network did not publish the validator port to the laptop. The validator remains on that network with no published port; CLI requests pass through the app's /api/validate route. Only the app gets a host-access bridge and laptop-only port 8002 (8000 was already occupied). This is transport, not a results UI or alternative validation engine.

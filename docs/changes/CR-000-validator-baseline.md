---
status: draft
drafted_by: Codex
---

# CR-000 — Initial local validator baseline

Date: 2026-11-19. Authorization: Brian approved Step 1 in chat. Status: local implementation verified; awaiting checkpoint review, not a release approval.

## Change and impact
Introduce official HL7 validator CLI 6.10.4, FHIR R4 core 4.0.1 and custom profile 0.1.0. No runtime model, prompt or excerpt changes. App landing text changes to Step 1; results UI is still deferred.

New failure modes: JVM startup/timeouts, missing packages, profile authoring mistakes, misunderstood terminology coverage and incorrect severity interpretation. Controls: pinned JAR checksum/images, bootstrap before runtime, raw OperationOutcome preservation, explicit incomplete state, mock process tests, real three-fixture regression and documented limitations. The custom resolvable-subject rule is explicitly distinguished from base FHIR requirements.

## Verification
Fast tests cover REQ-01 and REQ-11; actual fixture results are recorded under docs/examples/step-1 and in BUILD_JOURNAL.md. No AI calls in tests or regression. No public deployment.

## Release / rollback
This is a development checkpoint. If regression fails, do not advance to Step 2. Stop with `make stop`; the Step 0 commit `ed8666b` remains available as the previous code baseline. Preserve failed outcomes/anomalies for investigation. Model hosting remains Modal/vLLM/Qwen3-8B; no costs have been authorized or incurred for it.

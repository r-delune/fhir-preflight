---
status: draft
drafted_by: Codex
---

# Intended purpose

Status: Codex draft for Brian's review — 2026-11-19. Not yet approved.

FHIR Preflight helps software developers understand problems in synthetic FHIR R4 (4.0.1) health-data examples checked against a pinned profile. It presents validator findings, uses a hosted AI model to explain selected findings using supplied documentation, and lets a reviewer accept, edit or reject those explanations before exporting a report with provenance.

The validator determines the validation result. AI explanations cannot change it. The report records which checks ran and their limitations; passing those checks is not a guarantee of fitness for a clinical deployment.

The tool is for technical learning, demonstration and integration investigation. Inputs are fictional examples only. It does not connect to live EHR systems, interpret individual patients' clinical values, recommend care or automatically repair data.

During development the app and validator run on the laptop. Real model inference is planned on Modal using vLLM and Qwen3-8B; selected synthetic payload slices, issues and documentation are sent to that service. Tests use a deterministic mock. Public access is deferred to Step 7.

This statement defines product boundaries. Regulatory applicability conclusions are a separate reviewed assessment.

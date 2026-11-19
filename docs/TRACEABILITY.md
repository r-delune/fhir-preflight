---
status: draft
drafted_by: Codex
---

# Traceability — manual Step 2 baseline

REQ-01 through REQ-05 are working drafts; Brian authorized Steps 1–2 implementation in chat. No formal release approval is inferred.

| Requirement | Evidence now | Status / remaining work |
|---|---|---|
| REQ-01 | tests/test_validator.py; tests/test_validation_route.py; docs/examples/step-1/summary.json | CLI and workbench status/failure boundary verified locally |
| REQ-02 | tests/test_presentation.py injected model-claim case; architectural separation | Display boundary verified; actual model/review integration and full regression deferred to Steps 4–5 |
| REQ-03 | None yet | Step 4 |
| REQ-04 | None yet | Steps 4–5 |
| REQ-05 | Validator/profile/package provenance exists; no explanation yet | Model/explanation provenance deferred to Steps 4–5 |
| REQ-11 | tests/test_validator.py; real offline fixture outcomes; compose.yaml isolated validator network | Verified for Step 1 baseline |
| REQ-12 | tests/test_presentation.py; docs/examples/step-2/http-smoke.json | Stable semantic IDs verified locally |
| REQ-13 | tests/test_presentation.py; tests/frontend.test.cjs | Mapping and event logic verified; final browser click/mobile QA pending tooling recovery |
| REQ-14 | tests/test_presentation.py; tests/frontend.test.cjs | Fixture switching, result clearing, progress and incomplete-state logic verified |
| REQ-15 | tests/test_workflow_guidance.py; tests/frontend.test.cjs | Pipeline, severity/result explanations, governance links and verbatim nested message excerpts verified locally |
| REQ-16 | tests/test_governance.py; scripts/prepare_build_metadata.py | Allowlist, traversal/symlink rejection, Markdown safety, status/authorship, git/build hashes, read-only routes and default-off API docs verified; container smoke evidence recorded in journal |

Scaffold tests verify infrastructure only. The traceability generator is scheduled for Step 6. Hosted CI has no recorded runs when last checked; local results are recorded in the journal.

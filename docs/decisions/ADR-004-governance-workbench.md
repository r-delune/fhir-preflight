---
status: draft
drafted_by: Codex
---

# ADR-004 — Explain the workflow and expose repository governance read-only

Date: 2026-11-19. Status: Codex draft for Brian's review. Source: Brian explicitly requested REQ-15/REQ-16 before the Step 2 checkpoint.

## Context and alternatives
The results screen needs to explain its own limits and let the reviewer inspect the evidence behind its controls. Copying document text into templates would create a second source of truth. A generic filesystem browser would expose files beyond the intended governance set. Inferring approval from wording, a git commit, or permission to build would misrepresent review status.

## Decision
Add a short pipeline strip and plain-language result/severity guidance (REQ-15). Current stage is Example before a run, HL7 validator while submitting, and Findings after a completed result; incomplete runs point back to validation. AI explanation, human review and report remain visibly unavailable. Link REQ-02, ADR-002 and CR-000 to the relevant source documents.

The /governance page accepts only opaque document IDs in a fixed catalog. Each maps to one literal path; unknown IDs and symlink substitutions are rejected. Tests require every ADR, change record and regulatory Markdown draft to be deliberately cataloged. No route writes files. Swagger /docs, ReDoc /redoc and /openapi.json are disabled by default; only ENABLE_API_DOCS=1 enables them. Governance is served separately at /governance.

Read Markdown bytes from the repository (or their build-time copy in Docker). Render with pinned markdown-it-py, raw HTML disabled, active images disabled and link navigation restricted to HTTPS sources, safe fragments and cataloged documents. Local source/code paths outside the catalog become non-navigable rather than being served. Tables and safe generated anchors preserve requirement references. No separate copies of document prose live in templates.

Store flat front-matter metadata (`status`, `drafted_by`, optional `approved_by` and `approved_on`) in each source file. Existing documents remain draft unless explicit approval metadata is present; missing authorship is labelled unrecorded, not guessed. Approved status requires both approver and date. Metadata does not imply legal sign-off or release approval.

Git provenance compares displayed file bytes against HEAD locally. Docker copies docs and top-level Markdown but not .git; a generated build manifest records HEAD, per-document hashes and whether each file matched that commit. The browser verifies those hashes and clearly labels working-copy, modified-since-build or unavailable provenance. A dirty build must never claim its document text came from a clean commit.

## Consequences and verification
A new ADR/change/regulatory file requires a catalog addition and metadata. `make dev` generates the source manifest before building; a build without that manifest fails instead of inventing provenance. Direct repository edits are visible on the next local request; Docker requires rebuilding to update its snapshot. No hosted model, validator version, prompt or corpus change is made. Verify traversal/encoded paths/symlinks, active-content escaping, author/status presentation, exact/dirty git provenance, all required links and actual container routes. Final browser QA gaps remain explicit.

## Follow-up instruction from Brian
Serve repository documents at `/governance`. FastAPI schema/documentation endpoints return 404 unless `ENABLE_API_DOCS=1`; this keeps the default product surface focused and leaves development documentation an explicit option. Link “Build step 2 of 8” to the governance roadmap. Each finding identifies original HL7 wording and notes that AI explanation is planned for Step 4. Nested `message=...` text may be extracted for readability, but no wording may be invented and the original raw text remains available. These are Step 2 presentation requirements, not AI generation.

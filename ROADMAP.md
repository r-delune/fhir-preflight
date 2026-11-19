---
status: draft
drafted_by: Source template (author unverified); Codex updates
---

# Roadmap — FHIR Preflight

Codex updates this table at every checkpoint (status, date, link to the journal entry). Brian approves in chat or the journal; Codex records the source.
Details for each step are in `PLAN.md` §3. The full story is in `BUILD_JOURNAL.md`.

Status key: ⬜ not started · 🔨 in progress · ⏸ waiting for Brian · ✅ approved

| Step | What | Status | Started | Checkpoint | Journal | Approved |
|---|---|---|---|---|---|---|
| 0 | Skeleton, rules, CI, intended purpose, first requirements | ✅ progression approved in chat; hosted CI pending | 2026-11-19 | 2026-11-19 | [Entry #0](BUILD_JOURNAL.md#step-0) | ☐ |
| 1 | FHIR fixtures, our profile, validator running locally | ✅ progression approved in chat | 2026-11-19 | 2026-11-19 | [Entry #1](BUILD_JOURNAL.md#step-1) | ☐ |
| 2 | Results UI, pipeline guidance and read-only governance docs (REQ-15/REQ-16) | ⏸ checkpoint review; visual QA gap recorded | 2026-11-19 | 2026-11-19 | [Entry #2](BUILD_JOURNAL.md#step-2) | ☐ |
| 3 | Host the model on Modal (Codex prepares and explains) | ⬜ | | | | ☐ |
| 4 | AI explanations, citation checks, red-team | ⬜ | | | | ☐ |
| 5 | Review, export, activity log | ⬜ | | | | ☐ |
| 6 | Release v0.1 + reviewed AI Act / MDR drafts | ⬜ | | | | ☐ |
| 7 | Public demo on Fly.io (change request CR-001) | ⬜ | | | | ☐ |
| 8 | Model swap exercise (CR-002), release v0.2 | ⬜ | | | | ☐ |

## Now
- **Current step:** 2 — REQ-15/REQ-16 implemented and verified by automated and live-container checks; final visual/mobile evidence still pending
- **Waiting on Brian:** review the workbench and /governance pages, ask questions or request edits. Step 3 deployment is not underway; the Modal key is not needed for Step 2.
- **Open anomalies:** 2 (see `docs/ANOMALIES.md`)
- **Spend this month:** €0 (see `docs/COSTS.md`)

## Parked ideas
Things that came up but are out of scope for now. Add here instead of building them.

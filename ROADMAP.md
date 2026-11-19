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
| 2 | Results UI, pipeline guidance and read-only governance docs (REQ-15/REQ-16) | ✅ progression approved in chat; visual QA gap recorded | 2026-11-19 | 2026-11-19 | [Entry #2](BUILD_JOURNAL.md#step-2) | ☐ |
| 3 | Host the model on Modal (Codex prepares and explains) | 🔨 prepared locally; initial cache failed; isolated CPU app tested; publishing CI | 2026-11-19 | | [Step 3](BUILD_JOURNAL.md#step-3) | ☐ |
| 4 | AI explanations, citation checks, red-team | ⬜ | | | | ☐ |
| 5 | Review, export, activity log | ⬜ | | | | ☐ |
| 6 | Release v0.1 + reviewed AI Act / MDR drafts | ⬜ | | | | ☐ |
| 7 | Public demo on Fly.io (change request CR-001) | ⬜ | | | | ☐ |
| 8 | Model swap exercise (CR-002), release v0.2 | ⬜ | | | | ☐ |

## Now
- **Current step:** 3 — deployment code, pinned model/runtime and cost/runbook preparation; Step 2 desktop QA reviewer-reported; mobile/screenshot pending
- **Waiting on Brian:** confirm the saved spend limit after adding the card; retain last $1 constraint until known. No new cloud jobs while that control is unverified.
- **Open anomalies:** 3 (see `docs/ANOMALIES.md`)
- **Spend this month:** €0 (see `docs/COSTS.md`)

## Parked ideas
Things that came up but are out of scope for now. Add here instead of building them.

## Queued after the Step 3 checkpoint — planning review first
Brian requested a single fictional home blood-pressure integration use case,
visible/selectable target profiles, design-input UN → REQ traceability, a guided
cache-first demo and partner evidence reports. See the pending-direction entry
in BUILD_JOURNAL.md for the full constraints. After Step 3 is finished and
checkpointed, draft a PLAN.md section plus draft UN/REQ IDs, then stop for review
before implementation. The profile replacement must precede Step 4 (proposed
CR-004); local/invite-only uploads are planned alongside Step 7 as their own
change (proposed CR-005). Recheck numbering before creating either record.
No product changes or new profile are authorized for implementation yet.

Public-demo refinement (Brian, 2026-11-19): explanations are cache-only, including misses; no public request may wake the GPU. Carry this into the post-Step-3 product-plan draft.

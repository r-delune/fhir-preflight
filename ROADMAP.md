# Roadmap — FHIR Preflight

Codex updates this table at every checkpoint (status, date, link to the journal entry). Brian approves in chat or the journal; Codex records the source.
Details for each step are in `PLAN.md` §3. The full story is in `BUILD_JOURNAL.md`.

Status key: ⬜ not started · 🔨 in progress · ⏸ waiting for Brian · ✅ approved

| Step | What | Status | Started | Checkpoint | Journal | Approved |
|---|---|---|---|---|---|---|
| 0 | Skeleton, rules, CI, intended purpose, first requirements | ✅ progression approved in chat; hosted CI pending | 2026-11-19 | 2026-11-19 | [Entry #0](BUILD_JOURNAL.md#step-0) | ☐ |
| 1 | FHIR fixtures, our profile, validator running locally | ⏸ waiting for review | 2026-11-19 | 2026-11-19 | [Entry #1](BUILD_JOURNAL.md#step-1) | ☐ |
| 2 | Results UI (issues linked to JSON locations) | ⬜ | | | | ☐ |
| 3 | Host the model on Modal (Codex prepares and explains) | ⬜ | | | | ☐ |
| 4 | AI explanations, citation checks, red-team | ⬜ | | | | ☐ |
| 5 | Review, export, activity log | ⬜ | | | | ☐ |
| 6 | Release v0.1 + reviewed AI Act / MDR drafts | ⬜ | | | | ☐ |
| 7 | Public demo on Fly.io (change request CR-001) | ⬜ | | | | ☐ |
| 8 | Model swap exercise (CR-002), release v0.2 | ⬜ | | | | ☐ |

## Now
- **Current step:** 1 — local implementation verified; real fixtures matched pass/fail/fail
- **Waiting on Brian:** review docs/examples/step-1/README.md, ask questions and approve Step 2 when ready. Hosted CI evidence remains pending.
- **Open anomalies:** 1 (see `docs/ANOMALIES.md`)
- **Spend this month:** €0 (see `docs/COSTS.md`)

## Parked ideas
Things that came up but are out of scope for now. Add here instead of building them.

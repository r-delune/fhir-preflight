# ADR-003 — Browser results and conservative location mapping

Date: 2026-11-19. Brian authorized Step 2 with “start” in chat.

## Decision
Use server-rendered Jinja pages and small local CSS/JavaScript files for fixture selection, validator results and highlighting. No frontend framework, external assets or additional runtime component is needed for this step; HTMX remains deferred until needed. Results are fresh validator responses, not the saved regression snapshots. The validator, profile and package baseline remain unchanged.

Stable issue IDs (REQ-12) use a SHA-256 prefix over semantic issue fields, excluding volatile temp paths and line/column metadata. Identical duplicates share an ID but remain separate rows. This is a content identity, not a database row ID.

Location mapping (REQ-13) implements a deliberately small subset of the emitted path syntax: dot properties, numeric indices, resource comments, value[x] and ofType(Quantity)-style choices. It does not evaluate arbitrary FHIRPath. Missing fields highlight the nearest resolvable parent and say so; unsupported/unmatched expressions are clearly labelled. Raw validator paths remain visible.

## Consequences
The interface remains easy to inspect and runs without a CDN. New fixture selection clears findings; validator failure cannot retain an earlier pass label (REQ-01/REQ-14). Validation may take time, so submission shows a busy indicator. No AI explanation, review, caching or export is implemented at this checkpoint. The status is the validator service result; the UI cannot infer or override it.

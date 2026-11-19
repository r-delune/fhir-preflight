# Step 2 — browser workbench review

## What changed

The local workbench now has three panels: a read-only fictional FHIR example, the original validator findings, and a clearly marked future explanation/review area. There is no AI explanation or review persistence yet.

Choose an example and click **Run validation**. With JavaScript enabled, changing the dropdown immediately loads the new example and clears prior findings. The **Load example** button remains available as a fallback. Validation calls the actual local HL7 service; it does not replay the saved Step 1 results.

The outcome label comes from the validator service. The page shows error/warning/information counts, configured checks, disabled remote terminology and run provenance. A bad/unavailable service shows **Validation incomplete**, with no prior pass retained.

Each finding has a stable content-derived `VAL-…` reference. Selecting it is designed to highlight the matching JSON lines and show the original message in the right panel. If an exact field is missing or the path cannot be fully translated, the page explicitly labels the nearest-parent or unmapped fallback. This display helper does not evaluate arbitrary FHIRPath or validate the data itself.

## Real HTTP results

| Example | Outcome | Findings displayed | Comparison |
|---|---|---|---|
| Complete weight example | Pass (configured checks) | 6: 3 warnings, 3 information | All finding IDs matched Step 1 |
| Structural errors | Fail | 12: 6 errors, 3 warnings, 3 information | All finding IDs matched Step 1 |
| Profile & reference errors | Fail | 11: 5 errors, 3 warnings, 3 information | All finding IDs matched Step 1 |

See [HTTP smoke evidence](http-smoke.json). Counts are messages, not necessarily distinct defects.

## One finding explained without AI

In the profile/reference example, the unit code is `kg`, while our teaching profile fixes it to `g`. The validator rejects that mismatch. Kilograms are not generally invalid FHIR: they fail the particular grams-only rule we authored. The highlighted line should be the `code` field under `valueQuantity`, not the separate LOINC measurement code.

## Verification and open evidence

35 Python tests cover mapping, identity, escaping, fixture selection, status and service failures. Three Node tests execute the actual event-handler script against simulated DOM interfaces to check highlight/selection changes, loading a new fixture, and busy/back-navigation state. They are interaction-logic tests, not browser layout tests. Ruff passed.

The initial desktop screen was visually observed in Chrome via CUA, and a real browser validation POST returned HTTP 200. A screenshot of the initial desktop screen was emitted in the chat tooling, but no screenshot file was saved into the repo. The controller repeatedly timed out (one native call took over seven minutes). Final visual click-to-highlight confirmation and narrow/mobile layout checks therefore remain **pending** (ANOM-004). Do not infer those from the simulated-DOM tests. CSS includes smaller-screen layouts, but these have not been visually verified.

## Your review

Open http://127.0.0.1:8002. Select **Profile & reference errors**, run validation, then select the finding about `kg` being fixed to `g`. The JSON unit-code line should highlight and the right panel should show the selected message. Then try another example and confirm the old result clears. This review is optional hands-on learning; questions and requested edits are welcome.

`make dev` starts the services; `make stop` stops them. No account setup or paid service is involved. The next planned step is preparing the hosted model, which needs a separate cost/deployment checkpoint.

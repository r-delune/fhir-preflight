# Requirements

Status: first five drafted by Codex for Brian's review — 2026-11-19. Not yet approved.
IDs preserve the meanings proposed in PLAN.md. Product features and their verification are future work; Step 0 scaffold tests do not prove these requirements.

| ID | Required behaviour | Verification criterion | Planned implementation |
|---|---|---|---|
| REQ-01 | Validation status is determined only from validator results under the documented severity policy. An unavailable or failed validator produces a visible failure/incomplete state. | Exercise clean, warning, error and service-failure results; verify the documented mapping and no pass on failure. | Steps 1–2 |
| REQ-02 | Model output and explanation review decisions cannot change the stored validator result or displayed validation status. | Inject an explanation claiming an invalid payload is valid; accept, edit and reject it; confirm validation data/status are unchanged. | Steps 4–5 |
| REQ-03 | An explanation with any citation ID outside the excerpt set actually sent is flagged unsupported and cannot be presented as verified. An explanation without a valid citation is unverified. Valid IDs alone do not prove the explanation is supported. | Test unknown IDs, mixed valid/invalid IDs, no citations and valid IDs; verify labels and prevent an unsupported explanation becoming verified through acceptance alone. | Step 4 |
| REQ-04 | Every AI-generated explanation is visibly labelled in the interface and export, including reviewer-edited text derived from it. | Check UI and Markdown/JSON exports for accepted, edited, rejected and cached explanations; preserve generation origin and review state. | Steps 4–5 |
| REQ-05 | Each explanation records model ID and immutable revision, prompt version and excerpt-set version at generation; cached outputs preserve original provenance. | Generate with mock metadata, change configuration, retrieve original and cached outputs and verify original metadata is retained in storage and export. | Steps 4–5 |
| REQ-11 | Remote terminology is disabled by default. Validation requests cannot fetch remote resources or dependencies; bootstrap downloads occur before runtime. | Check `-tx n/a` and `-no-http-access` in the command, run all fixtures on an internal-only Docker network, and inspect the resulting limitations. | Step 1 baseline |

REQ-06 through REQ-10 remain proposals in PLAN.md until added for implementation. Tests will carry REQ IDs when the corresponding behaviour exists.

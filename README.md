# FHIR Preflight

Step 2: browser workbench for three synthetic FHIR examples, with real HL7 validation and clickable finding locations. AI explanations and review are future steps.

## Run locally

From this directory run `make setup`, then `make dev` (Docker Desktop running).
Open http://127.0.0.1:8002 for the workbench. Choose an example, run validation, then select a finding to highlight its JSON location. First setup downloads the pinned
validator and FHIR packages; allow time for the image build.

```sh
make validate
python3.12 scripts/validate.py fhir/fixtures/broken-structure.json
python3.12 scripts/validate.py fhir/fixtures/broken-profile-and-reference.json
make stop
```

The browser shows errors, warnings, information and enabled-check limitations. The CLI still prints original OperationOutcome JSON.
Exit codes: 0 pass under configured checks, 1 validation errors, 2 incomplete.
`make test` uses simulated validator process responses and the mock model;
`make regression` checks the three fixtures with the real local validator.
`make test` also runs three frontend interaction-logic checks with Node.js 22.22.1 (no npm dependencies). `make lint` checks Python style. No AI model, API key or cloud account is needed.
See [the explained runbook](docs/runbooks/local-validator.md) for details and limitations.

## How we work

Codex drafts, implements and explains. Brian reviews the work and asks questions.
Purpose and the first five requirements are drafted for review in docs/INTENDED_PURPOSE.md
and docs/REQUIREMENTS.md. BUILD_JOURNAL.md records changes and evidence.
Brian approved Steps 1 and 2 in chat. Each subsequent step waits for review; homework is optional.

## Where the AI runs

Planned runtime AI: Qwen3-8B served by vLLM on Modal. The development app and validator
run locally; actual AI requests go to the hosted endpoint after Step 3. Local Ollama is
not part of the project. Only the mock model adapter exists so far; no model is deployed.
Hosting costs and configuration will be verified before provisioning.

GitHub remote: https://github.com/r-delune/fhir-preflight. Actions is configured; no hosted workflow runs were returned when checked during Step 1. Local checks are recorded separately.

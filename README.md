# FHIR Preflight

Step 0 scaffold. Synthetic examples only; validation and AI explanations are not connected yet.

## Run locally

From this directory, run `make setup`, then `make dev`. Open http://127.0.0.1:8000.
The page should say Step 0 and that no validator or AI model is connected.
`make test` runs the mock-only scaffold checks; `make lint` checks Python style.
Python 3.12 and uv are required. No API key, Docker or cloud account is needed at this step.
The development server listens only on your laptop. Stop it with Ctrl+C.

## How we work

Codex drafts, implements and explains. Brian reviews the work and asks questions.
Purpose and the first five requirements are drafted for review in docs/INTENDED_PURPOSE.md
and docs/REQUIREMENTS.md. BUILD_JOURNAL.md records changes and evidence.
Step 1 waits for Brian's approval in chat or the journal; homework is optional.

## Where the AI runs

Planned runtime AI: Qwen3-8B served by vLLM on Modal. The development app and validator
run locally; actual AI requests go to the hosted endpoint after Step 3. Local Ollama is
not part of the project. At Step 0 only the mock adapter exists; no model is deployed.
Hosting costs and configuration will be verified before provisioning.

GitHub Actions is configured but has not run: this repository has no remote.

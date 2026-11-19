# FHIR Preflight

Step 0 scaffold. Synthetic examples only; validation and AI explanations are not connected yet.

## Run locally

From this directory, run `make setup`, then `make dev`. Open http://127.0.0.1:8000.
The page should say Step 0 and that no validator or AI model is connected.
`make test` runs the mock-only scaffold checks; `make lint` checks Python style.
Python 3.12 and uv are required. No API key, Docker or cloud account is needed at this step.
The development server listens only on your laptop. Stop it with Ctrl+C.

Read PLAN.md and AGENTS.md. Brian's Step 0 work belongs in docs/INTENDED_PURPOSE.md,
docs/REQUIREMENTS.md and BUILD_JOURNAL.md. Step 1 waits for journal approval.
GitHub Actions is configured but has not run: this repository has no remote.

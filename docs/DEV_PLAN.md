# Development plan — Step 0

Use a 62304-inspired lifecycle; no compliance claim. PLAN.md defines the ordered steps.
Codex drafts and implements each step, records evidence, and explains the work.
Brian learns by reviewing and asking questions; personal homework is optional.
Brian approves progression in chat or the journal. Codex drafts regulatory assessments
for review without representing them as Brian's adopted conclusions.

The runtime model is Qwen3-8B served through vLLM on Modal (Brian confirmed).
The app and validator run locally in development; the model is hosted remotely.
Tests/CI use a mock. No local Ollama integration is planned. Region, pricing,
GPU and exact revisions must be verified before Step 3 provisioning.
No hosting or paid service is provisioned yet.

Configuration items: application code, fixtures, profiles, validator, dependency lockfile,
model revision, prompts, excerpt set, reports and lifecycle records. Later steps will
add change records for model/prompt/excerpt/validator/hosting changes and regression evidence.

Tools: Python 3.12, uv, Git, pytest, Ruff and GitHub Actions; Codex assists development.
Codex is a development tool, not the runtime model. Review its changes and check outputs.
Log problems in ANOMALIES.md; link the change, control and verification when resolved.
Do not store secrets or real patient data. Local checks and CI use only the mock adapter.

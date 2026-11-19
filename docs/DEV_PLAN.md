# Development plan — Step 0

Use a 62304-inspired lifecycle; no compliance claim. PLAN.md defines the ordered steps.
Brian owns intended purpose, initial requirements, learning answers and regulatory conclusions.
Codex implements one step and records checks and decisions. Brian approves in the journal
before the next step. Model hosting remains unresolved: PLAN.md proposes Modal whereas
the preceding discussion proposed local Ollama. No hosting or paid service is provisioned.

Configuration items: application code, fixtures, profiles, validator, dependency lockfile,
model revision, prompts, excerpt set, reports and lifecycle records. Later steps will
add change records for model/prompt/excerpt/validator/hosting changes and regression evidence.

Tools: Python 3.12, uv, Git, pytest, Ruff and GitHub Actions; Codex assists development.
Codex is a development tool, not the runtime model. Review its changes and check outputs.
Log problems in ANOMALIES.md; link the change, control and verification when resolved.
Do not store secrets or real patient data. Local checks and CI use only the mock adapter.

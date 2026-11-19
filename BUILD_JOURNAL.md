# Build Journal

The development record for FHIR Preflight: what we did, why, how we checked it, what went wrong, what Brian learned. Codex appends an entry at every checkpoint; Brian fills in his sections and approves.

Newest entries at the bottom.

---

## Entry template

### #N — Step X: <title> — YYYY-MM-DD

**Goal:** what we wanted

**What changed** (Codex): files, commits/branch

**Why:** links to REQ-xx / ADR-xxx

**How we checked it:** commands run, tests, results

**What went wrong / surprises:**

**Decisions Codex made without asking:**

**Cost incurred this step:** (€0 if none)

**Brian — prediction (before running):**

**Brian — what actually happened and what I learned (own words):**

**Brian — explain-back answers:**

**Evidence:** links to tests, screenshots, docs

**Status:** ☐ approved by Brian — next step may start

---

<a id="step-0"></a>
### #0 — Step 0: Skeleton and rules — 2026-11-19

**Goal:** establish a runnable local skeleton, repeatable checks and learning records before FHIR or AI integration.

**What changed** (Codex): branch `codex/step-0-skeleton`; app/main.py, app/templates/index.html, mock adapter, tests/test_scaffold.py, pyproject.toml, uv.lock, Makefile, .github/workflows/ci.yml, README.md, .env.example, .gitignore, .python-version and planned directory placeholders. Added docs templates, DEV_PLAN.md, GLOSSARY.md, SOUP.md and ANOMALIES.md. Updated AGENTS.md command descriptions and ROADMAP.md. PLAN.md preserved.

**Why:** PLAN.md Step 0. No product REQ IDs assigned: Brian writes the first five before Codex adds any. Infrastructure tests are labelled `scaffold`, not falsely mapped to unwritten requirements.

**How we checked it:** `.venv/bin/python -m pytest`: 2 passed; `.venv/bin/python -m ruff check .`: all checks passed. The home-page test renders the template and checks the honest disconnected-service notice; another test rejects unsupported adapter configuration. `git diff --check` passed before this entry. Hosted GitHub Actions has NOT run: no remote is configured. CI green remains outstanding evidence; Step 0 is not fully approved or complete.

**What went wrong / surprises:** system Python 3.13 packages include an incompatible native module. uv's default cache was sandbox-blocked; resolving dependencies in the sandbox crashed in macOS network configuration. Used an isolated Python 3.12 virtual environment, a writable temporary cache, and approved elevated dependency resolution/install. TestClient emits a third-party deprecation warning (ANOM-001); tests still pass. No actual AI explanations or validator checks exist yet.

**Decisions Codex made without asking:** uv + committed lockfile provide exact dependency versions without modifying system packages. Plain Jinja hello page only; HTMX, SQLite and external adapters await later steps. CI scaffolding is prepared without creating/publishing a GitHub repo. Python product dependency versions/hashes are recorded; upstream licence verification and immutable CI action pins remain release work. No lasting model-hosting decision made: PLAN.md says Modal/vLLM while the preceding discussion proposed local Ollama. Resolve before model implementation. Future limitations to revisit: caching reuses an output but does not guarantee model rerun reproducibility; a locally stored hash chain alone cannot detect a full-history rewrite without a trusted external anchor.

**Cost incurred this step:** €0 in paid services; no model/GPU/cloud calls. Software packages downloaded locally.

**Brian — prediction (before running):**

<!-- Brian fills this in. -->

**Brian — what actually happened and what I learned (own words):**

<!-- Brian fills this in. -->

**Brian — explain-back answers:**

1. What is the mock adapter, and why do we use it before connecting a real model?
2. Why must the validator control pass/fail even if the AI disagrees?
3. What does a successful local test prove, and what does it leave unproven?

<!-- Brian answers these in his own words. -->

**Your turn:** rewrite docs/INTENDED_PURPOSE.md in your own words and write your first five numbered requirements in docs/REQUIREMENTS.md. Run `make dev`, open http://127.0.0.1:8000 and observe the Step 0 notice; stop with Ctrl+C. Record your observations above. Hosted CI evidence still needs a GitHub remote before this checkpoint can be fully satisfied.

**Evidence:** [tests](tests/test_scaffold.py), [dependency register](docs/SOUP.md), [workflow](.github/workflows/ci.yml), [anomaly](docs/ANOMALIES.md), [run instructions](README.md).

**Status:** ☐ approved by Brian — next step may start only after approval; hosted CI evidence pending.

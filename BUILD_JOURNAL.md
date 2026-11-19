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

### #0a — Step 0 review update — 2026-11-19

**Goal:** apply Brian's revised learning workflow and make model hosting unambiguous.

**User directions:** Brian asked Codex to do the work while he reviews the steps and asks questions. He then explicitly ruled out local Ollama and asked for clear docs. These supersede the earlier mandatory homework rules. They are not recorded as approval of the drafted requirements or the next build step.

**What changed:** drafted docs/INTENDED_PURPOSE.md and REQ-01–REQ-05 in docs/REQUIREMENTS.md with verification criteria; updated AGENTS.md, PLAN.md, README.md, ROADMAP.md and lifecycle templates for review-based learning. Added ADR-001 documenting Qwen3-8B/vLLM on Modal. Active architecture, development and cost docs now agree on remote model inference with a local development app/validator and mock-only automated tests.

**Why:** preserve the boundary in REQ-01/REQ-02 while making the plan useful for Brian's chosen learning style. Cite validity remains separate from source support (REQ-03). No feature or regulatory applicability conclusion is claimed implemented by these drafts.

**Explanation for review:** the mock is a predictable stand-in that costs nothing per call; it lets us check app plumbing before connecting AI. The validator controls pass/fail because an AI explanation can be wrong. Passing the two scaffold tests proves the home page responds with honest notices and unsupported adapter configuration fails; it does not prove FHIR validation, AI quality or product requirement coverage.

**Historical note:** Entry #0 describes the earlier working agreement and unresolved hosting question at that time. This entry supersedes those open actions: purpose/requirements are now drafted by Codex; homework is optional; Brian has selected hosted inference. His personal predictions and learning are not fabricated.

**How checked:** reviewed doc consistency and git diff whitespace. No runtime code or dependencies changed; the earlier two passing scaffold tests and lint results remain the runtime baseline. Hosted CI still has not run because there is no GitHub remote. Product requirements await implementation and verification in later steps.

**Cost incurred:** €0 in paid services. No cloud model provisioned.

**Review focus:** are the intended purpose and first five requirements understandable and appropriate? Brian can ask questions or request edits. Optional personal notes may be added here.

**Status:** awaiting Brian's review; no approval inferred. Step 1 not started. Hosted CI evidence remains pending.

<a id="step-1"></a>
### #1 — Step 1: Local FHIR validator — 2026-11-19

**Authorization:** Brian said “ok do it, let me knwo what i need to do” in response to the Step 1 proposal. This authorizes progressing from the Step 0 local baseline; hosted CI evidence is still pending and is not claimed complete.

**Goal:** three fictional FHIR Bundles, a teaching profile and a runnable pinned HL7 validator, with expected-versus-actual evidence.

**What changed (in progress):** Docker Compose app/validator services; pinned CLI/checksum and base images; profile and synthetic fixtures; CLI and regression scripts; process-boundary tests and runbook. ADR-002 compares the upstream server wrapper with a locally wrapped official CLI. REQ-11 added to the draft requirements for remote-terminology/network controls.

**Expectations before execution:** see [recorded expectations](docs/examples/step-1-expectations.md). Expected pass for valid fixture; missing status and decimal parse errors for broken structure; code/unit/subject-resolution errors for the profile/reference fixture.

**Checks so far:** 18 Python tests passed, Ruff passed, Compose configuration parsed. App image built with locked dependencies. These checks do not prove the fixtures validate as expected; real validator regression is pending the download/build.

**Problems so far:** validator JAR transfer timed out; restarted with range downloads and will verify the complete upstream SHA-256 before execution. System Python's HTTPS certificate store failed; using system curl's verified TLS rather than disabling certificate verification. Existing TestClient deprecation warning remains ANOM-001.

**Status:** in progress; actual validator results and final checkpoint to follow. No model deployment or paid services involved.

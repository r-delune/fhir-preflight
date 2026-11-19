---
status: draft
drafted_by: Source template (author unverified); Codex updates
---

# FHIR Preflight — Build Plan (v0.1 → public demo)

Owner: Brian Dillon (rdelune.dev) · Builder: Codex · Plan date: 2026-11-19

This file tells Codex **what** to build and **in what order**. `AGENTS.md` tells Codex **how to work** (transparency, journal, checkpoints). Read both before doing anything.

---

## 1. What this is (plain English)

A small web app that checks a **synthetic** FHIR health-data file, shows what is wrong, and has an AI model explain each problem in plain English. A human reviews every explanation (accept / edit / reject) and exports a report that records exactly which software, model and prompt versions produced it.

**The one rule that matters most:** the validator decides pass/fail. The AI only explains. The AI can never change the result.

### Intended purpose (Codex draft — Brian reviews in Step 0)
> FHIR Preflight helps software developers understand why a sample FHIR R4 payload fails validation against a pinned profile and what to investigate next. It is used with synthetic data only. It does not process real patient data, does not interpret clinical information about any individual, and does not support diagnosis, treatment or care decisions.

### Out of scope (do not build, even if it seems helpful)
- Real patient data, uploads of real records, live EHR connections
- Automatic repair of payloads (AI-suggested fixes applied to data)
- Clinical interpretation of values ("this weight is concerning")
- User accounts, payments, multi-tenant anything
- Regulatory Q&A chatbot

### Why it exists (three jobs at once)
1. **Portfolio:** a 5-minute demo — load broken file → see validator error → read AI explanation → correct it → export report → show the controls and tests behind it.
2. **Learning:** FHIR, hosting/operating an open-weight model, AI Act reasoning, an IEC 62304-*inspired* lifecycle, MDR intended-purpose reasoning.
3. **Business:** a repeatable "FHIR integration preflight" deliverable for rdelune clients. To be tested with prospects, not assumed.

---

## 2. Architecture

```
 Browser ──► Web app (Python/FastAPI, server-rendered + HTMX, SQLite)
                │
                ├──► Validator service (official HL7 FHIR validator, pinned version, Docker)
                │       returns OperationOutcome → decides pass/fail
                │
                └──► Model adapter ──► Hosted open-weight model
                          │              (vLLM on Modal serverless GPU, EU region,
                          │               scale-to-zero, OpenAI-compatible API, token auth)
                          └──► Mock adapter (tests + CI + offline dev; zero cost)
```

| Piece | Choice | Why |
|---|---|---|
| Web app | Python 3.12, FastAPI, Jinja2 + HTMX, SQLite | Small, readable, one language for Brian to follow |
| Validator | HL7 FHIR validator (via `hapifhir/org.hl7.fhir.validator-wrapper` Docker image, or `validator_cli.jar` subprocess — Codex compares both in an ADR) | Never write our own validator. Pin the version. Record which checks actually ran (structure, profile, invariants, terminology) |
| FHIR scope | R4 (4.0.1) core + **one small custom profile we author** (e.g. `DemoInfantWeightObservation`: requires `subject`, LOINC body-weight code, `valueQuantity` in grams via UCUM) | Authoring a StructureDefinition teaches profiling far better than consuming a big IG |
| Terminology | Disable remote terminology server by default (no calls to tx.fhir.org); document what this means for validation coverage | Keeps runs reproducible and data local |
| Model | Open-weight model, starting with **Qwen3-8B** (Apache-2.0 per its model card — Codex verifies current card and records it) served with **vLLM** | Hosting it yourself is the learning goal; licence allows commercial use |
| Model hosting | **Modal** serverless GPU, EU region, scale-to-zero, short scaledown window, bearer-token auth | Per-second billing, no idle cost; Starter plan includes monthly free credits (check current amount on modal.com/pricing and record in `docs/COSTS.md`) |
| App hosting (Step 7) | **Fly.io**, EU region, `auto_stop_machines`, smallest machine that runs the app; validator as a second small machine | Pay only while awake; cheap enough to leave up |
| Structured output | vLLM guided/structured JSON decoding against a JSON Schema | AI output is data the app can check, not free text |

**Hard rule: no silent fallback.** If the hosted model is down or cold, the UI says "model waking up" or "model unavailable". It never quietly switches to another provider. Every explanation records which endpoint, model ID and model revision produced it.

---

## 3. Build steps

Each step ends at a **CHECKPOINT** (see AGENTS.md). Codex stops, writes the journal entry, and waits for Brian's review. Approval may be given in chat or the journal.

**Working agreement updated 2026-11-19:** Codex drafts, implements, demonstrates and explains; Brian reviews the work and asks questions. Mandatory homework is replaced by review. Codex never invents Brian's personal learning, approvals or adopted regulatory conclusions.

**Model decision confirmed by Brian:** Qwen3-8B hosted through vLLM on Modal. The app and validator run locally during development; model inference runs on the hosted endpoint once Step 3 is completed. Tests and CI use the mock adapter. No local Ollama integration is planned. Region, GPU, pricing, licence and version details must be verified before deployment.

Every step has three parts:
- **Codex builds** — the code/docs
- **Review focus** — Codex prepares the explanation and evidence; Brian reviews and asks questions
- **Evidence** — what proves the step is done

### Step 0 — Skeleton and rules
**Codex builds:** repo layout (below), `pyproject.toml`, FastAPI hello page, pytest, ruff, GitHub Actions CI running tests with the **mock** model adapter, `BUILD_JOURNAL.md`, empty doc templates in `docs/`, `.env.example` (no secrets committed), `docs/GLOSSARY.md` seeded with FHIR/AI Act/62304 terms used in this plan.
**Review focus:** Codex drafts `docs/INTENDED_PURPOSE.md` and the first five requirements in `docs/REQUIREMENTS.md`, with verification criteria. Brian reviews the scope and wording.
**Evidence:** CI green; journal entry #0.

```
app/            web app (routes, templates, services)
app/adapters/   model adapters: mock.py, openai_compatible.py
validator/      Dockerfile / wrapper config, pinned version
fhir/profiles/  our StructureDefinition(s)
fhir/fixtures/  synthetic test payloads
fhir/excerpts/  pinned documentation excerpts with IDs (EX-001 …)
model/          Modal deployment code for vLLM
prompts/        versioned prompt files (explain_v1.md …)
tests/          pytest; test names/markers carry REQ IDs
docs/           lifecycle docs (see §5)
BUILD_JOURNAL.md
```

### Step 1 — FHIR fixtures, our profile, the validator running locally
**Codex builds:** `docker compose` with app + validator. Our custom profile. Three fixtures:
1. `valid-infant-weight.json` — passes
2. `broken-structure.json` — e.g. missing required `status`, wrong datatype
3. `broken-profile-and-reference.json` — wrong unit/code for our profile + dangling `subject` reference in a Bundle

A CLI script `scripts/validate.py <file>` that prints the OperationOutcome.
**Review focus:** Codex records expected fixture errors before running, compares actual results, and explains one profile constraint. Brian reviews the comparison.
**Evidence:** validator version + FHIR package versions recorded in `docs/SOUP.md`; Codex expectation vs actual in journal.

### Step 2 — Show the results
**Codex builds:** one-screen UI, three panels: *Sample data* (pick fixture, view JSON) · *Problems found* (severity, message, FHIRPath location, stable issue ID like `VAL-3`) · *Explanation & review* (empty for now). Clicking an issue highlights the location in the JSON. Show "Checks run: structure ✓ profile ✓ invariants ✓ terminology ✗ (disabled)".
**Review focus:** Codex explains one validator issue using the specification before adding AI. Brian reviews the reasoning.
**Step 2 extension (Brian, 2026-11-19):** add the How this works pipeline, completed-run/severity guidance, original-HL7 wording notes and verbatim nested-message excerpts with raw text preserved (REQ-15). Add a read-only `/governance` source-document browser with a fixed path catalog, safe Markdown, source status/drafter and verified git/build provenance (REQ-16). API docs/schema routes are disabled unless `ENABLE_API_DOCS=1`. Copy docs/ and top-level Markdown into Docker, without .git or .env. Link REQ-02, ADR-002, CR-000 and “Build step 2 of 8” to their governance records. See ADR-004.
**Evidence:** screenshot in journal; tests for issue-ID stability, workflow guidance, read-only document access, traversal/symlink rejection, Markdown safety, metadata/provenance and default-off API docs; actual container checks. The previously recorded visual-tooling gap must stay explicit until observed evidence closes it.

### Step 3 — Host the model (the big learning step)
**Codex builds:** `model/serve.py` deploying vLLM + Qwen3-8B on Modal: EU region, smallest GPU that fits (Codex justifies in an ADR), scale-to-zero, short scaledown window, model weights cached in a volume, bearer-token auth via Modal secret, pinned model revision (commit hash). A `docs/runbooks/model-hosting.md` with every command explained line by line. A smoke-test script measuring cold-start time, warm latency, tokens/sec.
**Review focus:** Codex prepares an explained runbook, verifies costs and implements the deployment once authorized. Brian supplies account access as necessary and reviews deployment, shutdown/redeployment, latency and measured billing evidence. No credentials go in git.
**Evidence:** `docs/SOUP.md` entry for the model (ID, revision hash, licence, quantisation, GPU, known anomalies — start the list); `docs/COSTS.md` with measured numbers; ADR for GPU and model choice.

### Step 4 — AI explanations, bounded and checked
**Codex builds:** "Explain" button per issue. The model receives only: the issue (ID, message, location), the relevant slice of the payload, and a small set of pinned excerpts from `fhir/excerpts/` with IDs. It must return JSON matching a schema:
```json
{ "issue_id": "VAL-3", "explanation": "...", "likely_cause": "...",
  "what_to_check": ["..."], "cited_excerpts": ["EX-004"],
  "confidence": "low|medium|high", "unknowns": ["..."] }
```
App-side checks (each one a numbered requirement with a test):
- `issue_id` must match the issue asked about
- every `cited_excerpts` ID must be in the set that was sent; otherwise the explanation is flagged "unsupported citation"
- explanation with no valid citation is shown as **unverified**, not as an answer
- nothing the model returns can alter validation status (test: inject a model response claiming "this is actually valid" → status unchanged)
- every AI text block is visibly labelled "AI-generated explanation"

Prompts live in `prompts/` with version numbers; the version is stored with every explanation. Cache explanations keyed by (payload hash, issue ID, prompt version, model revision, excerpt-set version) — saves money and makes results reproducible.
**Review focus:** Codex runs a red-team exercise with misleading excerpts or tricky fixtures, records observed anomalies and proposes controls/tests. Brian reviews the failures and proposed responses.
**Evidence:** tests pass with mock adapter in CI; manual run against hosted model recorded in journal; ≥3 anomalies logged.

### Step 5 — Review, export, activity log
**Codex builds:**
- Review: accept / edit / reject each explanation; edits stored as diffs with reviewer and timestamp.
- Export: Markdown report with findings, reviewer changes, and a provenance block (input hash, validator + package versions, profile version, model ID + revision, prompt version, excerpt-set version, reviewer, date). Also machine-readable JSON sidecar. AI-generated text marked as such in both.
- **Activity tab** in the app: append-only event log (file loaded, validation run, explanation requested/returned/cached, review decision, export). Each event stores the hash of the previous event (simple hash chain) so tampering is detectable; a "verify log" button checks the chain.
- Reviewer corrections can be tagged "possible anomaly" → feeds `docs/ANOMALIES.md`.
**Review focus:** Codex demonstrates review and export on all three fixtures, labels demonstration decisions as Codex-authored and explains the hash chain and its limits. Brian reviews the report and activity trail.
**Evidence:** sample export committed to `docs/examples/`; tests for log integrity.

### Step 6 — Release v0.1 (lifecycle practice)
**Codex builds:** `scripts/trace.py` generating `docs/TRACEABILITY.md` (REQ → tests → status) from test markers; release checklist; `docs/releases/v0.1.md` (what changed, known anomalies, regression results, SOUP versions, rollback plan). Tag `v0.1.0`.
**Review focus:** Codex drafts the **AI Act applicability memo** (`docs/regulatory/AI_ACT_MEMO.md`) and **MDR intended-purpose note** (`docs/regulatory/MDR_QUALIFICATION_NOTE.md`) using current primary sources and actual implementation evidence. Brian reviews; drafts are not represented as his adopted conclusions.
**Evidence:** tag exists; traceability shows every REQ has ≥1 passing test or a recorded justification.

### Step 7 — Go online (shareable demo, low cost)
**Codex builds:** Fly.io deploy (EU region), auto-stop on both machines, HTTPS. Public mode: **built-in synthetic fixtures only**; "paste your own synthetic file" only behind an invite code; per-day cap on model calls (global and per IP); cached explanations served first; a short notice: what the tool is, that output is AI-generated, synthetic data only, what is logged. A cost dashboard section in the Activity tab (model calls today/this month, estimated spend).
**Review focus:** Codex prepares the public-demo change request, impact analysis and updated risk/applicability drafts, including new users, abuse, interaction disclosure and logs/IPs. Brian reviews and approves the public release.
**Evidence:** `docs/changes/CR-001-public-demo.md`; live URL; cost for first month recorded.

### Step 8 — Change-control exercise: swap the model
**Codex builds:** deploy a second model (smaller or newer open-weight model) side by side; regression script runs all fixtures through both and produces a comparison table (citation validity rate, schema failures, unknowns raised, latency, cost per explanation).
**Review focus:** Codex presents keep / switch / roll back options with regression evidence and a recommendation in `docs/changes/CR-002-model-swap.md`. Brian reviews and approves the adoption decision.
**Evidence:** comparison committed; SOUP updated; release v0.2.

### Later (only after a real reason appears)
Larger excerpt set + retrieval (new SOUP component) · more profiles (e.g. IE/EU IPS) · fictional clinical-AI case study with an Article 6 / Articles 9–15 evidence map (paper exercise, not built) · paid client preflight run through the tool (brings in the GDPR/confidentiality gate).

---

## 4. Costs and controls

| Phase | What runs | Expected cost (Codex replaces with measured numbers in `docs/COSTS.md`) |
|---|---|---|
| Steps 0–2 | Laptop + Docker | €0 |
| Steps 3–6 | Modal GPU only while generating; scales to zero | Proposed ~$0.59 per 30 allocated minutes including configured CPU/RAM and broad-EU multiplier, before extra charges; only $1 active credit shown. See COSTS.md; approval required. |
| Step 7+ | Fly app + validator (auto-stop) + Modal on demand | Low single-digit to ~€15/month depending on machine sizes and traffic; the validator's RAM need is the main driver — measure it |

Controls (all required): scale-to-zero everywhere · explanation cache · daily call caps · invite code for custom input · spend alerts/limits on Modal and Fly (where the platform offers them) · mock adapter for all tests/CI · no GPU calls in CI.

Cold start is the trade-off: the first explanation after idle may take tens of seconds while the GPU wakes and loads the model. The UI must show this honestly. Measure it in Step 3.

---

## 5. Lifecycle documents (IEC 62304-*inspired*, not claimed compliance)

The app is **not** medical device software (no medical purpose for individual patients). We use 62304 as a voluntary discipline and record where we deviate. Never claim compliance or a formal safety class.

| Doc | 62304 area it practises | Started in step |
|---|---|---|
| `docs/DEV_PLAN.md` — lifecycle, tools (incl. Codex as a dev tool), config items, problem flow | §5.1 planning | 0 |
| `docs/INTENDED_PURPOSE.md` | (MDR / AI Act anchor) | 0 |
| `docs/REQUIREMENTS.md` — numbered `REQ-xx` | §5.2 requirements | 0 |
| `docs/ARCHITECTURE.md` + `docs/decisions/ADR-xxx.md` | §5.3 architecture | 1 |
| `docs/SOUP.md` — validator, FHIR packages, vLLM, model, Modal, Fly, key libraries: version, purpose, requirements on it, known anomalies | §8.1.2 SOUP | 1 |
| `docs/RISK.md` — hazard → cause → control → verification (harm = wrong technical guidance relied on by a developer/client) | §7 (+ ISO 14971 thinking) | 4 |
| `docs/ANOMALIES.md` | §9 problem resolution | 4 |
| `docs/TRACEABILITY.md` (generated) | §5.7 / traceability | 6 |
| `docs/releases/*`, `docs/changes/CR-*` | §5.8 release, §6/§8 change control | 6 |
| `docs/regulatory/*` (Codex drafts, Brian reviews) | AI Act, MDR | 6 |

Proposed requirement list (Codex drafts; Brian reviews; REQ-01 through REQ-05 are drafted in Step 0):
- REQ-01 Validation status is determined only by the validator.
- REQ-02 No model output can change validation status.
- REQ-03 An explanation citing an excerpt ID not in the sent set is flagged and not shown as verified.
- REQ-04 Every AI-generated text is visibly labelled as AI-generated in UI and exports.
- REQ-05 Every explanation records model ID, model revision, prompt version and excerpt-set version.
- REQ-06 No automatic fallback to a different model or provider.
- REQ-07 The activity log is append-only and its integrity can be verified.
- REQ-08 Exports include a complete provenance block.
- REQ-09 In public mode, only built-in fixtures are accepted without an invite code.
- REQ-10 Model calls are capped per day; when the cap is reached the UI says so.
- REQ-11 The app never sends payloads to a remote terminology server unless explicitly configured.

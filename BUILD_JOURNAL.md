---
status: draft
drafted_by: Source template (author unverified); Codex updates
---

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

#### Step 1 — verified checkpoint

**Final implementation:** the official CLI 6.10.4 runs in a Python development wrapper, with Java 17 from a digest-pinned image. App /api/validate proxies to the validator; no model adapter participates. Added a 0.1.0 custom profile, three fictional Bundles, download/checksum helper, validation/regression commands, exact package content lock, process/proxy tests and explained runbook. See [ADR-002](docs/decisions/ADR-002-validator-service.md), [CR-000](docs/changes/CR-000-validator-baseline.md), [requirements](docs/REQUIREMENTS.md), [SOUP](docs/SOUP.md) and [risk starter](docs/RISK.md).

**Expected versus actual:**

| Fixture | Expected | Actual | Result |
|---|---|---|---|
| valid-infant-weight | Pass | Pass; 0 errors, 3 warnings, 3 information messages | Matched |
| broken-structure | Missing status and numeric-value errors | Fail; 6 errors, including missing status and invalid decimal | Matched |
| broken-profile-and-reference | Wrong code, wrong unit and unresolved subject | Fail; 5 errors, including fixed code 29463-7, fixed unit g and demo-subject-1 | Matched |

Message counts are not distinct-defect counts: the same omission appears under several profiles; the deliberately wrong temperature code also activates core temperature-unit checks. Raw outcomes and provenance are committed under [docs/examples/step-1](docs/examples/step-1/README.md).

**Verification:** final Python suite: **20 passed**, with the previously recorded TestClient deprecation warning (ANOM-001). Ruff passed; git diff whitespace check passed. Real three-fixture regression passed through the app proxy on port 8002 with `-no-http-access`, `-tx n/a` and the validator on an internal-only network. Package inventory was identical across a fresh image rebuild and is checked before startup. The specific grams-only fixed-code error was also checked directly in the saved outcome. `make dev` verifies the cached JAR checksum, uses cached builds and waits for both services' health checks. Landing-page HTTP smoke check returned the Step 1 notice.

**What went wrong / corrections:**
- First supposedly valid fixture failed with two category errors because HL7 automatically applies core bodyweight to LOINC 29463-7. Added vital-signs category to every fixture and reran; no rule suppressed (ANOM-002, resolved).
- Port 8000 was occupied by an existing Python server. Left it running and chose app port 8002. Docker's internal validator network did not expose its host port, so requests now enter through the app proxy; validator has no published port (ANOM-003, resolved).
- Added an app health check after observing a request arrive before app startup had finished.
- GitHub remote appeared during work: https://github.com/r-delune/fhir-preflight. A read of workflow runs returned an empty list. Hosted CI is still not claimed green; earlier entries saying no remote describe historical state.
- The shared checkout changed to main during implementation, so initial Step 1 commit b67d36b landed there. The Step 1 branch was fast-forwarded to the same commit without rewriting history. Remaining checkpoint work is on codex/step-1-validator.

**Decisions and limits:** request-time validation is offline; image setup may download FHIR packages. Exact package contents are locked; if upstream defaults drift, a rebuild fails rather than accepting a new baseline silently. Three warnings on the passing fixture remain visible: two related to unit terminology without a server and one best-practice performer recommendation. The profile demonstrates technical constraints, not infant-age verification or clinical interpretation. Runtime results UI and AI/review features remain future work. No product compliance or formal safety classification is claimed.

**Cost incurred:** €0 paid services; local software/image/package downloads only. No hosted model or app resources provisioned.

**Your review:** read [the plain-English Step 1 guide](docs/examples/step-1/README.md). The app is running at http://127.0.0.1:8002; it currently confirms startup. Optional: run `make validate`, then `python3.12 scripts/validate.py fhir/fixtures/broken-profile-and-reference.json`. Ask about any result or development decision. Stop the local services with `make stop` if desired.

**Brian's personal observations / questions:** optional; not supplied or invented by Codex.

**Status:** ☐ awaiting Brian's checkpoint review. Step 2 has not started. AGENTS.md requires approval in chat or the journal before advancing. Hosted CI evidence remains a separate open item.

<a id="step-2"></a>
### #2 — Step 2: Show the results — 2026-11-19

**Authorization:** Brian said “start” after the Step 2 proposal. This approves progression from Step 1; it does not approve a paid model deployment or a public release.

**Goal:** select a synthetic fixture, see real validator findings and locate the affected data in a three-panel workbench.

**What changed:** branch `codex/step-2-results-ui`; app/main.py routes/static mounting, app/services/presentation.py, app/templates/index.html, local CSS/JavaScript and tests/test_presentation.py + tests/frontend.test.cjs. Docker app image now includes built-in fixtures. Makefile/CI include the frontend logic tests; Node is registered in SOUP before use. Updated requirements (REQ-12–REQ-14), architecture, traceability, glossary, risk/anomaly records and the review guide.

**Why:** [ADR-003](docs/decisions/ADR-003-results-presentation.md) documents a small server-rendered UI with no frontend library or external assets. REQ-01/REQ-14 keep status tied to the current validator result and clear it on fixture changes or failure. REQ-12 gives semantic finding identities; REQ-13 maps only known emitted path forms and labels fallback locations. REQ-02 has a presentation-level regression showing an injected model claim cannot alter the displayed validator status; model/review integration remains future verification.

**How checked:** 35 Python tests passed; three Node interaction-logic tests passed; Ruff and whitespace checks passed. All three actual HTTP result pages matched the Step 1 findings and stable IDs: complete fixture pass/6 findings, broken structure fail/12 findings, profile/reference fail/11 findings. See [saved comparison](docs/examples/step-2/http-smoke.json). These were real validator calls on the pinned offline service, without AI. Desktop initial rendering was observed in Chrome; a browser-submitted validation returned HTTP 200.

**What went wrong / limits:**
- Browser/IAB control repeatedly timed out; a native Chrome acquisition unexpectedly took over seven minutes despite a requested 30-second tool timeout. Native access briefly worked and emitted an initial desktop screenshot in chat, but no screenshot artifact was saved to the repo. Final visual highlight confirmation and mobile/narrow-screen QA remain pending (ANOM-004); they are not claimed complete.
- A smoke request was mistakenly started while the app was being recreated, and its connection closed. Waited for service health and validator idle, then reran the complete HTTP smoke check successfully. This was test orchestration, not a passing validator result.
- `uv` crashed inside the sandbox during `make test`/`make lint`, as seen in Step 0. Direct environment checks passed; final make commands were retried with the approved sandbox override.
- Example selection originally required clicking Load before Run. Added immediate form navigation on dropdown change to prevent validating the old fixture; the fallback Load button still works without JavaScript.

**Decisions:** use ordinary Jinja forms plus small local JS/CSS rather than add HTMX for this limited interaction. Finding IDs are hash-derived semantic references, not sequential numbers or persisted review records. Identical duplicate findings can share an ID while remaining separate displayed rows. FHIRPath mapping is deliberately limited; exact/parent/unmapped notes remain visible. The validator, profile, packages and hosted-model architecture are unchanged.

**Cost incurred:** €0 paid services. No hosted model or public app deployment.

**Your review:** open http://127.0.0.1:8002, select the profile/reference example, run validation and select the grams-unit finding. Ask about any message, design choice or step. See [plain-English guide](docs/examples/step-2/README.md). Suggested discussion: why a grams-only profile can reject otherwise valid units; why we label fallback locations; why passing a limited check retains warnings. No personal learning answers are invented.

**Evidence status:** UI implementation and local automated/HTTP checks ready for review. Final interactive/mobile browser verification and a saved screenshot artifact are still outstanding due to tooling; hosted GitHub CI has not been claimed green.

**Status:** ☐ awaiting Brian's review. Step 3 not started; AGENTS.md requires checkpoint approval before progression. Browser evidence gap remains open, rather than marking this step fully verified.

### #3-prep — Modal secret naming — 2026-11-19

Brian showed the Custom secret form with name `fhir-test` and asked what next.
Recorded the contract in model/README.md: secret `fhir-test`, key
`PREFLIGHT_API_KEY`, private randomly generated value supplied by Brian.
No secret value is generated, read or stored by Codex, and no external write or
deployment is performed. This is authorization for setup guidance, not paid
provisioning or proof that Step 2's outstanding visual evidence is complete.
The future deployment and client must use this contract. Documentation only;
no runtime changes or tests needed. Cost incurred: €0 paid services.

#### Step 2 reopened — REQ-15 / REQ-16 extension — 2026-11-19

**Authorization:** Brian explicitly requested an explanatory pipeline and read-only governance documents before the Step 2 checkpoint, then specified /governance, default-off API docs, original-wording notes, verbatim nested-message excerpts and “Build step 2 of 8”. ROADMAP.md was immediately returned to in-progress. The Modal secret contract is preserved, but no key is needed or read for this work and no cloud deployment occurs.

**What changed:** drafted REQ-15/REQ-16 and ADR-004; added pipeline/current-stage guidance, result/severity explanations and direct requirement/ADR/baseline links. Finding IDs and raw messages are unchanged; a nested message can be excerpted verbatim with full original text in a disclosure. Added /governance with a fixed ID-to-path catalog, repository Markdown rendering, source status/drafter metadata and per-document git/hash provenance. Docker copies docs/ and top-level Markdown plus a generated source manifest, excluding .git and .env. Swagger, ReDoc and OpenAPI routes are absent unless ENABLE_API_DOCS=1.

**Why / decisions:** see [ADR-004](docs/decisions/ADR-004-governance-workbench.md). Source metadata is the authority for document status and authorship; no approval is inferred from permission to build. Original template authors are labelled unverified, with Codex updates identified. Existing documents remain drafts. Unknown IDs/symlink substitutions fail closed. Markdown uses registered/pinned markdown-it-py 4.0.0 + mdurl 0.1.2, html=False, inactive images, restricted links and namespaced anchors. CSP prevents active content on the governance page. No source prose is copied into templates. A build manifest distinguishes committed document bytes from working copies; missing or changed hashes never become a clean-commit claim.

**Checks so far:** 75 Python tests and 3 Node event-logic tests passed; Ruff passed. Tests cover traversal/encoded paths/symlinks, every current ADR/change/regulatory draft being cataloged, active Markdown content, status/author metadata, source edits on subsequent reads, exact/dirty/unknown provenance, read-only routes, default API-doc 404s and explicit opt-in, pipeline stages/links/severities and nested-message quote/bracket handling. Real container checks follow below.

**What went wrong:** the first new anchor test caught blank lines splitting REQ-15/REQ-16 out of the Markdown table. Removed those blank lines in the source rather than special-case the renderer; the requirement anchors now render and tests pass. The pre-existing TestClient deprecation warning remains recorded. No new browser verification claim is made while ANOM-004 is open.

**Cost:** €0 paid services. No model, GPU, new hosting or external secret operation.

**Container findings and correction:** the first live /governance request returned 500 because Docker preserved private host modes on the original PLAN.md/AGENTS.md/BUILD_JOURNAL.md copies, making them unreadable to the non-root app user. Corrected image permissions only: top-level Markdown and manifest are 0444; docs files are 0444 and directories 0555. Host permissions remain unchanged. Added a fail-closed unreadable-source regression. Rebuilt from the cached dependency layer and verified all 22 sources are readable but not writable by the runtime user. .git and .env are absent. The initial source manifest correctly labelled changed documents as working copies based on the prior commit.

**Final verification:** 78 Python tests and 3 Node event-logic tests passed; make lint passed (same pre-existing TestClient warning). The actual container served all 22 allowlisted documents with status/drafter, git/hash provenance and restrictive CSP. /docs, /redoc and /openapi.json returned 404 by default. Literal and encoded traversal URLs returned 404. Real valid and profile/reference runs showed the correct pass/fail meanings, current Findings stage, wording notes (6 and 11), and the original-text disclosure for the verbatim nested excerpt. See [live smoke evidence](docs/examples/step-2/governance-smoke.json). Initial dependency downloads were slow (about nine minutes in Docker); no GPU or paid service ran.

**Source refresh at checkpoint:** make dev regenerates the git/content manifest. The local image is rebuilt again after the checkpoint commit so its displayed source commit identifies the committed document bytes; no clean-source claim is made for the earlier working-copy image. The UI itself exposes the current snapshot commit and file hash for inspection.

**Your review:** open http://127.0.0.1:8002 and http://127.0.0.1:8002/governance. Inspect the pipeline, a completed result, a nested-message excerpt and its raw disclosure. Follow REQ-02, ADR-002, CR-000 and the build-step link. Governance remains read-only and all current document statuses remain drafts. No secret value is needed for this review; the Modal contract is preparation only.

**Checkpoint status:** ☐ awaiting Brian's Step 2 review under AGENTS.md. The pre-existing final visual click/mobile/saved-screenshot gap (ANOM-004) remains open; no new browser screenshot is claimed. Step 3 deployment has not started. No regulatory conclusion, document approval or release approval has been invented.

<a id="step-3"></a>
### #3 — Step 3 hosted-model preparation — 2026-11-19

**Authorization:** Brian said “ok do it” after requesting the next step. This
approves preparation/progression from Step 2, not paid provisioning. Step 2's
ANOM-004 visual evidence gap remains open. Branch codex/step-3-model-hosting was
fast-forwarded to the completed Step 2 commit e6376e6 before edits.

**Built:** model/config.py, model/serve.py, model/smoke.py and offline tests;
explained docs/runbooks/model-hosting.md; proposed REQ-17, ADR-005 and CR-003;
SOUP, risk, architecture, costs, glossary, traceability and governance catalog
updates. Optional Modal SDK is separate from app runtime dependencies. The app
remains mock. No account credentials or endpoint secret values were read.

**Why:** a separately testable hosted baseline makes model behaviour and cloud
cost a controlled change. CPU-only pinned snapshot caching avoids paying for a
GPU download. One L4, bounded context/concurrency, scale-to-zero and explicit
stop/cache cleanup constrain the trial. Inference token travels through an
environment variable; no redirects or model/provider fallback. Operational paths
and unauthenticated container wake-ups remain documented exposure, so this is
not a public-demo release. EU compute/routing does not establish EU-only handling.

**Verified research:** official model card/API revision, SDK metadata, Modal
pricing/region/budget/API/CLI docs, vLLM API-key environment source and registry
CUDA digest. Exact upstream model snapshot is pinned; full remote dependency
resolution and image identity are still to be recorded after an approved build.

**Local checks:** 87 Python tests and 3 Node event-logic tests passed; Ruff passed.
New tests exercise secret/command boundary, HTTPS target restrictions, identity
mismatch rejection, fake-client timing and deployment resource settings using a
fake SDK. They do not prove real GPU fit/auth/latency. Existing TestClient
warning remains. Manual probe help runs without contacting cloud services.

**Costs / remaining evidence:** estimated $0.5873004 per 30 allocated minutes
under published broad-EU compute rates and configured CPU/RAM hard caps; extras
and allowances require review. Screenshot shows $1 active credit. Paid spend
incurred: $0. No image built remotely, model cached, endpoint deployed or remote
probe run. Real cold/warm measurements, runtime manifest, auth, stop/redeploy and
bill remain pending. Step 3 is not complete and Step 4 has not started.

**What went wrong:** optional SDK resolution initially stalled; stopped only
this task's uv processes and retried with bounded network retries and the
previously used temporary cache. Installation/lock verification is recorded below
when known. No cloud provisioning was used to bypass local verification.

**Review:** the runbook explains every command and separates local preparation
from chargeable commands. Brian reviews the proposed trial and budget settings;
no personal learning answers, regulatory conclusions or approval are invented.
AGENTS.md requires cost confirmation before paid provisioning. Await that
specific review after preparation, rather than claiming a hosted-model checkpoint.

**Upstream flag check:** vLLM 0.21.0 uses --no-enable-log-requests, replacing the older --disable-log-requests spelling. Corrected the proposed command against its versioned CLI documentation before any cloud build; also explicitly disabled output logging.

**Lock verification:** optional hosting group resolved 50 total packages; uv lock
--check --offline passed. Existing package versions were unchanged. Newly
resolved SDK dependencies are registered in SOUP with licence review explicitly
open. SDK wheel source inspection confirmed required_keys, routing_region,
startup_timeout and max_inputs support. Installing the wheels is still underway
at this preparation commit; no actual SDK import check is claimed yet.

**Final local preparation verification:** the serial locked SDK installation
completed (21 optional packages). A redundant local-wheel reuse check raced with
completion; the attempted stop found no process, and the same verified SDK
version was briefly reinstalled from the local wheel. Immediately ran uv sync
--locked --group hosting --offline successfully to restore the registry origin
and exact lock state. No dependency version changed. Real Modal 1.6.4 imported
model.serve without hydration/remote calls; CLI help confirmed run/deploy module
and environment flags plus app stop and volume delete syntax.

Local make dev rebuilt successfully. ADR-005, CR-003, Costs and Model Runbook all
returned HTTP 200 at /governance?doc=... and showed commit c7c167c provenance.
The first HTTP probe incorrectly used path-style document URLs and got 404;
corrected the probe to the app's actual query routing. No app change was needed.
Final documentation refresh follows this evidence commit so the UI displays its
committed bytes. No Modal credentials, GPU or model endpoint was accessed.

**Preparation outcome:** ready for Brian's cost review; cloud trial remains
pending. Next: verify secret exists and saved workspace credit/limits, obtain
explicit trial authorization, then cache/deploy/smoke/stop/redeploy and record
actual billing. This is an intermediate cost gate, not a claim Step 3 is complete.

### Pending direction — one fictional blood-pressure integration use case

**Source:** Brian's chat instruction after the Step 3 preparation review,
2026-11-19. **Plan only.** Finish and checkpoint Step 3 first; then draft a
PLAN.md section with UN/REQ IDs and stop for Brian's review before building.
This instruction does not approve the pending cloud spending proposal, document
approval, a model adoption or implementation of the product changes below.

**Current dependency:** Step 3 cloud cache/deployment, auth, latency,
stop/redeployment and billing evidence remain outstanding. The prepared trial
awaits cost authorization and verification of saved account limits/credit. No
model or cloud endpoint has been run. No product implementation starts here.

**Direction to carry into the post-checkpoint planning review:**

1. Use “official HL7 FHIR validator” and “FHIR R4” in UI/docs, avoiding “HL7”
   alone except where defining the organisation/terminology. Plan glossary entries
   for HL7, FHIR, HL7 v2, profile, StructureDefinition and Implementation Guide
   package. Explain the distinction between FHIR R4 and HL7 v2.
2. Draft docs/USE_CASE.md: explicitly fictional PulseKeep home blood-pressure
   monitoring startup integrates with explicitly fictional Northbridge General
   before a scarce hospital integration test slot. Check name collisions against
   well-known real products/hospitals before adopting the names; do not claim
   clearance without research. Personas: startup integration developer, hospital
   integration reviewer, startup quality lead. Walkthrough: target profile →
   messages → validate → locate findings → AI explanation → reject a wrong
   explanation → fix → rerun → export partner evidence. Remove neonatal,
   paediatric and infant scenarios from the product direction; plan a source audit
   and explicit treatment of historical evidence without silently falsifying it.
3. Draft design inputs UN-01 onwards and UN → REQ traceability, including knowing
   exactly which rules were checked, understanding problems without FHIR expertise
   and showing a partner evidence of the checks. Allocate unused REQ IDs when
   drafting; none is adopted or implemented by this entry.
4. Plan UI steps ① Target profile, ② Messages, ③ Check and review. Built-in
   profile selector shows name, version, publisher, canonical URL and content
   hash. Derive a plain-English summary from the actual StructureDefinition
   differential, never separately authored prose; raw JSON one click away. Record
   profile/hash per run and report. Header: “Message X checked against Profile Y
   vZ (hash)”. Built-in fictional messages belong to the chosen profile.
5. Before Step 4, propose formal replacement baseline CR-004 (next unused number
   at receipt; recheck before creation): fictional Northbridge General Blood
   Pressure v1.0.0, derived from the official FHIR R4 vital-signs blood-pressure
   profile. Panel, systolic/diastolic components, LOINC and UCUM mm[Hg]: mark every
   proposed code/constraint TODO(verify) until checked against the specification.
   Four expected-outcome fixtures recorded before running: valid; structural
   failure; missing diastolic plus mmHg instead of mm[Hg]; unresolved patient
   reference. Change impact includes requirements, fixtures, tests, risks, SOUP,
   docs, UI and actual regression evidence. Freeze this baseline before AI
   excerpts/saved explanations depend on it.
6. Plan uploads only, as a separate change record alongside Step 7 (provisionally
   CR-005; recheck numbering). Local/invite-only, never public demo; accept
   StructureDefinition JSON or Implementation Guide .tgz with size/type limits,
   parse data only, never request-time dependency downloads. Missing dependencies
   visibly fail with a list. Hash every uploaded file in provenance; synthetic-only
   upload notice. Draft risks for malicious/oversized files, real patient data,
   and silently missing package dependencies. Do not implement uploads now.
7. Plan a guided demo under five minutes with a step indicator and intro:
   “You’re the PulseKeep developer. Northbridge has given you its profile. Check
   your messages before the test slot.” Retain the fictional/synthetic/no clinical
   interpretation notice. Step 4 public demo uses explanations generated in
   advance, reviewed and cached with complete provenance. GPU only for genuinely
   new permitted inputs; honest model-waking state. Include one intentionally
   wrong cached explanation, explicitly labelled demonstration data, rejected
   through a Codex-authored demo review decision, never attributed to Brian.
8. Step 5 export is evidence for the integration partner: profile/hash, findings,
   fixes, AI review decisions, checks not run and all versions. Preserve REQ-02:
   AI/review cannot change the official validator result.

**Work now:** recorded the queue in this journal and ROADMAP.md only. PLAN.md,
requirements, fixtures, profiles, UI, glossary and runtime are unchanged by this
entry. No new use-case/ADR/change record has been created prematurely. No tests
run: this is an instruction/history update with no executable change.

**Next stop:** Step 3 cost authorization, then actual trial/checkpoint evidence;
after that, the draft product plan is a separate mandatory review before build.

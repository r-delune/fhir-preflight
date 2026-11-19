---
status: draft
drafted_by: Codex
---

# Third-party component register — Step 0

Exact local distribution hashes and sources are recorded in uv.lock. Licence labels below are provisional; verify upstream licence files before release. This first table records Step 0; later sections record validator, UI and proposed hosting additions. The hosted model is not deployed.

| Component | Exact version | Licence | Purpose / requirement | Known limitations |
|---|---|---|---|---|
| annotated-doc | 0.0.7 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| annotated-types | 0.8.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| anyio | 4.16.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| certifi | 2026.10.23 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| click | 8.5.1 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| colorama | 0.4.6 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| fastapi | 0.165.0 | MIT | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| h11 | 0.16.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| httpcore | 1.0.9 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| httpx | 0.28.1 | BSD-3-Clause | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| idna | 3.20 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| iniconfig | 2.3.1 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| jinja2 | 3.1.6 | BSD-3-Clause | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| markupsafe | 3.0.4 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| opentelemetry-api | 1.45.2 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| packaging | 26.3 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| pluggy | 1.7.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| pydantic | 2.14.3 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| pydantic-core | 2.50.4 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| pygments | 2.21.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| pytest | 9.2.0 | MIT | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| ruff | 0.17.5 | MIT | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| starlette | 1.10.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| typing-extensions | 4.16.0 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| typing-inspection | 0.4.5 | TODO(verify) | Transitive dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |
| uvicorn | 0.54.0 | BSD-3-Clause | Direct app/test dependency; install from lockfile | Not yet assessed; no claim of anomaly-free behaviour |

Development tools: uv 0.8.22 (MIT/Apache-2.0, verify); Python 3.12.0 local (PSF licence, verify). CI uses Python 3.12, actions/checkout@v4 and astral-sh/setup-uv@v6; action refs are major tags, not immutable commits. Before release, pin action commits and record runner versions. Codex is a development assistant; runtime/model revision is not exposed here.

## Step 1 components — registered before use

- HL7 FHIR Java validator CLI **6.10.4**, Apache-2.0 ([upstream licence](https://github.com/hapifhir/org.hl7.fhir.core/blob/6.10.4/LICENSE.txt)). Release asset SHA-256 `1106b9d58f9e363e47bea7c4fc065841e5fc91fe9d062775c3bfdd212bd653cc`, supplied by GitHub release metadata and verified on download. Requires structural/profile/invariant checking and machine-readable OperationOutcome output. Known limitations: terminology service disabled; local code checks may still run; unresolved references depend on validator policy; cold JVM/package loading is slow. No claim of exhaustive validation.
- FHIR package **hl7.fhir.r4.core#4.0.1**; FHIR specification CC0 ([licence](https://hl7.org/fhir/R4/license.html)); package-specific included notices retained in cache. Exact version requested; cache dependencies and hashes to be captured after bootstrap.
- Python container **3.12.16-slim-bookworm**, image index `sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df`. Python PSF licence plus Debian component licences. Supplies app/wrapper runtime; locked Python dependencies above.
- Eclipse Temurin JRE **17.0.21+9**, `17-jre-jammy` index `sha256:aa6381384f8db99762fa7d0d3c2b5de58874e5f12c96df4c13a1455376ae0ed1`. OpenJDK GPLv2 with Classpath Exception; image includes other component licences. Java runtime copied to Python image; verify launch and version in integration run.
- Docker Engine **28.4.0**, Compose **v2.39.4-desktop.1** observed locally; existing development tools. Docker Desktop has separate terms; no subscription purchased by this project. Required for isolated local service orchestration.

Container image digests pin contents; their full OS component licence inventory/security review is deferred to release preparation. New components must pass the fixture regression before a version change is adopted.

### Installed FHIR package baseline

Bootstrap resolved the packages below. `validator/packages.lock.json` records exact versions and per-package content hashes (excluding generated .index files). Image builds and service startup reject a different inventory; no package drift is accepted silently. A future changed upstream default may cause a build failure requiring deliberate cache/version review rather than an automatic upgrade. The packaged FHIR artifacts use their included licence notices; the project does not redistribute a full package archive in git.

| Package | Version | Content SHA-256 |
|---|---|---|
| hl7.fhir.r4.core | 4.0.1 | `f83bee4ac13dea6da256eb28fc34ee0b67f21411866a9a2c31a7261508358795` |
| hl7.fhir.uv.extensions | 5.4.0 | `0fc78158806baab3cc5268293b9a4120fb2089d0974b9b0200a060a9cc7eaeac` |
| hl7.fhir.uv.extensions.r4 | 5.2.0 | `8fea4a7f0d9f7ac33eba1a1f4fc6b0d9c68e22584146c8d0755908059d86161d` |
| hl7.fhir.xver-extensions | 0.1.0 | `25f89086a6d71a4304edad552c5752f579707ebbeb0c42169e35d456ebd1bdea` |
| hl7.terminology | 7.5.0 | `0f88b34ecc182e9b2b4629445006ac936fe8937a7ed32cd6d7fdbb0d217965b6` |
| hl7.terminology.r4 | 6.2.0 | `ee7ce5718d6de22145366891150bd5e1abe3778d5176e95427ed1e3c16c735c5` |
| hl7.terminology.r5 | 7.5.0 | `fd27739491e6145e716563e7149dcc29e71279df2eb856ba5fd147f9d2c87976` |

## Step 2 development components

The runtime remains the existing Python/Jinja/FastAPI stack plus locally authored CSS and browser JavaScript; no CDN, HTMX or new browser library is used. Node.js **v22.22.1** (observed locally; MIT and bundled component notices, https://nodejs.org/en/about/previous-releases) is a development-only tool for built-in `node:test`/`node:vm` interaction tests. These tests simulate DOM interfaces and do not establish actual layout or browser compatibility. CI uses `actions/setup-node@v4` with exact Node version 22.22.1; immutable action pinning remains release preparation work alongside existing actions. No npm packages are installed.

## Step 2 governance Markdown renderer — registered before use

- **markdown-it-py 4.0.0**, MIT, official package metadata: https://pypi.org/project/markdown-it-py/4.0.0/ ; upstream security guidance: https://markdown-it-py.readthedocs.io/en/latest/security.html . Required to render repository Markdown with raw HTML disabled (`html=False`), explicit safe link handling, no active images and no extra plugins. Known hazard: the default CommonMark configuration enables raw HTML; our constructor must explicitly disable it. Parser/configuration regressions could enable XSS, so malicious HTML/protocol fixtures are tested. Not a general HTML sanitizer.
- **mdurl 0.1.2**, MIT, transitive URL parser dependency: https://pypi.org/project/mdurl/0.1.2/ . Required for renderer link parsing; application additionally restricts navigation schemes and local document targets. Distribution hashes and all resolved versions will be recorded in uv.lock before installation.

No YAML or sanitization library is introduced. Document front matter is a deliberately limited flat metadata format, not general YAML, with fail-closed draft/unknown defaults. No additional raw HTML plugins are allowed.

## Step 3 proposed hosted-model baseline (registered before use)

Not deployed or adopted. See ADR-005 and CR-003. Runtime transitive packages and
image ID must be captured after the approved build; top-level pins alone do not
freeze the entire remote environment.

| Component | Exact identity | Licence / terms | Requirement / known anomalies |
|---|---|---|---|
| Qwen3-8B | Qwen/Qwen3-8B revision b968826d9c46dd6066d109eabc6255188de91218; BF16, no quantisation | Apache-2.0, upstream model card | REQ-17; invented facts, bad citations, malformed JSON, misleading confidence; not clinically validated |
| vLLM | 0.21.0 | Apache-2.0 | Serve pinned model only; GPU fit/startup not measured; API-key protection covers inference API, not all operational paths |
| Transformers | 5.8.1 | Apache-2.0 | Qwen tokenizer/chat template; dependency compatibility awaits remote build |
| Modal SDK | 1.6.4 | Apache-2.0 | Deployment-only optional dependency; no import-time remote execution; service usage governed separately by Modal terms |
| CUDA image | nvidia/cuda:12.9.0-devel-ubuntu22.04@sha256:26cd7d00c09c1f3ff187929c7f4aa7e9273020cb18e86730f40e062e8ffa4d33 | NVIDIA CUDA image licences + Ubuntu component licences; review distribution before release | Remote serving base, Python 3.12 added by Modal; driver supplied by platform |
| Modal compute/storage | Service (not an immutable software release); L4, region eu, routing eu-west | Modal service terms; pricing checked 2026-11-19 | REQ-17; availability, billing delays, cold starts, non-EU control plane/storage not excluded |

Sources: https://huggingface.co/Qwen/Qwen3-8B,
https://modal.com/docs/examples/vllm_inference,
https://github.com/modal-labs/modal-client,
https://modal.com/pricing. Hosting is not a free-model guarantee.

### Optional SDK resolved dependencies

Resolved locally for preparation; licence review remains open before release.

| Component | Version | Licence status | Purpose / limits |
|---|---|---|---|
| aiohappyeyeballs | 2.7.1 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| aiohttp | 3.14.5 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| aiosignal | 1.4.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| attrs | 26.1.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| cbor2 | 6.3.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| frozenlist | 1.8.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| grpclib | 0.4.9 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| h2 | 4.4.1 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| hpack | 4.2.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| hyperframe | 6.1.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| multidict | 7.2.1 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| propcache | 0.5.4 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| protobuf | 7.36.2 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| rich | 15.0.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| synchronicity | 0.12.7 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| toml | 0.10.2 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| types-certifi | 2021.10.8.3 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| types-toml | 0.10.8.20260518 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| watchfiles | 1.3.0 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |
| yarl | 1.25.1 | TODO(verify upstream licence) | Optional Modal SDK dependency; locked hashes in uv.lock; not app runtime; no anomaly-free claim |

### First remote image-build observation (ANOM-005)
The runtime image im-iosm6gspUOj9uHerxcKtDU built successfully (181.83 seconds),
but app registration failed before weight download/inference. Build log observed
vLLM 0.21.0, Transformers 5.8.1, torch 2.11.0 and huggingface-hub 1.33.0. These
are build observations, not a successfully adopted model baseline or a full
transitive lock. The separate CPU app shares this same image definition.

# Third-party component register — Step 0

Exact distribution hashes and sources are recorded in uv.lock. Licence labels below are provisional; verify upstream licence files before release. No validator, FHIR package, runtime AI model, cloud service or HTMX is used yet.

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

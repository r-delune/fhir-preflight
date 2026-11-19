# Step 1 — local checker runbook

## Start

From the WORKDEMO directory:

```sh
make dev
```

This verifies/downloads the pinned HL7 JAR, builds app and validator images, fetches FHIR packages at build time, and starts the two containers in the background. Docker Desktop must be running. First setup needs internet and may be slow. Subsequent request-time validation is offline. No hosted AI service or model is deployed at this step.

The hello page is http://127.0.0.1:8000. Results are available through the command below; the results UI comes in Step 2. The validator's development endpoint is bound to the laptop at http://127.0.0.1:8081.

## Check examples

```sh
make validate
python3.12 scripts/validate.py fhir/fixtures/broken-structure.json
python3.12 scripts/validate.py fhir/fixtures/broken-profile-and-reference.json
```

The first command chooses the valid fixture. Each prints the original OperationOutcome JSON; the short pass/fail summary goes to stderr. Exit code 0 = pass for configured checks, 1 = validation errors, 2 = incomplete/infrastructure failure. Use `--envelope` to include status, checks and provenance. The input hash describes the JSON reserialized by the wrapper, not the original file's whitespace.

`make regression` runs all three cases, checks expected error categories, and stores real results under docs/examples/step-1/. It uses the real validator, with no AI calls. `make test` runs fast isolated process-boundary tests with simulated validator responses; these do not establish FHIR conformance by themselves.

## Stop

```sh
make stop
```

This stops/removes the two local containers and their Compose network. Cached download and images remain for faster restart. No cloud resources are involved.

## Reading a result

Read `issue[].severity`, `details.text` / `diagnostics`, and `expression` / `location`. An error about `Observation.status` means the required workflow status is missing. A profile error about the quantity code `g` means the example violates our grams-only teaching rule; it does not mean kilograms are invalid FHIR generally.

Remote terminology is disabled, not every terminology check: locally available codes and profile-fixed values can still be checked. Do not infer that LOINC membership or every external value set has been verified. The profile name refers to the fictional example; it does not check infant age or medical appropriateness.

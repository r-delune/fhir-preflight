# Step 1 — what we built and what happened

Brian's role is to review this explanation and ask questions. No account setup, model deployment or homework is needed at this checkpoint.

## The working pieces

A **Bundle** is our envelope containing two fictional resources: a Patient and an Observation (a recorded measurement). A **profile** adds rules to standard FHIR. Our demo requires the body-weight code, grams, a numeric value and a subject that resolves to a Patient in the supplied data.

The existing HL7 validator does the checking. Our code sends data to it, preserves its OperationOutcome and reports pass/fail. There is no AI involved yet. AI will later explain these already-determined findings.

## Actual results

| Example | Expected | Actual | What it teaches |
|---|---|---|---|
| valid-infant-weight.json | Pass | Pass; 0 errors, 3 warnings, 3 information messages | Passing is limited to selected checks; warnings remain visible. |
| broken-structure.json | Fail | Fail; 6 errors, 3 warnings, 3 information messages | Missing status and a number supplied as text break required data rules. |
| broken-profile-and-reference.json | Fail | Fail; 5 errors, 3 warnings, 3 information messages | A wrong measurement code, kilograms and a missing referenced patient break our teaching profile. |

Counts are messages, not distinct defects: one missing field can be reported under several profiles. The deliberately wrong temperature code also causes the standard body-temperature profile to run, producing additional unit errors. This is expected behaviour and illustrates why we keep the original findings.

### One error explained without AI

The profile says the quantity code must be `g`. The broken example supplies `kg`. The validator reports: `Value is 'kg' but is fixed to 'g'`.

That means the data fails **our grams-only rule**. It does not mean kilograms are invalid FHIR. We neither convert the number nor repair the file automatically.

### What initially went wrong

My first supposedly valid example omitted the vital-signs category. The real validator rejected it because the body-weight code triggers FHIR's core bodyweight rules. I added the category, retained the validator rules, and reran the checks. ANOM-002 records that correction; the initial version remains in git history.

I also found port 8000 already occupied. I left that process alone and used 8002. The app forwards requests to an isolated validator because the internal Docker network does not publish a directly reachable validator endpoint on this setup (ANOM-003).

## Limits to understand

Remote terminology services are disabled. The validator retained two warnings about unit terminology and an information message about an unconfirmed value-set check, plus a best-practice warning about a missing performer. Local fixed-value and available terminology checks still operate. A pass is not full terminology certification, clinical validation, or a guarantee of integration with an EHR.

The checks metadata describes configured categories and a completed validator invocation; a malformed field can prevent further checks on that field. The profile name does not establish infant age or interpret the measurement clinically.

## Optional hands-on check

The app is running at http://127.0.0.1:8002; the page currently confirms startup. The results screen comes in Step 2.

From WORKDEMO:

```sh
make validate
python3.12 scripts/validate.py fhir/fixtures/broken-profile-and-reference.json
```

The first returns pass (with warnings); the second prints errors and returns exit code 1. `make stop` stops the two containers; `make dev` starts them and waits for readiness. Existing processes on port 8000 are unaffected.

Review prompts, if useful: Why can kilograms fail our profile while still being valid FHIR? Why does a passing run still have warnings? Ask about any line you want explained.

## Evidence

Raw validator results: [valid](valid-infant-weight.json), [broken structure](broken-structure.json), [broken profile/reference](broken-profile-and-reference.json), [summary](summary.json). Exact software/package baseline: [SOUP register](../../SOUP.md) and [package lock](../../../validator/packages.lock.json). Implementation and decision: [ADR-002](../../decisions/ADR-002-validator-service.md).

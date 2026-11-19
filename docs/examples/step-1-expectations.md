# Step 1 — Codex expectations recorded before validation

- `valid-infant-weight.json`: no error/fatal issues; warnings/information may remain because remote terminology is disabled.
- `broken-structure.json`: missing required Observation.status and a non-numeric Quantity.value should be errors.
- `broken-profile-and-reference.json`: wrong LOINC code, kilograms instead of the profile's fixed grams code, and an unresolved subject should fail. The custom subject invariant explicitly requires resolution to a Patient; this avoids assuming all dangling references are universally invalid FHIR.

The custom profile teaches structural constraints, not whether a fictional measurement is clinically appropriate or whether the subject is an infant. Passing is limited to configured checks.

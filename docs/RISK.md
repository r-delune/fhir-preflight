# Risk register

Template; assess as controls are introduced.

| ID | Hazard / harm | Cause | Control | Verification | Residual risk / decision |
|---|---|---|---|---|---|
| RISK-01 | Developer relies on a false passing result | Validator unavailable or response malformed | REQ-01: incomplete state, no pass on process failure | tests/test_validator.py process-failure cases; real fixture regression | Review pending; only configured checks are covered |
| RISK-02 | Developer assumes full terminology/clinical verification | Pass label hides disabled checks or profile scope | REQ-11; warnings retained, checks/provenance exposed, runbook scope statement | Offline real-validator outcomes and command/network checks | Review pending; no clinical interpretation is performed |
| RISK-03 | Faulty fixture becomes a misleading baseline | A supposedly valid example omits a standard requirement | Record expectations, run real engine, retain errors and correct fixture before adoption | ANOM-002 and three-fixture regression | Review pending; finite fixtures cannot prove complete validator correctness |
| RISK-04 | Reviewer investigates the wrong data location | FHIR logical paths differ from JSON, missing fields or unsupported path syntax | REQ-13: preserve raw path and explicitly label exact, parent or unmapped selection | tests/test_presentation.py and frontend event-logic tests; browser QA still pending | Review pending; mapping is a limited display helper, not a FHIRPath engine |
| RISK-05 | Old result is mistaken for a newly selected example | Fixture changes without clearing findings | REQ-14: new selection loads a new page, clears results and disables old validation during navigation | Route and frontend event-logic tests | Review pending; browser interaction confirmation outstanding |

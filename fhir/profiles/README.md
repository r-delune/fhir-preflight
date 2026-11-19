# DemoInfantWeightObservation — 0.1.0

A locally authored teaching profile derived from R4 Observation. The canonical URL uses example.org; the validator loads this file locally and never fetches the canonical URL.

Rules: code includes LOINC `29463-7` (body weight); subject is required and resolves to a Patient in the supplied data; value is a Quantity with a numeric value; system is UCUM (`http://unitsofmeasure.org`) and code is exactly `g` (grams). These are data constraints, not clinical interpretation.

The differential records only our extra constraints; HL7 generates the full snapshot from base Observation. For example, the grams rule narrows an otherwise valid UCUM weight unit: kilograms can be valid FHIR but intentionally fail this demo profile. `demo-subject-1` is our FHIRPath invariant, evaluated by the HL7 engine, requiring the subject reference to resolve. Unresolved external references are not universally invalid base FHIR.

The profile name identifies the fictional learning example. It does not verify infant age, assess a measurement's medical significance or implement every standard vital-signs profile requirement. Fixtures use no real-person data.

References: [HL7 profiling](https://hl7.org/fhir/R4/profiling.html), [R4 body-weight profile](https://hl7.org/fhir/R4/bodyweight.html), [StructureDefinition](https://hl7.org/fhir/R4/structuredefinition.html).

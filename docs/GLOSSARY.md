# Glossary

**FHIR:** A standard for exchanging health information using defined data structures called resources. We pin R4 (4.0.1) so examples use the same rules. [HL7](https://hl7.org/fhir/R4/)

**Profile:** Additional rules for a particular use of a FHIR resource. Our custom profile is planned for Step 1. [HL7](https://hl7.org/fhir/R4/profiling.html)

**Validator / OperationOutcome:** A validator checks a payload against selected rules. OperationOutcome is a FHIR resource for reporting issues; a clean result only covers the checks actually performed. [HL7](https://hl7.org/fhir/R4/operationoutcome.html)

**Mock adapter:** A small replacement for a service that gives predictable results during development and tests. Our mock makes no network or AI calls. [Python testing documentation](https://docs.python.org/3/library/unittest.mock.html)

**AI Act applicability assessment:** A written analysis of which EU AI Act provisions apply to a particular system and use. Codex drafts the assessment for Brian to review; review status is recorded explicitly. [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

**IEC 62304-inspired lifecycle:** We practise planning, requirements, verification and change control using this medical-device software standard as a reference. This phrase does not claim conformity or certification. [ISO](https://www.iso.org/standard/38421.html)

**SOUP:** Software of unknown provenance, a term used in IEC 62304. We use a component register to document third-party software, its exact version and limitations as a learning exercise. [IEC](https://webstore.iec.ch/en/publication/6792)

**Lockfile:** A generated list of exact dependency versions and distribution hashes. It helps install the same software on different computers. [uv](https://docs.astral.sh/uv/concepts/projects/sync/)

**CI:** Continuous integration runs automated checks when changes reach the connected repository. A workflow file alone is not evidence of a successful hosted run. [GitHub](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)

**ADR:** A short architecture decision record explaining a decision, alternatives and consequences. It helps future readers understand why the system looks this way. [Microsoft](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

**StructureDefinition / differential:** A StructureDefinition is the FHIR resource describing a structure or profile. A differential lists our extra rules; a snapshot combines those rules with inherited base rules. [HL7](https://hl7.org/fhir/R4/structuredefinition.html)

**Invariant / FHIRPath:** An invariant is a rule expressed as a condition that must hold. FHIRPath is the expression language the validator uses to evaluate rules such as whether a reference resolves. [HL7](https://hl7.org/fhir/R4/fhirpath.html)

**LOINC / UCUM:** LOINC identifies what was measured, while UCUM identifies the unit in a machine-readable way. Our demo fixes one measurement code and the grams unit; it does not assess the medical significance of a value. [HL7 terminology guidance](https://hl7.org/fhir/R4/terminologies-systems.html)

**Container / Docker Compose:** A container runs software in an isolated environment. Compose defines how our app and validator containers start and communicate on the laptop. [Docker](https://docs.docker.com/compose/)

**Stable finding ID:** A content-derived reference for a validator message. Reordering messages or changing temporary file metadata does not change this reference; it is not a persisted review record yet. [Python hashing documentation](https://docs.python.org/3/library/hashlib.html)

**Location mapping:** FHIRPath refers to the logical FHIR model, which is not always identical to JSON property names. Our display maps a limited set of emitted paths to JSON lines and labels parent or unsupported-path fallbacks explicitly. [HL7](https://hl7.org/fhir/R4/fhirpath.html)

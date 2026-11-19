"""Literal document paths. URLs select IDs; they never supply filesystem paths."""

DOCUMENTS = {
    "roadmap": ("Roadmap", "ROADMAP.md", "Plan & history"),
    "build-journal": ("Build Journal", "BUILD_JOURNAL.md", "Plan & history"),
    "plan": ("Build Plan", "PLAN.md", "Plan & history"),
    "working-rules": ("Working Rules", "AGENTS.md", "Plan & history"),
    "readme": ("Project README", "README.md", "Plan & history"),
    "intended-purpose": ("Intended Purpose", "docs/INTENDED_PURPOSE.md", "Lifecycle"),
    "requirements": ("Requirements", "docs/REQUIREMENTS.md", "Lifecycle"),
    "traceability": ("Traceability", "docs/TRACEABILITY.md", "Lifecycle"),
    "risk": ("Risk", "docs/RISK.md", "Lifecycle"),
    "soup": ("SOUP", "docs/SOUP.md", "Lifecycle"),
    "anomalies": ("Anomalies", "docs/ANOMALIES.md", "Lifecycle"),
    "development-plan": ("Development Plan", "docs/DEV_PLAN.md", "Lifecycle"),
    "architecture": ("Architecture", "docs/ARCHITECTURE.md", "Lifecycle"),
    "costs": ("Costs", "docs/COSTS.md", "Lifecycle"),
    "glossary": ("Glossary", "docs/GLOSSARY.md", "Lifecycle"),
    "adr-001": ("ADR-001 · Hosted model", "docs/decisions/ADR-001-hosted-model.md", "Decisions"),
    "adr-002": ("ADR-002 · Validator", "docs/decisions/ADR-002-validator-service.md", "Decisions"),
    "adr-003": ("ADR-003 · Results", "docs/decisions/ADR-003-results-presentation.md", "Decisions"),
    "adr-004": (
        "ADR-004 · Governance UI", "docs/decisions/ADR-004-governance-workbench.md", "Decisions"
    ),
    "cr-000": ("CR-000 · Baseline", "docs/changes/CR-000-validator-baseline.md", "Change records"),
    "ai-act": ("AI Act draft", "docs/regulatory/AI_ACT_MEMO.md", "Regulatory drafts"),
    "mdr": (
        "MDR qualification draft", "docs/regulatory/MDR_QUALIFICATION_NOTE.md", "Regulatory drafts"
    ),
}

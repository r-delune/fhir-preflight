# AGENTS.md — how Codex works in this repo

Read `PLAN.md` first. This file sets the working rules. They exist because **the owner (Brian) is using this project to learn**, so how the work is done matters as much as the result.

## 1. Work in small, visible steps
- Work on one step from `PLAN.md` at a time. Split a step into sub-tasks small enough to review in ~15 minutes each.
- One branch per step (`step-3-model-hosting`), small commits with messages that say *why*, not just *what*.
- Never start the next step until Brian has written "approved" (or similar) in the journal entry for the current one.

## 2. Stop at every CHECKPOINT
At the end of each step (and whenever you make a decision with lasting consequences), stop and append an entry to `BUILD_JOURNAL.md` using the template there. Then summarise in chat:
1. What I built (files changed, with paths)
2. Why (link the REQ / ADR)
3. How to see it working (exact commands, what you should see)
4. What I'm unsure about or chose without asking
5. **Your turn:** the "Brian does" task from `PLAN.md`, plus 2–3 explain-back questions about this step

## 3. Leave the learning tasks to Brian
- Do not complete any "Brian does" task, write his predictions, or write conclusions in `docs/regulatory/`. You may review them for consistency with the code and point out errors.
- When Brian runs commands himself (e.g. the model deploy), provide a runbook that explains each line. Do not run cloud deploys on his behalf unless he asks.

## 4. Explain as you go
- New concept → add or update an entry in `docs/GLOSSARY.md` (plain English, 2–4 sentences, one link to an authoritative source).
- Non-trivial decision → `docs/decisions/ADR-xxx.md` (context, options considered, decision, consequences). Keep it short.
- Code comments explain *why*, not *what*.

## 5. Traceability is not optional
- Every requirement in `docs/REQUIREMENTS.md` has an ID (`REQ-xx`).
- Tests reference REQ IDs (`@pytest.mark.req("REQ-02")`).
- New third-party component, model, image or service → entry in `docs/SOUP.md` before it is used (name, exact version/hash, licence, why, what we require of it, known anomalies).
- Changes to the model, prompt, excerpt set, validator version or hosting → a change record in `docs/changes/` with impact analysis and regression results.

## 6. Safety and cost rules
- **Synthetic data only.** Never add real patient data, realistic real-person identifiers, or data scraped from real systems.
- **No secrets in git.** Use `.env` (gitignored) locally and the platform secret stores in the cloud. Keep `.env.example` current.
- **Tests and CI use the mock model adapter.** No GPU or paid API calls in CI.
- **No silent fallback** to another model/provider. Fail visibly.
- The AI explains; it never changes validation results. Any change touching that boundary needs a test proving REQ-02 still holds.
- Before adding anything that costs money monthly, state the expected cost and wait for approval.

## 7. Honesty
- If something didn't work, say so in the journal — failures are the most useful learning material.
- Don't claim IEC 62304, AI Act or MDR compliance anywhere in code, docs or UI. Use "62304-inspired lifecycle" and "applicability assessment".
- If you're unsure about a FHIR or regulatory fact, mark it `TODO(verify)` and cite what you'd check, rather than guessing.

## 8. Commands (Codex keeps this section current)
```
make setup      # install locked dependencies into .venv (Python 3.12 + uv)
make dev        # Step 0: local hello page; validator/docker compose arrive in Step 1
make test       # pytest with mock adapter; scaffold checks until Brian writes requirements
make lint       # ruff
make trace      # Step 0: explains that generation is deferred to Step 6
```

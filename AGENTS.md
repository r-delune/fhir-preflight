# AGENTS.md — how Codex works in this repo

Read `PLAN.md` first. This file sets the working rules. They exist because **the owner (Brian) is using this project to learn**, so how the work is done matters as much as the result.

## 1. Work in small, visible steps
- Work on one step from `PLAN.md` at a time. Split a step into sub-tasks small enough to review in ~15 minutes each.
- One branch per step (`step-3-model-hosting`), small commits with messages that say *why*, not just *what*.
- Never start the next step until Brian approves it in chat or the journal. Record chat approval in the journal with its source; never invent approval.

## 2. Stop at every CHECKPOINT
At the end of each step (and whenever you make a decision with lasting consequences), stop and append an entry to `BUILD_JOURNAL.md` using the template there. Then summarise in chat:
1. What I built (files changed, with paths)
2. Why (link the REQ / ADR)
3. How to see it working (exact commands, what you should see)
4. What I'm unsure about or chose without asking
5. **Review:** explain the step in plain English, show evidence and invite questions. Exercises and explain-back questions are optional.

## 3. Codex drafts and demonstrates; Brian reviews
- Brian requested this workflow in chat on 2026-11-19: Codex does the work, Brian reviews the steps and asks questions. This supersedes the original mandatory hands-on learning tasks.
- Draft purpose statements, requirements, worked examples and evidence-based regulatory assessments for review. Clearly distinguish a Codex draft from Brian's approval or adopted conclusion.
- Do not invent Brian's predictions, observations, personal learning or decisions. Provide Codex explanations and observed evidence instead; Brian's personal notes are optional.
- Prepare explained runbooks and carry out authorized technical work. Brian supplies credentials/account access when needed; confirm verified cost before paid provisioning. Public releases and model adoption remain review checkpoints.
- Model target: Qwen3-8B through vLLM on Modal, as specified in PLAN.md. No local Ollama integration or automatic provider fallback. Verify hosting details before implementation.

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
make dev        # app + validator in Docker Compose, detached; first build downloads packages
make stop       # stop local containers
make validate   # validate built-in valid fixture; FILE=path selects another synthetic file
make regression # run the three fixtures through the real local validator
make test       # pytest with mock adapter + Node interaction-logic tests (Node 22.22.1)
make lint       # ruff
make trace      # Step 0: explains that generation is deferred to Step 6
```

# Claude Certified Architect – Foundations: Practice Exam (Plugin)

> Packaged and maintained by [Calvin Cheng](https://calvinx.com). The original question bank was created by [Olivier Legris](https://www.alterhq.com).
>
> Built from publicly available information. This is an unofficial community resource — Anthropic is not involved with this project.

A community-built practice exam for the **Claude Certified Architect – Foundations** certification, packaged as a **Claude Code plugin** — no manual file copying required.

149 scenario-based questions across 5 domains. Run `/ccaf-exam` in your terminal for an interactive, scored session.

---

## Install

In Claude Code:

```
/plugin marketplace add calvinchengx/ccaf-exam
/plugin install ccaf-exam@calvinchengx
```

That's it — `/ccaf-exam` is now available. The question bank ships inside the plugin, so there are no files to copy or paths to configure.

> If you host your own fork, replace `calvinchengx/…` with your `owner/repo`. You can also point the marketplace at a local path: `/plugin marketplace add /absolute/path/to/ccaf-exam`.

---

## Run the exam

```
/ccaf-exam          # 20 questions (default)
/ccaf-exam 10       # quick 10-question session
/ccaf-exam 60       # full exam simulation (matches the real 60-question exam)
/ccaf-exam 149      # every question, for extra practice
```

> The real certification exam is **60 questions in 120 minutes**. This bank has 149 questions, so `/ccaf-exam 60` mirrors the actual exam length while `/ccaf-exam 149` gives you the full set for extra practice.

The skill will:
- Ask your preferred question count, domain focus, and feedback mode
- Present each question via Claude's interactive UI (options A/B/C/D)
- **Shuffle answer positions every session** so you learn the material, not the answer key
- Give immediate feedback or an end-of-exam summary (your choice)
- Calculate a scaled score (100–1,000; pass at 720) and a per-domain breakdown

---

## Exam Structure

| Domain | Topic | Weight |
|--------|-------|--------|
| 1 | Agentic Architecture & Orchestration | 27% |
| 2 | Tool Design & MCP Integration | 18% |
| 3 | Claude Code Configuration & Workflows | 20% |
| 4 | Prompt Engineering & Structured Output | 20% |
| 5 | Context Management & Reliability | 15% |

- **Format:** Multiple choice, 4 options (1 correct, 3 distractors)
- **Real exam:** 60 questions, 120 minutes, $125 USD, credential valid 12 months
- **Scoring:** Scaled 100–1,000. Pass at 720 (~69% correct)
- **This bank:** 149 questions, all with explanations (well beyond the 60-question exam, for extra practice)

---

## What's inside

| Path | Description |
|------|-------------|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.claude-plugin/marketplace.json` | Marketplace manifest (enables `/plugin marketplace add`) |
| `skills/ccaf-exam/SKILL.md` | The `/ccaf-exam` runner |
| `skills/ccaf-exam/questions.json` | Structured question bank (id, domain, task, stem, options, correct index, explanation) |
| `data/exam.md` | Full human-readable exam with answer key, for reading/study |

The runner reads the structured `questions.json` directly — parsing is deterministic, and answer positions are randomized at runtime so no position bias is exposed.

---

## What the exam covers

Questions are drawn from 6 realistic production scenarios (4 selected per full run):

1. **Customer Support Resolution Agent** — agentic loops, tool design, escalation
2. **Code Generation with Claude Code** — CLAUDE.md, plan mode, slash commands
3. **Multi-Agent Research System** — coordinator patterns, error propagation, context
4. **Developer Productivity with Claude** — built-in tools, MCP integration
5. **Claude Code for CI/CD** — non-interactive mode, structured output, batch processing
6. **Structured Data Extraction** — JSON schemas, validation loops, human review

---

## Source

Based on the official *Claude Certified Architect – Foundations Certification Exam Guide* (Anthropic, v0.2 — June 30 2026), which provides domain descriptions, task statements, sample questions, and preparation exercises. Every question in this bank has been validated against that guide, which extends it with additional questions covering all 30 task statements.

---

## Disclaimer

Unofficial community resource. Not affiliated with or endorsed by Anthropic. The certification exam itself is administered separately by Anthropic.

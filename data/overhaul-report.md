# Question Bank Overhaul Report

Reviewed 77/77 questions via multi-agent workflow (accuracy check + shuffle-safe explanation rewrite + answer-key rebalance).

## Answer key distribution

| | A | B | C | D |
|---|---|---|---|---|
| Before | 18 | 50 | 9 | 0 |
| After  | 20 | 19 | 19 | 19 |

## Answer corrections applied (1)

- **Q49**: correct answer changed from original option B → a different option. The stem stipulates the three bugs are independent, non-interacting, and in different parts of the function, which removes the rationale for serializing; the keyed explanation is backwards (batching is not specifically "for interacting problems"), and Claude Code guidance favors giving precise, complete instructions up front for well-scoped fixes, making Option A at least as defensible as B — so the item is flawed and needs human review.

## Flagged for human review (1)

- **Q49**: The stem stipulates the three bugs are independent, non-interacting, and in different parts of the function, which removes the rationale for serializing; the keyed explanation is backwards (batching is not specifically "for interacting problems"), and Claude Code guidance favors giving precise, complete instructions up front for well-scoped fixes, making Option A at least as defensible as B — so the item is flawed and needs human review.

## Technical issues surfaced (5)

- **Q18**: Minor terminology looseness (not enough to change the answer): in the Claude Agent SDK the subagent-spawning tool was renamed from `Task` to `Agent` in Claude Code v2.1.63, though `Task` still appears in the SDK's tools list and permission records, so the stem's use of `Task` is acceptable. Also, within an `AgentDefinition` the per-agent tool list field is named `tools`, while `allowedTools` is the option used for auto-approving tool invocations; the stem blends these, but the underlying principle (the spawning tool must be in the allowed set) is correct and B remains the single best answer.
- **Q28**: Minor imprecision: `--resume` selects a session by ID (or from an interactive list) rather than a free-form "session-name," but this does not change which option is correct. Substantively the answer is sound.
- **Q29**: Minor terminology imprecision (not enough to change the answer): in the actual Agent SDK, forking is not a standalone `fork_session()` call but an option — `fork_session=True` (Python) / `forkSession: true` (TypeScript) — set on `query()` together with `resume=<session_id>`. Each fork produces a new independent session ID starting from a copy of the baseline history, which is exactly the behavior described, so the choice is still unambiguously correct.
- **Q49**: The stem explicitly stipulates the three bugs are independent, in different parts of the function, and do not interact. For independent, clearly-specified defects, the more efficient and commonly recommended approach is to report all of them together in one detailed message so Claude fixes them in a single pass, then verify. The keyed answer (sequential, one message per fix) and its explanation invert the usual rationale: they claim batching is for interacting problems, but one-at-a-time iteration is actually the tool reserved for complex, interacting changes where each step must be verified before the next. Because the bugs here are stated to be fully non-interacting, the single-detailed-message option is at least as defensible as, and arguably better than, the keyed sequential option. The question is ambiguous and the explanation's stated reasoning is backwards; if the intended teaching point is sequential verification, the stem should not emphasize independence and non-interaction.
- **Q54**: none — verified against the Claude Code memory docs (code.claude.com/docs/en/memory). Subdirectory CLAUDE.md files load on demand when Claude works in that directory (providing per-package scoping and preventing rule bleed), and the `@path/to/import` syntax loads shared conventions at launch, so the keyed answer describes the officially recommended modular pattern. Minor note: the distractor referencing `.claude/rules/` uses a fabricated `projects:` frontmatter key — the real field is `paths:` with glob patterns — which reinforces that it is not the correct choice.

## Explanations still referencing a letter after rewrite (0)

- None — all explanations are shuffle-safe.

## Syllabus reconciliation (FINAL — supersedes the four changes above)

After the overhaul, the four content edits were checked against the **official Claude Certified Architect – Foundations Exam Guide, v0.2 (last updated June 30 2026)**. The guide contradicts all four edits, because the multi-agent review had validated answers against the *current real-world SDK* rather than the exam's own (frozen) terminology and positions. For a certification practice tool, the syllabus is ground truth. **All four edits were reverted:**

| Q | Guide reference | Reverted to |
|---|---|---|
| **Q49** | Task 3.5: *"provide all issues in a single message (interacting problems) versus fixing them sequentially (independent problems)"* | Original answer — **sequential iteration** for the independent bugs. The overhaul's flip to "single message" was backwards. |
| **Q18** | Task 1.3: *"allowedTools must include \"Task\""* | `allowedTools` / `Task` (not `tools` / `Agent`). |
| **Q28** | Task 1.7: *"Named session resumption using --resume <session-name>"* | `--resume <session-name>` (not `<session-id>`). |
| **Q29** | Task 1.7 / Appendix: bare term *`fork_session`* | plain `fork_session` (not `fork_session=True` on `query()`). |

The reverted explanations remain **shuffle-safe** (no option-letter references), and the answer key was re-rebalanced to a uniform A20 / B19 / C19 / D19.

**Net effect of the whole overhaul (what actually shipped):** answer key de-biased (was B50/D0), all explanations made shuffle-safe, runtime option shuffling — and **zero net changes to any exam-tested answer or terminology** (the four attempted changes were reverted to the syllabus).

**`data/exam.md`** was regenerated from the final `questions.json` so the human-readable study copy matches the runner.

# Doc-Grounded Validation Report

All 77 questions validated against the **official Claude Certified Architect – Foundations Exam Guide (v0.2, 2026-06-30)** as the authoritative source, with official Anthropic docs available as secondary confirmation. Method: one validator agent per question (citing the specific task-statement bullet) + adversarial verification on any flagged conflict. Calibration rule: **the Exam Guide wins over live product docs on any terminology drift** — the exam tests the guide, not the current product.

## Result

| Verdict | Count |
|---|---|
| **aligned** (keyed answer matches the guide) | **77 / 77** |
| conflict_with_guide | 0 |
| doc_drift_noted | 0 |
| not_in_guide / out-of-scope | 0 |
| needs_human | 0 |

- **Every keyed answer is correct per the Exam Guide.** No conflicts, nothing flagged for human review.
- The four questions reverted after the syllabus review (Q18, Q28, Q29, Q49) were each validated against their specific task statements:
  - **Q18** → Task 1.3 (`allowedTools` must include `"Task"`) ✓
  - **Q28** → Task 1.7 (`--resume <session-name>`) ✓
  - **Q29** → Task 1.7 (`fork_session` branches from a shared baseline) ✓
  - **Q49** → Task 3.5 (independent issues → sequential iteration; single message is for *interacting* issues) ✓

## Scope & honest caveats

- **This pass confirms guide-alignment, which is what determines exam-correctness — it is not an independent re-derivation from live docs.** The validators resolved every question from the distilled syllabus reference and did not need to fetch product docs (0 doc fetches), because the bank was reverse-engineered from this same guide and is internally consistent with it.
- **Known doc drift remains (informational only, does not affect exam answers):** the current SDK/docs express some concepts with newer wording than the frozen guide — e.g. forking via `fork_session=True` / `CLAUDE_CODE_FORK_SUBAGENT=1`, and structured outputs via the `structured-outputs-2025-11-13` beta header. The guide's wording is retained deliberately, because that is what the exam tests.
- If you ever want a *stronger* guarantee, a heavier pass could force every validator to fetch and quote the relevant official doc (not just the guide) — at materially higher cost — to catch any case where the guide itself might be outdated relative to the product.

## Bottom line

The bank is **internally consistent with the official Exam Guide across all 77 questions**, with the answer key de-biased (A20/B19/C19/D19), all explanations shuffle-safe, and no exam-tested content diverging from the syllabus.

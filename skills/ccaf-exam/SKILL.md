---
name: ccaf-exam
description: Interactive Claude Certified Architect Foundations practice exam. Presents questions one by one using AskUserQuestion, tracks answers, and gives a final scaled score (100-1000, pass at 720).
allowed-tools: Read, Glob, AskUserQuestion
argument-hint: "[number of questions, e.g. /ccaf-exam 20 — defaults to 20]"
---

# Claude Certified Architect Exam Runner

Run an interactive practice exam for the Claude Certified Architect – Foundations certification.

## Step 1: Load the question bank

Read the exam data file `questions.json` that ships alongside this skill. Resolve it in this order and use the first that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/ccaf-exam/questions.json`
2. `questions.json` in this skill's own directory (the directory this SKILL.md was loaded from)
3. If neither path is known, use Glob for `**/ccaf-exam/questions.json` and read the match.

The file is a JSON object:
- `questions`: array of question objects, each with:
  - `id` (int), `domain` (int 1–5), `domain_title` (string), `task` (string like `"1.4"`), `task_desc` (string)
  - `stem` (string — scenario + question, may contain multiple paragraphs)
  - `options` (array of 4 strings, in canonical order)
  - `correct_index` (int 0–3 — index into `options` of the correct answer)
  - `explanation` (string)
- `pass_scaled`: 720
- `domains`: map of domain number → title

If the file cannot be read, stop and report the error clearly. Do not attempt to reconstruct questions from memory.

## Step 2: Configure the session

Use ONE AskUserQuestion call with 3 questions:

**Question 1** — How many questions?
- header: "Questions"
- Options: "10 questions", "20 questions" (Recommended), "60 — full exam simulation", "All 149 (extra practice)"
- Note: the real certification exam is **60 questions in 120 minutes**, so "60" mirrors the actual exam length. "All 149" runs the entire community practice bank. Users can type any other number via "Other".

**Question 2** — Domain focus?
- header: "Domain"
- Options: "All domains" (Recommended), "D1: Agentic Architecture", "D2: Tool Design & MCP", "D3: Claude Code Config"
- Note: users who want D4 (Prompt Engineering) or D5 (Context Management) can type it via "Other".

**Question 3** — Feedback mode?
- header: "Feedback"
- Options: "After each question" (Recommended), "Summary at the end only"

Build the question queue from the choices:
- If a domain is selected, filter `questions` to those whose `domain` field matches (D1→1, D2→2, …).
- Shuffle the filtered list into a random order.
- Take the first N per the count chosen (cap at the number available; if fewer exist, use all and say so).

## Step 3: Run the exam

For each question in the queue:

1. **Shuffle the options for this question before displaying.** Randomize the order of the four `options` strings, and vary which slot (A/B/C/D) holds the correct one from question to question — never leave the correct answer stuck in one position across the exam. Track which displayed letter now corresponds to the option at `correct_index`. This defeats any position bias in the source data. NEVER show `correct_index` or the canonical order to the user.

2. Output a progress line: `**Question [current] of [total] | Score: [correct]/[answered so far]**`

3. Use AskUserQuestion with 1 question:
   - `question`: the `stem`. Keep it readable — if very long, trim to the most essential scenario + the question itself.
   - `header`: "Q[id]" (e.g., "Q13")
   - `multiSelect`: false
   - Options (exactly 4, labels A–D, in the shuffled order you chose in step 1):
     - label: "A", description: [shuffled option text]
     - label: "B", description: [shuffled option text]
     - label: "C", description: [shuffled option text]
     - label: "D", description: [shuffled option text]

4. Record the user's answer. It is correct if the letter they chose maps back to the option at `correct_index`.

5. If feedback mode is "After each question":
   - If correct: output `Correct.` then a brief (1–2 sentence) version of the explanation.
   - If incorrect: output `Incorrect. Correct answer: [letter as shown to the user]` then the explanation (2–3 sentences, focused on why the correct answer is right).

6. If feedback mode is "Summary at the end only": acknowledge briefly and move on with no answer reveal.

7. Continue to the next question. Do not use AskUserQuestion between questions for anything except the question itself.

## Step 4: Final score

After all questions are answered, calculate and display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   EXAM COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Raw score:     [correct] / [total] ([percent]%)
Scaled score:  [scaled] / 1000
Pass mark:     720 / 1000 (~69% correct)

Result:        PASS  /  FAIL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Scaled score formula: `round(100 + (correct / total) * 900)`. PASS when scaled ≥ 720.

Then show a domain breakdown (only for domains that appeared in this session):
```
Domain breakdown:
  D1 Agentic Architecture    [correct]/[total] ([%]%)
  D2 Tool Design & MCP       [correct]/[total] ([%]%)
  D3 Claude Code Config      [correct]/[total] ([%]%)
  D4 Prompt Engineering      [correct]/[total] ([%]%)
  D5 Context Management      [correct]/[total] ([%]%)
```

If feedback mode was "Summary at the end only", then list every missed question:
```
Questions you missed:
  Q[id]: Correct answer was "[the correct option text]". [1-sentence explanation]
  ...
```

End with a one-line note pointing to the weakest domain if any scored below 60%.

## Rules

- Never reveal the correct answer before the user selects an option.
- Never skip or truncate questions mid-exam.
- Keep all output outside of AskUserQuestion calls clean and brief. This is an exam, not a conversation.
- If the question bank cannot be loaded, stop and report the error — do not improvise questions.

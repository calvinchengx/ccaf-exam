#!/usr/bin/env python3
"""Validate the ccaf-exam skill package: frontmatter, data-path resolution, question-bank
invariants, and scoring-logic correctness. Run: python3 scripts/validate.py

Exit code 0 = all checks pass, 1 = at least one failure. This covers everything that can be
checked WITHOUT a human answering the interactive AskUserQuestion flow (see the behavioral
checklist in the README / conversation for the manual smoke tests).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "ccaf-exam", "SKILL.md")
QJSON = os.path.join(ROOT, "skills", "ccaf-exam", "questions.json")
LETTERS = ["A", "B", "C", "D"]
LR = re.compile(r"\bOption[s]?\s+[A-D]\b|(?<![A-Za-z])[A-D]\)", re.I)
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())

passed, failed = [], []
def check(name, ok, detail=""):
    (passed if ok else failed).append(name)
    print(f"  {'✅' if ok else '❌'} {name}" + (f" — {detail}" if detail and not ok else ""))

# ---------- 1. Frontmatter ----------
print("Frontmatter:")
fm = open(SKILL, encoding="utf-8").read().split("---", 2)[1]
fm_lines = dict(re.findall(r"^([a-z-]+):\s*(.*)$", fm, re.MULTILINE))
check("name is ccaf-exam", fm_lines.get("name") == "ccaf-exam", fm_lines.get("name"))
check("NO context: fork (must run in main loop for AskUserQuestion)", "context" not in fm_lines)
at = fm_lines.get("allowed-tools", "")
check("allowed-tools includes AskUserQuestion", "AskUserQuestion" in at, at)
check("allowed-tools includes Read", "Read" in at, at)
check("argument-hint present", "argument-hint" in fm_lines)

# ---------- 2. Data-path resolution ----------
print("Data path:")
check("questions.json co-located with SKILL.md (own-dir fallback resolves)", os.path.isfile(QJSON))
check("SKILL.md references the ccaf-exam/questions.json path",
      "ccaf-exam/questions.json" in open(SKILL, encoding="utf-8").read())

# ---------- 3. Question-bank invariants ----------
print("Question bank:")
d = json.load(open(QJSON, encoding="utf-8"))
qs = d["questions"]
check("count field matches array length", d.get("count") == len(qs), f"{d.get('count')} vs {len(qs)}")
check("pass_scaled == 720", d.get("pass_scaled") == 720)
check("domains map covers 1-5", set(int(k) for k in d.get("domains", {})) == {1, 2, 3, 4, 5})
req = {"id", "domain", "domain_title", "task", "stem", "options", "correct_index", "explanation"}
check("every question has all required keys", all(req <= set(q) for q in qs))
check("every question has exactly 4 options", all(len(q["options"]) == 4 for q in qs))
check("no duplicate options within a question", all(len(set(q["options"])) == 4 for q in qs))
check("all options are non-empty strings", all(all(isinstance(o, str) and o.strip() for o in q["options"]) for q in qs))
check("correct_index in 0..3", all(0 <= q["correct_index"] <= 3 for q in qs))
check("domain in 1..5", all(q["domain"] in (1, 2, 3, 4, 5) for q in qs))
check("explanations non-empty", all(q["explanation"].strip() for q in qs))
check("NO option-letter refs in explanations (shuffle-safe)", not any(LR.search(q["explanation"]) for q in qs),
      str([q["id"] for q in qs if LR.search(q["explanation"])][:10]))
check("stems are unique", len({norm(q["stem"]) for q in qs}) == len(qs))
ids = [q["id"] for q in qs]
check("ids unique", len(set(ids)) == len(ids))
check("every domain has >=1 question (domain filter never empty)",
      all(any(q["domain"] == dom for q in qs) for dom in (1, 2, 3, 4, 5)))

# ---------- 4. Scoring logic (as specified in SKILL.md Step 4) ----------
print("Scoring logic:")
def scaled(correct, total):
    return round(100 + (correct / total) * 900)
check("all-correct → 1000 PASS", scaled(60, 60) == 1000 and scaled(60, 60) >= 720)
check("all-wrong → 100 FAIL", scaled(0, 60) == 100 and scaled(0, 60) < 720)
check("42/60 (70%) → PASS", scaled(42, 60) >= 720, scaled(42, 60))
check("41/60 (68.3%) → FAIL", scaled(41, 60) < 720, scaled(41, 60))
# pass boundary is ~68.9% correct
boundary = next(p for p in range(0, 101) if scaled(p, 100) >= 720)
check("pass boundary ≈ 69% correct", boundary == 69, f"{boundary}%")

# ---------- 5. Report (non-failing) ----------
from collections import Counter
print("\nReport (informational):")
print("  answer key:", dict(sorted(Counter(LETTERS[q["correct_index"]] for q in qs).items())))
print("  per-domain:", dict(sorted(Counter(q["domain"] for q in qs).items())))
print("  total questions:", len(qs))

print(f"\n{'='*40}\n{len(passed)} passed, {len(failed)} failed")
if failed:
    print("FAILURES:", failed)
    sys.exit(1)
print("ALL CHECKS PASSED ✅")

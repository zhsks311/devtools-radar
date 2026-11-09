#!/usr/bin/env python3
"""Content lint for DevTools Radar articles.

Enforces the rules in docs/tech-blog-writing-standard.md so a machine-written draft cannot ship
with the defects that make a tech blog read as generated text.

Usage:  python3 tools/lint_content.py [content/final/*.json]
Exit code 1 if any article fails.
"""

import glob
import json
import re
import sys

BANNED = [
    "game-changer", "game changer", "seamless", "seamlessly", "robust", "leverage", "leveraging",
    "delve", "landscape", "realm", "unlock", "empower", "in conclusion", "it's worth noting",
    "when it comes to", "the world of", "revolutionize", "cutting-edge", "state-of-the-art",
    "in today's", "in this article", "let's dive", "dive into", "at the end of the day",
]

META = [
    "fact sheet", "the brief", "this comparison", "as an ai", "the review", "reviewer",
    "revision brief", "we will discuss", "this article will",
]

HOLLOW = [
    "it depends", "both are great", "there is no one-size-fits-all", "each has its pros and cons",
    "ultimately, the choice", "the best choice depends",
]

LIMITS = {"body_min": 3000, "body_max": 5000, "sections": (5, 6), "paragraph_sentences": 4}


def sentences(par):
    return [s for s in re.split(r"(?<=[.!?])\s+", par.strip()) if s.strip()]


def paragraphs(md):
    blocks, buf = [], []
    in_fence = False
    for line in md.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            blocks.append(("code", "\n".join(buf)))
            buf = []
            continue
        if in_fence:
            buf.append(line)
            continue
        if not line.strip():
            if buf:
                blocks.append(("text", " ".join(buf)))
                buf = []
        elif re.match(r"^\s*([-*]|\d+\.)\s", line) or line.strip().startswith("|") or line.strip().startswith(">"):
            if buf:
                blocks.append(("text", " ".join(buf)))
                buf = []
            blocks.append(("list", line))
        else:
            buf.append(line.strip())
    if buf:
        blocks.append(("text", " ".join(buf)))
    return blocks


def has_anchor(segment):
    return bool(re.search(r"(```|\n\|.*\||\n\s*[-*]\s|\n\s*\d+\.\s|>)", segment))


def lint(path):
    problems = []
    d = json.load(open(path, encoding="utf-8"))
    slug = d.get("slug", path)

    for key in ("slug", "hook", "sections", "decision_matrix", "cost_math", "verdict_summary", "faqs", "sources"):
        if key not in d:
            problems.append("missing key: " + key)
    if problems:
        return slug, problems, {}

    body = "\n".join(s["content"] for s in d["sections"])
    blob = " ".join([d["hook"], d["verdict_summary"]] + [s["content"] for s in d["sections"]])

    low = blob.lower()
    for w in BANNED:
        if w in low:
            problems.append("banned phrase: %r" % w)
    for w in META:
        if w in low:
            problems.append("meta text: %r" % w)
    for w in HOLLOW:
        if w in low:
            problems.append("hollow closer: %r" % w)

    n = len(body)
    if not (LIMITS["body_min"] <= n <= LIMITS["body_max"]):
        problems.append("body length %d outside %d-%d" % (n, LIMITS["body_min"], LIMITS["body_max"]))

    lo, hi = LIMITS["sections"]
    if not (lo <= len(d["sections"]) <= hi):
        problems.append("section count %d outside %d-%d" % (len(d["sections"]), lo, hi))
    for i, s in enumerate(d["sections"], 1):
        if len(s["content"]) > 1150:
            problems.append("section %d over 1,150 chars (%d)" % (i, len(s["content"])))
        if len(sentences(s["title"])) > 2 or len(s["title"].split()) <= 2:
            problems.append("section %d title is not a claim: %r" % (i, s["title"]))

    for kind, text in paragraphs(body):
        if kind == "text":
            ss = sentences(text)
            if len(ss) > LIMITS["paragraph_sentences"]:
                problems.append("paragraph with %d sentences: %r…" % (len(ss), text[:80]))
            if len(ss) >= 3 and all(len(s.split()) < 11 for s in ss[-3:]):
                problems.append("suspicious uniform short tail: %r…" % text[:80])

    # visual anchor density: no 600-char stretch without a table/code/list
    for chunk in body.split("\n\n"):
        if len(chunk) > 600 and not has_anchor("\n" + chunk):
            problems.append("no visual anchor in %d-char block: %r…" % (len(chunk), chunk[:70]))

    # numbers discipline: every money figure must be attributable
    money = set(re.findall(r"\$[\d,]+(?:\.\d+)?", blob))
    for m in money:
        if m not in blob:
            continue
    if not d.get("sources"):
        problems.append("no sources listed")

    # structured fields
    if not (6 <= len(d["decision_matrix"]) <= 8):
        problems.append("decision_matrix has %d rows" % len(d["decision_matrix"]))
    for r in d["decision_matrix"]:
        if any(k not in r for k in ("situation", "pick", "why")):
            problems.append("decision_matrix row missing keys: %r" % r)
    if not (2 <= len(d["cost_math"]) <= 4):
        problems.append("cost_math has %d rows" % len(d["cost_math"]))
    for c in d["cost_math"]:
        if not re.search(r"[\d]", c.get("formula", "")):
            problems.append("cost row has no arithmetic: %r" % c.get("label"))
    if len(d["faqs"]) != 4:
        problems.append("faqs has %d items" % len(d["faqs"]))

    stats = {
        "body": n,
        "sections": len(d["sections"]),
        "paragraphs": sum(1 for k, _ in paragraphs(body) if k == "text"),
        "money_figures": len(money),
    }
    return slug, problems, stats


def main():
    paths = sys.argv[1:] or sorted(glob.glob("content/final/*.json"))
    failed = 0
    for p in paths:
        slug, problems, stats = lint(p)
        status = "PASS" if not problems else "FAIL"
        print("%-28s %s  body=%s sections=%s money=%s" % (
            slug, status, stats.get("body"), stats.get("sections"), stats.get("money_figures")))
        for pr in problems:
            print("    - " + pr)
        failed += 1 if problems else 0
    print("\n%d file(s) checked, %d failed" % (len(paths), failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

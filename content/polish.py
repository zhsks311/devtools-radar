#!/usr/bin/env python3
"""Final editorial pass: restore the hooks the revisions flattened, and fix clunky openers.

Each edit is (old, new). Missing old strings are reported so the patch never silently no-ops.
"""

import json
import os

BASE = "/workspace/devtools-radar/content/final"

EDITS = {
    # Supabase final article owns corrected Realtime billing; no legacy overwrite.

    "vercel-vs-cloudflare-pages": {
        "hook": "Both hosts now meter CPU time, so an idle `await` is free on either and paying for idle time no longer separates them. What separates them is transfer and requests on Vercel — 3 TB a month adds 2,048 GB × $0.15 = $307.20 — against CPU milliseconds on Cloudflare, where egress costs $0.",
        "replace": [
            (
                "confirm an existing project actually runs on it. An idle",
                "An idle",
            ),
            (
                "> Vercel Pro includes no CPU; Workers Paid includes 30M CPU-ms a month.",
                "> Workers Paid includes 30M CPU-ms a month; Vercel bills Active CPU and provisioned memory as separate metered lines.",
            ),
            (
                "Vercel Pro includes no CPU\n",
                "",
            ),
        ],
        "verdict": None,
        "drop_matrix": ["A request handler that runs longer than 5 minutes"],
    },

    "cursor-vs-github-copilot": {
        "hook": "The $20 all-you-can-eat AI editor is gone, and its replacement is an $8 tier that only runs Grok and a $30 tier where Claude and GPT tokens bill on top. Both Cursor and GitHub Copilot are now agent-first and credit-metered, and each one restricts its entry tier in a different place.",
        "replace": [
            (
                "That rules out treating cheap access as a neutral model buffet.",
                "Cheap access to other vendors' models is not part of the deal.",
            ),
            (
                "Cursor is contesting that ground: Premium lists",
                "Cursor pushes back on that line: Premium lists",
            ),
        ],
        "verdict": None,
    },

    "notion-vs-obsidian": {
        "hook": "On Notion Free, page history stops at 7 days; Business keeps 90, and an Obsidian vault under git has no plan-imposed cutoff at all. For ten people that is 10 × $20 × 12 = $2,400/year of Notion Business against 10 × $4 × 12 = $480/year of Sync, and the difference buys a permission model you either need or do not.",
        "replace": [
            (
                "For engineers choosing a notes app or team workspace, buy for recovery and access requirements: vendor pricing and official documentation, verified 2026-11-10.",
                "**Obsidian sells a folder.** Plain Markdown on your disk, no server, no meter, and the app itself is free without limits. **Notion sells shared state.** Permissions, databases and agents live on their servers, and everything around them carries a budget: page history, uploads, API calls, agent credits.",
            ),
            (
                "## The bill for 10 people: who should not pick Notion Business",
                "## For ten people, $2,400 a year buys permissions or it buys nothing",
            ),
        ],
        "verdict": None,
    },
}

for slug, spec in EDITS.items():
    path = os.path.join(BASE, slug + ".json")
    d = json.load(open(path, encoding="utf-8"))
    d["hook"] = spec["hook"]
    body = "\n".join(s["content"] for s in d["sections"])
    for old, new in spec["replace"]:
        hits = 0
        for s in d["sections"]:
            if old in s["content"]:
                s["content"] = s["content"].replace(old, new)
                hits += 1
        if hits == 0:
            print("  MISS [%s]: %r" % (slug, old[:70]))
    if spec.get("verdict"):
        d["verdict_summary"] = spec["verdict"]
    for drop in spec.get("drop_matrix", []):
        before = len(d["decision_matrix"])
        d["decision_matrix"] = [r for r in d["decision_matrix"] if r["situation"] != drop]
        if len(d["decision_matrix"]) == before:
            print("  MISS matrix drop [%s]: %r" % (slug, drop))
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    body = "\n".join(s["content"] for s in d["sections"])
    print("%-28s body=%d sections=%d matrix=%d" % (slug, len(body), len(d["sections"]), len(d["decision_matrix"])))

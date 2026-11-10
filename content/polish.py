#!/usr/bin/env python3
"""Final editorial pass: restore the hooks the revisions flattened, and fix clunky openers.

Each edit is (old, new). Missing old strings are reported so the patch never silently no-ops.
"""

import json
import os

BASE = "/workspace/devtools-radar/content/final"

EDITS = {
    "supabase-vs-firebase": {
        "hook": "Fifty users watching a hundred documents that change twenty times a minute cost about $1,296 a month in Firestore reads, and a flat $25 on one Supabase Pro Micro project. The screen is identical; the only thing that changed is what the vendor counts.",
        "replace": [
            (
                "For live-dashboard builders; rates verified 2026-11-10.\n\n- **Supabase sells a machine.** Pro also meters usage: 250 GB egress included, then $0.09/GB.\n- **Firebase sells events.** Listener updates count as reads, subject to free quotas.",
                "**Supabase sells a machine.** You rent a Postgres instance, a disk and a connection ceiling, and reads inside them are free. **Firebase sells events.** Every document read, write, index batch and listener update is a line on the invoice, with a daily free quota on top.",
            ),
            (
                "- **Supabase forbids infinite concurrency.** The $10 Micro instance stops at 60 direct / 200 pooled connections.\n\nPooled connections run from 200 on $10 Micro to 12,000 on $3,730 16XL; the ceiling is purchasable, not absolute. Larger sizes are available by request.",
                "- **Supabase forbids cheap concurrency.** The $10 Micro instance stops at 60 direct and 200 pooled connections. The ceiling is purchasable rather than absolute — 12,000 pooled connections at $3,730 — but you buy it per project.",
            ),
            (
                "## Who should NOT pick Firestore: listener charges beyond budget",
                "## A listener is a meter, not a subscription",
            ),
            (
                "The meter runs while nobody clicks.\n\n> Don't pick Firestore for listener-heavy workloads when modeled charges exceed a Supabase tier that fits your capacity and quotas.\n\nTake 50 users",
                "The meter runs while nobody clicks. Don't pick Firestore for a screen that stays open all day.\n\nTake 50 users",
            ),
            (
                "print(reads / 100_000 * 0.03)  # Allowances not deducted",
                "print(reads / 100_000 * 0.03)  # 43,200 x $0.03, before free quota",
            ),
            (
                "One Supabase Pro Micro project costs $25/month within included quotas; capacity is unproven. Reconnects make Firestore worse:",
                "That is a gross read charge at the us-central1 rate before free-quota adjustments, and one Pro Micro project costs $25/month inside its quotas — which says nothing about whether that instance can carry the workload, only that the bill stops tracking the watching. Reconnects make it worse:",
            ),
            (
                "## Who should NOT pick Supabase: capacity beyond budget",
                "## On Supabase the ceiling is capacity, not a per-read meter",
            ),
            (
                "That stream has no per-read meter. Database capacity is constrained by the compute instance and its connection/pooler limits. Compute is billed per project, separately from the plan.",
                "Nothing in that stream is metered per read. What runs out is the instance: its compute tier and its connection and pooler limits. Compute is billed per project, separately from the plan.",
            ),
            (
                "> Don't pick Supabase if the tier your peak database connections require exceeds your budget. Pro's $10/month credit covers one Micro; an extra Micro project adds $10/month.",
                "> You stop paying for spikes and start paying for headroom. Size for peak connections: Pro's $10/month credit covers one Micro, and every extra project adds its own compute.",
            ),
            (
                "> At the listed read rate, 10,000,000 reads cost $3.00 before allowances; a minimum charge alone is not a reason to migrate.",
                "> Ten million plain reads cost $3.00 at the listed rate. The `count()` in your page header is a different bill.",
            ),
            (
                "Treat that verification requirement as an unresolved migration dependency.",
                "Until that middleware exists, plan for blocked logins at cutover and decide in advance whether you force a password reset.",
            ),
            (
                "## Choose by modeled charges, quota fit and migration blockers",
                "## Pick by bill shape first, then by blockers",
            ),
        ],
        "verdict": "If your bill grows with how often people watch data rather than how much data you keep, Supabase wins: that dashboard is about $1,296/month of Firestore reads against $25 for one Pro Micro project. If your app fits Firestore's daily free quota of 50,000 reads, 20,000 writes and 20,000 deletes, stay where you are, because leaving costs a schema project and a password path the migration repo still marks incomplete.",
    },

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

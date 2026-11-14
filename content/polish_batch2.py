#!/usr/bin/env python3
"""Editorial polish for the batch-2 articles: restore the hooks and verdicts the review pass flattened.

Each edit is (old, new); a missing old string is reported so the patch never silently no-ops.
"""

import json
import os

BASE = "/workspace/devtools-radar/content/final"

EDITS = {
    "bun-vs-node": {
        "hook": (
            "Bun's own test count says node:http passes 403 of 415 tests, and Node's own calendar says "
            "v20 died on 24 March 2026. Neither runtime charges a cent, so the bill arrives somewhere "
            "else."
        ),
        "verdict": (
            "Pick Node if your service needs an API Bun documents as missing — getPeerCertificate(), "
            "SNICallback, createHook with real async ids — or if a native addon in your tree has no "
            "build for NODE_MODULE_VERSION 147. Pick Bun if the addons and APIs you depend on survive "
            "its 403-of-415 node:http count, because the runtime itself will never appear on an invoice."
        ),
        "replace": [
            (
                "> Retain the Node runtime and its required addon builds if you need to return to Node.\n\n",
                "",
            ),
            (
                "**Teams maintaining a Node service should retain Node if required APIs are missing in Bun; teams choosing bundled script tooling can pick Bun after compatibility checks.**\n\nCheck today:",
                "The acquisition changes who pays for Bun's roadmap. It does not change the licence, and it does not change the API surface you have to test.\n\nCheck today:",
            ),
        ],
    },
    "docker-vs-podman": {
        "hook": (
            "Docker Desktop is free at 249 employees and paid at 250: 200 developers × $15 = "
            "$3,000/month for the same binary. Podman has no seat price at all, which is why the real "
            "comparison is not daemon versus daemonless but which company may run the free one."
        ),
        "verdict": (
            "Pick Podman if your company sits under both free-use limits and you can fund the port, or "
            "if you are past them and want per-seat × headcount off the budget. Pick Docker if SSO, "
            "SCIM and Image Access Management have to arrive in one contract, or if Build Cloud minutes "
            "belong on the same invoice as the desktop."
        ),
        "replace": [
            (
                "- Podman's own pages sell no central admin controls; enterprise support arrives as a Red Hat build.",
                "- Podman Desktop's enterprise path is that Red Hat build: support and long-term maintenance, not a licence tier.",
            ),
        ],
    },
    "clerk-vs-auth0": {
        "verdict": (
            "Pick Clerk if most of your sign-ups never come back a second day, because Clerk bills only "
            "the ones who do — 50,000 MRU are included on a $25/month Pro plan. Pick Auth0 if your "
            "identity programme runs on enterprise SSO, many tenants and custom connections, and budget "
            "for the step: 501 B2C users cost $70 on Essentials, the same as 1,000."
        ),
    },
    "prisma-vs-drizzle": {
        "verdict": (
            "Pick Drizzle if a generated client is the thing you refuse to add and you can pin "
            "1.0.0-rc.5 having read its breaking notes. Pick Prisma if the generator is fine and you may "
            "want Prisma Postgres and Prisma Compute on the same bill, where the operation meter meets "
            "Pro at 5.875M queries; neither ORM will ever appear on an invoice."
        ),
    },
    "planetscale-vs-neon": {
        "verdict": (
            "Pick Neon if your databases sleep: suspended compute costs $0, and a branch per pull "
            "request costs $1.50 a month instead of a cluster. Pick PlanetScale if production must stay "
            "awake on a fixed cluster charge, or you already run Vitess-shaped MySQL — and test Neki "
            "outside production only, because its preview excludes it."
        ),
        "replace": [
            (
                "1 primary and 2 replicas across 3 availability zones. Neki is a platform preview, not production.",
                "1 primary and 2 replicas across 3 availability zones.",
            ),
            (
                "- Routers start at $6 (NKR-0). Neki is a platform preview, not production. Production router compute",
                "- Routers start at $6 (NKR-0). Production router compute",
            ),
            (
                "= $370/month, before storage, backups and network usage. Neki is a platform preview, not production.",
                "= $370/month, before storage, backups and network usage.",
            ),
        ],
    },
}

missing = []
# Reviewed final articles own these corrected claims; never restore legacy copy.
for _reviewed_slug in ('docker-vs-podman', 'clerk-vs-auth0', 'cursor-vs-github-copilot', 'bun-vs-node'):
    EDITS.pop(_reviewed_slug, None)

for slug, spec in EDITS.items():
    path = os.path.join(BASE, slug + ".json")
    d = json.load(open(path, encoding="utf-8"))
    if "hook" in spec:
        d["hook"] = spec["hook"]
    if "verdict" in spec:
        d["verdict_summary"] = spec["verdict"]
    for old, new in spec.get("replace", []):
        hit = False
        for s in d["sections"]:
            if old in s["content"]:
                s["content"] = s["content"].replace(old, new)
                hit = True
        for key in ("migration_guide",):
            pass
        if not hit:
            missing.append((slug, old[:60]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    body = "".join(s["content"] for s in d["sections"])
    print("%-24s body=%d" % (slug, len(body)))

print("missing:", missing)

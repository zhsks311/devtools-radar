# FACT SHEET — Supabase vs Firebase (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. If something is not here, either omit it or
write it as a qualitative statement with no number. Never invent a tool, CLI flag, price or benchmark.

## Supabase (source: https://supabase.com/pricing)

Free — $0
- 500 MB database per project, 5 GB egress, 5 GB cached egress, 1 GB file storage
- 50,000 MAU, unlimited API requests
- limit of 2 active projects; **Free projects are paused after 1 week of inactivity**

Pro — from $25/month
- 8 GB disk per project included, then $0.125/GB
- 250 GB egress included, then $0.09/GB; 250 GB cached egress, then $0.03/GB
- 100 GB file storage included, then $0.0213/GB
- 100,000 MAU included, then $0.00325/MAU
- daily backups kept 7 days, log retention 7 days, projects never paused for inactivity
- plan includes $10/month of compute credits = one Micro instance

Compute (billed per project, separately from the plan):
- Micro $10 — shared, 1 GB RAM, 60 direct connections / 200 pooler connections
- Small $15 — shared, 2 GB RAM, 90 / 400
- Medium $60 — shared, 4 GB RAM, 120 / 600
- Large $110 — dedicated 2 vCPU, 8 GB RAM, 160 / 800
- XL $210 — dedicated 4 vCPU, 16 GB RAM, 240 / 1,000

Official billing example: "a Pro org with 2 projects on Micro compute costs: $25 (plan) + $10 (project 1)
+ $10 (project 2) − $10 (credits) = $35/month."
⇒ Derived: one Pro project on Micro = $25/month all-in. Every extra project adds its compute cost.

Team $599/month, Enterprise custom — not relevant to this article.

Realtime (source: https://supabase.com/docs/guides/realtime/postgres-changes)
- "Postgres Changes" streams database events by adding tables to the `supabase_realtime` publication
  (`alter publication supabase_realtime add table your_table_name;`) — opt-in per table.
- Subscriptions are RLS-aware: clients receive rows they are allowed to select.
- Supabase's own docs also document Broadcast as the way to subscribe to database changes
  (docs link: .../realtime/subscribing-to-database-changes#using-broadcast).

## Firestore / Firebase (source: https://firebase.google.com/docs/firestore/pricing, https://cloud.google.com/firestore/pricing)

Free quota per day: 1 GiB stored, 50,000 document reads, 20,000 writes, 20,000 deletes,
10 GiB/month outbound transfer. Exactly ONE free database per project.

Paid rates, us-central1 default (per 100,000 documents):
- reads $0.03 · writes $0.09 · deletes $0.01
- TTL deletes $0.01 per 100,000

Index entry reads (verified, this is the part nobody quotes):
- one read per batch of up to 1,000 index entries read by a query
- kNN vector search: one read per batch of up to 100 vector index entries
- queries with up to ONE range field are NOT charged for index entries; a second range field starts billing
- `count()`/`sum()`/`avg()` bill index reads; a query reading 0 index entries has a 1-document-read minimum
  (example from docs: count() over 1,500 index entries = 2 document reads)
- `offset` bills a read per skipped document (offset 10 returning 1 doc = 11 reads)

Realtime listeners are billed as reads:
- one read each time a document is added to or updated in the result set of an active listener
- also one read when a document is removed from the result set because it changed
- offline persistence ON and disconnected >30 min ⇒ next reconnect billed like a brand-new query
- offline persistence OFF ⇒ every reconnect billed like a brand-new query

Worked arithmetic you may reuse (show the formula, do not present as a measured benchmark):
- 10,000,000 reads = 100 × 100,000 ⇒ 100 × $0.03 = $3.00
- 50 concurrent dashboard users, each listening to 100 documents that change 20 times/minute:
  50 × 100 × 20 × 60 × 24 × 30 ≈ 4.32 billion read events/month ≈ 43,200 × $0.03 ≈ $1,296/month
- same shape on Supabase Pro: $25/month (Micro) regardless of read volume inside the quota

## Migration reality (source: https://supabase.com/kb/guides/migrate-from-firestore-data, .../migrate-from-firebase-auth)

- Tooling: `supabase-community/firebase-to-supabase` (GitHub), scripts `firestore2json.js` and
  `json2supabase.js`; auth path uses `firestoreusers2json` + `import_users`.
- Scope: "copies the entire contents of a single Firestore collection to a single Postgres table" and the
  collection is "flattened" to columns of type text / numeric / boolean / jsonb.
- You write custom hooks to split nested JSON into related tables — i.e. schema design is your job.
- `json2supabase.js` takes a primary-key strategy: none / smallserial / serial / bigserial / uuid / firestore_id.
- Auth: passwords are migrated by hash-parameter import (base64_signer_key, base64_salt_separator, rounds,
  mem_cost — Firestore's SCRYPT params); verifying a user's existing Firebase password on first login needs
  a middleware component that the repo itself marks WORK IN PROGRESS (AWS Lambda variant listed as TBD).

## Do not claim
- No official "firestore-to-supabase CLI".
- Do not state an exact Firestore storage price per GB-month.
- Do not state measured cold-start milliseconds or query latency for either product.

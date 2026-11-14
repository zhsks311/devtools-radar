# Supabase / Firestore Realtime correction — 2026-11-14

Authoritative current article: content/final/supabase-vs-firebase.json. Prior flat-$25 fan-out conclusion withdrawn.

Two billing models, both with usage meters
Correction, November 14, 2026: this article previously treated Supabase Postgres Changes as unmetered and compared a high-fan-out workload with a flat $25 project. Supabase bills Realtime Messages separately from database compute, so that conclusion is withdrawn.

A database query and delivery of a Realtime change are different billing events. Supabase combines plan, compute and usage charges; Firestore Standard meters document operations, among other items.

| Meter | Published unit | Scope |
|---|---|---|
| Firestore Standard reads | $0.03/100,000 | us-central1, not every edition or region |
| Firestore Standard writes | $0.09/100,000 | Same regional model |
| Supabase Realtime | 5M messages included on Pro, then $2.50/M | Organization allowance; excess rounded up in 1M packages |
| Supabase Pro Micro base | $25 + $10 − $10 credit | One project, excludes usage overage |

Model deliveries before comparing prices
Assume 50 clients continuously watch the same 100 documents; every document changes 20 times/minute for 30 days. Each change reaches all 50 clients, with no coalescing, filtering or missed deliveries.

50 × 100 × 20 × 60 × 24 × 30 = 4.32 billion deliveries. Firestore Standard read-only gross cost at the stated rate is $1,296. This is arithmetic, not a load-test result.

Firestore bills listener additions and updates, plus removals caused by document changes; deleting a document does not itself add a listener read. Reconnects can reissue billed queries: always with offline persistence disabled, or after more than 30 minutes disconnected with it enabled.

Initial reads, reconnects, security-rule and index reads, storage, transfer and taxes are omitted. The underlying 86.4M updates would also incur writes: $77.76 gross at $0.09/100,000. Daily free quotas must be applied by day; unused quota is not a monthly pool.

Supabase messages, spend caps and throughput are separate
Postgres Changes counts one message per receiving client: one change delivered to 50 clients means 50 messages. Broadcast also counts the send plus each receiving client; Presence has its own traffic, so do not substitute one meter for another.

At 4.32B delivered messages, ceil((4.32B − 5M)/1M) × $2.50 = $10,787.50 overage. Adding the illustrative $25 Pro Micro base gives $10,812.50, before extra compute, egress, connections or other usage.

The model averages 1,666.7 deliveries/s. Published Pro limits are 500 messages/s, or 2,500/s for Pro without a spend cap; peak connections are 500 or 10,000 respectively. These are Realtime limits, not database pooler connections.

A spend cap covers Realtime quota overage: leaving it on can restrict service, not grant unlimited free delivery. Turning it off permits charges but does not remove throughput limits or prove capacity; validate burst load, payloads, RLS work and actual project settings.

Sources
https://supabase.com/pricing
https://supabase.com/docs/guides/realtime/postgres-changes
https://firebase.google.com/docs/firestore/pricing
https://cloud.google.com/firestore/pricing
https://supabase.com/kb/guides/migrate-from-firestore-data
https://supabase.com/docs/guides/platform/manage-your-usage/realtime-messages
https://supabase.com/docs/guides/realtime/limits
https://supabase.com/docs/guides/platform/cost-control
https://firebase.google.com/docs/firestore/compare-editions-for-native-mode

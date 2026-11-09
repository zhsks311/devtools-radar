# FACT SHEET — PlanetScale vs Neon (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Prices are AWS us-east-1 list prices from each vendor's own page, generated/updated 2026-11-09 and
2026-11-04. Some PlanetScale rates are published only through a rate endpoint; do not invent them.

## PlanetScale (sources: https://planetscale.com/pricing, https://planetscale.com/docs/postgres/pricing,
https://planetscale.com/docs/planetscale-plans, https://planetscale.com/blog/introducing-neki,
https://planetscale.com/changelog/neki)

Plans
- There is no free plan. PlanetScale's docs: "PlanetScale does not offer a free plan, previously known
  as the 'Developer' or 'Hobby' plan. All databases require a paid subscription starting with our Base
  plan."
- Single-node Postgres starts at $5/month.
- Price components: for Postgres — cluster size + storage (EBS) + backups + egress + optional
  dedicated PgBouncer + optional additional replicas; for Neki — shard compute + routers + network
  storage + backups + network usage; for Vitess — cluster size + storage + optional VTGates +
  replicas/sharding.
- Every branch runs on its own dedicated cluster and is billed separately, prorated to the
  millisecond.

Postgres SKUs (monthly, arm64 / x86-64 where they differ)
- HA, 3-node (1 primary + 2 replicas): PS-5 (1/16 vCPU, 512 MiB) $15; PS-10 (1/8, 1 GiB) $30 / $39;
  PS-20 (1/4, 2 GiB) $50 / $59; PS-40 (1/2, 4 GiB) $83 / $99; PS-80 (1, 8 GiB) $148 / $179;
  PS-160 (2, 16 GiB) $286 / $349; PS-320 (4, 32 GiB) $570 / $699; PS-640 (8, 64 GiB) $1,135 / $1,399;
  PS-1280 (16, 128 GiB) $2,265 / $2,799; PS-2560 (32, 256 GiB) $4,529 / $5,599.
- Single node (non-HA): PS-5 $5; PS-10 $10 / $13; PS-20 $17 / $20; PS-40 $28 / $33; PS-80 $50 / $60;
  PS-160 $96 / $117; PS-320 $190 / $233.
- Metal, 3-node, with local NVMe included: M-10 (1/8, 1 GiB, 10 GiB) $50 arm / $60 x86; M-40 with
  400 GiB $330 arm.

Neki — sharded Postgres (announced 11 Aug 2025; platform preview 10 Sep 2026)
- Sharded Postgres: application connects to a Neki router over the standard Postgres wire protocol, so
  existing drivers, ORMs and connection strings keep working; each shard is a real Postgres cluster
  with 1 primary and at least 2 replicas across 3 availability zones.
- "Neki has no single-node configuration." Shard compute = HA SKU rate × shards on the profile;
  extra replicas bill at the additional-replica rate.
- Neki standard 3-node SKUs (arm64 / x86-64): PS-10 $30 / $39; PS-20 $50 / $59; PS-40 $83 / $99;
  PS-80 $148 / $179; PS-160 $286 / $349; PS-320 $570 / $699; PS-640 $1,135 / $1,399.
- Routers: NKR-0 $6, NKR-1 $11, NKR-2 $22, NKR-5 $50, NKR-10 $90, NKR-20 $170, NKR-80 $680.
  Every Neki branch has at least one router group; the production router rate covers a three-router
  baseline (one per AZ): production router compute = router rate × observed routers ÷ 3.
- Resharding, schema changes, version upgrades and failovers are online workflows; you can start
  unsharded and reshard later.
- Platform preview is explicitly not for production workloads ("some of those changes will be
  breaking").

Vitess (MySQL) SKUs (monthly, x86-64, 3-node non-metal)
- PS-10 $39; PS-20 $59; PS-40 $99; PS-80 $179; PS-160 $349; PS-320 $699; PS-640 $1,399;
  PS-1280 $2,799; PS-2560 $5,599; PS-2800 $7,199.

Included allowances and metered rates (from the Postgres pricing doc)
- Storage: 10 GB included per instance; beyond that the region's volume rate applies, fetched from
  `/www/storage-rates` (not printed). HA clusters use the configured volume on the primary and both
  replicas. On the Base plan, production-branch storage is billed at $1.50/GB (1 primary + 2
  replicas) and development-branch storage at $0.50/GB.
- Backups: automated every 12 hours; backup and WAL storage included up to 2x disk size; overage
  $0.023 per GB-month, billed on the compressed size.
- Egress: production branch 100 GB/month included, PS-5 non-HA and development branches 10 GB/month;
  beyond that the region egress rate applies (fetched from `/www/egress-rates`, not printed). Ingress
  is free. Private connections (AWS PrivateLink, GCP Private Service Connect) are a flat $0.01/GB in
  both directions.
- Cross-region dedicated read replica traffic: streaming $0.04/GB in US regions, up to $0.16/GB in
  sa-east-1; archive and bootstrap $0.03/GB in US regions.
- IOPS and throughput above the included baselines (3,000 IOPS / 125 MiB/s on AWS gp3) are charged at
  dashboard-only rates.

## Neon (source: https://neon.com/pricing, updated 2026-11-04)

Positioning
- "A complete set of cloud backend primitives built around Lakebase Postgres ... from Databricks."
  Services: Lakebase Postgres, Managed Better Auth, Data API, Functions, Object Storage, AI Gateway.
- Plans: Free, Launch, Scale. Paid plans are pay-as-you-go, metered hourly, no monthly minimum, no
  per-project fee. The Free plan is permanent, no card. Invoices under $0.50 are not collected.

Units
- CU (Compute Unit) ≈ 4 GB RAM + CPU + SSD. CU-hour = compute size × hours running
  (0.25 CU × 4 h = 1 CU-hour). Suspended compute is $0.
- Storage in GB-months, metered hourly. Extra branch = branch-month, prorated hourly.

Free plan
- 100 CU-hours per project, 1 GB Postgres storage per project (20 GB across the account),
  100 projects, 10 branches per project, autoscaling up to 2 CU (8 GB RAM), scale to zero after
  5 minutes and it cannot be disabled, 5 GB egress per project, 6-hour history window (1 GB limit),
  1 manual snapshot, Auth up to 60,000 MAU per project, 5 GB object storage per project, 1M function
  invocations, 1-day monitoring retention.

Launch
- $0.106 per CU-hour. Autoscaling up to 16 CU (64 GB RAM). Scale to zero after 5 minutes, can be
  disabled. Storage $0.35/GB-month. Instant restore $0.20/GB-month. 10 branches per project
  (up to 5,000 per project on paid plans), extra branch $1.50/branch-month. History up to 7 days.
  500 GB egress per project included, then $0.10/GB. Up to 10,000 pooled connections per compute.
- Includes pgvector, PostGIS, TimescaleDB; Data API over HTTP; Object Storage $0.023/GB-month;
  Functions $0.10 per active Capacity-Hour, $0.025 per waiting Capacity-Hour, $0.60 per million
  invocations; AI Gateway with prepaid credits; Realtime in beta (free during beta); 3-day
  monitoring retention; spending notifications; protected branches. No SLA.

Scale
- $0.222 per CU-hour. Up to 16 CU autoscaling or fixed sizes up to 56 CU (224 GB RAM). Scale to zero
  configurable from 1 minute to always on. 25 branches. History up to 30 days. Private networking
  $0.01/GB; object storage and functions priced slightly higher ($0.12 active Capacity-Hour);
  SOC 2, ISO 27001/27701, GDPR/CCPA, HIPAA self-serve with a BAA, uptime SLA, metrics/logs export.

Neon's own typical monthly costs (Postgres compute + storage only)
- Intermittent load, 140 CU-hours + 1 GB: $15 on Launch, $31 on Scale.
- Low load, 190 CU-hours + 5 GB: $22 on Launch, $44 on Scale.
- Medium load, 720 CU-hours + 10 GB: $80 on Launch, $163 on Scale.
- High load, 3,000 CU-hours + 100 GB: $353 on Launch, $701 on Scale.
- XL load, 6,000 CU-hours + 1 TB: $1,682 on Scale (not listed for Launch).

## Derived arithmetic you may use (show the formula in the text)

- Always-on small database on Neon Launch: 0.25 CU × 730 h = 182.5 CU-hours × $0.106 = $19.35/month
  before storage, versus PlanetScale PS-5 HA at $15/month flat — the machine you never sleep is
  cheaper as a rental; the machine you sleep most of the day is cheaper as CU-hours.
- Same shape on Neon Scale: 182.5 × $0.222 = $40.52/month.
- One CU running all month on Launch: 1 × 730 = 730 CU-hours × $0.106 = $77.38; on Scale
  730 × $0.222 = $162.06.
- Branch sprawl: 20 branches on Neon Launch = 10 included + 10 × $1.50 = $15/month of branch storage.
  On PlanetScale a branch is its own cluster, so 20 PS-5 HA branches = 20 × $15 = $300/month,
  prorated to the millisecond.
- Storage at 100 GB on Neon Launch: 100 × $0.35 = $35/month. PlanetScale PS-5 HA includes 10 GB per
  instance, so 100 GB costs the region volume rate on three nodes — more than one volume's worth.
- Egress at 1 TB (1,024 GB) on Neon Launch: 1,024 − 500 = 524 GB over × $0.10 = $52.40/month. PlanetScale's
  production branch includes 100 GB and then bills the region rate, which is not printed.
- Four Neki shards of PS-20 plus the three-router baseline: 4 × $50 = $200 + 1 × $170 = $370/month
  before storage and backups, for 16 GiB of RAM across shards with two replicas each.

## Do not claim
- Do not claim PlanetScale has a free tier; it explicitly does not.
- Do not print a PlanetScale storage or egress dollar rate that is not in this sheet; those rates are
  region-dependent and published through endpoints.
- Do not claim Neki is generally available or production-ready; it is a platform preview and
  PlanetScale says not to run production on it.
- Do not claim Neon is a standalone company or "Neon by Vercel"; the pricing page says Databricks.
- Do not claim PlanetScale's own price is "cheaper than Neon" in general — it depends on idle hours;
  give the shape, not a slogan.
- Do not invent availability zones, regions or replicas beyond the counts above.
- Do not claim Vitess and Postgres behave identically on PlanetScale; Vitess is the MySQL product.

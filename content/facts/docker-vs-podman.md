# FACT SHEET — Docker vs Podman (verified 2026-11-10)

Rules: use ONLY numbers and product names from this sheet. Derived arithmetic must show its formula.
Podman has no price sheet; Docker's licence threshold is the centre of this article. Do not invent a
Docker Business list price — the pricing page shows "Contact us" and only Pro and Team print a number.

## Docker (sources: https://www.docker.com/pricing/, https://docs.docker.com/subscription-billing/desktop-license/,
https://docs.docker.com/subscription-billing/plans/docker/)

Prices on the pricing page (USD, per user per month)
- Docker Personal — $0.
- Docker Pro — $9.
- Docker Team — $15.
- Docker Business — no number on the page; it says "Contact us for pricing".
- Docker Hardened Images (DHI) — free for every developer; "Starting at $5k/repo" for production use
  with compliance support; enterprise DHI is quote-only and is required for end-of-life software
  security.
- Docker Premium Support and TAM is an add-on to Business and DHI.

Who must pay (Docker Desktop licence agreement, docs.docker.com)
- Free for: small businesses with **fewer than 250 employees AND less than $10 million in annual
  revenue**; personal use; education; non-commercial open source.
- A paid subscription is required for: professional use in larger organizations, government entities,
  and commercial use beyond the free tier.
- Plans that include Docker Desktop: Docker Pro, Team, Business.
- The licensing and distribution terms of Docker Engine and Moby do not change — the engine stays
  open source; the desktop app is what the licence gates.
- Docker Desktop is built on open-source software; the deskop binary is licensed under the Docker
  Subscription Service Agreement.

Billing mechanics (docs.docker.com/subscription-billing/plans/docker/)
- Plans are billed at a flat rate per user per month, monthly or annual.
- Team and Business: each seat extends the plan to one more member; you can only remove unused seats.
- Each plan includes a base allocation of Docker Build Cloud minutes per month; base minutes reset on
  the billing cadence and do not accumulate; purchased extra minutes expire at the end of the period.
- Testcontainers Cloud runtime minutes: pre-purchase at $3 per 100 minutes, or on-demand at $4 per
  100 minutes billed at the end of the month.
- Docker Offload licences exist on Team and Business; adding them requires sales contact.
- Cancelling: no pause, the unused portion is not refundable, access continues to the end of the paid
  cycle; an unpaid invoice starts a 15-day grace period.
- Plan gates that matter: Pro adds unlimited private repositories, Build Cloud and commercial Desktop
  use; Team adds audit logs and role-based access control; Business adds SSO, SCIM, Hardened Docker
  Desktop and Image Access Management.

## Podman (sources: https://podman.io/, https://podman-desktop.io/,
https://docs.podman.io/en/latest/markdown/podman-system-service.1.html)

Product and licence
- Podman 6.1.4 (latest stable), Podman Desktop 1.30.5, Apache License 2.0. No paid tier.
- Podman: daemonless, rootless containers; SELinux support, network policy enforcement, immutable
  containers (vendor description).
- Podman Desktop: vendor-neutral GUI for containers and Kubernetes; "trusted as part of the CNCF";
  Linux, macOS, Windows; OCI and Compose compatible; extensions; GPU acceleration; multi-arch builds;
  VPN/proxy support and air-gapped installation options.
- Enterprise support is a Red Hat offering (Red Hat Build of Podman Desktop), not a Podman Desktop
  price tier.

The compatibility layer, and its own warning (podman-system-service man page)
- `podman system service` runs a listening API: one part is a compatibility layer for the **Docker
  v1.40 API**, the other is the native Libpod layer.
- It supports systemd socket activation: the service starts on first client connection and exits
  after an inactivity timeout (`--time`, default 5 seconds). Default sockets:
  `unix://$XDG_RUNTIME_DIR/podman/podman.sock` rootless, `unix:///run/podman/podman.sock` rootful.
- Pointing Docker tooling at it is one environment variable:
  `export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock`.
- The man page's own security note: "the API grants full access to all Podman functionality, and thus
  allows arbitrary code execution as the user running the API, with no ability to limit or audit this
  access"; it recommends against exposing the socket over TCP without mutual TLS and suggests SSH
  forwarding instead.
- The command is not available when Podman runs directly on a Windows or macOS host (where it talks to
  a remote API service instead).
- The service supports only one listening socket; `--time 0` means no timeout.

## Derived arithmetic you may use (show the formula in the text)

- 25 developers on Docker Team: 25 × $15 = $375/month = $4,500/year.
- The same 25 on Docker Pro: 25 × $9 = $225/month = $2,700/year — but Pro is a personal plan with no
  org audit logs or RBAC, so the saving buys a governance hole.
- The cliff, not the slope: a company at 249 employees pays $0 for Docker Desktop; at 250 employees
  (or $10M+ revenue) every commercial Desktop seat is paid at once. 200 developers × $15 = $3,000/month
  = $36,000/year, and nothing about the software changed.
- Testcontainers Cloud at 4,000 runtime minutes/month: 4,000 ÷ 100 = 40 blocks; 40 × $4 = $160/month
  on-demand, or 40 × $3 = $120/month pre-purchased.
- DHI production at 12 repositories: 12 × $5,000 = $60,000/year, before any Business seats.
- Podman's bill for the same 25 developers: $0 in licence fees. The cost is the port: rewriting
  handlers that depend on Docker-only API surface, and the socket security decision above.

## Do not claim
- Do not print a Docker Business per-seat price. The page says "Contact us"; do not use $24 or any
  other figure as Docker's list price.
- Do not claim Docker Desktop is free for open source commercial use or for government.
- Do not claim Podman is a drop-in replacement with no work: the compatibility layer is Docker v1.40,
  the man page documents its limits, and the runtime under it is different.
- Do not claim Podman Desktop is Red Hat-only or paid; the desktop is free, Red Hat sells support.
- Do not invent Podman market share, adoption numbers, or "Docker removed the free tier" claims (the
  free tier for small companies still exists).
- Do not claim rootless containers are immune to compromise: Podman's own docs say the API socket is
  arbitrary code execution as that user.

---
name: boomi-best-practices
description: >
  Apply the official Boomi best practices framework when generating recommendations,
  reviewing account configurations, or enriching health check findings with live
  documentation. Use this skill when the user asks about Boomi best practices, wants
  improvement recommendations for their Boomi account, or when another skill (such as
  boomi-health-check) requests best practices enrichment. Always performs live WebSearch
  against help.boomi.com, community.boomi.com, and release notes before generating
  recommendations — never relies on training data alone.
---

# Boomi Best Practices Skill

This skill defines the official Boomi best practices framework used to enrich health check reports, generate improvement recommendations, and evaluate account configurations against Boomi's documented guidance.

---

## How to use this skill

This skill is invoked in two modes:

### Mode 1 — Health Check Enrichment (primary)
When the `boomi-health-check` skill generates findings, invoke this skill to:
1. Cross-reference each finding against the relevant best practice category
2. Fetch live Boomi guidance using the WebSearch queries in each category section
3. Enrich recommendations with official documentation links and specific guidance
4. Flag any findings that relate to known issues or deprecated features in recent release notes

### Mode 2 — Standalone Best Practices Review
When the user asks directly about Boomi best practices, implementation standards, or "how should we configure X", use this skill to structure the response with official references.

---

## CRITICAL: Always consult live documentation

**Before generating recommendations in any category, you MUST perform at least one WebSearch against official Boomi sources.** Boomi's best practices evolve with each runtime release, and guidance from 12+ months ago may be outdated. The search patterns in each section below are optimized for finding indexed Boomi documentation.

Official Boomi documentation sources (in priority order):
1. **help.boomi.com** — authoritative product documentation
2. **community.boomi.com** — peer-validated patterns, known issues, workarounds
3. **developer.boomi.com** — API reference, connector SDK, MCP/agent development
4. **boomi.com/blog** — architectural guidance, use case deep-dives
5. **Boomi release notes** — breaking changes, deprecations, new recommended settings

### How to search (help.boomi.com is client-side rendered — use WebSearch)

```
# General pattern — always include "boomi" and the topic
"boomi [topic] best practices"
site:help.boomi.com [topic]
site:community.boomi.com [topic] best practices
"boomi atomsphere [topic]" -site:competitor.com

# Release notes (check for recent changes to the topic area)
"boomi release notes" "[topic]" 2024 OR 2025
site:help.boomi.com "release notes" "[feature]"

# Community knowledge base articles
site:community.boomi.com "best practice" [topic]
site:community.boomi.com "tip" OR "guide" [topic]
```

---

## Best Practice Categories

Seven categories aligned to Boomi's product surface. Each category maps to one or more health check areas and can be owned by a standalone skill.

| # | Category | Health check mapping | Skill surface |
|---|---|---|---|
| §1 | Account & Licensing | account info, entitlements | `boomi-health-check` Step 2 |
| §2 | Runtime Infrastructure | `runtimeStatus`, `runtimeConfig` | `boomi-health-check` Step 3b |
| §3 | Integration Design | `deadProcesses`, `executionHealth` | `boomi-health-check` Step 4 |
| §4 | Deployment & Environments | `envConsistency` | `boomi-health-check` Step 4 |
| §5 | Execution & Observability | `executionHealth`, `deadProcesses` | `boomi-health-check` Step 4 |
| §6 | Security & Governance | `security` | `boomi-health-check` Step 4 |
| §7 | API Management | `apiGateway` | `boomi-health-check` Step 4 |

---

### §1 Account & Licensing

**Health check mapping:** Account info, entitlements, support tier, expiration

**What good looks like:**
- Support tier is active and not expiring within 90 days
- Entitlements match actual usage (API type, Molecule license, connection count)
- User accounts are active and associated with real individuals (no orphaned service accounts)
- Account has a named administrator or owner contact on record
- License utilization reviewed quarterly to avoid overages or unnecessary entitlements

**Common anti-patterns to flag:**
- Support expiring within 90 days with no renewal in progress
- Molecule runtimes deployed but Molecule entitlement not active
- API Management features in use but API entitlement is "NONE"
- Orphaned user accounts for former employees still active
- Account approaching connection limit with no license review scheduled

**WebSearch queries to run:**
```
site:help.boomi.com account management entitlements
site:help.boomi.com support tier renewal boomi
site:community.boomi.com boomi license management best practices
"boomi atomsphere" account entitlement molecule license
site:help.boomi.com user management deactivate account
```

**Key documentation areas on help.boomi.com:**
- Platform → Account Management → Licensing and Entitlements
- Platform → Account Management → User Management
- Platform → Account Management → Support Access

**Recommendation framing:**
> "Your support agreement expires on [date]. Boomi recommends initiating renewal 60 days in advance to avoid a lapse in support coverage."

---

### §2 Runtime Infrastructure

**Health check mapping:** `runtimeStatus`, runtime configuration, business continuity

> **Deep reference:** For detailed technical practices with specific JVM flags, NFS mount options, forked execution memory math, clustering requirements, and OS sizing — read `references/runtime-infrastructure-guide.md` before generating recommendations in this category.

**What good looks like:**
- All runtimes ONLINE, version within 1–2 releases of current, running Amazon Corretto OpenJDK
- JVM heap set with `-Xms` = `-Xmx` (no dynamic resizing); minimum 2–4 GB for production
- G1GC enabled (`-XX:+UseG1GC`) with `HeapDumpOnOutOfMemoryError` configured
- Working data directory on local SSD, not NFS/SMB; `70%` disk utilization alert in place
- Purge history configured (30 days for production; never 0 which disables purging)
- Release schedule set to SCHEDULED with a maintenance window; within 1–2 releases of current
- Production Molecules have ≥ 3 nodes on separate hosts/AZs; load balancer in front
- Forked execution enabled on Molecules; runner heap and concurrency tuned to node RAM
- Disaster recovery runbook documented, tested annually; config backed up to version control
- Atom-level certificates valid; 60-day alert, 30-day P1 threshold

**Common anti-patterns to flag:**
- `-Xms` and `-Xmx` set to different values (dynamic heap resizing = GC pauses)
- Oracle JDK instead of Amazon Corretto on Java 11+ (unsupported configuration)
- Working data directory on NFS/SMB (latency and locking issues) or `/tmp` (OS may purge)
- Purge history disabled (`purgeHistoryDays: 0`) — causes unbounded disk growth
- Runtime version 3+ releases behind current — security exposure, unsupported
- MANUAL release schedule on production runtimes without a documented reason
- Single-node Basic Atom or 2-node Molecule in production (no quorum safety)
- All Molecule nodes on the same physical host or availability zone (correlated failure risk)
- Forked execution not enabled on production Molecules
- Peak forked RAM not calculated: `Runner Heap × Max Simultaneous Forked Executions × Nodes`
- No DR runbook; configuration not version-controlled
- Atom co-located with database or other memory-intensive services
- High-frequency listener processes and batch processes on the same runtime

**WebSearch queries to run:**
```
site:help.boomi.com atom startup properties
site:help.boomi.com "working data" directory performance local storage molecule
site:help.boomi.com "purge history" settings independent purge schedules
site:community.boomi.com atom JVM heap best practices G1GC
"boomi molecule" sizing recommendations forked execution memory
site:help.boomi.com runtime release schedule rolling update
site:help.boomi.com Molecule high availability configuration NFS
site:community.boomi.com disaster recovery boomi best practices
site:help.boomi.com OpenTelemetry observability runtimes
site:community.boomi.com "forked execution" memory sizing
```

**Key documentation areas on help.boomi.com:**
- Integration → Atom Management → Atom Properties (startup, advanced properties)
- Integration → Atom Management → Runtime Release Schedules
- Integration → Atom Management → Observability Settings (OpenTelemetry)
- Integration → Molecule & Cloud Configuration → Local Storage
- Integration → Forked Execution in Molecules and Atom Clouds
- Platform → Certificates → Atom Certificates

**Release notes check:**
```
"boomi release notes" "atom" OR "runtime" 2024 OR 2025 "startup properties" OR "JVM" OR "OpenTelemetry"
```

**Recommendation framing:**
> "Boomi recommends [official guidance]. Your current configuration shows [finding]. To remediate: [specific steps with link to relevant help.boomi.com page]."

---

### §3 Integration Design

**Health check mapping:** `deadProcesses`, enriches `executionHealth`

Covers both general process design patterns and specialized integration patterns including EDI and trading partner management.

**What good looks like:**
- All deployed processes have error handling (Try/Catch shape or equivalent)
- Processes use subprocess patterns for reusable logic (not copy-paste)
- Dead processes reviewed quarterly and undeployed if unused
- Process names follow a consistent naming convention (e.g., `[System]-[Direction]-[Object]-[Action]`)
- Tracking fields populated for operational visibility
- Processes with high error rates have retry logic configured
- No processes with unbounded loops or missing Stop shapes on error paths
- Hard-coded values replaced with environment extensions or dynamic process properties

**Common anti-patterns to flag:**
- Processes with no Try/Catch and error rate > 0%
- Processes with `executionStatus: ERROR` more than 3 consecutive runs
- Duplicate process logic (same data flow duplicated across environments or use cases)
- Overly long processes (> 30 shapes) that should be decomposed into subprocesses
- Hard-coded values in process properties instead of environment extensions
- Connectors with credentials embedded in connection components (not extensions)
- "Allow Simultaneous Executions" enabled on processes that write to shared state (race conditions)
- Low Latency mode not used for high-frequency API/listener processes (<30 sec duration)
- Large data sets loaded into a single document instead of split-and-process batching (heap exhaustion risk)
- No heartbeat tracking fields on scheduled processes (silent success failures undetectable)

**WebSearch queries to run:**
```
site:help.boomi.com "try catch" error handling process
site:help.boomi.com process "best practices"
site:community.boomi.com process design best practices
"boomi atomsphere" error handling retry subprocess
site:help.boomi.com "tracking fields" process monitoring
"boomi" process naming convention best practices
site:community.boomi.com "dead process" cleanup
```

**Key documentation areas on help.boomi.com:**
- Integration → Building Integrations → Error Handling
- Integration → Building Integrations → Try/Catch Shape
- Integration → Building Integrations → Process Properties
- Integration → Building Integrations → Subprocesses and Process Call

#### §3a — EDI & Trading Partner Design

Applies when EDI processes or trading partners are present in the account.

**What good looks like:**
- Every trading partner has a unique ISA identifier (no duplicates)
- Production mode set to "Production" (not "Test") for live trading partners
- Acknowledgment modes configured per trading partner agreement
- Shared communication channels used for partners on the same protocol
- Trading partner processing groups link partners to processes
- AS2 certificates renewed before expiry
- EDI documents tracked with custom tracked fields for operational visibility

**Common anti-patterns to flag:**
- Duplicate ISA identifiers across trading partners (causes routing ambiguity)
- Trading partners marked as "Test" transmitting live documents
- No processing groups linking trading partners to processes (broken routing)
- AS2 certificates expired or within 30 days of expiry
- All EDI flows using a single generic process rather than partner-specific subprocesses

**WebSearch queries to run:**
```
site:help.boomi.com trading partner management best practices
site:help.boomi.com AS2 certificate renewal
site:community.boomi.com EDI trading partner best practices
"boomi" ISA identifier duplicate routing
site:help.boomi.com "processing group" EDI routing
"boomi atomsphere" EDI error handling acknowledgment
site:help.boomi.com shared communication channel configuration
```

---

### §4 Deployment & Environments

**Health check mapping:** `envConsistency`

**What good looks like:**
- Formal promotion pipeline: Dev → Test → Staging → Production
- All production processes were first validated in a non-production environment
- Package versioning notes explain what changed and why
- Deployment dates correlated with change management records
- Extensions (connections, process properties) configured per environment — no production values hardcoded
- Environment extensions reviewed after each deployment to catch connection drift
- Rollback plan documented for each major deployment

**Common anti-patterns to flag:**
- Direct-to-production deployments without a non-production environment stage
- Packages in non-production with no production counterpart (possible abandoned work)
- Extensions configured identically across test and production (shared endpoints)
- Deployments with no notes or version description
- Component versions significantly ahead in non-prod vs. production (large change backlog)

**WebSearch queries to run:**
```
site:help.boomi.com "deployed package" version management
site:help.boomi.com environment extensions best practices
site:community.boomi.com deployment pipeline best practices boomi
"boomi atomsphere" "promotion" environment pipeline
site:help.boomi.com "process properties" environment override
"boomi" change management deployment rollback
site:community.boomi.com "environment consistency" deployment
```

**Key documentation areas on help.boomi.com:**
- Integration → Deployment → Packaging and Deploying Processes
- Integration → Atom Management → Environment Extensions
- Integration → Environment Management

---

### §5 Execution & Observability

**Health check mapping:** `executionHealth`, `deadProcesses`

**Baseline thresholds (Boomi community consensus):**
| Error Rate | Classification | Action |
|---|---|---|
| < 2% | Healthy | Monitor |
| 2–5% | Elevated | Investigate top errors |
| 5–15% | Degraded | Prioritize remediation |
| > 15% | Critical | Immediate action required |

**What good looks like:**
- Production error rate < 5% (target < 2%); alert at >5%, escalate at >15% over rolling 1-hour window
- All deployed processes executed at least once per business cycle
- Scheduled processes staggered to avoid concurrent resource contention (stagger by 2–5 minutes)
- OpenTelemetry enabled on all runtimes; telemetry routed to a centralized observability platform (Datadog, New Relic, Dynatrace, Splunk)
- Atom heartbeat monitoring process runs on a schedule and posts to an external healthcheck endpoint (PagerDuty, UptimeRobot)
- Execution history searchable (custom tracked fields populated, execution summary meaningful)
- Heartbeat tracking fields on all scheduled processes to detect "silent success" failures (status=COMPLETE but 0 documents processed)
- Per-node Molecule metrics (JVM heap, thread count, active executions) exported via OTel for capacity planning

**Common anti-patterns to flag:**
- High-frequency schedules (every minute) on resource-intensive processes
- Multiple processes scheduled at the same minute without load balancing
- Processes with consistent ABORTED status (indicates runtime resource pressure)
- Executions with high `inboundErrorDocumentCount` but status COMPLETE (silent failures — no documents processed but process reports success)
- No tracking fields — execution history not searchable beyond status/date
- No external monitoring/alerting; relying solely on Boomi's native notifications
- No Atom heartbeat process — Boomi platform detection of offline Atom may be delayed
- Low Latency mode not used for high-frequency, short-duration API/listener processes (missing 30–50% throughput improvement)
- Simultaneous executions enabled on processes writing to shared state (race conditions)

**WebSearch queries to run:**
```
site:help.boomi.com execution record monitoring
site:community.boomi.com execution "error rate" threshold
"boomi" process schedule overlap best practices
site:help.boomi.com "process scheduling" concurrent
site:help.boomi.com OpenTelemetry observability runtimes
site:community.boomi.com "silent failure" OR "error document" boomi
site:help.boomi.com "custom tracked fields" execution history
site:help.boomi.com "low latency" process mode
site:community.boomi.com atom heartbeat monitoring process
site:community.boomi.com functional monitoring integration processes
```

**Release notes check:**
```
"boomi release notes" "execution" OR "scheduler" OR "OpenTelemetry" 2024 OR 2025
```

---

### §6 Security & Governance

**Health check mapping:** `security`

**What good looks like:**
- Each user has the minimum roles required for their function (least privilege)
- No user has more than 2–3 roles unless there is a documented business reason
- All PRODUCTION environments have role restrictions configured
- Custom roles used for fine-grained control rather than relying entirely on built-in roles
- API tokens and credentials rotated on a defined schedule (recommended: 90 days)
- User access reviewed quarterly; former employees promptly deactivated
- Audit log monitoring enabled for DELETE, user management, and environment changes
- Service accounts use dedicated API tokens (not personal user tokens)

**Common anti-patterns to flag:**
- Users with Administrator + Environment Management + full Build privileges simultaneously
- PRODUCTION environments with no role restrictions (open to all users with Env Mgmt)
- Personal email addresses used as service account usernames
- API tokens that have never been rotated (check audit log for token creation date)
- Accounts with no custom roles (over-reliance on broad built-in roles)
- Audit log not monitored or reviewed
- Atom process running as root or a domain admin (should use a non-privileged dedicated OS service account)
- Connector credentials (passwords, API keys) stored as hardcoded values in connection components — should use Environment Extensions or encrypted process properties
- Shared CA certificates bundled in connector components instead of deployed to the Atom truststore
- mTLS not enabled for inbound web service endpoints receiving sensitive data
- Molecule NFS shared mount accessible to OS users other than the Molecule service account
- TLS 1.0 or 1.1 enabled on the Atom Shared Web Server (minimum: TLS 1.2)

**WebSearch queries to run:**
```
site:help.boomi.com role "least privilege" security
site:help.boomi.com "environment role" restrictions production
site:community.boomi.com security best practices boomi
"boomi atomsphere" RBAC role-based access control
site:help.boomi.com API token management rotation
site:help.boomi.com "AccountUserRole" privileges
"boomi" user access review audit log monitoring
site:help.boomi.com audit log event types
```

**Key documentation areas on help.boomi.com:**
- Platform → Security → User Management
- Platform → Security → Role-Based Access
- Platform → Security → Environment Roles
- Platform → API Management → API Tokens

**Release notes check:**
```
"boomi release notes" "security" OR "roles" OR "permissions" 2024 OR 2025
```

---

### §7 API Management

**Health check mapping:** `apiGateway`

Covers API gateway infrastructure, API lifecycle management, application subscriptions, and all certificate/token expiry concerns at the gateway layer.

**What good looks like:**
- All gateways ACTIVE with auto-scaling configured for production traffic
- All deployed APIs have at least one active subscriber
- API plans configured with rate limits (no unlimited plans in production without justification)
- APIs versioned using semantic versioning
- SSL/TLS certificates on all gateway endpoints valid and not expiring within 30 days
- Consumer applications use meaningful names (not "App 1", "Test App")
- Deprecated API versions have a documented sunset date communicated to consumers
- Gateway memory and CPU monitored via observability tooling
- Certificate renewal process documented and tested

**Common anti-patterns to flag:**
- Deployed APIs with zero subscribers (dead API surface — security exposure)
- Unlimited API plans in production (no rate limiting = DDoS exposure)
- Applications without owner contact information
- Multiple applications sharing the same subscription/plan
- APIs deployed to production gateway not exposed through a staging gateway first
- Certificate expiry within 30 days on any gateway endpoint
- Self-signed certificates in production gateway endpoints
- API tokens with no documented expiry or rotation schedule

**WebSearch queries to run:**
```
site:help.boomi.com API gateway best practices
site:help.boomi.com "API Management" gateway configuration
site:community.boomi.com API gateway security best practices
"boomi API management" rate limiting plan configuration
site:help.boomi.com API versioning semantic
"boomi" API gateway SSL certificate management
site:help.boomi.com "deployed API" subscriber management
site:developer.boomi.com API management gateway
site:help.boomi.com certificate management renewal gateway
"boomi release notes" "API management" OR "gateway" 2024 OR 2025
```

**Key documentation areas:**
- API Management → Gateway Configuration
- API Management → API Policies and Plans
- API Management → Applications and Subscriptions
- Platform → Certificates → Gateway Certificates
- developer.boomi.com → Boomi API Reference → API Management

---

## Release Notes Review Protocol

**Always check release notes when generating recommendations.** Boomi releases quarterly with runtime patches in between. Recent releases may:
- Deprecate configuration options referenced in older guidance
- Introduce new recommended settings
- Fix known issues that explain findings in the health check
- Add new security requirements

### How to find the relevant release notes

```
# Find the most recent release notes
"boomi release notes" 2025 site:help.boomi.com
"boomi atomsphere release notes" 2025

# Find release notes for a specific area
"boomi release notes" "atom management" 2025
"boomi release notes" "API management" 2025
"boomi release notes" "security" 2025

# Find breaking changes or deprecations
"boomi" "deprecated" OR "breaking change" 2024 OR 2025
"boomi release notes" "removed" OR "no longer supported" 2025
```

### What to look for in release notes

| Look for | Why it matters |
|---|---|
| New startup property recommendations | May explain suboptimal runtime performance |
| Deprecated API endpoints | May affect integrations using older patterns |
| Security advisories | May indicate urgency on governance findings |
| New features related to findings | "There's now a better way to do this" |
| Known issues | May explain anomalous health check results |

---

## Community Knowledge Sources

The Boomi Community (community.boomi.com) contains peer-validated best practices that often go deeper than official docs. When official documentation is sparse on a topic, supplement with community search:

```
# Best practice articles
site:community.boomi.com "best practice" [topic]
site:community.boomi.com "tips and tricks" [topic]

# Troubleshooting known issues
site:community.boomi.com "known issue" [topic]
site:community.boomi.com "workaround" [topic]

# Architecture patterns
site:community.boomi.com "pattern" OR "architecture" [topic]
site:community.boomi.com "how to" [topic]
```

**High-value community article categories to search:**
- "Boomi best practices checklist"
- "Boomi performance tuning"
- "Boomi security hardening"
- "Boomi molecule sizing"
- "Boomi error handling patterns"
- "Boomi deployment pipeline"

---

## Integration with Health Check Skill

When used alongside `boomi-health-check`, this skill enriches each check section as follows:

| Health Check Section | Best Practice Category | What to Enrich |
|---|---|---|
| Account info / licensing | §1 Account & Licensing | Support renewal, entitlement gaps, orphaned users |
| Runtime Status | §2 Runtime Infrastructure | Version currency, HA, DR runbook, atom certs |
| Dead Processes | §3 Integration Design | Cleanup guidance, process lifecycle best practices |
| Env Consistency | §4 Deployment & Environments | Promotion pipeline guidance, deployment docs |
| Execution Health | §5 Execution & Observability | Error rate context, monitoring guidance, silent failures |
| Security | §6 Security & Governance | Role review, RBAC docs, recent security release notes |
| API Gateway | §7 API Management | Rate limiting, cert expiry, subscriber coverage |

### Enrichment output format

For each finding, add an **Official Guidance** block:

```
📋 **Official Guidance**
Source: [help.boomi.com / community.boomi.com / release notes]
Guidance: [1-2 sentences summarizing what Boomi recommends]
Applies to: [Runtime version range or "all versions"]
Link: [URL if available from WebSearch]
Last verified: [Date of the source you found]
```

---

## Recommendation Priority Framework

Use this framework to assign priority to all best practice recommendations:

| Priority | Criteria | Example |
|---|---|---|
| 🔴 P1 Critical | Production outage risk, security breach risk, data loss risk | Prod runtime offline, prod env with no access controls |
| 🟠 P2 High | Significant operational risk, compliance exposure, repeated failures | Error rate > 15%, no HA on production Molecule |
| 🟡 P3 Medium | Best practice deviation with moderate risk | Error rate 5-15%, processes missing error handling |
| 🟢 P4 Low | Hygiene improvements, optimization opportunities | Dead processes not cleaned up, deployment notes missing |
| ℹ️ P5 Advisory | "Nice to have" or future-state improvements | New Boomi feature that could simplify current approach |

---

## Feedback Collection

After delivering best practice recommendations, ask:

> "Were these recommendations relevant to your environment? Any areas I should go deeper on, or skip in future reviews?"

If the user provides feedback:
- Note any categories they've already addressed ("we have HA covered") — skip those in future enrichment passes
- Note any areas they want prioritized ("we care most about security") — weight those higher
- If the user identifies a recommendation as outdated or inapplicable, acknowledge it and note that live WebSearch should always be the source of truth over any cached guidance in this skill

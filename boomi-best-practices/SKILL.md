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

---

### 1. Runtime Configuration & Performance

**Health check mapping:** `runtimeStatus`, `runtimeConfig` (SOON check)

**What good looks like:**
- All runtimes ONLINE with version within 1-2 releases of current
- JVM heap sized appropriately for workload (minimum 1GB, recommended 2–4GB for production)
- Working data directory on fast local I/O (SSD), not network-mounted storage
- Purge history configured (recommended: 30–60 days, never 0/disabled in production)
- Observability/logging enabled and pointed at a log aggregator
- Release schedule set to SCHEDULED (not MANUAL) unless intentional for the environment
- Molecule nodes balanced with appropriate thread counts

**Common anti-patterns to flag:**
- Runtime on same host as database or other memory-intensive services
- Working data directory on NFS/SMB/network share
- Purge history disabled (`purgeHistoryDays: 0`) — causes unbounded disk growth
- Runtime version 3+ releases behind current — security exposure + unsupported configuration
- MANUAL release schedule on production runtimes without a documented reason
- Single-node Molecule in production (no HA)

**WebSearch queries to run:**
```
site:help.boomi.com atom startup properties
site:help.boomi.com "working data" directory performance
site:help.boomi.com "purge history" settings
site:community.boomi.com atom JVM heap best practices
"boomi molecule" sizing recommendations
site:help.boomi.com runtime release schedule
"boomi atom" "working directory" SSD performance
```

**Key documentation areas on help.boomi.com:**
- Integration → Atom Management → Atom Properties
- Integration → Atom Management → Runtime Release Schedules
- Integration → Atom Management → Observability Settings
- Integration → Molecule & Cloud Configuration

**Release notes check:**
```
"boomi release notes" "atom" OR "runtime" 2024 OR 2025 "startup properties" OR "JVM"
```

**Recommendation framing:**
> "Boomi recommends [official guidance]. Your current configuration shows [finding]. To remediate: [specific steps with link to relevant help.boomi.com page]."

---

### 2. Process Design & Code Quality

**Health check mapping:** `integrationPatterns` (SOON check), enriches `executionHealth` and `deadProcesses`

**What good looks like:**
- All deployed processes have error handling (Try/Catch shape or equivalent)
- Processes use subprocess patterns for reusable logic (not copy-paste)
- Dead processes reviewed quarterly and undeployed if unused
- Process names follow a consistent naming convention (e.g., `[System]-[Direction]-[Object]-[Action]`)
- Tracking fields populated for operational visibility
- Processes with high error rates have retry logic configured
- No processes with unbounded loops or missing Stop shapes on error paths

**Common anti-patterns to flag:**
- Processes with no Try/Catch and error rate > 0%
- Processes with `executionStatus: ERROR` more than 3 consecutive runs
- Duplicate process logic (same data flow duplicated across environments or use cases)
- Overly long processes (> 30 shapes) that should be decomposed into subprocesses
- Hard-coded values in process properties instead of environment extensions
- Connectors with credentials embedded in connection components (not extensions)

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

**Recommendation framing:**
> "Boomi recommends wrapping all process flows in a Try/Catch shape to ensure errors are captured and routed. [X] of your deployed processes have no error handling. See: help.boomi.com → Building Integrations → Error Handling."

---

### 3. Execution Health & Operations

**Health check mapping:** `executionHealth`, `deadProcesses`, `scheduleConflicts` (SOON check)

**Baseline thresholds (Boomi community consensus):**
| Error Rate | Classification | Action |
|---|---|---|
| < 2% | Healthy | Monitor |
| 2–5% | Elevated | Investigate top errors |
| 5–15% | Degraded | Prioritize remediation |
| > 15% | Critical | Immediate action required |

**What good looks like:**
- Production error rate < 5% (target < 2%)
- All deployed processes executed at least once per business cycle
- Scheduled processes staggered to avoid concurrent resource contention
- Execution history searchable (tracking fields populated, execution summary meaningful)
- Alerts configured for process failures (audit log or external monitoring)

**Common anti-patterns to flag:**
- High-frequency schedules (every minute) on resource-intensive processes
- Multiple processes scheduled at the same minute without load balancing
- Processes with consistent ABORTED status (indicates runtime resource pressure)
- Executions with high inboundErrorDocumentCount but status COMPLETE (silent failures)
- No monitoring/alerting configured beyond Boomi's native notifications

**WebSearch queries to run:**
```
site:help.boomi.com execution record monitoring
site:community.boomi.com execution "error rate" threshold
"boomi" process schedule overlap best practices
site:help.boomi.com "process scheduling" concurrent
"boomi atomsphere" execution monitoring alerting
site:community.boomi.com "silent failure" OR "error document" boomi
site:help.boomi.com "custom tracked fields" execution history
```

**Release notes check:**
```
"boomi release notes" "execution" OR "scheduler" 2024 OR 2025
```

---

### 4. Security & Governance

**Health check mapping:** `security`

**What good looks like:**
- Each user has the minimum roles required for their function (least privilege)
- No user has more than 2–3 roles unless there is a documented business reason
- All PRODUCTION environments have role restrictions configured
- Custom roles used for fine-grained control rather than relying entirely on built-in roles
- API tokens rotated on a defined schedule (recommended: 90 days)
- User access reviewed quarterly
- Audit log monitoring enabled for DELETE, user management, and environment changes
- Service accounts use dedicated API tokens (not personal user tokens)

**Common anti-patterns to flag:**
- Users with Administrator + Environment Management + full Build privileges simultaneously
- PRODUCTION environments with no role restrictions (open to all users with Env Mgmt)
- Personal email addresses used as service account usernames
- API tokens that have never been rotated (check audit log for token creation date)
- Accounts with no custom roles (over-reliance on broad built-in roles)
- Audit log not monitored or reviewed

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

### 5. Environment Consistency & Deployment

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

### 6. API Gateway & API Management

**Health check mapping:** `apiGateway`

**What good looks like:**
- All gateways ACTIVE with auto-scaling configured for production traffic
- All deployed APIs have at least one active subscriber
- API plans configured with rate limits (no unlimited plans in production without justification)
- APIs versioned using semantic versioning
- SSL/TLS configured with valid, non-expired certificates on all gateway endpoints
- Consumer applications use meaningful names (not "App 1", "Test App")
- Deprecated API versions have a documented sunset date communicated to consumers
- Gateway memory and CPU monitored via observability tooling

**Common anti-patterns to flag:**
- Deployed APIs with zero subscribers (dead API surface — security exposure)
- Unlimited API plans in production (no rate limiting = DDoS exposure)
- Applications without owner contact information
- Multiple applications sharing the same subscription/plan
- APIs deployed to production gateway not exposed through a staging gateway first
- Certificate expiry within 30 days on any gateway endpoint

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
```

**Key documentation areas:**
- API Management → Gateway Configuration
- API Management → API Policies and Plans
- API Management → Applications and Subscriptions
- developer.boomi.com → Boomi API Reference → API Management

**Release notes check:**
```
"boomi release notes" "API management" OR "gateway" 2024 OR 2025
```

---

### 7. EDI & Trading Partner Management

**Health check mapping:** EDI-specific extension of `executionHealth`

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

### 8. Certificate & Token Expiry

**Health check mapping:** `certificates` (SOON check)

**What good looks like:**
- No deployed expired certificates
- Certificate expiry monitored with alerts ≥ 30 days in advance
- Token expiry tracked in a secrets management system
- Certificate renewal process documented and tested
- Wildcard certificates used where appropriate to reduce maintenance overhead

**Common anti-patterns to flag:**
- Expired certificates deployed (will cause immediate connectivity failures)
- Certificates expiring within 30 days with no renewal in progress
- Self-signed certificates in production
- API tokens with no documented expiry or rotation schedule

**WebSearch queries to run:**
```
site:help.boomi.com certificate management renewal
site:help.boomi.com "DeployedExpiredCertificate" OR "certificate expiry"
site:community.boomi.com certificate renewal boomi atom
"boomi atomsphere" SSL certificate best practices
site:help.boomi.com PGP certificate management
```

---

### 9. Business Continuity & Resilience

**Health check mapping:** `businessContinuity` (SOON check)

**What good looks like:**
- Production Molecules have ≥ 2 nodes (HA configuration)
- Disaster recovery runbook documented and tested annually
- Boomi Cloud Atoms used where on-premise HA is not feasible
- Runtime upgrade schedule aligned with Boomi's quarterly release cycle
- Backup of process components and account configuration maintained (export/backup)
- Critical process failures trigger PagerDuty/Opsgenie/email alerts

**Common anti-patterns to flag:**
- Single-node Molecule in production (SPOF)
- No documented runbook for runtime failure
- Runtimes running versions more than 3 releases behind (unsupported configuration)
- No external monitoring of process execution health (Boomi-only alerting)
- No component backup/export schedule

**WebSearch queries to run:**
```
site:help.boomi.com Molecule high availability configuration
site:community.boomi.com disaster recovery boomi best practices
"boomi atomsphere" high availability HA molecule cluster
site:help.boomi.com "runtime upgrade" release schedule
"boomi" backup export components account
site:community.boomi.com business continuity integration platform
```

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
| Runtime Status | §1 Runtime Configuration | Add version currency check, HA recommendation for single-node prod |
| Execution Health | §3 Execution Health | Add error rate context, link to monitoring guidance |
| Dead Processes | §2 Process Design | Add cleanup guidance, link to process lifecycle best practices |
| Env Consistency | §5 Deployment | Add promotion pipeline guidance, link to deployment docs |
| Security | §4 Security | Add role review guidance, link to RBAC docs, check recent security release notes |
| API Gateway | §6 API Management | Add plan/rate limit guidance, check for cert expiry, link to API management docs |

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

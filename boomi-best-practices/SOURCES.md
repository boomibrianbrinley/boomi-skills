# Boomi Official Documentation Sources

Quick reference for agents: where to find authoritative Boomi guidance, organized by topic.

> **Note:** help.boomi.com uses client-side rendering and is not directly fetchable. Always use **WebSearch** with the patterns below. The `site:help.boomi.com` operator finds indexed pages that search engines have crawled.

---

## Primary Sources (always check these)

| Source | URL | Best for |
|---|---|---|
| Help Portal | https://help.boomi.com | Product documentation, how-to guides, configuration reference |
| Developer Portal | https://developer.boomi.com | REST API reference, Connector SDK, MCP/Agent development |
| Community | https://community.boomi.com | Peer knowledge, known issues, workarounds, architecture patterns |
| Release Notes | Search: `"boomi release notes" 2025 site:help.boomi.com` | Breaking changes, deprecations, new features, security fixes |
| Boomi Blog | https://boomi.com/blog | Architecture guidance, use case deep-dives, product announcements |
| Boomi on Postman | https://www.postman.com/boomi-team/ | Live API collections for Platform API and AtomSphere API |

---

## WebSearch Patterns by Topic

### Runtime & Atom Management

```
# Startup properties and JVM configuration
site:help.boomi.com "atom startup properties"
"boomi atom" JVM heap size recommendations
site:community.boomi.com atom "startup properties" best practices

# Performance and working directory
site:help.boomi.com "working data" atom performance
"boomi" working directory NFS performance issues
site:community.boomi.com atom performance tuning

# Molecule high availability
site:help.boomi.com molecule "high availability" configuration
"boomi molecule" cluster sizing nodes
site:community.boomi.com molecule HA disaster recovery

# Runtime release schedules
site:help.boomi.com "runtime release schedule"
"boomi" atom runtime upgrade schedule quarterly
site:help.boomi.com "atom version" upgrade

# Purge history
site:help.boomi.com "purge history" atom settings
"boomi" purge history days recommendation

# Observability
site:help.boomi.com "runtime observability" settings logging
"boomi" atom logging observability OpenTelemetry
```

### Process Design

```
# Error handling
site:help.boomi.com "try catch" shape error handling
"boomi atomsphere" error handling best practices
site:community.boomi.com process error handling try catch

# Subprocess patterns
site:help.boomi.com "subprocess" OR "process call" shape
"boomi" subprocess reusable process pattern
site:community.boomi.com subprocess architecture pattern

# Process properties and extensions
site:help.boomi.com "process properties" extension environment
"boomi" process property override environment extension

# Tracking and visibility
site:help.boomi.com "custom tracked fields" execution
"boomi" execution tracking visibility monitoring
site:community.boomi.com tracked fields process monitoring

# Naming conventions
site:community.boomi.com process naming convention best practices
"boomi" process naming standards convention
```

### Execution & Scheduling

```
# Execution history and monitoring
site:help.boomi.com "execution record" query monitoring
"boomi" execution history monitoring alerting
site:community.boomi.com execution monitoring best practices

# Schedule configuration
site:help.boomi.com "process schedule" configuration
"boomi" process scheduling concurrent overlap
site:community.boomi.com schedule overlap resource contention

# Error investigation
site:help.boomi.com execution error troubleshooting
"boomi" execution ABORTED ERROR status troubleshooting
site:community.boomi.com execution error common causes
```

### Security & Governance

```
# RBAC and roles
site:help.boomi.com "role" "environment" access control
"boomi atomsphere" RBAC least privilege
site:community.boomi.com security roles best practices

# Environment restrictions
site:help.boomi.com "environment role" restriction production
"boomi" production environment access control restriction

# API tokens and credentials
site:help.boomi.com "API token" management rotation
"boomi" API token security rotation best practices
site:community.boomi.com API token management

# Audit logging
site:help.boomi.com "audit log" event types monitoring
"boomi atomsphere" audit log security monitoring
site:community.boomi.com audit log event types list

# Security release notes
"boomi release notes" security 2024 OR 2025
"boomi" security advisory CVE 2024 OR 2025
```

### Deployment & Environments

```
# Package deployment
site:help.boomi.com "packaged component" deploy
"boomi" deployment pipeline best practices
site:community.boomi.com deployment best practices boomi

# Environment extensions
site:help.boomi.com "environment extensions" configuration
"boomi" environment extension connection override
site:community.boomi.com environment extensions best practices

# Promotion pipeline
site:help.boomi.com environment classification promotion
"boomi" dev test staging production promotion pipeline
site:community.boomi.com environment promotion strategy

# Change management
"boomi" change management deployment notes versioning
site:community.boomi.com change management boomi deployment
```

### API Management

```
# Gateway configuration
site:help.boomi.com "API gateway" configuration
"boomi API management" gateway best practices
site:community.boomi.com API gateway configuration tips

# Rate limiting and plans
site:help.boomi.com "API plan" rate limiting
"boomi" API rate limit plan configuration
site:community.boomi.com API plan rate limiting best practices

# SSL and certificates on gateways
site:help.boomi.com "API gateway" SSL certificate
"boomi" API gateway HTTPS TLS certificate
site:community.boomi.com API gateway certificate renewal

# Subscriptions and applications
site:help.boomi.com "deployed API" application subscription
"boomi" API subscriber management best practices

# API versioning
site:help.boomi.com API versioning strategy
"boomi" API version deprecation sunset
```

### EDI & Trading Partners

```
# Trading partner configuration
site:help.boomi.com "trading partner" configuration best practices
"boomi" EDI trading partner setup
site:community.boomi.com EDI trading partner best practices

# AS2 and certificates
site:help.boomi.com AS2 certificate configuration
"boomi" AS2 certificate renewal expiry
site:community.boomi.com AS2 certificate renewal

# EDI acknowledgments
site:help.boomi.com EDI acknowledgment "997" OR "999" configuration
"boomi" EDI acknowledgment mode trading partner
site:community.boomi.com EDI acknowledgment best practices

# Processing groups
site:help.boomi.com "trading partner processing group"
"boomi" EDI routing processing group configuration
```

### Certificate & Key Management

```
# Certificate expiry
site:help.boomi.com certificate expiry management
"boomi" "expired certificate" OR "certificate renewal"
site:community.boomi.com certificate management boomi

# PGP keys
site:help.boomi.com PGP certificate management
"boomi" PGP key rotation renewal

# Certificate API
site:help.boomi.com "DeployedExpiredCertificate" API
"boomi atomsphere" certificate expiry API monitoring
```

### Business Continuity

```
# High availability
site:help.boomi.com Molecule "high availability" failover
"boomi molecule" HA cluster failover configuration
site:community.boomi.com boomi disaster recovery HA

# Backup and restore
site:help.boomi.com component backup export account
"boomi atomsphere" backup components export
site:community.boomi.com boomi backup restore strategy

# Monitoring and alerting
site:help.boomi.com process failure notification alerting
"boomi" external monitoring alerting PagerDuty OR Opsgenie
site:community.boomi.com boomi alerting monitoring integration
```

---

## Release Notes — How to Find by Version

Boomi releases quarterly (typically March, June, September, December). Between releases there are runtime patches.

```
# Find the latest release notes
"boomi platform" "release notes" 2025
"boomi atomsphere" release notes latest

# Find release notes for a specific version
"boomi" "release notes" "25.1" OR "25.2" OR "25.3" OR "25.4"

# Find what changed in a specific area
"boomi release notes" "runtime" 2025
"boomi release notes" "API management" 2025
"boomi release notes" "security" 2025
"boomi release notes" "EDI" OR "B2B" 2025

# Find deprecation notices
"boomi" deprecated 2025 atomsphere
"boomi" "no longer supported" 2024 OR 2025
"boomi release notes" "removed" 2025
```

---

## Developer API Reference

For recommendations that involve automation or custom tooling:

| API Area | Search Pattern |
|---|---|
| Platform REST API reference | `site:developer.boomi.com "platform API" reference` |
| AtomSphere API objects | `site:developer.boomi.com atomsphere API objects` |
| GraphQL schema | `site:developer.boomi.com graphql boomi` |
| Connector SDK | `site:developer.boomi.com connector SDK development` |
| MCP / Agent APIs | `site:developer.boomi.com "model context protocol" OR MCP agent` |
| Postman collections | `boomi API postman collection github` |

---

## How to Cite Sources in Recommendations

When you find official guidance, cite it clearly so users can verify:

```markdown
**Source:** [help.boomi.com / community.boomi.com / developer.boomi.com]
**Article/Section:** [Page title or section heading from the found page]
**URL:** [Full URL from WebSearch result]
**Relevance:** [One sentence explaining why this guidance applies to the finding]
```

If WebSearch returns no indexed results for a specific query, note it explicitly:
> "No specific Boomi documentation found for this configuration. Recommendation is based on general best practices and community consensus. Manual verification against help.boomi.com recommended."

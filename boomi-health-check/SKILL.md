---
name: boomi-health-check
description: >
  Generate a comprehensive Boomi account health check report. Use this skill when the
  user asks for an account health check, health report, health score, risk assessment,
  or a structured review of their Boomi platform across environments. Also trigger when
  the user mentions "run a health check", "check my Boomi account", "how healthy is my
  account", or wants a graded report with recommendations. Pairs with the
  boomi-best-practices skill to enrich findings with official Boomi documentation.
---

# Boomi Account Health Check Skill

You are an expert Boomi platform health analyst. This skill guides you through generating a comprehensive health check report for a Boomi account, formatted to the same standard as professional Boomi customer health check presentations.

> **Requires:** The `boomi-best-practices` skill should also be installed. After collecting health check data, invoke the best practices skill to enrich each finding with live Boomi documentation, WebSearch queries, and official guidance before generating recommendations. If the best practices skill is not available, note this in the report and proceed with the built-in guidance below.

---

## When to use this skill

Use this skill when the user asks for:
- An account health check or health report
- A Boomi platform review
- A health score or risk assessment
- A structured summary of account health across environments

---

## Scope and Constraints

**This skill is read-only.** It NEVER:
- Creates, modifies, or deletes any Boomi component, process, or configuration
- Triggers executions or deployments
- Changes role assignments, environment settings, or runtime properties
- Writes to any external system

All MCP tool calls made by this skill are **read operations only** (`boomi_get_*`, `boomi_list_*`, `boomi_query_*`, `boomi_health_check_summary`). If a user requests an action (e.g. "fix this", "apply the recommendation"), clarify that the skill identifies and reports — it does not remediate.

---

## Step 0 — Discovery: Capability Check

Before running any analysis, call `boomi_get_account_info` to determine what capabilities are available for this account. This prevents wasted tool calls on features the account tier doesn't support.

```
boomi_get_account_info(accountId: "<id or omit for default>")
```

Check the response and set these flags internally:

| Field | Check | If missing/false |
|---|---|---|
| `apiType` | Is API Management enabled? | Skip `apiGateway` check — set to `info` |
| `expirationDate` | Within 90 days? | Flag as high-priority licensing finding |
| `moleculeEntitlement` | Is Molecule licensed? | Note if Molecule runtimes are present without entitlement |
| `supportLevel` | Is support active? | Include in licensing section |

Tell the user: _"Checking account capabilities before starting analysis…"_

**Gate:** If `boomi_get_account_info` returns an error or empty response, STOP and tell the user:
> "I couldn't retrieve account info. Please verify the account ID and that your credentials have read access, then retry."

---

## Step 1 — Select account and environments

If the user has not specified an account, call `boomi_list_accounts` and ask them to choose.

If the user has not specified environments, ask:
> "Which environments would you like to include? Options: **all**, **production only**, or name specific environments."

Common shortcuts:
- "prod" / "production only" → pass `environments: "production"`
- "everything" / "all" → pass `environments: "all"`
- Named envs → pass `environments: ["ENV_NAME_1", "ENV_NAME_2"]`

**Gate:** If no environments exist in scope, STOP:
> "No environments found for this account in the selected scope. Please verify the account or select a different scope."

---

## Step 2 — Gather licensing and account details

**Always** call `boomi_get_account_info` to capture licensing and entitlement details. These must appear in every report.

```
boomi_get_account_info(accountId: "<id>")
```

Record and include in the report:
- Account name, ID, and type
- Support level / tier
- Expiration date (flag if within 90 days)
- API type and entitlement status
- Molecule entitlement (note if molecule usage exceeds entitlement)

**Gate:** If account info is unavailable after Step 0, skip licensing details and note: _"Account details unavailable — licensing section omitted."_ Proceed to Step 3.

---

## Step 3 — Call boomi_health_check_summary

Call the tool with the resolved parameters:

```
boomi_health_check_summary(
  accountId: "<id or omit for default>",
  environments: "<all | production | [names]>",
  daysBack: <30 for monthly, 7 for weekly, 90 for quarterly>
)
```

Tell the user: _"Running health checks across [N] environments — this may take 20–30 seconds…"_

**Gate:** If `boomi_health_check_summary` fails or returns no checks:
- If error is auth-related: STOP and surface the error to the user
- If error is timeout: Retry once; if it fails again, note partial data and proceed with available checks
- If response has no environments in scope: STOP — confirm environment selection with user

---

## Step 3b — Gather runtime configurations

**Always** call `boomi_list_runtimes` then `boomi_get_runtime_details` for each runtime (up to 10; prioritize production runtimes if more than 10 exist).

```
boomi_list_runtimes(accountId: "<id>")

// For each runtime ID returned:
boomi_get_runtime_details(
  runtimeId: "<id>",
  sections: ["overview", "startup", "runtime-props", "disk-space", "release"],
  accountId: "<id>"
)
```

Analyze and include in the report:
- **JVM heap settings** — flag if `com.boomi.container.maxMemory` or `-Xmx` is not set or below 2GB for production
- **Runtime version** — flag if runtime is more than 2 releases behind the latest Boomi runtime version
- **Release schedule** — note if auto-update is enabled/disabled and the scheduled window
- **Disk space** — flag if any runtime is above 80% disk utilization
- **Observability** — note if monitoring/alerting is not configured
- **Runtime properties** — flag non-default JVM args, custom classpath entries, or security policy overrides that deviate from best practices

---

## Step 4 — Interpret the results

The tool returns a `checks` object with these six categories. Interpret each one:

### runtimeStatus — Infrastructure
| Tool status | Meaning |
|---|---|
| `pass` | All runtimes online |
| `warn` | Non-production runtimes offline |
| `fail` | PRODUCTION runtime(s) offline — **critical** |
| `info` | No runtimes found in scope |

### executionHealth — Operations
| Tool status | Meaning |
|---|---|
| `pass` | Error rate < 5% |
| `warn` | Error rate 5–14% |
| `fail` | Error rate ≥ 15% |
| `info` | No execution data available |

### deadProcesses — Operations
| Tool status | Meaning |
|---|---|
| `pass` | All deployed processes are actively executing |
| `warn` | Some processes never ran in the analysis window |
| `fail` | ≥ 30% of deployed processes had zero executions |
| `info` | Cannot determine (no runtimes or packages) |

### envConsistency — Deployment
| Tool status | Meaning |
|---|---|
| `pass` | All non-prod deployments are promoted to production |
| `warn` | Some processes exist in non-prod but not in production |
| `info` | Cannot compare (only one environment classification present) |

### security — Governance
| Tool status | Meaning |
|---|---|
| `pass` | No governance concerns |
| `warn` | Users with excessive roles OR unrestricted non-prod environments |
| `fail` | PRODUCTION environments with no role restrictions |
| `info` | Security data unavailable |

### apiGateway — Governance
| Tool status | Meaning |
|---|---|
| `pass` | All gateways online, APIs have subscribers |
| `warn` | Deployed APIs with no subscribers |
| `fail` | Gateway(s) offline |
| `info` | GraphQL endpoint not accessible on this account tier |

---

## Step 5 — Overall health score

Map the `overallStatus` and check summary to an overall score:

| Condition | Score | Color |
|---|---|---|
| No fail/warn checks | **A** (Healthy) | Green |
| 1 warn, 0 fail | **B** (Good) | Blue |
| 2+ warns, 0 fail | **C** (Needs Attention) | Amber |
| 1+ fail | **D** (At Risk) | Red |
| Critical fail (prod runtime offline) | **F** (Critical) | Red |

---

## Step 5.5 — Enrich findings with official Boomi guidance

**Before formatting the report**, enrich each failing or warning check with live documentation using the `boomi-best-practices` skill. For each check with status `fail` or `warn`:

1. Identify the matching best practice category from the table below
2. Run the WebSearch queries listed in that category (from `boomi-best-practices` SKILL.md)
3. Check for recent release notes relevant to the finding
4. Search the Boomi Community for known issues or workarounds
5. Add an **Official Guidance** block to the recommendation for that finding

| Health Check | Best Practice Category | Key search terms |
|---|---|---|
| account / licensing | §1 Account & Licensing | support renewal, entitlements, user management |
| runtimeStatus | §2 Runtime Infrastructure | atom startup properties, molecule HA, JVM heap, atom certs |
| deadProcesses | §3 Integration Design | dead process cleanup, process lifecycle, error handling |
| envConsistency | §4 Deployment & Environments | environment promotion, deployment pipeline |
| executionHealth | §5 Execution & Observability | execution error rate, monitoring, alerting, silent failures |
| security | §6 Security & Governance | RBAC, environment role restrictions, audit log |
| apiGateway | §7 API Management | gateway configuration, rate limiting, certificates |

**Minimum documentation check per report:** At a minimum, always search for:
```
"boomi release notes" 2025          ← check for breaking changes or new recommendations
site:community.boomi.com best practices boomi atomsphere   ← community guidance index
```

## Step 6 — Format the report

### Inline markdown (default)
Use for quick checks. Sections separated by `---`. Use tables for Runtime Inventory and Recommendations. Bold the overall grade.

### Branded HTML + PowerPoint (when user asks for a "report", "PowerPoint", "slides", or "Word doc")

**Do NOT generate Python scripts or write file content inline.** Instead, call `boomi_generate_health_report` — it generates both a branded `.pptx` and a standalone `.html` file using the Boomi Exosphere design system (coral/navy/purple) and saves them directly to disk. No Python or additional software needed; it runs in the MCP server which is already part of this project.

#### Calling the tool

After generating recommendations (Step 6), call:

Before calling the tool, ask the user:
1. **Where to save the files** — folder path (default: `~/Downloads/boomi-reports`)
2. **What to name the files** — a short prefix like `"CENet-HealthCheck-Q1-2026"` (no extension needed). If not provided, default to `"boomi-health-{accountName}-{date}"`

```
boomi_generate_health_report(
  accountName:     "<name from boomi_get_account_info>",
  accountId:       "<account ID>",
  generatedAt:     "<ISO timestamp from boomi_health_check_summary>",
  daysBack:        <number>,
  overallStatus:   "<pass | warn | fail>",
  summary:         { pass: N, warn: N, fail: N, info: N },
  checks:          <full checks object from boomi_health_check_summary>,
  accountDetails:  <full object from boomi_get_account_info>,
  runtimeDetails:  <array of objects from boomi_get_runtime_details, one per runtime>,
  recommendations: [
    { priority: "critical|high|medium|low", area: "...", finding: "...", action: "..." },
    ...
  ],
  outputDir:       "<user-provided folder or omit for default>",
  fileNamePrefix:  "<user-provided name or omit for default>"
)
```

The tool returns `{ pptxPath, htmlPath, generatedAt }`. Tell the user:
> "Your reports have been saved:
> - **PowerPoint:** `<pptxPath>`
> - **HTML:** `<htmlPath>`
>
> Open them from Finder or drag the HTML into a browser to preview."

#### Report structure (PowerPoint slides — all sections always required)
- Slide 1: Cover — Account name, date, analysis window, grade badge (A/B/C/D)
- Slide 2: Executive Summary — score cards (pass/warn/fail/info counts) + key findings
- Slide 3: **Licensing & Account Details** — account type, support tier, expiration, entitlements, flags
- Slide 4: **Runtime Configuration** — inventory table, JVM heap, version, release schedule, disk, observability flags
- Slides 5–10: One slide per check category (runtimeStatus, executionHealth, deadProcesses, envConsistency, security, apiGateway)
- Slide 11: **Recommendations** — prioritized table covering ALL findings (licensing + runtime config + 6 checks)

---

## Boomi Report Design System

**These design rules apply to ALL output formats** (PowerPoint, HTML, inline markdown). They are derived from the official Boomi health check presentation template. Always follow them — do not deviate without explicit user instruction.

### Typography
- **Font family:** Poppins (fallback: Arial, sans-serif)
- **Cover / section header titles:** 46pt, Poppins regular, color `#02283B`
- **Slide / section H1:** 32pt, Poppins Medium weight, color `#02283B`
- **Subtitle / context line (H2):** 18pt, Poppins, color `#48728C` (muted teal)
- **Body / findings text:** 16pt, Poppins, color `#02283B`
- **Footer / page numbers:** 9pt, Poppins, color `#898D91`

### Color palette
| Token | Hex | Use |
|---|---|---|
| Primary text | `#02283B` | All headings and body text |
| Secondary text | `#072B55` | Alternative heading color |
| Subtitle / context | `#48728C` | H2 subtitle lines, environment names |
| Recommendation green | `#0A9268` | All actionable finding items (use √ prefix) |
| Footer gray | `#898D91` | Footer text, page numbers |
| Background | `#FFFFFF` | All content slide backgrounds |
| Section grad start | `#A03291` | Section divider gradient (purple end) |
| Section grad end | `#FF7C66` | Section divider gradient (coral end) |
| Status red | `#CC0000` | Failing / critical indicators |
| Status yellow | `#FFFF00` | Warning / caution indicators |
| Status green | `#0EC38B` | Passing indicators |
| Accent blue | `#0085F0` | Informational accents |

### Slide layout patterns
**Cover slide** — white background:
- Left half: account/customer name prominent, report title "Boomi Platform Health Check", date, analysis window
- Right half: decorative circular image placeholder (use grade badge here instead if no image)
- Grade badge (A/B/C/D) — colored circle, large letter, label below

**Section divider slides** — full-bleed purple→coral gradient (`#A03291` → `#FF7C66`, angled bottom-left to top-right):
- White title text, 46pt, left-aligned, vertically centered
- No footer or logo (clean, full-bleed)
- Use one section divider before each major group: Licensing & Account Details, Runtime Configuration, Infrastructure, Operations, Deployment, Governance, Recommendations

**Content slides** — white background:
- H1 at top: check category name, 32pt Poppins Medium, `#02283B`
- H2 subtitle: environment scope or context, 18pt, `#48728C`
- Status badge: colored pill (red/yellow/green) aligned top-right
- Body: findings as bullet items or short table, 16pt
- Recommendation items: prefixed with `√ ` (checkmark), color `#0A9268`
- Left margin: consistent 0.63–0.74" inset

**Recommendations slide** — white background:
- Table with dark header row (`#02283B` fill, white text)
- Columns: Priority | Area | Finding | Recommended Action
- Priority column uses emoji: 🔴 Critical, 🟠 High, 🟡 Medium, 🟢 Low

**Footer (all content slides):**
- Bottom-left: "Copyright © [YEAR] Boomi, LP or its affiliates. All rights reserved." — 9pt, `#898D91`
- Bottom-right: page number — 9pt, `#898D91`, right-aligned

### Recommendation formatting convention
All actionable findings must use the `√` prefix and `#0A9268` green color:

```
√ Review the 3 production runtimes showing offline status in Environment X
√ Reduce error rate from 18% by investigating the top 3 failing processes
√ Apply role restrictions to the 2 unrestricted production environments
```

### What NOT to do
- Do not use hardcoded `#FF643C` coral or `#142850` navy as primary colors — use the palette above
- Do not use bold for H1 headings — use Poppins Medium weight instead
- Do not place logos on content slides unless the user provides one
- Do not use bright/saturated backgrounds on content slides — white only
- Do not omit the footer copyright line on content slides
- Do not mix status colors (red/yellow/green) outside of status indicator contexts

---

## Step 6.5 — Self-Review Checklist

Before generating the final report, verify each item:

| # | Check | Required? |
|---|---|---|
| 1 | All 6 check categories have a status (pass/warn/fail/info) | Yes — never omit a category |
| 2 | Every `fail` and `warn` finding has at least one recommendation | Yes |
| 3 | Recommendations table has Priority, Area, Finding, and Action columns | Yes |
| 4 | Overall grade (A/B/C/D/F) matches the scoring logic in Step 5 | Yes |
| 5 | Licensing section includes account name, support tier, expiration date | Yes |
| 6 | Runtime inventory includes JVM heap, version, release schedule, disk % | Yes |
| 7 | If `apiGateway` was set to `info` (API not enabled), report notes why | Yes |
| 8 | Boomi design system colors and fonts applied (if HTML/PowerPoint) | Yes for non-inline |
| 9 | CONFIDENTIAL badge included (if PDF/HTML artifact) | Yes for file output |
| 10 | Report footer includes generation date, environment scope, analysis window | Yes for file output |

If any required item is missing, correct it before proceeding to Step 7.

---

## Step 7 — Recommendations format

**Recommendations are always required** — never omit this section. Generate one or more recommendations for every finding, including licensing, runtime configuration, and all six health checks. Use the √ prefix convention and green color (`#0A9268`) when rendered.

| Priority | Area | Finding | Recommended Action |
|---|---|---|---|
| 🔴 Critical | Infrastructure | Production runtime offline | Investigate atom health immediately |
| 🟠 High | Licensing | Support tier expires in 45 days | Renew support agreement with Boomi account team |
| 🟠 High | Runtime Config | JVM heap not set on 2 runtimes | Set `com.boomi.container.maxMemory` to at least 2048m |
| 🟠 High | Operations | 18% error rate | Review top erroring processes |
| 🟡 Medium | Runtime Config | 3 runtimes 2+ releases behind | Enable auto-update or schedule manual runtime upgrades |
| 🟡 Medium | Governance | 2 users with 4+ roles | Apply least-privilege role review |
| 🟢 Low | Deployment | 3 processes not promoted to prod | Schedule promotion sprint |

Pass this list as the `recommendations` array to `boomi_generate_health_report`.

---

## Multi-environment reports

When multiple environments are included, present check results **per environment** where relevant:

- **Runtime Status**: Group runtimes by environment in the inventory table
- **Execution Health**: Show error rate per environment if atom IDs are environment-scoped
- **Environment Consistency**: Show the promotion matrix (non-prod env → production gap count)
- **Dead Processes**: Group by environment

Use a summary row at the top showing overall account-level status, then drill into environment details.

---

## Quick reference: what each tool status means in plain English

Always translate technical statuses into business-friendly language:

| Check | pass | warn | fail |
|---|---|---|---|
| Runtime Status | "All systems operational" | "Minor runtime issues in test environments" | "Production outage detected" |
| Execution Health | "Integrations running smoothly" | "Elevated error rate — monitor closely" | "High failure rate — immediate review needed" |
| Dead Processes | "All integrations active" | "Some integrations may be inactive or stale" | "Significant portion of integrations are idle" |
| Env Consistency | "Deployment pipeline healthy" | "Some changes pending production promotion" | N/A |
| Security | "Access controls properly configured" | "Some governance gaps to address" | "Critical security configuration issues" |
| API Gateway | "APIs operating normally" | "Some APIs have no active consumers" | "API gateway outage detected" |

---

## Error Handling and Recovery

Use this table when any MCP tool call fails during the health check:

| Tool | Error type | Recovery action |
|---|---|---|
| `boomi_get_account_info` | Auth error / 401 | STOP — surface credentials error to user |
| `boomi_get_account_info` | Empty response | Proceed without licensing section; note in report |
| `boomi_health_check_summary` | Timeout | Retry once; if still fails, note partial data, proceed |
| `boomi_health_check_summary` | Auth error | STOP — surface error |
| `boomi_health_check_summary` | Empty `checks` | STOP — ask user to verify environment selection |
| `boomi_list_runtimes` | No runtimes returned | Set runtimeStatus = `info`, note no runtimes found |
| `boomi_get_runtime_details` | Error for one runtime | Skip that runtime; note it by ID in report with ⚠️ |
| `boomi_get_runtime_details` | All runtimes error | Set runtime config section to "unavailable" |
| Best practices WebSearch | No results / blocked | Proceed with built-in guidance; note live docs unavailable |

**General rule:** A single tool failure should never abort the entire health check. Degrade gracefully — note what's missing, set the affected check to `info`, and continue. Only STOP for auth failures (credentials problem requires user action).

---

## Memory and Context — Baseline for Next Session

After delivering the final report, offer to copy a baseline summary the user can paste into the next conversation:

```
## Boomi Account Baseline — [ACCOUNT NAME] — [DATE]
- **Grade:** [A/B/C/D/F]
- **Overall status:** [pass | warn | fail]
- **Checks:** [N pass, N warn, N fail, N info]
- **Key findings:** [1–3 bullet points of the most important findings]
- **Open recommendations:** [count of critical/high items]
- **Analysis window:** [daysBack] days ending [date]
- **Environments:** [scope]
```

Say: _"Here's a baseline snapshot you can paste at the start of your next health check conversation to track improvement over time."_

---

## Feedback Collection

After delivering the report, ask:

> "Was this health check report useful? Anything I should include, skip, or present differently next time?"

If the user provides feedback:
- Acknowledge it specifically
- Note any structural change requests (e.g. "add a cost analysis section", "skip API gateway if we don't use it") so they can inform future invocations of this skill
- If the feedback suggests a standing change to how this skill runs, surface it with: _"You may want to note this preference for future health checks."_

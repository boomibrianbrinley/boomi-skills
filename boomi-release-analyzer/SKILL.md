---
name: boomi-release-analyzer
description: >
  Analyze Boomi platform release notes against deployed integration processes to
  determine upgrade impact. Use this skill when a user asks about Boomi release
  notes, wants to know how a Boomi update affects their account, asks for an
  upgrade impact assessment, or wants to know if a Boomi release will break
  anything. Also trigger when the user mentions "Boomi update", "what changed in
  Boomi", "release notes impact", or "safe to upgrade". The skill fetches live
  release notes via WebSearch, compares them against deployed components from
  the MCP, and produces a scored impact report in Boomi-branded HTML.
---

# Boomi Release Notes Analyzer

Produces a scored, Boomi-branded upgrade impact report by cross-referencing
Boomi platform release notes against the user's deployed integration processes.

## Quick Start

1. **Ask which environment** to analyze (production is default)
2. **Ask for analysis depth**: Quick (executive brief) or Full (technical appendix)
3. **Ask for Boomi version** to analyze — or say "latest"
4. **Fetch release notes** → follow all embedded links
5. **Fetch deployed components** via MCP
6. **Analyze + score** each deployed process
7. **Output** Boomi-branded HTML report

For full analysis workflow → see sections below.
For branded HTML output → read the `boomi-branding` skill before generating HTML.
For PDF output → read the `boomi-reporting` skill.

---

## Step 1 — Fetch Boomi Release Notes

Use **WebSearch** to locate the release notes. Boomi publishes on help.boomi.com
using Docusaurus (client-side rendered), so search engines have cached versions.

**Search queries to try (in order):**
1. `site:help.boomi.com "release notes" [VERSION or YEAR]`
2. `Boomi platform release notes [VERSION] changelog`
3. `help.boomi.com Boomi runtime release [YEAR]`

**After finding the main release notes page:**
- Use WebFetch on every embedded link that references a feature, connector,
  process execution, runtime, or API change — release notes often link out to
  sub-pages with the full technical detail
- Prioritize links about: connectors, process execution, runtime changes,
  API Management, script/map shape changes, data handling

**Sections to capture from release notes:**
- New features and capabilities
- Changed behavior (any existing functionality that works differently)
- Deprecated features (anything being removed)
- Bug fixes affecting runtime behavior
- Connector updates (new versions, authentication changes, endpoint changes)
- Performance / execution changes
- Security patches with behavioral impact

---

## Step 2 — Fetch Deployed Components

Call `boomi_list_deployed_packages` with the selected environment:

```
boomi_list_deployed_packages(
  environment: "[ENV_NAME_OR_ID]",
  daysBack: 365,
  componentType: "process"
)
```

This returns for each deployed process:
- `componentId` — unique identifier
- `componentName` — process name
- `componentType` — always "process" when filtered
- `packageVersion` — deployed version
- `deploymentDate` — when it was last deployed
- `environment` — environment name
- `classification` — PRODUCTION / TEST / etc.

**For Quick (shallow) analysis:** The process names + deployment dates are
sufficient. Cross-reference by connector type inference from process names
(e.g. "Salesforce Sync" implies Salesforce connector usage).

**For Full (deep) analysis:** Additionally call `boomi_get_component_diff` for
each process to retrieve its component XML. From the XML extract:
- Connector shapes: `<shape type="connector" ...>` — identifies connector types
- Map shapes: `<shape type="map" ...>` — data transformation
- Script shapes: `<shape type="script" ...>` — Groovy/JavaScript
- Decision/Branch shapes — flow control
- Cross-reference `connectorType` attributes against release note connector changes

Batch component fetches: do 5 at a time to avoid rate limits.

---

## Step 3 — Impact Scoring

Score each deployed process against each release note change:

| Score | Criteria |
|-------|----------|
| **HIGH** | The process uses a connector, shape, or feature that changed behavior, was deprecated, or requires re-configuration. Immediate action required before upgrading. |
| **MEDIUM** | The process uses something adjacent to a change — may be affected depending on configuration. Review recommended. |
| **LOW** | A new feature is available that could improve this process, but no breaking changes. Optional review. |
| **NONE** | No overlap between this process and the release note changes. |

**Aggregate account-level score:**
- ANY High → account impact: **HIGH**
- No High, any Medium → account impact: **MEDIUM**
- Only Low → account impact: **LOW**
- All None → **NO IMPACT**

---

## Step 4 — Report Structure

### Quick (Shallow) Report

**Executive Brief** — target: 1 page
1. Header: Boomi Release [VERSION] — Impact Assessment for [ACCOUNT/ENV]
2. Overall impact badge (HIGH / MEDIUM / LOW / NO IMPACT)
3. Summary paragraph (3–5 sentences): what changed, what's affected, what to do
4. Impact table: Process Name | Impact Score | Reason (one line)
5. Recommended actions (numbered, most urgent first)
6. Footer: date generated, environment analyzed, process count

### Full (Deep) Report

Deliver the Executive Brief above, PLUS:

**Technical Appendix** — per-process detail
For each High/Medium process:
- Process name + componentId
- Release note changes that apply (quoted)
- Specific shapes/connectors affected in this process
- Recommended remediation steps
- Estimated effort: Low / Medium / High

**Connector Impact Summary**
- Table: Connector Type | Release Note Change | # Processes Affected | Severity

---

## Step 5 — HTML Output

Before generating HTML, read the `boomi-branding` skill for colors, fonts,
and component patterns. Apply these rules:

### Required HTML structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Boomi Release Impact Report — [VERSION]</title>
  <!-- Poppins font -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <!-- Phosphor Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css">
  <style>
    /* Use CSS variables from boomi-branding skill */
    :root {
      --boomi-coral: #FF7C69;
      --boomi-purple: #A93FA5;
      --boomi-navy: #273E59;
      --boomi-white: #FFFFFF;
      --gray-50: #F9FAFB;
      --gray-100: #F3F4F6;
      --gray-200: #E5E7EB;
      --font-sans: "Poppins", -apple-system, sans-serif;
    }
  </style>
</head>
<body>
  <!-- Header banner with gradient -->
  <!-- CONFIDENTIAL badge (amber #FEF3C7 bg, #92400E text) top-right -->
  <!-- Overall impact badge (HIGH=coral, MEDIUM=amber, LOW=blue, NONE=green) -->
  <!-- Summary section -->
  <!-- Impact table -->
  <!-- [If Full report] Technical appendix -->
  <!-- Footer with date + environment + count -->
</body>
</html>
```

### Impact badge colors

| Impact | Background | Text | Border |
|--------|-----------|------|--------|
| HIGH   | `#FDECEA`  | `#B91C1C` | `#FCA5A5` |
| MEDIUM | `#FEF3C7`  | `#92400E` | `#FCD34D` |
| LOW    | `#DBEAFE`  | `#1E40AF` | `#93C5FD` |
| NONE   | `#D1FAE5`  | `#065F46` | `#6EE7B7` |

### Impact table design

```html
<table style="width:100%;border-collapse:collapse;font-family:var(--font-sans);font-size:0.875rem">
  <thead>
    <tr style="background:var(--boomi-navy);color:white">
      <th style="padding:0.75rem 1rem;text-align:left;font-weight:600">Process</th>
      <th style="padding:0.75rem 1rem;text-align:center;font-weight:600">Impact</th>
      <th style="padding:0.75rem 1rem;text-align:left;font-weight:600">Reason</th>
      <th style="padding:0.75rem 1rem;text-align:left;font-weight:600">Action</th>
    </tr>
  </thead>
  <!-- rows with alternating background: white / --gray-50 -->
</table>
```

---

## File Naming

```
boomi_release_impact_[VERSION]_[ENVNAME]_YYYYMMDD.html
```

Example: `boomi_release_impact_v24.2_PRODUCTION_20260330.html`

---

## Interaction Pattern

```
User: "Analyze the latest Boomi release notes for my production environment"
Assistant: "I'll run a Boomi release impact assessment for your production
environment. A couple of quick questions:
1. Do you want a Quick (executive brief) or Full (with technical appendix)?
2. [Optional] Any specific Boomi version, or should I fetch the latest?

I'll fetch the live release notes and cross-reference against all your deployed
processes."
```

---

## Error Handling

- **Release notes not found via search**: Tell the user, ask them to paste the
  URL or copy the release notes text directly
- **No deployed packages returned**: Confirm environment name is correct; list
  available environments
- **Component XML unavailable**: Fall back to name-based inference for that
  process; note this in report with ⚠️ symbol
- **Timeout on bulk component fetch**: Reduce batch size to 3; continue

---

## Anti-Patterns (Never Do)

- Never invent release note content — only use fetched data
- Never mark a process as HIGH impact without a specific release note citation
- Never skip the WebFetch step for embedded links in the release notes page
- Never generate the report without checking for the boomi-branding skill first
- Never omit the footer (date / environment / process count)

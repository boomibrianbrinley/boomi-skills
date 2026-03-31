# Release Notes Analyzer — Prompt Testing Guide

Use these prompts to validate the skill end-to-end. Start with Test 1 (simplest),
confirm it works, then progress to the complex case when you're confident in the setup.

---

## Prerequisites (check before any test)

- [ ] Boomi MCP server is connected in Claude Desktop / claude.ai
- [ ] WebSearch is enabled in your Claude settings
- [ ] You have at least one deployed environment with active processes
- [ ] The `boomi-release-analyzer` skill is loaded in your Claude project
- [ ] The `boomi-branding` skill is loaded (needed for Test 3)

---

## Test 1 — Smoke Test (Quick, Latest Release, Inline Only)

**Purpose:** Confirm the skill activates, WebSearch finds release notes, and MCP returns deployed packages.

**Prompt:**
```
Use the boomi-release-analyzer skill.

Analyze the latest Boomi platform release notes against my deployed processes.
Use my most recently used Boomi account.
Target my Production environment (or the first available environment if Production doesn't exist).
Analysis depth: Quick.
Output: Inline summary only — no HTML file.

Keep it brief — I'm testing the setup, not a full report.
```

**What to verify:**
1. Claude invokes WebSearch for Boomi release notes (you'll see a search tool call)
2. Claude calls `boomi_list_deployed_packages` (you'll see the MCP tool call)
3. The response includes:
   - A clear overall impact score (HIGH / MEDIUM / LOW / NO IMPACT)
   - At least one row in the impact table with a process name
   - A plain-English explanation of what was checked
4. No errors about missing skills or unavailable MCP tools

**Common failures and fixes:**

| Symptom | Fix |
|---------|-----|
| "I can't search the web" | Enable WebSearch in Claude Desktop → Settings |
| "No MCP tools available" | Confirm MCP server is running: `node mcp/stdio.mjs` (should hang silently) |
| "No environments found" | Log into the web app at least once so `data/saved-accounts.json` exists |
| Skill not invoked | In Claude Desktop, open the Project and confirm `boomi-release-analyzer` is listed under skills |

---

## Test 2 — Targeted Environment Test (Specific Environment, Medium Depth)

**Purpose:** Validate environment selection, link-following behavior, and that the right processes are analyzed.

**Prompt:**
```
Use the boomi-release-analyzer skill.

I want an impact assessment for the latest Boomi release notes against
my [ENVIRONMENT NAME] environment.

Replace [ENVIRONMENT NAME] with one of:
  - Your exact production environment name (e.g. "Production", "PROD", "prod-us")
  - Or the first environment returned by boomi_list_environments

Analysis depth: Quick.
Output: Inline summary.

In your response I specifically want to see:
1. Which Boomi release version you analyzed (headline the version clearly)
2. How many processes you found deployed to that environment
3. The top 3 highest-impact processes (or all of them if fewer than 3)
4. At least one embedded link you followed from the release notes, and what additional
   detail it provided
```

**What to verify:**
1. Claude correctly targets the named environment (not a different one)
2. The process count matches what you'd expect from that environment
3. Claude followed at least one embedded release note link (confirms link-following works)
4. The versioned release is clearly identified in the output

---

## Test 3 — Complex Case: Full Technical Analysis with Branded HTML

**Purpose:** End-to-end test of the full workflow — deep component XML analysis, impact scoring
across connector types, and Boomi-branded HTML output.

**Use this when:** You want to validate the complete feature before sharing with stakeholders.

**Prompt:**
```
Use the boomi-release-analyzer skill.

I need a comprehensive upgrade impact assessment. Here are my requirements:

Account: [use my most recently used Boomi account]
Environment: [your production environment name]
Boomi release: [leave blank for latest, or specify a version like "25.2"]
Analysis depth: Both (executive brief + technical appendix)

Step-by-step instructions:
1. Use WebSearch to find the Boomi release notes — search for the most recent
   release on help.boomi.com. Follow every embedded link that refers to:
   connector changes, process execution behavior, runtime updates, script shapes,
   map function changes, or API Management changes.

2. Call boomi_list_deployed_packages for my production environment with daysBack=365.
   List all process-type packages you find.

3. For each deployed process, call boomi_get_component_diff to retrieve component XML.
   From the XML, identify:
   - Which connector types are used (Salesforce, HTTP Client, Database, File, etc.)
   - Whether any map shapes, script shapes, or decision shapes are present
   - The connector operation type (GET/POST/UPSERT/etc.)
   Batch these calls 5 at a time.

4. Cross-reference the release note changes against what you found in each process.
   Score each process: HIGH / MEDIUM / LOW / NONE.

5. Generate two things:
   a. An inline summary with the impact table and top recommended actions
   b. A complete Boomi-branded HTML file saved to disk
      - Read the boomi-branding skill before generating the HTML
      - File name: boomi_release_impact_[VERSION]_PROD_[TODAY_DATE].html
      - Include: gradient header banner, CONFIDENTIAL badge, impact table,
        technical appendix for HIGH and MEDIUM items only, footer with
        process count and date generated

For the technical appendix, for each HIGH or MEDIUM process include:
- The specific release note change that applies (quote it)
- The specific connector/shape in the process that is affected
- Recommended action and estimated effort (Low/Medium/High)
```

**What to verify:**
1. Claude makes multiple `boomi_get_component_diff` calls (deep analysis working)
2. Connector types appear in the impact reasoning (not just process names)
3. Technical appendix is present for HIGH/MEDIUM items
4. HTML file is generated and saved to disk
5. Opening the HTML file shows Boomi branding: Poppins font, coral/navy header, correct badge colors
6. CONFIDENTIAL badge appears in the header

**Performance expectations:**
- Quick analysis: 30–90 seconds
- Full technical analysis: 2–5 minutes (depends on number of deployed processes)
- If you have 50+ processes, component XML fetching will take longer — this is normal

---

## Interpreting Results

### What "HIGH" means in practice
A HIGH score means a deployed process uses a specific connector, shape, or feature
that changed in the analyzed release. **This does not automatically mean it will break** —
it means it warrants manual review before upgrading that runtime or deploying to production.

### What "NONE" means
NONE means no overlap was found between this process and the release changes.
For Quick analysis, this is based on process names and deployment dates.
For Full analysis, this is based on component XML — more reliable.

### When to re-run
- After every minor Boomi release before upgrading production runtimes
- After deploying significant new processes (they won't be in the previous report)
- When the Boomi release notes reference your known connector types

---

## Regression Check Prompts

Use these quick checks after any changes to the skill file:

```
Quick regression: Use boomi-release-analyzer.
Analyze latest Boomi release vs my default environment, quick depth, inline only.
Confirm you: (1) used WebSearch, (2) called boomi_list_deployed_packages,
(3) returned an impact score and table.
```

```
Link-following check: Use boomi-release-analyzer.
Find the latest Boomi release notes. List every embedded link you followed
and one sentence about what each link added to your analysis.
Don't fetch deployed packages yet — just confirm link coverage.
```

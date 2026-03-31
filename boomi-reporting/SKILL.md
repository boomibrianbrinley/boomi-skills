---
name: boomi-reporting
description: >
  Generate executive summaries, execution summaries, and branded PDF scorecards
  for Boomi accounts using the Boomi Platform Explorer MCP. Use this skill whenever
  a user asks about Boomi account activity, wants a summary of what happened on an
  account, asks for an execution report, wants a weekly scorecard, or asks to
  "tell me about my Boomi account". Also trigger when users ask to query Boomi
  executions, audit logs, or want any kind of Boomi reporting output — even if they
  don't use the words "skill" or "report". If the user mentions Boomi and any kind
  of summary, history, activity, or scorecard, use this skill.
---

# Boomi Reporting Skill

Generates polished summaries and PDF scorecards for Boomi accounts. Covers prompt
patterns, summary logic, and PDF generation — all following Boomi brand guidelines.

## Quick Start

1. **List accounts** → ask user to select one (never assume)
2. **Ask for time range** → offer common options or accept custom
3. **Ask for summary type** → executive, execution, or both
4. **Ask for output format** → inline, PDF, or both
5. **Gather data** → run the right tools in parallel
6. **Deliver** → structured summary and/or Boomi-branded PDF

For full details on each step → see `references/prompts.md`
For PDF generation code → see `references/pdf-scorecard.md`
For data tool selection logic → see `references/data-tools.md`

---

## The Golden Interaction Pattern

Always follow this flow. Never skip step 1 — never default to "most recently used"
without asking first, unless the user explicitly says so.

```
Step 1: List available Boomi accounts → present as options
Step 2: Ask which account + what time range + what type of summary
Step 3: Run data tools in parallel based on summary type
Step 4: Deliver output in chosen format
```

**Prompt that drives this flow:**
> "Start by listing my available Boomi accounts and prompt me to select one, and ask
> me for the time range. Then give me an [executive | execution | both] summary based
> on my selections."

---

## Summary Types

### Executive Summary
High-level narrative for stakeholders. Synthesize across tools — not just executions.

**Tools to use:** audit log, executions, environments, runtimes, API gateways
**Output shape:** narrative prose covering:
- Overall health and activity level
- User activity (logins, new users, role changes)
- Configuration changes (connections, extensions, CORS, tokens)
- Component changes or transfers
- Any anomalies or items needing attention

### Execution Summary
Operational/runtime focused. Data-driven, technical audience.

**Tools to use:**
- `boomi_query_executions` — production and scheduled runs
- `boomi_query_audit_log` (filter `type: as.process.test_execution`) — test/dev runs from Build canvas
- `boomi_analyze_execution_anomalies` — anomaly detection on production runs

> **Important:** Test executions triggered from the Boomi Build canvas only exist
> in the audit log — they never appear in `boomi_query_executions`. Always pull
> both sources for a complete picture.

**Output shape:** table + narrative covering:
- Total executions (production + test), broken out separately
- Pass/fail counts for production runs
- Process names, durations, environments
- Errors flagged with details
- Anomaly detection results
- Dev/test volume vs production volume distinction

### Both
Run all tools in parallel and deliver executive narrative first, execution data second.

---

## Prompt Engineering Tips for Boomi Queries

These patterns produce better results with less tool overhead:

| Instead of... | Use... | Why |
|---|---|---|
| "Tell me about my account" | "Give me an executive summary of account [X] over the last 7 days" | Scopes tools to audit log + summary output |
| "What happened with executions?" | "Give me an execution summary of account [X] over the last 7 days" | Single word swap, routes to execution tools only |
| "Check my most recent account" | "...my most recently used Boomi account" | Eliminates disambiguation step |
| Vague time range | Explicit: "last 7 days", "last 30 days" | Avoids unnecessary clarification round-trip |
| No output format specified | Add "as a PDF" or "inline" or "both" | Routes output path without follow-up |

**Key principle:** The word `executive` vs `execution` is the primary signal that
routes which tools are called. Be deliberate about which word you use.

**Account disambiguation:** If the user has multiple accounts and doesn't specify,
always list and ask. Never silently default — the wrong account wastes a tool call
and returns confusing data.

---

## Output Format Options

| Format | When to use |
|---|---|
| **Inline** | Quick checks, conversational context, sharing in chat |
| **PDF** | Weekly reports, stakeholder sharing, filing |
| **Both** | When user wants to review inline first, then export |

Always ask if not specified. Default to inline if the request is clearly conversational.

For PDF generation → read `references/pdf-scorecard.md` before writing any code.

---

## Data Classification

All Boomi account, audit, and execution data is classified as **CONFIDENTIAL**.

- Always include a CONFIDENTIAL badge in the header of any PDF artifact
- Badge: amber/yellow background `#FEF3C7`, dark amber text `#92400E`
- Place top-right in the header banner alongside the document title

---

## File Naming

All generated files must include a date stamp:
`boomi_[report-type]_YYYYMMDD.ext`

Examples:
- `boomi_weekly_scorecard_20260329.pdf`
- `boomi_execution_report_20260329.pdf`
- `boomi_executive_summary_20260329.pdf`

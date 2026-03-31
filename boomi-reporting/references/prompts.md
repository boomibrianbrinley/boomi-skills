# Boomi Reporting — Prompt Reference

## Canonical Prompt Patterns

These are the polished prompts developed through real usage. Use them as-is or
adapt for your context. The key words are highlighted — changing them changes
which tools are invoked.

---

### List Accounts
```
List the Boomi accounts you have access to.
```
- Calls `boomi_list_accounts` once
- Returns clean list, no extra data fetched

---

### Interactive Summary (Recommended Default)
```
Start by listing my available Boomi accounts and prompt me to select one,
and ask me for the time range. Then give me an [executive | execution | both]
summary based on my selections.
```
- Pauses for user input before running any data tools
- Collects: account, time range, summary type in one interaction
- Swap `executive` / `execution` / `both` based on need

---

### Executive Summary (Direct)
```
Give me an executive summary of my most recently used Boomi account
over the last 7 days.
```
- Uses most recently used account — no disambiguation needed
- Triggers: audit log, executions, environments
- Output: narrative prose, stakeholder-ready

---

### Execution Summary (Direct)
```
Give me an execution summary of my most recently used Boomi account
over the last 7 days.
```
- Same structure, single word difference (`execution` vs `executive`)
- Triggers: executions query + anomaly detection only
- Output: table + operational narrative

---

### Scorecard with PDF
```
Give me a weekly scorecard for account [accountId] over the last 7 days
and export it as a PDF.
```

---

## Interaction Design Notes

### Always Ask Before Running
The most important rule: **never silently default to an account**.
Even if there's a "most recently used" account available, ask the user to confirm
unless the prompt explicitly says "most recently used".

```
# Good — user explicitly granted permission to default
"...my most recently used Boomi account..."

# Needs clarification — user has multiple accounts
"Tell me about my Boomi account"
```

### Collecting Inputs Efficiently
Collect all three inputs in a single interaction using the widget:
1. Which account?
2. What time range?
3. Executive, execution, or both?

This avoids 3 separate back-and-forth turns.

### Time Range Defaults
Offer these as quick options:
- Last 7 days ← most common
- Last 14 days
- Last 30 days
- Last 90 days

---

## What Each Summary Type Covers

### Executive Summary Checklist
- [ ] Overall health statement (errors? anomalies?)
- [ ] Active users + new users + role changes
- [ ] Configuration changes (connections, extensions, CORS, tokens)
- [ ] Component changes, deployments, or cross-account transfers
- [ ] Credential handling notes (were passwords copied?)
- [ ] Dev/test activity vs production activity distinction
- [ ] Any items needing attention

### Execution Summary Checklist
- [ ] Total executions in period
- [ ] Pass/fail counts and percentages
- [ ] Process names, durations, environments
- [ ] Error details if any
- [ ] Anomaly detection results (z-score outliers)
- [ ] Test/manual vs scheduled/production distinction

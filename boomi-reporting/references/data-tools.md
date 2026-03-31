# Boomi Reporting — Data Tool Selection Guide

## Tool Routing by Summary Type

| Summary Type | Primary Tools | Secondary Tools |
|---|---|---|
| Executive | `boomi_query_audit_log` | `boomi_query_executions`, `boomi_list_environments`, `boomi_list_runtimes` |
| Execution | `boomi_query_executions`, `boomi_query_audit_log` | `boomi_analyze_execution_anomalies` |
| Both | All of the above | Run in parallel |

> **Why audit log is required for execution summaries:**
> `boomi_query_executions` only captures production and scheduled runs — processes
> that have been deployed and run against an environment. Test/dev executions
> triggered from the Boomi Build canvas (`type: as.process.test_execution`) never
> appear there. They only exist in the audit log. A complete execution summary
> must include both sources to avoid missing development activity entirely.

---

## Tool Reference

### boomi_list_accounts
- **When:** Always first — to present account options to user
- **Params:** None
- **Returns:** accountId, username, lastUsed, addedAt

### boomi_query_audit_log
- **When:** Executive summary — captures all account activity
- **Key params:**
  - `accountId` — required
  - `days` — match user's selected time range
  - `maxResults` — use 500 for comprehensive coverage
- **What to look for:**
  - `type: account` + `action: ON_ENTRY` → user logins
  - `type: user` + `action: ADD` → new users
  - `type: user` + `action: UPDATE` → role changes
  - `type: as.extensions` + `action: EDIT` → connection/extension config changes
  - `type: account` + `action: EDIT` → account-level config (CORS, etc.)
  - `type: as.component` + `action: COPY` → component transfers (check TARGET_ACCOUNT, COPY_PASSWORDS)
  - `type: user.token` + `action: ADD` → API token creation
  - `type: as.process.test_execution` → dev/test runs (not production)
  - `type: as.process.manual_execution` → manual production runs

### boomi_query_executions
- **When:** Execution summary — production process run history
- **Key params:**
  - `accountId` — required
  - `daysBack` — match user's time range
  - `status` — omit for all, or filter to ERROR for issues only
- **Note:** This captures scheduled/production executions.
  Test executions appear in the audit log, not here.

### boomi_analyze_execution_anomalies
- **When:** Execution summary — always run alongside query_executions
- **Key params:**
  - `accountId` — required
  - `daysBack` — match time range
- **Note:** Requires 5+ executions per process to flag anomalies.
  Low-volume accounts may return no anomalies — this is expected.

### boomi_list_environments
- **When:** Executive summary context — understand account structure
- **Use for:** Naming environments in summaries ("Production", "Demo", etc.)

### boomi_list_runtimes
- **When:** Executive summary — check atom/molecule health
- **Use for:** Flagging offline or degraded runtimes

---

## Reading Audit Log Events

### Component Transfer Pattern
```json
{
  "type": "as.component",
  "action": "COPY",
  "properties": {
    "TARGET_ACCOUNT": "wwt-I7UFBZ",
    "COMPONENT_NAME": "Platform API Folder Update",
    "COPY_PASSWORDS": "false"   ← always note this
  }
}
```
- Group all COPY events by TARGET_ACCOUNT
- Always surface COPY_PASSWORDS status — critical for security review
- Note: folder permissions are account-scoped and don't transfer

### User Management Pattern
```json
{ "type": "user", "action": "ADD", "properties": { "USER_ID": "new@example.com" } }
{ "type": "user", "action": "UPDATE", "properties": { "ROLE_NAME": "Developer" } }
```

### Config Change Pattern
```json
{ "type": "account", "action": "EDIT", "properties": { "ORIGIN_LIST": "http://localhost:3000 GET,POST" } }
{ "type": "as.extensions", "action": "EDIT", "properties": { "ENVIRONMENT_ID": "..." } }
```

## Execution Types — Where They Live

This is a critical distinction:

| Execution type | Source | Tool |
|---|---|---|
| Scheduled / production runs | Process Reporting | `boomi_query_executions` |
| Manually triggered production runs | Process Reporting | `boomi_query_executions` |
| Test mode runs (from Build canvas) | Audit Log only | `boomi_query_audit_log` (filter `type: as.process.test_execution`) |

Test executions from the Build canvas **never appear** in `boomi_query_executions`.
They are only recorded in the audit log under `type: as.process.test_execution`.
If you skip the audit log on an execution summary, you will silently miss all
development/test activity — which on active development accounts can be the
majority of total execution volume.

---

## Parallel Tool Execution

For execution summary, run these in parallel:
```
boomi_query_executions(accountId, daysBack)
boomi_query_audit_log(accountId, days, type="as.process.test_execution", maxResults=500)
boomi_analyze_execution_anomalies(accountId, daysBack)
```

For "both" summary type, add these to the parallel batch:
```
boomi_query_audit_log(accountId, days, maxResults=500)   ← full audit log for executive layer
boomi_list_environments(accountId)
```

Never wait for one to complete before starting the others — fetch all data
simultaneously, then synthesize.

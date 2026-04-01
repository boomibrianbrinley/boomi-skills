# Skill Contracts — boomi-skills

Formal cross-skill input/output contracts. Each skill that produces output for another skill must conform to its contract. Skills that consume input must validate against it.

---

## boomi-health-check → boomi-best-practices

**Producer:** `boomi-health-check` (Step 5.5)
**Consumer:** `boomi-best-practices` (Mode 1 — Health Check Enrichment)

### Input contract (what health-check passes to best-practices)

```
{
  check: "runtimeStatus" | "executionHealth" | "deadProcesses" | "envConsistency" | "security" | "apiGateway",
  status: "fail" | "warn",
  finding: string,           // 1-sentence plain-English description of the finding
  category: string           // §1–§6 from best-practices (see mapping table in health-check SKILL.md)
}
```

### Output contract (what best-practices returns to health-check)

```
{
  check: string,             // same check name passed in
  officialGuidance: {
    source: string,          // "help.boomi.com" | "community.boomi.com" | "release notes"
    guidance: string,        // 1-2 sentence summary of official recommendation
    appliesTo: string,       // version range or "all versions"
    link: string | null,     // URL if available from WebSearch
    lastVerified: string     // ISO date of the source found
  }
}
```

**Consumer behavior:** If `officialGuidance` is null or unavailable, health-check proceeds with built-in guidance and notes "Live documentation unavailable" in the report.

---

## boomi-health-check → boomi-generate-health-report (MCP tool)

**Producer:** `boomi-health-check` (Step 6)
**Consumer:** `boomi_generate_health_report` MCP tool

### Input contract

```
{
  accountName: string,
  accountId: string,
  generatedAt: string,          // ISO timestamp
  daysBack: number,
  overallStatus: "pass" | "warn" | "fail",
  summary: { pass: number, warn: number, fail: number, info: number },
  checks: object,               // full checks object from boomi_health_check_summary
  accountDetails: object,       // full object from boomi_get_account_info
  runtimeDetails: object[],     // array from boomi_get_runtime_details
  recommendations: {
    priority: "critical" | "high" | "medium" | "low",
    area: string,
    finding: string,
    action: string
  }[],
  outputDir?: string,
  fileNamePrefix?: string
}
```

### Output contract

```
{
  pptxPath: string,
  htmlPath: string,
  generatedAt: string
}
```

---

## boomi-release-analyzer → boomi-branding

**Producer:** `boomi-release-analyzer` (Step 5)
**Consumer:** `boomi-branding` skill

### Dependency

`boomi-release-analyzer` reads the `boomi-branding` skill before generating HTML. No structured data is passed — it is a read dependency, not a data contract.

**Required fields from boomi-branding:**
- CSS variables (color tokens)
- Font stack (Poppins + fallbacks)
- Impact badge color table
- Table header style

---

## boomi-reporting → boomi-branding

**Producer:** `boomi-reporting` (PDF output)
**Consumer:** `boomi-branding` skill

### Dependency

Same as release-analyzer: read dependency before generating PDF artifacts. Required fields: color tokens, CONFIDENTIAL badge spec, font stack.

---

## Cross-skill compatibility matrix

| From skill | To skill | Contract type | Status |
|---|---|---|---|
| boomi-health-check | boomi-best-practices | Data (structured findings) | Defined above |
| boomi-health-check | boomi_generate_health_report | MCP tool call | Defined above |
| boomi-release-analyzer | boomi-branding | Read dependency | Defined above |
| boomi-reporting | boomi-branding | Read dependency | Defined above |
| boomi-health-check | boomi-reporting | None (separate workflows) | N/A |
| agentic-design-patterns | all skills | Audit / enrichment (read-only) | No data contract needed |

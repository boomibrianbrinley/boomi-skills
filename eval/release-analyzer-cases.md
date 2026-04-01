# Release Analyzer Skill — Evaluation Cases

Benchmark test cases for `boomi-release-analyzer`. Each case defines the input scenario, expected behavior, and pass/fail criteria.

---

## How to use

For each case:
1. Simulate the described account state and release note content
2. Invoke the release analyzer skill
3. Compare actual output against the Expected Output criteria
4. Mark Pass / Fail / Partial for each criterion

---

## Case RA-01 — No Impact

**Scenario:** Release notes contain only UI changes; no connector or runtime changes.

**Input state:**
- Release version: any
- Release notes content: UI updates to Build canvas, new dashboard widget
- Deployed processes: mix of Salesforce, Database, and HTTP connectors

**Expected output:**
- [ ] Account impact: **NO IMPACT**
- [ ] All processes scored **NONE**
- [ ] Upgrade Gate: **Yes — Safe to Upgrade**
- [ ] Upgrade recommendation block present in report
- [ ] No Technical Appendix section (even in Full mode, since no High/Medium)
- [ ] Report footer includes date, environment, process count

---

## Case RA-02 — High Impact: Connector Breaking Change

**Scenario:** Release notes deprecate a connector version in use.

**Input state:**
- Release notes: "Salesforce Connector v3 deprecated; v3-authenticated flows will fail after [date]"
- Deployed processes: 3 processes using Salesforce connector (identified by name inference or XML)

**Expected output:**
- [ ] Account impact: **HIGH**
- [ ] 3 processes scored **HIGH**
- [ ] Each HIGH process has a specific release note citation
- [ ] Upgrade Gate: **Remediate First** or **Do Not Upgrade**
- [ ] Pre-conditions block lists specific action (migrate to Salesforce v4)
- [ ] Technical Appendix (Full mode): each process listed with connector shape and remediation steps

---

## Case RA-03 — Mixed Impact: Medium + None

**Scenario:** Release note changes adjacent to some processes.

**Input state:**
- Release notes: "Database connector v2 behavior change: null handling now throws exception instead of silently skipping"
- Deployed processes: 2 processes with Database connector, 5 with HTTP connector only

**Expected output:**
- [ ] Account impact: **MEDIUM**
- [ ] 2 processes scored **MEDIUM** (Database connector)
- [ ] 5 processes scored **NONE** (HTTP only)
- [ ] Upgrade Gate: **Conditional**
- [ ] Pre-conditions block mentions null handling review
- [ ] No processes incorrectly scored HIGH

---

## Case RA-04 — Empty Environment

**Scenario:** No deployed processes in the selected environment.

**Input state:**
- Environment: "STAGING" (newly created, no deployments)
- `boomi_list_deployed_packages` returns empty array

**Expected output:**
- [ ] Skill does NOT error or abort
- [ ] Account impact: **NO IMPACT**
- [ ] Report notes "No deployed processes found in STAGING"
- [ ] Upgrade Gate: **Yes — Safe to Upgrade** (nothing to break)
- [ ] Report still has footer and date

---

## Case RA-05 — Release Notes Not Found

**Scenario:** Search returns no results for the specified version.

**Input state:**
- User specifies version: "v99.0" (fictional)
- All 3 WebSearch queries return no results

**Expected output:**
- [ ] Skill does NOT guess or invent release note content
- [ ] Skill informs user: "I couldn't find release notes for v99.0. Please paste the URL or release notes text."
- [ ] Skill does NOT generate a report with fabricated findings
- [ ] Skill does NOT mark any process as HIGH without a citation

---

## Case RA-06 — Upgrade Gate: Do Not Upgrade

**Scenario:** Critical runtime change with no workaround.

**Input state:**
- Release notes: "JVM version requirement changes from Java 11 to Java 17 — Java 11 runtimes will not start after upgrade"
- Account: All runtimes running Java 11 (confirmed via `boomi_get_runtime_details`)

**Expected output:**
- [ ] Account impact: **HIGH**
- [ ] Upgrade Gate: **Do Not Upgrade** (🔴)
- [ ] Reason block cites Java version requirement
- [ ] Pre-conditions block: "Upgrade all runtimes to Java 17 before applying the Boomi update"
- [ ] At least one 🔴 Critical recommendation in report

---

## Case RA-07 — Quick vs Full Mode

**Scenario:** Same account, same release notes, different depth requested.

**Input state:**
- 1 HIGH process, 3 MEDIUM processes
- Quick mode requested first, then Full mode

**Quick mode expected output:**
- [ ] Executive Brief only (1 page equivalent)
- [ ] Impact table present
- [ ] No Technical Appendix
- [ ] Upgrade Gate present

**Full mode expected output:**
- [ ] Executive Brief present
- [ ] Technical Appendix present for HIGH and MEDIUM processes
- [ ] Connector Impact Summary table present
- [ ] All Quick mode elements still present

---

## Case RA-08 — No Release Note Citations for HIGH

**Scenario:** Skill attempts to mark process as HIGH without citation.

**Input state:** Any scenario.

**Anti-pattern check:**
- [ ] If skill marks any process HIGH, it MUST include a quoted release note passage or specific cited change
- [ ] A process named "Salesforce_Sync" is NOT sufficient evidence — connector type inference only → MEDIUM at most without XML confirmation

---

## Scoring guide

| Pass rate | Assessment |
|---|---|
| 8/8 cases pass | Skill is production-ready |
| 6-7/8 pass | Minor gaps — document and track |
| 4-5/8 pass | Significant issues — do not ship |
| < 4/8 pass | Skill needs rework |

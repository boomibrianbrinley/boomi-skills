# Health Check Skill — Evaluation Cases

Benchmark test cases for `boomi-health-check`. Each case defines the input scenario, expected behavior, and pass/fail criteria. Use these when validating changes to the skill or comparing outputs across model versions.

---

## How to use

For each case:
1. Simulate the described account state (or use a real account that matches)
2. Invoke the health check skill
3. Compare actual output against the Expected Output criteria
4. Mark Pass / Fail / Partial for each criterion

---

## Case HC-01 — All Green Account

**Scenario:** Healthy account with no issues.

**Input state:**
- 2 environments: Production, Test
- 3 runtimes: all ONLINE, all within 1 release of current, JVM heap ≥ 2GB, disk < 70%
- Error rate: 2% over 30 days
- All deployed processes active
- All non-prod processes promoted to production
- Security: roles properly restricted
- API Gateway: online, all APIs have subscribers

**Expected output:**
- [ ] Overall grade: **A (Healthy)**
- [ ] `overallStatus: pass`
- [ ] All 6 checks show `pass`
- [ ] Recommendations section present but contains only Low/Advisory items or is empty
- [ ] No `warn` or `fail` badges in report
- [ ] Runtime inventory table present with version, JVM, disk columns

---

## Case HC-02 — Production Runtime Offline

**Scenario:** Critical infrastructure failure.

**Input state:**
- 1 production environment
- 1 production runtime: OFFLINE
- Error rate: 45% (executions failing due to runtime being down)
- Everything else nominal

**Expected output:**
- [ ] Overall grade: **F (Critical)**
- [ ] `runtimeStatus: fail`
- [ ] `executionHealth: fail`
- [ ] At least one 🔴 Critical recommendation for production runtime
- [ ] Recommendation contains "Investigate atom health" or equivalent
- [ ] Business language translation: "Production outage detected"

---

## Case HC-03 — Expiring Support + Elevated Error Rate

**Scenario:** Mixed warning signals, no critical failures.

**Input state:**
- Support expiration: 45 days from now
- Error rate: 8% over 30 days
- 2 runtimes 2 releases behind
- Everything else nominal

**Expected output:**
- [ ] Overall grade: **C (Needs Attention)** (2+ warns)
- [ ] `executionHealth: warn`
- [ ] Licensing section flags expiration as high priority
- [ ] At least one 🟠 High recommendation for support renewal
- [ ] At least one 🟡 Medium recommendation for runtime version
- [ ] `runtimeStatus` check reflects version staleness

---

## Case HC-04 — API Management Not Enabled

**Scenario:** Account without API Management entitlement.

**Input state:**
- `apiType`: null or "NONE"
- All other checks: pass
- 1 production runtime online

**Expected output:**
- [ ] `apiGateway: info` (not fail)
- [ ] Report notes "API Management not enabled on this account tier"
- [ ] No API Gateway warning/error in recommendations
- [ ] Grade unaffected by API gateway status
- [ ] Step 0 discovery sets API flag = false before reaching Step 3

---

## Case HC-05 — Auth Failure on boomi_health_check_summary

**Scenario:** Credentials revoked mid-run.

**Input state:**
- `boomi_get_account_info` succeeds
- `boomi_health_check_summary` returns auth error (401)

**Expected output:**
- [ ] Skill STOPs after auth error
- [ ] User receives clear error message about credentials
- [ ] No partial report generated
- [ ] Retry logic NOT triggered (auth errors don't retry)

---

## Case HC-06 — Large Multi-Environment Account (10+ runtimes)

**Scenario:** Enterprise account with many environments and runtimes.

**Input state:**
- 5 environments: 2 Production, 3 Test
- 12 runtimes total; prioritize top 10 (production first)
- Mixed JVM heap settings
- 1 test environment runtime OFFLINE

**Expected output:**
- [ ] Report groups runtimes by environment
- [ ] Only 10 runtimes detailed (production prioritized in selection)
- [ ] `runtimeStatus: warn` (non-prod offline, not prod)
- [ ] Runtime inventory table present for all analyzed runtimes
- [ ] Grade no worse than **B** if only test runtime offline

---

## Case HC-07 — Feedback Collection

**Scenario:** Post-report feedback flow.

**Input state:** Any completed health check.

**Expected output:**
- [ ] Skill asks feedback question after delivering report
- [ ] Skill does not ask multiple feedback questions
- [ ] If user says "skip the API section next time", skill acknowledges
- [ ] Skill offers baseline copy-paste block after feedback exchange

---

## Scoring guide

| Pass rate | Assessment |
|---|---|
| 7/7 cases pass | Skill is production-ready |
| 5-6/7 pass | Minor gaps — document and track |
| 3-4/7 pass | Significant regressions — do not ship |
| < 3/7 pass | Skill needs rework |

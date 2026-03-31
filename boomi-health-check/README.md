# boomi-health-check

**A professional Boomi account health assessment — in minutes, not days.**

This skill runs a structured health check across your entire Boomi account and produces
the same kind of report a Boomi consultant would deliver — covering runtime infrastructure,
integration performance, security posture, deployment consistency, and API gateway health.
The output is a graded report (A through F) with prioritized recommendations you can act on.

---

## What it checks

| Area | What it looks at |
|---|---|
| **Runtime Infrastructure** | Are all your Atoms and Molecules online? Are they running current software versions? Is JVM memory configured correctly? Is disk space healthy? |
| **Integration Performance** | What's your error rate over the last 30 days? Which integrations are failing most often? |
| **Inactive Integrations** | Which integrations are deployed but never actually run? These are candidates for cleanup or investigation. |
| **Deployment Pipeline** | Are integrations promoted consistently from test to production? Or are there changes sitting in non-production that never made it to prod? |
| **Security & Governance** | Do users have appropriate role assignments? Are production environments properly restricted? |
| **API Gateway** | Are your API gateways online? Do your published APIs have active subscribers? |
| **Licensing & Account Details** | What's your support tier and expiration date? Are you within your entitlements? |

Each area is scored **pass / warn / fail**, and the overall account gets a letter grade:

| Grade | Meaning |
|---|---|
| **A** | Everything looks healthy |
| **B** | Minor items to monitor |
| **C** | Several issues that need attention |
| **D** | One or more critical failures |
| **F** | Production is down or severely impacted |

---

## What you get

Claude produces a full health check report with:

- **Executive summary** — overall grade, score card, and key findings at a glance
- **Per-check findings** — what was found, what it means in plain English, and what to do about it
- **Prioritized recommendations** — ranked from critical to low, with specific actions
- **Runtime inventory** — details on every Atom and Molecule in scope
- **Official Boomi guidance** — each finding is enriched with live documentation from
  `help.boomi.com` and the Boomi Community so recommendations are grounded in Boomi's
  own best practices, not just general advice

**Report formats:**
- **Inline summary** — fast, conversational, good for a quick check-in
- **Branded HTML report** — standalone file you can share with your team or a customer
- **PowerPoint presentation** — professionally formatted slides in Boomi's visual identity,
  ready to present without any editing

---

## When to use it

Ask Claude something like:

- *"Run a health check on my Boomi account"*
- *"How healthy is our Boomi production environment?"*
- *"Generate a Boomi health report for the last 30 days"*
- *"Give me a risk assessment of our Boomi platform"*
- *"Create a Boomi health check presentation for our customer"*

---

## Install this skill only

### Claude Desktop (Mac)

Run the installer in your terminal, then restart Claude Desktop:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-health-check
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

Open PowerShell and run:

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-health-check
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-health-check
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-health-check ~/.claude/skills/boomi-health-check
```

> **Verifying the install:** In Claude Desktop, start a new conversation and ask
> *"What skills do you have available?"* — you should see `boomi-health-check` listed.

---

## Requirements

- The **Boomi Platform API Explorer** MCP server must be running and connected to your Boomi
  account — this is how Claude pulls live data from your account
- The **`boomi-best-practices`** skill should also be installed — it enriches each health
  check finding with live documentation from Boomi's official help site and community
- The **`boomi-branding`** skill should be installed if you want branded HTML or PowerPoint output

---

## Add to a specific project (submodule)

```bash
git submodule add -b main https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-skills
git submodule update --init --recursive
git commit -m "Add boomi-skills submodule"
```

After cloning a project that uses this submodule:

```bash
git submodule update --init --recursive
```

---

## Updating

```bash
cd ~/boomi-skills && git pull
```

---

## Related skills

- **`boomi-best-practices`** — Enriches findings with official Boomi guidance (recommended)
- **`boomi-branding`** — Required for branded HTML and PowerPoint report output
- **`boomi-release-analyzer`** — Focused upgrade impact assessment for a specific Boomi release

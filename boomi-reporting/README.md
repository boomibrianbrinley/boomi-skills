# boomi-reporting

**Turn your Boomi account activity into a polished report — in seconds.**

This skill generates two types of reports from your live Boomi account data: an executive
summary for stakeholders who need the big picture, and an execution summary for your
operations team who needs the technical detail. Both can be delivered inline in the chat
or exported as a branded PDF scorecard.

---

## What it produces

### Executive Summary
The "what happened on our platform" report for managers and stakeholders.

Covers everything that changed on your account over a selected time period:
- Overall account health and activity level
- Who logged in, what roles changed, any new users added
- Configuration changes — connections modified, extensions updated, CORS settings, API tokens
- Component changes or transfers between environments
- Anything unusual or worth flagging

### Execution Summary
The "how did our integrations run" report for your operations or development team.

Covers everything related to how your integrations performed:
- Total executions across production and development environments
- Pass/fail breakdown with error details
- Which processes ran the most, which failed the most
- How long processes took to run
- Anomaly detection — processes that behaved differently than their historical baseline
- Development/test runs (from the Boomi Build canvas) shown separately from production runs

### Both
Run everything at once. Executive narrative first, execution data second.

---

## Output formats

| Format | Best for |
|---|---|
| **Inline** | Quick checks, sharing in chat, reviewing before exporting |
| **PDF scorecard** | Weekly reports, customer deliverables, filing for records |
| **Both** | Review inline first, then export the PDF |

All PDF output is Boomi-branded and marked **CONFIDENTIAL** automatically.

---

## When to use it

Ask Claude something like:

- *"Give me an executive summary of my Boomi account for the last 7 days"*
- *"Generate a weekly execution report as a PDF"*
- *"Tell me what happened on our Boomi account this month"*
- *"Run an execution summary for our production environment"*
- *"Create a Boomi scorecard for last week"*

Claude will ask you to confirm which account and time range before running anything —
it never assumes or defaults to a previous selection.

---

## Install this skill only

### Claude Desktop (Mac)

Run the installer in your terminal, then restart Claude Desktop:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-reporting
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

Open PowerShell and run:

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-reporting
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-reporting
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-reporting ~/.claude/skills/boomi-reporting
```

> **Verifying the install:** In Claude Desktop, start a new conversation and ask
> *"What skills do you have available?"* — you should see `boomi-reporting` listed.

---

## Requirements

| Dependency | Required for | Notes |
|---|---|---|
| **Boomi Platform API Explorer** (MCP server) | All report types | Must be running and connected to your Boomi account. Provides `boomi_query_executions`, `boomi_query_audit_log`, `boomi_analyze_execution_anomalies`, and `boomi_list_accounts`. |
| **Python 3** with `reportlab` | PDF scorecard output | Install with `pip install reportlab`. Only needed if you request PDF output — inline summaries have no Python dependency. |
| **`boomi-branding`** skill | PDF output formatting | Recommended. Ensures PDF scorecards use correct Boomi colors, fonts, and layout. |

**Installing reportlab:**
```bash
pip install reportlab
# or, in a virtual environment:
uv pip install reportlab
```

PDF generation also downloads the Poppins font files from Google Fonts at runtime —
an internet connection is required the first time a PDF is generated on a new machine.

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

Restart Claude Desktop after pulling updates.

---

## Related skills

- **`boomi-branding`** — Required for branded PDF scorecard output
- **`boomi-health-check`** — Deeper platform health assessment with graded findings
- **`boomi-best-practices`** — Enriches findings with official Boomi guidance

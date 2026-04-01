# Boomi Skills

Centralized [Claude Code](https://claude.ai/code) skills for Boomi projects.

Skills in this repo provide Claude with Boomi-specific design standards, coding patterns,
and reference material so that any project can produce consistent, on-brand output without
repeating the same context in every conversation.

> **⚠ Temporary home.** This repo is a shared starting point for the team while we work toward
> a permanent shared repository under a team or organization license. Once that's in place, the
> canonical location will move and this repo will redirect accordingly. In the meantime, treat
> this as the working source of truth.

---

## Available Skills

### [`boomi-health-check`](boomi-health-check/README.md)
A professional Boomi account health assessment covering runtime infrastructure, integration
performance, security, deployment consistency, and API gateway health. Produces a graded
report (A–F) with prioritized recommendations — as a quick summary, a branded HTML file,
or a PowerPoint presentation ready to share with a customer.

### [`boomi-release-analyzer`](boomi-release-analyzer/README.md)
Answers "will this Boomi update break anything?" Fetches live release notes, cross-references
them against your deployed integrations, and scores each one (HIGH / MEDIUM / LOW / NONE).
Produces an upgrade impact report so you know exactly what needs attention before you upgrade.

### [`boomi-branding`](boomi-branding/README.md)
The Boomi design playbook for Claude — colors, typography, logos, icons, UI component patterns,
and a ready-to-use HTML template. Any output Claude produces will look like it came from
Boomi's own design team. Used automatically by other skills when generating reports.

### [`boomi-best-practices`](boomi-best-practices/README.md)
Ensures every recommendation Claude makes about your Boomi account is backed by official
Boomi documentation. Before giving advice, it searches `help.boomi.com`, the Boomi Community,
and release notes in real time — so guidance is current, cited, and trustworthy.

### [`boomi-reporting`](boomi-reporting/README.md)
Generates executive summaries and execution reports from your live Boomi account data.
Ask for a quick inline summary or a branded PDF scorecard — covering account activity,
user changes, configuration events, integration performance, and anomaly detection.

### [`global-utilities`](global-utilities/README.md)
General-purpose utilities available in any project or conversation: public IP lookup,
current date/time in any timezone, DNS record resolution, and SSL certificate checking.
No project-specific context required — useful everywhere.

### [`git-conventions`](git-conventions/README.md)
Consistent git patterns for every session: commit message format, branch naming, PR
structure, submodule workflows, staging safety rules, and standard `.gitignore` defaults.
Install once and Claude applies these conventions automatically across all projects.

---

## MCP Server

### [`mcp-server`](mcp-server/README.md)
Exposes all skills to **Claude Desktop, Gemini CLI, Cursor, and any other MCP-compatible
AI tool** — not just Claude Code CLI. The server auto-starts when the AI tool launches,
provides `list_skills`, `get_skill`, and `update_skills` tools, and works on macOS,
Linux, and Windows 11. A one-time `node register.mjs` wires it into every detected tool
automatically.

---

## Installation

Skills are installed into `~/.claude/skills/` — a directory that both **Claude Desktop**
and **Claude Code CLI** load automatically. Install once and every project has access.

### Claude Desktop (Mac) — install all skills

Open Terminal and run:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)
```

Then **quit and reopen Claude Desktop**. Skills load on startup.

### Claude Desktop (Windows) — install all skills

Open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
```

Then **quit and reopen Claude Desktop**. Skills load on startup.

### Claude Code CLI (macOS / Linux / WSL) — install all skills

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)
```

No restart needed — skills are available in your next Claude Code session.

### Install a single skill

Add the skill name as an argument to install only what you need:

```bash
# Mac / Linux
bash <(curl -fsSL .../install.sh) boomi-health-check

# Windows PowerShell (after cloning)
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-health-check
```

> **Verifying the install:** In Claude Desktop or Claude Code, ask
> *"What skills do you have available?"* — installed skills will be listed.

> **Windows note:** Symlinks require Developer Mode or Administrator privileges.
> The PowerShell installer falls back to Directory Junctions automatically if neither is available.

---

## Adding to a Specific Project (Submodule)

For projects shared via `git clone` where collaborators need the skills without running
the installer:

### macOS / Linux

```bash
# From the project root
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/add-to-project.sh)
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/add-to-project.ps1 | iex
```

Or manually:

```bash
git submodule add -b main https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-skills
git submodule update --init --recursive
```

After cloning a project that uses this submodule:

```bash
git submodule update --init --recursive
```

---

## Updating Skills

> For the full reference — editing, pushing, updating submodule pins, and new machine setup — see **[UPDATING-SKILLS.md](UPDATING-SKILLS.md)**.

Edit files directly in your local clone:

```bash
cd ~/boomi-skills
# edit files...
git add -A && git commit -m "boomi-branding: describe change" && git push
```

Changes are live immediately in any project using the global `~/.claude/skills/` symlinks.
Projects using the submodule approach can pull the update with:

```bash
git submodule update --remote skills/boomi-skills
git add skills/boomi-skills && git commit -m "Update boomi-skills to latest"
```

---

## Architecture

See [`boomi-branding/SKILL-SHARING-STRATEGY.md`](boomi-branding/SKILL-SHARING-STRATEGY.md)
for the full A+C+D centralization strategy this repo implements.

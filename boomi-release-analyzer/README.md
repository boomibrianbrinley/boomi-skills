# boomi-release-analyzer

**"Will this Boomi update break anything?"**

This skill answers that question. When Boomi releases a platform update, it reads the release notes,
cross-references them against every integration you have deployed, and tells you exactly what's at
risk — before you upgrade.

---

## What it does

When you ask Claude to analyze a Boomi release, it will:

1. **Fetch the live release notes** from Boomi's documentation site for the version you specify
   (or the latest release if you don't specify one)
2. **Pull your deployed integrations** from your Boomi account
3. **Score each integration** against the changes in that release:
   - 🔴 **HIGH** — This integration uses something that changed. Action required before upgrading.
   - 🟡 **MEDIUM** — This integration may be affected. Worth reviewing.
   - 🟢 **LOW** — A new feature is available that could improve this integration, but nothing is broken.
   - ⚪ **NONE** — No overlap. This integration is unaffected.
4. **Produce an overall account impact rating** (HIGH / MEDIUM / LOW / NO IMPACT)
5. **Generate a report** — either a concise executive brief or a full technical breakdown with
   per-integration detail and recommended remediation steps

---

## When to use it

Ask Claude something like:

- *"Analyze the latest Boomi release notes for my production environment"*
- *"Will the new Boomi update break any of my integrations?"*
- *"What changed in Boomi this quarter and does it affect us?"*
- *"Is it safe to upgrade our Boomi runtime?"*
- *"Give me an upgrade impact report for Boomi version 24.2"*

---

## Report types

**Quick (Executive Brief)** — Best for a fast go/no-go decision
- One-page summary with overall impact rating
- Impact table showing which integrations are affected and why
- Prioritized list of actions before upgrading

**Full (Technical Appendix)** — Best for your development team
- Everything in the Quick report, plus:
- Per-integration detail: which connectors or shapes are affected, and how
- Connector impact summary across all integrations
- Estimated remediation effort per affected integration

The report is delivered as a branded HTML file you can save, share, or print.

---

## Install this skill only

### macOS / Linux / WSL / Git Bash

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-release-analyzer
```

### Windows (PowerShell)

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-release-analyzer
```

### Manual

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-release-analyzer ~/.claude/skills/boomi-release-analyzer
```

---

## Requirements

- The **Boomi Platform API Explorer** MCP server must be running and connected to your Boomi
  account — this is how Claude pulls your deployed integrations
- The **`boomi-branding`** skill should also be installed for properly formatted HTML reports

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

- **`boomi-branding`** — Required for branded HTML report output
- **`boomi-health-check`** — Broader account health assessment (runtime, security, execution health)
- **`boomi-best-practices`** — Boomi official guidance, used to enrich recommendations

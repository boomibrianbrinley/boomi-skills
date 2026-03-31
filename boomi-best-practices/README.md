# boomi-best-practices

A [Claude Code](https://claude.ai/code) skill providing the official Boomi best practices
framework for evaluating account configurations, enriching health check findings, and
generating improvement recommendations.

Use this skill when reviewing Boomi account health, generating recommendations, or when
another skill (such as `boomi-health-check`) requests best practices enrichment.

> **Live web search:** This skill always performs a live search against `help.boomi.com`,
> `community.boomi.com`, and Boomi release notes before generating recommendations.
> It never relies on training data alone.

---

## What's included

| File | Contents |
|---|---|
| `SKILL.md` | Skill definition, framework, and usage instructions for Claude |
| `SOURCES.md` | Authoritative Boomi documentation sources and search strategy |

---

## Install this skill only

### macOS / Linux / WSL / Git Bash

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-best-practices
```

### Windows (PowerShell)

```powershell
# Clone first, then install the specific skill:
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-best-practices
```

### Manual (any platform)

```bash
# 1. Clone the skills repo (or pull if already cloned)
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills

# 2. Symlink just this skill into Claude's global skills directory
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-best-practices ~/.claude/skills/boomi-best-practices
```

Once linked, Claude Code loads this skill automatically in every project session — no
per-project configuration needed.

---

## Add to a specific project (submodule)

If you need the skill to travel with a project repo (so collaborators get it on `git clone`):

```bash
# From your project root
git submodule add -b main https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-skills
git submodule update --init --recursive
git commit -m "Add boomi-skills submodule"
```

The skill will be available at `skills/boomi-skills/boomi-best-practices/`.

After cloning a project that already has the submodule:

```bash
git submodule update --init --recursive
```

---

## Updating

```bash
cd ~/boomi-skills
git pull
```

Changes are live immediately if you're using the global symlink approach.
If using a submodule in a project, also run:

```bash
git submodule update --remote skills/boomi-skills
git add skills/boomi-skills && git commit -m "Update boomi-skills to latest"
```

---

## Related skills

- **`boomi-branding`** — Boomi visual identity and UI standards
- **`boomi-health-check`** — Account health checks that call this skill for enrichment

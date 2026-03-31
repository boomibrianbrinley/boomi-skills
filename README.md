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

### `boomi-branding`
Visual identity and UI standards for Boomi-branded outputs.

| Reference file | Contents |
|---|---|
| `references/colors.md` | Brand color palette, CSS variables, usage rules |
| `references/icons.md` | Phosphor Icons setup, common patterns, known rendering pitfalls |
| `references/logos.md` | Inline SVG wordmark (preferred), base64 CSS fallbacks, sizing rules |
| `references/components.md` | Card, badge, table, and layout patterns |
| `references/diagrams.md` | Architecture diagram conventions |
| `references/html-template.md` | Starter HTML template with Boomi theme wired up |

### `boomi-best-practices`
Integration and development standards for Boomi AtomSphere projects.

---

## Installation

### macOS / Linux / WSL / Git Bash

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
```

Both scripts:
1. Clone this repo to `~/boomi-skills/`
2. Create `~/.claude/skills/` (or `%USERPROFILE%\.claude\skills\` on Windows)
3. Symlink each skill in — Claude Code loads them automatically in every project

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

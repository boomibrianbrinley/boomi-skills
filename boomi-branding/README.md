# boomi-branding

A [Claude Code](https://claude.ai/code) skill providing Boomi visual identity standards,
UI component patterns, and brand reference material.

Use this skill when building Boomi-branded HTML reports, dashboards, UI components, or
any output that should conform to Boomi's design system.

---

## What's included

| File | Contents |
|---|---|
| `references/colors.md` | Brand color palette, CSS variables, semantic usage rules |
| `references/icons.md` | Phosphor Icons setup, common patterns, known rendering pitfalls |
| `references/logos.md` | Inline SVG wordmark (preferred), base64 CSS fallbacks, sizing rules |
| `references/components.md` | Card, badge, table, and layout patterns aligned to Boomi Exosphere |
| `references/diagrams.md` | Architecture diagram conventions |
| `references/html-template.md` | Starter HTML template with Boomi theme, fonts, and CSS wired up |

---

## Install this skill only

### macOS / Linux / WSL / Git Bash

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-branding
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
# Then in the same session:
# The script installs all discovered skills — to install only this one, clone first then run:
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-branding
```

### Manual (any platform)

```bash
# 1. Clone the skills repo (or pull if already cloned)
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills

# 2. Symlink just this skill into Claude's global skills directory
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-branding ~/.claude/skills/boomi-branding
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

The skill will be available at `skills/boomi-skills/boomi-branding/`.

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

## Design system reference

This skill references the [Boomi Exosphere design system](https://exosphere.boomi.com).
Where specific component specs or color tokens are documented in Exosphere, those take
precedence over anything in this skill.

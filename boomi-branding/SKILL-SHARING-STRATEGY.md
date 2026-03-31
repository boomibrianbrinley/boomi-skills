# Skill Centralization Strategy — Boomi Skills

**Status: Implemented** — this document reflects the live architecture as of March 2026.

---

## Architecture: Option A + C + D

Three layers, each serving a distinct purpose:

| Layer | Option | What it does | Status |
|-------|--------|--------------|--------|
| **Source of truth** | D — `boomi-skills` repo | Canonical home; version-controlled; editable | ✅ Live at `github.com/boomibrianbrinley/boomi-skills` |
| **Always-on for your machine** | C — `~/.claude/skills/` global | Symlinks into local repo clone; zero per-project config | ✅ Wired on Brian's machine |
| **Portability to collaborators** | A — Git submodule | Remote pointer in consuming repos; resolved via `git submodule update` | ✅ Added to `boomi-platform-api-explorer` |

---

## Why Not Option B (local filesystem symlink)?

A filesystem symlink can only point to a **local path** — it cannot reference a URL or remote
resource. The submodule (Option A) is the correct mechanism for a "pointer to a remote resource":

| What you want | What actually does it |
|---|---|
| "Symlink to a web resource" | Git submodule — remote pointer, resolved on demand |
| Always-current on your machine | `~/.claude/skills/` symlinked to local clone (Option C) |
| Bootstrap a new machine / collaborator | `install.sh` / `install.ps1` (Option D) |

---

## Live Setup (as implemented)

### Skills repo
- **GitHub:** `https://github.com/boomibrianbrinley/boomi-skills` (public)
- **Local clone:** `~/boomi-skills/`
- **Skills inside:**
  - `boomi-branding/` — visual identity, icons, logos, components
  - `boomi-best-practices/` — integration and development standards

### Global symlinks (Brian's machine)
```
~/.claude/skills/boomi-branding       → ~/boomi-skills/boomi-branding
~/.claude/skills/boomi-best-practices → ~/boomi-skills/boomi-best-practices
```
Claude Code loads these automatically in every project session.

### Submodule in `boomi-platform-api-explorer`
```
skills/boomi-skills/  →  github.com/boomibrianbrinley/boomi-skills (pinned commit)
```
Provides portability — anyone who clones the project and runs
`git submodule update --init --recursive` gets the skills without needing the installer.

---

## Day-to-Day Workflow

### Editing a skill
```bash
cd ~/boomi-skills
# edit files in boomi-branding/ or boomi-best-practices/
git add -A && git commit -m "boomi-branding: describe change" && git push
```
Changes are live immediately via the global symlinks. No restart needed.

### Updating the submodule pin in a project
```bash
# From inside boomi-platform-api-explorer (or any consuming project)
git submodule update --remote skills/boomi-skills
git add skills/boomi-skills
git commit -m "Update boomi-skills to latest"
git push
```

### Bootstrap a new machine
```bash
# macOS / Linux / WSL
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)

# Windows PowerShell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
```

### Add skills to a new project
```bash
# macOS / Linux
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/add-to-project.sh)

# Windows PowerShell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/add-to-project.ps1 | iex
```

---

## Adding a New Skill

```bash
cd ~/boomi-skills
mkdir my-new-skill
# create SKILL.md and reference files
git add my-new-skill/ && git commit -m "Add my-new-skill" && git push

# Wire it globally (or re-run install.sh which auto-discovers all skills)
ln -s ~/boomi-skills/my-new-skill ~/.claude/skills/my-new-skill
```

The `install.sh` / `install.ps1` scripts auto-discover any folder containing a `SKILL.md`,
so re-running the installer is sufficient for new skills.

---

## Planned Skills (fast follows)

| Skill | Status |
|---|---|
| `boomi-branding` | ✅ Live |
| `boomi-best-practices` | ✅ Live (initial version) |

---

## File Map

```
boomi-skills/                    ← repo root (github.com/boomibrianbrinley/boomi-skills)
  README.md
  install.sh                     ← macOS/Linux/WSL bootstrap
  install.ps1                    ← Windows PowerShell bootstrap
  add-to-project.sh              ← submodule helper (bash)
  add-to-project.ps1             ← submodule helper (PowerShell)
  boomi-branding/
    SKILL.md
    SKILL-SHARING-STRATEGY.md    ← this file
    references/
      colors.md
      icons.md
      logos.md
      components.md
      diagrams.md
      html-template.md
  boomi-best-practices/
    SKILL.md
    SOURCES.md
```

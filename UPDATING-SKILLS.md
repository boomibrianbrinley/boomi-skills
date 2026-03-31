# How to Update the Boomi Skills

All skill content lives in the **`boomi-skills` repo** (`github.com/boomibrianbrinley/boomi-skills`),
not in this project. This file explains how to make changes and keep everything in sync.

---

## Where things live

| Location | What it is |
|---|---|
| `~/boomi-skills/` | Local clone of the canonical skills repo |
| `~/.claude/skills/boomi-branding` | Symlink → `~/boomi-skills/boomi-branding` (auto-loaded by Claude) |
| `~/.claude/skills/boomi-best-practices` | Symlink → `~/boomi-skills/boomi-best-practices` |
| `skills/boomi-skills/` | Git submodule in this project (pinned to a commit) |

---

## Making a skill update

### 1. Edit the files in the canonical location

```bash
cd ~/boomi-skills
# edit any file inside boomi-branding/ or boomi-best-practices/
```

Changes are **immediately visible to Claude** on your machine the moment you save —
no restart needed, because `~/.claude/skills/` symlinks resolve to the live files.

### 2. Commit and push to the skills repo

```bash
cd ~/boomi-skills
git add -A
git commit -m "boomi-branding: describe what changed"
git push
```

### 3. Update the submodule pin in consuming projects

Each project that uses `boomi-skills` as a submodule holds a pinned commit reference.
After pushing to the skills repo, pull that new commit into any project that needs it:

```bash
# From inside this project (boomi-platform-api-explorer)
git submodule update --remote skills/boomi-skills
git add skills/boomi-skills
git commit -m "Update boomi-skills submodule to latest"
git push
```

Repeat for any other project that has `boomi-skills` as a submodule.

> **Note:** You don't have to update every project immediately. The submodule pin is
> intentional — it gives each project stability. Update when ready.

---

## Telling Claude to update a skill

You can ask Claude directly in any session:

> "Update the boomi-branding skill — add X to the icons reference"

Claude will edit the files in the context of wherever it's running. If it edits
`skills/boomi-skills/boomi-branding/` (the submodule copy), remind it:

> "Edit the canonical copy in `~/boomi-skills/boomi-branding/` instead."

Or just tell Claude at the start of a session:

> "Any skill edits should go to `~/boomi-skills/`, not the submodule copy."

---

## Adding a new skill to the skills repo

```bash
cd ~/boomi-skills
mkdir my-new-skill
# create SKILL.md and any reference files
git add my-new-skill/
git commit -m "Add my-new-skill"
git push
```

Then wire it up globally on your machine:

```bash
ln -s ~/boomi-skills/my-new-skill ~/.claude/skills/my-new-skill
```

Or re-run the installer which auto-discovers any folder containing a `SKILL.md`:

```bash
bash ~/boomi-skills/install.sh
```

---

## Setting up on a new machine

```bash
# macOS / Linux
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)

# Windows PowerShell
irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
```

This clones `~/boomi-skills/`, creates `~/.claude/skills/`, and wires the symlinks.

---

## Quick reference

| Task | Command |
|---|---|
| Edit a skill | `cd ~/boomi-skills && edit the file` |
| Push skill changes | `cd ~/boomi-skills && git add -A && git commit -m "..." && git push` |
| Update submodule in this project | `git submodule update --remote skills/boomi-skills && git add skills/boomi-skills && git commit` |
| Bootstrap a new machine | `bash <(curl -fsSL .../install.sh)` |
| Add a new skill globally | `ln -s ~/boomi-skills/new-skill ~/.claude/skills/new-skill` |

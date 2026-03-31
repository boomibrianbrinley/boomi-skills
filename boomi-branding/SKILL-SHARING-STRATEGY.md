# Skill Centralization Strategy — Boomi Branding (and Boomi Best Practices)

**Problem:** The `boomi-branding` skill (and soon `boomi-best-practices`) contains reference material
that should be available to any Claude Code project that produces Boomi-branded output. Copying the
folder into every repo creates drift — updates made in one project don't propagate.

**Goal:** One source of truth, always current, available to any project with minimal setup.

---

## Chosen Architecture: Option A + C + D

Three layers, each serving a distinct purpose:

| Layer | Option | What it does |
|-------|--------|--------------|
| **Source of truth** | D — Private skills repo | Canonical home for all skills; version-controlled; editable |
| **Always-on for your machine** | C — `~/.claude/skills/` global | Symlink into the local skills repo clone; zero per-project config |
| **Portability to other machines / collaborators** | A — Git submodule | Remote pointer in consuming repos; resolved via `git submodule update` |

### Why not Option B (local symlink only)?

A filesystem symlink can only point to a local path — it cannot reference a URL or remote resource.
The submodule (Option A) **is** the correct mechanism for "a pointer to a remote resource":

| What you want | What actually does it |
|---|---|
| "Symlink to a web resource" | Git submodule — remote pointer, resolved on demand |
| Always-current on your machine | `~/.claude/skills/` symlinked to local clone (Option C) |
| Bootstrap a new machine / collaborator | Install script that clones the skills repo and wires it up (Option D) |

---

## Layer 1 — The Skills Repo (Option D)

Create a dedicated private GitHub repo as the single source of truth.

### Suggested repo structure

```
boomi-skills/                        ← repo root
  install.sh                         ← bootstrap script (see Layer 3)
  boomi-branding/
    SKILL.md
    SKILL-SHARING-STRATEGY.md        ← this file (canonical copy lives here)
    references/
      colors.md
      components.md
      diagrams.md
      html-template.md
      icons.md
      logos.md
  boomi-best-practices/              ← fast follow
    SKILL.md
    ...
```

### One-time setup

```bash
# Clone to a stable local path — the global symlinks depend on this location
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
```

### Editing the skill

Always edit files inside `~/boomi-skills/`. Changes are immediately reflected everywhere
that uses a symlink (Option C), and can be pushed to propagate to submodule consumers (Option A).

```bash
cd ~/boomi-skills
# edit files...
git add -A && git commit -m "Update boomi-branding: ..."
git push
```

---

## Layer 2 — Global Availability (Option C)

Symlink each skill from `~/.claude/skills/` into the local `~/boomi-skills/` clone.
Claude Code loads `~/.claude/skills/` automatically for every project on your machine —
no per-project configuration needed.

```bash
mkdir -p ~/.claude/skills

# boomi-branding
ln -s ~/boomi-skills/boomi-branding ~/.claude/skills/boomi-branding

# boomi-best-practices (when ready)
ln -s ~/boomi-skills/boomi-best-practices ~/.claude/skills/boomi-best-practices
```

Because the target is the local git clone, the symlink resolves to the latest committed
(and even uncommitted) version of the skill at all times.

### Caveat: dual-loading on your own machine

If a project also has the skill as a submodule (Layer 3) AND your global `~/.claude/skills/`
is wired up, Claude sees the skill from both paths. This is harmless but redundant.
**On your machine, rely on the global; the submodule exists for portability only.**

---

## Layer 3 — Portability via Submodule (Option A)

For any project that you share via `git clone` — where collaborators or other machines
need the skill without having the global `~/.claude/` setup — add the skills repo as a submodule.

```bash
# From inside the consuming project root
git submodule add https://github.com/boomibrianbrinley/boomi-skills.git skills-shared

# Or mount a specific skill directly at the expected path:
git submodule add -b main --name boomi-branding \
  https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-branding
```

### Updating a submodule to the latest skills

```bash
git submodule update --remote skills/boomi-branding
git add skills/boomi-branding
git commit -m "Update boomi-branding skill to latest"
```

### After cloning a project that has submodules

```bash
git submodule update --init --recursive
```

---

## Layer 4 — Bootstrap Script (Option D, install.sh)

The install script ties all three layers together. Run it on any new machine to go from zero
to fully wired in one command.

```bash
#!/usr/bin/env bash
# install.sh — Bootstrap Boomi skills on a new machine
set -euo pipefail

SKILLS_REPO="https://github.com/boomibrianbrinley/boomi-skills.git"
SKILLS_DIR="$HOME/boomi-skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

# 1. Clone or update the skills repo
if [ -d "$SKILLS_DIR/.git" ]; then
  echo "→ Updating boomi-skills..."
  git -C "$SKILLS_DIR" pull --ff-only
else
  echo "→ Cloning boomi-skills..."
  git clone "$SKILLS_REPO" "$SKILLS_DIR"
fi

# 2. Ensure ~/.claude/skills exists
mkdir -p "$CLAUDE_SKILLS"

# 3. Symlink each skill into the global Claude skills directory
for skill in boomi-branding boomi-best-practices; do
  target="$SKILLS_DIR/$skill"
  link="$CLAUDE_SKILLS/$skill"
  if [ -d "$target" ]; then
    if [ -L "$link" ]; then
      echo "✓ $skill already linked"
    elif [ -e "$link" ]; then
      echo "⚠ $link exists and is not a symlink — skipping (resolve manually)"
    else
      ln -s "$target" "$link"
      echo "✓ Linked $skill"
    fi
  else
    echo "  (skipping $skill — not found in skills repo)"
  fi
done

echo ""
echo "Done. Skills available at ~/.claude/skills/"
```

Store this script at the root of the `boomi-skills` repo. Run it with:

```bash
curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh | bash
# or after cloning:
bash ~/boomi-skills/install.sh
```

---

## Summary: What Lives Where

| File / folder | Lives in | Consumed via |
|---|---|---|
| Skill content (`SKILL.md`, `references/`) | `boomi-skills` repo | Symlink (global) or submodule (per-project) |
| `install.sh` | `boomi-skills` repo root | Run once per machine |
| `~/.claude/skills/boomi-branding` | Local machine only | Symlink → `~/boomi-skills/boomi-branding` |
| `skills/boomi-branding` in a project | Consuming project repo | Git submodule → `boomi-skills` repo |

---

## CLAUDE.md Reference Block

Add this to the `CLAUDE.md` of any project that includes the skill as a submodule:

```markdown
## Boomi Skills (shared)

`skills/boomi-branding/` is a git submodule pointing to the `boomi-skills` repo.

- **Do not edit files inside `skills/boomi-branding/` directly** — changes belong in the skills repo.
- To update to the latest: `git submodule update --remote skills/boomi-branding`
- On a new machine without the global `~/.claude/skills/` setup, run:
  `bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)`
```

---

## Execution Checklist

### Phase 1 — boomi-branding (now)
- [ ] Create `boomi-skills` private repo on GitHub
- [ ] Move canonical `boomi-branding/` into it (including this strategy doc)
- [ ] Run `install.sh` to wire up `~/.claude/skills/`
- [ ] In `boomi-platform-api-explorer`: add as submodule or rely on global (your call)
- [ ] Remove or gitignore the old `skills/boomi-branding/` copy in this repo

### Phase 2 — boomi-best-practices (fast follow)
- [ ] Move `boomi-best-practices/` into `boomi-skills` repo
- [ ] Update `install.sh` to include it (already written above)
- [ ] Re-run `install.sh`

#!/usr/bin/env bash
# =============================================================================
# install.sh — Bootstrap Boomi skills (macOS / Linux / WSL / Git Bash)
# =============================================================================
# Usage:
#   bash install.sh                   # install all available skills
#   bash install.sh boomi-branding    # install a specific skill only
#
# Run from anywhere via curl:
#   bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)
# =============================================================================
set -euo pipefail

SKILLS_REPO="https://github.com/boomibrianbrinley/boomi-skills.git"
SKILLS_DIR="$HOME/boomi-skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

# Detect platform for informational output
case "$(uname -s)" in
  Darwin)  PLATFORM="macOS" ;;
  Linux)
    if grep -qi microsoft /proc/version 2>/dev/null; then
      PLATFORM="WSL"
    else
      PLATFORM="Linux"
    fi ;;
  MINGW*|MSYS*|CYGWIN*) PLATFORM="Git Bash (Windows)" ;;
  *)       PLATFORM="Unknown" ;;
esac

echo ""
echo "┌─────────────────────────────────────────────┐"
echo "│         Boomi Skills Installer              │"
echo "│         Platform: $PLATFORM"
echo "└─────────────────────────────────────────────┘"
echo ""

# ── 1. Clone or update the skills repo ───────────────────────────────────────

if [ -d "$SKILLS_DIR/.git" ]; then
  echo "→ Updating boomi-skills repo..."
  git -C "$SKILLS_DIR" pull --ff-only
else
  echo "→ Cloning boomi-skills repo to $SKILLS_DIR..."
  git clone "$SKILLS_REPO" "$SKILLS_DIR"
fi

# ── 2. Ensure ~/.claude/skills exists ────────────────────────────────────────

mkdir -p "$CLAUDE_SKILLS"

# ── 3. Determine which skills to install ─────────────────────────────────────

if [ $# -gt 0 ]; then
  # Specific skills requested on the command line
  SKILLS=("$@")
else
  # Auto-discover: any directory in the skills repo that contains a SKILL.md
  SKILLS=()
  while IFS= read -r skill_dir; do
    SKILLS+=("$(basename "$skill_dir")")
  done < <(find "$SKILLS_DIR" -maxdepth 2 -name "SKILL.md" -exec dirname {} \; | sort)
fi

# ── 4. Symlink each skill into ~/.claude/skills/ ──────────────────────────────

INSTALLED=0
SKIPPED=0
ERRORS=0

for skill in "${SKILLS[@]}"; do
  target="$SKILLS_DIR/$skill"
  link="$CLAUDE_SKILLS/$skill"

  if [ ! -d "$target" ]; then
    echo "  ⚠  '$skill' not found in skills repo — skipping"
    (( SKIPPED++ )) || true
    continue
  fi

  if [ -L "$link" ]; then
    # Already a symlink — update if target changed
    current_target="$(readlink "$link")"
    if [ "$current_target" = "$target" ]; then
      echo "  ✓  $skill (already linked)"
    else
      ln -sf "$target" "$link"
      echo "  ↺  $skill (retargeted: was $current_target)"
    fi
    (( INSTALLED++ )) || true
  elif [ -e "$link" ]; then
    echo "  ⚠  $link exists and is not a symlink — skipping (resolve manually)"
    (( SKIPPED++ )) || true
  else
    ln -s "$target" "$link"
    echo "  ✓  $skill → $link"
    (( INSTALLED++ )) || true
  fi
done

# ── 5. Summary ────────────────────────────────────────────────────────────────

echo ""
echo "Done."
echo "  Installed/verified : $INSTALLED"
[ "$SKIPPED" -gt 0 ]  && echo "  Skipped            : $SKIPPED"
[ "$ERRORS"  -gt 0 ]  && echo "  Errors             : $ERRORS"
echo ""
echo "Skills available at: $CLAUDE_SKILLS"
echo ""

# ── WSL note ──────────────────────────────────────────────────────────────────
if [ "$PLATFORM" = "WSL" ]; then
  echo "Note (WSL): Claude Desktop on Windows reads skills from the Windows"
  echo "user profile, not the WSL filesystem. Run install.ps1 in PowerShell"
  echo "to also wire up the Windows-side Claude skills directory."
  echo ""
fi

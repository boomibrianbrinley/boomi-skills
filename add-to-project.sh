#!/usr/bin/env bash
# =============================================================================
# add-to-project.sh — Add boomi-skills as a git submodule in a project
# =============================================================================
# Run this from the ROOT of the consuming project repo.
#
# Usage:
#   bash add-to-project.sh                         # adds all skills under skills/
#   bash add-to-project.sh boomi-branding          # adds one skill only
#   bash add-to-project.sh boomi-branding boomi-best-practices
# =============================================================================
set -euo pipefail

SKILLS_REPO="https://github.com/boomibrianbrinley/boomi-skills.git"

# Verify we're inside a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: run this script from the root of a git repository."
  exit 1
fi

PROJECT_ROOT="$(git rev-parse --show-toplevel)"

if [ $# -gt 0 ]; then
  SKILLS=("$@")
else
  # Default: add all known skills
  SKILLS=("boomi-branding" "boomi-best-practices")
fi

echo ""
echo "Adding boomi-skills submodule(s) to: $PROJECT_ROOT"
echo ""

for skill in "${SKILLS[@]}"; do
  mount_path="skills/$skill"
  abs_path="$PROJECT_ROOT/$mount_path"

  if [ -d "$abs_path/.git" ] || git submodule status "$mount_path" &>/dev/null; then
    echo "  ✓  $skill already a submodule — updating to latest..."
    git submodule update --remote "$mount_path"
    git add "$mount_path"
  elif [ -d "$abs_path" ]; then
    echo "  ⚠  $mount_path exists but is not a submodule."
    echo "     Remove or rename it first, then re-run this script."
    continue
  else
    echo "  +  Adding $skill as submodule at $mount_path..."
    # Add the full repo as a submodule; sparse checkout would need a post-checkout hook
    # For simplicity we add the whole repo — Claude only reads the skill dir it's pointed at
    git submodule add -b main "$SKILLS_REPO" "$mount_path"
    git add "$mount_path" .gitmodules
    echo "  ✓  $skill added"
  fi
done

echo ""
echo "Submodule(s) staged. Commit with:"
echo "  git commit -m 'Add boomi-skills submodule(s)'"
echo ""
echo "Other contributors can initialize after cloning with:"
echo "  git submodule update --init --recursive"
echo ""

# ── CLAUDE.md reminder ────────────────────────────────────────────────────────
echo "Remember to add this block to your project's CLAUDE.md:"
echo ""
cat <<'CLAUDEMD'
## Boomi Skills (shared)

`skills/boomi-branding/` (and `skills/boomi-best-practices/`) are git submodules
pointing to the `boomi-skills` repo.

- **Do not edit files inside these folders directly** — changes belong in the skills repo.
- Update to latest: `git submodule update --remote skills/boomi-branding`
- Initialize after cloning: `git submodule update --init --recursive`
- Bootstrap global skills on a new machine:
  - macOS/Linux: `bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)`
  - Windows:     `irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex`
CLAUDEMD

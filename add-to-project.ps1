# =============================================================================
# add-to-project.ps1 — Add boomi-skills as a git submodule in a project
# =============================================================================
# Run this from the ROOT of the consuming project repo.
#
# Usage:
#   .\add-to-project.ps1                                    # adds all skills
#   .\add-to-project.ps1 -Skills boomi-branding             # one skill only
#   .\add-to-project.ps1 -Skills boomi-branding,boomi-best-practices
# =============================================================================
[CmdletBinding()]
param(
    [string[]]$Skills = @("boomi-branding", "boomi-best-practices")
)

$ErrorActionPreference = "Stop"

$SkillsRepo = "https://github.com/boomibrianbrinley/boomi-skills.git"

# Verify we're inside a git repo
try {
    $projectRoot = git rev-parse --show-toplevel 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
} catch {
    Write-Error "Run this script from the root of a git repository."
    exit 1
}

# Normalize path separators
$projectRoot = $projectRoot -replace "/", "\"

Write-Host ""
Write-Host "Adding boomi-skills submodule(s) to: $projectRoot"
Write-Host ""

foreach ($skill in $Skills) {
    # Use forward slashes for git commands (git on Windows expects them)
    $mountPath = "skills/$skill"
    $absPath   = Join-Path $projectRoot "skills\$skill"

    # Check if already a submodule
    $submoduleStatus = git submodule status $mountPath 2>&1
    $isSubmodule = ($LASTEXITCODE -eq 0) -and ($submoduleStatus -notmatch "^fatal")

    if ($isSubmodule) {
        Write-Host "  ✓  $skill already a submodule — updating to latest..."
        git submodule update --remote $mountPath
        git add $mountPath
    } elseif (Test-Path $absPath) {
        Write-Host "  ⚠  $mountPath exists but is not a submodule."
        Write-Host "     Remove or rename it first, then re-run this script."
        continue
    } else {
        Write-Host "  +  Adding $skill as submodule at $mountPath..."
        git submodule add -b main $SkillsRepo $mountPath
        git add $mountPath .gitmodules
        Write-Host "  ✓  $skill added"
    }
}

Write-Host ""
Write-Host "Submodule(s) staged. Commit with:"
Write-Host "  git commit -m 'Add boomi-skills submodule(s)'"
Write-Host ""
Write-Host "Other contributors can initialize after cloning with:"
Write-Host "  git submodule update --init --recursive"
Write-Host ""
Write-Host "Remember to add this block to your project's CLAUDE.md:"
Write-Host ""
Write-Host @'
## Boomi Skills (shared)

`skills/boomi-branding/` (and `skills/boomi-best-practices/`) are git submodules
pointing to the `boomi-skills` repo.

- **Do not edit files inside these folders directly** — changes belong in the skills repo.
- Update to latest: `git submodule update --remote skills/boomi-branding`
- Initialize after cloning: `git submodule update --init --recursive`
- Bootstrap global skills on a new machine:
  - macOS/Linux: `bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh)`
  - Windows:     `irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex`
'@

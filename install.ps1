# =============================================================================
# install.ps1 — Bootstrap Boomi skills (Windows / PowerShell)
# =============================================================================
# Usage:
#   .\install.ps1                     # install all available skills
#   .\install.ps1 -Skills boomi-branding             # specific skill
#   .\install.ps1 -Skills boomi-branding,boomi-best-practices
#
# Run from anywhere via PowerShell (requires ExecutionPolicy RemoteSigned or Bypass):
#   irm https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.ps1 | iex
#
# Symlink note:
#   Symbolic links on Windows require either:
#     (a) Developer Mode enabled  (Settings → Privacy & Security → For Developers)
#     (b) Running this script as Administrator
#   If neither is available, the script falls back to Directory Junctions,
#   which work without elevation but are local-only (no cross-drive support).
# =============================================================================
[CmdletBinding()]
param(
    [string[]]$Skills = @()
)

$ErrorActionPreference = "Stop"

$SkillsRepo   = "https://github.com/boomibrianbrinley/boomi-skills.git"
$SkillsDir    = Join-Path $env:USERPROFILE "boomi-skills"
$ClaudeSkills = Join-Path $env:USERPROFILE ".claude\skills"

# ── Helper: test if running as Administrator ──────────────────────────────────
function Test-Admin {
    $current = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
    return $current.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# ── Helper: test if Developer Mode is enabled ────────────────────────────────
function Test-DeveloperMode {
    try {
        $key = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"
        $val = Get-ItemPropertyValue -Path $key -Name "AllowDevelopmentWithoutDevLicense" -ErrorAction SilentlyContinue
        return ($val -eq 1)
    } catch {
        return $false
    }
}

# ── Helper: create a link (symlink preferred, junction fallback) ──────────────
function New-SkillLink {
    param([string]$Target, [string]$Link)

    $canSymlink = (Test-Admin) -or (Test-DeveloperMode)

    if ($canSymlink) {
        New-Item -ItemType SymbolicLink -Path $Link -Target $Target -Force | Out-Null
        return "symlink"
    } else {
        # Junction: no admin required, same-volume NTFS only
        New-Item -ItemType Junction -Path $Link -Target $Target -Force | Out-Null
        return "junction"
    }
}

# ── Banner ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "┌─────────────────────────────────────────────┐"
Write-Host "│         Boomi Skills Installer              │"
Write-Host "│         Platform: Windows (PowerShell)      │"
Write-Host "└─────────────────────────────────────────────┘"
Write-Host ""

$isAdmin    = Test-Admin
$isDevMode  = Test-DeveloperMode
$canSymlink = $isAdmin -or $isDevMode

if (-not $canSymlink) {
    Write-Host "  ⚠  Symlinks unavailable (no admin rights and Developer Mode is off)."
    Write-Host "     Falling back to Directory Junctions (local volumes only)."
    Write-Host "     To enable symlinks: Settings → Privacy & Security → For Developers → ON"
    Write-Host ""
}

# ── 1. Clone or update the skills repo ───────────────────────────────────────

if (Test-Path (Join-Path $SkillsDir ".git")) {
    Write-Host "→ Updating boomi-skills repo..."
    git -C $SkillsDir pull --ff-only
} else {
    Write-Host "→ Cloning boomi-skills repo to $SkillsDir..."
    git clone $SkillsRepo $SkillsDir
}

# ── 2. Ensure ~/.claude/skills exists ────────────────────────────────────────

if (-not (Test-Path $ClaudeSkills)) {
    New-Item -ItemType Directory -Path $ClaudeSkills -Force | Out-Null
}

# ── 3. Determine which skills to install ─────────────────────────────────────

if ($Skills.Count -eq 0) {
    # Auto-discover: any directory containing a SKILL.md
    $Skills = Get-ChildItem -Path $SkillsDir -Recurse -Depth 1 -Filter "SKILL.md" |
              Select-Object -ExpandProperty DirectoryName |
              ForEach-Object { Split-Path $_ -Leaf } |
              Sort-Object
}

# ── 4. Link each skill into %USERPROFILE%\.claude\skills\ ────────────────────

$installed = 0
$skipped   = 0

foreach ($skill in $Skills) {
    $target = Join-Path $SkillsDir $skill
    $link   = Join-Path $ClaudeSkills $skill

    if (-not (Test-Path $target)) {
        Write-Host "  ⚠  '$skill' not found in skills repo — skipping"
        $skipped++
        continue
    }

    $existingItem = Get-Item -Path $link -ErrorAction SilentlyContinue

    if ($existingItem) {
        $isLink = ($existingItem.LinkType -eq "SymbolicLink") -or ($existingItem.LinkType -eq "Junction")
        if ($isLink) {
            $currentTarget = $existingItem.Target
            if ($currentTarget -eq $target) {
                Write-Host "  ✓  $skill (already linked)"
            } else {
                Remove-Item -Path $link -Force
                $linkType = New-SkillLink -Target $target -Link $link
                Write-Host "  ↺  $skill (retargeted as $linkType)"
            }
        } else {
            Write-Host "  ⚠  $link exists and is not a link — skipping (resolve manually)"
            $skipped++
            continue
        }
    } else {
        $linkType = New-SkillLink -Target $target -Link $link
        Write-Host "  ✓  $skill → $link ($linkType)"
    }
    $installed++
}

# ── 5. Summary ────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "Done."
Write-Host "  Installed/verified : $installed"
if ($skipped -gt 0) { Write-Host "  Skipped            : $skipped" }
Write-Host ""
Write-Host "Skills available at: $ClaudeSkills"
Write-Host ""

if (-not $canSymlink) {
    Write-Host "Note: Junctions were used instead of symlinks. This works for local"
    Write-Host "use but will not resolve correctly if the skills directory moves drives."
    Write-Host "Re-run as Administrator (or with Developer Mode on) to upgrade to symlinks."
    Write-Host ""
}

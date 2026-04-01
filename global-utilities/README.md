# global-utilities

**General-purpose utilities available in any project or conversation.**

This skill provides Claude with a set of everyday tools that aren't tied to any specific
project — things like looking up your public IP address. Install it once and it's available
everywhere.

---

## What's included

### Public IP Lookup
Find out the public IP address of the machine you're working on. Useful for firewall
allowlisting, VPN verification, network diagnostics, or any time you just need to know
what IP the outside world sees.

Ask Claude something like:
- *"What's my public IP address?"*
- *"What IP should I allowlist for this machine?"*
- *"Am I coming from the right IP?"*

Uses [ipify.org](https://www.ipify.org/) — free, no rate limits, no logging.

---

## Requirements

This skill has no runtime dependencies beyond Claude's built-in **WebFetch** capability,
which must be enabled in your Claude session. No MCP server or software installs required.

---

## Install this skill only

### Claude Desktop (Mac)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) global-utilities
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills global-utilities
```

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) global-utilities
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/global-utilities ~/.claude/skills/global-utilities
```

---

## Updating

```bash
cd ~/boomi-skills && git pull
```

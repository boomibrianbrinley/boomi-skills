# global-utilities

**General-purpose utilities available in any project or conversation.**

This skill gives Claude a set of everyday tools that aren't tied to any specific project —
looking up your public IP, getting the current time, resolving DNS records, and checking
SSL certificates. Install it once and it's available everywhere.

---

## What's included

### Public IP Lookup
Find out the public IP address of the machine you're working on. Useful for firewall
allowlisting, VPN verification, network diagnostics, or any time you just need to know
what IP the outside world sees.

Ask Claude: *"What's my public IP?"* or *"What IP should I allowlist for this machine?"*

Uses [ipify.org](https://www.ipify.org/) — free, no rate limits, no logging.

### Current Date and Time
Get a precise current timestamp in UTC or any IANA timezone. Useful when Claude needs
an exact "now" for report headers, log entries, file names, or scheduling questions.

Ask Claude: *"What time is it in Tokyo?"* or *"Give me the current UTC timestamp."*

Uses [timeapi.io](https://timeapi.io/) — free, no API key required for time queries.

### DNS Lookup
Resolve DNS records for any domain — A, AAAA, MX, TXT, CNAME, NS, and more. Useful
for verifying DNS propagation, checking mail routing, or diagnosing connectivity issues.

Ask Claude: *"What IP does api.example.com resolve to?"* or *"Show me the MX records for example.com."*

Uses [Google Public DNS-over-HTTPS](https://developers.google.com/speed/public-dns/docs/doh/json) — no API key required.

### SSL Certificate Check
Check a domain's SSL certificate expiry date, issuer, and TLS grade. Useful before going
live, after a cert renewal, or when diagnosing SSL handshake errors.

Ask Claude: *"When does the SSL cert expire for example.com?"* or *"Give me a TLS grade for our API gateway."*

Uses `openssl` (via bash) for fast expiry/issuer checks, and the
[SSL Labs API](https://www.ssllabs.com/) for full TLS grading.

---

## Requirements

| Dependency | Required for | Notes |
|---|---|---|
| **WebFetch** (Claude capability) | IP lookup, time lookup, DNS lookup, SSL Labs grading | Must be enabled in your Claude session. Built into Claude — no install needed. |
| **Bash / openssl** | SSL certificate expiry and issuer (fastest method) | `openssl` is pre-installed on macOS and most Linux distros. On Windows, use Git Bash or WSL. |

No MCP server required. No external software installs required beyond `openssl` for SSL checks.

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

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

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

> **Verifying the install:** Ask Claude *"What skills do you have available?"* — you should
> see `global-utilities` listed.

---

## Add to a specific project (submodule)

```bash
git submodule add -b main https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-skills
git submodule update --init --recursive
git commit -m "Add boomi-skills submodule"
```

After cloning a project that uses this submodule:

```bash
git submodule update --init --recursive
```

---

## Updating

```bash
cd ~/boomi-skills && git pull
```

Restart Claude Desktop after pulling updates. Claude Code CLI picks up changes automatically in the next session.

---

## Related skills

- **`git-conventions`** — Consistent git commit, branch, and PR patterns

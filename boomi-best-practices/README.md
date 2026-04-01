# boomi-best-practices

**Recommendations grounded in Boomi's own documentation — not guesswork.**

This skill ensures that when Claude gives you advice about your Boomi account, it's backed
by official Boomi guidance. Before generating any recommendation, it searches Boomi's help
site, community forums, and release notes in real time — so you get current, authoritative
answers rather than generic suggestions based on outdated training data.

---

## What it does

Every time Claude makes a recommendation about your Boomi platform, this skill:

1. **Searches live** — queries `help.boomi.com`, `community.boomi.com`, and Boomi release
   notes for the most current guidance on the topic
2. **Cites the source** — links recommendations back to the official Boomi documentation
   that supports them
3. **Flags recent changes** — surfaces anything in the latest Boomi releases that's relevant
   to the finding

The result is recommendations you can trust and share with confidence — with a paper trail
back to Boomi's own documentation.

---

## When it kicks in

This skill is used automatically by other skills when they generate findings or recommendations:

- **`boomi-health-check`** — enriches each health check finding with official Boomi guidance
  before producing the final report
- Any time Claude reviews Boomi account configurations and suggests improvements

You can also invoke it directly:

- *"What does Boomi recommend for JVM heap settings on Molecules?"*
- *"What are the best practices for Boomi environment security?"*
- *"What does Boomi say about cleaning up dead processes?"*

---

## Why this matters

Claude's training data has a knowledge cutoff. Boomi releases updates regularly, and
best practices evolve. This skill ensures Claude always checks the current state of
Boomi's documentation rather than relying on what it learned during training — which
may be months or years out of date.

---

## Install this skill only

### Claude Desktop (Mac)

Run the installer in your terminal, then restart Claude Desktop:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-best-practices
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

Open PowerShell and run:

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-best-practices
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-best-practices
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-best-practices ~/.claude/skills/boomi-best-practices
```

> **Verifying the install:** In Claude Desktop, start a new conversation and ask
> *"What skills do you have available?"* — you should see `boomi-best-practices` listed.

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

---

## Requirements

| Dependency | Required for | Notes |
|---|---|---|
| **WebSearch** (Claude capability) | All recommendations | Used to query `help.boomi.com`, `community.boomi.com`, and Boomi release notes in real time. Must be enabled in your Claude session. |
| **WebFetch** (Claude capability) | Full documentation coverage | Used to retrieve the content of individual documentation pages found via search. Must be enabled in your Claude session. |

No MCP server or additional software installs are required.

---

## Related skills

- **`boomi-health-check`** — Uses this skill to enrich health check findings (recommended pair)
- **`boomi-release-analyzer`** — Release impact assessments
- **`boomi-branding`** — Branded report output

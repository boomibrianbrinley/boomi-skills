# boomi-branding

**Consistent, on-brand Boomi output — every time.**

This skill gives Claude the Boomi design playbook: colors, typography, logo usage, icons,
UI component patterns, and a ready-to-use HTML template. Any report, dashboard, or document
Claude produces will look like it came from Boomi's own design team.

---

## What it covers

| Reference | What it gives you |
|---|---|
| **Colors** | The full Boomi brand palette — coral, navy, purple, and supporting colors — with CSS variables and rules for when to use each one |
| **Icons** | How to use Phosphor Icons (Boomi's icon library), common patterns, and a list of known rendering pitfalls to avoid |
| **Logos** | The correct way to embed the Boomi wordmark — inline SVG for reliability, with sizing guidelines for headers, footers, reports, and compact layouts |
| **Components** | Cards, badges, tables, and layout patterns that match the Boomi Exosphere design system |
| **Diagrams** | Conventions for architecture and integration flow diagrams |
| **HTML Template** | A complete starter template with Boomi fonts, colors, and CSS already wired up — ready to drop content into |

---

## When it kicks in

This skill runs automatically when Claude is generating:

- Health check reports or executive summaries
- Release impact assessments
- Any HTML output that should look like a Boomi product
- UI components, dashboards, or mockups for Boomi-related tools

You don't need to ask for it explicitly — other skills (like `boomi-health-check` and
`boomi-release-analyzer`) call for it automatically when they produce formatted output.

---

## Install this skill only

### Claude Desktop (Mac)

Run the installer in your terminal, then restart Claude Desktop:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-branding
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

Open PowerShell and run:

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-branding
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-branding
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-branding ~/.claude/skills/boomi-branding
```

> **Verifying the install:** In Claude Desktop, start a new conversation and ask
> *"What skills do you have available?"* — you should see `boomi-branding` listed.

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

## Design system reference

This skill is built on the [Boomi Exosphere design system](https://exosphere.boomi.com).
Where Exosphere specifies component or color details, those take precedence.

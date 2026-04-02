# boomi-log-troubleshooter

**Diagnose Boomi container and process logs — with internal Confluence runbooks, automatically.**

This skill analyzes Boomi container logs (atom/molecule startup, JVM, scheduling, listeners) and
process execution logs (connector errors, shape failures, data errors) by doing two things at once:
surfacing what's actually wrong from the log, and searching your Confluence knowledge base for
relevant runbooks, known issues, and resolution steps. The result is a root-cause diagnosis, not
just a log summary.

---

## What it does

When you paste a log or point Claude to a downloaded log file, it will:

1. **Identify the log type** — container log (atom/molecule startup, JVM, ActiveMQ, scheduling,
   listeners) vs. process log (execution-level connector errors, shape failures, data errors)
2. **Extract and categorize issues** into three buckets:
   - **Critical** — caused failures, data loss, or service interruption (SEVERE entries,
     uncaught exceptions, missed schedules, listener crashes, network outages)
   - **Warning** — degraded performance or could become critical (low memory, disk approaching
     limits, slow poll times, auth config gaps)
   - **Informational** — context that helps but isn't a problem (startup properties, version info)
3. **Search Confluence** — for each critical or warning issue, searches the **ASE** (Advanced
   Support Engineering) and **SUP** (Product Support) spaces using `searchConfluenceUsingCql`
   with targeted queries based on the actual error patterns found
4. **Produce a structured diagnosis report** — log summary, findings with Confluence links,
   and a prioritized list of specific next steps

---

## When to use it

Ask Claude something like:

- *"Analyze this Boomi container log"*
- *"Why did my atom restart overnight?"*
- *"What's wrong with my process — it keeps failing at the database connector"*
- *"Look at my logs and tell me what's causing the missed schedules"*
- *"Troubleshoot this atom log"*

You can paste raw log content directly or provide a path to a downloaded `.log` file.

---

## Requirements

| Dependency | Required for | Notes |
|---|---|---|
| **Confluence MCP integration** | Searching ASE / SUP spaces | Uses `searchConfluenceUsingCql` and `getConfluencePage` tools. Requires Atlassian Cloud ID `2cd0c4d5-fb26-4e47-b128-dbf33f624fa2`. |
| **Boomi Platform API Explorer** (optional) | Downloading logs directly | If you want Claude to fetch and analyze a log without you pasting it, the MCP server's `boomi_download_atom_log` or `boomi_download_webserver_log` tools can retrieve the file. Requires the runtime to be **ONLINE**. |
| **Claude Code** (for log file reads) | Reading downloaded ZIP logs | If logs are downloaded as ZIP archives to `data/logs/`, Claude Code has disk access to unzip and read them. Claude Desktop (chat) cannot read local files. |

---

## Install this skill only

### Claude Desktop (Mac)

Run the installer in your terminal, then restart Claude Desktop:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-log-troubleshooter
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

Open PowerShell and run:

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills boomi-log-troubleshooter
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) boomi-log-troubleshooter
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/boomi-log-troubleshooter ~/.claude/skills/boomi-log-troubleshooter
```

> **Verifying the install:** In Claude Desktop, start a new conversation and ask
> *"What skills do you have available?"* — you should see `boomi-log-troubleshooter` listed.

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

## How it searches Confluence

The skill uses `searchConfluenceUsingCql` with the Atlassian Cloud ID
`2cd0c4d5-fb26-4e47-b128-dbf33f624fa2`. It targets the **ASE** and **SUP** spaces with queries
built from the actual error patterns found in the log — exception class names, error message
fragments, component names, and symptom descriptions.

Example query: `space in ("ASE","SUP") AND text ~ "listener failed queue" ORDER BY lastModified DESC`

For highly relevant results, it fetches the full page content with `getConfluencePage` to extract
specific runbook steps. If a search returns nothing useful, it tries at least two alternative
query variations before reporting that no articles were found.

---

## Related skills

- **`boomi-best-practices`** — Enriches findings with official Boomi public documentation from
  `help.boomi.com` and the Boomi Community (complements the internal Confluence search)
- **`boomi-health-check`** — Broader account health assessment covering runtimes, executions,
  security, and API gateways

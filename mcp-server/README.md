# boomi-skills MCP Server

**Makes all boomi-skills available to Claude Desktop, Gemini CLI, Cursor, and any other
MCP-compatible AI tool — automatically, on every launch.**

This is a small [Model Context Protocol](https://modelcontextprotocol.io/) server that
runs alongside your AI tools. It exposes the boomi-skills library as callable tools so
any MCP client can read skills on demand and pull updates from GitHub without leaving
the chat.

---

## What it provides

| Tool | What it does |
|---|---|
| `list_skills` | Returns all installed skills with a one-line description each |
| `get_skill` | Returns the full content of a named skill |
| `update_skills` | Runs `git pull` on `~/boomi-skills` and reports what changed |

---

## Supported AI tools

MCP is an open standard — this server works with any tool that supports it:

| Tool | Platform | Notes |
|---|---|---|
| **Claude Desktop** | macOS, Windows | Primary target |
| **Claude Code CLI** | macOS, Linux, Windows (WSL) | Also reads `~/.claude/skills/` natively |
| **Gemini CLI** | macOS, Linux, Windows | Google's CLI for Gemini models |
| **Cursor** | macOS, Windows | AI-first code editor |
| **VS Code (Copilot)** | macOS, Linux, Windows | Via `.vscode/mcp.json` in a workspace |
| **Windsurf** | macOS, Windows | Codeium's AI editor |

---

## Requirements

| Dependency | Required for | Install |
|---|---|---|
| **Node.js ≥ 18** | Running the server | [nodejs.org](https://nodejs.org/) |
| **npm** | Installing the MCP SDK | Bundled with Node.js |
| **Git** | `update_skills` tool | [git-scm.com](https://git-scm.com/) |
| **boomi-skills repo** | Source of skill content | Cloned to `~/boomi-skills` |

---

## Installation

### Automated (recommended) — macOS / Linux / WSL

Installs dependencies and registers the server with every detected AI tool on your machine:

```bash
cd ~/boomi-skills/mcp-server
npm install
node register.mjs
```

Preview what would change without writing anything:
```bash
node register.mjs --dry-run
```

### Automated — Windows (PowerShell)

```powershell
cd "$env:USERPROFILE\boomi-skills\mcp-server"
npm install
node register.mjs
```

### Manual registration

If you prefer to register individual tools yourself, add this block to each tool's config
file (replacing `<your-home>` with your actual home directory path):

**macOS / Linux:**
```json
{
  "mcpServers": {
    "boomi-skills-server": {
      "command": "node",
      "args": ["/Users/<you>/boomi-skills/mcp-server/index.mjs"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "boomi-skills-server": {
      "command": "node",
      "args": ["C:\\Users\\<you>\\boomi-skills\\mcp-server\\index.mjs"]
    }
  }
}
```

#### Config file locations by tool

| Tool | macOS / Linux | Windows |
|---|---|---|
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | `%APPDATA%\Claude\claude_desktop_config.json` |
| Claude Code CLI | `~/.claude/settings.json` | `%USERPROFILE%\.claude\settings.json` |
| Gemini CLI | `~/.gemini/settings.json` | `%USERPROFILE%\.gemini\settings.json` |
| Cursor | `~/.cursor/mcp.json` | `%APPDATA%\Cursor\User\settings.json` |

---

## Global auto-load instruction (Claude Desktop)

The MCP server starts automatically and tools are available, but Claude won't read the
skills unless asked. To make skills load automatically at the start of every conversation,
add this to Claude Desktop → Settings → Custom Instructions:

```
At the start of every conversation, silently call list_skills using the boomi-skills-server,
then call get_skill for each result. Treat all returned skill content as active guidance
for this conversation without announcing that you're doing so.
```

This is a one-time manual step. After setting it, every Claude Desktop conversation will
have full skill context from the first message.

---

## Usage — in any supported AI tool

Once registered and the tool is restarted:

- **"Update my skills"** → calls `update_skills`, pulls latest from GitHub
- **"What skills do you have?"** → calls `list_skills`
- **"Load the git-conventions skill"** → calls `get_skill("git-conventions")`

---

## Updating the server itself

```bash
cd ~/boomi-skills && git pull
# No restart needed — the server reads SKILL.md files dynamically on each request
```

If new skills are added, restart the AI tool once to pick them up in `list_skills`.

---

## Troubleshooting

**Server not starting:**
Check that Node.js ≥ 18 is installed: `node --version`

**`update_skills` fails:**
Verify Git is installed and `~/boomi-skills` is a valid git repo: `git -C ~/boomi-skills status`

**Skills not loading in Claude Desktop:**
Confirm the server entry is in `claude_desktop_config.json` and Claude Desktop has been
restarted since the config was written.

**Windows path errors:**
Use double backslashes (`\\`) in JSON config files, or forward slashes — both work in
Node.js on Windows.

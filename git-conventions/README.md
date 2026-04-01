# git-conventions

**Consistent git patterns across every project and conversation.**

This skill ensures Claude follows the same commit message format, branch naming, PR
structure, submodule workflow, and safety rules every time — without you having to
re-explain your preferences in each session.

---

## What it covers

| Convention | What it enforces |
|---|---|
| **Commit messages** | Type prefix (`feat`, `fix`, `chore`, etc.), imperative mood, Co-Authored-By footer, heredoc formatting for multi-line messages |
| **Branch naming** | `type/short-description` format with hyphens |
| **Pull requests** | Title length, Summary + Test plan body template, `gh pr create` command pattern |
| **Staging files** | Prefer specific file paths over `git add -A`; check for credentials before staging |
| **Submodule operations** | Update, init, status — consistent command patterns |
| **Safety rules** | Never force-push main, never `--no-verify`, never amend published commits |
| **.gitignore defaults** | Standard exclusions for credentials, Claude internals, macOS, editors, session files |
| **Recovery patterns** | Safe rollback, undo last commit, discard file changes |

---

## When it kicks in

This skill is always active once installed. Claude will apply these conventions whenever:

- Creating a commit or pull request
- Naming a new branch
- Staging files for commit
- Working with submodules
- Suggesting `.gitignore` additions
- Recovering from a git mistake

You don't need to ask — the conventions apply automatically.

---

## Requirements

This skill has no runtime dependencies. It is purely a reference document that Claude
reads to apply consistent git patterns. No tools, APIs, or software installs required.

---

## Install this skill only

### Claude Desktop (Mac)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) git-conventions
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Desktop (Windows)

```powershell
git clone https://github.com/boomibrianbrinley/boomi-skills.git "$env:USERPROFILE\boomi-skills"
& "$env:USERPROFILE\boomi-skills\install.ps1" -Skills git-conventions
```

After the script completes, quit and reopen Claude Desktop. The skill loads automatically.

### Claude Code CLI (macOS / Linux / WSL)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/boomibrianbrinley/boomi-skills/main/install.sh) git-conventions
```

### Manual (any platform)

```bash
git clone https://github.com/boomibrianbrinley/boomi-skills.git ~/boomi-skills
mkdir -p ~/.claude/skills
ln -s ~/boomi-skills/git-conventions ~/.claude/skills/git-conventions
```

> **Verifying the install:** Ask Claude *"What skills do you have available?"* — you should
> see `git-conventions` listed.

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

- **`global-utilities`** — General-purpose utilities (IP lookup, time, DNS, SSL checks)

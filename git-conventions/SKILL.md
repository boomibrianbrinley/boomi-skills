# Git Conventions Skill

Consistent git patterns for commit messages, branch naming, pull requests, submodules,
and safety rules. Apply these conventions in every git operation across all projects.

---

## Commit Messages

### Format

Use a single-line subject (imperative mood, ≤72 chars), optionally followed by a blank
line and a body. Always end with the Co-Authored-By footer when Claude is the author.

```
<type>(<scope>): <short description>

<optional body — explain the why, not the what>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Types:**
| Type | When to use |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `chore` | Maintenance (deps, config, gitignore, build) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `style` | Formatting, whitespace — no logic change |
| `test` | Adding or updating tests |
| `perf` | Performance improvement |

**Scope** (optional) — the area affected, e.g. `feat(events):`, `fix(health):`, `chore(deps):`

### Always use a heredoc for multi-line messages

```bash
git commit -m "$(cat <<'EOF'
feat(health): add runtime version comparison

Highlights runtimes running below the account's modal version
so operators can identify nodes that need updating.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Branch Naming

```
<type>/<short-description>
```

Examples:
- `feat/execution-anomaly-chart`
- `fix/events-time-window`
- `chore/update-boomi-skills-submodule`
- `docs/api-guide`

Use hyphens, not underscores. Keep it short and readable.

---

## Pull Requests

### Title
Under 70 characters. Imperative mood. Same type prefix as commits if helpful.

### Body template
```markdown
## Summary
- <bullet 1>
- <bullet 2>

## Test plan
- [ ] <thing to verify>
- [ ] <thing to verify>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Create with gh CLI
```bash
gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
- bullet

## Test plan
- [ ] item

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Staging Files

**Prefer staging specific files** over `git add -A` or `git add .`:
```bash
git add src/specific-file.js public/css/styles.css
```

Only use `git add -A` when you have verified there are no unintended files
(credentials, large binaries, `.env`) in the working tree.

---

## Submodule Operations

### Update a submodule to latest remote
```bash
git submodule update --remote skills/boomi-skills
git add skills/boomi-skills
git commit -m "chore: update boomi-skills submodule to latest"
git push
```

### After cloning a repo with submodules
```bash
git submodule update --init --recursive
```

### Check which commit a submodule is pinned to
```bash
git submodule status
```

---

## Safety Rules

These are hard rules — never bypass them:

| Rule | Why |
|---|---|
| **Never `git push --force` to main/master`** | Overwrites shared history permanently |
| **Never `--no-verify`** | Skips hooks that exist for a reason; fix the hook failure instead |
| **Never `git reset --hard` without checking** | Discards uncommitted work — verify `git status` first |
| **Never amend a published commit** | Rewrites history others may already have pulled |
| **Never commit `.env`, credentials, or secrets** | Check `.gitignore` before `git add` on config files |
| **Create new commits, don't amend, after hook failure** | Hook failure = commit did NOT happen; amend would rewrite the previous commit |

---

## .gitignore Patterns to Always Include

These paths should be excluded in every project:

```gitignore
# Credentials and local config
.env
*.env.*
config.json
data/saved-accounts.json

# Claude Code internals
.claude/settings.json
.claude/settings.local.json
.claude/worktrees/

# Session files
session_transcript.md
**/session_transcript.md

# macOS
.DS_Store

# Editors
.vscode/
.idea/
*.swp
```

---

## Rollback / Recovery Patterns

**See what changed since last commit:**
```bash
git diff HEAD
```

**Undo last commit but keep changes staged:**
```bash
git reset --soft HEAD~1
```

**Discard changes to a specific file (not committed):**
```bash
git checkout -- path/to/file.js
```

**Find a safe rollback point:**
```bash
git log --oneline -20
```

# agentic-design-patterns skill

Encodes all 21 agentic design patterns from *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* (Antonio Gulli) as an evaluation and implementation framework for Claude.

## What it does

- **Audits** existing agentic projects (MCP servers, skill libraries, AI workflows) against all 21 patterns
- **Guides** the design of new agentic systems with pattern-based checklists
- **Produces** prioritised gap analyses with specific, actionable findings
- **Enriches** other skills with agentic design guidance

## The 21 Patterns

| # | Pattern | Part |
|---|---------|------|
| 1–7 | Prompt Chaining, Routing, Parallelization, Reflection, Tool Use, Planning, Multi-Agent | Foundations |
| 8–11 | Memory Management, Learning & Adaptation, MCP, Goal Setting & Monitoring | Memory & Context |
| 12–14 | Exception Handling, Human-in-the-Loop, RAG | Resilience |
| 15–21 | A2A, Resource Optimization, Reasoning, Guardrails, Evaluation, Prioritization, Exploration | Advanced |

## Adding to a project

```bash
# From the project root
bash skills/boomi-skills/add-to-project.sh agentic-design-patterns
```

Or manually add as a submodule:
```bash
git submodule add https://github.com/boomibrianbrinley/boomi-skills.git skills/boomi-skills
```

## Analysis repository

Project-specific findings live at:
`https://github.com/boomibrianbrinley/boomi-agentic-design-patterns`

## Usage examples

```
# Audit a project
"Using the agentic-design-patterns skill, audit this MCP server against all 21 patterns"

# Design review
"Review this new tool schema against Pattern 5 (Tool Use) and Pattern 10 (MCP)"

# Full gap analysis
"Run a full agentic design pattern gap analysis on boomi-skills and produce a prioritised roadmap"
```

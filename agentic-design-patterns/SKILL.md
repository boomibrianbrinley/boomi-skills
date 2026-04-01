---
name: agentic-design-patterns
description: >
  Apply the 21 agentic design patterns from "Agentic Design Patterns: A Hands-On Guide
  to Building Intelligent Systems" (Antonio Gulli) when designing, building, or reviewing
  agentic systems — including MCP servers, Claude skills, AI workflows, and tool-based
  agents. Use this skill when asked to review an agentic project for pattern compliance,
  design a new agentic system, audit an MCP server, or identify gaps in how a project
  uses AI agents. Works across any project — not specific to Boomi.
---

# Agentic Design Patterns Skill

This skill encodes all 21 agentic design patterns from *Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems* (Antonio Gulli, 424 pages) as an evaluation and implementation framework.

Use it to:
- **Design** a new agentic system with the right patterns from the start
- **Audit** an existing MCP server, skill library, or AI workflow against the 21 patterns
- **Gap-analyse** a project and produce a prioritised improvement roadmap
- **Enrich** another skill's output with agentic design guidance

**Analysis repository:** `https://github.com/boomibrianbrinley/boomi-agentic-design-patterns`
Project-specific findings (once run) live in `analysis/` in that repo.

---

## How to Use This Skill

### Mode 1 — Design Review (audit an existing project)
When asked to audit or review a project:
1. Explore the project's agentic surface — tools, skills, prompts, orchestration logic
2. Score each of the 21 patterns using the Pattern Scorecard below
3. Identify gaps (High/Medium/Low) and produce a prioritised change list
4. Commit findings to the analysis repo if available

### Mode 2 — Implementation Guide (build something new)
When designing a new agentic system:
1. Walk through the relevant pattern groups for the use case
2. Apply the implementation indicators as a design checklist
3. Flag any anti-patterns before they become technical debt

### Mode 3 — Enrichment (called by another skill)
When another skill (e.g. `boomi-health-check`) requests agentic design context:
1. Identify which patterns are most relevant to the findings
2. Provide pattern-specific recommendations in the output

---

## Pattern Scorecard (quick reference)

Use this table when scoring a project. Fill in Current State and Gap Level.

| # | Pattern | Part | Gap Level Options |
|---|---------|------|-------------------|
| 1 | Prompt Chaining | Foundations | None / Low / Medium / High |
| 2 | Routing | Foundations | None / Low / Medium / High |
| 3 | Parallelization | Foundations | None / Low / Medium / High |
| 4 | Reflection | Foundations | None / Low / Medium / High |
| 5 | Tool Use | Foundations | None / Low / Medium / High |
| 6 | Planning | Foundations | None / Low / Medium / High |
| 7 | Multi-Agent | Foundations | None / Low / Medium / High |
| 8 | Memory Management | Memory & Context | None / Low / Medium / High |
| 9 | Learning & Adaptation | Memory & Context | None / Low / Medium / High |
| 10 | Model Context Protocol | Memory & Context | None / Low / Medium / High |
| 11 | Goal Setting & Monitoring | Memory & Context | None / Low / Medium / High |
| 12 | Exception Handling & Recovery | Resilience | None / Low / Medium / High |
| 13 | Human-in-the-Loop | Resilience | None / Low / Medium / High |
| 14 | Knowledge Retrieval (RAG) | Resilience | None / Low / Medium / High |
| 15 | Inter-Agent Communication (A2A) | Advanced | None / Low / Medium / High |
| 16 | Resource-Aware Optimization | Advanced | None / Low / Medium / High |
| 17 | Reasoning Techniques | Advanced | None / Low / Medium / High |
| 18 | Guardrails & Safety | Advanced | None / Low / Medium / High |
| 19 | Evaluation & Monitoring | Advanced | None / Low / Medium / High |
| 20 | Prioritization | Advanced | None / Low / Medium / High |
| 21 | Exploration & Discovery | Advanced | None / Low / Medium / High |

---

## Part One — Foundations (Patterns 1–7)

---

### Pattern 1: Prompt Chaining

**Definition:** Decomposing a complex task into a sequence of smaller, focused LLM calls where the output of one step becomes the input of the next. Each step is optimised for a single sub-task.

**When to apply:** Any multi-step workflow where one LLM call cannot reliably handle all concerns at once — e.g. extract → transform → summarise.

**Implementation indicators (what good looks like):**
- Tasks are broken into discrete, single-purpose prompt steps
- Each step has a clearly scoped input and output contract
- Intermediate outputs are validated before passing to the next step
- Chain length is minimised — no unnecessary hops
- Steps are independently testable

**Anti-patterns to flag:**
- One massive prompt trying to do everything
- Passing entire conversation history as context to every step (unbounded token growth)
- No validation between steps — garbage flows silently through the chain
- Hardcoded step sequences that can't branch on intermediate results

**Evaluation questions:**
- Can each step in the chain be described in one sentence?
- Is each step's output format documented and validated?
- Would removing any step break the chain, or is it dead weight?

---

### Pattern 2: Routing

**Definition:** Directing agent requests to the most appropriate handler, model, tool, or sub-agent based on the content, intent, or context of the input. The router is the first decision node.

**When to apply:** When you have multiple tools/agents with different specialisations and need to dispatch intelligently without trying everything.

**Implementation indicators:**
- A clear routing decision is made before any expensive tool calls
- Router uses intent classification or keyword signals — not arbitrary order
- Routing logic is explicit and auditable (not buried in a giant system prompt)
- Fallback / "no match" route is defined
- Router decisions are logged for debugging

**Anti-patterns to flag:**
- Sequential tool-trying until one succeeds ("try everything" pattern)
- Routing hardcoded by position in a list rather than content classification
- Single monolithic agent handling all intents without routing
- Router with no fallback — unknown inputs cause silent failure

**Evaluation questions:**
- Is there an explicit routing step, or does the agent just try tools until one works?
- Can you describe the routing rules in plain language?
- What happens when no route matches?

---

### Pattern 3: Parallelization

**Definition:** Executing multiple independent agent tasks or tool calls concurrently to reduce total latency and improve throughput. Results are collected and merged after all parallel branches complete.

**When to apply:** When two or more sub-tasks have no data dependency on each other and can be safely run simultaneously.

**Implementation indicators:**
- Independent tasks are identified and launched concurrently (`Promise.all`, async parallel execution)
- No unnecessary serialisation of tasks that could run in parallel
- Results are aggregated after all branches complete
- Error handling accounts for partial failure (one branch fails, others continue)
- Parallel execution is bounded — not unbounded fan-out

**Anti-patterns to flag:**
- Sequential execution of independent API calls (unnecessary latency)
- Parallelising dependent tasks (race conditions, incorrect ordering)
- No timeout or cancellation for parallel branches
- Assuming all branches succeed — no partial-failure handling

**Evaluation questions:**
- Are there sequential steps that have no dependency on each other?
- What happens if one parallel branch fails — does the whole operation fail?
- Is parallel fan-out bounded, or can it grow unbounded with input size?

---

### Pattern 4: Reflection

**Definition:** The agent reviews and critiques its own output before presenting it, using a secondary pass (or a separate critic agent) to catch errors, improve quality, or verify correctness.

**When to apply:** High-stakes outputs — code generation, formal reports, critical decisions — where a first-pass error would be costly.

**Implementation indicators:**
- A review or validation step follows generation
- The critic uses different criteria than the generator (not just re-generating)
- Reflection output is acted upon — flagged issues cause revision, not just warnings
- Reflection is bounded — a fixed number of revision passes, not infinite
- Self-reflection is distinguishable from external validation

**Anti-patterns to flag:**
- No review step on outputs that will be acted upon directly
- Critic prompt identical to generator prompt (useless reflection)
- Infinite reflection loops with no termination condition
- Reflection that always approves (degenerate critic)

**Evaluation questions:**
- Is there any review pass on generated outputs before they reach the user?
- Does the critic actually change the output, or just rubber-stamp it?
- How many revision passes are allowed before the agent gives up?

---

### Pattern 5: Tool Use

**Definition:** The agent extends its capabilities by calling external tools — APIs, databases, code executors, file systems — to gather information or take actions beyond what the LLM can do from memory alone.

**When to apply:** Any time the agent needs current data, deterministic computation, or side effects in external systems.

**Implementation indicators:**
- Tools have precise, narrow schemas — one tool per capability
- Tool descriptions are written for the LLM, not for humans (action-oriented, unambiguous)
- Tool inputs are validated before execution
- Tool outputs are structured and predictable
- Tool errors are caught and returned as structured feedback, not raw exceptions
- Tools are stateless where possible (side-effect-free reads vs. writes are separated)

**Anti-patterns to flag:**
- Tools with vague descriptions that confuse the routing model
- One giant "do everything" tool
- Tools that return raw HTML or unstructured text when JSON would serve better
- No error handling — exceptions bubble to the top as tool failures
- Write tools with no confirmation step

**Evaluation questions:**
- Can you describe what each tool does in one sentence?
- Does each tool do exactly one thing?
- What does the tool return on error — a structured error object, or an exception?

---

### Pattern 6: Planning

**Definition:** The agent generates an explicit plan — a sequence of steps, goals, or sub-tasks — before executing, enabling it to reason about the full scope of a task before committing to any action.

**When to apply:** Complex multi-step tasks where the path to completion is non-obvious and needs to be reasoned about before execution begins.

**Implementation indicators:**
- A planning step precedes execution on non-trivial tasks
- Plans are externalised (written to memory or shown to the user) — not internal monologue only
- Plans are revisable when execution reveals new information
- Plan steps are granular enough to be individually executable and verifiable
- Planning includes contingency — "if X fails, do Y"

**Anti-patterns to flag:**
- Jumping straight to execution on complex tasks without a plan
- Plans that are too high-level to be actionable ("step 1: solve the problem")
- Plans generated and then completely ignored during execution
- Plans with no revision mechanism — stale plans applied to changed circumstances

**Evaluation questions:**
- For complex tasks, is there an explicit planning step?
- Is the plan externalised and reviewable?
- Can the plan be updated mid-execution if circumstances change?

---

### Pattern 7: Multi-Agent

**Definition:** A system of specialised agents collaborating to complete complex tasks, with one agent (orchestrator) coordinating the work of others (workers). Division of labour enables depth and parallelism.

**When to apply:** When a task requires multiple specialisations that would overload a single agent's context, or when sub-tasks can be safely delegated and run concurrently.

**Implementation indicators:**
- Clear orchestrator / worker hierarchy with defined handoff contracts
- Each agent has a single, well-scoped responsibility
- Agent communication is structured (not free-form text blobs)
- The orchestrator synthesises worker outputs — workers don't talk to each other directly unless A2A (Pattern 15) is intentional
- Agent boundaries align with capability boundaries, not arbitrary splits

**Anti-patterns to flag:**
- Agents with overlapping responsibilities causing duplication or conflicts
- Free-form string passing between agents (brittle, no schema)
- Orchestrator that micromanages each step (defeats the purpose of delegation)
- No strategy when a worker agent fails
- Multi-agent overhead for tasks that a single agent handles fine

**Evaluation questions:**
- Is there a clear orchestrator that coordinates and synthesises?
- Does each worker agent do one thing well?
- What is the structured contract for communication between agents?

---

## Part Two — Memory & Context (Patterns 8–11)

---

### Pattern 8: Memory Management

**Definition:** Strategies for persisting, retrieving, and managing information across agent interactions — including in-context memory (conversation), external memory (vector stores, databases), and episodic memory (past task records).

**When to apply:** Any agent that needs to maintain state across multiple interactions, sessions, or tool calls.

**Memory types:**
| Type | Scope | Implementation |
|------|-------|----------------|
| In-context | Current session | Conversation history, injected context |
| External | Cross-session | Vector DB, key-value store, files |
| Episodic | Past tasks | Task logs, session transcripts |
| Semantic | Domain knowledge | Reference documents, skill files |

**Implementation indicators:**
- Memory is tiered — not everything goes into the context window
- Retrieval is selective — only relevant memories are injected
- Memory has a TTL or eviction policy — stale memories are removed
- Write operations to external memory are explicit and intentional
- Memory contents are scrubbed of sensitive data before persistence

**Anti-patterns to flag:**
- Stuffing the entire conversation history into every prompt
- No persistence mechanism — every session starts from zero
- Unscrubbed credentials or tokens written to memory
- Memory that grows unboundedly with no eviction

**Evaluation questions:**
- How does the agent remember information between sessions?
- Is there a mechanism to forget or expire stale memories?
- Is sensitive data excluded from memory writes?

---

### Pattern 9: Learning & Adaptation

**Definition:** The agent improves its behaviour over time based on feedback, outcomes, and accumulated experience — either through few-shot examples updated from real interactions, or through explicit feedback loops.

**When to apply:** Repeated-task agents where performance should improve with usage; systems where user corrections should be incorporated.

**Implementation indicators:**
- Successful patterns are captured and reused (few-shot examples updated)
- Failures are logged with enough context for post-hoc analysis
- User corrections are incorporated into future behaviour (not discarded)
- There is a feedback loop — output → evaluation → adjustment
- Adaptation is bounded and auditable — not unbounded self-modification

**Anti-patterns to flag:**
- Agent that makes the same mistakes across sessions with no learning mechanism
- Feedback collected but never acted upon
- Unbounded self-modification with no human oversight
- Learning from unvalidated feedback (garbage in, garbage out)

**Evaluation questions:**
- Does the agent get better at repeated tasks over time?
- How are user corrections or feedback signals captured and used?
- Is the learning process auditable?

---

### Pattern 10: Model Context Protocol (MCP)

**Definition:** A standardised protocol for exposing tools, resources, and capabilities to LLMs in a consistent, discoverable, and interoperable way. MCP enables agents to use tools from any compliant server without custom integration.

**When to apply:** When building tool servers that need to be consumed by multiple agents or clients; when standardising how an agent discovers and calls external capabilities.

**Implementation indicators (MCP server):**
- Tools use precise Zod/JSON Schema definitions with descriptive field names
- Tool descriptions are written to guide the LLM's selection decision — not just API docs
- Resources (read-only data) are separated from tools (actions)
- Server handles errors gracefully — returns structured error objects, not raw exceptions
- Schema changes trigger server restarts — no stale schema served
- Each tool does one thing (see Pattern 5)

**Implementation indicators (MCP client/consumer):**
- Tool selection is driven by description matching, not hardcoded tool names
- Fallback behaviour when a tool is unavailable
- Tool call results are validated before being used

**Anti-patterns to flag:**
- Tool descriptions written for humans, not for LLM routing decisions
- Tools with optional parameters that are actually required in practice
- No versioning strategy for tool schema changes
- Mixing read operations and write operations in the same tool
- MCP server with no error handling — raw exceptions exposed to the LLM

**Evaluation questions:**
- Are tool descriptions optimised for LLM comprehension, not human reading?
- Are reads and writes cleanly separated into different tools?
- What does the server return when a tool call fails?

---

### Pattern 11: Goal Setting & Monitoring

**Definition:** Explicitly defining success criteria for agent tasks and continuously monitoring progress toward those goals — enabling early detection of drift, loops, or failure.

**When to apply:** Long-running agents, autonomous tasks, or any scenario where the agent could get stuck or drift from the original intent.

**Implementation indicators:**
- Goals are explicit and measurable at task start
- Progress is tracked and surfaced (status updates, step trackers, logs)
- The agent can detect when it is stuck or looping
- A timeout or maximum step count prevents infinite execution
- Completion criteria are checked against the original goal, not just "ran to end"

**Anti-patterns to flag:**
- No explicit goal state — agent runs until it decides it's done
- No timeout or circuit breaker
- Success declared when execution completes, not when goal is achieved
- No progress visibility during long-running tasks

**Evaluation questions:**
- Can you state the agent's goal in one measurable sentence?
- Is there a timeout or maximum step count?
- How does the user know what the agent is currently doing?

---

## Part Three — Resilience (Patterns 12–14)

---

### Pattern 12: Exception Handling & Recovery

**Definition:** Detecting, classifying, and recovering from failures at every layer of the agent system — tool failures, model errors, network issues, and invalid outputs — without crashing or losing state.

**When to apply:** All production agentic systems. Non-negotiable.

**Implementation indicators:**
- Every tool call has error handling — catch, classify, and respond
- Transient errors trigger retry with backoff; permanent errors escalate
- Error messages returned to the LLM are informative enough to enable recovery
- State is preserved on failure — work done so far is not lost
- Errors are logged with enough context for debugging

**Anti-patterns to flag:**
- Raw exceptions surfaced to the user or LLM
- Retry logic with no backoff (hammering a failing endpoint)
- Silent failures — error swallowed, agent continues with bad state
- No distinction between retryable and non-retryable errors

**Evaluation questions:**
- What happens when a tool call returns a 500?
- Does the agent retry? With backoff? How many times?
- Is error state preserved for debugging after a failure?

---

### Pattern 13: Human-in-the-Loop

**Definition:** Explicitly pausing agent execution to request human confirmation, input, or approval before taking consequential or irreversible actions.

**When to apply:** Before destructive operations, significant state changes, financial transactions, or any action the user should review before it executes.

**Implementation indicators:**
- Consequential actions are identified and gated on human confirmation
- The confirmation request clearly describes what will happen
- The agent waits — it does not proceed on timeout
- Human input is validated — not blindly accepted
- Override / reject paths are handled gracefully

**Anti-patterns to flag:**
- Destructive operations executed without confirmation
- Confirmation requests that are too vague ("Proceed? y/n")
- Agent proceeding after timeout without explicit user approval
- Human-in-the-loop only on obvious actions — missing subtle consequential ones

**Evaluation questions:**
- Which actions in the system are irreversible?
- Are all irreversible actions gated on explicit confirmation?
- What does the agent do if the user says no?

---

### Pattern 14: Knowledge Retrieval (RAG)

**Definition:** Augmenting the agent's responses with relevant information retrieved from an external knowledge base at query time — grounding outputs in current, domain-specific, or private knowledge the model doesn't have in its weights.

**When to apply:** When the agent needs domain knowledge, current information, or private data not in the model's training data.

**Implementation indicators:**
- Retrieval is triggered when the agent identifies a knowledge gap
- Retrieved context is filtered for relevance before injection
- Sources are cited in outputs (traceability)
- Retrieved context is bounded — no unbounded injection
- Retrieval index is kept current — stale data is identified and evicted

**Anti-patterns to flag:**
- Hallucinating answers when retrieval would provide ground truth
- Injecting entire documents rather than relevant passages
- No source citation — user cannot verify claims
- Stale knowledge base with no update mechanism

**Evaluation questions:**
- When does the agent search vs. answer from training data?
- Are sources cited in the output?
- How is the knowledge base kept current?

---

## Part Four — Advanced (Patterns 15–21)

---

### Pattern 15: Inter-Agent Communication (A2A)

**Definition:** Structured communication protocols between agents operating as peers — enabling agents to delegate, collaborate, and share results without a centralised orchestrator.

**When to apply:** Distributed agent systems where multiple specialists need to communicate directly without routing through a single orchestrator.

**Implementation indicators:**
- Agent-to-agent messages have a defined schema (not free-form text)
- Agents are discoverable — a registry or manifest describes available agents
- Message delivery is reliable — acknowledgment and retry on failure
- Agents are not tightly coupled — they can be replaced without rewriting callers
- Security: agents authenticate to each other before exchanging data

**Anti-patterns to flag:**
- Free-form string messages between agents with no schema
- Hardcoded agent addresses — no discovery mechanism
- No acknowledgment or delivery guarantee
- Agents sharing credentials or tokens through messages

**Evaluation questions:**
- What is the message contract between agents?
- How does one agent discover what another agent can do?
- What happens if the receiving agent is unavailable?

---

### Pattern 16: Resource-Aware Optimization

**Definition:** Monitoring and managing computational resources — tokens, API calls, latency, cost — to keep the agent system within acceptable bounds while maximising output quality.

**When to apply:** Production systems with cost constraints, latency SLAs, or rate limits.

**Implementation indicators:**
- Token usage is tracked and bounded per request
- Expensive operations are cached and reused
- Model selection is tiered — cheap/fast models for simple tasks, expensive/smart for complex ones
- Rate limits are respected with backoff logic
- Cost is visible — not a black box

**Anti-patterns to flag:**
- Using the most expensive model for all tasks regardless of complexity
- No caching — identical queries hit the API every time
- No token budget — context windows fill unboundedly
- Rate limit errors treated as hard failures rather than retry triggers

**Evaluation questions:**
- Is there a caching layer for repeated queries?
- Are different models used for different complexity tiers?
- Is token usage visible and bounded?

---

### Pattern 17: Reasoning Techniques

**Definition:** Explicit strategies for improving the quality of the agent's reasoning — including chain-of-thought, tree-of-thought, self-consistency, and structured decomposition — applied at prompt design time.

**When to apply:** Complex reasoning tasks where a single direct answer is likely to be wrong or shallow.

**Key techniques:**
| Technique | When | What it does |
|-----------|------|--------------|
| Chain-of-Thought | Step-by-step problems | Forces explicit reasoning steps |
| Tree-of-Thought | Exploratory problems | Explores multiple reasoning paths |
| Self-Consistency | High-stakes answers | Samples multiple answers, takes the majority |
| ReAct | Tool use | Interleaves reasoning and action |
| Scratchpad | Complex computation | Provides working space before final answer |

**Implementation indicators:**
- Prompts instruct the model to show its reasoning, not just its answer
- Multi-step problems use structured decomposition
- High-stakes outputs use self-consistency or verification
- Reasoning traces are preserved for debugging

**Anti-patterns to flag:**
- Direct answer prompts for problems requiring multi-step reasoning
- No reasoning trace — impossible to debug wrong answers
- Treating all tasks as equal complexity (over-engineering simple tasks)

**Evaluation questions:**
- For complex queries, does the agent reason step-by-step or jump to answers?
- Is the reasoning trace visible for debugging?
- Are different reasoning strategies used for different complexity levels?

---

### Pattern 18: Guardrails & Safety

**Definition:** Mechanisms that prevent the agent from generating harmful, incorrect, or unauthorised outputs — including input filtering, output validation, scope constraints, and behavioural boundaries.

**When to apply:** All production systems. Non-negotiable for any system with external users or consequential actions.

**Implementation indicators:**
- Input validation before processing (reject malformed or malicious inputs)
- Output validation before delivery (check for hallucinations, policy violations, format errors)
- Scope constraints are explicit — agent knows what it must not do
- Sensitive data is never returned in tool outputs (credentials, PII)
- Guardrail violations are logged, not silently dropped

**Anti-patterns to flag:**
- No input sanitisation — prompt injection possible
- Credentials or tokens returned in tool responses
- Agent scope defined only by "hopefully the model knows" — no explicit constraints
- Guardrail failures silently swallowed

**Evaluation questions:**
- What prevents the agent from returning sensitive data (tokens, passwords, PII)?
- Is there explicit scope definition — what the agent must NOT do?
- Are guardrail violations logged?

---

### Pattern 19: Evaluation & Monitoring

**Definition:** Systematically measuring agent performance — accuracy, latency, cost, and user satisfaction — and using those metrics to detect regression and drive improvement.

**When to apply:** Any production agent system. Required before calling a system production-ready.

**Implementation indicators:**
- Key metrics are defined: latency, error rate, cost per query, task completion rate
- Metrics are collected automatically — not manual sampling
- Baselines are established so regressions are detectable
- Evaluation runs on a representative test set
- Results are visible — not buried in logs

**Anti-patterns to flag:**
- No metrics — "it seems to work" is the only signal
- Metrics collected but never reviewed
- Evaluation on cherry-picked examples, not representative samples
- No regression detection — silent quality degradation

**Evaluation questions:**
- What metrics are tracked for this agent system?
- How would you know if quality regressed after a change?
- When was the agent last evaluated against a test set?

---

### Pattern 20: Prioritization

**Definition:** When the agent has multiple possible actions, tasks, or tool calls to consider, explicit prioritisation logic determines what to do first — based on urgency, impact, dependencies, or resource cost.

**When to apply:** Multi-task agents, agents managing queues of work, or systems where resource constraints require trade-offs.

**Implementation indicators:**
- Task/action selection uses explicit priority criteria, not arbitrary order
- Priority is dynamic — updated as context changes
- High-priority tasks preempt lower-priority ones when resources are constrained
- Prioritisation logic is auditable — not a black box inside the LLM
- Starvation is prevented — low-priority tasks eventually execute

**Anti-patterns to flag:**
- First-in-first-out with no priority weighting
- Priority hardcoded and never re-evaluated
- High-priority tasks can block indefinitely
- Prioritisation entirely delegated to the LLM with no deterministic rules

**Evaluation questions:**
- How does the agent decide what to do first when multiple tasks are pending?
- Is prioritisation logic explicit and auditable?
- Can low-priority tasks starve?

---

### Pattern 21: Exploration & Discovery

**Definition:** The agent proactively explores its environment — discovering available tools, data sources, or capabilities — rather than relying on a static, pre-defined catalogue.

**When to apply:** Dynamic environments where the set of available tools or resources changes, or when the agent should surface opportunities the user hasn't explicitly requested.

**Implementation indicators:**
- Agent can enumerate available tools/resources at runtime
- Discovery results are cached — not re-discovered on every query
- Agent surfaces relevant capabilities the user may not know about
- Exploration is bounded — agent doesn't exhaustively probe everything
- Discovery results are used to improve routing and planning

**Anti-patterns to flag:**
- Hardcoded tool lists that break when tools are added or removed
- No mechanism to surface newly available capabilities
- Exhaustive enumeration on every request (no caching of discovery results)
- Discovery that cannot distinguish relevant from irrelevant capabilities

**Evaluation questions:**
- How does the agent know what tools are available?
- What happens when a new tool is added — does the agent discover it automatically?
- Is discovery output cached and refreshed on a schedule?

---

## Evaluation Output Format

When producing a gap analysis, structure the output as:

```
## Agentic Design Pattern Audit — [Project Name]

### Overall Maturity: [Foundational / Developing / Proficient / Advanced]

### Pattern Scorecard
[table with all 21 patterns, Current State, Gap Level, Priority]

### Top Gaps (P1 first)
1. [Pattern] — [specific gap] — [file/location] — [recommended change]
...

### Strengths
- [Pattern]: [what is done well]
...

### Cross-Project Applicability
[Findings that likely apply to other projects in the same ecosystem]
```

---

## Priority Framework

| Level | Criteria | Examples |
|---|---|---|
| **P1 Critical** | Agent correctness or security at risk | No guardrails, credentials in tool output, no error handling |
| **P2 High** | Significant reliability or quality gap | No exception recovery, no memory persistence, no evaluation |
| **P3 Medium** | Best practice gap with moderate risk | No planning step, no reflection on key outputs, no caching |
| **P4 Low** | Optimisation opportunity | Parallelisation potential, better reasoning techniques |
| **P5 Advisory** | Future-state improvements | A2A, exploration/discovery, learning & adaptation |

---

## References

- Source book: `Agentic_Design_Patterns.pdf` in `boomibrianbrinley/boomi-agentic-design-patterns`
- Analysis documents: `analysis/` in `boomibrianbrinley/boomi-agentic-design-patterns`
- Frameworks referenced in the book: LangChain, LangGraph, CrewAI, Google Agent Developer Kit (ADK)
- Claude MCP documentation: https://docs.anthropic.com/en/docs/claude-code/mcp

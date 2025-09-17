---
title: "Model Context Protocol (MCP): 3 Misconceptions and Fixes"
author: "Jim Clark"
url: "https://www.docker.com/blog/mcp-misconceptions-tools-agents-not-api/"
date: "2025-09-15"
---

![lie 1920 x 1080 px e1756918175653](https://www.docker.com/app/uploads/2025/08/lie-1920-x-1080-px-e1756918175653.jpg)

**MCP is not an API. Tools are not agents. MCP is more than tools. Here’s what this means in practice.**

Most developers misread the Model Context Protocol because they map it onto familiar API mental models. That mistake breaks agent designs, observability, and the “last mile” where non-deterministic reasoning must meet deterministic execution. This piece corrects three common misconceptions and offers concrete patterns that actually work.

###**1) Misconception #1: “MCP is just another API”**

**Claim people make:**Treat an MCP call like calling REST or gRPC.
**Reality:**MCP is a model-facing protocol designed for LLM tool use, intent mediation, and context exchange. It does not replace RPC. It often uses APIs and RPC under the hood, but its purpose is to make those safely and effectively usable by non-deterministic agents.

**Why the confusion happens**

* Teams default to API thinking because it is familiar and testable.
* Most demos show “call tool, get result,” which looks like HTTP.

**What MCP actually gives you**

***Tool interfaces for models**that carry intent and affordances, not just endpoints.
***Context surfaces**beyond request/response: prompts, elicitations, and resources that shape model behavior.
***A seam between non-deterministic planning and deterministic execution**so the last mile can be reliable.

**Design patterns that work**

***API behind MCP:**Keep your stable business APIs. Wrap them with MCP tool definitions that express preconditions, success criteria, and affordances the model can reason about.
***Deterministic “last mile”:**Treat tool execution as deterministic and idempotent where possible. Validate inputs derived from model planning. Fail closed.

**Anti-patterns to avoid**

* Treating MCP tools as business APIs with complex state changes and no guardrails.
* Expecting strict schema obedience without model-aware validation and retries.

**Mini-checklist**

* Define tool preconditions and postconditions.
* Return machine-checkable outcomes the agent can evaluate.
* Log plan → tool → result so you can replay and audit.

###**2) Misconception #2: “Tools are agents”**

**Claim people make:**A tool with input and output is an agent.
**Reality:**Tools execute. Agents plan, re-plan, and evaluate. Agents loop until goals are satisfied. Tools do not.

**Why the confusion happens**

* Unix mental model: “compose tools and you get intelligence.”
* Modern LLM demos blur the line when a single call seems to “do everything.”

**What separates agents from tools**

***Agency:**goal tracking, re-planning, and error recovery.
***Evaluation:**fitness functions and success criteria, not just status codes.
***Memory and context:**prompts and resources evolve across steps.

**Design patterns that work**

***Control loop outside the tool:**Keep the agent loop responsible for deciding which tool to run next and why.
***Explicit success metrics:**Give the agent measurable checks to know if it should stop, retry, or escalate to a human.
***Human elicitation via MCP:**When confidence is low or ambiguity is high, use MCP prompts to ask the user for disambiguation.

**Anti-patterns to avoid**

* Cramming planning into a single tool invocation.
* Measuring “agent performance” only with tool latency.

**Mini-checklist**

* Write the agent’s goal, constraints, and stop conditions.
* Add retries with backoff and tool-specific error handling.
* Capture traces for each loop iteration.

###**3) Misconception #3: “MCP is just tools”**

**Claim people make:**MCP equals tool definitions with JSON in and out.
**Reality:**MCP includes**resources**,**prompts**, and**elicitations**in addition to tools. These are first-class for context-rich work.

**Why the confusion happens**

* Early adopters only wired tools and ignored the rest of the spec.
* Many examples look like “natural language over an API.”

**What you miss if you ignore the rest**

***Resources:**structured artifacts the agent can read, write, and reference across steps.
***Prompts:**reusable, versioned instruction sets the system can attach, test, and audit.
***Elicitations:**structured human-in-the-loop requests when only a user can resolve ambiguity.

**Design patterns that work**

***Resource adapters:**Map knowledge bases, files, and tickets into MCP resources with permissions and lifecycle.
***Prompt registries:**Treat prompts like code. Version, test, and roll back.
***Human checkpoints:**Define when to elicit user input and how to resume the loop afterward.

**Anti-patterns to avoid**

* Using MCP as a “voice layer” over existing services without resources or prompts.
* Hard-coding long prompts inside the application rather than managing them via MCP.

**Mini-checklist**

* Expose at least one resource type the agent can read and one it can write.
* Register prompts with IDs and versions.
* Define user elicitation flows for low-confidence branches.

**Putting it together: The architecture seam that makes AI reliable**

***Non-deterministic layer:**model planning, tool choice, re-planning, evaluation.
***Deterministic layer:**tool execution, input validation, idempotency, side-effect control.
***MCP as the seam:**tools, resources, prompts, and elicitations connect the two layers with observable traces and policies.

**Observability and governance**

* Trace plan → prompt → tool → resource updates.
* Version prompts and tool specs.
* Enforce access, rate limits, and approvals at the MCP boundary.

###**Conclusion**

If you keep thinking “API,” you will ship brittle, one-shot demos. Treat tools as deterministic executors, treat agents as planners and evaluators, and use all of MCP — tools, resources, prompts, and elicitations — as the seam where intelligent behavior meets reliable systems.

###**Implementation guide**

**Inventory APIs**and wrap them with MCP tools that declare pre/postconditions.

1.**Define agent goals**and fitness functions. Encode stop criteria.
2.**Model resources**the agent needs. Add read/write guards and retention.
3.**Stand up a prompt registry**with testing and rollback.
4.**Add human elicitations**for low-confidence paths.
5.**Instrument traces**and create replayable sessions for audits.
6.**Run chaos drills**where tools fail and confirm the agent recovers or escalates.

**Common pitfalls and how to avoid them**

***Treating MCP like REST:**Add success checks and evaluation, not just status codes.
***One-shot agent calls:**Build loops with retries and human checkpoints.
***No resource model:**The agent thrashes without durable context.
***Prompt sprawl:**Version prompts and run A/B tests.
***Opaque operations:**Without traces you cannot debug or trust outcomes.

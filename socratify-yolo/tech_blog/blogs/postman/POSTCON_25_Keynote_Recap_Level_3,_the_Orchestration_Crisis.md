---
title: "POST/CON 25 Keynote Recap: Level 3, the Orchestration Crisis"
author: "The Postman Team"
url: "https://blog.postman.com/how-to-orchestrate-apis-for-ai-workflows/"
date: "2025-09-15"
---

# POST/CON 25 Keynote Recap: Level 3, the Orchestration Crisis
![](https://secure.gravatar.com/avatar/573f4b6edb0f489da6a791474935ad1fd443825a82d943bd7d02fa52ad995ef7?s=96&d=https%3A%2F%2Fblog.postman.com%2Fwp-content%2Fuploads%2F2021%2F11%2Favatars-01.png&r=g)
[The Postman Team](https://blog.postman.com/author/thepostmanteam/)
June 30, 2025
_This blog is the fourth in a series recapping everything we shared at POST/CON 25. New here? Start with our_[ _keynote recap_](https://blog.postman.com/post-con-25-keynote-recap/ "https://blog.postman.com/post-con-25-keynote-recap/") _, then read_[ _Level 1: The Fragmented Workflow_](https://blog.postman.com/how-to-streamline-api-development-workflow/ "https://blog.postman.com/how-to-streamline-api-development-workflow/") _and_[ _Level 2: The Invisible API_](https://blog.postman.com/how-to-solve-api-distribution-disconnect/ "https://blog.postman.com/how-to-solve-api-distribution-disconnect/") _to see why we’re treating API development like a boss battle. Or jump straight to the keynote replay:_
Everything changes when your API consumers stop being human. Developers read docs, adapt to quirks, and know how to debug when things break. However, AI agents expect structured schemas, predictable responses, and workflows that never need babysitting. This is where systems fail: in the gap between expectation and reality.
Your perfectly functional APIs suddenly become unreliable. Your well-documented endpoints confuse autonomous agents. Your error handling becomes an infinite loop.
This is**Level 3: The Orchestration Crisis**, where the rules of API design get rewritten for a world where intelligence is distributed across humans and machines.
## Mission brief: Build systems that work for both humans and machines
This is a whole new gameplay mode. Building APIs and workflows that reliably support autonomous agents while also serving human developers is a real challenge. One system that does both, without a bunch of messy hacks.
The difference between success and failure comes down to execution. Teams that get this right ship features faster because they’re not maintaining parallel systems. They adapt to new AI capabilities quickly because their infrastructure is already compatible. They solve problems other teams can’t because they have both human creativity and machine scale working together.
Here’s how Postman helps you master this new game mode.
At a glance:
***AI Agent Builder**
***Model Context Protocol (MCP)**
***MCP Server Generation**
***MCP and AI Request Types**
***MCP Server Network**
***Postman Flows**
***Agent Mode (Join the waitlist)**
***Postman Ecosystem (Preview)**
## Mission 3.1: Build AI tools from the APIs you already have
**Problem:**You’ve built APIs that work perfectly for your web app and mobile clients. Now you want to add AI capabilities, but you’re looking at months of custom integration work to make your existing APIs usable by agents.
**Objective:**Transform your current APIs and collections into structured tools that agents can use safely and reliably without rebuilding everything from scratch.
### AI Agent Builder: A unified suite for building and deploying intelligent agents
Building production-ready AI agents usually involves stitching together multiple tools, writing custom integration code, and managing complex deployment pipelines. The [AI Agent Builder](https://www.postman.com/ai-on-postman/postman-ai-agent-builder/overview/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://www.postman.com/ai-on-postman/postman-ai-agent-builder/overview/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog") consolidates the process into a single, integrated workflow in Postman.
**What this changes:**
* Unifies development workflow across design, testing, and deployment
* Eliminates custom infrastructure code
* Shortens iteration cycles for rapid prototyping
* Supports scaling, monitoring, and management
﻿﻿Sorry, your browser doesn’t support embedded videos.
The AI Agent Builder is the engine behind all the other AI capabilities in Postman, powering server generation, multi-model testing, and workflow orchestration in a cohesive platform.
### Model Context Protocol (MCP): The standard for AI-API communication
MCP is becoming the de facto standard for connecting AI agents to APIs, much like REST did for web APIs. As an early adopter, you can ensure your APIs work with any MCP-compatible agent, not just specific vendors or frameworks.
**Why this matters:**
* Your APIs become instantly compatible with ChatGPT, Claude, Gemini, and future AI models
* Agents get structured access instead of guessing by parsing documentation
* You maintain full control over what agents can and can’t do
* Faster setup, safer automation, and a smoother path to production-ready agents
#### (New!) MCP Server Generation: One-click agent integration
Turn any Postman Collection into a production-ready [MCP server](https://www.postman.com/explore/mcp-generator/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://www.postman.com/explore/mcp-generator/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog"). Existing API docs, examples, and tests become the foundation for seamless agent integration.
**How it works:**
1. Take any collection: your own APIs, or public APIs from the Postman API Network
2. Generate an MCP server configuration
3. Deploy to make that API accessible to any MCP-compatible agent in your applications
﻿﻿﻿Sorry, your browser doesn’t support embedded videos.
**Example in action:**You want to build an AI assistant that can process payments. Instead of writing custom integration code for Stripe’s API, you take Stripe’s collection from the Postman API Network and generate an MCP server. This enables your AI agents to handle refunds, check payment statuses, and process transactions. The same endpoints that power Stripe’s dashboard now support your AI customer service bots, automated billing, and financial reporting.
#### (New!) MCP and AI request types: Test agent behavior with the same clarity you test APIs
Testing AI agent interactions used to be complex and full of guesswork. Now, you can test agent logic across multiple LLMs and workflows with the same clarity and control you have when testing REST APIs.
**Use the MCP request type to:**
* Import MCP server configurations directly into Postman
* Send MCP requests alongside HTTP, gRPC, and WebSocket calls
* See exactly what data agents receive and how they respond
* Validate tool behavior across different scenarios before deployment
**Use the AI request type to:**
* Run the same prompt across Claude, GPT-4, Gemini, and other models side-by-side
* Compare how different models handle your API error responses
* Optimize prompts for specific models and use cases
* Validate agent logic consistency across providers
**Example in action:**You’re building an agent that processes customer support tickets. Testing the same ticket classification prompt across three models reveals clear differences: GPT-4 correctly categorizes 94% of tickets but sometimes hallucinates urgency levels, Claude gets 89% accuracy but handles edge cases more reliably, while Gemini processes tickets fastest but struggles with technical terminology. Now, you can choose the right model based on real data, not marketing claims.
#### MCP Server Network: Find trusted tools for agents without the guesswork
Building effective agents starts with reliable APIs. The [MCP Server Network](https://www.postman.com/explore/mcp-servers/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://www.postman.com/explore/mcp-servers/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog") is a curated public workspace featuring verified, ready-to-use MCP servers for popular APIs like Stripe, Notion, and Google Maps.
**What’s available:**
* Verified MCP servers for essential business tools
* Community contributions with usage metrics, reliability scores, and peer reviews
* Quality assurance that ensures tools work consistently in production environments
* Regular updates to keep pace with API changes and new features
Developers can build faster with confidence. API publishers can make their tools discoverable and agent-ready without bespoke tooling or integrations.
![](https://blog.postman.com/wp-content/uploads/2025/06/MCP-Server-Network-1024x625.png)
**Example in action:**A startup building an AI-powered development assistant wants to help developers with repository management and code reviews. Instead of writing custom integration code for GitHub’s API, they use the pre-built GitHub MCP server from the network. In one afternoon, their AI agent can create pull requests, review code changes, and manage issues. They ship developer productivity features instead of building API integrations.
### Postman Flows: Visual orchestration that handles AI reality
Flows offers a visual canvas for building workflows that combine APIs, AI models, and business logic. By handling variable responses, model failures, and human oversight where necessary, Flows is designed to manage the unpredictability of AI, unlike traditional workflow tools.
**What makes Flows different:**
* Visual workflow design that’s accessible to developers, PMs, and domain experts
* Native AI model support for OpenAI, Anthropic, and more
* Trigger-based execution that responds to webhooks, schedules, or API calls
* Error handling built for AI-specific failure modes like hallucinations, rate limits, and model downtime
* Observable execution with detailed logs and debugging tools
#### (New!) Flows Actions: Deploy workflows without managing infrastructure
With [Flows Actions](https://learning.postman.com/docs/postman-flows/build-flows/actions/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://learning.postman.com/docs/postman-flows/build-flows/actions/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog"), deploy any workflow to Postman’s cloud with one click. Turn your visual workflows into production services that scale automatically and integrate with your existing systems.
![](https://blog.postman.com/wp-content/uploads/2025/06/Flows-Actions-1024x686.png)
### Agent Mode (Join the waitlist): AI pair programming for APIs
[Agent Mode](https://www.postman.com/product/agent-mode/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://www.postman.com/product/agent-mode/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog") is a conversational agent inside Postman that can take action on your behalf. It can send requests, build collections, write tests, and fix broken workflows using the same tools you already use.
**What Agent Mode can do:**
* Generate full API collections from requirements or documentation
* Debug failing requests and suggest or implement fixes automatically
* Write comprehensive test suites based on actual API behavior
* Optimize workflows based on usage data and performance metrics
![](https://blog.postman.com/wp-content/uploads/2025/06/Agent-Mode-1024x632.png)
And soon, it’ll extend beyond Postman with API access and MCP integration, giving you automation that scales with your systems.
_Agent Mode is now rolling out to external users.[Join the waitlist](https://www.postman.com/product/agent-mode/ "https://www.postman.com/product/agent-mode/") to have it enabled in your account._
## Mission complete: You’ve defeated the Inconsistent System
Your development stack now includes:
***Hybrid-ready APIs**that serve both human developers and AI agents with equal reliability and performance
***Orchestrated workflows**that blend human judgment with AI automation at any scale
***Observable automation**that maintains control and debugging clarity even as complexity grows
***Ecosystem integration**that connects AI capabilities to your existing development and deployment workflows
You’re not choosing between human efficiency and machine intelligence anymore. You’ve built systems that amplify both.
### Postman Ecosystem (Preview): Connect everything you build
You’ve built intelligent systems. Now imagine scaling that across every tool, team, and platform.
The Postman Ecosystem extends everything you’ve created. From API security to SDKs and gateways, it integrates with the [tools you already use](https://www.postman.com/product/integrations/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog), and lets you build new ones to match your workflow.
**How it extends your work:**
* API gateways help developers onboard, troubleshoot, and stay on top of changes
* API security tools surface potential vulnerabilities and help you ship more secure APIs
* SDKs and documentation drive distribution and accelerate onboarding
![](https://blog.postman.com/wp-content/uploads/2025/06/Postman-Ecosystem-1024x576.png)
**The vision:**A team builds intelligent systems using the tools from Mission 3.1. When they deploy an API change, the ecosystem kicks in to run security scans and pull context from gateways, all from unified workflows that scale across the team’s entire stack.
_[Apply for early access](https://www.postman.com/developers/ecosystem/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog) to build an app for the Postman Ecosystem._
## Game complete: The new era of API development
We used a gaming metaphor to tell the POST/CON 25 story, but what we’re describing is a fundamental shift in how software gets built. APIs have evolved from simple data connectors into the intelligent infrastructure behind hybrid human-AI systems.
You’re no longer just building endpoints. You’re creating the foundation for collaboration between human developers and AI agents. Systems that adapt to both creativity and computation. Workflows that scale human decision-making with automated execution. Infrastructure that gets smarter as AI advances.
The levels are complete, but this is where the real work begins.
The tools are here, the standards are emerging, and the early adopters are pulling ahead. The question isn’t whether AI will transform software development, it’s who will define what that transformation looks like.
**It’s your move.**[Join the community](https://community.postman.com/t/build-your-reputation-by-contributing-to-the-postman-community/80055/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog "https://community.postman.com/t/build-your-reputation-by-contributing-to-the-postman-community/80055/?utm_campaign=global_fy26q2_postcon25-keynote&utm_medium=web&utm_source=postman_blog&utm_content=level-3-keynote-blog") to share what you’re building, earn certifications that prove your expertise, and connect with other developers shaping the future of human-AI collaboration.
Tags: [AI](https://blog.postman.com/tag/ai/) [API Development](https://blog.postman.com/tag/api-development/) [API-First](https://blog.postman.com/tag/api-first/) [Collaboration](https://blog.postman.com/tag/collaboration/) [Collections](https://blog.postman.com/tag/collections/) [POST/CON](https://blog.postman.com/tag/post-con/) [Postman Collections](https://blog.postman.com/tag/postman-collections/)
![](https://secure.gravatar.com/avatar/573f4b6edb0f489da6a791474935ad1fd443825a82d943bd7d02fa52ad995ef7?s=80&d=https%3A%2F%2Fblog.postman.com%2Fwp-content%2Fuploads%2F2021%2F11%2Favatars-08.png&r=g)
The Postman Team
Postman is the single platform for designing, building, and scaling APIs—together. Join over 40 million users who have consolidated their workflows and leveled up their API game—all in one powerful platform.
[View all posts by The Postman Team →](https://blog.postman.com/author/thepostmanteam/)

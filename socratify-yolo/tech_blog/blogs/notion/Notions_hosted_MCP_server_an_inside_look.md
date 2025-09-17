---
title: "Notion’s hosted MCP server: an inside look"
company: "notion"
url: "https://www.notion.so/blog/notions-hosted-mcp-server-an-inside-look"
focus_area: "block-based systems, database architecture, real-time sync"
system_score: 98
content_length: 13322
type: "comprehensive_systems_collection"
date: "2025-09-15"
---

[All posts](/blog)

[← All posts](/blog)

Published July 15, 2025 in [Tech](/blog/topic/tech)

# Notion’s hosted MCP server: an inside look

By Kenneth Sinder

Software Engineer, Notion

8 min read

Share this post

  * [](http://twitter.com/share?text=Notion’s hosted MCP server: an inside look&url=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)
  * [](https://www.linkedin.com/sharing/share-offsite/?url=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)
  * [](https://www.facebook.com/sharer/sharer.php?u=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look&t=Notion’s hosted MCP server: an inside look)
  * [](/cdn-cgi/l/email-protection#6d520f020914502302190402038fedf41e4d05021e1908094d202e3d4d1e081f1b081f574d0c034d04031e0409084d01020206485d2c0519191d1e5742421a1a1a43030219040203430e0200420f01020a420302190402031e4005021e19080940000e1d401e081f1b081f400c034004031e04090840010202064b0c001d561e180f07080e19502302190402038fedf41e4d05021e1908094d202e3d4d1e081f1b081f574d0c034d04031e0409084d01020206)



When Anthropic announced [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) in November 2024, the vision was simple but powerful: Align tech companies and builders around a universal language to discover and interact with tools.

MCP goes beyond conventions like REST, which has powered web APIs for decades. It provides _context_ to large language models (LLMs) so they know when and how to use each of the tools a provider like Notion, Figma, or Stripe broadcasts. Skipping the usual process of piecing together technical docs to build a traditional API integration, customers interact with systems using natural language as part of a conversation or workflow.

Cursor and Claude Code are **MCP clients,** or LLM “frontends,” that act as end user–facing agents. They convert natural-language requests into calls to actions (“tools”) offered by different service providers called **MCP servers** —think Notion, Stripe, or Figma.

Earlier this year, Notion began to get requests for an MCP server. We heard from large enterprises embracing AI-first workflows into their knowledge-work and product-development processes. We also heard from individual toolmakers, developers, and Notion Ambassadors who wanted an easy solution to migrate data into Notion and interact with their workspaces from familiar LLM tools like Cursor and Claude Desktop.

As an initial proof-of-concept, we wanted to provide Notion’s existing API capabilities as AI-invokable actions, proving how the “tools” model unlocks productivity in agentic workflows.

![](/_next/image?url=%2Ffront-static%2Fshared%2Fcallouts%2Fnote-illustration.png&w=128&q=75)

**You might see**[ posts out there](https://www.latent.space/p/why-mcp-won)**boasting MCP as the “winner”** over REST API documentation and specification tools like OpenAPI. While we’re excited about MCP’s popularity, **we see these technologies working together**. Even with MCP, there’s a need for structured conventions. The [TypeScript SDK for MCP supports](https://github.com/modelcontextprotocol/typescript-sdk/blob/dd69efa1de8646bb6b195ff8d5f52e13739f4550/README.md#quick-start) the Zod library for defining each tool’s spec.

Fast-forwarding to today: we’ve built a code-generation pipeline for Notion’s hosted MCP server, converting our generated OpenAPI schemas to Zod and plumbing those into the hosted MCP server’s tools.

## First release: open-source MCP server

We started by releasing a downloadable [notion-mcp-server](https://github.com/makenotion/notion-mcp-server?tab=readme-ov-file) in early April. It could be installed in Cursor or Claude Desktop (though it required technical knowledge). Setup involved creating a new Notion API integration and either copying the API key into MCP headers or building a Docker image. Once configured, it enabled flows like creating pages in Notion from AI agent chat.

![GIF \(taken from the notion-mcp-server README file\) of using Cursor AI chat to create a page in Notion using the open-source MCP server.](https://images.ctfassets.net/spoqsaf9291f/KOqFQjcqg1VWBPy4zRc1T/9092c3c4a7391f4c8bfe167102e169c4/mcp_server.gif)

GIF (taken from the notion-mcp-server README file) of using Cursor AI chat to create a page in Notion using the open-source MCP server.

Behind the scenes, the library parsed Notion’s [public OpenAPI spec](https://github.com/makenotion/notion-mcp-server/blob/9eb8ec3e3588aff626452dc36962740f6d85d8b5/scripts/notion-openapi.json#L4), a formal description of available API endpoints and their interfaces. It processed this file, converting MCP tool calls into HTTP API calls to Notion’s public API using your configured API key. Each API endpoint mapped 1:1 to an MCP tool in the server. The MCP server received requests from the MCP client and translated them to API calls, personalized for your download.

Though adoption was challenging and functionality was limited, we wanted to move quickly to get something in the hands of our users. Feedback from early adopters revealed two critical insights: the technical barrier was too high for widespread adoption and the 1:1 API mapping created suboptimal experiences for AI agents, like high-context token consumption from working with hierarchical block data in JSON.

## Today: all-in-one remote MCP solution

These learnings shaped our next iteration—we’ve worked hard to expose a powerful combination of existing and new tools for anyone to use, deepening Notion’s value as a connected workspace. Imagine going from a requirements doc in Notion to a working prototype in Cursor, updating task statuses on the fly and updating project stakeholders, all without leaving your code editor.

The key insight: It’s now easier for AI agent tools to plug into your Notion workspace, empowering a more intuitive agent experience by:

  * **Hosting our own MCP server** with a rapid development loop using our existing codebase and internal tooling. Notion can quickly ship improvements without requiring users to download updated packages.

  * **Creating a single central integration** that exposes a tailored suite of tools optimized for AI agents—not HTTP calls to the API. We can skip RESTful web API practices and ship “private” functionality slices with LLM-friendly descriptions, accessible only through the MCP server, for a delightful agent experience.




![High-level diagram of the MCP data flow, where Notion hosts both the MCP Server and the Public API, and your tools contain MCP clients that connect to the remote MCP server to access our tools.](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fspoqsaf9291f%2F7Eb8JtrKn4L9zWRyp0NjcU%2Fa2023910fa72b1ff4e9ee2375a0c8b5f%2Fmcp_data_flow.png&w=3840&q=75)

High-level diagram of the MCP data flow, where Notion hosts both the MCP Server and the Public API, and your tools contain MCP clients that connect to the remote MCP server to access our tools.

Now, each user goes through a “one-click” OAuth authorization flow to securely connect to the same public integration. Users install MCP in their workspace, granting the permissions they have normally in the app to the MCP integration.

After successful connection, the flow redirects back to the tool they were using (like Cursor). Our MCP server manages sessions and securely stores the API token from the OAuth exchange to authenticate with Notion’s public API when they make tool calls.

We worked closely with Cursor’s engineering team to prioritize a delightful OAuth connection experience using streamable HTTP. We also support SSE (server-sent events) for compatibility with more clients, as it’s the other major transport protocol recommended for MCP.

Beyond tech stack and hosting, we also needed to decide which AI tools to offer. Our approach: work with the team building the in-app Notion Agent to expose AI-first tools preferably over existing `/v1/` API endpoints.

To build the set of MCP tools, we combined two kinds of operations under the hood:

  * **Notion Agent–oriented tools**. For example, `create-pages` and `update-page` are new, ground-up rewrites of existing Create & Update Page APIs, providing interfaces that make more sense for an AI agent conversation than a traditional, rigid web API. 

    * Built with Notion-flavored Markdown in mind, with tool descriptions and responses tailored for agentic workflows rather than deterministic, structured JSON for backend integrations.

    * Markdown provides efficient content density per LLM token, requiring fewer tool interactions and less cost than the open-source MCP server for common use cases.

    * The `search` tool fits here too. We exposed the existing v1 search API to cover simple use cases or accounts without Notion AI enabled, but the main `search` tool supports semantic search via questions, surfacing pages across your Notion workspace plus over ten third-party connected apps!

  * **Existing API tools**. Borrowing from the open-source MCP server’s success, we closed functionality gaps by adding MCP tools that wrap existing v1 APIs. 

    * For example, the `create-comment` tool v1 API functionality, augmented with AI-friendly tool descriptions to avoid rough edges from the open-source package.

    * These prompts give your MCP client context on when and how to use each tool.




This combined strategy provides expansive functionality while ensuring details like Notion’s URLs and IDs work seamlessly across tool calls in your chat window.

## Highlight: Notion-flavored Markdown

The Notion MCP beta gave us an opportunity to trial a new way of representing page content that’s much easier for AI agents to create, edit, and view. We pioneered an enhanced “Notion-flavored” Markdown spec, creating a powerful markup language tailored to Notion’s broad set of blocks.

If you’ve followed us for a while, you might remember [our 2022 blog post](https://www.notion.com/blog/creating-the-notion-api) about building the Notion API. Back then, we rejected Markdown in favor of JSON to allow for expressiveness like rich-text colors, databases, and other Notion-specific editing that CommonMark Markdown can’t model.

Three years later, we’ve heard about the challenges of making several API requests to work with block children in a hierarchical JSON format. We came back to Markdown to introduce feature parity with Notion blocks, trialing this approach exclusively in our remote MCP server.

Here’s a sneak peek at the Notion-flavored Markdown spec:

**Callouts**

![Notion-flavored Markdown: ](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fspoqsaf9291f%2F6g8cy9WKZzXAa3Uost7hxL%2F1a43c27fc335a1f24dcf3c7310bec091%2FScreenshot_2025-07-10_at_2.56.18%C3%A2__PM.png&w=3840&q=75)

**Columns**

![Notion-flavored Markdown: ](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fspoqsaf9291f%2F57HMWeXbCF4YKFQJ0a0LpY%2F812116d9e9e48e5121e9714ad1e7981a%2FScreenshot_2025-07-10_at_2.56.33%C3%A2__PM.png&w=3840&q=75)

**Pages**

![Notion-flavored Markdown: ](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fspoqsaf9291f%2F5tJCiZX4j4rjZBDp2M7nbf%2F9056c2fa7da0a6e815959f6b985ae1b3%2FScreenshot_2025-07-10_at_2.56.46%C3%A2__PM.png&w=3840&q=75)

**Databases**

![Notion-flavored Markdown: Databases](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fspoqsaf9291f%2F5kHWrL54KJkrHnpjCo5FS9%2Fec250a7000675b17a3cdb15d10e3b16c%2FScreenshot_2025-07-10_at_2.57.01%C3%A2__PM.png&w=3840&q=75)

More details are available in the tool descriptions exposed via the MCP server. In fact, you can ask your AI agent in chat to summarize the Notion-flavored Markdown spec for you! Otherwise, leave the implementation details to us and describe in natural language what you want to add or edit in a page—let the LLM do the magic.

## Looking forward

This launch represents just the beginning of our journey to make Notion the ultimate hub for AI-powered knowledge work. As we continue expanding our MCP capabilities, we’ll keep focusing on what matters most: making powerful tools accessible to everyone, regardless of technical expertise.

We’re also continuing to collaborate with Cursor and other teams to lead the way on new conventions that make MCP easier to discover, more secure, and more dependable, like marketplaces of trusted MCP servers and clients and server discovery protocols.

We’re thrilled to see what you’ll build with Notion MCP! Let us know what you create on social at @NotionHQ.

Share this post

  * [](http://twitter.com/share?text=Notion’s hosted MCP server: an inside look&url=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)
  * [](https://www.linkedin.com/sharing/share-offsite/?url=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)
  * [](https://www.facebook.com/sharer/sharer.php?u=https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look&t=Notion’s hosted MCP server: an inside look)
  * [](/cdn-cgi/l/email-protection#19267b767d602457766d707677fb99806a3971766a6d7c7d39545a49396a7c6b6f7c6b233978773970776a707d7c39757676723c2958716d6d696a2336366e6e6e3777766d707677377a7674367b75767e3677766d7076776a3471766a6d7c7d34747a69346a7c6b6f7c6b3478773470776a707d7c34757676723f787469226a6c7b737c7a6d2457766d707677fb99806a3971766a6d7c7d39545a49396a7c6b6f7c6b233978773970776a707d7c3975767672)



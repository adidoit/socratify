---
title: "Reports of Deno's Demise Have Been Greatly Exaggerated"
author: "Unknown"
url: "https://deno.com/blog/greatly-exaggerated"
date: "2025-09-15"
---

# Reports of Deno's Demise Have Been Greatly Exaggerated

May 20, 2025[](/feed "Atom Feed")

* [![](https://github.com/ry.png)Ryan Dahl](https://github.com/ry)

* [Deno Deploy](/blog?tag=deno-deploy)

There’s been some criticism lately about Deno - about Deploy, KV, Fresh, and our momentum in general. You may have seen some of the criticism online; it’s made the rounds in the usual places, and attracted a fair amount of attention.

Some of that criticism is valid. In fact, I think it’s fair to say we’ve had a hand in causing some amount of fear and uncertainty by being too quiet about what we’re working on, and the future direction of our company and products. That’s on us.

In other places, recent criticisms have been inaccurate, or speculative. That’s why we’re writing this post; to set the record straight. This is a catch-up on where we are, what we’ve learned, and what we’re building next. Some have feared that Deno itself is diminishing or fading away, but this couldn’t be further from the truth. Since the release of [Deno 2](/2) last October - barely over six months ago! - Deno adoption has more than doubled according to our monthly active user metrics. Deno 2’s robust Node compatibility effectively removed a major adoption barrier, unblocking a wide range of serious use cases. The platform has gotten faster, simpler, and more capable. Deno is now used more widely - and more seriously - than ever before.

## Deno Deploy

One of the biggest questions we’ve been hearing is about Deno Deploy â€” specifically, the reduction in available regions. While we understand the optics of this scaling back, it isn’t for the reasons often feared or accused.

Rather, reality is: most applications don’t need to run everywhere. They need to be fast, close to their data, easy to debug, and compliant with local regulations. We are optimizing for that.

We launched Deno Deploy in 2021 to explore a new model for serverless JavaScript. It started in 25 regions, grew to 35, and now runs in 6. That reduction was driven by cost, yes - but also by usage. Most developers weren’t deploying simple stateless functions. They were building full-stack apps: apps that talk to a database, that almost always is located in a single region. We saw that most of the time, the excess regions were mostly unused. When traffic spikes came, the idle regions would hit capacity quickly causing latency spikes. We found that routing to a further away larger region was often faster than running in a nearby cold one.

We were chasing a vision of “edge” that didn’t match how people were actually using the service. We shouldn’t have been silent about this.

Deno Deploy is under heavy development - we haven’t quite released the latest version yet, but it’s imminent. You can [request early access here](https://dash.deno.com/account).

Deploy is evolving into a platform for hosting applications - not just functions. It’ll support subprocesses, background tasks, OpenTelemetry, build pipelines, caching, and even self-hosted regions. It runs full-stack frameworks like Next.js, SvelteKit, and of course, Fresh.

Soon, you’ll be able to pin your app to a region - or run it in your own cloud. That’s something we’ve heard again and again from users who care about control, compliance, and performance. More coming soon.

## KV

[Deno KV](/kv) is our zero-setup, globally consistent key-value store with a simple API and [real-time capabilities](https://docs.deno.com/examples/kv_watch/). We realize that for things like session data, feature flags, and collaborative presence, KV works great. Developers love it for what it is: a zero-config global store that just works.

But it doesn’t solve everything. It’s not a general-purpose database, and it doesn’t replace relational systems for most applications. To address these broader needs for state management, we have multiple efforts in the pipeline:

* Firstly, we’re working on making traditional relational databases more readily available and simpler to use within Deno Deploy.

* And secondly, we believe that Deno KV itself doesn’t go far enough in simplifying how compute and state are bound. So, inspired by systems like Cloudflare’s Durable Objects, we are working on a new project to achieve this deeper integration, aiming to bind state directly to computation.

Given these new directions, Deno KV will remain in beta. We will continue to address critical bugs and security issues for its current version. While KV is useful for its intended purpose, its role is not to be the central or evolving solution for all state management in Deno. We reserve the right to make significant changes to Deno KV in the future as these other state initiatives mature and our overall platform strategy evolves. We’re excited to share more on these new pipeline projects soon.

## Fresh

Fresh is alive and well - it powers every app and website we build. We know many of you have been eagerly anticipating Fresh 2, and perhaps some have felt frustrated by the wait. We hear you. We could have shipped something sooner, but it was crucial to get the fundamentals right and we didn’t want to compromise on quality for a quick marketing splash. We depend on Fresh for all our sites, so its excellence is paramount. We just wrote a detailed [post](/blog/an-update-on-fresh) about the significant improvements coming in Fresh 2 â€“ go read it! A stable release is coming later this year.

## Deno, the runtime platform

Deno isn’t just a runtime anymore; it’s a complete platform for building and running JavaScript systems. Here’s what’s built in:

* [TypeScript](https://docs.deno.com/runtime/fundamentals/typescript/) and [JSX](https://docs.deno.com/runtime/reference/jsx/) support
* [Granular permissions and sandboxing](https://docs.deno.com/runtime/fundamentals/security/) for secure execution
* A full [Language Server Protocol](https://docs.deno.com/runtime/reference/lsp_integration/) (LSP), [VS Code extension](https://docs.deno.com/runtime/reference/vscode/), and [`deno check`](https://docs.deno.com/runtime/reference/cli/check/) for type checking
* [Jupyter notebook integration](https://docs.deno.com/runtime/reference/cli/jupyter/) with LSP-powered TypeScript type checking
* [`deno compile`](https://docs.deno.com/runtime/reference/cli/compile/) to generate standalone binaries
* [Strong Node/npm compatibility](https://docs.deno.com/runtime/fundamentals/node/), including [workspace support](https://docs.deno.com/runtime/fundamentals/workspaces/)
* First-class observability via [built-in OpenTelemetry](https://docs.deno.com/runtime/fundamentals/open_telemetry/), providing structured tracing out-of-the-box.**This is an essential infrastructure piece, not an afterthought, as some have derided.**
* [`deno fmt`](https://docs.deno.com/runtime/reference/cli/fmt/) for auto-formatting JavaScript, TypeScript ([and even CSS or SQL within template strings](https://deno.com/blog/v2.3#improvements-to-deno-fmt))
* [Fundamentally built on ES Modules](https://docs.deno.com/runtime/fundamentals/modules/) and [web standards](https://docs.deno.com/runtime/reference/web_platform_apis/)
* A global deploy surface (via [Deno Deploy](/deploy))
* A publishing system ([JSR](https://jsr.io)) with open governance, [a growing standard library](https://jsr.io/@std), and excellent workspace support

You can write, run, test, deploy, and monitor - all with a single toolchain. We’ve been tightening integration. Fewer flags. Better defaults. Smaller gaps. The pieces work together better than ever before.

We’re not chasing feature parity with other runtimes. We’re building a cohesive system. We’re trying to fundamentally improve JavaScript development. If we have faulted, it’s because we’ve stretched too far in this goal. But I don’t think anyone can argue that Deno isn’t striving for a better world for the world’s default programming language.

## Why we’re doing this

Scripting languages are the ergonomic end-state for a large class of problems: business logic where engineering time is the limiting factor.

Ruby, Python, Lua, Perl, and JavaScript all follow that thread. But JavaScript is the one distributed on every device, with standards bodies, independent implementations across tech conglomerates, and a massive vibrant ecosystem. The scripting language with a future we believe is JavaScript (and TypeScript). It deserves a platform to match, not a patchwork of ad hoc tools. A single batteries included system.

Just like JavaScript gives you garbage collection and built-in arrays, Deno gives you a permissions system, a web server, observability, linting, and type safety - all out of the box. You don’t need to glue it together. Deno is the glue.

## Looking ahead

We’re not winding down. We’re winding up.

We’re continuing to improve performance, compatibility, and polish across the platform. JSR is maturing. We’ve [recently established](/blog/jsr-open-governance-board) an Open Governance Board and are actively working to transition JSR into an independent, community-driven foundation.

Our work in [TC39](https://github.com/tc39/proposal-source-phase-imports) and [WinterTC (formerly WinterCG)](https://deno.com/blog/wintertc) continues. We’re also [actively challenging Oracle’s misleading JavaScript trademark](https://javascript.tm/). This is all part of our broad effort to improve and grow the JavaScript ecosystem.

We’re building new products based on everything we’ve learned from Deploy and KV, not yet released. They aim to make persistent, distributed applications simpler. More on that very soon.

We recognize that our silence has sometimes been a source of uncertainty, and we’re committed to improving our communication as we move forward with these exciting developments.

Thanks for reading. And to everyone building with Deno: thank you.

â€“ Ryan

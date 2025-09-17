---
title: "Building Aira, Postman’s Product Research Agent"
author: "Numaan Ashraf"
url: "https://blog.postman.com/building-aira-postmans-product-research-agent/"
date: "2025-09-15"
---

# Building Aira, Postman’s Product Research Agent
![](https://secure.gravatar.com/avatar/dd5833357e08f39ede0b78e7accdfd8da16e31fcccdff6996c5996d67ca3149e?s=96&d=https%3A%2F%2Fblog.postman.com%2Fwp-content%2Fuploads%2F2021%2F11%2Favatars-05.png&r=g)
[Numaan Ashraf](https://blog.postman.com/author/numaan-ashraf/)
August 27, 2025
At our company, we’re constantly experimenting with how AI agents can accelerate real-world work. One of our most useful internal agents so far has been**Aira**, our product research agent built on top of our agent platform to automate research on user feedback. This project taught us not only how to build quickly, but also how to involve users early, learn from their behavior, and evolve the agent into something that truly saves time and creates value.
In this post, we’ll walk through:
1. Why we built this agent
2. The design principles we followed
3. How we implemented it step by step
4. What worked, what didn’t, and what’s next
### Why Build a Research Agent?
Every product team faces the same challenge: staying on top of market trends, user feedback, and customer signals. Doing this manually is slow, repetitive, and error-prone. For example:
* You can easily end up with dozens of user issues and comments open in separate tabs, making it hard to see the big picture.
* Summarizing key insights for a decision can take hours of scrolling, copying, and piecing together notes.
* Different teams often repeat the same research because there’s no single system collecting, analyzing, and sharing insights.
We wanted an agent that could:
***Continuously scan**Postman’s issue tracker.
***Extract structured insights**such as user workflows, pain points, feature requests, workarounds, and reactions.
***Summarize in context**so that product managers and leaders could immediately act on the information.
***Integrate seamlessly into existing workflows**like Slack, so users wouldn’t need to change the way they already work.
The goal was not to build a perfect system from the start, but to create a tool that could evolve over time, getting smarter and more useful as more people interacted with it.
### Design Principles
We set a few non‑negotiable design principles before we started building:
1.**Agent-as-a-colleague:**The agent should feel like a teammate – easy to talk to and able to hold a natural, conversational exchange.
2.**Composable capabilities:**The agent should be built from smaller parts (search, retrieval, security, user experience, usage analytics) that could be reused or upgraded easily.
3.**Ship fast & iterate with real users:**We start small, ship quickly, and rely on user feedback to show us what advanced features mattered most.
### Agent Development
#### 1\. Quick Prototype
We built our first prototype in a single afternoon. It only handled a single issue on our [issue tracker on GitHub](https://github.com/postmanlabs/postman-app-support/issues), but it extracted meaningful insights: user pain points, workflows, proposed workarounds, and overall sentiment. Even though it was basic, it proved that we could quickly turn raw feedback into something actionable.
For this first prototype, we used the GPT‑4.1 model. We chose it because of its very large context window (up to one million tokens) allowed us to process GitHub issues with hundreds of comments without losing context. This gave the prototype enough capacity to capture the full flow of discussion within an issue and summarize it effectively.
While the Agent Block from our agent platform (Postman Flows) managed the core agent loop, we still had to equip it with the right tools to work in practice. To begin with, we provided a small but useful set of tools so the agent could operate directly inside Slack and combine Slack conversations with GitHub issue data. These initial tools included:
* Get last n messages from a Slack channel (for conversation context)
* Send a message to a Slack channel
* Get issue information from GitHub
* Summarize issue comments from GitHub
![](https://blog.postman.com/wp-content/uploads/2025/08/image-19-1024x620.png)
Using OpenAI models within the AI Agent block in Postman Flows, combined with the GitHub API, we created a working prototype in less than an hour. Even more important, we could deploy it instantly, generate a shareable URL, and connect it to a Slack app. By the end of the first day, people were already trying it out in Slack conversations.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-10-1024x539.png)Aira prototype working with Abhinav, Postman’s CEO, directly in Slack
#### 2\. User Feedback & Iteration
Once people started using it, we began to see real patterns in the questions they asked. Flows analytics and detailed logs gave us visibility into what users wanted, how they phrased their questions, and where our agent was falling short. It wasn’t enough to summarize individual issues, users wanted to see patterns, trends, and broader insights.
![analysing real user queries and agent's response with Flows Analytics](https://blog.postman.com/wp-content/uploads/2025/08/image-12-1024x662.png)
Product managers asked for features like weekly sentiment analysis, the ability to find correlations between different pain points, and clustering of related requests. This feedback guided our next iteration. We also used Postman workspace updates to share progress and structured updates directly with pilot users in Slack. This helped close the feedback loop and made it clear that their input was directly shaping the agent.
![closing the feedback loop via Postman's workspace updates after a new agent version is deployed](https://blog.postman.com/wp-content/uploads/2025/08/image-13-1024x616.png)
#### 3\. Scaling Up
After getting user feedback and realizing that users wanted to see patterns, trends, and broader insights, our first architecture quickly reached its limits.
There were two main reasons it did not scale well:
* The GitHub issue tracker had over 3,000 open issues and more than 10,000 closed issues. That sheer volume made it difficult to handle with one-off retrieval calls.
* It was unrealistic for the agent loop to fire off thousands of API calls for a single query and then try to fit all of that data into even the largest context windows.
To move forward, we needed a new approach: creating a knowledge base for the full issue tracker that the agent could rely on as its source of truth.
We chose to build this knowledge base as a knowledge graph. The reason was clear – user questions were increasingly horizontal, spanning across many issues at once rather than diving deep into a single thread. We began to see repeated themes in the questions, such as workflows, solutions, and user reactions spread across multiple issues. A knowledge graph gave us the structure to connect those issues together through relationships, letting the agent surface insights that were not visible when looking at issues one by one.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-14-1024x804.png)Aira’s knowledge graph
By reusing the extraction methods from our first version, we could process every issue and build this graph knowledge easily, choosing Neo4j as the underlying database to store and query the graph effectively. At the same time, we upgraded the model to a reasoning-class, moving from GPT‑4.1 to o3. Upgrading to a reasoning-class model proved transformative – once we provided the agent with precise context about the knowledge graph’s schema and relationships, the model could iteratively refine its queries, learning from each attempt and steadily improving its ability to generate accurate, useful results. Thanks to built-in support for these models within the Flows AI Agent Block, the transition was quick and seamless. This shift from single-issue insights to cross-issue analysis was when the agent started to feel like a truly powerful research assistant.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-20-1024x608.png)Aira’s architecture with knowledge graph
![](https://blog.postman.com/wp-content/uploads/2025/08/image-21.png)Aira’s core agentic loop on Postman Flows ![](https://blog.postman.com/wp-content/uploads/2025/08/image-9-1024x533.png)Aira’s cross-issue analysis
While building this agent, one of our core design principles was to create composable components that could be reused both within this agent and across any other agents we build. By investing early in reusable modules, we reduced duplication and sped up future development.
The most important reusable components we developed include:
**Slack Authentication**
Postman Flows allows us to expose the entire workflow as an endpoint. When registering for events such as incoming user queries, this endpoint is registered as a webhook in Slack. To secure this interaction, we implemented authentication and verification of all incoming requests following [Slack’s guidelines](https://api.slack.com/authentication/verifying-requests-from-slack). Recognizing that every Slack-based agent would require this, we built a reusable module that can be quickly configured for each new Slack app.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-24.png)Slack Authentication module
**Acknowledging User Queries**
We observed that when users didn’t see a reply within 2–3 minutes, they assumed the agent had stalled. This caused unnecessary frustration. To improve the experience, we built a component that acknowledges queries immediately, letting users know their request is being processed. This reassurance became a pattern we could reuse across multiple agents.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-22-1024x797.png)User ‘ack’
**Responding Back to Users**
At the end of an agentic loop, the system must respond to users, whether in a channel, group, or a direct message. We created a plug‑and‑play module for sending responses back to Slack, which not only improved this agent, but also positioned us to expand into other Slack bot use cases with minimal extra effort.
![](https://blog.postman.com/wp-content/uploads/2025/08/image-23-539x1024.png)
#### 4\. Adoption & Transformation
Adoption spread naturally. Because the agent lived inside Slack, teams didn’t need training – they simply pulled it into their channels and started using it. Over time, daily active usage grew, and teams pushed the agent beyond its original limits. Their feedback drove new iterations and features, making the agent more effective each week.
The pilot was so successful that we soon opened access to the wider product management team. This meant the insights were no longer siloed but were now available across the organization. The agent became a shared resource, helping everyone make faster and more confident decisions.
### What Worked
***Reusable building blocks.**The same parts we used here could be applied to other agents, saving time and effort.
***Structured insights.**Focusing on a clear use case helped us deliver the right experience and the right type of insights for our business.
***Natural adoption.**Because it was built into Slack, people used it without needing onboarding or training.
### What Didn’t
***Hallucination risk.**Early versions sometimes produced answers without sources. We fixed this by requiring citations.
***Over- and under-fetching.**Sometimes the agent pulled too much or too little data. We adjusted the retrieval system to balance results.
### What’s Next
Looking ahead, we’re focusing on three areas:
1.**Deeper integrations**with planning tools, so insights can flow directly into roadmaps and task management.
2.**Collaboration across multiple agents,**for example combining this research agent with our competitive insight and customer insight agents to produce richer results.
3.**Domain-specific improvements,**training the agent to better understand the API ecosystem and our company and product strategies.
### Closing Thoughts
The research agent has already transformed how our teams work. A task that once took a week of manual review now takes just an afternoon. Just as importantly, it showed us a model for the future:**agents as teammates, deeply embedded in our workflows, constantly improving through business context & real-world use.**
If you want to build something similar on our agent platform, start small. Choose one repetitive workflow, connect the right tools, and put it in the hands of real users. Always keep a human in the loop to supervise and refine it. Over time, the benefits will build, and the agent will grow into an indispensable colleague.
A special shout out to [Shyam Bahety](https://www.linkedin.com/in/bahetyshyam/), Postman’s first Forward Deployed Engineer, who partnered closely with Postman’s leaders and the pilot group to prototype, deploy, and evolve this agent.
Tags: [AI Agents](https://blog.postman.com/tag/ai-agents/) [Engineering](https://blog.postman.com/tag/engineering/)
![](https://secure.gravatar.com/avatar/dd5833357e08f39ede0b78e7accdfd8da16e31fcccdff6996c5996d67ca3149e?s=80&d=https%3A%2F%2Fblog.postman.com%2Fwp-content%2Fuploads%2F2021%2F11%2Favatars-05.png&r=g)
Numaan Ashraf
Numaan Ashraf heads Forward Deployed Engineering at Postman, working directly with leading enterprises to solve their toughest API and AI challenges.
[View all posts by Numaan Ashraf →](https://blog.postman.com/author/numaan-ashraf/)

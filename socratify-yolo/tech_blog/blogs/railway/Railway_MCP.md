---
title: "Railway MCP"
author: "Unknown"
url: "https://blog.railway.com/p/railway-mcp-server"
date: "2025-09-15"
---

![Avatar of Mahmoud Abdelwahab](https://s3-us-west-2.amazonaws.com/public.notion-static.com/9d04f63c-b5ae-41a4-88ea-0ddddb953729/me.jpeg)Mahmoud Abdelwahab

Aug 20, 2025

Yes, yes we know it can feel like “Just one more MCP server, bro. I swear this one’s different…” But in all honesty, we think you’ll like what the Railway MCP server can do.

Here’s a quick demo where we one-shot a Next.js app, deploy it, give it a domain, and then spin-up a Postgres database and a ClickHouse database.

Beyond the 0 → 1 experience, the MCP server offers a bunch of tools that coding agents can use to iterate on existing projects:

*`deploy`\- Deploy a service. This tool can be called more than once so coding agents can continuously apply changes.
*`deploy-template`\- Deploy a template from the [Railway Template Library](https://railway.com/deploy). This makes it possible to deploy arbitrarily complex collections of services and databases.
*`create-environment`and`link-environment`for working with environments. Great for ensuring that coding agents are working in an isolated environment
*`list-variables`and`set-variables`for configuring and pulling variables
*`get-logs`\- Retrieve build or deployment logs for a service. Useful for having coding agents debug deployed services.

You can find the complete list of tools as well as detailed setup instructions in the [project’s README on GitHub](https://github.com/railwayapp/railway-mcp-server).

In most cases, using MCP to manage infrastructure doesn’t really make sense. Infrastructure is typically complex, hard to automate, and with most providers you end up paying for resources regardless of your usage.

With Railway you can one-shot your infra and only pay for what you use.

## [Railway as the ideal deployment target for agents](/p/railway-mcp-server#railway-as-the-ideal-deployment-target-for-agents)

Agents need deployment targets that are reliable, scalable, and cost-efficient. Railway checks all of these boxes.

### [Pricing and autoscaling](/p/railway-mcp-server#pricing-and-autoscaling)

If an agent spins up resources that go idle shortly after, you don’t get stuck with a big bill. On Railway you only pay for active compute time and resources you actually use. This makes the platform ideal for for experimentation and fast iteration.

![Railway’s usage-based pricing](/_next/image?url=https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fa63b5cbc-d4d5-4113-9555-0919a5dd0f1f%2F661b12fc-9ada-4e04-95b4-eff31d415095%2FCleanShot_2025-08-20_at_23.10.362x.png%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Content-Sha256%3DUNSIGNED-PAYLOAD%26X-Amz-Credential%3DASIAZI2LB466YOTYDV3G%252F20250915%252Fus-west-2%252Fs3%252Faws4_request%26X-Amz-Date%3D20250915T132241Z%26X-Amz-Expires%3D3600%26X-Amz-Security-Token%3DIQoJb3JpZ2luX2VjEPz%252F%252F%252F%252F%252F%252F%252F%252F%252F%252FwEaCXVzLXdlc3QtMiJHMEUCIQD8Ej1sMm0r%252FrDD78l366XLDDm%252BwVuhZYmcOj5O99gCaAIgG6YhHgubL9tEkZMnveIQUADyBS5Igp5JChaLSYAMZGQq%252FwMIdRAAGgw2Mzc0MjMxODM4MDUiDNfsvyg8v%252FXF7StizCrcA4jLGatCaw%252B0XATChUUkXagjN8xv%252Fcho5FWe%252BrOOqymHfjUbsorCrphjOO2MeBiNnbFVavgUCT%252BWRhN8fixa8RpEnSsIt5VdkTM26R%252FNgcDQsG5pNSX%252FEuCVr9Aq5RiD8VYM8y138oCDdphX6TZXIWtOOwsnVkDB48SACb9fGQmwiy8CqAAFbqIfqIQG%252B2pfks%252FOb5ZxUp8848aHuywh7YANpj419ZYn8RfUi0hzCenDvGmK9dQDopajRY%252FFIB3IIAepEahyYzEZ4DPH6HQbe9ZfWeOu%252B7yXLyFXb04dz7%252BIlb7DXI8D0U%252BvQwxmImmujOKal5l3iekpYS%252B3FEC1MvAbolksvkbJiatH9XCcaUNWdo83wVnuTcVPOElCmZIYIsw1cyRHsgeQIba49z55ClqcU7QjOdsugFFZ%252BuG32f%252FXV9n9f5DvS4rbMpBTAlUrcs4Va2%252BHjnWYLiH4qnC3fJ1sfX25HE%252BsYV8WR4qzPqGEKSEd8UhgYxYzUPh77SAaUUjdkZFrOL13M%252F8YsF9UwOiXGTLhgrfoOKf1U3jKIdN8m4lYohiT0C3a0wzzIwpEa97ayA4M1Stn%252FVy6CQWbC%252FuiTJZVPhWMdcxM%252Bw1ZN%252BWJXgp%252BBpaqheSW987KMJeEoMYGOqUB1VJISOCeSK95lAy66NOoyQMfHIPDsYvRJMbMt0c44jGZzUBJEA78NfdPznvzmTZDZ7vkPRlSuw6q%252Fl%252BPOK%252FgRkzOfHAcDfaQCiI8CSK7x2iyOh4Os3%252B7rq7zKpBEJXpEtlemwIrP1ucF1f5E6%252FNBpZsR1uKRERD03eBp6jVOd0Ady1r2GixOcQGsKHPCU2wVQcv1nQzTycsHr%252Bwt2Xytf%252B6%252Fb%252FFY%26X-Amz-Signature%3Dc991da7599e114e7f9d9519ce63320bbc37a1b16380804c8b0d7d62d2fac6277%26X-Amz-SignedHeaders%3Dhost%26x-amz-checksum-mode%3DENABLED%26x-id%3DGetObject&w=3840&q=75)

Railway’s usage-based pricing

Additionally, all deployed services on Railway support vertical autoscaling out-of-the-box. So you don’t need to pick an instance size and pay a fixed monthly fee that doesn’t take your usage into account.

### [Environments ](/p/railway-mcp-server#environments-)

Railway enables you to spin up isolated environments. This means that coding agents can make changes to deployed resources without affecting resources in other environments. You can run multiple agents in parallel and give each one their own environment.

![Environments on Railway](/_next/image?url=https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fa63b5cbc-d4d5-4113-9555-0919a5dd0f1f%2F24a43d0e-fe65-4826-80e4-aad5d66a3611%2FCleanShot_2025-08-20_at_23.25.242x.png%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Content-Sha256%3DUNSIGNED-PAYLOAD%26X-Amz-Credential%3DASIAZI2LB466YOTYDV3G%252F20250915%252Fus-west-2%252Fs3%252Faws4_request%26X-Amz-Date%3D20250915T132241Z%26X-Amz-Expires%3D3600%26X-Amz-Security-Token%3DIQoJb3JpZ2luX2VjEPz%252F%252F%252F%252F%252F%252F%252F%252F%252F%252FwEaCXVzLXdlc3QtMiJHMEUCIQD8Ej1sMm0r%252FrDD78l366XLDDm%252BwVuhZYmcOj5O99gCaAIgG6YhHgubL9tEkZMnveIQUADyBS5Igp5JChaLSYAMZGQq%252FwMIdRAAGgw2Mzc0MjMxODM4MDUiDNfsvyg8v%252FXF7StizCrcA4jLGatCaw%252B0XATChUUkXagjN8xv%252Fcho5FWe%252BrOOqymHfjUbsorCrphjOO2MeBiNnbFVavgUCT%252BWRhN8fixa8RpEnSsIt5VdkTM26R%252FNgcDQsG5pNSX%252FEuCVr9Aq5RiD8VYM8y138oCDdphX6TZXIWtOOwsnVkDB48SACb9fGQmwiy8CqAAFbqIfqIQG%252B2pfks%252FOb5ZxUp8848aHuywh7YANpj419ZYn8RfUi0hzCenDvGmK9dQDopajRY%252FFIB3IIAepEahyYzEZ4DPH6HQbe9ZfWeOu%252B7yXLyFXb04dz7%252BIlb7DXI8D0U%252BvQwxmImmujOKal5l3iekpYS%252B3FEC1MvAbolksvkbJiatH9XCcaUNWdo83wVnuTcVPOElCmZIYIsw1cyRHsgeQIba49z55ClqcU7QjOdsugFFZ%252BuG32f%252FXV9n9f5DvS4rbMpBTAlUrcs4Va2%252BHjnWYLiH4qnC3fJ1sfX25HE%252BsYV8WR4qzPqGEKSEd8UhgYxYzUPh77SAaUUjdkZFrOL13M%252F8YsF9UwOiXGTLhgrfoOKf1U3jKIdN8m4lYohiT0C3a0wzzIwpEa97ayA4M1Stn%252FVy6CQWbC%252FuiTJZVPhWMdcxM%252Bw1ZN%252BWJXgp%252BBpaqheSW987KMJeEoMYGOqUB1VJISOCeSK95lAy66NOoyQMfHIPDsYvRJMbMt0c44jGZzUBJEA78NfdPznvzmTZDZ7vkPRlSuw6q%252Fl%252BPOK%252FgRkzOfHAcDfaQCiI8CSK7x2iyOh4Os3%252B7rq7zKpBEJXpEtlemwIrP1ucF1f5E6%252FNBpZsR1uKRERD03eBp6jVOd0Ady1r2GixOcQGsKHPCU2wVQcv1nQzTycsHr%252Bwt2Xytf%252B6%252Fb%252FFY%26X-Amz-Signature%3D75d954a4ce16d5dbf936639218f740f5b7a1c8cf4dae47501125d236692a5d12%26X-Amz-SignedHeaders%3Dhost%26x-amz-checksum-mode%3DENABLED%26x-id%3DGetObject&w=3840&q=75)

Environments on Railway

## [Bonus: Design decisions we made](/p/railway-mcp-server#bonus-design-decisions-we-made)

We made a few design decisions along the way when building the Railway MCP Server. None of them are set in stone, but we thought it would be useful to share our reasoning and the trade-offs that led us here.

### [No destructive actions](/p/railway-mcp-server#no-destructive-actions)

This one is the most obvious one. If there are no`delete-x`MCP tools, the odds of the coding agent running a destructive action goes down significantly. This way, you avoid running into this situation.

![Coding agent deciding to nuke a database](/_next/image?url=https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Fa63b5cbc-d4d5-4113-9555-0919a5dd0f1f%2F00de1e19-b09a-4dc1-80b4-181baa264c2d%2Fimage.png%3FX-Amz-Algorithm%3DAWS4-HMAC-SHA256%26X-Amz-Content-Sha256%3DUNSIGNED-PAYLOAD%26X-Amz-Credential%3DASIAZI2LB466YOTYDV3G%252F20250915%252Fus-west-2%252Fs3%252Faws4_request%26X-Amz-Date%3D20250915T132241Z%26X-Amz-Expires%3D3600%26X-Amz-Security-Token%3DIQoJb3JpZ2luX2VjEPz%252F%252F%252F%252F%252F%252F%252F%252F%252F%252FwEaCXVzLXdlc3QtMiJHMEUCIQD8Ej1sMm0r%252FrDD78l366XLDDm%252BwVuhZYmcOj5O99gCaAIgG6YhHgubL9tEkZMnveIQUADyBS5Igp5JChaLSYAMZGQq%252FwMIdRAAGgw2Mzc0MjMxODM4MDUiDNfsvyg8v%252FXF7StizCrcA4jLGatCaw%252B0XATChUUkXagjN8xv%252Fcho5FWe%252BrOOqymHfjUbsorCrphjOO2MeBiNnbFVavgUCT%252BWRhN8fixa8RpEnSsIt5VdkTM26R%252FNgcDQsG5pNSX%252FEuCVr9Aq5RiD8VYM8y138oCDdphX6TZXIWtOOwsnVkDB48SACb9fGQmwiy8CqAAFbqIfqIQG%252B2pfks%252FOb5ZxUp8848aHuywh7YANpj419ZYn8RfUi0hzCenDvGmK9dQDopajRY%252FFIB3IIAepEahyYzEZ4DPH6HQbe9ZfWeOu%252B7yXLyFXb04dz7%252BIlb7DXI8D0U%252BvQwxmImmujOKal5l3iekpYS%252B3FEC1MvAbolksvkbJiatH9XCcaUNWdo83wVnuTcVPOElCmZIYIsw1cyRHsgeQIba49z55ClqcU7QjOdsugFFZ%252BuG32f%252FXV9n9f5DvS4rbMpBTAlUrcs4Va2%252BHjnWYLiH4qnC3fJ1sfX25HE%252BsYV8WR4qzPqGEKSEd8UhgYxYzUPh77SAaUUjdkZFrOL13M%252F8YsF9UwOiXGTLhgrfoOKf1U3jKIdN8m4lYohiT0C3a0wzzIwpEa97ayA4M1Stn%252FVy6CQWbC%252FuiTJZVPhWMdcxM%252Bw1ZN%252BWJXgp%252BBpaqheSW987KMJeEoMYGOqUB1VJISOCeSK95lAy66NOoyQMfHIPDsYvRJMbMt0c44jGZzUBJEA78NfdPznvzmTZDZ7vkPRlSuw6q%252Fl%252BPOK%252FgRkzOfHAcDfaQCiI8CSK7x2iyOh4Os3%252B7rq7zKpBEJXpEtlemwIrP1ucF1f5E6%252FNBpZsR1uKRERD03eBp6jVOd0Ady1r2GixOcQGsKHPCU2wVQcv1nQzTycsHr%252Bwt2Xytf%252B6%252Fb%252FFY%26X-Amz-Signature%3D9ad7b692ee08bc0e72a8236422bdcbc373e74cb90d05164123527c1ae0dffad9%26X-Amz-SignedHeaders%3Dhost%26x-amz-checksum-mode%3DENABLED%26x-id%3DGetObject&w=3840&q=75)

Coding agent deciding to nuke a database

However, coding agents can still run arbitrary CLI commands, so you should be careful.

### [Local MCP](/p/railway-mcp-server#local-mcp)

MCP has a transport layer responsible for how clients and servers talk to each other and how authentication is handled. It takes care of setting up connections, framing messages, and making sure communication between MCP participants is secure.

MCP currently supports two types of transport:

* Stdio transport: This uses standard input and output streams for communication between local processes on the same machine. It’s the fastest option since there’s no network overhead, which makes it ideal when everything is running locally.
* Streamable HTTP transport: This uses HTTP POST for sending messages from client to server, with optional Server-Sent Events for streaming responses. It’s what enables remote servers to work and supports common HTTP authentication methods like bearer tokens, API keys, and custom headers. MCP recommends OAuth as the way to obtain these tokens.

Remote MCP servers make a lot of sense in the broader vision of MCP. In that world, any AI tool could act as a host, connect to multiple remote MCP servers, and pick the right tool for the job.

For Railway, though, most of our users are developers working inside editors like VS Code, Cursor, or Claude Code. In that context, a remote MCP server doesn’t bring much benefit.

Another limitation is authentication. Since Railway doesn’t yet support OAuth, the only way to connect to a remote MCP server would be to hardcode API tokens. That means going to the Railway dashboard, generating an API key in your account settings, and then manually adding it to your MCP config file. Not exactly a great experience.

We also haven’t come across a real use case where an MCP host only works with remote servers, nor have users asked us to integrate Railway that way. So instead, we went with a local MCP server. The Railway CLI already offers a seamless authentication flow, so setup is as simple as:

1. [Install the CLI](https://docs.railway.com/guides/cli)
2. Run`railway login`
3. [Install the MCP server](https://github.com/railwayapp/railway-mcp-server)[ ](https://github.com/railwayapp/railway-mcp-server)

There’s also a nice side effect of using the CLI as a dependency. If something breaks or the agent hits an edge case, it can fall back to the same workflows a developer would use manually. Rather than getting stuck, it just calls the CLI, which makes the system more resilient and avoids frustrating dead ends.

### [Using the Railway CLI under the hood](/p/railway-mcp-server#using-the-railway-cli-under-the-hood)

Under the hood, the MCP server runs CLI commands. This approach helped us spot gaps in the experience of integrating with the CLI programmatically, which gives us valuable feedback for improving it.

    import { exec } from "node:child_process";
    import { promisify } from "node:util";
    import { analyzeRailwayError } from "./error-handling";
    
    const execAsync = promisify(exec);
    
    export const runRailwayCommand = async (command: string, cwd?: string) => {
    	const { stdout, stderr } = await execAsync(command, { cwd });
    	return { stdout, stderr, output: stdout + stderr };
    };
    
    export const checkRailwayCliStatus = async (): Promise<void> => {
    	try {
    		await runRailwayCommand("railway --version");
    		await runRailwayCommand("railway whoami");
    	} catch (error: unknown) {
    		return analyzeRailwayError(error, "railway whoami");
    	}
    };

## [Conclusion](/p/railway-mcp-server#conclusion)

We’d love to hear how you’re using the Railway MCP server and what improvements you’d like to see. Share your feedback with us [on Central Station](https://station.railway.com/feedback/model-context-protocol-for-railway-railw-c040b796) and help us shape future versions. And if you’re building an agent platform and want to use Railway to power the underlying infrastructure, [we’d love to chat](https://railway.com/pricing#enterprise-calendar-embed).

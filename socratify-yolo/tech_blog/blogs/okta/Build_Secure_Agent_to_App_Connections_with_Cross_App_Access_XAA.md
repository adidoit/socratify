---
title: "Build Secure Agent-to-App Connections with Cross App Access (XAA)"
company: "okta"
url: "https://developer.okta.com/blog/2025/09/03/cross-app-access"
focus_area: "identity systems, authentication, security architecture"
system_score: 85
content_length: 24158
type: "comprehensive_systems_collection"
date: "2025-09-15"
---

  * [agentic-ai](/blog/tags/agentic-ai)
  * [cross-app-access](/blog/tags/cross-app-access)
  * [enterprise-ai](/blog/tags/enterprise-ai)
  * [mcp](/blog/tags/mcp)
  * [oauth](/blog/tags/oauth)
  * [sso](/blog/tags/sso)
  * [xaa](/blog/tags/xaa)



#  Build Secure Agent-to-App Connections with Cross App Access (XAA)

[![avatar-sohail-pathan.jpeg](/assets-jekyll/avatar-sohail-pathan-fa148e78133752dcc86034268bffe3367e2708874b1ea957b09712e8937b8cc7.jpg)](/blog/authors/sohail-pathan/) [Sohail Pathan](/blog/authors/sohail-pathan/)

September 3, 2025

9 MIN READ 

[__](https://twitter.com/intent/tweet?text=Build Secure Agent-to-App Connections with Cross App Access \(XAA\) by @oktadev &url=https://developer.okta.com/blog/2025/09/03/cross-app-access "Share on Twitter")[__](https://www.linkedin.com/shareArticle?mini=true&url=https://developer.okta.com/blog/2025/09/03/cross-app-access "Share on Linkedin")

![Build Secure Agent-to-App Connections with Cross App Access \(XAA\)](/assets-jekyll/blog/cross-app-access/social-a5f372110365d57a5d63d8a747991bedef75479eb05b2c35447db1867915f52d.jpg)

Secure access with enterprise IT oversight between independent applications that communicate with each other is a recognized gap in [OAuth 2.0](https://developer.okta.com/docs/concepts/oauth-openid/). Enterprises can’t effectively regulate cross-app communication, as OAuth 2.0 consent screens rely on users granting access to their individual accounts. Now, with the advent of AI agents that communicate across systems, the need to solve the gap is even greater – especially given the growing importance of enterprise AI security in protecting sensitive data flows.

## What is Cross App Access (XAA)?

Cross App Access (XAA) is a new protocol that lets integrators enable secure agent-to-app and app-to-app access. Instead of scattered integrations and repeated logins, enterprise IT admins gain centralized control: they can decide what connects, enforce security policies, and see exactly what’s being accessed. This unlocks seamless, scalable integrations across apps — whether it’s just two like Google Calendar and Zoom, or hundreds across the enterprise. Read more about Cross App Access in this post:

[ Integrate Your Enterprise AI Tools with Cross-App Access ](/blog/2025/06/23/enterprise-ai)

Manage user and non-human identities, including AI in the enterprise with Cross App Access

[ ![avatar-avatar-semona-igama.jpeg](/assets-jekyll/avatar-semona-igama-03eb4c28aca3765f862b574e032d32f6f8186d04ae9f0db75bed9c74f48a9a3f.jpg) ](/blog/authors/semona-igama/) [Semona Igama](/blog/authors/semona-igama/)

Or watch the video about Cross App Access:

In this post, we’ll go hands-on with Cross App Access. Using **Todo0** (the Resource App) and **Agent0** (the Requesting App) as our sample applications, and **Okta as the enterprise Identity Provider (IdP)** , we’ll show you how to set up trust, exchange tokens, and enable secure API calls between apps that enable enterprise IT oversight. By the end, you’ll not only understand how the protocol works but also have a working example you can adapt to your own integrations.

If you’d rather watch a video of the setup and how XAA works, check this one out.

## Prerequisites to set up the AI agent to app connections using Cross App Access (XAA)

To set up secure agent-to-app connections with Cross App Access (XAA), you’ll need the following:

  1. **Okta Developer Account (Integrator Free Plan):** You’ll need an Okta Developer Account with the Integrator Free Plan. This account will act as your Identity Provider (IdP) for setting up Cross App Access. 
     * If you don’t already have an account, sign up for a new one here: [Okta Integrator Free Plan](https://developer.okta.com/signup)
     * Once created, sign in to your new org
  2. **AWS Credentials:** You’ll need an **AWS Access Key ID** and **AWS Secret Access Key**
     * The IAM user or role associated with these credentials must have access to **Amazon Bedrock,** specifically the **Claude 3.7 Sonnet model,** enabled
     * If you don’t know how to obtain the credentials, [follow this guide](https://github.com/oktadev/okta-cross-app-access-mcp/blob/main/guide/aws-bedrock.md)
  3. **Developer Tools:** These tools are essential for cloning, editing, building, and running your demo applications 
     * **[Git](https://git-scm.com/downloads)** – to clone and manage the repository
     * **[VS Code](https://code.visualstudio.com/Download)** – for reading and modifying the sample source code
     * **[Dev Containers Extension (VS Code)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)** – recommended, as it automatically configures dependencies and environments when you open the project
     * **[Docker](https://www.docker.com/products/docker-desktop/)** – required by the Dev Container to build and run the sample applications in isolated environments



**Table of Contents**

  * What is Cross App Access (XAA)?
  * Prerequisites to set up the AI agent to app connections using Cross App Access (XAA)
  * Use Okta to secure AI applications with OAuth 2.0 and OpenID Connect (OIDC)
    * Enable Cross App Access in your Okta org
    * Create the resource app (Todo0)
    * Create the requesting app (Agent0)
    * Establishing connections between Todo0 & AI agent (Agent0)
  * Set up a test user in Okta org
    * Create the test user
    * Assign the Okta applications to the test user
  * Configure the Node.js Cross App Access project
    * The Cross App Access MCP project at a glance
  * Configure OAuth 2.0 and AI foundation models environment files
    * Generate OIDC configuration and access token files
    * Configure AI and resource application connection values
    * Register OAuth 2.0 redirect URIs for both apps
  * Initialize the database and run the project
    * Bootstrap the project
    * Run and access the apps in your browser
  * Testing the XAA flow: From Bob to Agent0 to Todo0
    * Interact with Todo0, the XAA resource app, by creating tasks
    * Let the AI agent, the requesting app, access your todos
  * Behind the scenes: the OAuth 2.0 Identity Assertion Authorization Grant
  * Need help setting up secure cross-domain enterprise AI application access?
  * Learn more about Cross App Access, OAuth 2.0, and securing your applications



## Use Okta to secure AI applications with OAuth 2.0 and OpenID Connect (OIDC)

Before we dive into the code, we need to register our apps with Okta. In this demo:

  * **Agent0** : the AI agent **requesting app** (makes the API call on behalf of the user)
  * **Todo0** : the **resource app** (owns the protected API)
  * **Managed connection** : the trust relationship between the two apps, created in Okta



We’ll create both apps in your Okta Integrator Free Plan account, grab their client credentials, and then connect them.

### Enable Cross App Access in your Okta org

> ⚠️ **Note:** Cross App Access is currently a **self-service Early Access (EA) feature**. It must be enabled through the Admin Console before the apps appear in the catalog. If you don’t see the option right away, refresh and confirm you have the necessary admin permissions. Learn more in the [Okta documentation on managing EA and beta features](https://help.okta.com/oie/en-us/content/topics/security/manage-ea-and-beta-features.htm).

  1. Sign in to your Okta Integrator Free plan account
  2. In the **Okta Admin Console** , select **Settings > Features**
  3. Navigate to **Early access**
  4. Find **Cross App Access** and select **Turn on** (enable the toggle)
  5. Refresh the Admin Console



![Enable Cross App Access feature in Okta Admin Console](/assets-jekyll/blog/cross-app-access/image9-bc8230f0c6093ded10d2a9f8fe8b944cca4483cecbb6c8385456c53641e09d13.jpg)

### Create the resource app (Todo0)

  1. In the Okta Admin console, navigate to **Applications > Applications**
  2. Select **Browse App Catalog**
  3. Search for **Todo0 - Cross App Access (XAA) Sample Resource App** , and select it
  4. Select **Add Integration**
  5. Enter “Todo0” in the Application label field and click **Done**
  6. Click the **Sign On** tab to view the **Client ID** and **Client secret**. These are required to include in your `.env.todo`



![View Client ID and Client Secret for Todo0 Resource App in Okta Admin Console](/assets-jekyll/blog/cross-app-access/image1-e99c8be2ee71bc48f0e601857b33cc1e6b1e48016ce3ecf9fbb3f39836ca51cf.jpg)

### Create the requesting app (Agent0)

  1. Go back to **Applications > Applications**
  2. Select **Browse App Catalog**
  3. Search for **Agent0 - Cross App Access (XAA) Sample Requesting App** , and select it
  4. Select **Add Integration**
  5. Enter **Agent0** in the Application label field and click **Done**
  6. Click the **Sign On** tab to view the **Client ID** and **Client secret**. These are required to be included in your `.env.agent`



![View Client ID and Client Secret for Agent0 Requesting App in Okta Admin Console](/assets-jekyll/blog/cross-app-access/image10-ca87575c16cdfb1f3a5797b26abe26e5a48848d80da76d59d0736cf89f9515f4.jpg)

### Establishing connections between Todo0 & AI agent (Agent0)

  1. From the **Applications** page, select the **Agent0** app
  2. Go to the **Manage Connections** tab
  3. Under **App granted consent** , select **Add requesting apps** , select **Todo0** , then **Save**
  4. Under **Apps providing consent** , select **Add resource apps** , select **Todo0** , then **Save**



![Connect Agent0 and Todo0 apps in Okta by managing connections](/assets-jekyll/blog/cross-app-access/image8-444990197b52457129ebd56a69bbf10c766de96438907cf34f10a1ef7533ee68.jpg)

Now **Agent0** and **Todo0** are connected. If you check the **Manage Connection** tab for either app, you’ll see that the connection has been established.

## Set up a test user in Okta org

Now that the apps are in place, we need a test user who will sign in and trigger the Cross App Access flow.

### Create the test user

  1. In the **Okta Admin Console** , go to **Directory > People**
  2. Select **Add Person**
  3. Fill in the details: 
     * **First name:** Bob
     * **Last name:** Tables
     * **Username / Email:** `bob@tables.fake`
  4. Under **Activations** , select **Activate now** , mark **☑️ I will set password,** and create a temporary password
  5. Optional: You can mark **☑️ User must change password on first login**
  6. Select **Save** (If you don’t see the new user right away, refresh the page)



![Create a test user Bob Tables in Okta Admin Console](/assets-jekyll/blog/cross-app-access/image11-5374cb4e267b8a45e593d9e521c82a56b98340f1a67bd0cfe1c57069cc83bded.jpg)

### Assign the Okta applications to the test user

  1. Open the **Bob Tables** user profile
  2. Select **Assign Applications**
  3. Assign both **Agent0** (requesting app) and **Todo0** (resource app) to Bob



![Assign Agent0 and Todo0 applications to Bob Tables user in Okta](/assets-jekyll/blog/cross-app-access/image5-b00f06b5223c22635d872affa93e3ff23a0ace3649fc36dd638c373cb7164a5f.jpg)

This ensures Bob can sign in to Agent0, and Agent0 can securely request access to Todo0 on his behalf.

> **⚠️ Note:** Bob will be the identity we use throughout this guide to demonstrate how Agent0 accesses Todo0’s API through Cross App Access.

## Configure the Node.js Cross App Access project

With your Okta environment (apps and user) ready, let’s set up the local project. Before we dive into configs, here’s a quick look at what you’ll be working with.

  1. Clone the repository:
         
         git clone https://github.com/oktadev/okta-cross-app-access-mcp
         

  2. Change into the project directory:
         
         cd okta-cross-app-access-mcp
         

  3. Open **VS Code Command Palette** and run **“Dev Containers: Open Folder in Container”**  
To open Command Palette, select View > Command Palette…, MacOS keyboard shortcut `Cmd+Shift+P`, or Windows keyboard shortcut `Ctrl+Shift+P`




> ⚠️ Note: This sets up all dependencies, including Node, Redis, Prisma ORM, and Yarn.

![Open project in VS Code Dev Container for local development](/assets-jekyll/blog/cross-app-access/image7-2645b7db682744a8bc808c7e865ca3078aad6e75e77d62505942c93e87b0626e.jpg)

### The Cross App Access MCP project at a glance
    
    
    okta-cross-app-access-mcp/
    ├─ packages/
    │  ├─ agent0/               # Requesting app (UI + service) – runs on :3000
    │  │  └─ .env               # Agent0 env (AWS creds)
    │  ├─ todo0/                # Resource app (API/UI) – runs on :3001
    │  ├─ authorization-server/ # Local auth server for ID-JAG + token exchange
    │  │  └─ .env.agent         # IdP creds (Agent0 side)
    │  │  └─ .env.todo          # IdP creds (Todo0 side)
    │  ├─ id-assert-authz-grant-client/ # Implements Identity Assertion Authorization Grant client logic
    ├─ .devcontainer/           # VS Code Dev Containers setup
    ├─ guide/                   # Docs used by the README
    ├─ images/                  # Diagrams/screens used in README
    ├─ scripts/                 # Helper scripts
    ├─ package.json             
    └─ tsconfig.json
    

## Configure OAuth 2.0 and AI foundation models environment files

At this point, you have:

  * **Client IDs and Client Secrets** for both **Agent0** and **Todo0** (from the Okta Admin Console)
  * Your **Okta org URL** , visible in the Okta Admin Console profile menu of the Admin Console. It usually looks like
        
        https://integrator-123456.okta.com
        




This URL will be your **IdP issuer URL** and is shared across both apps.

### Generate OIDC configuration and access token files

From the project root, run:
    
    
    yarn setup:env
    

This scaffolds the following files:

  * `packages/authorization-server/.env.todo`
  * `packages/authorization-server/.env.agent`
  * `packages/agent0/.env`



### Configure AI and resource application connection values

Open each file and update the placeholder with your org-specific values:

**`authorization-server/.env.todo`**
    
    
    CUSTOMER1_EMAIL_DOMAIN=tables.fake
    CUSTOMER1_AUTH_ISSUER=<Your integrator account URL>
    CUSTOMER1_CLIENT_ID=<Todo0 client id>
    CUSTOMER1_CLIENT_SECRET=<Todo0 client secret>
    

**`authorization-server/.env.agent`**
    
    
    CUSTOMER1_EMAIL_DOMAIN=tables.fake
    CUSTOMER1_AUTH_ISSUER=<Your integrator account URL>
    CUSTOMER1_CLIENT_ID=<Agent0 client id>
    CUSTOMER1_CLIENT_SECRET=<Agent0 client secret>
    

**`agent0/.env`**
    
    
    AWS_ACCESS_KEY_ID=<your AWS access key id>
    AWS_SECRET_ACCESS_KEY=<your AWS secret access key>
    

> **⚠️ Note:**
> 
>   1. The **issuer URL** (`CUSTOMER1_AUTH_ISSUER`) is the same in both `.env.todo` and `.env.agent`
>   2. The **Client ID/Client secret** values differ because they come from the respective apps you created
>   3. AWS credentials are required only for Agent0 (requesting app)
> 


### Register OAuth 2.0 redirect URIs for both apps

Finally, we need to tell Okta where to send the authentication response for each app.

**For Agent0:**

  1. From your Okta Admin Console, navigate to **Applications > Applications**
  2. Open the **Agent0** app
  3. Navigate to the **Sign On** tab
  4. In the **Settings** section, select **Edit**
  5. In the **Redirect URIs** field, add
         
         http://localhost:5000/openid/callback/customer1
         

  6. Select **Save**



**Repeat the same steps for Todo0:**

  1. Open the **Todo0** app
  2. Go to the **Sign On** tab > **Settings** > **Edit**
  3. In the **Redirect URIs** field, add:
         
         http://localhost:5001/openid/callback/customer1
         

  4. Select **Save**



Now both apps know where to redirect after authentication.

## Initialize the database and run the project

With the apps and environment configuration in place, the next step is to prepare the local project, set up its databases, and bring both applications online.

### Bootstrap the project

From the root of the repo, install all workspaces and initialize the databases:
    
    
    yarn bootstrap
    

Since this is your first run, you’ll be asked whether to reset the database. Type “`y`” for both Todo0 and Agent0.

### Run and access the apps in your browser

Once the bootstrap is complete, start both apps (and their authorization servers) with:
    
    
    yarn start
    

Open the following ports in your Chrome browser’s tab:

  * **Todo0 (Resource App):** <http://localhost:3001>
  * **Agent0 (Requesting App):** <http://localhost:3000>



At this point, both apps should be live and connected through Okta. 🎉

## Testing the XAA flow: From Bob to Agent0 to Todo0

With everything configured, it’s time to see Cross App Access in action.

### Interact with Todo0, the XAA resource app, by creating tasks

  1. In the **Work Email** field, enter: `bob@tables.fake`, and select **Continue** ![Sign in to Todo0 app using Bob Tables test user](/assets-jekyll/blog/cross-app-access/image14-14521e0b01eb54416020503ed93799659eb21b6577336a8bc0d10b980e9fc2d3.jpg)
  2. You’ll be redirected to the Okta Login page. Sign in with the test user credentials: 
     * **Username:** `bob@tables.fake`
     * **Password:** the temporary password you created earlier
  3. The first time you sign in, you’ll be prompted to: 
     * Set a new password
     * Enroll in [**Okta Verify**](https://help.okta.com/en-us/content/topics/mobile/okta-verify-overview.htm) for MFA
  4. Once logged in, add several tasks to your to-do list
  5. Select one of the tasks and mark it as complete to verify that the application updates the status accurately ![Add and complete tasks in Todo0 Resource App UI](/assets-jekyll/blog/cross-app-access/image6-bc553ff1855f351e73198ac55ecb705586b8c50d09c6cb6a49abae05ca7642c8.jpg)



### Let the AI agent, the requesting app, access your todos

  1. Open the **Agent0** app in your browser ![Initialize AWS Bedrock client in Agent0 Requesting App](/assets-jekyll/blog/cross-app-access/image2-eb865f6baa2038754a58b41228def41948ee5a550bc321e2398f4b1c438c5b33.jpg)
  2. Select **Initialize** to set up the AWS Bedrock client. Once connected, you’ll see the following message:  
`✅ Successfully connected to AWS Bedrock! You can now start chatting.`
  3. Select the **Connect to IdP** button 
     * Behind the scenes, Agent0 requests an identity assertion from Okta and exchanges it for an access token to Todo0
     * If everything is configured correctly, you’ll see the following message  
`Authentication completed successfully! Welcome back.` ![Authenticate Agent0 app with Okta and receive tokens](/assets-jekyll/blog/cross-app-access/image13-6eeb86b30b7a7ce38a79831695d352b7988523734fe31a7d3afb91e82e67f11b.jpg)
  4. To confirm that **Agent0** is actually receiving tokens from Okta: 
     * Open a new browser tab and navigate to: `http://localhost:3000/api/tokens`
     * You should see a JSON payload containing: **`accessToken`, `jagToken`, and `idToken`** This verifies that Agent0 successfully authenticated through Okta and obtained the tokens needed to call Todo0 ![JSON payload containing tokens](/assets-jekyll/blog/cross-app-access/image15-9c618cdaac2d601c6d020bf9917717e8f9bce978207636d4253516fb72f0e7f6.jpg)
  5. Now interact with Agent0 using natural prompts. For example: write this prompt 
         
         What's on my plate in my to-do list?
         

> **⚠️ Note:** Agent0 will call the Todo0 API using the access token and return your pending tasks ![Agent0 app displays pending tasks from Todo0 using Cross App Access](/assets-jekyll/blog/cross-app-access/image17-ebdbc77bbb3783055a42564c16011b781fb61b3ba5f245d06a5ccda187588fe4.jpg)

  6. Let’s try some more prompts 
     * Ask Agent0 to **add a new task**
     * Ask it to **mark an existing task complete**
     * Refresh the Todo0 app — you’ll see the changes reflected instantly ![Add and complete tasks in Todo0 Resource App UI](/assets-jekyll/blog/cross-app-access/image4-80f25a80b7b1bd475e9d9fedf38b12a3ec64a8abe6ccdbd57b92181b6dcae404.jpg)



## Behind the scenes: the OAuth 2.0 Identity Assertion Authorization Grant

**✅ Bob Tables** logs in once with Okta  
⏩ **Agent0 (requesting app)** gets an identity assertion from Okta  
🔄 Okta vouches for Bob and exchanges that assertion for an access token  
👋 **Agent0** uses that token to securely call the **Todo0 (resource app)** API

![Illustration showing secure agent-to-app connections using Okta Cross App Access](/assets-jekyll/blog/cross-app-access/mermaid-b6c393ffac9ab72f0fca41845c12b1463391dd381f44aa4e6dff3a75366e210f.svg)

**🎉 Congratulations! You’ve successfully configured and run the Cross App Access project.**

## Need help setting up secure cross-domain enterprise AI application access?

If you run into any issues while setting up or testing this project, feel free to post your queries to the forum: 👉 [Okta Developer Forum](https://devforum.okta.com)

If you’re interested in implementing **Cross App Access (XAA)** in your own application — whether as a **requesting app** or a **resource app** — and want to explore how Okta can support your use case, reach out to us at: 📩 **[xaa@okta.com](mailto:xaa@okta.com)**

## Learn more about Cross App Access, OAuth 2.0, and securing your applications

If this walkthrough helped you understand how Cross App Access works in practice, you might enjoy diving deeper into the standards and conversations shaping it. Here are some resources to continue your journey

  * 📘 [Cross App Access Documentation](https://help.okta.com/oie/en-us/content/topics/apps/apps-cross-app-access.htm) – official guides and admin docs to configure and manage Cross App Access in production
  * 🎙️ [Developer Podcast on MCP and Cross App Access](https://www.youtube.com/watch?v=qKs4k5Y1x_s) – hear the backstory, use cases, and why this matters for developers
  * 📄 [OAuth Identity Assertion Authorization Grant (IETF Draft)](https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/) – the emerging standard that powers this flow



If you’re new to OAuth or want to understand the basics behind secure delegated access, check out these resources:

  * [What the Heck is OAuth?](/blog/2017/06/21/what-the-heck-is-oauth)
  * [What’s the Difference Between OAuth, OpenID Connect, and SAML?](https://www.okta.com/identity-101/whats-the-difference-between-oauth-openid-connect-and-saml/)
  * [Secure Your Express App with OAuth 2.0, OIDC, and PKCE](/blog/2025/07/28/express-oauth-pkce)
  * [Why You Should Migrate to OAuth 2.0 From Static API Tokens](/blog/2023/09/25/oauth-api-tokens)
  * [How to Get Going with the On-Demand SaaS Apps Workshops](/blog/2023/07/27/enterprise-ready-getting-started)



Follow us on [LinkedIn](https://www.linkedin.com/company/oktadev), [Twitter](https://twitter.com/oktadev), and subscribe to our [YouTube](https://www.youtube.com/c/oktadev) channel for more developer content. If you have any questions, please leave a comment below!

[![avatar-sohail-pathan.jpeg](/assets-jekyll/avatar-sohail-pathan-fa148e78133752dcc86034268bffe3367e2708874b1ea957b09712e8937b8cc7.jpg)](/blog/authors/sohail-pathan/) [Sohail Pathan](/blog/authors/sohail-pathan/)

[__](https://github.com/iamspathan "GitHub Profile")[__](https://twitter.com/iamspathan "Twitter Profile")[__](https://www.linkedin.com/in/iamspathan "Linkedin Profile")

Sohail is a Senior Developer Advocate at Okta with roots in mobile app development and hands-on experience designing, building, and publishing APIs. Now, he helps developers secure their apps by turning complex OAuth and API topics into clear, actionable guides. When he's not coding or speaking at conferences, you'll find him on a quest for the perfect plate of biryani.

[ __Previous post](/blog/2025/08/20/ios-mfa "How to Build a Secure iOS App with MFA")

[](/blog/2025/09/03/cross-app-access)

Okta Developer Blog Comment Policy

We welcome relevant and respectful comments. Off-topic comments may be removed.

Please enable JavaScript to view the comments inline. [Visit the forum to comment](https://devforum.okta.com/c/okta-dev-blog/17). 

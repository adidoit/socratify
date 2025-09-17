---
title: "Secure Your Express App with OAuth 2.0, OIDC, and PKCE"
company: "okta"
url: "https://developer.okta.com/blog/2025/07/28/express-oauth-pkce"
focus_area: "identity systems, authentication, security architecture"
system_score: 85
content_length: 30511
type: "comprehensive_systems_collection"
date: "2025-09-15"
---

  * [authentication](/blog/tags/authentication)
  * [express](/blog/tags/express)
  * [javascript](/blog/tags/javascript)
  * [node](/blog/tags/node)
  * [oauth](/blog/tags/oauth)
  * [oidc](/blog/tags/oidc)
  * [pkce](/blog/tags/pkce)



#  Secure Your Express App with OAuth 2.0, OIDC, and PKCE

[![avatar-akanksha-bhasin.jpeg](/assets-jekyll/avatar-akanksha-bhasin-24d4e63bcf2c0d54a7edf954e4a17d096cf0c1fc3b1f42771956ebd37c93a32b.jpg)](/blog/authors/akanksha-bhasin/) [Akanksha Bhasin](/blog/authors/akanksha-bhasin/)

July 28, 2025

9 MIN READ 

[__CODE](https://github.com/oktadev/okta-express-oauth-pkce-example "Sample code on GitHub")

[__](https://twitter.com/intent/tweet?text=Secure Your Express App with OAuth 2.0, OIDC, and PKCE by @oktadev &url=https://developer.okta.com/blog/2025/07/28/express-oauth-pkce "Share on Twitter")[__](https://www.linkedin.com/shareArticle?mini=true&url=https://developer.okta.com/blog/2025/07/28/express-oauth-pkce "Share on Linkedin")

![Secure Your Express App with OAuth 2.0, OIDC, and PKCE](/assets-jekyll/blog/express-oauth-pkce/express-oauth-pkce-social-image-d8ec82313edd624093dd24166878501878079f9404b2fc42db9b9d3185a8348e.jpg)

Every web application needs authentication, but building it yourself is risky and time-consuming. Instead of starting from scratch, you can integrate Okta to manage user identity and pair Passport with the openid-client library in Express to simplify and secure the login flow. In this tutorial, you’ll build a secure, role-based expense dashboard where users can view their expenses tailored to their team.

Check out the complete source code on [GitHub](https://github.com/oktadev/okta-express-oauth-pkce-example) and get started without setting it up from scratch.

**Table of Contents**

  * Why use Okta for authentication
    * Why use PKCE in OAuth 2.0
  * A secure web app using Express, OAuth 2.0, and PKCE
  * Create your Express project and install dependencies
  * Configure environment variables for OIDC authentication
  * Create the Okta OIDC web application
  * Build the Express app
    * Define team mapping and sample expenses
    * Create a file to handle authentication
    * Set up routing in Express
    * Add EJS views in Express
  * Run the Express app with authentication
  * Learn more about OAuth 2.0, OIDC, and PKCE



## Why use Okta for authentication

Building an authentication system and handling credentials, sessions, and tokens is highly insecure and exposes your application to serious vulnerabilities.

Okta provides a secure, scalable, and standards-based solution using OpenID Connect (OIDC) and OAuth 2.0. It also integrates seamlessly with OIDC client libraries for your favorite tech stack and allows you to fetch tokens.

### Why use PKCE in OAuth 2.0

To further strengthen security, this project uses PKCE (Proof Key for Code Exchange), defined in [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636). PKCE is a security extension to the Authorization Code flow. Developers initially designed PKCE for mobile apps, but experts now recommend it for all OAuth clients, including web apps. It helps prevent CSRF and authorization code injection attacks and makes it useful for every type of OAuth client, even confidential clients such as web apps that use client secrets. As OAuth 2.0 has steadily evolved, security best practices have also advanced. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html) captures the consensus on the most effective and secure implementation strategies. Additionally, the upcoming OAuth 2.1 draft requires PKCE for all authorization code flows, reinforcing it as a baseline security standard.

With Okta, you can implement modern authentication features and focus on your application logic without worrying about authentication infrastructure.

## A secure web app using Express, OAuth 2.0, and PKCE

Let’s build an expense dashboard where users log in with Okta and view spending data based on their role. Whether they work in Finance, Marketing, or HR, each team views only its own expenses. To keep things minimal in this demo project, we’ll define roles and users directly in the app.

You’ll also use OpenID Connect (OIDC) through the openid-client library for authentication. Then, you’ll map each user’s email from the ID token to a team. The dashboard applies principles of least privilege and displays expenses by team, so each user sees only their department’s spending.

**Prerequisites**

  * Node.js installed (v22+ recommended)

  * [Okta Integrator Free Plan org](https://developer.okta.com/signup/)




## Create your Express project and install dependencies

Create a new project folder named `express-project-okta`, and open a terminal window in the project folder.

Initialize a new Node.js project:
    
    
    npm init -y
    

Install the required packages:
    
    
    npm install express@5.1 passport@0.7 openid-client@6.6 express-session@1.18 ejs@3.1 express-ejs-layouts@2.5 dotenv
    

Now, install the development dependencies:
    
    
    npm install --save-dev nodemon
    

In the package.json file, update the scripts property with the following:
    
    
      "scripts": {
        "start": "nodemon index.js"
      }
    

**What do these dependencies do?**

These installed packages become your Express project’s dependencies.

  * **`express`** : Handles routing and HTTP middleware for your web app

  * **`passport`** : Sets up and maintains server-side sessions

  * **`openid-client`** : Node.js OIDC library with PKCE support; handles the OAuth handshake and token exchange.

  * **`express-session`** : Manages user sessions on the server

  * **`dotenv`** : Loads environment variables from a `.env` file

  * **`ejs`** : Enables dynamic HTML rendering using embedded JavaScript templates

  * **`express-ejs-layouts`** : Adds layout support to EJS, helping manage common layout structures across views




## Configure environment variables for OIDC authentication

Create a `.env` file in the root directory with placeholders for your Okta configuration.
    
    
    OKTA_ISSUER=https://{yourOktaDomain}
    OKTA_CLIENT_ID={yourClientId}
    OKTA_CLIENT_SECRET={clientSecret}
    APP_BASE_URL=http://localhost:3000
    POST_LOGOUT_URL=http://localhost:3000
    

In the next step, you’ll get these values from your Okta Admin Console.

## Create the Okta OIDC web application

Before you begin, you’ll need an Okta Integrator Free Plan account. To get one, sign up for an [Integrator account](https://developer.okta.com/login). Once you have an account, sign in to your [Integrator account](https://developer.okta.com/login). Next, in the Admin Console:

  1. Go to **Applications** > **Applications**
  2. Click **Create App Integration**
  3. Select **OIDC - OpenID Connect** as the sign-in method
  4. Select **Web Application** as the application type, then click **Next**
  5. Enter an app integration name

  6. Configure the redirect URIs: 
     * **Sign-in redirect URIs** : `http://localhost:3000/authorization-code/callback`
     * **Sign-out redirect URIs** : `http://localhost:3000`
  7. In the **Controlled access** section, select the appropriate access level
  8. Click **Save**

Where are my new app's credentials?

Creating an OIDC Web App manually in the Admin Console configures your Okta Org with the application settings.

After creating the app, you can find the configuration details on the app’s **General** tab:

  * **Client ID** : Found in the **Client Credentials** section
  * **Client Secret** : Click **Show** in the **Client Credentials** section to reveal
  * **Issuer** : Found in the **Issuer URI** field for the authorization server that appears by selecting **Security** > **API** from the navigation pane.



You’ll need these values for your application configuration:
    
    
    OKTA_OAUTH2_ISSUER="https://dev-133337.okta.com/oauth2/default"
    OKTA_OAUTH2_CLIENT_ID="0oab8eb55Kb9jdMIr5d6"
    OKTA_OAUTH2_CLIENT_SECRET="NEVER-SHOW-SECRETS"
    

Your Okta domain is the first part of your issuer, before `/oauth2/default`.

**NOTE** : You can also use the [Okta CLI Client](https://github.com/okta/okta-cli-client) or [Okta PowerShell Module](https://github.com/okta/okta-powershell-cli) to automate this process. See [this guide](https://developer.okta.com/docs/guides/sign-into-web-app/-/create-okta-application/) for more information about setting up your app.

## Build the Express app

Create an `index.js` file in your project root. It serves as the main entry point for your application. Use it to initialize the Express app, set up the routes, and configure [Passport](https://www.passportjs.org/) to manage user sessions by serializing and deserializing users on each request.
    
    
    import express from 'express';
    import session from 'express-session';
    import passport from 'passport'; 
    import routes from './routes.js';
    import expressLayouts from 'express-ejs-layouts';
    
    const app = express();
    
    app.set('view engine', 'ejs');
    app.use(expressLayouts); 
    app.set('layout', 'layout');
    app.use(express.urlencoded({ extended: false }));
    
    app.use(session({
      secret: "your-hardcoded-secret",
      resave: false,
      saveUninitialized: true,
    }));
    
    app.use(passport.initialize());
    app.use(passport.session());
    
    passport.serializeUser(function (user, done) {
      done(null, user);
    });
    
    passport.deserializeUser(function (obj, done) {
      done(null, obj);
    });
    
    app.use('/', routes);
    
    app.listen(3000, () => {
      console.log('Server listening on http://localhost:3000');
    });
    

### Define team mapping and sample expenses

Create a `utils.js` file to serve as a data module for your project. This file includes a user-to-team mapping and has dummy expense data for each team, covering all teams configured for testing in your web app.

The application determines the user’s team context from the email claim in the ID token and filters the expense list accordingly, so the dashboard displays only that team’s data.

To customize the data, open `utils.js` and update the following objects:

  * `ALL_TEAMS_NAME` \- an array listing all teams in your organization

  * `userTeamMap` \- maps each user’s email (or “admin” for full access) to a specific team

  * `dummyExpenseData` \- contains sample expense data for each team



    
    
    export const ALL_TEAMS_NAME = ["finance", "hr", "legal", "marketing", "dev advocacy"];
    
    export const userTeamMap = {
      "hannah.smith@task-vantage.com": "admin",
      "grace.li@task-vantage.com": "legal",
      "frank.wilson+@task-vantage.com": "dev advocacy",
      "carol.lee@task-vantage.com": "finance",
      "alice.johnson@task-vantage.com": "marketing",
      "sarah.morgan@task-vantage.com": "hr",
    };
    
    export const dummyExpenseData = {
      finance: [
        {
          name: "Alice Johnson",
          item: "Product Launch Campaign",
          amount: 1200,
        },
        {
          name: "Bob Smith",
          item: "Promotional Material",
          amount: 450,
        },
        {
          name: "Carol Lee",
          item: "Team Lunch",
          amount: 180,
        },
        {
          name: "David Kim",
          item: "Event Booth",
          amount: 950,
        },
      ],
      hr: [
        {
          name: "Eve Martinez",
          item: "Internet",
          amount: 300,
        },
        {
          name: "Frank Wilson",
          item: "Compliance Training",
          amount: 600,
        },
        {
          name: "Grace Li",
          item: "Conference Travel",
          amount: 1500,
        },
        {
          name: "Henry Zhang",
          item: "Team Offsite",
          amount: 1000,
        },
      ],
      marketing: [
        {
          name: "Alice Johnson",
          item: "Payroll Processing",
          amount: 750,
        },
        {
          name: "Carol Lee",
          item: "Compliance Training",
          amount: 400,
        },
        {
          name: "Eve Martinez",
          item: "Team Lunch",
          amount: 200,
        },
        {
          name: "Frank Wilson",
          item: "Team Offsite",
          amount: 850,
        },
      ],
      legal: [
        {
          name: "Grace Li",
          item: "Event Booth",
          amount: 1100,
        },
        {
          name: "David Kim",
          item: "Product Launch Campaign",
          amount: 1300,
        },
        {
          name: "Bob Smith",
          item: "Conference Travel",
          amount: 1250,
        },
        {
          name: "Henry Zhang",
          item: "Team Lunch",
          amount: 170,
        },
      ],
      "dev-advocacy": [
        {
          name: "Eve Martinez",
          item: "Internet",
          amount: 280,
        },
        {
          name: "Frank Wilson",
          item: "Payroll Processing",
          amount: 720,
        },
        {
          name: "Grace Li",
          item: "Compliance Training",
          amount: 500,
        },
        {
          name: "Alice Johnson",
          item: "Team Offsite",
          amount: 950,
        },
      ],
    };
    
    export function getModifiedTeam(team) {
      if (!team?.trim()) return [];
    
      const toPascalCase = (str) =>
        str
          .trim()
          .split(/\s+/)
          .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ');
    
      const toKebabCase = (str) => str.trim().toLowerCase().split(' ').join('-');
    
      if (team === 'admin') {
        return ALL_TEAMS_NAME.map((element) => ({
          id: toKebabCase(element),
          label: toPascalCase(element),
        }));
      }
    
      return [
        {
          id: toKebabCase(team),
          label: toPascalCase(team),
        },
      ];
    }
    

The file also defines `getModifiedTeam`, a helper that converts a team name into an array of objects. Each object has an id and a label. If the team is admin, the function returns an object for every entry in `ALL_TEAMS_NAME`; otherwise, it returns a single object for the specified team. Later in the project, the app calls this function to transform the user’s team information.

### Create a file to handle authentication

Create an `auth.js` file for this step. This file uses the [openid-client](https://www.npmjs.com/package/openid-client) library to handle the OIDC flow: it logs users in, exchanges the authorization code for tokens, and logs them out. It also defines a middleware that guards protected routes.

In the auth.js file, add the following code:
    
    
    import * as client from "openid-client";
    import "dotenv/config";
    
    import { getModifiedTeam, userTeamMap } from './utils.js';
    
    async function getClientConfig() {
      return await client.discovery(new URL(process.env.OKTA_ISSUER), process.env.OKTA_CLIENT_ID, process.env.OKTA_CLIENT_SECRET);
    }
    
    export async function login(req, res) {
      try {
        const openIdClientConfig = await getClientConfig();
    
        const code_verifier = client.randomPKCECodeVerifier();
        const code_challenge = await client.calculatePKCECodeChallenge(code_verifier);
        const state = client.randomState();
    
        req.session.pkce = { code_verifier, state };
        req.session.save(); 
    
        const authUrl = client.buildAuthorizationUrl(openIdClientConfig, {
          scope: "openid profile email offline_access",
          state,
          code_challenge,
          code_challenge_method: "S256",
          redirect_uri: `${process.env.APP_BASE_URL}/authorization-code/callback`,
        });
    
        res.redirect(authUrl);
      } catch (error) {
        res.status(500).send("Something failed during the authorization request");
      }
    }
    
    function getCallbackUrlWithParams(req) {
      const host = req.headers["x-forwarded-host"] || req.headers.host || "localhost";
      const protocol = req.headers["x-forwarded-proto"] || req.protocol;
      const currentUrl = new URL(`${protocol}://${host}${req.originalUrl}`);
      return currentUrl;
    }
    
    export async function authCallback(req, res, next) {
      try {
        const openIdClientConfig = await getClientConfig();
    
        const { pkce } = req.session;
    
        if (!pkce || !pkce.code_verifier || !pkce.state) {
          throw new Error("Login session expired or invalid. Please try logging in again.");
        }
    
        const tokenSet = await client.authorizationCodeGrant(openIdClientConfig, getCallbackUrlWithParams(req), {
          pkceCodeVerifier: pkce.code_verifier,
          expectedState: pkce.state,
        });
    
        const { name, email } = tokenSet.claims();
        const teams = getModifiedTeam(userTeamMap[email]);
    
        const userProfile = {
          name,
          email,
          teams,
          idToken: tokenSet.id_token,
        };
    
        delete req.session.pkce;
    
        req.logIn(userProfile, (err) => {
          if (err) {
            return next(err);
          }
    
          return res.redirect("/dashboard");
        });
      } catch (error) {
        console.error("Authentication error:", error.message);
        return res.status(500).send(`Authentication failed: ${error.message}`);
      }
    }
    
    export async function logout(req, res) {
      try {
        const openIdClientConfig = await getClientConfig();
    
        const id_token_hint = req.user?.idToken;
    
        const logoutUrl = client.buildEndSessionUrl(openIdClientConfig, {
          id_token_hint,
          post_logout_redirect_uri: process.env.POST_LOGOUT_URL,
        });
    
        req.logout((err) => {
          if (err) return next(err);
    
          req.session.destroy((err) => {
            if (err) return next(err);
            res.redirect(logoutUrl);
          });
        });
      } catch (error) {
        res.status(500).send('Something went wrong during logout.');
      }
    }
    
    export function ensureAuthenticated(req, res, next) {
      if (req.isAuthenticated()) {
        return next();
      }
      res.redirect("/login");
    }
    

This file includes the following functions:

  1. **`getClientConfig`** \- Retrieves the authorization server’s metadata using the discovery endpoint.
  2. **`login`** \- This function starts the Authorization Code + PKCE flow. It generates the required values to enable PKCE: the **code_verifier** and **code_challenge**. These values, along with the `state` value protect the user sign in process from attack vectors. [PKCE](https://datatracker.ietf.org/doc/html/rfc7636) protects against auth code interception attacks, and the state parameter protects against [Cross-Site Request Forgery (CSRF)](https://owasp.org/www-community/attacks/csrf). The openid-client builds the user sign in URL with these values and redirects the user to Okta to complete the authentication challenge.
  3. **`getCallbackUrlWithParams`** \- Reconstructs the complete callback URL, including protocol, host, path, and query.
  4. **`authCallback`** \- This function runs when the user redirects back to the app after the authentication challenge succeeds. At this point, the redirect URL back into the application includes the auth code. The OIDC client verifies the auth code by checking that the **state** value matches the parameter in the first redirect. Once verified, the openid-client library uses the auth code for the token exchange by adding the **code_verifier** to the token request. The authorization server validates the **auth code** and the **code_verifier** value to ensure the request comes from the client making the original authentication request, mitigating attacks using stolen auth codes. Once we get back valid tokens, we handle the app’s business logic, such as mapping the user to a team and storing the profile details and ID token in the session. If everything succeeds, it redirects the user to the dashboard.
  5. **`logout`** \- Logs the user out of the app and redirects to the post-logout URL.
  6. **`ensureAuthenticated`** \- Middleware that allows authenticated users to proceed and redirects others to the login page.



### Set up routing in Express

Now things start to come together and feel like a real app. The `routes.js` file defines all the essential routes, from login and logout to viewing your profile, the expense dashboard, and individual team expense pages. The app handles each endpoint’s core logic and checks a user’s authentication status before granting access to protected pages.

It acts as our app’s traffic controller, directing users to the right pages and ensuring that only logged-in users can view sensitive information like the expense dashboard or group details. This structure keeps our app organized and secure and lays the foundation for a smooth user experience.
    
    
    import express from "express";
    import "dotenv/config";
    
    import { authCallback, ensureAuthenticated, login, logout } from "./auth.js";
    import { dummyExpenseData } from './utils.js';
    
    const router = express.Router();
    
    router.get("/", (req, res) => {
      res.render("home", { title: "Home", user: req.user });
    });
    
    router.get("/login", login);
    
    router.get("/authorization-code/callback", authCallback);
    
    router.get("/profile", ensureAuthenticated, (req, res) => {
      res.render("profile", { title: "Profile", user: req.user });
    });
    
    router.get("/dashboard", ensureAuthenticated, (req, res) => {
      const team = req.user?.teams || [];
    
      res.render("dashboard", {
        title: "Dashboard",
        user: req.user,
        team,
      });
    });
    
    router.get("/team/:id", ensureAuthenticated, (req, res) => {
      const teamId = req.params.id;
      const teamList = req.user?.teams || [];
    
      const team = teamList.find((team) => team.id === teamId);
      if (!team) {
        return res.status(404).send("Team not found");
      }
    
      const expenses = dummyExpenseData[teamId];
      const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    
      res.render("expenses", {
        title: team.name,
        user: req.user,
        team,
        expenses,
        total,
      });
    });
    
    router.get("/logout", logout);
    
    export default router;
    

### Add EJS views in Express

Now it’s time to give the app a user interface. You’ll use EJS templates to build pages that respond dynamically to who’s logged in and what data they see. The app uses `ejs` templates to render the pages, plus `express-ejs-layouts` for common layout structures.

Create a folder named `views`, then add the following EJS files:

**home.ejs**
    
    
    <% if (user) { %>
    <h1>Welcome, <%= user.name || 'User' %>!</h1>
    <% } else { %>
    <h1>Welcome</h1>
    <% } %>
    
    <p class="lead">Log your expenses and manage your team's spending on the dashboard.</p>
    
    <% if (user) { %>
    <a href="/dashboard" class="btn btn-primary">Go to Dashboard</a>
    <% } else { %>
    <a href="/login" class="btn btn-success">Login</a>
    <% } %>
    
    

**profile.ejs**
    
    
    <h1>Profile</h1>
    <p><h2 style="display: inline-block; margin: 0; font-size: 16px;">Name:</h2> <%= user.name %></p>
    <p><h2 style="display: inline-block; margin: 0; font-size: 16px;">Email:</h2> <%= user.email %></p>
    

**layout.ejs**
    
    
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title><%= typeof title !== 'undefined' ? title : 'Expense Dashboard' %></title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
        <style>
        html, body {
            height: 100%;
            margin: 0;
          }
          body {
            display: flex;
            flex-direction: column;
          }
          .content {
            flex: 1;
          }
          .team-heading {
            display: inline-block;
            font-weight: 600;
            color: #2c3e50; 
            margin-bottom: 1rem;
          }
        </style>
      </head>
      <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
          <div class="container">
            <a class="navbar-brand" href="/dashboard">Expense Dashboard</a>
            <div>
              <% if (user) { %>
              <a href="/dashboard" class="btn btn-light btn-sm me-2">Dashboard</a>
              <a href="/profile" class="btn btn-light btn-sm me-2">Profile</a>
              <a href="/logout" class="btn btn-danger btn-sm">Logout</a>
              <% } else { %>
              <a href="/login" class="btn btn-success btn-sm">Login</a>
              <% } %>
            </div>
          </div>
        </nav>
    
      <main class="container content">
        <%- body %>
      </main>
    
      <footer class="text-center mt-5 mb-3 text-muted">
        &copy; Okta Inc. Expense Dashboard
      </footer>
      </body>
    </html>
    

**dashboard.ejs**
    
    
    <h1>Dashboard</h1>
    <p>Welcome, <%= user.name || 'User' %></p>
    <h2 style="font-size: 24px;">Your Teams</h2>
    <% if (team && team.length > 0) { %>
    <ul class="list-group">
      <% team.forEach(team => { %>
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <%= team.label %>
        <a href="/team/<%= team.id %>" class="btn btn-primary btn-sm">View</a>
      </li>
      <% }) %>
    </ul>
    <% } else { %>
    <p>You are not part of any teams yet.</p>
    <% } %>
    

**expenses.ejs**

The EJS template renders the team info and expenses data in a tabular format.
    
    
    <h1><%= team.label %></h1>
    <div>Welcome to the <p class="team-heading"><%= team.label %></p> team page.</div>
    <br/>
    <% if (expenses && expenses.length > 0) { %>
    <h2 style="font-size: 24px;">Expenses</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Name</th>
          <th>Item</th>
          <th>Amount ($)</th>
        </tr>
      </thead>
      <tbody>
          <% expenses.forEach(exp => { %>
        <tr>
          <td><%= exp.name %></td>
          <td><%= exp.item %></td>
          <td><%= exp.amount %></td>
        </tr>
        <% }) %>
      </tbody>
    </table>
    <div class="alert alert-info"><h6 style="display: inline-block; margin: 0;">Total:</h6> $<%= total %></div>
    <% } else { %>
    <p>No expenses found for this team.</p>
    <% } %>
    

## Run the Express app with authentication

In your terminal, start the server:

`npm start`

Open your browser and navigate to <http://localhost:3000>.

Click **Login** and authenticate with your Okta account. The app then displays your Expense Dashboard, Profile, and a Log out option.

> **Note:** When you’re signed in to the Developer Console as an admin, Okta keeps your org session active and automatically logs you into the app. To test other user accounts, use an incognito tab to test the login flow.

#### Admin view:

![Admin View Dashboard](/assets-jekyll/blog/express-oauth-pkce/admin-view-db1a44c11da76fa7bc67012c25d3f76047454533637673d18e4f101b5cc9ad47.jpg)

#### User view:

![User View Dashboard](/assets-jekyll/blog/express-oauth-pkce/user-view-084f25b2245a932ff8f24ce7a3bf6f8629d14d92eba2b5a47bd1712c07da2be4.jpg)

#### Expenses view:

![Expenses View](/assets-jekyll/blog/express-oauth-pkce/expenses-c3774a156edf0903f34922d56ec85f0ac0e0d81543b033e131d64cbc56aae7d7.jpg)

And that’s it! You’ve built a secure Expense Dashboard and connected your Express application to Okta using OIDC and OAuth.

## Learn more about OAuth 2.0, OIDC, and PKCE

Here’s a quick rundown of the features I used in this project to build a secure expense dashboard:

  * **OpenID Connect (OIDC)** is an identity and authentication layer built on OAuth 2.0.

  * **Authorization Code Flow with PKCE** is the most secure flow for server-side and browser-based web apps.




If you’d like to explore the whole project and skip setting it up from scratch, check out the complete source code on [GitHub](https://github.com/oktadev/okta-express-oauth-pkce-example).

To explore further, check out these official Okta resources to learn more about the key concepts.

  * [Authentication vs Authorization](https://www.okta.com/identity-101/authentication-vs-authorization/)

  * [OAuth 2.0 and OpenID Connect overview](https://developer.okta.com/docs/concepts/oauth-openid)

  * [Implement Authorization Code with PKCE](https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main)

  * [Authorization Servers in Okta](https://developer.okta.com/docs/concepts/auth-servers)




Follow us on [LinkedIn](https://www.linkedin.com/company/oktadev), [Twitter](https://twitter.com/oktadev), and subscribe to our [YouTube](https://www.youtube.com/c/oktadev) channel to see more content like this. If you have any questions, please comment below!

[![avatar-akanksha-bhasin.jpeg](/assets-jekyll/avatar-akanksha-bhasin-24d4e63bcf2c0d54a7edf954e4a17d096cf0c1fc3b1f42771956ebd37c93a32b.jpg)](/blog/authors/akanksha-bhasin/) [Akanksha Bhasin](/blog/authors/akanksha-bhasin/)

[__](https://github.com/akankshabhasin "GitHub Profile")[__](https://twitter.com/Akii_20 "Twitter Profile")[__](https://www.linkedin.com/in/akankshabhasin "Linkedin Profile")

Akanksha has a developer background and experience building global developer communities. She has given talks on various technologies, hosted large-scale events and hackathons, advocated for developers, and fostered partnerships and open-source initiatives. Outside work, she loves dancing and traveling; you'll often find her capturing serene skies through her phone.

[ __Previous post](/blog/2025/07/22/react-pwa "Create a React PWA with Social Login Authentication") [Next post __](/blog/2025/07/31/ciba-okta "Introducing CIBA for Secure Transaction Verification")

[](/blog/2025/07/28/express-oauth-pkce)

Okta Developer Blog Comment Policy

We welcome relevant and respectful comments. Off-topic comments may be removed.

Please enable JavaScript to view the comments inline. [Visit the forum to comment](https://devforum.okta.com/c/okta-dev-blog/17). 

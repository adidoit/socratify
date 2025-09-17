---
title: "Deno 2.5: Permissions in the config file"
author: "Unknown"
url: "https://deno.com/blog/v2.5"
date: "2025-09-15"
---

# Deno 2.5: Permissions in the config file

September 10, 2025[](/feed "Atom Feed")

* [![](https://github.com/bartlomieju.png)Bartek Iwa≈Ñczuk](https://github.com/bartlomieju)
* [![](https://github.com/lambtron.png)Andy Jiang](https://github.com/lambtron)

* [Product Update](/blog?tag=product-update)

To upgrade to Deno 2.5, run the following in your terminal:

    deno upgrade

If Deno is not yet installed, run one of the following commands to install or [learn how to install it here](https://docs.deno.com/runtime/manual/getting_started/installation).

    # Using Shell (macOS and Linux):
    curl -fsSL https://deno.land/install.sh | sh
    
    # Using PowerShell (Windows):
    iwr https://deno.land/install.ps1 -useb | iex

## What’s new in Deno 2.5

* Permission sets in config
* Setup and teardown APIs to`Deno.test`
* WebSocket headers
* Runtime API for`deno bundle`
* HTML entrypoint support in`deno bundle`
* Permissions audit log
*`deno run`lists all tasks and scripts
* Simpler stdio from`Deno.ChildProcess`
* More consistent behavior for formatting options
* Dependency management
* Node.js`setTimeout`and`setInterval`with`--unstable-node-globals`
*`--watch`environment variables with`--env-file`
* Set TCP backlog size to`Deno.serve`
* TSConfig compatibility for frameworks
* Performance improvements
* Other features
* V8 14.0 and TypeScript 5.9.2
* Acknowledgments

## Permission sets in config

Oftentimes, granular permissions vary depending on context and subcommand: you may run`deno main.ts`with a certain set of permissions that differ from`deno test`or`deno compile`.

To simplify managing permissions in these scenarios, we have added permission sets that you can set in your`deno.json`config file:

deno.json

    {
      "permissions": {
        "process-data": {
          "read": ["./data"],
          "write": ["./data"]
        }
        // ...more permissions can be defined here by name...
      },
      "tasks": {
        "dev": "deno run -P=process-data main.ts"
      }
    }

That way, you can run a command with pre-defined permission flags:

    # Long
    deno run --permission-set=process-data main.ts
    
    # Short
    deno run -P=process-data main.ts

You can also set a`default`permission set, which can be used with`-P`with no argument:

deno.json

    {
      "permissions": {
        "default": {
          "read": ["./deno.json"],
          "env": true,
          "run": {
            "allow": ["git"]
          }
        }
      },
      "tasks": {
        "dev": "deno run -P main.ts"
      }
    }

Permissions can also be optionally specified within the`test`,`bench`, or`compile`keys:

deno.json

    {
      "test": {
        "permissions": {
          "read": ["./data"]
        }
      }
    }

When defined this way, you must pass the permission flag`-P`when running`deno test`, or you’ll receive an error:

    > deno test
    error: Test permissions were found in the config file. Did you mean to run with`-P`?
        at file:///Users/david/dev/scratch2/package-a/deno.json
    > deno test -P
    ...runs...
    > deno test --allow-read
    ...runs...
    > deno test -A
    ...runs...

For more information, please refer to [our documentation](https://docs.deno.com/runtime/fundamentals/configuration#permissions).

## Setup and teardown APIs to`Deno.test`

To make testing easier, we’ve added these new APIs to [`Deno.test`](https://docs.deno.com/runtime/fundamentals/testing/) to help perform setup and teardown for test cases:

*`Deno.test.beforeAll`
*`Deno.test.beforeEach`
*`Deno.test.afterAll`
*`Deno.test.afterEach`

Here’s a concrete example showing how to set up a test database:

test.ts

    import sqlite from "node:sqlite";
    import { assertEquals } from "jsr:@std/assert";
    
    let testDb: sqlite.DatabaseSync;
    
    // Run once before all tests
    Deno.test.beforeAll(() => {
      testDb = new sqlite.DatabaseSync(":memory:");
      testDb.exec(`CREATE TABLE users (
          id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE
        );
`);
    });
    
    // Run before each individual test
    Deno.test.beforeEach(() => {
      testDb.exec("DELETE FROM users");
      const insert = testDb.prepare(
        "INSERT INTO users (name, email) VALUES (?, ?)",
      );
      insert.run("Alice", "alice@example.com");
      insert.run("Bob", "bob@example.com");
    });
    
    // Run after each individual test
    Deno.test.afterEach(() => {
      // Clean up test data
      testDb.exec("DELETE FROM users");
    });
    
    // Run once after all tests
    Deno.test.afterAll(() => {
      testDb.close();
    });
    
    Deno.test("should find user by email", () => {
      const query = testDb.prepare("SELECT * FROM users WHERE email = ?");
      const user = query.get("alice@example.com");
      assertEquals(user?.name, "Alice");
    });
    
    Deno.test("should create new user", () => {
      const insert = testDb.prepare(
        "INSERT INTO users (name, email) VALUES (?, ?)",
      );
      insert.run("Charlie", "charlie@example.com");
    
      const countQuery = testDb.prepare("SELECT COUNT(*) as count FROM users");
      const result = countQuery.get();
      assertEquals(result!.count, 3); // 2 from beforeEach + 1 new
    });

For more information, please refer to [our`deno test`documentation](https://docs.deno.com/api/deno/testing#test-hooks).

## WebSocket headers

We’ve extended the WebSocket spec to allow for specifying custom headers when initiating a WebSocket connection:

main.ts

    const ws = new WebSocket("wss://api.example.com/socket", {
      headers: new Headers({
        "Authorization":`Bearer ${token}`,
        "X-Custom": "value",
      }),
    });

This can be useful in scenarios when you need to authenticate, attach session state, or pass metadata right at the handshake stage, without leaking sensitive data in the URL or doing extra roundtrips.

_Keep in mind that this will not work in browsers._

## Runtime API for`deno bundle`

In 2.4, [we re-introduced`deno bundle`](/v2.4#deno-bundle), which creates a single-file JavaScript file from JavaScript or TypeScript. In this release, we’ve added support for a runtime API, allowing you to programmatically bundle your client or server side JavaScript or TypeScript.

For example, you have`index.tsx`:

index.tsx

    import { render } from "npm:preact";
    
    import "./styles.css";
    
    const app = (
      <div>
        <p>Hello World!</p>
      </div>
    );
    
    render(app, document.body);

You can bundle programmatically with this`bundle.ts`script:

bundle.ts

    const result = await Deno.bundle({
      entrypoints: ["./index.tsx"],
      outputDir: "dist",
      platform: "browser",
      minify: true,
    });
    console.log(result);

Note that the [`Deno.bundle`](https://docs.deno.com/api/deno/~/Deno.bundle) API is experimental and must be used with the flag`--unstable-bundle`.

For more information about available runtime options and configurations, [please refer to our documentation](https://docs.deno.com/runtime/reference/bundling/).

## HTML entrypoint support in`deno bundle`

Previously,`deno bundle`required a`.js`/`.ts`/`.jsx`/`.tsx`file as an entrypoint. Now with 2.5, it can support HTML files as inputs:

    deno bundle --outdir dist index.html

With this command,`deno bundle`will find scripts referenced in the HTML file, bundle them, and then update the paths in`index.html`to point to the bundled scripts. If your app imports global css (`import "./styles.css"`), this will be bundled and injected into the HTML output as well.

With the same`index.tsx`from above, and an HTML file:

index.html

    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Example</title>
        <script src="./index.tsx" type="module"></script>
      </head>
    </html>

When you run`deno bundle --outdir dist index.html`, this is the resulting HTML:

    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Example</title>
        <script src="./index-2TFDJWLF.js" type="module" crossorigin></script>
        <link rel="stylesheet" crossorigin href="./index-EWSJYQGA.css">
      </head>
    </html>

Note that the bundled output includes a hash based on the bundled content, to fingerprint this specific bundle.

HTML inputs are also fully supported in the runtime API mentioned above.

While simple and zero-config, this feature overlaps a bit with Vite . In fact, [Fresh recently adopted Vite](https://deno.com/blog/fresh-and-vite) for its development server and build pipeline. Think of it this way:

*`deno bundle index.html`\- great for small, static apps where you just want a quick packaged build.
* Vite - better for complex projects that benefit the wider Vite ecosystem.

Both paths run seamlessly on Deno - you can pick whichever fits your workflow best.

## Permissions audit log

One core aspect of security is having an audit log for accountability, which shows who did what, when, and how.

With 2.5, we’ve added a`DENO_AUDIT_PERMISSIONS`env var that sets the path for a JSONL permission audit log, which contains the permission and value.

main.ts

    console.log(Deno.env.get("FOO"));
    const content = await Deno.readTextFile("data.csv");
    Deno.writeTextFileSync("log.txt", "...");

    DENO_AUDIT_PERMISSIONS=./permission.log deno run -A main.ts

Here’s an example of what the audit log might look like:

permission.log

    {
      "v": 1,
      "datetime": "2025-09-05T12:12:35Z",
      "permission": "env",
      "value": "FOO"
    }
    {
      "v": 1,
      "datetime": "2025-09-05T12:14:18Z",
      "permission": "read",
      "value": "data.csv"
    }
    {
      "v": 1,
      "datetime": "2025-09-05T12:14:26Z",
      "permission": "write",
      "value": "log.txt"
    }

This can be combined with the env var [`DENO_TRACE_PERMISSIONS=1`](https://docs.deno.com/runtime/fundamentals/security/#permissions), which will also add the stack trace for permission requests to the audit log.

For more information, please visit [our documentation](https://docs.deno.com/runtime/fundamentals/security/#permissions).

##`deno run`lists all tasks and scripts

Previously,`deno run`with no arguments printed an error, but in 2.5 it will output a list of available tasks from`deno.json`and scripts from`package.json`:

    deno run
    Please specify a [SCRIPT_ARG] or a task name.
    
    Available tasks:
    - dev
        deno run -A --env --watch=static/,routes/,data/ dev.ts
    - build
        deno run -A dev.ts build
    - db:push (package.json)
        dotenv drizzle-kit push
    - db:generate (package.json)
        dotenv drizzle-kit generate

This will make it simpler to quickly see what tasks and scripts you can execute from the command line.

## Simpler stdio from`Deno.ChildProcess`

We’ve added convenience methods to`stdout`and`stderr`streams in`Deno.ChildProcess`, making it easier to get various output types. For example:

main.ts

    const sub = new Deno.Command("cat", {
      args: ["hello.txt"],
      stdout: "piped",
    }).spawn();
    
    // 2.4 and before
    import { toText } from "jsr:@std/streams/to-text";
    const stdout = await toText(sub.stdout);
    
    // 2.5
    const stdout = await sub.stdout.text();

Convenience methods that are now available, match those on [`Response`](https://developer.mozilla.org/en-US/docs/Web/API/Response):

*`Deno.SubprocessReadableStream.arrayBuffer()`->`ArrayBuffer`
*`Deno.SubprocessReadableStream.bytes()`->`Uint8Array`
*`Deno.SubprocessReadableStream.json()`->`unknown`
*`Deno.SubprocessReadableStream.text()`->`string`

## More consistent behavior for formatting options

When the`spaceSurroundingProperties`option is set to false, [`deno fmt`](https://docs.deno.com/runtime/reference/cli/fmt/) will now also apply this to braces in named`import`and`export`statements:

deno.json

    {
      "fmt": {
        "spaceSurroundingProperties": false
      }
    }

    // Old: Spaces preserved in`import`statement.
    import { foo } from "bar";
    
    const baz = {a: 1};
    
    // New: Spaces removed.
    import {foo} from "bar";
    
    const baz = {a: 1};

This behavior roughly matches [that of stylistic’s curly rule](https://eslint.style/rules/object-curly-spacing). Note that this option defaults to`true`, so users won’t be affected unless they have explicitly configured it to`false`.

Thank you [mologie](https://github.com/mologie) for this contribution!

## Dependency management

In 2.5, we’ve introduced several changes to improve dependency management. Firstly, we have changed the`deno install`report format to make it more useful when managing dependencies:

    $ deno install
    Installed 181 packages in 2093ms
    Reused 161 packages from cache
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    +++++++++++++++++++++++++++++++++++++++
    Downloaded 10 packages from JSR
    ++++++++++
    Downloaded 86 packages from npm
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    ++++++++++++++++++++++++++++
    
    Dependencies:
    + jsr:@deno/rust-automation 0.21.0
    + jsr:@denosaurs/emoji 0.3.1
    + jsr:@fresh/core 2.0.0-alpha.58
    + jsr:@fresh/plugin-tailwind 0.0.1-alpha.9
    + jsr:@std/data-structures 1.0.9
    + jsr:@std/front-matter 1.0.9
    + jsr:@std/internal 1.0.10
    + jsr:@std/testing 1.0.15
    + jsr:@std/toml 1.0.6
    + jsr:@std/yaml 1.0.9
    + npm:@algolia/client-search 4.14.3
    + npm:@algolia/requester-fetch 4.14.3
    + npm:@maxmind/geoip2-node 5.0.0
    + npm:@opentelemetry/api 1.9.0
    + npm:@preact/signals 2.2.1
    …

You now get a quick overview how many direct dependencies were installed, how many packages were pulled from a cache as well as how many JSR and npm packages were downloaded.

We have also simplified the warning displayed if an npm package installed with`deno install`requires a build script:

    ╭ Warning
    │
    │  Ignored build scripts for packages:
    │  npm:sharp@0.34.3
    │
    ╰─ Run "deno install --allow-scripts=npm:sharp@0.34.3" to run build scripts.

_We will soon ship a tool that makes management of these build scripts more convenient, collaborative and secure._

###`no-unversioned-import`lint rule

The [`no-unversioned-import`](https://docs.deno.com/lint/rules/no-unversioned-import) rule requires that all`npm:`and`jsr:`import statements include a version number. This lint rule is enabled by default.

While it’s convenient to write`import chalk from "npm:chalk"`for quick hacking, it’s not recommended in production, as Deno will automatically pull the latest version of the package. If the package published a breaking change, it could cause your code to fail.

main.ts

    import chalk from "npm:chalk";

    $ deno lint
    
    error[no-unversioned-import]: Missing version in specifier
     --> /dev/main.ts:1:19
      |
    1 | import chalk from "npm:chalk";
      |                   ^^^^^^^^^^^
      = hint: Add a version requirement after the package name
    
      docs: https://docs.deno.com/lint/rules/no-unversioned-import

_This rule is part of the`recommended`set and will be applied automatically if you haven’t configured [`deno lint`](https://docs.deno.com/runtime/reference/cli/lint/)._

###`no-import-prefix`lint rule

The [`no-import-prefix`](https://docs.deno.com/lint/rules/no-import-prefix) rule ensures that all dependencies are declared in either`deno.json`or`package.json`rather than imported directly from URLs or package registries. This promotes better dependency management and makes it easier to track and update dependencies.

deno.json

    {
      "imports": {
        "oak": "jsr:@oak/oak@17"
      }
    }

main.ts

    import { Application } from "oak/application";
    import chalk from "npm:chalk";

    $ deno lint
    
    error[no-import-prefix]: Inline 'npm:', 'jsr:' or 'https:' dependency not allowed
     --> /dev/main.ts:2:19
      |
    2 | import chalk from "npm:chalk";
      |                   ^^^^^^^^^^^
      = hint: Add it as a dependency in a deno.json or package.json instead and reference it here via its bare specifier
    
      docs: https://docs.deno.com/lint/rules/no-import-prefix

_This rule is part of the new`workspace`set and will be applied automatically if there’s`deno.json`or`package.json`discovered._

## Node.js`setTimeout`and`setInterval`with`--unstable-node-globals`

This release brings back`--unstable-node-globals`flag that makes Deno use Node.js flavor of`setTimeout`,`setInterval`,`clearTimeout`, and`clearInterval`API.

For context, Deno has always used Web version of these APIs. The change is subtle - the Web APIs return and accept numbers (timer ID), but Node.js APIs return and accept`Timer`object.

Some npm libraries rely on`Timer.ref()`or`Timer.unref()`APIs that have equivalent`Deno.refTimer()`and`Deno.unrefTimer()`, but over the years we noticed that this situation leads to more confusion rather than simplification of developers’ lives.

So starting with Deno v2.5 you can use [`--unstable-node-globals`](https://docs.deno.com/runtime/reference/cli/unstable_flags/#--unstable-node-globals) flag, or [`DENO_COMPAT=1`env var](/blog/v2.4#deno_compat1) to tell Deno to prefer using Node.js timer APIs.

We plan to change used APIs to be Node.js version in Deno 3. For most users there will be no changes required to adjust to the new APIs.

##`--watch`environment variables with`--env-file`

When using [`--watch`](https://docs.deno.com/runtime/getting_started/command_line_interface/#watch-mode) and [`--env-file`](https://docs.deno.com/runtime/reference/env_variables/#.env-file) flag, Deno will automatically reload environment variables when your environment file is updated.

Thank you [meetdhanani17](https://github.com/meetdhanani17) for this contribution!

## Set TCP backlog size to`Deno.serve`

[`Deno.serve`](https://docs.deno.com/runtime/fundamentals/http_server/) is a one-line, dead simple way to build an HTTP server. However, previously, there wasn’t an easy way to set the backlog size (the maximum number of pending TCP connections to queue for your listener), which is useful if you’re expecting huge bursts of traffic.

In 2.5, we’ve added a new argument,`tcpBacklog`, letting you explicitly set the maximum number of queued incoming connections that can used with`Deno.listen{Tls}`and`Deno.serve`:

server.ts

    Deno.serve({
      port: 4600,
      tcpBacklog: 4096,
    }, (_req) => new Response("hello"));

The default TCP backlog has been increased to 511, which is a default used by many high performance servers.

## TSConfig compatibility for frameworks

Deno 2.4 [expanded its`tsconfig.json`compatibility](/blog/v2.4#better-tsconfigjson-support) with a focus on allowing Vite-configured projects to type-check with`deno check`out-of-the-box. Previously, these would have required a well-versed user to convert the configuration so the Deno CLI and [LSP](https://docs.deno.com/runtime/reference/lsp_integration/) would work.

Deno 2.5 adds support for [`compilerOptions.rootDirs`](https://github.com/denoland/deno/pull/30495) and the [`"bundler"`](https://github.com/denoland/deno/pull/30603) option for`compilerOptions.moduleResolution`, fixing type-checking for the following project templates:

***SvelteKit**: [`npx sv create`](https://svelte.dev/docs/cli/sv-create)
***Next.js**: [`npx create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app)

You can try these out by creating a basic application from one of these commands as you would with Node.js, adding a`deno.json`file with content`{}`to enable the LSP and running the`deno check`command. Ensure the Deno extension is installed.

We aim for comprehensive TypeScript/`tsconfig.json`compatibility with modern Node.js projects. Please continue reporting any discovered incompatibility using our [issue tracker](https://github.com/denoland/deno/issues)!

## Performance improvements

**Emit cache optimization**: Deno now only clears its emit cache when the underlying`deno_ast`version changes, rather than on every update, significantly reducing unnecessary recompilation overhead.

**CommonJS wrapper efficiency**: Memory usage and heap allocations have been reduced when creating CommonJS wrapper modules, making Node.js compatibility more efficient.

**Conditional JSX transpilation**: JSX transpilation is now skipped entirely when JSX is disabled, avoiding unnecessary processing overhead for projects that don’t use JSX.

**Improved`structuredClone`**: The`structuredClone`API now uses more efficient internal implementations, speeding up object cloning operations.

**`Buffer`method optimizations**: The`Buffer.subarray`and`Buffer.prototype.utf8Slice`methods have been optimized for better performance when working with binary data.

**Node-API optimizations**: Various Node.js API compatibility layer optimizations reduce overhead when using native Node.js modules.

## Other features

**Disable hostname verification in TLS connections**: For development and testing scenarios, you can now disable hostname verification in TLS connections, providing more flexibility when working with self-signed certificates or non-standard certificate configurations. ([#30409](https://github.com/denoland/deno/pull/30409))

**Unix socket and vsock proxy support via environment variable**: You can now enable parsing Unix socket and vsock proxies for the`fetch`API with environment variables. ([#30377](https://github.com/denoland/deno/pull/30377))

**Pull-based diagnostics in LSP**: The Language Server Protocol implementation now uses pull-based diagnostics, improving performance and responsiveness when working with large codebases in your editor. ([#30325](https://github.com/denoland/deno/pull/30325))

**Enhanced Node.js async hooks**: Improved Node.js compatibility with async hooks implementation for`nextTick`TickObject tracking, making it easier to migrate existing Node.js applications that rely on this functionality. ([#30578](https://github.com/denoland/deno/pull/30578))

**Bundle dependencies support**: npm packages that use`bundleDependencies`in their`package.json`are now fully supported, expanding compatibility with the broader npm ecosystem. ([#30521](https://github.com/denoland/deno/pull/30521))

**Vsock transport for telemetry**: OpenTelemetry now supports vsock transport, enabling telemetry data collection in specialized virtualized environments and improving observability options. ([#30001](https://github.com/denoland/deno/pull/30001))

## V8 14.0 and TypeScript 5.9.2

Deno 2.5 upgrades to¬†V8 14.0 and [TypeScript 5.9.2](https://devblogs.microsoft.com/typescript/announcing-typescript-5-9/) bringing new language features and performance improvements.

This release includes a big overhaul of [the`Temporal`API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal). As the implementation of this API matures across JavaScript engines, our hopes are that we can soon remove`--unstable-temporal`flag.

## Acknowledgments

We couldn‚Äôt build Deno without the help of our community! Whether by answering questions in our community¬†[Discord server](https://discord.gg/deno)¬†or¬†[reporting bugs](https://github.com/denoland/deno/issues), we are incredibly grateful for your support. In particular, we‚Äôd like to thank the following people for their contributions to Deno 2.5: ÊûóÁÇ≥ÊùÉ, Alex Yang, Asher Gomez, cions, ctrl+d, Daniel Osvaldo Rahmanto, EdamAmex, Edilson Pateguana, Garret Thompson, gerald, James Bronder, Jo√£o Victor Lopes, Kendell R, Kenta Moriuchi, Kingsword, Krhougs, Kumbham Ajay Goud, Laurence Rowe, Lucas Vieira, Luke Swithenbank, Meet Dhanani, Oliver Kuckertz, Ruyut, sgasho, and ud2.

Would you like to join the ranks of Deno contributors?¬†[Check out our contribution docs here](https://docs.deno.com/runtime/manual/references/contributing), and we‚Äôll see you on the list next time.

Believe it or not, the changes listed above still don‚Äôt tell you everything that got better in 2.5. You can view the¬†[full list of pull requests merged in Deno 2.5 on GitHub](https://github.com/denoland/deno/releases/tag/v2.5.0).

Thank you for catching up with our 2.5 release, and we hope you love building with Deno!

>**üö®Ô∏è¬†[There have been major updates to Deno Deploy!](/deploy)¬†üö®Ô∏è**
>
> * [Database connections and data explorer right in the UI](https://docs.deno.com/deploy/early-access/reference/databases/)
> * [Connect to AWS and GCP via Cloud Connections](https://docs.deno.com/deploy/early-access/reference/cloud-connections/)
> * [Automatic and immediate observability and telemetry](https://docs.deno.com/deploy/early-access/reference/observability/)
>

>
> and¬†[much more!](https://docs.deno.com/deploy/early-access/changelog/)
>
> [Get early access today.](/deploy)

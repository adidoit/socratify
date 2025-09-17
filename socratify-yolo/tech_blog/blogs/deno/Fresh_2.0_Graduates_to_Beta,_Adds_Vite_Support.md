---
title: "Fresh 2.0 Graduates to Beta, Adds Vite Support"
author: "Unknown"
url: "https://deno.com/blog/fresh-and-vite"
date: "2025-09-15"
---

# Fresh 2.0 Graduates to Beta, Adds Vite Support

September 2, 2025[](/feed "Atom Feed")

* [![](https://github.com/marvinhagemeister.png)Marvin Hagemeister](https://github.com/marvinhagemeister)

* [Product Update](/blog?tag=product-update)
* [Fresh](/blog?tag=fresh)

After 63 alpha releases, Fresh 2.0 is graduating to beta. These betas are effectively release candidates ‚Äî the architecture is now stable, and the last big change has landed.

That change is Vite integration. With the new [plugin](https://jsr.io/@fresh/plugin-vite), Fresh can now optionally run as a Vite plugin, giving developers access to hot module reloading, the full Vite plugin ecosystem, and modern tooling for both client and server code ‚Äî all while remaining fully usable without Vite.

    import { defineConfig } from "vite";
    import { fresh } from "@fresh/plugin-vite";
    
    export default defineConfig({
      plugins: [fresh()],
    });

The Fresh Vite plugin fully embraces Vite‚Äôs new [Environment API](https://vite.dev/guide/api-environment) to leverage the power of the plugin ecosystem for both server code and client code. For configuration details, see the [Fresh docs](https://fresh.deno.dev/docs/advanced/vite).

## Hot module reloading in islands

With Vite providing access to the underlying module graph of each environment, we can now provide proper hot module reloading (“HMR”) support. Instead of reloading the page and losing all state, HMR allows UI elements to be swapped out whilst keeping the current page alive. Right now, this is scoped to island code and server-only changes will still reload the page.

## 10x faster boot times

A lot of care has been spent on making the production output as efficient as possible. In Fresh 2, routes are now loaded on demand ‚Äî only the code needed to handle a request is loaded and executed. With the Vite plugin, we‚Äôre going a step further and will bundle the server code to reduce the number of files that need to be resolved and loaded.

As a result, starting a Fresh app in production is an order-of-magnitude faster. In our projects, we‚Äôve seen boot times improve by**9‚Äì12√ó**, depending on project size. We measure this from the moment the process starts until the app is ready to handle requests. That time usually includes resolving files, loading and instantiating modules, and other work done by the JavaScript engine.

Here are the boot numbers for the Fresh website:

* Before:¬†`86ms`
* After:¬†`8ms`

## Out of the box`react`aliasing

Aliasing`react`,`react-dom`and other packages to`preact/compat`has always been a bit tricky. This mapping often needed to be manually specified, and required app code to use`esm.sh`instead of pulling dependencies directly from`npm`. Having to be conscious about this was never an ideal setup.

With our Vite plugin, this will be taken care of for you. Install third party npm packages as usual and never run into aliasing issues again!

## The`<Head>`component is back!

The beloved [`<Head>`](https://fresh.deno.dev/docs/examples/modifying-the-head) component from Fresh 1.x is back again! It can be used from components to render elements into the`<head>`portion of an HTML document.

    export default function Page() {
      return (
        <div>
          <Head>
            <title>About me</title>
          </Head>
          <h1>About me</h1>
          <p>some text about me...</p>
        </div>
      );
    }

This feature isn‚Äôt tied to the Vite integration ‚Äî you can already use it today in a Fresh 2 app. We had removed it in 1.x because the implementation was messy and hurt rendering performance. But with Fresh 2‚Äôs cleaner architecture and the chance to explore different approaches, we‚Äôve landed on a much simpler, more efficient solution.

## Try it out!

You can try out the Vite plugin today by running:

    deno run -Ar jsr:@fresh/init

This will guide you through setting up a simple Fresh app that‚Äôs ready to be used with Vite. Let us know if you run into [any issues](https://github.com/denoland/fresh/issues)!

Already using Fresh 1.x? The updated [migration guide](https://fresh.deno.dev/docs/examples/migration-guide) walks you through upgrading to Fresh 2.0 step by step.

Also check out the [new guide on deploying to Cloudflare Workers](https://fresh.deno.dev/docs/deployment/cloudflare-workers), if that’s your preference.

>**üö®Ô∏è¬†[There have been major updates to Deno Deploy!](https://deno.com/deploy)¬†üö®Ô∏è**
>
> * [Improved Playgrounds with livestreaming logs, traces, and templates like Next.js](https://www.youtube.com/watch?v=fRFqZsBivCo)
> * [Automatic and immediate observability and telemetry](https://www.youtube.com/watch?v=PwDU8yTZmUM)
> * [Simpler management for environment variables](https://x.com/deno_land/status/1935625197295739103)
>

>
> and¬†[much more!](https://docs.deno.com/deploy/early-access/changelog/)
>
> [Get early access today.](https://deno.com/deploy)

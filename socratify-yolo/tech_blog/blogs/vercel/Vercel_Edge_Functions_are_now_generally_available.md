---
title: "Vercel Edge Functions are now generally available"
company: "vercel"
url: "https://vercel.com/blog/edge-functions-generally-available"
content_length: 10644
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

5 min read

Copy URL

Copied to clipboard!

Dec 15, 2022

Faster, cheaper, more flexible compute for your workloads.

Access to fast, global compute can give developers more flexibility to build rich experiences, regardless of their users' physical location or network speed. Vercel's Edge Functions aim to bring this capability into every developer's toolkit for building on the Web. 

This past summer, alongside our GA of Edge Middleware, we released Edge Functions to Public Beta. During our beta period, our Edge Network has seen over 30 _billion_ Edge Function invocations.

Since launching, we’ve made Edge Functions **faster** , more **flexible** , and **capable of even larger workloads** :

  * Major infrastructure optimizations for improved performance

  * Support for `cache-control` [standard](https://vercel.com/docs/concepts/functions/edge-functions/edge-caching) for function responses

  * Added ability to express region preference

  * Added support for WebAssembly workloads

  * Increased function size limits for Enterprise and Pro teams




Now, we’re excited to announce that beginning today, Edge Functions are now generally available (GA) for all customers.

## Link to headingWhat are Edge Functions?

Vercel Edge Functions are JavaScript, TypeScript, or WebAssembly functions that are generally more efficient and faster than traditional Serverless compute, since they operate within a much leaner runtime. Deployed globally by default, Edge Functions run in the region closest to the request for the lowest latency possible.

pages/api/hello.ts
    
    
    1
    
    export const config = {
    
    2
    
      runtime: 'edge'
    
    3
    
    }
    
    4
    
    
    
    
    5
    
    export default function handler(req: Request) {
    
    6
    
      return new Response("Hello World");
    
    7
    
    }

A hello world Edge Function in Next.js. Edge Functions are natively available in Next.js, SvelteKit, Astro, and Nuxt or as a standalone function. runtime: 'edge' can be leveraged with Vercel CLI 28.9.0 and above.

Unlike Edge Middleware, Functions run _after_ the cache, and therefore can both cache and return responses, making them great for data fetching or rewrites. 

> “We’ve been using an Edge API Route to proxy requests to our backend and rewrite headers on the fly. The lightweight nature of the Edge Runtime and the ability to stream responses ensures that response times stay fast. Additionally, the switch from regular API Routes reduced our costs significantly. We’ve been using an Edge API Route to proxy requests to our backend and rewrite headers on the fly. The lightweight nature of the Edge Runtime and the ability to stream responses ensures that response times stay fast. Additionally, the switch from regular API Routes reduced our costs significantly. We’ve been using an Edge API Route to proxy requests to our backend and rewrite headers on the fly. The lightweight nature of the Edge Runtime and the ability to stream responses ensures that response times stay fast. Additionally, the switch from regular API Routes reduced our costs significantly. ”
> 
> ![](https://assets.vercel.com/image/upload/contentful/image/e5382hct74si/7cO0izVtCL4iq4ccV4L7Cx/c30245621a7d92fbc66756db4029387f/Group_6__2_.png)
> 
> **Connor Bär , ** Senior Frontend Engineer

Vercel Edge Functions are natively supported by Next.js, and many other frameworks like [Nuxt](https://nuxt-on-the-edge.vercel.app/), [Astro](https://astro-on-the-edge.vercel.app/), and [SvelteKit](https://sveltekit-on-the-edge.vercel.app/). Edge Functions can also be created as a standalone function in Vercel CLI.

In Next.js, set your app’s default runtime to `edge`, or select the runtime for an individual function. 

## Link to headingMaximum speed, minimum cost

Edge Functions use the lightweight Edge Runtime, which is built on the V8 engine used by the Chrome browser and doesn’t run within a MicroVM, making Edge Functions generally faster and more cost-effective than traditional serverless. 

Vercel's own open-source [OG Image Generation project](https://vercel.com/docs/concepts/functions/edge-functions/og-image-generation) now leverages Edge Functions for global, fast compute. By moving to the Edge, these APIs return almost 40% faster than a hot Serverless Function at a fraction of the cost.

This efficiency means that generating a million images with OG Image Generation running in Edge Functions costs nearly 15x less than the cost of generating those same million images in Serverless Functions.

## Link to headingWhat's changed: Even more flexibility

### Link to headingRegional Edge Functions

Vercel now gives you the option to [express a region preference](https://vercel.com/blog/regional-execution-for-ultra-low-latency-rendering-at-the-edge) for Edge Functions, close to your data source.

Edge Functions are deployed globally by default, so compute happens in the region closest to the user making the request. For tasks that don't require a database, like our OG Image Generation tool, this reduces latency between function and user, reinforcing the benefit of fast, global compute.

However, for functions that need to query a database, global compute could mean the request takes _longer_ because the request could come in from a region far from the database. That additional latency may mean that the benefits of Edge Functions get outweighed by the length of that request. 

With Regional Edge Functions, you can bind a function to a specific region, close to your database. This ensures that the benefit of fast compute isn't negated by additional latency.

With millions of files in Sanity, **Keystone Education Group, in partnership with** **NoA Ignite** relies on fast, efficient data fetching from the headless CMS to power Keystone's site. Running those API Routes efficiently is a priority for their development team, so compute co-location is crucial. At this scale, the team can save money and deliver an improved experience for their Sanity-based content by leveraging the leaner runtime.

> “We shifted Keystone's API Routes incrementally from Serverless to Edge Functions and couldn't be happier. It was very straightforward for us to make the change on Vercel, and as a result, we've been able to reduce costs and we've seen our compute efficiency drastically improve. We shifted Keystone's API Routes incrementally from Serverless to Edge Functions and couldn't be happier. It was very straightforward for us to make the change on Vercel, and as a result, we've been able to reduce costs and we've seen our compute efficiency drastically improve. We shifted Keystone's API Routes incrementally from Serverless to Edge Functions and couldn't be happier. It was very straightforward for us to make the change on Vercel, and as a result, we've been able to reduce costs and we've seen our compute efficiency drastically improve. ”
> 
> ![](https://assets.vercel.com/image/upload/contentful/image/e5382hct74si/4pUW2zdaBlS9rjLCPIFQkn/392a11ec3962d5a799bbb8684a69c1df/Group_7__5_.png)
> 
> **Tormod Ulsberg , ** Principal Architect

### Link to headingSupport for WebAssembly 

Because Vercel’s Edge Functions run in a lightweight execution environment built on the [V8 JavaScript Engine](https://v8.dev/), we were able to [add support for WebAssembly, or Wasm](https://vercel.com/blog/introducing-support-for-webassembly-at-the-edge), a language similar to Assembly language that’s commonly supported as a low-level language by browsers.

WebAssembly lets you take a function written in a different language—like C or Rust—and use that directly in Edge Functions. This lets you move many existing libraries to Edge Functions just by recompiling for Wasm. Complex, computationally heavy workloads often run twice as fast in WebAssembly as they do when written in JavaScript.

Moving Vercel’s [OG Image Generation](https://vercel.com/blog/introducing-vercel-og-image-generation-fast-dynamic-social-card-images) to Wasm and Edge Functions, Image Generation became **5x faster** in P99 TTFB.

### Link to headingIncreased workload size and improved infrastructure

Pro and Enterprise customers can now use larger Edge Functions. We’ve increased the size limit for Edge Functions to 2 MB for Pro customers and 4 MB for Enterprise customers. That’s 2x and 4x bigger than before, respectively.

We’ve also significantly improved our routing for Edge Functions, massively reducing the time it takes to start executing a function. 

## Link to headingThe future of Edge Functions

We’re excited to continue improving our compute products—both Edge and Serverless Functions.

First, we’re improving the compatibility between Edge Functions and Serverless Functions. Our goal is for the Edge Runtime to be a proper subset of the Node.js API. We want users to be able to choose their execution environment based on performance and cost characteristics, not the API.

We’re also improving the observability and error reporting for functions, starting with Vercel Logs and Monitoring. We want to make it easier for you to understand how your functions are executing and how and when they encounter errors. We want to make understanding how your functions work on Vercel clearer and troubleshooting problems simpler.

We're working towards a goal of seamless interoperability with a great developer experience, both locally and in production, across all our compute products.

## Link to headingPricing and Limits

Edge Functions are billed in units of 50 ms of CPU time per invocation, called execution units. CPU time is the time spent performing computations, not including the time spent waiting for data fetches. This means that if you query a database or fetch an API—even from a slower backend like an AI inference service—you're not paying for the time spent waiting for the data fetch.

Hobby users have 500,000 monthly Edge Function execution units included for **free**. Pro and Enterprise teams have 1 million monthly Edge Function execution units included for free and can[ add on additional usage](https://vercel.com/pricing).

You can see the number of executions, execution units, and the CPU time usage of your Edge Functions in your account dashboard.

## Link to headingNext steps

To get started with Vercel, [deploy an Edge Function](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fedge-api-routes%2Fhello-world-next&project-name=next-edge-api-route&repository-name=next-edge-api-route) or check out our [documentation](https://vercel.com/docs/concepts/functions/edge-functions) to get started.

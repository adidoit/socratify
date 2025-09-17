---
title: "How we optimized package imports in Next.js"
company: "vercel"
url: "https://vercel.com/blog/how-we-optimized-package-imports-in-next-js"
content_length: 10623
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

5 min read

Copy URL

Copied to clipboard!

Oct 13, 2023

40% faster cold boots and 28% faster builds

In the [latest version of Next.js](https://nextjs.org/blog/next-13-5), we've made improvements to optimize package imports, improving both local dev performance and production cold starts, when using large icon or component libraries or other dependencies that re-export hundreds or thousands of modules.

This post explains why this change was needed, how we've iterated towards our current solution, and what performance improvements we've seen.

## Link to headingWhat is a barrel file?

A **barrel file** in JavaScript is a way to group and export multiple modules from a single file. It allows for easier importing of the grouped modules by providing a centralized location to access them.

For example, let's say we have three modules (`module1.js`, `module2.js`, `module3.js`) within a `utils/` directory. We can create a barrel file named `index.js` within the same directory:

index.js
    
    
    1
    
    export { default as module1 } from './module1';
    
    2
    
    export { default as module2 } from './module2';
    
    3
    
    export { default as module3 } from './module3';

Now, instead of importing each module individually like this in your application:
    
    
    1
    
    import module1 from './utils/module1';
    
    2
    
    import module2 from './utils/module2';
    
    3
    
    import module3 from './utils/module3';

We can import _all_ modules collectively using the barrel file, without needing to know about the internal structure:
    
    
    1
    
    import { module1, module2, module3 } from './utils';

Barrel files can improve code organization and maintainability by providing an easily accessible interface for related modules. Because of this, it’s used widely by JavaScript packages, especially icon and component libraries.

Some popular icon and component libraries have **up to 10,000 re-exports in their entry barrel file**.

## Link to headingWhat's the problem with barrel files?

There's a hidden cost with JavaScript runtimes in every `require(...)` and `import '...'`. If you want to use one single export from a barrel file that imports thousands of other things, you are still paying the price of importing other unneeded modules.

For many popular React packages, **it takes 200~800ms just to import them**. In some extreme cases, it can [take a few seconds.](https://marvinh.dev/blog/speeding-up-javascript-ecosystem-part-7/)

These slowdowns affect both local development and production performance, especially in a serverless environment. Every time the app is started, we’ll have to import everything again.

## Link to headingCan’t we tree-shake it?

Tree-shaking is a _bundler_ feature (Webpack, Rollup, Parcel, esbuild, etc.), not a JavaScript runtime feature. If the library is marked as `external`, it remains a black box. The bundler can't do optimizations inside that box because the dependency would be required at runtime instead.

![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F1uvdi71hoXKaRi6vTls0qi%2F4cda29f439bf169b7166edb47e87369f%2Fbundle__12_.png&w=1920&q=75)![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F2y0SENU7KUhl5uAuo4O1Nj%2Ff290bfe7e1dfa116a4467c670e626206%2Fbundle__13_.png&w=1920&q=75)

If we choose to bundle the library together with the application code, tree-shaking will work if the import doesn’t have side effects (`sideEffects` in `package.json`). However, it will take more time to compile all modules, analyze the whole module graph, and then tree-shake properly. This causes substantially slower builds.

![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F5GDRnrI1GVaQvVIgm0HUUK%2Fcd2bbbb90f699071d6ffa630a4d7d0a4%2Fbundle__7_.png&w=1920&q=75)![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F51xcJ5VwnREoAkuI6JhUZ7%2F3cc76e57dac2c7a1c16652713966542e%2Fbundle__6_.png&w=1920&q=75)

## Link to headingOur first attempt: `modularizeImports`

The first approach we tried in Next.js was called [`modularizeImports`](https://nextjs.org/docs/architecture/nextjs-compiler#modularize-imports). This option allows you to configure the mapping relationship of exported names and their original module paths behind a package’s barrel file entrypoint.

For example, if the package `my-lib` has this `index.js` as the entry:

my-lib/index.js
    
    
    1
    
    export { default as module1 } from './module1';
    
    2
    
    export { default as module2 } from './module2';
    
    3
    
    export { default as module3 } from './module3';

We can configure a compiler transform of `my-lib/{{member}}`, which tells Next.js to change the user's import `import { module2 } from 'my-lib'` into `import module2 from 'my-lib/module2'`. This means we can skip the barrel file and directly import from the target, preventing loading unnecessary modules.

This change makes both the build time _and_ runtime fast:

![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F5MQ3kHxpyrYnXxSUMqX8gL%2Fa5740a5e0bed853b4ed0d5a9f7848bef%2Fbundle__9_.png&w=1920&q=75)![](/vc-ap-vercel-marketing/_next/image?url=https%3A%2F%2Fassets.vercel.com%2Fimage%2Fupload%2Fcontentful%2Fimage%2Fe5382hct74si%2F2tpTkpBkvN8yj6T5olIgqc%2Fc29d6c982c990166a521a21443bdf167%2Fbundle__8_.png&w=1920&q=75)

However, this configuration is based on the internal directory structure of the library, and is configured heavily by hand. There are millions of `npm` packages with different versions, and there’s no way to scale with this solution efficiently.

If the bundler includes a default configuration for popular libraries without locking down the library’s version, this will make the import transformation invalid when the internal structure of that lib changes in the future. We needed a better solution.

## Link to headingNew solution: `optimizePackageImports`

To solve the remaining difficulties of configuring the `modularizeImports` option, we’ve introduced a new `optimizePackageImports` option to do it automatically in [Next.js 13.5](https://nextjs.org/blog/next-13-5).

To start, you can configure which packages to opt in:

next.config.js
    
    
    1
    
    module.exports = {
    
    2
    
      experimental: {
    
    3
    
        optimizePackageImports: ["my-lib"]
    
    4
    
      }
    
    5
    
    }

When this option is enabled, Next.js will analyze the entry file of `my-lib` and figure out if it’s a barrel file. If so, it analyzes the file on the fly and automatically maps all imports, similarly to how `modularizeImports` works.

This process is cheaper than tree-shaking, since it only scans the entry barrel files in one pass. It also recursively handles nested barrel files and wildcard exports (`export * from`), and bails out of the process when hitting a non-barrel file.

Since this new option doesn’t depend on the package's internal implementations, we [pre-configured a list of common libraries](https://github.com/vercel/next.js/blob/12e888126ccf968193e7570a68db1bc35f90d52d/packages/next/src/server/config.ts#L710-L765) that immediately benefit from this, such as `lucide-react` and `@headlessui/react.`

In the future, we’re exploring ideas to automatically tell if a package should be opted-in or not. For now, the list can keep expanding as the community and our team discover new packages to optimize.

## Link to headingMeasuring performance improvements

We've seen improvements in local development speed, production build speed, as well as faster cold starts.

### Link to headingLocal development

In our local benchmarking on a M2 MacBook Air, when using one of the most popular icon or component libraries, we are seeing **a 15%~70% development time boost** depending on the actual library:

  * `@mui/material`: 7.1s (2225 modules) -> 2.9s (735 modules) (-4.2s)

  * `recharts`: 5.1s (1485 modules) -> 3.9s (1317 modules) (-1.2s)

  * `@material-ui/core`: 6.3s (1304 modules) -> 4.4s (596 modules) (-1.9s)

  * `react-use`: 5.3s (607 modules) -> 4.4s (337 modules) (-0.9s)

  * `lucide-react`: 5.8s (1583 modules) -> 3s (333 modules) (-2.8s)

  * `@material-ui/icons`: 10.2s (11738 modules) -> 2.9s (632 modules) (-7.3s)

  * `@tabler/icons-react`: 4.5s (4998 modules) -> 3.9s (349 modules) (-0.6s)

  * `rxjs`: 4.3s (770 modules) -> 3.3s (359 modules) (-1.0s)




These time savings are for the initial boot in local dev, but they _also_ affect the speed of Hot Module Replacement (HMR), letting live local dev feel much faster. The numbers add up quickly if you are using multiple libraries with many sub-modules.

### Link to headingProduction builds

In a benchmark of a Next.js App Router page with `lucide-react` and `@headlessui/react`, built on a M2 MacBook Air, `next build` runs **~28% faster** because it no longer needs to do module resolution and tree-shaking.

### Link to headingFaster cold boots

In a local environment, we’re seeing the Node.js server start **~10% faster** when rendering a simple route that uses `lucide-react` and `@headlessui/react`.

In a serverless environment like Vercel, this decreases both the deployed code size and the number of Node.js `require` calls. We’ve measured up to **40% faster cold starts** paired with other improvements included in [Next.js 13.5](https://nextjs.org/blog/next-13-5).

### Link to headingRecursive Barrel Files

[The last change](https://github.com/vercel/next.js/pull/56489) we've made handles recursive barrel files, optimizing them into a single module. To test, we created [this module](https://unpkg.com/browse/recursive-barrel@1.0.0/) with 4 levels of 10 `export *` expressions, equaling 10,000 modules in total.

Before, this recursive package would take ~30 seconds to compile. After, it's just ~7s. We've seen 90% faster reloads from some [customers](https://github.com/vercel/next.js/pull/56489#issuecomment-1751099866) with over 100,000 modules.

## Link to headingConclusion

We recommend upgrading to the latest version of Next.js to see significant performance improvements in local dev performance and production cold starts. You might also consider adding [this ESLint rule](https://github.com/gajus/eslint-plugin-canonical#no-barrel-import) to prevent barrel file imports.

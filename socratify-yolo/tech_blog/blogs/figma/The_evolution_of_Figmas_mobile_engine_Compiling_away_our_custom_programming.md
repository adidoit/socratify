---
title: "The evolution of Figma’s mobile engine: Compiling away our custom programming language"
company: "figma"
url: "https://www.figma.com/blog/figmas-journey-to-typescript-compiling-away-our-custom-programming-language/"
content_length: 31850
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

May 1, 2024

# The evolution of Figma’s mobile engine: Compiling away our custom programming language

![](data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAUABQDASIAAhEBAxEB/8QAFwABAQEBAAAAAAAAAAAAAAAAAAcFBv/EACcQAAEEAQMDAwUAAAAAAAAAAAIAAQMEBQYRIQcSIhMxURQyQWFx/8QAFwEBAQEBAAAAAAAAAAAAAAAAAwIEBf/EAB0RAAICAwADAAAAAAAAAAAAAAECAAMREiEEMUH/2gAMAwEAAhEDEQA/AIxXnlOCMKlb1LMp7kZ/czLWvaNyNDGTZAclATOPNcT3Lb8sulh0zPpvsyGUrMNY5OwGd+dvn+LrIaMeWjkrx1K0bzC4xyM/L/G6wW3EPhfU6lXjq9WzSOwZE6kMcRVJBdm9mRb+d0xm6GROvKAG4s2xD7OyK9k+mEA4GAJWuoT/AF+AuBZ8hCFzH9OykPTS/Zl1ZTjOY3CNvFt+G4REdQlMSBKTnrMsmQcjLd+1kREJHYink//Z)![](https://cdn.sanity.io/images/599r6htc/regionalized/a7c01cb408b1e1583fd837cb4104e14805f20716-1364x1365.jpg?w=1364&h=1365&q=75&fit=max&auto=format)

Brandon LinSoftware Engineer

  * [Inside Figma](https://www.figma.com/blog/inside-figma/)
  * [Quality & performance](https://www.figma.com/blog/quality-and-performance/)
  * [Engineering](https://www.figma.com/blog/engineering/)
  * [Infrastructure](https://www.figma.com/blog/infrastructure/)
  * [Behind the scenes](https://www.figma.com/blog/behind-the-scenes/)
  * 


We’ve long written core parts of our mobile rendering architecture in Skew, the custom programming language we invented to squeeze additional performance out of our playback engine. Here’s how we automatically migrated Skew to TypeScript without disrupting a single day of development.

[Skew](https://evanw.github.io/skew-lang.org/) began as a side project in the early days of Figma. At the time, Skew fulfilled a critical need at Figma: to build out our prototype viewer with support on both the web and mobile. What started as a way to quickly spin this up became an entire compile-to-JavaScript programming language that enabled more advanced optimizations and faster compile times. But as we accumulated more and more code in Skew in the prototype viewer over the years, we slowly realized that it was difficult for new hires to ramp up on, couldn’t easily integrate with the rest of our codebase, and was missing a developer ecosystem outside of Figma. The pain of scaling it grew to outweigh its original advantages.

We recently finished migrating all Skew code at Figma to TypeScript, the industry standard language for the web. TypeScript is a sea change for the team and enables:

  * Streamlined integration with both internal and external code via static imports and native package management
  * A massive developer community that has built tools like linters, bundlers, and static analyzers
  * Modern JavaScript features like [async/await](https://javascript.info/async-await) and a more flexible type system
  * Seamless onboarding for new developers and lower friction for other teams



![A snippet of Skew code](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAKCAYAAAC0VX7mAAAACXBIWXMAABYlAAAWJQFJUiTwAAABcElEQVQokX2SW3KrMBAFvRKj0VsCyRiBHXv/++oUMje5qbjy0cUHVa0zZ+YkIohotIu4slDbyuPZ+LhXcvaIsQxKGIYz5/M3wzB8fYf/OO2yjnHYXBkvVz4ejeezUa8zLlfEhkOqfgmG90JBtMXEkVQq6zZ36bw2Yl2wqaJ9RlxEieF8fqV7x0n0kVCbPrZPmVJHrtdCvRTCOGFSwaSKTQVtPeorrWJQB0f6b2HvMXThNGUutVBKwaexJ7dxxMdMTJkYI9b5XoUOuac3xmPE/BTaEJkulaXN3LaVbbtR5oVUZkKeCCGQUiSlhPMR7RMmTi9swIg9hF0qOO+o10rbFu73O4/nk7auzMvCVArOOYwxaGNQIq9FiUbtKEENitP+U2vThdbZ3t+8XGht4bbdaK0xz3MfP+fc01lrUer9Yk7WHq/uQmMIwRNi6D3tgp19VO99l/VxnUMp1bf962z2cvcXrRGsFqRv7O9b+8e7w/4EAt4ey+16P6gAAAAASUVORK5CYII=)![A snippet of Skew code](https://cdn.sanity.io/images/599r6htc/regionalized/06e1934ce83f7d5429b8df3544fb46fc6961a0ae-766x406.png?w=528&h=280&q=75&fit=max&auto=format)

Left: A snippet of Skew code. 

![TypeScript code corresponding to this Skew code.](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAABUUlEQVQokX2S227rIBBF8yWxmRluxhgnbpJK7f//1jrCuSg9UvuwBTywtJjNwTlBRZlioc4buW7E9kHaLqTtRFgymgOjCsMwcDweX3meh2F45SAiiBN8yKT6QWw30nqlbFfy+Uw4N/xpQVNkdI5hHH8Ahv9yEFG6pVjESje6EJczuZ1JbSWsHdiwuaApIWaMHfpmenzLA+hwamia0bxgeSZMlTgv+FLQMu1AP8/4PKE+4FQZRRj7ao/96N6AcgdaWQnzidw2yrqRakWnhOSE5UwsdY+ljKSITBkpExIS6uwdqGiqxPVKvX7Tbt+0yye1z3GaEO8R87vd3dDudt4Yvd/vu26oavsM97ZjIbUL9fpFu32xdOB2IdeGzwUNj2L+KsV8YG9aBLWApUIoC2lu+9NCLq/YE/hLIXspPgTMBBOHOLcPtrf4XPs3+XH+w64b/gPWWwGi6qxINQAAAABJRU5ErkJggg==)![TypeScript code corresponding to this Skew code.](https://cdn.sanity.io/images/599r6htc/regionalized/2e168248e54bbe0ae652ce2023be7018c755c17a-866x408.png?rect=1,0,865,408&w=528&h=249&q=75&fit=max&auto=format)

Right: Typescript code corresponding to this Skew code.

This migration only recently became possible for three reasons:

  * More mobile browsers started to support WebAssembly
  * We replaced many core components of our Skew engine with the corresponding components from our C++ engine, which meant we wouldn’t lose as much performance if we moved to TypeScript
  * Team growth allowed us to allocate resources to focus on the developer experience



#### WebAssembly saw widespread mobile support and improved performance

When we first built Figma’s mobile codebase, mobile browsers didn’t support WebAssembly and couldn’t load large bundles in a performant way. This meant that it wasn’t possible to use our main C++ engine code (which would need to compile to WebAssembly). At the same time, TypeScript was in its infancy; it wasn’t the obvious choice compared to Skew, which had static types and a stricter type system [that allowed for advanced compiler optimizations](https://github.com/evanw/esbuild/issues/771#issuecomment-775546908). Fortunately, WebAssembly obtained widespread mobile support by 2018 and, according to our tests, reliable mobile performance by 2020.

#### Other performance improvements caught up to Skew’s optimizations

When we first started using Skew, there were a few key benefits: classic compiler optimizations, like constant folding and devirtualization, along with web-specific ones like generating JavaScript code with real integer operations. The longer we spent with these optimizations, the harder it was to justify a departure from a language we had cultivated for so long. For instance, in 2020, benchmarks indicated that loading Figma prototypes would’ve been nearly twice as slow using TypeScript in Safari, which was a blocker because Safari was (and still is*) the only browser engine allowed on iOS.

*In iOS 17.4, [Apple opened up its system to other browser engines for users in the EU](https://www.theverge.com/2024/1/25/24050478/apple-ios-17-4-browser-engines-eu). WebKit remains the only browser engine for other users around the world.

Some years after WebAssembly obtained widespread mobile support, we replaced many core components of our Skew engine with the corresponding components from our C++ engine. Since the components we replaced were the hottest code paths—like file loading—we wouldn’t lose as much performance if we moved to TypeScript. This experience gave us confidence that we could forego the advantages of Skew’s optimizing compiler.

#### Figma’s prototyping and mobile teams grew

In Figma’s earlier years, we couldn’t justify diverting resources to perform an automated migration because we were building as fast as possible with a small team. Scaling the prototyping and mobile teams into larger organizations afforded us the resources to do so.

## Converting the codebase

When we first prototyped this migration in 2020, our benchmarks showed that performance would be nearly twice as slow using TypeScript. Once we saw that WebAssembly support was good enough and moved the core of the mobile engine to C++, we fixed up our old prototype during our company [Maker Week](https://www.figma.com/blog/inside-maker-week-more-than-a-hackathon/). We demonstrated a working migration that passed all tests. Despite the thousands of developer experience issues and non-fatal type errors, we had a rough plan to migrate all of our Skew code safely.

Our goal was simple: convert the whole codebase to TypeScript. While we could have manually rewritten each file, we couldn’t afford to interrupt developer velocity to rewrite the entire codebase. More importantly, we wanted to avoid runtime errors and performance degradations for our users. While we ended up automating this migration, it wasn’t a quick switch. Unlike moving from another “JavaScript-with-types” language to TypeScript, Skew had actual semantic differences that made us uncomfortable with an immediate switch to TypeScript. For example, TypeScript only initializes namespaces and classes after we import a file, meaning we could run into runtime errors if we import the files in an unexpected order. By contrast, Skew makes every symbol available at runtime to the rest of the codebase upon loading, so these runtime errors wouldn’t be a problem.

Evan has said he took some learnings from this experience to make web bundler [esbuild](https://esbuild.github.io/).

We opted to gradually roll out a new code bundle generated from TypeScript so that there would be minimal disruptions to developer workflows. We developed a Skew-to-TypeScript transpiler that could take Skew code as input and output generated TypeScript code, building upon the work that Evan Wallace, Figma’s former CTO, started years ago.

#### Phase 1: Write Skew, build Skew

We kept the original build process intact, developed the transpiler, and checked in the TypeScript code to GitHub to show developers what the new codebase would look like.

![Developing a Typescript transpiler, alongside our original Skew pipeline](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAABYlAAAWJQFJUiTwAAACkElEQVQ4jY2TSW/TUBRG/T9iv+chiTM0JJBGoS1NS9UyJBTEUDEUSlMCaUuaxElcAhKjGCQEQkiAEGLNAoFYseQndMmfYM2y8kHPKSKqQGLxyVfy8/Hx9b2ap+t4EZ1OJBJ4uqRp5lmPV1iPz7Nhj9E2bDp6hI6u0zSz1JOL1DItVt0FWjKtnsPT9WDAiaCpQh3uCj1oWyPUsxuszHxhZe4rV0fv0nSK9ExBzzJpJCpUSx9YKm9xZfwtDWdqILMLGPRMGfRdk667L7hWuEv12BbVE9+pjb+iGS/hOxLfsWmMnGH50Dcunf5BdfoT12NzChgoIQVV0ZSy75j00w69eIKGW6G+t0s9f4P15AJtM63s6QrBRrRELX+P5fH3XM35NK3R0Go4WlvXWXMtVvIuK5kYa7ZDS7hhPOHQMYywh+qTGmaU5VSRxT1T1Nw8TWGF9zftGP1YEt+00dZMg+P7U0ycGqN0rMC5bJSW1OlJHd8W+LakJw08aXA57TA7m+PA8QLzE2lWo4JNJ8ajyTLPyxe5X5hCq9uCuakM2aVp8mcPcLKQoGlLfEuyGbPCqLptSxZGXUYXJshcPsjBQ/uoJSz6bpJnR87z+rzH48kK2obQuZBxODo5wvxYiqpr0RYG3V1pK8OUTXkixeFShrO5GNctQc+0uJ0t8qA4w61UDk39Ic80aMVN2lFJRwzGaLjRO7NGU+ioFqkokd8j1zEMuoYIa+2maQRPR8zgTcHhVd4OHiYkvjEA7ozDIDvg3fHUQvy5BtodR/Cu6PB5Nh58nInzMmdxQ/4BhhY7hn/L0AwODPvS2H6SlIECvchawf24oPc3w38kXLvBWQXdVj38qYquWr+hN/0vMFy7wdltxfoFjy/HtWPtFfAAAAAASUVORK5CYII=)![Developing a Typescript transpiler, alongside our original Skew pipeline](https://cdn.sanity.io/images/599r6htc/regionalized/23731112bed6116f1b3c08e5d80dc0716f93b10d-2160x1440.png?w=804&h=536&q=75&fit=max&auto=format)

Developing a Typescript transpiler, alongside our original Skew pipeline

#### Phase 2: Write Skew, build TypeScript

Once we generated a TypeScript bundle that passed all of our unit tests, we started rolling out production traffic to build from the TypeScript codebase directly. In this phase, developers still wrote Skew, and our transpiler transpiled their code into TypeScript and updated TypeScript code living in GitHub. Additionally, we continued to fix type errors in the generated code; TypeScript could still generate a valid bundle even if there were type errors!

![Rolling out production traffic to the TypeScript codebase that our TypeScript compiler generated from Skew source code](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAABYlAAAWJQFJUiTwAAAC3klEQVQ4jY2TW28bRRiG90dwiLKzR9u7dmLHxcYNaWKnbWjTEOOIcCgNVcAJjbGpD2s7qRNQD0AIBJU2SoVKuMh9JYQEEhIIkIrUG6Re8hf4BVxG86BZW4VyAxevZrTz6pl3v+8bLRCCQBe0dV0GwqJhZ6l589S8EnV3gpYZpe4cZ21khUupBlWvSNdMsSOm2BUzbIo4gdBlWwiUNAVsGwYdU8iWk6SSrrNy+htWznzPWu4qTb/Au2NvUJ75jjfnfuPt4x/zvvsC90Sbb/Xr7OgFAhVG19UaAmXXtmTPt+n4WbmWu0a5+JDywu9cmrxDY+QstUyFt+Yfsrz4B6v5u3wQu8DPw7d4MHTIbaMoe7EEW4kxueHGpNbWddYjNr3RCF0vzmV/nsozHSqZHrXEqzSdNJf9OVZzu5QnDqiMvcN2pMRPQ5/z65Nfse++zCenFri9sMqH4zNoLSGo+g4rWZ9yKkbVjdA0fVpWnMBwCYRJzfFZHj3BxVSBNS/Ntj3Nj0/f5P4TX7IffYXPzp5n/7U621NzaFXboPTcCJOLExSKOV5PR2k5Bhuuybpr0nJMltIxTp3LkC/mWBz3ue4W+GVojwdPHbJnlHgvmeFaZpJNP4lWcU3OTKdIL58ke36Kl3JxmlGbKzGHjahDI2pTOjHKsQsF0hdPMjudYis6yQ/Dn3J/+C439dmwu21h9LtcNwVLqQhz+SQvToxQ9h1apup6X03bCM9n80nO5ZPhfsNKciCWOBSr3BDPht1VausCTVED26Dp2bSiFm1T3dY3hBKCumlQdQxUeRqGoCNMNoXPlkjQFbaaw0FKgbZpG3I3acsvchHuZF35Udxi3VDDPjCFNz+u4HHJvk9INeDa1YjJwXiEr5/35L3THnvHHK5YfwPDl/QvDQCPUinQo1/uWcbRTsKSCnQr7cgbnkn3nwn/Q+phDLwq6ZGq4Z9q0xGqNuHHvvF/AhVo4D1SrL8AdT3VAn2csmIAAAAASUVORK5CYII=)![Rolling out production traffic to the TypeScript codebase that our TypeScript compiler generated from Skew source code](https://cdn.sanity.io/images/599r6htc/regionalized/f1745cf9837b710dde20a0551ac6881e496b24fd-2160x1440.png?w=804&h=536&q=75&fit=max&auto=format)

Rolling out production traffic to the TypeScript codebase that our TypeScript compiler generated from Skew source code

#### Phase 3: Write TypeScript, build TypeScript

Once everyone went through the TypeScript build process, we needed to make the TypeScript code the source of truth for development. After identifying a time when no one was merging code, we cut off the auto-generation process and deleted the Skew code from the codebase, effectively requiring that developers write code in TypeScript.

![Making the cutover to use the Typescript codebase as the source of truth for developers](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAABYlAAAWJQFJUiTwAAACYUlEQVQ4jZWTS08TURTH53M49zW3ZdpSxhJK5SEPrQhBHj5AiRINLVRIywwz0ycRA9GgMW4wYqILt67EnUs/Aku/hGuW5P7NTJvSKIa4+GUm55z533P/54zmEYIQXVce4XBEGkVzBkVzDrYcgkslfF0PaxyRwnpiGWvWFjbi97HFk/ApRT1iqu1YElUjAs0nJAyWGVGu0YP1lI189hvyN7+j0L8LR15BmRL4jGMzPoPc2Bc8mT7G6tVPsKPjqEVNvL42rw7m83gxkA0FVU0Y6pkZRSWWUU8zu8jNHiN3+yfWhg/hdI2iIijKQqCUXMTK5A88XviFfPYIdmwSjVhCvZ1awuGSo/ZHppXm6wR1KfE8GUfDtGDH5rCRrmCjv4Fi9wO4ItnqkMGOjmEtvYeV4c8o9FbhyAwqQmDHSmMvPYrtuAXNJQQlU6LQ142CFUdJdsEVcXhGAh6LwCMUPml66NIIHNGHTWMIDk/BI0aY84MaGtQRaEXBcG+gB9fvjCJ7axAPU4EgQZUH3urBsMLCYDBNLnWgh/lOtHXJMDV2GZnlCQwvjmMhnYBjcFQEC0/1dBIKev/A/wPNZhSPrChmRyzcHezBqinhcooyDwTDdWoKtlbnL0G9GW8LhvvFKEqSYdNg8BlFTTDUJUOVNX35HzRf11WwOmVKUeNUvUpwHPZLfMhE8CYp0OD0zMfzUR1PpbWvRIlqGAzv+yS+3jBxNGHiYyaCHXmhYCjWHoqn66dhgBBUGVEvYxwHKQPveg3sxznq/MzH8/BaYq0OT4M/5SR46Qii3KL90QVXbuWDxk5+A+EYx0xV1zWHAAAAAElFTkSuQmCC)![Making the cutover to use the Typescript codebase as the source of truth for developers](https://cdn.sanity.io/images/599r6htc/regionalized/2721f0f0937fa5609e35d23b4cab6c47237cf3e6-2160x1440.png?w=804&h=536&q=75&fit=max&auto=format)

Making the cutover to use the Typescript codebase as the source of truth for developers

This was a solid approach. Having full control over the workings of the Skew compiler meant we could use it to make Phase 1 much easier; we could add and modify parts of the Skew compiler with complete freedom to satisfy our needs. Our gradual rollout also ended up paying dividends. For example, we internally caught a breakage with our Smart Animate feature as we were rolling out TypeScript. Our gated approach allowed us to quickly turn off the rollout, fix the breakage, and rethink how to proceed with our rollout plan.

We also gave ample notice about the cutover to use TypeScript. On a Friday night, we merged all the necessary changes to remove the auto-generation process and to make all of our continuous integration jobs run off the TypeScript files directly.

## A note on our transpiler work

If you don’t know how compilers work, here’s a bird’s-eye view: A compiler itself consists of a frontend and a backend. The frontend is responsible for parsing and understanding the input code and performing things like type-checking and syntax checking. The frontend then converts this code to an**** intermediate representation (IR), a data structure that fully captures the original semantics and logic of the original input code, but structured so that we don’t need to worry about re-parsing the code.

The backend of the compiler is responsible for turning this IR into a variety of different languages. In a language like C, for example, one backend would typically generate assembly/machine code, and in the Skew compiler, the backend generates mangled and minified JavaScript.

A **transpiler** is a special type of compiler whose backends produce human-readable code rather than mangled machine-like code; in our case, the backend would need to take the Skew IR and produce human-readable TypeScript.

The process of writing the **transpiler** was relatively straightforward in the beginning: We borrowed a lot of inspiration from the JavaScript backend with the appropriate code to generate based on the information we encountered in the IR. At the tail end we ran into several issues that were trickier to track down and deal with:

  * **Performance issues with array destructuring:** Moving away from JavaScript array destructuring yielded up to 25% in performance benefits.
  * **Skew’s “devirtualization” optimization:** We took extra steps during the rollout to make sure devirtualization, a compiler optimization, did not break our codebase’s behavior.
  * **Initialization order matters in TypeScript:** Symbol ordering in TypeScript matters as opposed to Skew, so our transpiler needed to generate code that respected this ordering.



##### Performance issues with array destructuring

When investigating offline performance differences between Skew and TypeScript in some sample prototypes, we noticed that the frame rate was lower in TypeScript. After much investigation, we found out the root cause was array destructuring–which, it turns out, is rather slow in JavaScript.

To complete an operation like `const [a, b] = function_that_returns_an_array()`, JavaScript constructs an iterator that iterates through the array instead of directly indexing from the array, which is slower. We were doing this to retrieve arguments from JavaScript’s `arguments` keyword, resulting in slower performance on certain test cases. The solution was simple: We generated code to directly index the arguments array instead of destructuring, and improved per-frame latency by up to 25%!

##### Skew’s “devirtualization” optimization

Check out [this post](https://marcofoco.com/blog/2016/10/03/the-power-of-devirtualization/) to learn more about devirtualization.

Another issue was divergent behavior between how TypeScript and Skew deal with class methods, which caused the aforementioned breakage in Smart Animate during our rollout. The Skew compiler does something called **devirtualization** , which is when–under certain conditions–a function gets pulled out of a class as a performance optimization and gets hoisted to a global function:

JavaScript
    
    
    myObject.myFunc(a, b)
    // becomes...
    myFunc(myObject, a, b)

This optimization happens in Skew but not TypeScript. The Smart Animate breakage happened because `myObject` was null, and we saw different behaviors–the devirtualized call would run fine but the non-devirtualized call would result in null access exception. This made us worry if there were other such call sites that had the same problem.

To assuage our worries, we added logging in all functions that would partake in devirtualization to see if this problem had ever occurred in production. After enabling this logging for a brief period of time, we analyzed our logs and fixed all problematic call sites, making us more confident in the robustness of our TypeScript code.

##### Initialization order matters in TypeScript

A third issue we encountered is how each respective language honors initialization order. In Skew, you can declare variables, classes and namespaces, and function definitions anywhere in code and it won’t care about the order in which they are declared. In TypeScript, however, it _does_ matter whether you initialize global variables or class definitions first; initializing static class variables before the class definition is a compile-time error.

Our initial version of the transpiler got around this by generating TypeScript code without using namespaces, effectively flattening every single function into the global scope. This maintained similar behavior to Skew, but the resulting code was not very readable. We reworked parts of the transpiler to emit TypeScript code in the proper order for clarity and accuracy, and added back TypeScript namespaces for readability.

Despite these challenges, we eventually built a transpiler that passed all of our unit tests and produced compiling TypeScript code that matched Skew’s performance. We opted to fix some small issues either manually in Skew source code, or once we cut over to TypeScript—rather than writing a new modification to the transpiler to fix them. While it would be ideal for all fixes to live in the transpiler, the reality is that some changes weren’t worth automating and we could move faster by fixing some issues this way.

## Case study: Keeping developers happy with source maps

Throughout this process, developer productivity was always top of mind. We wanted to make the migration to TypeScript as easy as possible, which meant doing everything we could to avoid downtime and create a seamless debugging experience.

Web developers primarily debug with debuggers supplied by modern web browsers; you set a _breakpoint_ in your source code and when the code reaches this point, the browser will pause and developers can inspect the state of the browser’s JavaScript engine. In our case, a developer would want to set breakpoints in Skew or TypeScript (depending on which phase of the project we were in).

But the browser itself can only understand JavaScript, while breakpoints are actually set in Skew or TypeScript. How does it know where to stop in the compiled JavaScript bundle given a breakpoint in source code? Enter: source maps, the way a browser knows how to link together compiled code to source code. Let’s look at a simple example with this Skew code:

Plain text
    
    
    def helper() {
      return [1, 3, 4, 5];
    }
    
    def myFunc(myInt int) int {
      var arrayOfInts List<int> = helper();
      return arrayOfInts[0] + 1;
    }

This code might get compiled and minified down to the following JavaScript:

JavaScript
    
    
    function c(){return [1,3,4,5];}function myFunc(a){let b=c();return b[0]+1;}

This syntax is hard to read. Source maps map sections of the generated JavaScript back to specific sections of the source code (in our case, Skew). A source map between the code snippets would show mappings between:

  * `helper → c`
  * `myInt → a`
  * `arrayOfInts → b`



Check out [this article on source maps](https://web.dev/articles/source-maps) for more technical details on generating, understanding, and debugging source maps.

A source map normally will have file extension `.map`. One source map file will associate with the final JavaScript bundle so that, given a code location in the JavaScript file, the source map for our JavaScript bundle would tell us:

  * The Skew file this section of JavaScript came from
  * The code location within this Skew file that corresponds to this portion of JavaScript



Whenever a developer sets a debugger breakpoint in Skew, the browser simply reverses this source map, looks up the portion of JavaScript that this Skew line corresponds to, and sets a breakpoint there.

Here’s how we applied this to our TypeScript migration: Our original infrastructure generated Skew to JavaScript source maps that we used for debugging. However, in Phase 2 of our migration, our bundle generation pipeline was completely different, generating TypeScript followed by bundling with esbuild. If we tried to use the same source maps from our original infrastructure, we would get incorrect mappings between JavaScript and Skew code, and developers would be unable to debug their code while we’re in this phase.

We needed to generate new source maps using our new build process. This involved three pieces of work, illustrated below:

![Diagram of generating new sourcemaps using our new build process](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAABYlAAAWJQFJUiTwAAAC0klEQVQ4jV2SS28cRRSF5xewQCBhdVc/pvpR3T0943gsJwInEykbyIYIpCyysoSDHdsz/ZrumfGQRFlESCyQEELKDvgX/LAsrfpQ9RiCWJSOSvfWrXPPOYN1qNhmY9ax0q10qWXCi+Qpp6MzLtQDylhRJikXmeJSSRrp8uPRHn88/ZhfHn9GNwooVaovU8VpGjB4Ob7D2y9mvD6Y6k0iWWaHnB/9wHf333E1+ZYuzVlnY+okoYol63TIb1/t8dfqI/48+ZSXBzHrZKKbJOUylAy26Ui/Obyrt6OcTnq6CUfM75wwv9dQ5I/oVMomGdGEEdXQowtcfjq2+P3ZJ/z8eI9NHul1mtOqRC+Gvh60/pBVEGGwtm0q4VMGRxTxjCIY0ciALgipfJ/CEdTCZjUUXKeCNhZU0qeJQqpgyMJ1GGziBLP2Okr6gYUTc5484/lkwZV6SBsqVqYmg35gZVnUlk1l25SGgCtopEftu5TCvtXweNYPbYTNwh3z/XTL8wfvmO9/wyrJuU7GLMOY0nWobKv/uDZoWTSOoJUeS8/p7z3DV5MDDJrG0glZZE9YTE8o089pI8Uq/g9D+wPDnq0jaAOPZnjLsBtK1pGi9eW/GhbyHvPoIQuZ00hJKz9oaAb1feZzIXqjGhVQxJKLwGdwnY54c3gXg2blwkk5y885PXzNVfYlXZyyjjMaY4zn0nhOv17jOztDYkWXjSjThBfxLof67fFM32qoCzfnfLribPYri/0nrNKcTTphGStq6WHC3xkMPepImljp62yfNsn0XA71wERmm41YBaHuNRSSUj2inHxNoabUUcxSKcpAUhrhHUHjCmpXUPoudRjSJaluooiF7zKobXHTCKFrIYw2utdIuNSOR+k4FK5D6bkUZkCv3c7dnYa2qevS90yPLhxxM6hs631t2zcmBpVladPcP+gf/f/sDPnHlN2x9G39prLt938DCJ3JCMpcUhgAAAAASUVORK5CYII=)![Diagram of generating new sourcemaps using our new build process](https://cdn.sanity.io/images/599r6htc/regionalized/286fc5900a860382eb604f2b2831e567cfd74ca6-2160x1440.png?w=804&h=536&q=75&fit=max&auto=format)

Diagram of generating new sourcemaps using our new build process

**Step 1** : Generate a TypeScript → JavaScript source map `ts-to-js.map`. esbuild can automatically generate this map when it generates the JavaScript bundle.

**Step 2** : Generate a Skew → TypeScript source map for each Skew source file. If we name the file `file.sk`, the transpiler will name the source map `file.map`. By emulating how the Skew → JavaScript backend of the Skew compiler creates source maps, we implemented this in our TypeScript transpiler.

**Step 3** : Compose these source maps together to yield a map from Skew to JavaScript. For this, we implemented the following logic in our build process:

For each entry `E` in `ts-to-js.map`:

  * Determine which TypeScript file this entry maps into and open its source map, `fileX.map`.
  * Look up the TypeScript code location from `E` in this source map, `fileX.map`, to obtain the code location in the corresponding Skew file `fileX.sk`.
  * Add this as a new entry in our final source map: the JavaScript code location from `E` combined with the Skew code location.



With our final source map handy, we could now map our new JavaScript bundle to Skew without disrupting the developer experience.

## Case study: Conditional compilation

In Skew, top-level “if” statements allow for conditional code compilation, and we specify the conditions using compile-time constants via a “defines” option passed to the Skew compiler. We can use this to define multiple build targets—which bundle in different parts of the code—for a given codebase, so we can have different bundles for different ways of using the same codebase. For example, one bundle variant could be the actual bundle that’s deployed to users, and another could be one used only for unit testing. This allows us to specify that certain functions or classes use different implementations in debug or release builds.

To be more explicit, the following Skew code defines a different implementation for a `TEST` build:

Plain text
    
    
    if BUILD == "TEST" {
      class HTTPRequest {
        def send(body string) HTTPResponse {
          # test-only implementation...
        }
    
        def testOnlyFunction {
          console.log("hi!")
        }
      }
    } else {
      class HTTPRequest {
        def send(body string) HTTPResponse {
          # real implementation...
        }
      }
    }

This would compile to the following JavaScript when passing a `BUILD: "TEST"` definition to the Skew compiler:

JavaScript
    
    
    function HTTPRequest() {}
    HTTPRequest.prototype.send = function(body) {
      // test-only implementation...
    }
    
    HTTPRequest.prototype.testOnlyFunction = function(body) {
      console.log("hi!")
    }

However, conditional compilation is not part of TypeScript. Instead, we had to perform the conditional compilation in the build step _after_ type-checking, as part of the bundling step using esbuild’s “defines” and dead code elimination features. The defines could therefore no longer influence type-checking, meaning code like the above example where the method `testOnlyFunction` is only defined in the `BUILD: "TEST"` build could not exist in Typescript.

We fixed this problem by converting the above Skew code to the following TypeScript code:

JavaScript
    
    
    // Value defined during esbuild step
    declare const BUILD: string
    
    class HTTPRequest {   
      send(body: string): HTTPResponse {
        if (BUILD == "TEST") {
          // test-only implementation...
        } else {
          // real implementation...
        }
      }
      
      testOnlyFunction() {
        if (BUILD == "TEST") {
          console.log("hi!")
        } else {
          throw new Error("Unexpected call to test-only function")
        }
      }
    }

This compiles to the same JavaScript code that the original Skew code also directly compiled to:

JavaScript
    
    
    function HTTPRequest() {}
    HTTPRequest.prototype.send = function(body) {
      // test-only implementation...
    }
    HTTPRequest.prototype.testOnlyFunction = function(body) {
      console.log("hi!")
    }

Unfortunately, our final bundle was now slightly larger. Some symbols that were originally only available in one compile-time mode became present in all modes. For example, we only used `testOnlyFunction` when the build mode `BUILD` was set to `"TEST"`, but after this change the function was always present in the final bundle. In our testing, we found this increase in bundle size to be acceptable. We were still be able to remove unexported top-level symbols, though, via [tree-shaking](https://en.wikipedia.org/wiki/Tree_shaking).

## A new era of prototyping development, now in TypeScript

By migrating all Skew code to TypeScript, we modernized a key codebase at Figma. Not only did we pave the way for it to integrate much more easily with internal and external code, developers are working more efficiently as a result. Writing the codebase initially in Skew was a good decision given the needs and capabilities of Figma at the time. However, technologies are constantly improving and we learned to never doubt the rate at which they mature. Even though TypeScript may not have been the right choice back then, it definitely is now.

We want to reap all the benefits of moving to TypeScript, so our work doesn’t stop here. We’re exploring a number of future possibilities: integration with the rest of our codebase, significantly easier package management, and direct use of new features from the active TypeScript ecosystem. We learned a lot about different facets of TypeScript—like import resolutions, module systems, and JavaScript code generation—and we can’t wait to put those learnings to good use.

_We would like to thank Andrew Chan, Ben Drebing, and Eddie Shiang for their contributions to this project. If work like this appeals to you, come[work with us at Figma](https://www.figma.com/careers/#job-openings)!_

## Subscribe to Figma’s editorial newsletter

Enter email*

I agree to opt-in to Figma's mailing list.*

By clicking “Submit” you agree to our [TOS](https://www.figma.com/tos/) and [Privacy Policy](https://www.figma.com/privacy/).

## Create and collaborate with Figma

[Get started for free](https://www.figma.com/signup)

---
title: "Enabling Kotlin incremental compilation on Buck2"
author: "Iveta Kovalenko"
url: "https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/"
date: "2025-09-15"
---

![](https://engineering.fb.com/wp-content/uploads/2025/08/kotlin-thumb.png)

By [Iveta Kovalenko](https://engineering.fb.com/author/iveta-kovalenko/ "Posts by Iveta Kovalenko")

The Kotlin incremental compiler has been a true gem for developers chasing faster compilation since its introduction in build tools. Now, we’re excited to bring its benefits to [Buck2](https://buck2.build/) – Meta’s build system – to unlock even more speed and efficiency for Kotlin developers.

Unlike a traditional compiler that recompiles an entire module every time, an incremental compiler focuses only on what was changed. This cuts down compilation time in a big way, especially when modules contain a large number of source files.

Buck2 promotes small modules as a key strategy for achieving fast build times. Our codebase followed that principle closely, and for a long time, it worked well. With only a handful of files in each module, and Buck2’s support for fast incremental builds and parallel execution, incremental compilation didn’t seem like something we needed.

But, let’s be real: Codebases grow, teams change, and reality sometimes drifts away from the original plan. Over time, some modules started getting bigger – either from legacy or just organic growth. And while big modules were still the exception, they started having quite an impact on build times.

So we gave the Kotlin incremental compiler a closer look – and we’re glad we did. The results? Some**critical modules now build up to 3x faster**. That’s a big win for developer productivity and overall build happiness.

Curious about how we made it all work in Buck2? Keep reading. We’ll**walk you through the steps we took to bring the Kotlin incremental compiler to life**in our Android toolchain.

## Step 1: Integrating Kotlin’s Build Tools API

As of Kotlin 2.2.0, the only guaranteed public contract to use the compiler is through the command-line interface (CLI). But since the CLI doesn’t support incremental compilation (at least for now), it didn’t meet our needs. Alternatively, we could integrate the Kotlin incremental compiler directly via the internal compiler’s components – APIs that are technically accessible but not intended for public use. However, relying on them would’ve made our toolchain fragile and likely to break with every Kotlin update since there’s no guarantee of backward compatibility. That didn’t seem like the right path either.

Then we came across the Build Tools API ([KEEP](https://github.com/Kotlin/KEEP/issues/421)), introduced in Kotlin 1.9.20 as the official integration point for the compiler – including support for incremental compilation. Although the API was still marked as experimental, we decided to give it a try. We knew it would eventually stabilize, and saw it as a great opportunity to get in early, provide feedback, and help shape its direction. Compared to using internal components, it offered a far more sustainable and future-proof approach to integration.

### ⚠️ Depending on kotlin-compiler? Watch out!

In the Java world, a _shaded_ library is a modified version of the library where the class and package names are changed. This process – called shading – is a handy way to avoid classpath conflicts, prevent version clashes between libraries, and keeps internal details from leaking out.

Here’s quick example:

* Unshaded (original) class: com.intellij.util.io.DataExternalizer
* Shaded class: org.jetbrains.kotlin.com.intellij.util.io.DataExternalizer

The Build Tools API depends on the _shaded_ version of the Kotlin compiler (kotlin-compiler-embeddable). But our Android toolchain was historically built with the _unshaded_ one (kotlin-compiler). That mismatch led to java.lang.NoClassDefFoundError crashes when testing the integration because the shaded classes simply weren’t on the classpath.

Replacing the unshaded compiler across the entire Android toolchain would’ve been a big effort. So to keep moving forward, we went with a quick workaround: We unshaded the Build Tools API instead. 🙈 Using the [jarjar](https://github.com/google/jarjar) library, we stripped the org.jetbrains.kotlin prefix from class names and rebuilt the library.

Don’t worry, once we had a working prototype and confirmed everything behaved as expected, we circled back and did it right – fully migrating our toolchain to use the shaded Kotlin compiler. That brought us back in line with the API’s expectations and gave us a more stable setup for the future.

## Step 2: Keeping previous output around for the incremental compiler

To compile incrementally, the Kotlin compiler needs access to the output from the previous build. Simple enough, but Buck2 deletes that output by default before rebuilding a module.

With [incremental actions](https://buck2.build/docs/rule_authors/incremental_actions/), you can configure Buck2 to skip the automatic cleanup of previous outputs. This gives your build actions access to everything from the last run. The tradeoff is that it’s now up to you to figure out what’s still useful and manually clean up the rest. It’s a bit more work, but it’s exactly what we needed to make incremental compilation possible.

## Step 3: Making the incremental compiler cache relocatable

At first, this might not seem like a big deal. You’re not planning to move your codebase around, so why worry about making the cache relocatable, right?

Well… that’s until you realize you’re no longer in a tiny team, and you’re definitely not the only one building the project. Suddenly, it does matter.

Buck2 supports [distributed builds](https://buck2.build/docs/users/remote_execution/), which means your builds don’t have to run only on your local machine. They can be executed elsewhere, with the results sent back to you. And if your compiler cache isn’t relocatable, this setup can quickly lead to trouble – from conflicting overloads to strange ambiguity errors caused by mismatched paths in cached data.

So we made sure to configure the root project directory and the build directory explicitly in the incremental compilation settings. This keeps the compiler cache stable and reliable, no matter who runs the build or where it happens.

## Step 4: Configuring the incremental compiler

In a nutshell, to decide what needs to be recompiled, the Kotlin incremental compiler looks for changes in two places:

* Files within the module being rebuilt.
* The module’s dependencies.

Once the changes are found, the compiler figures out which files in the module are affected – whether by direct edits or through updated dependencies – and recompiles only those.

To get this process rolling, the compiler needs just a little nudge to understand how much work it really has to do.

So let’s give it that nudge!

### Tracking changes inside the module

When it comes to tracking changes, you’ve got two options: You can either let the compiler do its magic and detect changes automatically, or you can give it a hand by passing a list of modified files yourself. The first option is great if you don’t know which files have changed or if you just want to get something working quickly (like we did during prototyping). However, if you’re on a Kotlin version earlier than 2.1.20, you have to provide this information yourself. Automatic source change detection via the Build Tools API isn’t available prior to that. Even with newer versions, if the build tool already has the change list before compilation, it’s still worth using it to optimize the process.

This is where Buck’s incremental actions come in handy again! Not only can we preserve the output from the previous run, but we also get hash digests for every action input. By comparing those hashes with the ones from the last build, we can generate a list of changed files. From there, we pass that list to the compiler to kick off incremental compilation right away – no need for the compiler to do any change detection on its own.

### Tracking changes in dependencies

Sometimes it’s not the module itself that changes, it’s something the module depends on. In these cases, the compiler relies on classpath snapshot. These snapshots capture the Application Binary Interface (ABI) of a library. By comparing the current snapshots to the previous one, the compiler can detect changes in dependencies and figure out which files in your module are affected. This adds an extra layer of filtering on top of standard compilation avoidance.

In Buck2, we added a dedicated action to generate classpath snapshots from library outputs. This artifact is then passed as an input to the consuming module, right alongside the library’s compiled output. The best part? Since it’s a separate action, it can be run remotely or be pulled from cache, so your machine doesn’t have to do the heavy lifting of extracting ABI at this step.

![](https://engineering.fb.com/wp-content/uploads/2025/08/classpath-snapshots-for-abi-4.png)

If, after all, only your module changes but your dependencies do not, the API also lets you skip the snapshot comparison entirely if your build tool handles the dependency analysis on its own. Since we already had the necessary data from Buck2’s incremental actions, adding this optimization was almost free.

## Step 5: Making compiler plugins work with the incremental compiler

One of the biggest challenges we faced when integrating the incremental compiler was making it play nicely with our custom compiler plugins, many of which are important to our build optimization strategy. This step was necessary for unlocking the full performance benefits of incremental compilation, but it came with two major issues we needed to solve.

### 🚨 Problem 1: Incomplete results

As we already know, the input to the incremental compiler does not have to include all Kotlin source files. Our plugins weren’t designed for this and ended up producing incomplete results when run on just a subset of files. We had to make them incremental as well so they could handle partial inputs correctly.

![](https://engineering.fb.com/wp-content/uploads/2025/08/incremental-compiler.png)

### 🚨 Problem 2: Multiple rounds of Compilation

The Kotlin incremental compiler doesn’t just recompile the files that changed in a module. It may also need to recompile other files in the same module that are affected by those changes. Figuring out the exact set of affected files is tricky, especially when circular dependencies come into play. To handle this, the incremental compiler approximates the affected set by compiling in multiple rounds within a single build.

_💡Curious how that works under the hood? The_[ _Kotlin blog on fast compilation_](https://blog.jetbrains.com/kotlin/2020/09/the-dark-secrets-of-fast-compilation-for-kotlin/) _has a great deep dive that’s worth checking out._

This behavior comes with a side effect, though. Since the compiler may run in multiple rounds with different sets of files, compiler plugins can also be triggered multiple times, each time with a different input. That can be problematic, as later plugin runs may override outputs produced by earlier ones. To avoid this, we updated our plugins to accumulate their results across rounds rather than replacing them.

![](https://engineering.fb.com/wp-content/uploads/2025/08/multiple-rounds.png)

## Step 6: Verifying the functionality of annotation processors

Most of our annotation processors use Kotlin Symbol Processing (KSP2), which made this step pretty smooth. KSP2 is designed as a standalone tool that uses the Kotlin Analysis API to analyze source code. Unlike compiler plugins, it runs independently from the standard compilation flow. Thanks to this setup, we were able to continue using KSP2 without any changes.

_💡 Bonus: KSP2 comes with its own built-in incremental processing support. It’s fully self-contained and doesn’t depend on the incremental compiler at all._

Before we adopted KSP2 (or when we were using an older version of the Kotlin Annotation Processing Tool (KAPT), which operates as a plugin) our annotation processors ran in a separate step dedicated solely to annotation processing. That step ran before the main compilation and was always non-incremental.

## Step 7: Enabling compilation against ABI

To maximize cache hits, Buck2 builds Android modules against the class ABI instead of the full JAR. For Kotlin targets, we use the jvm-abi-gen compiler plugin to generate class ABI during compilation.

But once we turned on incremental compilation, a couple of new challenges popped up:

1. The jvm-abi-gen plugin currently lacks direct support for incremental compilation, which ties back to the issues we mentioned earlier with compiler plugins.
2. ABI extraction now happens twice – once during compilation via jvm-abi-gen, and again when the incremental compiler creates classpath snapshots.

In theory, both problems could be solved by switching to full JAR compilation and relying on classpath snapshots to maintain cache hits. While that could work in principle, it would mean giving up some of the build optimizations we’ve already got in place – a trade-off that needs careful evaluation before making any changes.

For now, we’ve implemented a custom (yet suboptimal) solution that merges the newly generated ABI with the previous result. It gets the job done, but we’re still actively exploring better long-term alternatives.

Ideally, we’d be able to reuse the information already collected for classpath snapshot or, even better, have this kind of support built directly into the Kotlin compiler. There’s an open ticket for that: [KT-62881](https://youtrack.jetbrains.com/issue/KT-62881/Pass-to-the-compilation-only-ABI-snapshot-of-the-classpath). Fingers crossed!

## Step 8: Testing

Measuring the impact of build changes is not an easy task. Benchmarking is great for getting a sense of a feature’s potential, but it doesn’t always reflect how things perform in “the real world.” Pre/post testing can help with that, but it’s tough to isolate the impact of a single change, especially when you’re not the only one pushing code.

We set up A/B testing to overcome these obstacles and measure the true impact of the Kotlin incremental compiler on Meta’s codebase with high confidence. It took a bit of extra work to keep the cache healthy across variants, but it gave us a clean, isolated view of how much difference the incremental compiler really made at scale.

We started with the largest modules – the ones we already knew were slowing builds the most. Given their size and known impact, we expected to see benefits quickly. And sure enough, we did.

## The impact of incremental compilation

The graph below shows early results on how enabling incremental compilation for selected targets impacts their local build times during incremental builds over a 4-week period. This includes not just compilation, but also annotation processing, and a few other optimisations we’ve added along the way.

With incremental compilation, we’ve seen about a 30% improvement for the average developer. And for modules without annotation processing, the speed nearly doubled. That was more than enough to convince us that the incremental compiler is here to stay.

![](https://engineering.fb.com/wp-content/uploads/2025/08/kotlin-modules.png)

## What’s next

Kotlin incremental compilation is now supported in Buck2, and we’re actively rolling it out across our codebase! For now, it’s available for internal use only, but we’re working on bringing it to the recently introduced [open source](https://github.com/facebook/buck2) toolchain as well.

But that’s not all! We’re also exploring ways to expand incrementality across the entire Android toolchain, including tools like Kosabi (the Kotlin counterpart to [Jasabi](https://engineering.fb.com/2017/11/09/android/rethinking-android-app-compilation-with-buck/)), to deliver even faster build times and even better developer experience.

To learn more about Meta Open Source, visit our [open source site](https://opensource.fb.com/), subscribe to our [YouTube channel](https://www.youtube.com/channel/UCCQY962PmHabTjaHv2wJzfQ), or follow us on [Facebook](https://www.facebook.com/MetaOpenSource), [Threads](https://www.threads.net/@metaopensource), [X](https://x.com/MetaOpenSource) and [LinkedIn](https://www.linkedin.com/showcase/meta-open-source?fbclid=IwZXh0bgNhZW0CMTEAAR2fEOJNb7zOi8rJeRvQry5sRxARpdL3OpS4sYLdC1_npkEy60gBS1ynXwQ_aem_mJUK6jEUApFTW75Emhtpqw).

### Share this:

* [ Click to share on Facebook (Opens in new window) Facebook ](https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/?share=facebook)
* [ Click to share on Threads (Opens in new window) Threads ](https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/?share=custom-1706294701)
* [ Click to share on X (Opens in new window) X ](https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/?share=x)
* [ Click to share on LinkedIn (Opens in new window) LinkedIn ](https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/?share=linkedin)
* [ Click to share on Hacker News (Opens in new window) Hacker News ](https://engineering.fb.com/2025/08/26/open-source/enabling-kotlin-incremental-compilation-on-buck2/?share=custom-1699562127)
* [ Click to email a link to a friend (Opens in new window) Email ](mailto:?subject=%5BShared%20Post%5D%20Enabling%20Kotlin%20incremental%20compilation%20on%20Buck2&body=https%3A%2F%2Fengineering.fb.com%2F2025%2F08%2F26%2Fopen-source%2Fenabling-kotlin-incremental-compilation-on-buck2%2F&share=email)
*

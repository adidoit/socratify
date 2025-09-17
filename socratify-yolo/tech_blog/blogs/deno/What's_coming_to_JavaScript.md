---
title: "What's coming to JavaScript"
author: "Unknown"
url: "https://deno.com/blog/updates-from-tc39"
date: "2025-09-15"
---

# What's coming to JavaScript

June 26, 2025[](/feed "Atom Feed")

* [![](https://github.com/lucacasonato.png)Luca Casonato](https://github.com/lucacasonato)
* [![](https://github.com/lambtron.png)Andy Jiang](https://github.com/lambtron)

* [Engineering](/blog?tag=engineering)

Deno is a JavaScript company, and we believe JavaScript should be simple, powerful, and fun. Deno aims to modernize JavaScript and its tooling, with [native TypeScript support](https://docs.deno.com/runtime/fundamentals/typescript/), and bridging the gap between server-side and browser JavaScript with [web standard APIs](https://docs.deno.com/runtime/reference/web_platform_apis/). As such, we’re very invested in advancing the JavaScript ecosystem and [participate in standards committees like TC39](/blog/deno-joins-tc39), because we want JavaScript to be better and more effective for everyone.

TC39’s 108th meeting recently [advanced 9 proposals](https://tc39.es/process-document/) across 4 stages, which represent rough ideas (stage 0) to fully standardized features (stage 4).

Here’s a brief summary of each and what that might mean for the future of JavaScript.

Stage 4

* Explicit Resource Management (`using`)
*`Array.fromAsync`
*`Error.isError`

Stage 3

* Immutable`ArrayBuffer`

Stage 2

*`Random.Seeded`
*`Number.prototype.clamp`

Stage 1

* Keep Trailing Zeros
* Comparisons
* Random Functions

## Advanced to stage 4

### Explicit Resource Management (`using`)

The new`using`declaration (and its async variant`await using`) adds deterministic cleanup for resources, inspired by languages like C# and Python. Objects can define`[Symbol.dispose]()`(or`[Symbol.asyncDispose]()`) that is automatically called when a`using`block ends. For example:

    class FileHandle {
      constructor(name) {
        this.name = name; /* open file... */
      }
      [Symbol.dispose]() {
        console.log(`${this.name} closed`); /* close file */
      }
    }
    function readFile() {
      {
        using file = new FileHandle("data.txt");
        // read from file...
      }
      // file.[Symbol.dispose]() was called here automatically
    }
    readFile(); // logs "data.txt closed"

This ensures cleanup (like closing files or streams) even if an exception occurs inside the block, making resource management easier and safer.

This feature is supported in [Chrome 134, Firefox 134,](https://v8.dev/features/explicit-resource-management#explicit-resource-management-support) and [Deno v2.3](/blog/v2.3#explicit-resource-management-and-the-using-keyword).

In Deno you can already use the`using`keyword to manage resources like file handles ([`Deno.File`](https://docs.deno.com/api/web/~/File)), network sockets ([`Deno.Conn`](https://docs.deno.com/api/deno/~/Deno.Conn)), and more. For example, here we stop a HTTP server automatically after having made a request to it:

    using server = Deno.serve({ port: 8000 }, () => {
      return new Response("Hello, world!");
    });
    
    const response = await fetch("http://localhost:8000");
    console.log(await response.text()); // "Hello, world!"
    
    // The server is automatically closed here because of the`using`keyword

The Deno team is also interested in using the`using`keyword to simplify async context propagation through In fact, Deno’s support for [async context propagation](https://github.com/tc39/proposal-async-context) (stage 2) already enables us to do things like [auto-instrumentation of`console.log`to include HTTP information](/blog/zero-config-debugging-deno-opentelemetry#the-issue-with-logs). However, right now every time you want to create a new span to track some work, you need to create a new function and run it. This is cumbersome:

    async function doWork() {
      const parent = tracer.startSpan("doWork");
      return parent.run(async () => {
        console.log("doing some work...");
        return true;
      });
    }

The Deno team is proposing [disposable`AsyncContext.Variable`](https://github.com/tc39/proposal-async-context-disposable), which would allow you to use the`using`keyword to simplify this code:

    async function doWork() {
      using parent = tracer.startActiveSpan("doWork");
      console.log("doing some work...");
      return true;
    }

See? Much less boilerplate!

###`Array.fromAsync`

[`Array.fromAsync`](https://github.com/tc39/proposal-array-from-async) is like`Array.from`but works with async iterables, returning a**Promise**that resolves to the resulting array. It also supports a mapping function and`thisArg`, just like`Array.from`.

For example, given an async generator of values, you can write:

    async function* generate() {
      yield await Promise.resolve(1);
      yield await Promise.resolve(2);
    }
    const nums = await Array.fromAsync(generate()); // [1, 2]

Here`Array.fromAsync(generate())`returns a promise that resolves to`[1, 2]`once all yielded values are ready. This makes common async collection patterns much simpler and more readable.

[`Array.fromAsync`is available in all browsers, as well as Deno v1.38 and Node v22.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fromAsync#browser_compatibility)

###`Error.isError`

[`Error.isError(value)`](https://github.com/tc39/proposal-is-error) is a new built‚Äëin for reliably detecting error objects. It returns`true`if`value`is any kind of Error (including cross-realm or subclassed errors), and`false`otherwise. For example:

    Error.isError(new TypeError("oops")); // true
    Error.isError({ name: "TypeError", message: "oops" }); // false

While this is almost never needed, authoring certain code, such as some polyfills, can be difficult without this functionality.

[`Error.isError`has support in all browsers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/isError#browser_compatibility), as well as in [Deno v2.2](https://deno.com/blog/v2.2).

## Stage 3

### Immutable`ArrayBuffer`

[Immutable`ArrayBuffer`is now at Stage 3](https://github.com/tc39/proposal-immutable-arraybuffer), introducing`transferToImmutable()`and`sliceToImmutable()`methods. Calling`transferToImmutable()`on a buffer moves its data into a new, unchangeable buffer and detaches the original. For example:

    let buf = new ArrayBuffer(100);
    let imm = buf.transferToImmutable();
    // buf is now detached (byteLength 0), and imm is a new immutable ArrayBuffer of length 100
    console.log(buf.byteLength, imm.byteLength); // 0, 100
    
    // attempting to modify imm will throw a TypeError
    imm[0] = 1; // TypeError: Cannot modify an immutable ArrayBuffer

Similarly,`sliceToImmutable(start, end)`creates an immutable copy of a subrange. Immutable buffers _cannot be detached or modified_ , which makes sharing binary data (e.g. across threads or workers) safer and more efficient.

We are planning to make use of this in Deno to optimize various APIs that take byte arrays as inputs, such as`new Response()`or`Deno.writeFile()`. This will allow us to avoid unnecessary copies and improve performance when working with binary data.

## Stage 2

###`Random.Seeded`

Current pseudo-random number generator methods (`Math.random()`for instance) are automatically seeded, making it not reproducible across runs or realms. However, there are times when you‚Äôd want a reproducible set of random values.

[This proposal](https://github.com/tc39/proposal-seeded-random) for a new`SeededPRNG`class provides reproducible randomness by allowing you to set a seed. You create a`Random.Seeded(seedValue)`object and use its`.random()`method instead of`Math.random()`. For example:

    const prng = new Random.Seeded(42);
    for (let i = 0; i < 3; i++) {
      console.log(prng.random());
      // prints the same sequence on every run given seed 42
    }

This is useful in games or simulations where repeatability matters. You can also derive new seeds or clone state from an existing`PRNG`for complex scenarios.

###`Number.prototype.clamp`

[The`Number.prototype.clamp(min, max)`function](https://github.com/tc39/proposal-math-clamp) (originally`Math.clamp`) returns a number bounded between`min`and`max`. This is handy for keeping values within a range. For example:

    (5).clamp(0, 10); // 5
    
    (-5).clamp(0, 10); // 0 (floored at 0)
    (15).clamp(0, 10); // 10 (capped at 10)

If`min > max`, it throws a`RangeError`. This avoids verbose patterns like`Math.min(Math.max(x, min), max)`and clarifies intent.

## Stage 1

### Keep Trailing Zeros

[New formatting options in`Intl.NumberFormat`](https://github.com/tc39/proposal-decimal) will allow preserving or stripping trailing zeros in formatted numbers, which is useful for representing human-readable decimal values (e.g. money).

The`trailingZeroDisplay: "auto"`setting (default)**keeps zeros**according to the specified precision;`"stripIfInteger"`removes them when the number is an integer. For example:

    // Keep two decimal places (auto-preserve zeros):
    new Intl.NumberFormat("en", {
      minimumFractionDigits: 2,
      trailingZeroDisplay: "auto",
    })
      .format(1.5); // "1.50"
    
    // Strip zeros if unnecessary:
    new Intl.NumberFormat("en", {
      minimumFractionDigits: 0,
      trailingZeroDisplay: "stripIfInteger",
    })
      .format(2); // "2"  (not "2.0")

This gives developers finer control over number formatting (e.g. currency or fixed-point output) without ad-hoc string manipulation.

### Comparisons

[The**Comparisons**proposal](https://github.com/tc39/proposal-inspector) aims to standardize how JavaScript produces**human-readable representations of values**‚Äî similar to`util.inspect`in Node.js or how test runners print diffs.

The goal is to give test frameworks and console tools a consistent way to generate diffs ‚Äî especially across runtimes and realms.

### Random Functions

[This proposal introduces a new`Random`namespace](https://github.com/tc39/proposal-random-functions) with convenience methods to avoid common pitfalls with randomness. The methods in the`Random`namespace not only can generate random numerical values, but also accept and return collections.

Here are some examples:

    // Random integer between -5 and 5
    Random.int(-5, 5); // -1
    
    // Random Number between 0 and 10
    Random.number(0, 10); // 8
    
    // Random number between 0, 5 with steps of 0.1
    Random.number(0, 5, 0.1); // 1.1
    
    // Randomly select n items from an array.
    const name = Random.take(["Alice", "Bob", "Carol"], 2); // ['Alice', 'Bob']
    
    // With replacement.
    Random.take(["Alice", "Bob", "Carol"], 2, { replace: true }); // ['Alice', 'Alice']
    
    // With weights.
    Random.take(["Alice", "Bob", "Carol"], 2, { weights: [1, 1, 5] }); // ['Alice', 'Bob']
    
    // Select one random item.
    Random.sample(["Alice", "Bob", "Carol"]); // 'Bob'
    
    // Mutate and return a "shuffled" Array in-place.
    Random.shuffle([1, 2, 3, 4]); // [4,2,1,3]
    
    // Return a new shuffled array.
    const shuffled = Random.toShuffled([1, 2, 3, 4]);

The goal is to make random-related code**safer and more concise**, reducing off-by-one errors and improving consistency.

# What’s next

TC39 continues to evolve and improve JavaScript to meet the needs of modern developers. Deno is committed to web standards and actively participates in these discussions to use JavaScript, which directly simplifies how you could write JavaScript in Deno (see [async context propagation](https://github.com/tc39/proposal-async-context) and our [built-in OpenTelemetry API](/blog/zero-config-debugging-deno-opentelemetry)). The next TC39 meeting where these proposals will be further discussed is scheduled for late September.

>**üö®Ô∏è[There have been major updates to Deno Deploy!](/deploy) üö®Ô∏è**
>
> * [Improved Playgrounds with livestreaming logs, traces, and templates like Next.js](https://www.youtube.com/watch?v=fRFqZsBivCo)
> * [Automatic and immediate observability and telemetry](https://www.youtube.com/watch?v=PwDU8yTZmUM)
> * [Simpler management for environment variables](https://x.com/deno_land/status/1935625197295739103)
>

>
> and [much more!](https://docs.deno.com/deploy/early-access/changelog/)
>
> [Get early access today.](/deploy)

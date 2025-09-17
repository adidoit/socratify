---
title: "Rust in production at Figma"
company: "figma"
url: "https://www.figma.com/blog/rust-in-production-at-figma/"
content_length: 25736
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

May 2, 2018

# Rust in production at Figma

![](data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAUABQDASIAAhEBAxEB/8QAHAABAAEEAwAAAAAAAAAAAAAAAAUBAgMEBgcI/8QAJRAAAgIDAAAFBQEAAAAAAAAAAQIDBAAFEQYTITFhBxIVIiMy/8QAFwEAAwEAAAAAAAAAAAAAAAAAAQUGBP/EAB0RAAICAgMBAAAAAAAAAAAAAAECAAMEERIhUTH/2gAMAwEAAhEDEQA/AOwPHniCeltIKMYdYSnmSMo9SO+wzeTd1KmrNmJJQUQSElT6g5D/AFXuwVPx7CeNLDOUC+7EEZYm2i1up08d2ZI69mUIXlHQRzvMn0oLOeo8WxBT2Zz+nYW1VinQH7ZFDDvzjMcFqu8StBLG0fP1KsOYw8SJk2J4xbebC5u45rdh55C3+pD3JjxBv7+0uQ1bcoNesP5oBwD5xjK6hQcqvY9iO1iMazRlK+0vQR+XDbnRAfQBzzGMZRFF38iEM3s//9k=)![](https://cdn.sanity.io/images/599r6htc/regionalized/193b6e56f51b0c0ac8ae1fdeaab81f9f14b48531-416x416.jpg?w=416&h=416&q=75&fit=max&auto=format)

Evan WallaceCo-founder, Figma

  * [Inside Figma](https://www.figma.com/blog/inside-figma/)
  * [Quality & performance](https://www.figma.com/blog/quality-and-performance/)
  * [Engineering](https://www.figma.com/blog/engineering/)
  * [Product updates](https://www.figma.com/blog/product-updates/)
  * 


![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAAA50lEQVQoz53RPctGUBzHcc8lBjFJYVUWEyMLg91otRjIIqW8BbPVw2KQjN7b7+4Y77qucg3f5ZzOp3P+h6IoCp8SBAGmacL3fQRBAMuynrVvZ6hPGxzHwXVdFEWBvu/Rti3yPIfjOOB5/j2oquoDbNuG4ziwLAvGcUSWZdA07T1Into0Da7rwn3fOM8T8zyjrmvYtv0e1HUdZVli3/cHmqYJ67qiqioYhvEeFEURURQ98yN1XYdhGJAkCSRJeg+SFEWB53mI4xhpmiIMw2cULMv+BpLIj8qy/OAkcjuGYX4H/0fT9Nf9P7Gn6JBIx6S6AAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/4ebb54efbfa2fd4951e04ddb0b3f2b67146976ad-2120x1000.png?rect=1,0,2119,1000&w=1632&h=770&q=75&fit=max&auto=format)

How Mozilla’s new language dramatically improved our server-side performance

 _Like building state-of-the-art web apps?[Come work at Figma!](https://www.figma.com/careers/)_

At [Figma](https://www.figma.com), performance is one of our most important features. We strive to enable teams to work at the speed of thought, and our multiplayer syncing engine is a critical part of this vision. Everyone should see each change made to a Figma document in real time.

The multiplayer server we [launched with two years ago](https://blog.figma.com/multiplayer-editing-in-figma-8f8076c6c3a6) is written in TypeScript and has served us surprisingly well, but Figma is rapidly growing more popular and that server isn’t going to be able to keep up. We decided to fix this by rewriting it in Rust.

[Rust](https://www.rust-lang.org/en-US/) is a new programming language from Mozilla, the company that makes Firefox. They’re using it to build a next-generation browser prototype called [Servo](https://research.mozilla.org/servo-engines/) which demonstrates that browsers can be way faster than they are today. Rust is similar to C++ in performance and low-level ability but has a type system which [automatically prevents whole classes of nasty bugs](https://polyfloyd.net/post/how-rust-helps-you-prevent-bugs/) that are common in C++ programs.

We chose Rust for this rewrite because it combines best-in-class speed with low resource usage while still offering the safety of standard server languages. Low resource usage was particularly important to us because some of the performance issues with the old server were caused by the garbage collector.

We think this is an interesting case study of using Rust in production and want to share the issues we encountered and the benefits we achieved in the hope that it will be useful to others considering a similar rewrite.

## Scaling our service with Rust

Our multiplayer service is run on a fixed number of machines, each with a fixed number of workers, and each document lives exclusively on one specific worker. That means each worker is responsible for some fraction of currently open Figma documents. It looks something like this:

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAAAsSAAALEgHS3X78AAABOElEQVQ4y6WSTY7CMAyFe5dZI8H15i6sEWtmM2UBt0FVKxX6/xeH99IY2mo0I5hID2LX/mLHCfq+P4tIbf+5yADrFODnCOP2S6A1xjhxv/QPw+Bs7K9ghQSG+Jj6ICN+jaZI27ZSFIVTXdcCgCDH7cuypEzTNLbruhT+7xmQkGV1CLR5ntssy2xVVRbxToQARgljcNATSMO34IqbislMJJQQ2myT/6iSPs0ZgaCHaCtlMD8ykCf6U10iKyNUfepnDq/Ed/MEsn8PEQ3UahSIO3RAHdAkbl4hW0aADkWmU9VEBaKa2VX82PJiKMYP5jFl3isrZ2ucsC76OW3IzFr+6x2+8LDHd4jTv3DaBQ7WXkLVi2JOQwZYhwD384l2tjD20O5N7ckgK4ii6COO41WSJBto/aY2ZJB1B5f53xhJTkJ5AAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/2f1548aa28e236a50ba53859b13c5fdf70908bb6-800x531.png?rect=1,0,799,531&w=804&h=534&q=75&fit=max&auto=format)

The main problem with the old server was the unpredictable latency spikes during syncing. The server was written in TypeScript and, being single-threaded, couldn’t process operations in parallel. That meant a single slow operation would lock up the entire worker until it was complete. A common operation is to encode the document and Figma documents can get very large, so operations would take an arbitrarily-long amount of time. Users connected to that worker would be unable to sync their changes in the meantime.

Throwing more hardware at the problem wouldn’t have solved this issue because a single slow operation would still lock up the worker for all files associated with that worker. And we couldn’t just create a separate node.js process for every document because the memory overhead of the JavaScript VM would have been too high. Really only a handful of documents were ever big enough to cause problems, but they were affecting the quality of service for everyone. Our temporary solution was to isolate the crazy documents to a completely separate pool of “heavy” workers:

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAAAsSAAALEgHS3X78AAABXUlEQVQ4y6WSTU7DMBCFcxfWSHA97sIadQ0bygJug6JUKjSN8+sx33OcNolQERDptR7H8808T7K+79/MrA7/fMSA9Zrx80LweeFg8N5Hab3eH4Yhxqw/YG0F3PJynw55S88YmrVta8fjMaquawNg5MR1VVWSb5omdF23Z/95ARRk3R0HQ1mW4XA4BOdc6InJCYIAk0xnKHQGKkgWYnNzKVmJgjYCAhrY0z5dCjzljEDoW2ztVVH2dFAVU9WYqM4E7QRr2xNwykluzkD5TxCbDkoTXEDuMAI9sZ8BY4dzoCxjdRqKzacqTR0K2ALgwoIJyH+0zHAWlldD8WkwpynrXtW5rGHVGLOxYV7Xw0B651R5Abz4HX77AKD1QIujxurjd0j1J7p4Z0PjqpD7Ud47OnVYlyriRgxYjxn3c4ede4INevijNmKIleV5flUUxfVut7tFN79SUYwiVwyxvgChQN5qd3YsTgAAAABJRU5ErkJggg==)![](https://cdn.sanity.io/images/599r6htc/regionalized/7cb4c2114a729a419638d4235f01fc1b260a3cf0-800x531.png?rect=1,0,799,531&w=804&h=534&q=75&fit=max&auto=format)

This kept the service up but meant we had to continually look out for crazy documents and move them over to the heavy worker pool by hand. It bought us enough time to solve these problems for real, which we did by moving the performance-sensitive parts of the multiplayer server into a separate child process. That child process is written in Rust and communicates with its host process using stdin and stdout. It uses so little memory compared to the old system that we can afford to fully parallelize all documents by just using a separate child process per document. And serialization time is now over 10x faster so the service is now acceptably fast even in the worst case. The new architecture looks like this:

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAANCAYAAACpUE5eAAAACXBIWXMAAAsSAAALEgHS3X78AAABaElEQVQ4y5WSS07DMBCGc1POwQ56jEocA1akqy66K6hwhW6qtm6d+O0Z/nFjFCKQyEifEiczn8ePxnu/TCmtwTvYgreZbIfadQhh2cQYX3LOeyIyQINuJpqZpXYP17MIVxhc+I/Av0INTF6ogc7KGJ6LuETYokANxZlGgSWQMaaAPEJxeddakw+eYop01TqfTifWnVY+hHYqpHFnEHLf9wV5Ry5DyNdOc+ctm+j4oq+klJIcFSKESGyRqKRt6aAuaVgGW2vZOVfeheADW++4i7bQO0vyHx4lzTUYtEDhtOUjybMKpKsqlL0S5BuWyy4FNsmz8ZaG2ptw2mEV1eKxUHKKUAQp3qR+0uF0D8chE6C4AFlBDkdWkjImBw6HM+zvt3BVheKcXpm6n/W86jWqyCR0u04/Ojz/dm3+GXmoPcP1KofyhJY3GHyCHfiYyW6o3YirORwOd8fj8R6XcwEewONMpGYhDnF9AQxO5HRrJuTEAAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/87448ddbbe8f49d41fd89618c644b2738bc8249c-800x504.png?rect=1,0,799,504&w=804&h=507&q=75&fit=max&auto=format)

## Server-side performance improvements

The performance improvements are incredible. The following graphs show various metrics for the week before, during, and after the progressive rollout. The huge drop in the middle is where the progressive rollout hit 100%. Keep in mind that these improvements are in server-side performance, not client-side performance, so they mainly just mean that the service will continue to run smoothly for everyone without any hiccups.

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABZ0lEQVQoz5WS21LCMBCGeSh9Ay702eRxvBC4QB6FsVU8kbbQnDbJ+m8asIwyjpnZJnv4v+5sMvHeP6aUDF9YyLPWOhsRXSpjYSC/mkCwhNP+VhRjZGvtCShn1F4CNgAuBLiAUJVglM94IXdmZ7myFa0C6yEDQwgKtRzwgcmeu4Mgnx2hUwrsQyx+4N4RHyyx8SH3XIDzE1AKtaPUaMe73vEBAhHuree3veFtq1khBwBLzXOjuWp6ft/bBCYaSIpoBBTxrrfpBcIaxSjkznj+OFiuVM9PsNfO/IhtO4PbyJ2fd2g9cadtxN+ly6QAb45WYke/FTMudYNFCyCFb+AS82pkhp4oDfPDOQS2eDKIDTPFpCBi6zw7/Hw04zxDYeCWM3AOZ5ckEWMolxeHCx7WHzHRCPAz3zLe18w5dw9nDVvJQ/+niWYtDLDuJpvN5rqqqmld17fYb7Bnk/PRTrFRfFxXtFOwrr4Aq5JBTn45pxMAAAAASUVORK5CYII=)![](https://cdn.sanity.io/images/599r6htc/regionalized/7437b3d0aa565eb15fb384fad1753afbee3eca03-720x413.png?w=804&h=461&q=75&fit=max&auto=format)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABVklEQVQoz5WSb07DMAzFeydusA9wN7gNfAA2jXGYaUyDKWvXP4md2DwnHUioFRDptfWL/YuTtGLmVxEZdGb0fa9t22rTNNp13VyaGgOsTYXHCkE9lUREWte1Hg4H3e/36pxT5M8BT5hbGnCJwI1mknHkICWhEARdCroT7332yuzXSGOtA+s5A5GUgYxkz0lNnHKVJtP4PSOZBEYUNZ7lvQ1qOnvWAHBHUc+B8yIx/REYY3QhJj0NJB9dAbqetAUInppncQ84I4+gwBGLRPvOxPQTSJgc0BKSxFOUPrB0gSCWFp03nuTsS1zm4Jd3suOJ2OUFuALwhG1j9Xi5D7WYcKPw8jnadq0zTzgK4twpF690mL5v+QnFR7s9iAGLWSlFG/DixUsTHsRS/ogjWI/VMAx3+N8eoA20hl7+qfVYew/WbbXdbq92u90CuoGuf9fblG+1C2N9AoY3Q55nP0QdAAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/5251b4480459e10b091f4f9119601253544ad269-800x458.png?w=804&h=460&q=75&fit=max&auto=format)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABVUlEQVQoz5WS207DMAyG91DwBlywZ2OPwwXbLsYeZVIrQGjrDm0OdhLz2y0DTStilX7Fdu0viZ0JEb2WUrz88YUQpOs6iTGO5iiDmVcTAJdwDmOJSBLnnLRtK957SSmNAffIXShwAacZgrlc+XLOBSBbr/0eahuwXgyIRANyysVREhWlLCg/q/yc5FLlF3BuQOzeaNExcHk/BXk7Btl7ksDZ4KfIsJNgv/8DCck7R0Vh9cHLZxvlFFgaR/KBTbZdNDhuIZyz3UClt1IiunEBxM8ucgakqI6esJKtjYtQbyPH1A6r1uhhEtr2DVyih3vdh1kb3/cMCRKJhTBltRnxiGv7SBDD7k+I1aaiDEzZgHM4O50glIZJm3ByRNLZ1xSNWTyf87RGgVubMt7YDA/2Gc4aWulDv1Fas1YGWE+TzWZzX1XVQ13XU+jxFlWVqlJ7qgyw7r4AnwxD91nFS7sAAAAASUVORK5CYII=)![](https://cdn.sanity.io/images/599r6htc/regionalized/a99194a59adff026121fe63e823e9c1320193833-720x413.png?w=804&h=461&q=75&fit=max&auto=format)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABVElEQVQoz5WSX1ICMQzGOZTewAc5mx7HB4EH5CjMLE87yK7uvyZN4pdQARmc0c5+022a/JKmnRHRm6qOdmOM42hd153U972llG65mjOYeT0DcIVFe+2AzQA0TWN1XYfato0kOedbwAYxSwcuReRQjKIXA4FKKekwDCH4hu1qSIk9YP81gHA6wGCcRSfONlA2ymKgHyXqAb9JL4CLE5BFrEus+z5Z3SVrR7IRYJcnYU8Anz8BuQAHYv2c2D4mMp/7xJ4E6+P8Dc7w9ROU/yB6234A3Qmz4FN3Yu8fZ03MOlFWTzaks/oy4wTCaAniTsAV6I1XXhruB7CyDmnppVc0EVqRyBIfq4TiVlBEQ8QBXAD4DimUy03HMkfFWU42Pdt8v9hzJBTZxy3jOTzjsb5gsYHW/tD/KY/ZOAOsp9l2u72vqupht9vNocf/qKpclf/PnQHW3Rc2fEO381VzewAAAABJRU5ErkJggg==)![](https://cdn.sanity.io/images/599r6htc/regionalized/9cc3b8d47d4154bb3fa232a6aa0a3b55bfebe03d-720x413.png?w=804&h=461&q=75&fit=max&auto=format)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABa0lEQVQoz52RW07DMBBFsyd20A/YG+wGPoBWUBZTFdGk5NE87Bl7zL0mlSA/VFi6cWbsOZ5HoapvZjalxYoxJudcGscx9X2fxX/6eLZcZIC1LfDZwGiXF0QkA9q2TWVZpqqqUtd12cczxCyBDVhrAtd4sZ6d0eYFn4UQDMEGSBb/6ePZjxXn2Bqs5wzEpTqgDNFgij2/Psv+ls0t+g10oqkevDUTSpWQvIakAY9AE2w320juMuDoNX2cJnvvXDqcXPocfCL8iL3sfbZPTvMDhHIwVKAxA+UMjACi3NSOPoLMLLOq3tkBj9DXObEOvsGrTaLmJBiy5h4FTCFDJAM3oDdMXHCRZQVcYE/ZhtELSg3Z51k+KhmcRxsUbYlshSljQ2yEUwb1CcAjJ4dMMZMY0JYs/nOdfZhtthFIL6ullEMnA8k9FtM03QH6AG2hF+j1Uum3XlRz7D1Yt8Vut7va7/cr6Aa6/qcYuyLrC5fkQpNKci87AAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/58fb07c6132692bf1ee0809be5ef4ec3eac87107-800x458.png?w=804&h=460&q=75&fit=max&auto=format)

Here are the numeric changes in peak metrics as compared to the old server:

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAAAsSAAALEgHS3X78AAABbklEQVQoz5WSS1LDMBBEfSduwILcDW4DCyAUhMOkkpXjv5NY0ojXihwIlQW4qi1pPPPUI7k4Ho+fwzDs45XHzKJz7iKmdQjhvKY+eu/jnmeaplVB4K3v+2Ycx0jgnKgicmLbtmnUWsVt18au79Nc8aqqUg6mauqXhV7AKqARhcPhYMSMXc0zOtYaAZojdpiOSZorD1CQGTaocP8qh0tAVV3XcbfbmcBAUxtQ1VO03KaXS/NJwUJqfxhHk1Pg38Cu6ypgsSxLY34BNICBQq19AJalDRJwGK4DdRYCNk2jpJScgHmcgVPW7JB2TQaYXwIFou3AAWvHdIYcnAG0oPOUAueWBZBPLp3hb4e65Tpfis23rV8m6veQS8aQ5ewkfZfrHy3XAJcCvhAo5Yq544PXQzE2wskaY8jydhLeUx7tOv0ZwEr0XAB6IPAEbIXeAX78R6rJtY+w7ov1en2z2Wxut9vtAt3NIvYn5fyFGGJ9AXhiP2JLQGsdAAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/aef8d9f50f52218911be208167b18dac8966d646-800x458.png?w=804&h=460&q=75&fit=max&auto=format)

## The benefits and drawbacks of Rust

While Rust helped us write a high performance server, it turns out the language wasn’t as ready as we thought. It’s much newer than standard server-side languages and still has a lot of rough edges (described below).

As a result, we dropped our initial plan to rewrite our whole server in Rust and chose to focus solely on the performance-sensitive part instead. Here are the pros and cons we encountered in that rewrite:

### Pros

  * Low memory usage



Rust combines fine-grained control over memory layout with the lack of a GC and has a very minimal standard library. It used so little memory that it was actually practical to just start a separate Rust process for every document.

  * Awesome performance



Rust definitely delivered on its promise of optimal performance, both because it can take advantage of all of LLVM’s optimizations and because the language itself is designed with performance in mind. Rust’s [slices](https://doc.rust-lang.org/1.22.0/std/slice/) make passing raw pointers around easy, ergonomic, and safe, and we used that a lot to avoid copying data during parsing. The [HashMap API](https://doc.rust-lang.org/std/collections/struct.HashMap.html) is implemented with [linear probing](https://en.wikipedia.org/wiki/Linear_probing) and [Robin Hood hashing](https://en.wikipedia.org/wiki/Hash_table#Robin_Hood_hashing), so unlike C++’s [unordered_map API](https://en.cppreference.com/w/cpp/container/unordered_map) the contents can be stored inline in a single allocation and are much more cache-efficient.

  * Solid toolchain



Rust comes with [cargo](https://doc.rust-lang.org/cargo/index.html) built-in, which is a build tool, package manager, test runner, and documentation generator. This is a standard addition for most modern languages but is a very welcome improvement coming from the outdated world of C++, the other language we had considered using for the rewrite. Cargo was well-documented and easy to use, and it had helpful defaults.

  * Friendly error messages



Rust is more complex than other languages because it has an additional piece, the borrow checker, with its own unique rules that need to be learned. People have put a lot of effort into making the error messages readable and it really shows. They make learning Rust much nicer.

### Cons

  * Lifetimes are confusing



In Rust, storing a pointer in a variable can prevent you from mutating the thing it points to as long as that variable is in scope. This guarantees safety but is overly restrictive since the variable may not be needed anymore by the time the mutation happens. Even as someone who has been following Rust from the start, who writes compilers for fun, and who knows how to think like the borrow checker, it’s still frustrating to have to pause your work to solve the little unnecessary borrow checker puzzles that can come up regularly as you work. There are good examples of the problems this creates in [this blog post](https://smallcultfollowing.com/babysteps/blog/2016/04/27/non-lexical-lifetimes-introduction/).

_What we did about it:_ We simplified our program to a single event loop that reads data from stdin and writes data to stdout (stderr is used for logging). Data either lives forever or only lives for the duration of the event loop. This eliminated pretty much all borrow checker complexities.

_How this is being fixed:_ The Rust community is planning to address this with [non-lexical lifetimes](https://github.com/rust-lang/rfcs/blob/master/text/2094-nll.md). This feature shrinks the lifetime of a variable such that it stops after the last time it’s used. Then a pointer will no longer prevent the mutation of the thing it points to for the rest of the scope, which will eliminate many borrow checker false-positives.

  * Errors are hard to debug



Error-handling in Rust is intended to be done by returning a value called “Result” that can represent either success or failure. Unlike with exceptions, creating an error value in Rust does not capture a stack trace so any stack traces you get are for the code that reported the error instead of the code that caused the error.

_What we did about it:_ We ended up converting all errors to strings immediately and then using a macro that includes the line and column of the failure in the string. This was verbose but got the job done.

_How this is being fixed:_ The Rust community has apparently come up with several workarounds for this issue. One of them is called [error-chain](https://docs.rs/error-chain/*/error_chain/) and another one is called [failure](https://boats.gitlab.io/failure/). We didn’t realize these existed and we aren’t sure if there’s a standard approach.

  * Many libraries are still early



Figma’s document format is compressed so our server needed to be able to handle compressed data. We tried using two separate Rust compression libraries that were both used by Servo, Mozilla’s next-generation browser prototype, but both had subtle correctness issues that would have resulted in data loss.

_What we did about it:_ We ended up just using a tried-and-true C library instead. Rust is built on LLVM so it’s pretty trivial to call C code from Rust. Everything is just LLVM bitcode in the end!

_How this is being fixed:_ The bugs in the affected libraries were reported and have since been fixed.

  * Asynchronous Rust is difficult



Our multiplayer server talks over WebSockets and makes HTTP requests every so often. We tried writing these request handlers in Rust but hit some concerning ergonomic issues around the futures API (Rust’s answer for asynchronous programming). The [futures API](https://docs.rs/futures/0.1.25/futures/) is very efficient but somewhat complex as a result.

For example, chaining operations together is done by constructing a giant nested type that represents the whole operation chain. This means everything for that chain can be allocated in a single allocation, but it means that error messages generate long unreadable errors reminiscent of template errors in C++ (an example is [here](https://gist.github.com/evanw/06a672db1897482eadfbbf37ebf9b9ec)). That combined with other issues such as needing to adapt between different error types and having to solve complex lifetime issues made us decide to abandon this approach.

_What we did about it:_ Instead of going all-in on Rust, we decided to keep the network handling in node.js for now. The node.js process creates a separate Rust child process per document and communicates with it using a message-based protocol over stdin and stdout. All network traffic is passed between processes using these messages.

_How this is being fixed:_ The Rust team is hard at work on [adding async/await to Rust](https://github.com/rust-lang/rfcs/blob/master/text/2033-experimental-coroutines.md), which should solve many of these issues by hiding the complexity of futures underneath the language itself. This will allow the “?” error-handling operator that currently only works with synchronous code to also work with asynchronous code, which will cut down on boilerplate.

## Rust and the future

While we hit some speed bumps, I want to emphasize that our experience with Rust was very positive overall. It’s an incredibly promising project with a solid core and a healthy community. I’m confident these issues will end up being solved over time.

Our multiplayer server is a small amount of performance-critical code with minimal dependencies, so rewriting it in Rust even with the issues that came up was a good tradeoff for us. It enabled us to improve server-side multiplayer editing performance by an order of magnitude and set Figma’s multiplayer server up to scale long into the future.

![](data:image/jpeg;base64,/9j/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAUABQDASIAAhEBAxEB/8QAHAABAAEEAwAAAAAAAAAAAAAAAAUBAgMEBgcI/8QAJRAAAgIDAAAFBQEAAAAAAAAAAQIDBAAFEQYTITFhBxIVIiMy/8QAFwEAAwEAAAAAAAAAAAAAAAAAAQUGBP/EAB0RAAICAgMBAAAAAAAAAAAAAAECAAMEERIhUTH/2gAMAwEAAhEDEQA/AOwPHniCeltIKMYdYSnmSMo9SO+wzeTd1KmrNmJJQUQSElT6g5D/AFXuwVPx7CeNLDOUC+7EEZYm2i1up08d2ZI69mUIXlHQRzvMn0oLOeo8WxBT2Zz+nYW1VinQH7ZFDDvzjMcFqu8StBLG0fP1KsOYw8SJk2J4xbebC5u45rdh55C3+pD3JjxBv7+0uQ1bcoNesP5oBwD5xjK6hQcqvY9iO1iMazRlK+0vQR+XDbnRAfQBzzGMZRFF38iEM3s//9k=)![](https://cdn.sanity.io/images/599r6htc/regionalized/193b6e56f51b0c0ac8ae1fdeaab81f9f14b48531-416x416.jpg?w=416&h=416&q=75&fit=max&auto=format)

Evan Wallace is the co-founder and former Chief Technology Officer at Figma.

[Twitter](https://twitter.com/evanwallace)

## Subscribe to Figma’s editorial newsletter

Enter email*

I agree to opt-in to Figma's mailing list.*

By clicking “Submit” you agree to our [TOS](https://www.figma.com/tos/) and [Privacy Policy](https://www.figma.com/privacy/).

## Related articles

  * [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAABiElEQVQoz62SN4oqUBSGjWBAEQwYEHNEzIgKIjY2xkrEQlCxsLEVA7oEC0GwEcFtWFi5ADf0Pe6FKd6M001x4HCL7/zhKhQKBWK0Wi2JRIJut0utViMQCBCNRgkGg8RiMXK5HNVqlfV6zfF4pN/vk06ncbvdqNVqvjiKr0Wj0RCJRGg2m5TLZUKhEIVCgWKxSCqVol6v0+v1mM/nzGYzuU8mExqNBnq9/idQpVLhcrkolUokk0mpajqdstvtGAwGLJdLTqeThIhjQvFisaDVamE0Gn8CxdhsNqkqHo+Tz+c5n8+8Xi/2+z3b7Zbn88nlcpEwh8NBJpORkYi4PgLNZrPM0e/3k81muV6vvN9vNpsNnU6H2+3G4/FgPB5jt9sxmUwYDAaUSuVnoMfjod1uy/CFytVqxf1+ZzQayUPD4ZDD4SBtWq1WaVWn030GikfRqshIQL1eL5VKRbYpShFxiEbD4TBOp1MWIWDC7q9Ai8UioT6fT1oREQiQUCK+hiju+3yD/W/5L+Yf6TYFTxjlbEMAAAAASUVORK5CYII=)![](https://cdn.sanity.io/images/599r6htc/regionalized/f5e0b63326f08745f246b676731c5ad01bc92b59-2120x1000.png?w=528&h=249&q=75&fit=max&auto=format)18 designers predict UI/UX trends for 2018December 15, 2017By Valerie VetetoA designer’s obsession always circles back to one simple question: How can we improve the user’s experience?](https://www.figma.com/blog/eighteen-designers-predict-ui-ux-trends-for-2018/)

    * [Insights](https://www.figma.com/blog/insights/)
    * [UI/UX](https://www.figma.com/blog/ui-ux/)
    * [Thought leadership](https://www.figma.com/blog/thought-leadership/)

  * [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAJCAYAAAAywQxIAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAnElEQVQoz62S0Q7CIAxFaQtsA8YYuEyn/v9nXnHxdSYOH85Tm5O2t0ophSNEa4QYkXLB4DyIGd/6PxwXje2QygXL9YYwTWBpFGpjd+G6PZDzgt46MEmDsK4c07xPuC53lHFDp/15IbPAjxFxLgghwXcJRvrzQiJCX8OY6pRxGGCJQS033JM2BnMY8XQOmQncKnxj67skEQT6k/AXXmUMuHzU05qJAAAAAElFTkSuQmCC)![](https://cdn.sanity.io/images/599r6htc/regionalized/5463674dc55f56a1bf7fd9b0464ae26fd2b1728c-2120x1000.png?w=528&h=249&q=75&fit=max&auto=format)A Sketch user’s perspective on switching to FigmaJune 13, 2018By Marco PacificoI used Figma for a month and I was blown away by its features and how well it works. ](https://www.figma.com/blog/a-sketch-users-perspective-on-switching-to-figma/)

    * [Working Well](https://www.figma.com/blog/working-well/)
    * [Design](https://www.figma.com/blog/design/)
    * [Productivity](https://www.figma.com/blog/productivity/)
    * [Figma Design](https://www.figma.com/blog/figma-design/)
    *   * [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAALCAYAAAB/Ca1DAAAACXBIWXMAABYlAAAWJQFJUiTwAAABXUlEQVQoz53SvUtCURjH8XPP9ap59cZVQTDoBbwaOUUGIlQ2BEGUNAkVZBQEVgSCYk0hVEM6RYFDNESD9DoYRBBRQ0RLFBEN1T/QHm2/HsPdo8Nnebh8Oec+hzHGIEaqqvltrUgTaScRMkA6ib3eoJm0QqKIwsdhVlLgfIdmBzTbhKIMQZabRYP8/xQSy8JtKSPku0VP6AxOzz5stnMEAneIRnfh94cpbBIJqmQKFukRg/5f5NLfmFsrwehbQiRawFbhFccnz0gk5qFpDpFg5SrLsMtfSIR/cFr8wGpxG/0jw0hNJ/F0fY/Pt3dk0mnoui4StJJRWFkZY94XHE2UUUpmsN4dxF6wCw/JBVzm84jHYlBVVSRY2ayX/mEcPr6CrGsGF229uHFouOIyDl1uLBoGfB4PLYqLbrkS1WBhLQgyN2Zp6xs0z5FJYhClsXfIYCI66ahyVmes0WC9/gACJBj/aEDnZAAAAABJRU5ErkJggg==)![](https://cdn.sanity.io/images/599r6htc/regionalized/65be0edbf385363c4ae5211353ea26e78dc689cf-1400x748.png?w=528&h=282&q=75&fit=max&auto=format)Advanced Project Permissions for design systemsNovember 29, 2017By Thomas WrightWith increasing intensity, design and product teams are mulling over the what’s and the how’s of design systems.](https://www.figma.com/blog/advanced-project-permissions-for-design-systems/)

    * [Inside Figma](https://www.figma.com/blog/inside-figma/)
    * [Collaboration](https://www.figma.com/blog/collaboration/)
    * [Design](https://www.figma.com/blog/design/)
    * [Product updates](https://www.figma.com/blog/product-updates/)
    * [Design systems](https://www.figma.com/blog/design-systems/)
    * [Security](https://www.figma.com/blog/security/)
    * 


## Create and collaborate with Figma

[Get started for free](https://www.figma.com/signup)

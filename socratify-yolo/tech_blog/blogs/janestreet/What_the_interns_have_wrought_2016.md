---
title: "What the interns have wrought, 2016"
company: "janestreet"
url: "https://blog.janestreet.com/what-the-interns-have-wrought-2016/"
content_length: 7875
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Now that the interns have mostly gone back to school, it’s a good time to look back at what they did while they were here. We had a bumper crop – more than 30 dev interns between our London, New York and Hong Kong offices – and they worked on just about every corner of our code-base.

In this post, I wanted to talk about just one of those areas: building efficient, browser-based user interfaces.

Really, that’s kind of a weird topic for us. Jane Street is not a web company, and is not by nature a place that spends a lot of time on pretty user interfaces. The software we build is for our own consumption, so the kind of spit and polish you see in consumer oriented UIs are just not that interesting here.

But we do care about having functional, usable user interfaces. The work we do is very data driven, and that rewards having UIs that are good at presenting up-to-date data clearly and concisely. And we want to achieve that while keeping complexity of developing these UIs low.

Historically, almost all of our UIs have been text-based. While I love the command line, it does impose some limitations. For one thing, terminals don’t offer any (decent) graphical capabilities. But beyond that obvious constraint, getting all the pieces you need for a decent UI to work well in a terminal, from scrolling to text-entry widgets, requires a lot of work that just isn’t necessary in a browser.

So this year, we’ve finally started pushing to make it easy for us to write browser-based applications, in particular relying on OCaml’s shockingly good [JavaScript back-end](http://ocsigen.org/js_of_ocaml/). This has allowed us to write web applications in OCaml, using our usual tools and libraries. As I’ve [blogged](/incrementality-and-the-web/) [about](/self-adjusting-dom/) [previously](/self-adjusting-dom-and-diffable-data/), we’ve also been exploring how to use [Incremental](https://github.com/janestreet/incremental_kernel), a framework for building efficient on-line computations, to make browser UIs that are both pleasant to write and performant.

That’s roughly where we were at the beginning of the summer: some good ideas about what designs to look at, and a few good foundational libraries. So the real story is what our interns, Aaron Zeng and Corwin de Boor, did to take us farther.

## Web Tables

Aaron Zeng’s project was to take all of the ideas and libraries we’d been working on and put them to use in a real project. That project was _web-tables_ , a new user-interface for an existing tool developed on our options desk, called the _annotated signal publisher_. This service provides a simple way for traders to publish and then view streams of interesting tabular data often based on analysis of our own trading or trading that we see in the markets.

The publisher fed its data to _Catalog_ , our internal pub-sub system. From Catalog, the data could be viewed in Excel, or in our terminal-based Catalog browser. But neither of these approaches worked as well or as flexibly as we wanted.

Enter web-tables. What we wanted was pretty simple: the ability to display tabular data from the annotated signal publisher with customizable formatting, filtering and sorting. This involved breaking a lot of new ground, from figuring out how do the sorting and filtering in an efficient and incremental way, to fixing performance issues with our RPC-over-websockets implementation, to figuring out a deployment and versioning story that let people easily create and deploy new views of their data.

One of the great things about the project is how quickly it was put into use. The options guys started using web-tables before the project was even really finished, and there was a tight feedback loop between Aaron and his mentor Matt Russell, who was using the tool on a daily basis.

## Optimizing rendering

Aaron’s web-tables work used [`incr_dom`](https://github.com/janestreet/incr_dom), a small framework that sets up the basic idioms for creating UIs using Incremental. As part of that work, we discovered some limitations of the library that made it hard to hit the performance goals we wanted to. Corwin de Boor’s project was to fix those limitations.

The key to building an efficient UI for displaying a lot of data is figuring out what work you can avoid. To this end, Corwin wanted to build UIs that logically contained thousands or even millions of rows, while only actually materializing DOM nodes corresponding to the hundred or so rows that are actually in view.

In order to figure out which nodes to render, he had to first figure out which nodes would be visible, based on the location of the browser’s viewport. This in turn required a way of looking up data-points based on where that data would be expected to render on the screen.

Corwin did this by building a data structure for storing the expected height of each object that could be rendered, while allowing one to query for a node based on the sum of the heights of all the nodes ahead of it. He did this by taking an existing splay tree library and rewriting it so it could be parameterized with a reduction function that would be used to aggregate extra information along the spine of the splay tree. By integrating the reduction into splay tree itself, the necessary data could be kept up to date efficiently as the splay tree was modified.

Corwin also spent a lot of time improving `incr_dom` itself, taking inspiration from other systems like [React](https://facebook.github.io/react/) and the [Elm](http://elm-lang.org/) language. We even corresponded a bit with Jordan Walke and Evan Czaplicki, the authors of React and Elm respectively.

One thing that came out of this was a neat trick for making the `incr_dom` API cleaner by using a relatively new feature of OCaml called [open types](https://sites.google.com/site/ocamlopen/). The details are a little technical (you can see the final result [here](https://github.com/janestreet/virtual_dom/blob/master/src/event_intf.ml) and [here](https://github.com/janestreet/incr_dom/blob/master/src/app_intf.ml#L98)), but I think what we ended up with is a bit of an advance on the state of the art.

There were a lot of other bits and pieces, like improving the handling of keyboard events in `js_of_ocaml`, creating a new incremental data-structure library called [`incr_select`](https://github.com/janestreet/incr_select) for more efficiently handling things like focus and visibility, and restructuring the `incr_dom` APIs to make them simpler to understand and open up new opportunities for optimization.

By the end, Corwin was able to build a demo that smoothly scrolled over a million rows of continuously updating data, all while keeping update times below 5ms. We’re now looking at how to take all of this work and feed it into real applications, including Aaron’s work on web-tables.

## Sound like fun?

If this sounds like interesting stuff, you should consider applying for a [summer internship](http://janestreet.com/apply) with us!

Jane Street internships are a great learning experience, and a lot of fun to boot. You even get a chance to travel: interns get to visit Hong Kong, London or New York (depending on where they started!) as part of their summer.

And the projects I described here are really just a taste. Here are some other projects interns worked on this summer:

  * Building a low-latency order router.
  * Adding data representation optimizations to the OCaml compiler
  * A service for simulating a variety of network failures, to make it easier to test distributed applications.
  * Making it possible to write [Emacs extensions in OCaml](https://github.com/janestreet/ecaml) (this was actually Aaron Zeng’s second project)



and that’s still just a small sample. One thing I love about the work at Jane Street is the surprising variety of problems we find ourselves needing to solve.

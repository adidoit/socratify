---
title: "What the interns have wrought, 2017 edition"
company: "janestreet"
url: "https://blog.janestreet.com/what-the-interns-have-wrought-2017/"
content_length: 10521
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Intern season is coming to a close, and it’s a nice time to look back (as I’ve done in [previous](/what-the-interns-have-wrought-rpc_parallel-and-core_profiler) [years](/what-the-interns-have-wrought-2016)) and review some of what the interns did while they were here. The dev intern program has grown considerably, with almost 40 dev interns between our NY, London, and Hong Kong offices.

Given that each intern does at least two projects in separate areas over the summer, there are a lot of projects to describe. And they really run the gamut across Jane Street’s departments and codebases. A few examples off the top of my head: building an incremental packet-capture database; creating tools for visualizing message rates on exchange lines; adding tracing tools for Async; implementing an OCaml API to Nessus; working on algorithms for efficient scheduling in a parallel/incremental system; monitoring the state of our networking switches.

Rather than try in vain to survey the full project list, I’ve picked out a few to go into a bit more depth on.

## Caching Snapshots

This one has to do with the somewhat obscure world of marketdata, so a little background seems in order.

_Marketdata_ is roughly speaking the data feeds published by securities exchanges. These feeds provide you enough information to determine the full set of open orders that are resting on the exchange at any given point in time. This is typically done by providing a detailed, transaction-by-transaction log of what happened on the exchange, including every order added, cancelled or traded.

To correctly interpret such a feed, you need to see messages in order and without gaps. This lets you rebuild the open order state incrementally, starting from a known state.

These feeds are generally distributed using IP multicast, which provides a scalable way of distributing some of these rather big data feeds to many consumers. Because IP multicast is unreliable, you need _gap-fillers_ to replay messages that are lost, and _snapshot servers_ to provide clients with a known starting state, so they can start in the middle of the day without having to replay a full day’s worth of messages.

Exchanges like NASDAQ and ARCA (two US equity exchanges) provide both gap-fillers and snapshot servers, but they are on the other end of a finite-bandwidth pipe. We have some big applications that consists of many individual components that each need to subscribe to the same feeds. We have our own gap-filler infrastructure, but we don’t currently have our own snapshot servers. That means that when these systems are restarted, they all end up requesting snapshots at the same time. These snapshot storms can really strain the bandwidth on our exchange connections.

To deal with this, intern Maciej Debski worked on a snapshot cache. The goal of the cache is to stand between clients and exchange-side snapshot servers, and to keep requested snapshots around for a short period of time, say, 30 seconds. This means that if we have a storm of snapshot requests, we don’t have to forward any but the first of those to the exchange-side snapshot server.

This work was all done in the context of _Mu_ , our system for consuming and normalizing multicast-based marketdata feeds. To make this work, Maciej wrote the snapshot server, created a protocol for clients to request snapshot over our internal Async-RPC protocol, and dove into the Mu client code to add support for grabbing snapshots from the proxy instead of from the exchange-side server.

I think it’s a nice reflection both of the Mu codebase and of Maciej’s good work that a working draft of the project was completed in a few weeks! It’s not through review yet, but this is serious practical work that we expect will materially improve the quality of our marketdata.

## Tracking Traits

Bugs are an unavoidable part of programming. At Jane Street, we put a lot of effort into testing and type-level checks, but mistakes still slip through. Sometimes, these mistakes are bad enough that it’s not enough to simply fix the bug; we have to figure out which concrete pieces of software are exposed to the bug, so we can do something about it.

Justin Cheng’s intern project was to build a system that would help us answer the question of which pieces of software are exposed to a given bug. Most of our code is stored in a single large Mercurial repository with about a million revisions. If a bug was found in one revision and resolved in another, we want to be able to figure whether a given revision is a descendant of the revision where the bug was introduced, but not a descendant of the revision where the bug was resolved. As you can imagine, this is really a graph algorithm at heart.

The system Justin built is structured around the following concepts:

  * A _gene_ corresponds to a fact which is _seeded_ at a given revision, and is inherited by all descendant nodes.
  * A _genome_ is the set of all genes that apply to a given revision.



A _trait_ corresponds to a pair of genes, one that _observes_ the trait, and one that _addresses_ it. A revision is considered to have the trait if its genome has the observing but not the addressing gene.

From a performance point of view, we wanted to be able to do all the work associated with traits efficiently, in both space and time. After working through a bunch of possible designs, Justin ended up implementing a system that eagerly computed the genome of every revision, making trait queries constant time and very fast. In order to keep memory usage down, genomes were hash-consed, meaning that each unique genome was represented exactly once, with multiple instances simply using the same copy.

The key then, was to make the process of seeding genes efficient. In the worst case, seeding a gene on the base revision of the entire repository would require a walk over the entire million-node data-structure, since it would affect the genome of every revision. Even though adding and removing of seeds is relatively rare, we wanted it to be fast so that it wouldn’t interfere with the availability of the [Iron](/code-review-that-isnt-boring) server, within which all of this trait tracking would be housed.

Part of the solution is to take advantage of the fact that Mercurial already presents the graph of revisions in a topologically sorted order, meaning that it’s easy to update the gene graph by simply walking it in that order. In addition, by keeping the data structure tight and minimizing the amount of work that needs to be done per node, even the worst-case walk could be made quite fast indeed. By the end, Justin got the worst-case walk down to 80ms, which is fast enough for our purposes. And that’s for the worst case; the common case of placing a seed on a fairly recent revision should take only a handful of milliseconds.

This project also nicely samples all the different kinds of work it requires to build production software. In addition to doing the algorithmic work, Justin was responsible for integration and testing: hooking traits into Iron, adding a UI for interacting with traits, and writing functional tests.

## Deriving Diffs

I’ve written [before](/self-adjusting-dom-and-diffable-data) about some of the ways in which diffs are an effective software engineering tool. One place it shows up a lot is in transferring data between systems efficiently and incrementally.

In particular, consider an application that has a master process that maintains a large and complex state, and a collection of worker processes that also maintain continuously updated copies of that state. Instead of transferring to the workers the entirety of the state whenever the master is updated, we’d rather just send diffs. To do that, we need types for representing diffs as well as code for computing diffs and applying patches.

Consider the following trivial record type.
    
    
    type t =
      { a: int
      ; b: float
      ; c: string
      }
    

You could write the following type to represent diffs to values of type `t`.
    
    
    type diff_t =
      | A of int
      | B of float
      | C of string
    

This highlights that there’s a mechanical relationship between the shape of the type and the shape of the diff type. Rather than having to write this kind of mechanical code by hand, for his intern project, Tomasz Syposz wrote a new syntax extension called `ppx_diff`, which creates both the types and the code for working with them automatically.

Much of the complexity of the project comes from thinking through all the corner cases, and understanding how one should construct a diff in each case. That includes handling the various different type constructors in OCaml, primarily records, variants and tuples. It also means thinking through how to deal with polymorphic types.

In addition, there are some design decisions that need to be left to the user. In particular, the code generator isn’t well positioned to make decisions about exactly how fine-grained the diffs should be. For example, if you have a nested record, like the following:
    
    
    type u =
      { foo: int
      ; bar: float
      }
    
    type t =
      { baz: u
      ; quuk: u
      }
    

Should the diff type go one level deep, like this:
    
    
    type diff_t = Baz of u | Quuk of u
    

Or two levels deep?
    
    
    type diff_u = Foo of int | Bar of float
    type diff_t = Baz of diff_u | Quuk of diff_u
    

Instead of deciding entirely on its own, `ppx_diff` has room for user annotations to decide when the diff granularity should go down to the next level of the data type.

All in, `ppx_diff` is a nice example of the power of syntactic abstractions. In this case, being able to operate at the level of syntax allows us to get rid of a huge amount of drudgery in a way that simply wouldn’t be possible in the host language on its own, while still maintaining the guarantees of a strongly typed protocol.

## Becoming an intern

This is just a taste of the kinds of projects that software development interns work on each summer at Jane Street. If you find these projects exciting, you should [apply](https://www.janestreet.com/join-jane-street/apply/)!

If it sounds like these projects require background you don’t have, don’t worry. You don’t have to know anything about functional programming or OCaml or the financial markets to join us for the summer. We’re are looking for smart and effective programmers and we are happy to teach them what they need to know.

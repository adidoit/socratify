---
title: "Reimplementing TCP/IP"
company: "janestreet"
url: "https://blog.janestreet.com/what-the-interns-have-wrought-2018/"
content_length: 16030
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Yet again, intern season is coming to a close, and so it’s time to look back at what the interns have achieved in their short time with us. I’m always impressed by what our interns manage to squeeze into the summer, and this year is no different.

There is, as you can imagine, a lot of ground to cover. With 45 interns between our NY, London and Hong Kong offices, there were a lot of exciting projects. Rather than trying to do anything even remotely exhaustive, I’m just going to summarize a handful of interesting projects, chosen to give a sense of the range of the work interns do.

The first project is about low-level networking: building the bones of a user-level TCP/IP stack. The second is more of a Linux-oriented security project: building out support for talking to various kernel subsytems via netlink sockets, to help configuration and management of firewalls. And the last is a project that I mentored, which has to do with fixing some old design mistakes in [Incr_dom](https://github.com/janestreet/incr_dom), our framework for building efficient JavaScript Web-UIs in OCaml.

(You should remember, every intern actually gets two projects, so this represents just half of what an intern might do here in a summer.)

# Reimplementing TCP/IP

Trading demands a lot in performance terms from our networking gear and networking code. Much of this has to do with how quickly exchanges generate marketdata. The US equity markets alone can peak at roughly 5 million messages per second, and volumes on the options markets are even higher.

For that reason, we end up using some pretty high-performance 10G (and 25G) network cards. But fast hardware isn’t enough; it’s hard to get really top-notch networking performance while going through the OS kernel. For that reason, several of these cards have user-space network stack implementations to go along with them.

But these implementations are a mixed bag. They work well, but the subtle variations in behavior between vendors make it hard to build portable code. And the need for these user-space layers to fit to traditional networking APIs means that it’s hard to get the maximum performance that is achievable by the hardware.

For this reason, we’ve been finding ourselves spending more time writing directly to lower-level, frame-oriented APIs that are exported by these cards. That’s relatively straightforward for a stateless protocol like UDP, but TCP is a different beast.

That’s where intern **Sam Kim** came in. He spent half the summer reading over a copy of _TCP/IP Illustrated_ (volumes [1](https://www.amazon.com/TCP-Illustrated-Protocols-Addison-Wesley-Professional/dp/0321336313/ref=sr_1_1?ie=UTF8&qid=1533592482&sr=8-1&keywords=tcp%2Fip+illustrated%2C+volume+1) and [2](https://www.amazon.com/TCP-IP-Illustrated-Implementation-Vol/dp/020163354X/ref=sr_1_3?ie=UTF8&qid=1533592482&sr=8-3&keywords=tcp%2Fip+illustrated%2C+volume+1)!), and building up a user-space TCP implementation in pure OCaml. He was able to leverage our existing APIs (and, critically, the testing framework we had in place for such protocols) to build up a new implementation of the protocol, optimized for our environment of fast local LANs. And he wrote a lot of tests, helping exercise many different aspects of the code.

This is not a small amount of work. TCP is a complex protocol, and there’s a lot of details to learn, including connection setup, retransmission, and congestion control.

One of the more exciting moments of this project was at the end, when, after doing all the testing, we connected Sam’s implementation to a real network card and ran it. After some small mistakes in wiring it up (not Sam’s mistakes, I should mention!) it worked without a hitch, and kept on working after he added a bunch of induced packet drops. Surely there’s more work to do on the implementation, but it’s an auspicious start.

# Talking to the Kernel via Netlink

We have an in-house, Linux-based firewall solution called nap-enforcer, which relies on the built-in stateful firewall functionality in Linux’s netfilter subsystem. Part of this stateful firewall support is the ability to keep track of the protocol state of connections going through the firewall, i.e., connection tracking, or conntrack for short. Conntrack is necessary for the correct handling of stateful protocols, like FTP.

When troubleshooting firewall issues, it’s helpful to be able to inspect and modify the tables that carry this state. We also want to be able to subscribe to events from conntrack and generate log messages for interesting changes, like a connection being open or closed.

This functionality can be controlled via a _netlink socket_ , which is a special kind of socket that enables message-oriented communication between userspace processes and the kernel.

Initially, we built nap-enforcer on top of the command-line `conntrack` utility. This worked well enough at first, but it doesn’t work well for subscribing to streams of events, and `conntrack` itself has some issues: it’s easy to crash it, and it’s inconsistent in its behavior, which just makes it hard to use.

**Cristian Banu’s** project was to fix this by writing an OCaml library that lets us talk directly to various kernel subsystems (primarily conntrack) over netlink sockets.

This is trickier than it might seem. Some of these interfaces are rather poorly documented, and existing C libraries don’t always offer very convenient APIs, so a large part of the job was reading the Linux kernel code to understand what really is happening and then figuring out a convenient and type-safe way to make this functionality available to OCaml. The resulting library offers a generic and safe high-level interface to netlink sockets, plus some abstractions built on top for specific netlink-based protocols.

One tricky corner of a high-level netlink API is providing a safe interface for constructing valid Netlink messages without making assumptions about the higher-level protocol. Cristian’s library wraps those computations in an [Atkey-style indexed monad](https://github.com/janestreet/base/blob/v0.11.1/src/monad_intf.ml#L222) which guarantees that the underlying C library (libmnl) is used in a safe way and that the resulting message is valid at the generic netlink level.

Cristian also worked out a way to have repeatable automated tests for the netlink library under our build system, [jenga](https://github.com/janestreet/jenga). This is a non-trivial problem because most of these kernel APIs require root access and kernel modules that aren’t loaded by default. His solution involves running tests in a network namespace with an owning user namespace that maps the unprivileged user running the test suite to the root user. This allows the test cases to use otherwise privileged network-related system calls, but only on the subset of network resources governed by the testing namespace.

The project is not yet finished, but the results are very promising, and we hope to move this to production over the next few months.

# Streamlining Incr_dom

For a while now, we’ve been using a library we developed internally, called [Incr_dom](https://github.com/janestreet/incr_dom), for building web front-ends in OCaml.

You can think of Incr_dom as a variation on [React](https://reactjs.org/) or the [Elm Architecture](https://guide.elm-lang.org/architecture/), except with a different approach to performance. A key feature of React and Elm is that they let you express your UI via simple data-oriented models plus simple functions that do things like compute the view you want to present, typically in the form of a so-called [virtual DOM](https://github.com/Matt-Esch/virtual-dom).

What Incr_dom adds to the mix is a lot of power to optimize the computations that need to be done when doing things like computing the view given the current value of the model. (Elm and React both have nice approaches to this as well, though they err on the side of having an easier to use optimization framework that isn’t as powerful.) This is important to us because of the nature of our business: trading applications often have complex, fast-changing models, and being able to render those efficiently is of central importance.

That’s why Incr_dom is built on Incremental, a library whose entire purpose is optimization. Incremental is good at constructing, well, [incremental computations](https://en.wikipedia.org/wiki/Incremental_computing), i.e., computations that only need to do a small amount of work when the input changes in small ways. The key is that Incremental lets you write your code so that it reads like a simple all-at-once computation, but executes like a hand-tuned, incremental one. Incremental computations are very useful when constructing UIs in this style, since your data model doesn’t typically change all at once.

I’ve written [more](https://blog.janestreet.com/incrementality-and-the-web/) than a [few](https://blog.janestreet.com/self-adjusting-dom/) blog [posts](https://blog.janestreet.com/self-adjusting-dom-and-diffable-data/) about the basic ideas, and since then, we actually had some interns do [much of the work](https://blog.janestreet.com/what-the-interns-have-wrought-2016/) of getting it up and running. But that initial design had some sharp edges that we didn’t know how to fix. And that’s where **Jeanne Luning Prak’s** project this year came in.

The key problem with the original design was something called the “derived model”. To understand where the derived model comes into play, you need to know a bit more about Incr_dom. An Incr_dom app needs to know how to do more than how to render its model. Here’s a simplified version of the interface that a simple Incr_dom app needs to satisfy which shows a bit more of the necessary structure.
    
    
    module type App = sig
      type model
      type action
      
      val view : model Incr.t -> schedule:(action -> unit) -> Vdom.t Incr.t
    
      val apply_action : model -> action -> model
    end
    

The `view` function is what we described above. It takes as its input an incremental model, and returns an incremental virtual-dom tree. Note that it also takes a function argument, called `schedule`, whose purpose is to allow the virtual-dom to have embedded callbacks that can in turn trigger actions that update the model. This is essentially how you wire up a particular behavior to, say, a button click.

Those actions are then applied to the model using the provided `apply_action` function. This all works well enough for cases where the required optimization is fairly simple. But it has real limitations, because the `apply_action` function, unlike the `view` function, isn’t incremental.

To see why this is important, imagine you have a web app that’s rendering a bunch of data in a table, where that table is filtered and sorted inside of the browser. The filtering and sorting can be done incrementally in the `view` function, so that changing data can be handled gracefully. But ideally, you’d like for the `apply_action` function to have access to some of the same data computed by `view`. In particular, if you define an action that moves you to the next row, the identity of that row depends on how the data has been sorted and filtered. And you don’t want to recompute this data every time someone wants to move from one row to the next.

In the initial design, we came up with a somewhat inelegant solution, which was to add a new type, the _derived model_ , which is computed incrementally, and then shared between the `view` and `apply_action` functions. The resulting interface looks something like this:
    
    
    module type App = sig
      type model
      type derived_model
      type action
      
      val derive : model Incr.t -> derived_model Incr.t
    
      val view
        :  model Incr.t
        -> derived_model Incr.t
        -> schedule:(action -> unit)
        -> Vdom.t Incr.t
    
      val apply_action
        :  model
        -> derived_model
        -> action
        -> model
    end
    

And this works. You can now structure your application so that the information that both the view and the action-application function need to know can be shared in this derived model.

But while it works, it’s awkward. Most applications don’t need a derived model, but once any component needs to use it, every intermediate part of your application now has to think about and handle the derived model as well.

I came into the summer with a plan for how to resolve this issue. On some level, what we really want is a compiler optimization. Ideally, both `view` and `apply_action` would be incremental functions, say, with this signature:
    
    
    module type App = sig
      type model
      type action
      
      val view : model Incr.t -> schedule:(action -> unit) -> Vdom.t Incr.t
    
      val apply_action : model Incr.t -> action Incr.t -> model Incr.t
    end
    

Then, both `apply_action` and `view` can independently compute what they need to know about the row structure, and do so incrementally. At that point there’s only one problem left: these computations are incremental, but they’re still being duplicated.

But that’s easy enough to fix, I thought: we can do some form of clever common-subexpression elimination. The basic idea was to cache some computations in a way that when `view` and `apply_action` tried to compute the very same thing, they would end up with a single copy of the necessary computation graph, rather than two.

This turned out to be complicated for a few reasons, one of them being the rather limited nature of JavaScript’s support for weak references, which are needed to avoid memory leaks.

Luckily, Jeanne had a better idea. Rather than some excessively clever computation-sharing, we could just change the shape of the API. Instead of having separate functions for `view` and `apply_action`, we would have one function that computed both. To that end, she created a new type, a `Component.t`, which had both the `view` and the `apply_action` logic. The type is roughly this:
    
    
    module Component : sig
       type ('model,'action) t =
          { view : Vdom.t
          ; apply_action : 'action -> 'model }
    end
    

And now, the app interface looks like this:
    
    
    module type App = sig
      type model
      type action
      
      val create
        :  model Incr.t
        -> schedule:(action -> unit)
        -> (action,model) Component.t Incr.t
    end
    

Because `create` is a single function, it can behind the scenes structure the computation any way it wants, and so can share work between the computation of the view and the computation of the action-application function.

This turned out to be a really nice design win, totally eliminating the concept of the derived model and making the API a lot simpler to use. And she’s gotten to see the full lifecycle of the project: figuring out how to best fix the API, implementing the change, testing it, documenting it, and figuring out how to smash the tree to upgrade everyone to the new world.

And actually, this is only about half of what Jeanne did in this half of the summer. Her other project was to write a syntax extension to create a special kind of incremental pattern-match, which has applications for any use of Incremental, not just for UIs. That should maybe be the subject of another blog post.

# Apply to be an intern!

I hope this gives you a sense of the nature and variety of the work that interns get to do, as well as a sense of the scope and independence that they get in choosing how to tackle these problems.

If this sounds like a fun way to spend the summer, you should [apply](https://www.janestreet.com/join-jane-street/apply/)! And in case you’re wondering: no, you don’t need to be a functional programming wizard, or have ever programmed in OCaml, or know anything about finance or trading, to be an intern. Most of our interns come in with none of that, and they still do great things!

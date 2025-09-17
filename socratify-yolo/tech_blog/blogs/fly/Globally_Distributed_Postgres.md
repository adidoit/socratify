---
title: "Globally Distributed Postgres"
company: "fly"
url: "https://fly.io/blog/globally-distributed-postgres/"
content_length: 15567
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Author
     ![Kurt Mackey](/static/images/kurt.webp)

Name
     Kurt Mackey 
@mrkurt
     [ @mrkurt ](https://twitter.com/mrkurt)
Author
     ![Kurt Mackey](/static/images/kurt.webp)

Name
     Kurt Mackey 
@mrkurt
     [ @mrkurt ](https://twitter.com/mrkurt)
![](/blog/globally-distributed-postgres/assets/cats-around-the-world.webp) Image by [ Annie Ruygt ](https://annieruygtillustration.com/)

Fly runs apps (and databases) close to users, by taking Docker images and transforming them into Firecracker micro-vms running on our hardware around the world. You should try deploying an app: [it only takes a few minutes](https://fly.io/docs/speedrun/).

This is a story about a cool hack we came up with at Fly. The hack lets you do something pretty ambitious with full-stack applications. What makes it cool is that it’s easy to get your head around, and involves just a couple moving parts, assembled in a simple but deceptively useful way. We won’t bury the lede: we’re going to talk about how you can deploy a standard CRUD application with globally-replicated Postgres, **for both reads and writes** , using standard tools and a simple Fly feature.

If you’ve build globally distributed apps in the past, you’re probably familiar with the challenges. It’s easy to scale out a database that’s only ever read from. Database engines have features to stand up “read replicas”, for high-availability and caching, so you can respond to incoming read requests quickly. This is great: you’re usually more sensitive to the performance of reads, and normal apps are grossly read-heavy. 

But these schemes break down when users do things that update the database. It’s easy to stream updates from a single writer to a bunch of replicas. But once writes can land on multiple instances, mass hysteria! Distributed writes are hard. 

Application frameworks like Rails have features that address this problem. Rails will let you automatically switch database connections, so that you can serve reads quickly from a local replica, while directing writes to a central writer. But they’re painful to set up, and deliberately simplified; the batteries aren’t included. 

Our read/write hack is a lot simpler, involves very little code, and it’s easy to understand. Let’s stick with the example of a standard Rails application (a difficult and common case) and dive in.

### When Your Only Tool Is A Front-End Proxy, Every Problem Looks Like An HTTP Header

You can think of Fly.io as having two interesting big components. We have a system for transforming Docker containers into fast, secure Firecracker micro-VMs. And we have a global CDN built around our Rust front-end proxy. 

We run all kinds of applications for customers here. Most interesting apps want some kind of database. We want people to run interesting apps here, and so we provide Fly Postgres: instances of Postgres, deployed automatically in read-replica cluster configurations. If your application runs in Dallas, Newark, Sydney and Frankfurt, it’s trivial to tell us to run a Postgres writer in Dallas and replicas everywhere else. 

Fly has a lot of control over how requests are routed to instances, and little control over how instances handle those requests. We can’t reasonably pry open customer containers and enable database connection-switching features for users, nor would anyone want us to. 

You can imagine an ambitious CDN trying to figure out, on behalf of its customers, which requests are reads and writes. The GETs and HEADs are reads! Serve them in the local region! The POSTs and DELETEs are writes! Send them to Dallas! Have we solved the problem? Of course not: you can’t look at an HTTP verb and assume it isn’t going to ask for a database update. Most GETs are reads, but not all of them. The platform has to work for all the requests, not just the orthodox ones.

So, short of getting in between the app and its database connection and doing something really gross, we’re in a bit of a quandary.

A bit more on “gross” here: you can get your database layer to do this kind of stuff for you directly, using something like [pgpool](https://www.pgpool.net/docs/latest/en/html/runtime-config-load-balancing.html) so that the database layer itself knows where to route transactions. But there’s a problem with this: your app doesn’t expect this to happen, and isn’t built to handle it. What you see when you try routing writes at the database connection layer is something like this:

  1. A read query for data, from read replica, perhaps for validation: **0ms**. 🤘

  2. A write to the primary, in a different region: **20-400ms**. 😦

  3. A read query to the primary, for consistency, in a different region: **20-400ms**. 🙀

  4. More read queries against primary for consistency, in a different region: **20-400ms**. 😱

  5. Maybe another write to the primary: **20-400ms**. 😵

  6. Repeat ☠️.




It is much, much faster to ship the whole HTTP request where it needs to be than it is move the database away from an app instance and route database queries directly. Remember: replay is happening _with Fly’s network_. HTTP isn’t bouncing back and forth between the user and our edge (that would be slow); it’s happening inside our CDN.

It turns out, though, that with just a little bit of cooperation from the app, it’s easy to tell reads from writes. The answer is: every instance assumes it can handle every request, even if it’s connected to a read replica. Most of the time, it’ll be right! Apps are read-heavy! 

When a write request comes in, just try to do the write, like a dummy. If the writer is in Dallas and the request lands in Frankfurt, the write fails; you can’t write to a read replica. Good! That failure will generate a predictable exception. Just catch it:

Wrap text  Copy to clipboard 
    
    
    rescue_from ActiveRecord::StatementInvalid do |e|
      if e.cause.is_a?(PG::ReadOnlySqlTransaction)
        r = ENV["PRIMARY_REGION"]
        response.headers["fly-replay"] = "region=#{r}"
        Rails.logger.info "Replaying request in #{r}"
        render plain: "retry in region #{r}", status: 409
      else
        raise e
      end
    end
    

In 8 lines of code, we catch the read-only exceptions and spit out a `fly-replay` header, which tells our proxy to retry the same request in the writer’s region. 

You could imagine taking this from 8 lines of code to 1, by packaging this logic up in a gem. That’s probably a good idea. The theme in this blog post though is that all the machinery we’re using to make this work is simple enough to keep in your head.

Our proxy does the rest of the work. The user, none the wiser, has their write request served from Dallas. Everything… works?

## The Fly-Replay Header

This design isn’t why we built the `fly-replay` feature into our proxy.

The problem we were originally aiming at with the header was load balancing. We have clients that serve several hundred million images a day off Fly. And, some time ago, we had incidents where all their traffic would get routed to out-of-the-way places, like Tokyo, which struggled (ie: melted) to keep up with the load. 

The immediate routing issues were easy to fix. But they weren’t the real problem. Even as traffic was getting sent to overloaded Tokyo servers, we had tons of spare capacity in other nearby regions. Obviously, what we want to do is spread the load to that spare capacity. 

But the obvious solutions to that problem don’t work as well as you’d assume in practice. You can’t just have Tokyo notice it’s overloaded and start sending all its traffic to Singapore. Now Singapore is melting! What’s worse, traffic load is an eventual consistency problem, and the farther away an unloaded region is from Tokyo, the less likely it is that Tokyo can accurately and instantaneously predict its load. 

Here’s the thing, though: HTTP is cheap, especially when you’ve got persistent connections (the backhaul between our edges and the workers where apps actually run is HTTP2). 

And so, `fly-replay`. When a request hits Tokyo, we estimate which process has capacity based on gossiped load data. We then send the request to the server running that process. _Then_ we check to see if the process still has capacity. If it does, great, we dump the request into the user process. If it doesn’t, we send a reply to the edge server saying “hey, this process is full, try another”. The effect is something we call latency shedding: if we can try every instance of an app process quickly enough we’ll always be able to service a request.

### You can see this in action.

If this stuff is interesting to you, check out [this simple Rails app we put together](https://fly-global-rails.fly.dev/) (maybe we’ve mentioned that it’s ridiculously easy to boot apps up on Fly?). What you’re looking at is a globally deployed stock Rails app that explicitly steers the database with `fly-replay`. You’re landing on an instance of the application because our BGP Anycast routes took you there; for me, my connecting region is Chicago. But you can tell the app to replay your request in a bunch of other regions; click the tabs.

## 80% Of The Time It Works Every Time

Whether you understand it in your bones or not, a big part of why you’re using a database like Postgres is that you want strong consistency. Strongly consistent databases are easy to work with. You issue a write to a consistent database, and then a read, and the read sees the result of a write. When you lose this feature, things get complicated fast, which is part of why people often prefer to scale up single database servers rather than scaling them out.

Obviously, once you start routing database (or HTTP) requests to different servers based on local conditions, you’ve given up some of that consistency. We can’t bend the laws of physics! When you read from Frankfurt and then write to Dallas, Dallas will quickly replicate the altered rows to Frankfurt, but not instantly. There’s a window of inconsistency.

We have a couple of responses to this.

First, in a lot of cases, it might not matter. There are large classes of applications where short inconsistencies between writes and subsequent reads aren’t a big problem. Data replicates fast enough that your users probably won’t see inconsistencies. If displaying stale data doesn’t cause real problems, maybe worry about it another time.

Second, if you want “read-your-own-writes-between-requests” behavior, you can implement that with the same header. When you set `fly-replay` to the writer, set a timestamp in the user’s session, during which you fly-replay all the requests. HTTP is cheap! 

Third, you could simulate synchronous replication. _Actual_ synchronous replication doesn’t work well on cross-geo clusters, but Postgres does let you see query replica freshness. [We run these kinds of queries for health checks](https://github.com/fly-apps/postgres-ha/blob/main/cmd/flycheck/pg.go#L121-L151). You could build a little logic into your app to check the replication lag on the user’s region and delay the HTTP response until it’s ready.

Finally, though, it’s just the case that this pattern won’t work for every application. It’s neat, and it makes Postgres read-replicas much easier to use, but it isn’t a cure-all.

# flyctl postgres create

That’s it. That’s the tweet. One command gets you a multi-database-capable Postgres cluster, with high-availability read replicas, in whichever regions you want us to run it in.

[ Try Fly for free → ](https://fly.io/docs/speedrun/)

![](/static/images/cta-cat.webp)

## Maybe Your App is Actually Write Heavy

There are database engines designed handle distributed write scenarios, some with native geographic partitioning – and you can use them on Fly, too.

Have you seen CockroachDB? It’s amazing. CockroachDB gives developers all the tools they need to model geographic distribution into their schemas. With the right schema, Cockroach moves the chunks of data close to the most active users and keep writes wicked fast. You’ll need the Enterprise edition to really take advantage of this, but it’s legit. 

Generally, if you’re prepared to manage your own database, [you can deploy it on Fly](https://github.com/fly-apps/cockroachdb) by attaching volumes to your instances; volumes are arbitrarily-sized block devices and some rules that we enforce in the background to pin your app to worker hosts where those volumes live. Volumes are the storage fabric on which our Postgres is built, and you can just build directly on them.

So you can see the outline of two big approaches here: you can configure Postgres (or, rather, we can configure Postgres for you) to deploy in a configuration where you’re distributed _enough_ to get 90% of the benefit of distribution, and, if that works for you, you can stick with Postgres, which is great because everybody loves Postgres, and because Postgres is what your existing apps already do.

Or, you can deploy on distributed-by-design databases like Cockroach, where databases are split into geographically distributed regions and concurrency is managed by Raft consensus.

## And That’s It

Multi-reader, single-writer Postgres configurations aren’t a new thing. Lots of people use them. But they’re annoying to get working, especially if you didn’t start building your application knowing you were going to need them.

If you’re scaling out Postgres instead of scaling it up, there’s a good chance you’re doing it because you want to scale your application geographically. That’s why people use Fly.io; it’s our whole premise. We do some lifting to make sure that running an app close to your users on Fly.io doesn’t involve a lot of code changes. This strategy, of exploiting our proxy to steer database writes, is sort of in keeping with that idea.

It should work with other databases too! There’s no reason we can see why you can’t use the same trick to get MySQL read replicas working this way. If you play around with doing that on Fly.io, [please tell us about it at our community site](https://community.fly.io/).

Meanwhile, if you’re averse to science projects, we think we’re on track to become the simplest conceivable way to hook a full-stack application up to a scalable Postgres backend. Give it a try.

* * *

Want to know more? [Join the discussion](https://community.fly.io/t/multi-region-database-guide/1600).

Last updated 
•      Jun 30, 2021 
[ Share this post on Twitter ](https://twitter.com/share?text=Globally Distributed Postgres&url=https://fly.io/blog/globally-distributed-postgres/&via=flydotio) [ Share this post on Hacker News ](http://news.ycombinator.com/submitlink?u=https://fly.io/blog/globally-distributed-postgres/&t=Globally Distributed Postgres) [ Share this post on Reddit ](http://www.reddit.com/submit?url=https://fly.io/blog/globally-distributed-postgres/&title=Globally Distributed Postgres)

Author
     ![Kurt Mackey](/static/images/kurt.webp)

Name
     Kurt Mackey 
@mrkurt
     [ @mrkurt ](https://twitter.com/mrkurt)
Author
     ![Kurt Mackey](/static/images/kurt.webp)

Name
     Kurt Mackey 
@mrkurt
     [ @mrkurt ](https://twitter.com/mrkurt)

Next post ↑ 
     [ FYI: Livebook 0.2 with Kino ](/blog/livebook-with-kino/)
Previous post ↓ 
     [ Monitoring Elixir Apps on Fly.io With Prometheus and PromEx ](/blog/monitoring-your-fly-io-apps-with-prometheus/)

Next post ↑ 
     [ FYI: Livebook 0.2 with Kino ](/blog/livebook-with-kino/)
Previous post ↓ 
     [ Monitoring Elixir Apps on Fly.io With Prometheus and PromEx ](/blog/monitoring-your-fly-io-apps-with-prometheus/)

---
title: "How Discord Scaled Elixir to 5,000,000 Concurrent Users"
company: "discord"
url: "https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users"
type: "direct_systems_collection"
date: "2025-09-15"
---

From the beginning, Discord has been an early adopter of Elixir. The Erlang VM was the perfect candidate for the highly concurrent, real-time system we were aiming to build. We developed the original prototype of Discord in Elixir; that became the foundation of our infrastructure today. Elixir’s promise was simple: access the power of the Erlang VM through a much more modern and user-friendly language and toolset.

Fast forward two years, and we are up to nearly **five million concurrent users** and **millions of events per second** flowing through the system. While we don’t have any regrets with our choice of infrastructure, we did have to do a lot of research and experimentation to get here. Elixir is a new ecosystem, and the Erlang ecosystem lacks information about using it in production (although [Erlang in Anger](https://www.erlang-in-anger.com/) is awesome). What follows is a set of lessons learned and libraries created throughout our journey of making Elixir work for Discord.

### Message Fanout

While Discord is rich with features, most of it boils down to pub/sub. Users connect to a WebSocket and spin up a session process (a GenServer), which then communicates with remote Erlang nodes that contain guild (internal for a “Discord Server”) processes (also GenServers). When anything is published in a guild, it is fanned out to every session connected to it.

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/612402838c03b687ecc16d55_1*R4RGQCxpeFo2gZB41Zbu9w.gif)

When a user comes online, they connect to a guild, and the guild publishes a presence to all other connected sessions. Guilds have a lot of other logic behind the scenes, but here’s a simplified example:

This was a fine approach when we originally built Discord to groups of 25 of less. However, we have been fortunate enough to have “good problems” arise as [people started using Discord for large scale groups](https://facebook.github.io/react/blog/2015/10/19/reactiflux-is-moving-to-discord.html). Eventually we ended up with many Discord servers like [/r/Overwatch](https://www.reddit.com/r/Overwatch/) with up to 30,000 concurrent users. During peak hours, we began to see these processes fail to keep up with their message queues. At a certain point, we had to manually intervene and turn off features that generated messages to help cope with the load. We had to figure this out before it became a full-time job.

We began by [benchmarking](https://github.com/alco/benchfella) hot paths within the guild processes and quickly stumbled onto an obvious culprit. Sending messages between Erlang processes was not as cheap as we expected, and the reduction cost — Erlang unit of work used for process scheduling — was also quite high. We found that the wall clock time of a single send/2 call could range from 30μs to 70us due to Erlang de-scheduling the calling process. This meant that during peak hours, publishing an event from a large guild could take anywhere from 900ms to 2.1s! Erlang processes are effectively single threaded, and the only way to parallelize the work is to shard them. That would have been quite an undertaking, and we knew there had to be a better way.

We knew we had to somehow distribute the work of sending messages. Since spawning processes in Erlang is cheap, our first guess was to just spawn another process to handle each publish. However, each publish could be scheduled at a different time, and Discord clients depend on linearizability of events. That solution also wouldn’t scale well because the guild service was also responsible for an ever-growing amount of work.

Inspired by a [blog post](http://www.ostinelli.net/boost-message-passing-between-erlang-nodes/) about boosting performance of message passing between nodes, [Manifold](https://github.com/hammerandchisel/manifold) was born. Manifold distributes the work of sending messages to the remote nodes of the PIDs (Erlang process identifier), which guarantees that the sending processes at most only calls send/2 equal to the number of involved remote nodes. Manifold does this by first grouping PIDs by their remote node and then sending to Manifold.Partitioner on each of those nodes. The partitioner then consistently hashes the PIDs using :erlang.phash2/2, groups them by number of cores, and sends them to child workers. Finally, those workers send the messages to the actual processes. This ensures the partitioner does not get overloaded and still provides the linearizability guaranteed by send/2. This solution was effectively a drop-in replacement for send/2:

An awesome side-effect of Manifold was that we were able to not only distribute the CPU cost of fanning out messages, but also reduce the network traffic between nodes:

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61240284f45c7e110039b18b_0*tDxgj1LH9PE-BZsz.png)

_Network Reduction on 1 Guild Node_

Manifold is available on our GitHub, so give it a spin. <https://github.com/discordapp/manifold>.

### Fast Access Shared Data

Discord is a distributed system achieved through [consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing). Using this method requires us to create a ring data structure that can be used to lookup the node of a particular entity. We want that to be fast, so we chose the wonderful [library by Chris Moos](https://github.com/chrismoos/hash-ring) via a Erlang C port (process responsible for interfacing with C code). It worked great for us, but as Discord scaled, we started to notice issues when we had bursts of users reconnecting. The Erlang process responsible for controlling the ring would start to get so busy that it would fail to keep up with requests to the ring, and the whole system would become overloaded. The solution at first seemed obvious: run multiple processes with the ring data to better utilize all the machine’s cores to answer the requests. However, we noticed that this was a hot path. Could we do better?

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6124028442d2a3304ba031b2_1*UcM21Vu8CeoYLKuYIn-d5A.gif)

Let’s break down the cost of this hot path.

  * A user can be in any number of guilds, but an average user is in 5.
  * An Erlang VM responsible for sessions can have up to 500,000 live sessions on it.
  * When a session connects, it has to lookup the remote node for each guild it is interested in.
  * The cost of communicating with another Erlang process using request/reply is about 12μs.



If the session server were to crash and restart, it would take about 30 seconds just for the cost of lookups on the ring. That does not even account for Erlang de-scheduling the single process involved in the ring for other processes’ work. Could we remove this cost completely?

The first thing people do in Elixir when they want to speed up data access is to introduce [ETS](http://erlang.org/doc/man/ets.html). ETS is a fast, mutable dictionary implemented in C; the tradeoff is that data is copied in and out of it. We couldn’t just move our ring into ETS because we were using a C port to control the ring, so [we converted the code to pure Elixir](https://github.com/hammerandchisel/ex_hash_ring). Once that was implemented, we had a process whose job was to own the ring and constantly copy it into ETS so other processes could read directly from ETS. This noticeably improved performance, but ETS reads were about 7μs, and we were still spending 17.5 seconds on looking up values in the ring. The ring data structure is actually fairly large, and copying it in and out of ETS was the majority of the cost. We were disappointed; in any other language we could easily just have a shared value that was safe to read. There had to be a way to do this in Erlang!

After doing some research, we found [mochiglobal](https://github.com/mochi/mochiweb/blob/master/src/mochiglobal.erl), a module that exploits a feature of the VM: if Erlang sees a function that always returns the same constant data, it puts that data into a read-only shared heap that processes can access without copying the data. mochiglobal takes advantage of this by creating an Erlang module with one function at runtime and compiling it. Since the data is never copied, the lookup cost decreases to 0.3us, bringing the total time down to **750ms**! There’s no such thing as a free lunch though; the cost of building a module with a data structure as large as the ring at runtime can take up to a second. The good news is that we rarely change the ring, so it was a penalty we were willing to take.

We decided to port mochiglobal to Elixir and add some functionality to avoid creating atoms. Our version is called FastGlobal and is available at <https://github.com/discordapp/fastglobal>.

### Limited Concurrency

After solving the performance of the node lookup hot path, we noticed that the processes responsible for handling guild_pid lookup on the guild nodes were getting backed up. The inherent back pressure of the slow node lookup had previously protected these processes. The new problem was that nearly 5,000,000 session processes were trying to stampede ten of these processes (one on each guild node). Making this path faster wouldn’t solve the problem; the underlying issue was that the call of a session process to this guild registry would timeout and leave the request in the queue of the guild registry. It would then retry the request after a backoff, but perpetually pile up requests and get into an unrecoverable state. Sessions would block on these requests until they timed out while receiving messages from other services, causing them to balloon their message queues and eventually OOM the whole Erlang VM resulting in [cascading service outages](https://status.discordapp.com/incidents/dj3l6lw926kl).

We needed to make session processes smarter; ideally, they wouldn’t even try to make these calls to the guild registry if a failure was inevitable. We didn’t want to use a [circuit breaker](https://en.wikipedia.org/wiki/Circuit_breaker_design_pattern) because we didn’t want a burst in timeouts to result in a temporary state where no attempts are made at all. We knew how we would solve this in other languages, but how would we solve it in Elixir?

In most other languages, we could use an atomic counter to track outstanding requests and bail early if the number was too high, effectively implementing a semaphore. The Erlang VM is built around coordinating through communication between processes, but we knew we didn’t want to overload a process responsible for doing this coordination. After some research we stumbled upon :ets.update_counter/4**,** which performs atomic conditional increment operations on a number inside an ETS key. Since we needed high concurrency, we could also run ETS in write_concurrency mode but still read the value out, since :ets.update_counter/4**** returns the result. This gave us the fundamental piece to create our [Semaphore](https://github.com/hammerandchisel/semaphore) library. It is extremely easy to use and performs really well at high throughput:

This library has proved instrumental in protecting our Elixir infrastructure. A similar situation to the aforementioned cascading outages occurred as recently as last week, but there were no outages this time. Our presence services crashed due to an unrelated issue, but the session services did not even budge, and the presence services were able to rebuild within minutes after restarting:

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61240284fa047bc8bbc52c6a_0*vQF45QgC60mIsfaw.png)

_Live presences within presence service_

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61240284c6822095978617f6_0*2KspurjfjWgjW7BV.png)

 _CPU usage on the session services around the same time period._

You can find our Semaphore library on GitHub at <https://github.com/discordapp/semaphore>.

### Conclusion

Choosing to use and getting familiar with Erlang and Elixir has proven to be a great experience. If we had to go back and start over, we would definitely choose the same path. We hope that sharing our experiences and tools proves useful to other Elixir and Erlang developers, and we hope to continue sharing as we progress on our journey, solving problems and learning lessons along the way.

_We are hiring, so_[ _come join us_](https://discordapp.com/jobs) _if this type of stuff tickles your fancy._

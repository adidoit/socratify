---
title: "How Discord Stores Trillions of Messages"
company: "discord"
url: "https://discord.com/blog/how-discord-stores-trillions-of-messages"
type: "direct_systems_collection"
date: "2025-09-15"
---

![The Discord logo surrounded by representations of chat messages. They look to be shooting out from the Discord logo.](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/640658a746a8ce16d18f27ac_027_Header.png)

Engineering & Developers

# How Discord Stores Trillions of Messages

![Bo Ingram](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/640664069a8b908442f19f7b_Bo%27s%20Photo.jpg)

Bo Ingram

March 6, 2023

In 2017, we wrote a blog post on [how we store billions of messages.](https://discord.com/blog/how-discord-stores-billions-of-messages) We shared our journey of how we started out using MongoDB but migrated our data to Cassandra because we were looking for a database that was scalable, fault-tolerant, and relatively low maintenance. We knew we’d be growing, and we did!

We wanted a database that grew alongside us, but hopefully, its maintenance needs wouldn’t grow alongside our storage needs. Unfortunately, we found that to not be the case — our Cassandra cluster exhibited serious performance issues that required increasing amounts of effort to just maintain, not improve.

Almost six years later, we’ve changed a lot, and how we store messages has changed as well.  
‍

## Our Cassandra Troubles

We stored our messages in a database called cassandra-messages. As its name suggests, it ran Cassandra, and it stored messages. In 2017, we ran 12 Cassandra nodes, storing billions of messages.

At the beginning of 2022, it had 177 nodes with trillions of messages. To our chagrin, it was a high-toil system — our on-call team was frequently paged for issues with the database, latency was unpredictable, and we were having to cut down on maintenance operations that became too expensive to run.

What was causing these issues? First, let’s take a look at a message.

The CQL statement above is a minimal version of our message schema. Every ID we use is a [Snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake), making it chronologically sortable. We partition our messages by the channel they’re sent in, along with a bucket, which is a static time window. This partitioning means that, in Cassandra, all messages for a given channel and bucket will be stored together and replicated across three nodes (or whatever you’ve set the replication factor).

Within this partitioning lies a potential performance pitfall: a server with just a small group of friends tends to send orders of magnitude fewer messages than a server with hundreds of thousands of people.

In Cassandra, reads are more expensive than writes. Writes are appended to a commit log and written to an in memory structure called a memtable that is eventually flushed to disk. Reads, however, need to query the memtable and potentially multiple SSTables (on-disk files), a more expensive operation. Lots of concurrent reads as users interact with servers can hotspot a partition, which we refer to imaginatively as a “hot partition”. The size of our dataset when combined with these access patterns led to struggles for our cluster.

When we encountered a hot partition, it frequently affected latency across our entire database cluster. One channel and bucket pair received a large amount of traffic, and latency in the node would increase as the node tried harder and harder to serve traffic and fell further and further behind.

Other queries to this node were affected as the node couldn’t keep up. Since we perform reads and writes with quorum consistency level, all queries to the nodes that serve the hot partition suffer latency increases, resulting in broader end-user impact.

Cluster maintenance tasks also frequently caused trouble. We were prone to falling behind on compactions, where Cassandra would compact SSTables on disk for more performant reads. Not only were our reads then more expensive, but we’d also see cascading latency as a node tried to compact.

We frequently performed an operation we called the “gossip dance”, where we’d take a node out of rotation to let it compact without taking traffic, bring it back in to pick up hints from Cassandra’s hinted handoff, and then repeat until the compaction backlog was empty. We also spent a large amount of time tuning the JVM’s garbage collector and heap settings, because GC pauses would cause significant latency spikes.  
‍

## Changing Our Architecture

Our messages cluster wasn’t our only Cassandra database. We had several other clusters, and each exhibited similar (though perhaps not as severe) faults.

In our [previous iteration of this post](https://discord.com/blog/how-discord-stores-billions-of-messages), we mentioned being intrigued by ScyllaDB, a Cassandra-compatible database written in C++. Its promise of better performance, faster repairs, stronger workload isolation via its shard-per-core architecture, and a garbage collection-free life sounded quite appealing.

Although ScyllaDB is most definitely not void of issues, it is void of a garbage collector, since it’s written in C++ rather than Java. Historically, our team has had many issues with the garbage collector on Cassandra, from GC pauses affecting latency, all the way to super long consecutive GC pauses that got so bad that an operator would have to manually reboot and babysit the node in question back to health. These issues were a huge source of on-call toil, and the root of many stability issues within our messages cluster.

After experimenting with ScyllaDB and observing improvements in testing, we made the decision to migrate all of our databases. While this decision could be a blog post in itself, the short version is that by 2020, we had migrated every database but one to ScyllaDB.

The last one? Our friend, cassandra-messages.

Why hadn’t we migrated it yet? To start with, it’s a big cluster. With trillions of messages and nearly 200 nodes, any migration was going to be an involved effort. Additionally, we wanted to make sure our new database could be the best it could be as we worked to tune its performance. We also wanted to gain more experience with ScyllaDB in production, using it in anger and learning its pitfalls.

We also worked to improve ScyllaDB performance for our use cases. In our testing, we discovered that the performance of reverse queries was insufficient for our needs. We execute a reverse query when we attempt a database scan in the opposite order of a table’s sorting, such as when we scan messages in ascending order. The ScyllaDB team prioritized improvements and implemented performant reverse queries, removing the last database blocker in our migration plan.

We were suspicious that slapping a new database on our system wasn’t going to make everything magically better. Hot partitions can still be a thing in ScyllaDB, and so we also wanted to invest in improving our systems upstream of the database to help shield and facilitate better database performance.  
‍

## Data Services Serving Data

With Cassandra, we struggled with hot partitions. High traffic to a given partition resulted in unbounded concurrency, leading to cascading latency in which subsequent queries would continue to grow in latency. If we could control the amount of concurrent traffic to hot partitions, we could protect the database from being overwhelmed.

To accomplish this task, we wrote what we refer to as data services — intermediary services that sit between our API monolith and our database clusters. When writing our data services, we chose a language we’ve been using [more and more at Discord](https://discord.com/blog/why-discord-is-switching-from-go-to-rust): Rust! We’d used it for a few projects previously, and it lived up to the hype for us. It gave us fast C/C++ speeds without having to sacrifice safety.

Rust touts fearless concurrency as one of its main benefits — the language should make it easy to write safe, concurrent code. Its libraries also were a great match for what we were intending to accomplish. The [Tokio ecosystem](https://tokio.rs/) is a tremendous foundation for building a system on asynchronous I/O, and the language has driver support for both Cassandra and ScyllaDB.

Additionally, we found it a joy to code in with the help the compiler gives you, the clarity of the error messages, the language constructs, and its emphasis on safety. We became quite fond of how once it compiled, it generally works. Most importantly, however, it lets us say we rewrote it in Rust (meme cred is very important).

Our data services sit between the API and our ScyllaDB clusters. They contain roughly one gRPC endpoint per database query and intentionally contain no business logic. The big feature our data services provide is request coalescing. If multiple users are requesting the same row at the same time, we’ll only query the database once. The first user that makes a request causes a worker task to spin up in the service. Subsequent requests will check for the existence of that task and subscribe to it. That worker task will query the database and return the row to all subscribers.

This is the power of Rust in action: it made it easy to write safe concurrent code.

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6406629e7ba3569d3c32c8ed_Example%201%402x.png)

Let’s imagine a big announcement on a large server that notifies @everyone: users are going to open the app and read the message, sending tons of traffic to the database. Previously, this might lead to a hot partition, and on-call would potentially need to be paged to help the system recover. With our data services, we’re able to significantly reduce traffic spikes against the database.

The second part of the magic here is upstream of our data services. We implemented consistent hash-based routing to our data services to enable more effective coalescing. For each request to our data service, we provide a routing key. For messages, this is a channel ID, so all requests for the same channel go to the same instance of the service. This routing further helps reduce the load on our database.

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/640662a51e3e13599d292404_Example%202%402x.png)

These improvements help a lot, but they don’t solve all of our problems. We’re still seeing hot partitions and increased latency on our Cassandra cluster, just not quite as frequently. It buys us some time so that we can prepare our new optimal ScyllaDB cluster and execute the migration.  
‍

## A Very Big Migration

Our requirements for our migration are quite straightforward: we need to migrate trillions of messages with no downtime, and we need to do it quickly because while the Cassandra situation has somewhat improved, we’re frequently firefighting.

Step one is easy: we provision a new ScyllaDB cluster using our [super-disk storage topology](https://discord.com/blog/how-discord-supercharges-network-disks-for-extreme-low-latency). By using Local SSDs for speed and leveraging RAID to mirror our data to a persistent disk, we get the speed of attached local disks with the durability of a persistent disk. With our cluster stood up, we can begin migrating data into it.

Our first draft of our migration plan was designed to get value quickly. We’d start using our shiny new ScyllaDB cluster for newer data using a cutover time, and then migrate historical data behind it. It adds more complexity, but what every large project needs is additional complexity, right?

We begin dual-writing new data to Cassandra and ScyllaDB and concurrently begin to provision ScyllaDB’s Spark migrator. It requires a lot of tuning, and once we get it set up, we have an estimated time to completion: three months.

That timeframe doesn’t make us feel warm and fuzzy inside, and we’d prefer to get value faster. We sit down as a team and brainstorm ways we can speed things up, until we remember that we’ve written a fast and performant database library that we could potentially extend. We elect to engage in some meme-driven engineering and rewrite the data migrator in Rust.

In an afternoon, we extended our data service library to perform large-scale data migrations. It reads token ranges from a database, checkpoints them locally via SQLite, and then firehoses them into ScyllaDB. We hook up our new and improved migrator and get a new estimate: nine days! If we can migrate data this quickly, then we can forget our complicated time-based approach and instead flip the switch for everything at once.

We turn it on and leave it running, migrating messages at speeds of up to 3.2 million per second. Several days later, we gather to watch it hit 100%, and we realize that it’s stuck at 99.9999% complete (no, really). Our migrator is timing out reading the last few token ranges of data because they contain gigantic ranges of tombstones that were never compacted away in Cassandra. We compact that token range, and seconds later, the migration is complete!

We performed automated data validation by sending a small percentage of reads to both databases and comparing results, and everything looked great. The cluster held up well with full production traffic, whereas Cassandra was suffering increasingly frequent latency issues. We gathered together at our team onsite, flipped the switch to make ScyllaDB the primary database, and ate celebratory cake!  
‍

## Several Months Later…

We switched our messages database over in May 2022, but how’s it held up since then?

It’s been a quiet, well-behaved database (it’s okay to say this because I’m not on-call this week). We’re not having weekend-long firefights, nor are we juggling nodes in the cluster to attempt to preserve uptime. It’s a much more efficient database — we’re going from running 177 Cassandra nodes to just 72 ScyllaDB nodes. Each ScyllaDB node has 9 TB of disk space, up from the average of 4 TB per Cassandra node.

Our tail latencies have also improved drastically. For example, fetching historical messages had a p99 of between 40-125ms on Cassandra, with ScyllaDB having a nice and chill 15ms p99 latency, and message insert performance going from 5-70ms p99 on Cassandra, to a steady 5ms p99 on ScyllaDB. Thanks to the aforementioned performance improvements, we’ve unlocked new product use cases now that we have confidence in our messages database.

At the end of 2022, people all over the world tuned in to watch the World Cup. One thing we discovered very quickly was that goals scored showed up in our monitoring graphs. This was very cool because not only is it neat to see real-world events show up in your systems, but this gave our team an excuse to watch soccer during meetings. We weren’t “watching soccer during meetings”, we were “proactively monitoring our systems’ performance.”

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6406587246a8ce1cfe8f105f_Screen%20Shot%202023-02-27%20at%205.44.56%20PM.png)

We can actually tell the story of the World Cup Final via our message send graph. The match was tremendous. Lionel Messi was trying to check off the last accomplishment in his career and cement his claim to being the greatest of all time and lead Argentina to the championship, but in his way stood the massively talented Kylian Mbappe and France.

Each of the nine spikes in this graph represents an event in the match.

  1. Messi hits a penalty, and Argentina goes up 1-0.
  2. Argentina scores again and goes up 2-0.
  3. It’s halftime. There’s a sustained fifteen-minute plateau as users chat about the match.
  4. The big spike here is because Mbappe scores for France and scores again 90 seconds later to tie it up!
  5. It’s the end of regulation, and this huge match is going to extra time.
  6. Not much happens in the first half of extra time, but we reach halftime and users are chatting.
  7. Messi scores again, and Argentina takes the lead!
  8. Mbappe strikes back to tie it up!
  9. It’s the end of extra time, we’re heading to penalty kicks!
  10. Excitement and stress grow throughout the shootout until France misses and Argentina doesn’t! Argentina wins!



![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64065884c4a34e2bcb7b470d_Screen%20Shot%202023-02-27%20at%205.52.07%20PM.png)

Coalesced messages per second

People all over the world are stressed watching this incredible match, but meanwhile, Discord and the messages database aren’t breaking a sweat. We’re way up on message sends and handling it perfectly. With our Rust-based data services and ScyllaDB, we’re able to shoulder this traffic and provide a platform for our users to communicate.

We’ve built a system that can handle trillions of messages, and if this work is something that excites you, [check out our careers page](https://discord.com/careers). We’re hiring!  
‍

Tags

No items found.

![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/640664069a8b908442f19f7b_Bo%27s%20Photo.jpg)

Bo Ingram

Senior Software Engineer @ Discord

## related articles

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/689f7cdf79694c891764399a_GCDC_NvidiaLogoLockUp_Blog.png)Product & FeaturesTransforming Game Discovery with Instant Play Experiences on Discord](/blog/transforming-game-discovery-with-instant-play-experiences-on-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/687185569dd0ac147ad89a64_image5.jpg)Product & FeaturesReward Your Play: Complete Quests. Earn Orbs. Get Sweet Stuff.](/blog/discord-orbs)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6494b1e02e40699d67a766e6_Summer_June.png)Product & FeaturesDiscord Update: June 30, 2025 Changelog](/blog/discord-update-june-30-2025-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/684a07a2968307ee558f19dd_image5.png)Product & FeaturesGet More From Your Boosts With New Server Perks](/blog/get-more-from-your-boosts-with-new-server-perks)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/684a0b131c3be3d6f58e5fe9_image3.png)Product & FeaturesGift Nitro and Earn A Flavorful Splash for your Avatar ](/blog/gift-nitro-and-earn-a-flavorful-splash-for-your-avatar)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/683a1be02c321cc94c5ad745_image7.png)Product & FeaturesDiscord Social SDK Updates & Integrations](/blog/discord-social-sdk-updates-integrations)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/683a385e31ae16bd173ee8d9_image2.png)Product & FeaturesDiscord Patch Notes: June 3, 2025](/blog/discord-patch-notes-june-3-2025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6825245fd44e60c25bfd350c_image4.png)Product & FeaturesGo Beyond, Plus Ultra! with the My Hero Academia Collection](/blog/go-beyond-plus-ultra-with-the-my-hero-academia-collection)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/68128a3b85b6f59abff99f3d_StarWars_BLOG%20BANNER%20720.jpg)Product & FeaturesSTAR WARS™ Makes Its Way to Discord](/blog/star-wars-makes-its-way-to-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: May 1, 2025](/blog/discord-patch-notes-may-1-2025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6801703e88ed1f8cb5d6e459_\(DMKT05-NP\)Nameplates_BlogBanner_AB_FINAL_V1.png)Product & FeaturesWorthy of a Plaque: Nameplates Land in the Shop](/blog/nameplates-land-in-the-shop)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/67f83b2996e977048a0bc26e_image1.png)Product & FeaturesMake More Closet Space! Nitro Members Can Now Keep Avatar Decoration Quest Rewards for Longer](/blog/nitro-members-keep-quest-rewards-longer)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: April 3, 2025](/blog/discord-patch-notes-april-3-2025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/65e0d5d41a1beac596a12aaa_March%20Changelog%20Headers.png)Product & FeaturesDiscord Update: March 25, 2025 Changelog](/blog/discord-update-march-25-2025-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/67e1a71360e0b28ee369fc83_\(DMKT08-PQ1\)_Blog_Banner_Static_Final_1800x720.png)Product & FeaturesRevamped Overlay & Refreshed Desktop Give Game Time a Boost](/blog/player-release-q12025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: March 11, 2025](/blog/discord-patch-notes-march-11-2025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: February 3, 2025](/blog/discord-patch-notes-february-3-2025)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/657a71a24b4bc2f1879762ea_Winter_December.png)Product & FeaturesDiscord Update: December 19, 2024 Changelog](/blog/discord-update-december-19-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/675b74044f5f48260b2905b1_image9.png)Product & FeaturesGift Ideas for the Dedicated Discord User in Your Life](/blog/gift-ideas-for-the-discord-user-in-winter-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: December 5, 2024](/blog/discord-patch-notes-december-5-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/636042835883b97b259ef618_Fall_November.png)Product & FeaturesDiscord Update: November 18, 2024 Changelog](/blog/discord-update-november-18-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/672e95661de7c16c8d8f7417_image2.png)Product & FeaturesCelebrate Arcane’s Second Season with a new Shop Collection](/blog/arcane-shop-collection)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: November 1, 2024](/blog/discord-patch-notes-november-1-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/670ef8932fc56d10786649dd_\(CCD_17_D%26D\)_MKT_01_Blog%20Banner_Full.jpg)Product & FeaturesSet Out for a Discord Adventure! Check Out Our Roll20 Adventure & D&D Shop Collection ](/blog/discord-roll20-adventure-and-dnd-shop-collection)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: October 1, 2024](/blog/discord-patch-notes-october-1-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/66ecb1eaa5561774cf2c00d5_650233ad5dcf4b6825522e09_Fall_September.png)Product & FeaturesDiscord Update: September 26, 2024 Changelog](/blog/discord-update-september-26-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/66e9ed278d78eb7c65473d11_image10.png)Product & FeaturesDiscover More Ways to Play with Apps – Now Anywhere on Discord!](/blog/discover-more-ways-to-play-with-apps-now-anywhere-on-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/66d8cb358a1c941cb416372c_Blog%20Banner%20Styleframe.jpg)Product & FeaturesLegacy Shop Favorites Emerge from The Vault for a First Anniversary Encore! ](/blog/legacy-shop-favorites-emerge-from-the-vault-for-a-first-anniversary-encore)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: August 30, 2024](/blog/discord-patch-notes-august-30-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6360419dba12275999ef0eee_Summer_August.png)Product & FeaturesDiscord Update: August 28, 2024 Changelog](/blog/discord-update-august-28-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/66bf8f185b919e6dbac816c4_image1.png)Product & FeaturesQueue Up Your Playlists on Discord with the Amazon Music Listening Party Activity!](/blog/amazon-music-activity)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: August 1, 2024](/blog/discord-patch-notes-august-1-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/62d0746010f70706d1341f68_image3.png)Product & FeaturesNow Available: See What’s Happening on Discord, Directly from your Xbox console](/blog/see-whats-happening-on-discord-directly-from-your-xbox)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64c7e8751b517e9cc56a5238_Summer_July.png)Product & FeaturesDiscord Update: July 26, 2024 Changelog](/blog/discord-update-july-26-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6691b8a2e59e9c4657d56d27_SpongeBob_Banner_blog%20header%201_B.png)Product & FeaturesWHO LIVES ON YOUR PROFILE FOR ALL TO SEE? 🎶 SPONGEBOB, IN THE SHOP!](/blog/spongebob-shop-collection)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: July 1, 2024](/blog/discord-patch-notes-july-1-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6494b1e02e40699d67a766e6_Summer_June.png)Product & FeaturesDiscord Update: June 20, 2024 Changelog](/blog/discord-update-june-20-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/666788d74e610cffdd4e4808_image1.jpg)Product & FeaturesHow to Join Discord Calls Directly From Your PS5® — No Phone Needed! ](/blog/join-discord-calls-directly-from-ps5-no-phone-needed)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6660a79090f7f35de8735e0e_image2.png)Product & FeaturesFeast Your Monit-eyes on Today's Exciting Developer Updates!](/blog/feast-your-moniteyes-on-todays-exciting-developer-updates)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6657ad0a58988c5decbfbc53_Header_3.png)Product & FeaturesDiscord Patch Notes: May 2024](/blog/discord-patch-notes-may-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/664ce605c29e6a3266d6ef95_image3.png)Product & FeaturesRefining Discord’s Mobile Experience With Your Feedback ](/blog/refining-discords-mobile-experience-with-your-feedback)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/646d3dfadaf245263be22231_Spring_May.png)Product & FeaturesDiscord Update: May 13, 2024 Changelog](/blog/discord-update-may-13-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/66315deb32012c249564aab3_Header_7.png)Product & FeaturesDiscord Patch Notes: April 2024](/blog/discord-patch-notes-april-2024)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6441bd561f47091d8174e16c_Spring_April.png)Product & FeaturesDiscord Update: April 3, 2024 Changelog](/blog/discord-update-april-3-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6602021256195cd027a3f0b8_VLR_Blog_Header_Banner_1800x720px_V2.png)Product & FeaturesLock in. Stand out. VALORANT arrives in the Shop.](/blog/valorant-shop-collection)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/65e0d5d41a1beac596a12aaa_March%20Changelog%20Headers.png)Product & FeaturesDiscord Update: March 5, 2024 Changelog](/blog/discord-update-march-5-2024-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/657a71a24b4bc2f1879762ea_Winter_December.png)Product & FeaturesDiscord Update: December 13, 2023 Changelog](/blog/discord-update-december-13-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/656a67621c4ba32e7c3710fc_image14.png)Product & FeaturesImproving Our Mobile Experience](/blog/improving-our-mobile-experience)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/654409dbbf40922256139a9a_Fall_October.png)Product & FeaturesDiscord Update: October 19, 2023 Changelog](/blog/discord-update-october-19-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6514773178cb945e3c97705b_Discord_Collectible_BlogHeader%20Banner_V6_RESIZED.png)Product & FeaturesAvatar Decorations & Profile Effects: Collect and Keep the Newest Styles](/blog/avatar-decorations-collect-and-keep-the-newest-styles)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/650233ad5dcf4b6825522e09_Fall_September.png)Product & FeaturesDiscord Update: September 13, 2023 Changelog](/blog/discord-update-september-13-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64f8ce1927fcd30fdfe80a56_23_117_Xbox_Social_1800x720.png)Product & FeaturesNow Available: Stream Your Xbox Games Directly to Discord](/blog/xbox-stream-to-discord-announcement)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64c7e8751b517e9cc56a5238_Summer_July.png)Product & FeaturesDiscord Update: July 29, 2023 Changelog](/blog/discord-update-july-29-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/649e03012c058e734627d965_Remixing-Blog-Header.png)Product & FeaturesMeme Up Some Fun with Remix](/blog/meme-up-some-fun-with-remix)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6494b1e02e40699d67a766e6_Summer_June.png)Product & FeaturesDiscord Update: June 22, 2023 Changelog](/blog/discord-update-june-22-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/648cef33984677d825ca2763_PortalArticleHeader_1800x720.png)Product & FeaturesServer Subscriptions Just Got Super Powered: Introducing Media Channels, Tier Templates and more!](/blog/server-subscriptions-updates-media-channels-tier-templates-and-more)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/646d3dfadaf245263be22231_Spring_May.png)Product & FeaturesDiscord Update: May 22, 2023 Changelog](/blog/discord-update-may-22-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/645c294e1f5bcda693b9df11_usernames%20blog%20header.png)Product & FeaturesEvolving Usernames on Discord](/blog/usernames)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6441bd561f47091d8174e16c_Spring_April.png)Product & FeaturesDiscord Update: April 14, 2023 Changelog](/blog/discord-update-april-14-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/643d9e196f9a672e57e79b3f_Community%20Onboarding_Blog%20Header_blog%20header.jpg)Product & FeaturesWelcome Your New Members Easily with Community Onboarding](/blog/community-onboarding-welcome-your-new-members)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64399621c8daafe18d84b451_VoiceMessages_Blog_1800x720%402x.png)Product & FeaturesIntroducing Discord Voice Messages](/blog/discord-voice-messages)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/642ca8066bcbdd2a77f4a702_NAD_NitroBanner_Purple.png)Product & FeaturesApril Showers Bring Super-Cool Nitro Powers](/blog/april-showers-bring-super-cool-nitro-powers)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/642c93aa534c2922f17a99e7_2023_BurstReactions_Static_BlogHDR_005.png)Product & FeaturesNew to Discord Nitro: Super Reactions Make Your Emoji Burst to Life](/blog/super-reactions-make-emoji-burst-to-life-discord-nitro)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/642c8db3a577675a498f6168_BackupBlogHeaders_Batch2Artboard%205.png)Product & FeaturesReady Your Airhorns! 🎺 Discord Soundboard is Coming Your Way](/blog/ready-your-airhorns-discord-soundboard-is-coming)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6419e9dca30b3d2df089afb5_Spring_March.png)Product & FeaturesDiscord Update: March 20, 2023 Changelog](/blog/discord-update-march-20-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64121f8765e921a28f9a2b54_Discord%20HQ%20-%202.png)Product & FeaturesNow in Nitro: Bring Your Vibe to Discord with New Themes ](/blog/bring-your-vibe-to-discord-with-new-themes-in-nitro)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/633cc73511d1b97578f933e1_2022_Activities_BlogNews_1800x720%20\(1\).png)Product & FeaturesDiscord Activities: Play Games and Watch Together](/blog/server-activities-games-voice-watch-together)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/64064bb87f76f7e45341ed38_AI-DD-Blog-Header.png)Product & FeaturesDiscord is Your Place for AI with Friends](/blog/ai-on-discord-your-place-for-ai-with-friends)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/640843453613c80273894d6e_playstation_launch_blog%20header.png)Product & FeaturesNow Available: Use Discord Voice Chat on Your PlayStation®5 Console](/blog/playstation-5-voice-integration-announcement)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/63ebf6ed3437144cd8e9791f_Winter_February.png)Product & FeaturesDiscord Update: February 20, 2023 Changelog](/blog/discord-update-february-20-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/63ea5288a7bf7a7fedd49468_StageChannels_v2_Blog-01.png)Product & FeaturesIntroducing Video, Screen Share, and Text Chat Support for Stage Channels](/blog/introducing-video-screen-share-text-chat-support-for-stage-channels)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/63d05bf7a7feb14ac067b4bf_Winter_January.png)Product & FeaturesDiscord Update: January 25, 2023 Changelog](/blog/discord-update-january-25-2023-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6393ae0ce6ab8ebeb1bab04d_image1.png)Product & FeaturesMake Your Connection: Connected Accounts Get a Huge Functionality Boost](/blog/connected-accounts-functionality-boost-linked-roles)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6387a302c7db2474abd10c5c_Macro%20Hero-Blog.png)Product & FeaturesAnnouncing Server Subscriptions and the Creator Portal, Now Open to More Communities ](/blog/server-and-creator-subscriptions)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/636042835883b97b259ef618_Fall_November.png)Product & FeaturesDiscord Update: November 1, 2022 Changelog](/blog/discord-update-november-1-2022-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/634dde89272560563ac10898_2022_Q3_AppDirectory_Admin_HeroBanner_1800x720.png)Product & FeaturesAttention Server Owners: The App Directory is Here!](/blog/app-directory-is-here-mods-and-admins)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/633cc7f6518225f5dbb2b104_Discord%20Nitro_Blog%20Header.png)Product & FeaturesIntroducing Discord Nitro Basic ](/blog/introducing-discord-nitro-basic)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/632a295901d7d8875861dbaf_2022_AutoModSpamFilters_Static_003.png)Product & FeaturesBlocking Spam Gets Easier Thanks to New AutoMod and Safety Tools](/blog/new-anti-spam-raid-automod-safety-update)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/631bbb77ff041e9b9bcd8505_UZEzk_N4.jpeg)Product & FeaturesForum Channels: A Space for Organized Conversations](/blog/forum-channels-space-for-organized-conversation)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6360419dba12275999ef0eee_Summer_August.png)Product & FeaturesDiscord Update: August 29, 2022 Changelog](/blog/discord-update-august-29-2022-changelog)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/62d0746010f70706d1341f68_image3.png)Product & FeaturesNow Available: Join Discord Voice Chat Directly From Your Xbox](/blog/xbox-voice-integration-announcement)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6303aecce5701f3c643a7600_2022_BTS_Headers_001_BlogHeader_1800x720%20\(1\).png)Product & FeaturesDiscover Your Next Favorite Campus Club in Student Hubs](/blog/discover-your-next-favorite-campus-club-in-student-hubs)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/627c1b4c6ee1e643be45d12d_image1.png)Product & FeaturesAn Exciting Update to Discord for Android](/blog/android-react-native-framework-update)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/620c1dfaef1e54219ddfd35e_accessibility-blog-header.png)Product & FeaturesHow We’re Improving the Discord Experience for Everyone ](/blog/improving-app-accessibility-a11y-updates)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/62a281f083081c68ebb94672_Discord%20HQ%20-%203.png)Product & FeaturesAn Update on Tools for Building and Sustaining Communities on Discord ](/blog/update-tools-building-sustaining-communities-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/629e8853e258b321e97c123d__AutoMod_Blog%20Header.png)Product & FeaturesMeet Your Newest Community Moderator: AutoMod Is Here ](/blog/automod-launch-automatic-community-moderation)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/621d47edf5432e885b897c9a_Text%20in%20Voice_Blog%20Header.png)Product & FeaturesSharing Messages in Voice Just Got Way Easier: Introducing Text Chat in Voice Channels ](/blog/text-in-voice-chat-channel-announcement-tiv)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/627aa5ffa059bc90ed8ae4ad_2022_Bday_Theme_004BlogHeader_1800x720.png)Product & FeaturesCelebrate Discord’s Bir7hday with Party Mode! ](/blog/7th-birthday)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/625489cc18bfe0b12a83e4a2_202201010_PM_CommandPermissionsBlog_JJ_v04.jpg)Product & FeaturesPermission to Slash, Granted: Introducing Slash Command Permissions](/blog/slash-commands-permissions-discord-apps-bots)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61fc3af219cf1b4ce968fed4_Communities%20Header.png)Product & FeaturesTesting 1-2-3: A Note on Upcoming Community Experiments](/blog/a-note-on-upcoming-community-experiments)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61f334952f2c7f6a86199a87_P1PlaystationStatic_Blog%20Header.png)Product & FeaturesPlayStation® x Discord: Connect Your Account and Show What You’re Playing ](/blog/playstation-discord-account-connection-linking-game-status)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61ae5d8cc6b66360dd9a46d8_gJLNp2js.png)Product & FeaturesBuilding Sustainable Creator Communities on Discord](/blog/building-sustainable-creator-communities-on-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/6192ad513cf1cf722a9729e8_app%20blog%20header.png)Product & FeaturesApp Discovery is Coming to Discord](/blog/discord-bots-and-app-discovery-announcement)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/611af09cdf661e59a3374d0a_1_NtFr9IAUxLPuiKKlRTK1zQ.png)Product & FeaturesWhat’s Next for Communities at Discord](/blog/whats-next-for-communities-at-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61157ed85b6f072f90523594_0_S4sPwKey9htV30Wd.png)Product & FeaturesNitro Users Now Get an Enhanced Video Experience with Three Months of YouTube Premium](/blog/nitro-users-now-get-an-enhanced-video-experience-with-three-months-of-youtube-premium)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/611581e42d97c066e19a71bf_0_HYed_1mRELDpUACo.png)Product & FeaturesConnect the Conversation with Threads on Discord](/blog/connect-the-conversation-with-threads-on-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/61159293a75598c375d2a6cd_0_VaKxKfSRas4uvSsD.png)Product & FeaturesUnleash Your Creativity with Stickers on Discord](/blog/unleash-your-creativity-with-stickers-on-discord)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/613fa20e01edfb6ea3e0de92_StageDiscovery_Blog_2500x1000_4MB.gif)Product & FeaturesDiscover the Next Great Community in Stage Discovery](/blog/discover-the-next-great-community-in-stage-discovery)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/611aed65e55f7402bb175a54_1_nau2qmMD7F2bOX8eydqBVw.png)Product & FeaturesStarting Servers on Discord is Easier Than Ever](/blog/starting-servers-on-discord-is-easier-than-ever)

[![](https://cdn.prod.website-files.com/5f9072399b2640f14d6a2bf4/611af09cdf661e59a3374d0a_1_NtFr9IAUxLPuiKKlRTK1zQ.png)Product & FeaturesCaptivate Your Community with Stage Channels](/blog/captivate-your-community-with-stage-channels)

.

How Discord Stores Trillions of MessagesOur Cassandra TroublesChanging Our ArchitectureData Services Serving DataA Very Big MigrationSeveral Months Later

How Discord Stores Trillions of MessagesOur Cassandra TroublesChanging Our ArchitectureData Services Serving DataA Very Big MigrationSeveral Months Later

Search

[![Home page](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f68ec_50421399b7d807a39b976375b8b2f21e_Symbol.svg)](/)

Language

English (US)

![](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f68fd_13b796631a0178df3105d55d1d629706_Chevron%20Down.svg)

  * Čeština

  * Dansk

  * Deutsch

  * English

  * English (UK)

  * Español

  * Español (América Latina)

  * Français

  * Hrvatski

  * Italiano

  * lietuvių kalba

  * Magyar

  * Nederlands

  * Norsk

  * Polski

  * Português (Brasil)

  * Română

  * Suomi

  * Svenska

  * Tiếng Việt

  * Türkçe

  * Ελληνικά

  * български

  * Русский

  * Українська

  * हिंदी

  * ไทย

  * 한국어

  * 中文

  * 中文(繁體)

  * 日本語




Social

[![Twitter](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f6891_91ce5945e0716b8f27aba591ed3ce824_x.svg)](https://twitter.com/discord)[![Instagram](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68a1_456a1737b263ca0ec63b760ac332ed2a_instagram.svg)](https://www.instagram.com/discord/)[![Facebook](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68b5_a77cbd313cca7494393b7a8ccc20fa16_facebook.svg)](https://www.facebook.com/discord/)[![Youtube](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68c9_341e1594d600b55ff2302e0169b321ce_youtube.svg)](https://www.youtube.com/discord)[![Tiktok](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68d2_1b8105cd54e8b765ed7c14cd03b13ffc_tiktok.svg)](https://www.tiktok.com/@discord)

Menu

Product

![](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f6915_0de9af0fe90fba53b80f020909344da6_Chevron%20Down.svg)

[Download](/download)[Nitro](/nitro)[Status](https://discordstatus.com/)[App Directory](/application-directory)

Company

![](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f6915_0de9af0fe90fba53b80f020909344da6_Chevron%20Down.svg)

[About](/company)[Jobs](/careers)[Brand](/branding)[Newsroom](/newsroom)

Resources

![](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f6915_0de9af0fe90fba53b80f020909344da6_Chevron%20Down.svg)

[College](/college)[Support](https://support.discord.com/hc)[Safety](/safety)[Blog](/blog)[StreamKit](/streamkit)[Creators](/creators)[Community](/community)[Developers](/developers)[Quests](/ads/quests)[Official 3rd Party Merch](https://discordmerch.com/evergreenfooter)[Feedback](https://support.discord.com/hc/en-us/community/topics)

Policies

![](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119f90b32c4c283f6915_0de9af0fe90fba53b80f020909344da6_Chevron%20Down.svg)

[Terms](/terms)[Privacy](/privacy)Cookie Settings[Guidelines](/guidelines)[Acknowledgements](/acknowledgements)[Licenses](/licenses)[Company Information](/company-information)

Social

[![Twitter](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f6891_91ce5945e0716b8f27aba591ed3ce824_x.svg)](https://x.com/discord)[![Instagram](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68a1_456a1737b263ca0ec63b760ac332ed2a_instagram.svg)](https://www.instagram.com/discord/)[![Facebook](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68b5_a77cbd313cca7494393b7a8ccc20fa16_facebook.svg)](https://www.facebook.com/discord/)[![Youtube](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68c9_341e1594d600b55ff2302e0169b321ce_youtube.svg)](https://www.youtube.com/discord)[![Tiktok](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/66fd119e90b32c4c283f68d2_1b8105cd54e8b765ed7c14cd03b13ffc_tiktok.svg)](https://www.tiktok.com/@discord)

![Discord](https://cdn.prod.website-files.com/5f8dd67f8fdd6f51f0b50904/67ac9e0891a02325abf50c81_63bbb8d20f0336ebb2218972a83c5eec_Wordmark.svg)

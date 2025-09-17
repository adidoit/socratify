---
title: "Delivering billions of messages exactly once"
category: "startups"
url: "https://segment.com/blog/exactly-once-delivery/"
type: "elite_systems_architecture"
elite: true
date: "2025-09-15"
---

Twilio Blog

  * [Overview](/en-us/blog)
  * [ Developers ](/en-us/blog/developers)

  * [ Industry Insights ](/en-us/blog/insights)

  * [ Product News ](/en-us/blog/products)

  * [ Events ](/en-us/blog/events)

  * [ Partners ](/en-us/blog/partners)

  * [ Company ](/en-us/blog/company)




# Delivering billions of messages exactly once

[ Blog](/en-us/blog)/ [ Industry Insights](/en-us/blog/insights)/  Delivering billions of messages exactly once




* * *

**Tags**

[ Customer data platform ](https://www.twilio.com/en-us/blog/tag.use-case%253Acustomer-data-platform)

**Products**

[ Connections ](/content/twilio-com/global/en-us/products/connections.html)

* * *

[ Start for free  ](https://segment.com/signup?utm_referrer=https%3A%2F%2Fwww.twilio.com%2Fen-us%2Fblog%2Finsights%2Fexactly-once-delivery) [ Get a demo  ](https://segment.com/demo?utm_referrer=https%3A%2F%2Fwww.twilio.com%2Fen-us%2Fblog%2Finsights%2Fexactly-once-delivery)

Time to read: 

  * [ Facebook logo ](https://www.facebook.com/sharer/sharer.php?u=https://www.twilio.com/en-us/blog/insights/exactly-once-delivery "Share via Facebook")
  * [ Twitter Logo Follow us on Twitter ](https://twitter.com/intent/tweet?url=https://www.twilio.com/en-us/blog/insights/exactly-once-delivery "Share via X")
  * [ LinkedIn logo ](https://www.linkedin.com/sharing/share-offsite/?url=https://www.twilio.com/en-us/blog/insights/exactly-once-delivery "Share via LinkedIn")
  * [ ](mailto:?subject=Delivering billions of messages exactly once&body=Here's a link to the piece from Twilio: https://www.twilio.com/en-us/blog/insights/exactly-once-delivery "Share via Email")
  * [ ](https://www.twilio.com/blog.feed.xml "Twilio RSS")



June 29, 2017 

**Written by**

[ Amir Abu Shareb ](https://www.twilio.com/en-us/blog/authors/author.aabushareb)

Twilion 

* * *

## Delivering billions of messages exactly once

The single requirement of all data pipelines is that **they cannot** _**lose**_ **data**. Data can usually be delayed or re-ordered–but never dropped. 

To satisfy this requirement, most distributed systems guarantee [_at-least-once delivery_](http://www.cloudcomputingpatterns.org/at_least_once_delivery/) _._ The techniques to achieve at-least-once delivery typically amount to: _“retry, retry, retry”_. You never consider a message ‘delivered’ until you receive a firm acknowledgement from the consumer.

But as a user, _at-least-once delivery_ isn’t _really_ what I want. I want messages to be delivered **once.** And _only_ once.

Unfortunately, [achieving anything close to _exactly-once delivery_ requires a bullet-proof design.](http://bravenewgeek.com/you-cannot-have-exactly-once-delivery/) Each failure case has to be carefully considered as part of the architecture–it can’t be “bolted on” to an existing implementation after the fact. And even then, it’s pretty much impossible to have messages only ever be delivered once. 

In the past three months we’ve built an entirely new de-duplication system to get as close as possible to exactly-once delivery, in the face of a wide variety of failure modes. 

The new system is able to track 100x the number of messages of the old system, with increased reliability, at a fraction of the cost. Here’s how. 

## The problem

Most of Twilio Segment’s internal systems handle failures gracefully using retries, message re-delivery, locking, and [two-phase commits](https://en.wikipedia.org/wiki/Two-phase_commit_protocol). But, there’s one notable exception: **clients that send data directly to our public API.**

Clients (particularly mobile clients) have frequent network issues, where they might send data, but then miss the response from our API.

Imagine, you’re riding the bus, booking a room off your iPhone using [HotelTonight](https://www.hoteltonight.com/). The app starts uploading usage data to Twilio Segment’s servers, but you suddenly pass through a tunnel and lose connectivity. Some of the events you’ve sent have already been processed, but the client never receives a server response. 

In these cases, clients retry and re-send the _same_ events to Twilio Segment’s API, even though the server has technically already received those exact messages.

From our server metrics, approximately **0.6%** of events that are ingested within a 4-week window are duplicate messages that we’ve already received. 

This error rate might sound insignificant. But for an e-commerce app generating billions of dollars in revenue, a **0.6%** discrepancy can mean the difference between a profit and a loss of millions. 

## De-duplicating our messages

So we understand the meat of the problem–we have to remove duplicate messages sent to the API. But how?

Thinking through the high-level API for any sort of dedupe system is simple. In Python (_aka pseudo-pseudocode_), we could represent it as the following:

Python

Copy code
    
    
    def dedupe(stream):
      for message in stream:
        if has_seen(message.id): 
          discard(message)
        else:
          publish_and_commit(message)

For each message in our stream, we first check if we’ve seen that particular message, keyed by its id (which we assume to be unique). If we’ve seen a message before, discard it. If it’s new, we re-publish the message and commit the message atomically. 

To avoid storing all messages for all time, we keep a ‘de-duplication window’–defined as the time duration to store our keys before we expire them. As messages fall outside the window, we age them out. We want to guarantee that there exists only a single message with a given ID sent within the window.

The behavior here is easy to describe, but there are two aspects which require special attention: **read/write performance** and **correctness**.

We want our system to be able to de-duplicate the billions of events passing through our pipeline–and do so in a way that is both low-latency and cost efficient. 

What’s more, we want to ensure the information about which events we’ve seen is written durably so we can recover from a crash, and that we never produce duplicate messages in our output.

## Kafka Deduplication Architecture

To achieve deduplication in Kafka, we’ve created a ‘two-phase’ architecture which reads off Kafka, and de-duplicates all events coming in within a 4-week window. Incoming messages are assigned a unique ID and logged to Kafka, while a Go program functions as the deduplication “worker:" reading new messages, checking if they are duplicates, and (if so) then sending them to the Kafka output topic.

![Diagram of dedupe architecture with Kafka input topics \(partitions p1, p2, p3\) read by separate workers using RocksDB, then publishing to Kafka output topics.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_JTBe3gdD.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_JTBe3gdD.png)

The dedupe high-level architecture

## Kafka topology

To understand how this works, we’ll first look at the [Kafka](https://kafka.apache.org/) stream topology. All incoming API calls are split up as individual messages, and read off a Kafka input topic. 

First, each incoming message is tagged with a unique `**messageId**` , generated by the client. In most cases this is a UUIDv4 (though we are considering a switch to [ksuids](/content/twilio-com/global/en-us/blog/developers/a-brief-history-of-the-uuid/)). If a client does not supply a messageId, we’ll automatically assign one at the API layer.

We don’t use vector clocks or sequence numbers because we want to reduce the client complexity. Using UUIDs allows _anyone_ to easily send data to our API, as almost every major language supports it.

Json

Copy code
    
    
    {
      "messageId": "ajs-65707fcf61352427e8f1666f0e7f6090",
      "anonymousId": "e7bd0e18-57e9-4ef4-928a-4ccc0b189d18",
      "timestamp": "2017-06-26T14:38:23.264Z",
      "type": "page"
    }

Individual messages are logged to Kafka for durability and replay-ability. They are partitioned by messageId so that we can ensure the same `messageId` will _always_ be processed by the same consumer.

This is an important piece when it comes to our data processing. Instead of searching a central database for whether we’ve seen a key amongst **hundreds of billions** of messages, we’re able to narrow our search space by orders of magnitude simply by routing to the right partition. 

The dedupe “worker” is a Go program which reads off the Kafka input partitions. It is responsible for reading messages, checking whether they are duplicates, and if they are new, sending them to the Kafka output topic. 

In our experience, the worker and Kafka topology are both extremely easy to manage. We no longer have a set of large [Memcached](https://memcached.org/) instances which require failover replicas. Instead we use embedded [RocksDB](http://rocksdb.org/) databases which require zero coordination, and gets us persistent storage for an extremely low cost. More on that now!

## The RocksDB worker

Each worker stores a local [RocksDB database](http://rocksdb.org/) on its local EBS hard drive. RocksDB is an embedded [key-value store developed at Facebook](https://www.facebook.com/notes/facebook-engineering/under-the-hood-building-and-open-sourcing-rocksdb/10151822347683920/), and is optimized for incredibly high performance.

Whenever an event is consumed from the input topic, the consumer queries RocksDB to determine whether we have seen that event’s `**messageId**` . 

If the message does not exist in RocksDB, we add the key to RocksDB and then publish the message to the Kafka output topic. 

If the message already exists in RocksDB, the worker simply will not publish it to the output topic and update the offset of the input partition, acknowledging that it has processed the message.

## Performance

In order to get high performance from our database, we have to satisfy three query patterns for every event that comes through:

  1. **detecting existence** of random keys that come in, but likely don’t exist in our DB. These may be found anywhere within our keyspace.

  2. **writing** new keys at a high write throughput

  3. **aging out** old keys that have passed outside of our ‘de-duplication window’




In effect, we have to constantly scan the entire database, append new keys, _and_ age out old keys. And ideally, it happens all within the same[ data model.](/content/twilio-com/global/en-us/blog/insights/data/data-modeling/)

![Diagram showing a query pattern: \(1\) check if key exists, \(2\) write key, \(3\) age out old keys, using arrows and labeled boxes.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_RgKPQ6Mx.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_RgKPQ6Mx.png)

Our database has to satisfy three very separate query patterns

Generally speaking, the majority of these performance gains come from our database performance–so it’s worth understanding the internals that make RocksDB perform so well. 

RocksDB is an [log-structured-merge-tree](https://en.wikipedia.org/wiki/Log-structured_merge-tree) [(](https://en.wikipedia.org/wiki/Log-structured_merge-tree)[LSM)](https://en.wikipedia.org/wiki/Log-structured_merge-tree) database–meaning that it is constantly appending new keys to a **write-ahead-log** on disk, as well as storing the sorted keys in-memory as part of a **memtable**.

![Diagram of an in-memory write buffer storing sorted key ranges, with a zoomed-in view showing segments like "key00 to key25" and "key87 to key95".](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_GVMN41HL.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_GVMN41HL.png)

Keys are sorted in-memory as part of a memtable

Writing keys is an extremely fast process. New items are journaled straight to disk in append-only fashion (for immediate persistence and failure recovery), and the data entries are sorted in-memory to provide a combination of fast search and batched writes. 

Whenever enough entries have been written to the **memtable** , it is persisted to disk as an **SSTable** (sorted-string table). Since the strings have already been sorted in memory, they can be flushed directly to disk. 

![Diagram showing an in-memory write buffer at Level 0, and multiple levels of persistent storage \(Levels 1-4\) with increasing numbers of data blocks.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_G6rOuUWk.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_G6rOuUWk.png)

The current memtable is flushed to disk as an SSTable at Level 0

Here’s an example of flushing from our production logs:

Bash

Copy code
    
    
    [JOB 40] Syncing log #655020
    [default] [JOB 40] Flushing memtable with next log file: 655022
    [default] [JOB 40] Level-0 flush table #655023: started
    [default] [JOB 40] Level-0 flush table #655023: 15153564 bytes OK
    [JOB 40] Try to delete WAL files size 12238598, prev total WAL file size 24346413, number of live WAL files 3.

Each SSTable is immutable–once it has been created, it is never changed–which is what makes writing new keys so fast. No files need to be updated, and there is no write amplification. Instead, multiple SSTables at the same ‘level’ are merged together into a new file during an out-of-band compaction phase. 

![Diagram showing data compaction from Level 0 \(in-memory\) down to Level 1 storage, with multiple storage levels labeled Level 0 through Level 4.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_3MXxKr2t.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_3MXxKr2t.png)

_When individual SSTables at the same level are compacted, their keys are merged together, and then the new file is promoted to the next higher level._

Looking through our production logs, we can see an example of these compaction jobs. In this case, job 41 is compacting 4 level 0 files, and merging them into a single, larger, level 1 file. 

Bash

Copy code
    
    
    /data/dedupe.db$ head -1000 LOG | grep "JOB 41"
    [JOB 41] Compacting 4@0 + 4@1 files to L1, score 1.00
    [default] [JOB 41] Generated table #655024: 1550991 keys, 69310820 bytes
    [default] [JOB 41] Generated table #655025: 1556181 keys, 69315779 bytes
    [default] [JOB 41] Generated table #655026: 797409 keys, 35651472 bytes
    [default] [JOB 41] Generated table #655027: 1612608 keys, 69391908 bytes
    [default] [JOB 41] Generated table #655028: 462217 keys, 19957191 bytes
    [default] [JOB 41] Compacted 4@0 + 4@1 files to L1 => 263627170 bytes

After a compaction completes, the newly merged SSTables become the definitive set of database records, and the old SSTables are unlinked.

If we log onto a production instance, we can see this write-ahead-log being updated–as well as the individual SSTables being written, read, and merged. 

![Terminal window listing files by size, showing .log and .sst files with their byte sizes and filenames.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_CmCMPjpN.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_CmCMPjpN.png)

_The log and the most recent SSTable dominate the I/O_

If we look at the SSTable statistics from production, we can see that we have four total ‘levels’ of files, with larger and larger files found at each higher level.

RocksDB keeps indexes and [bloom filters](https://en.wikipedia.org/wiki/Bloom_filter) of particular SSTables stored on the SSTable itself–and these are loaded into memory. These filters and indexes are then queried to find a particular key. and then the full SSTable is loaded into memory as part of an LRU basis. 

In the vast majority of cases, we see _new_ messages–which makes our dedupe system the textbook use case for bloom filters. 

Bloom filters will tell us whether a key is ‘possibly in the set’, or ‘definitely not in the set’. To do this, the bloom filter keeps set bits for various hash functions for any elements which have been seen. If all the bits for a hash function are set, the filter will return that the message is ‘possibly in the set’.

![Diagram showing three elements {x, y, z} being mapped via colored arrows to positions in a bit array, as part of a Bloom filter w.](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_lJfKGNN2.png)

![](/content/dam/segment/global/en/blog/legacy/2017/exactly-once-delivery/asset_lJfKGNN2.png)

_Querying for w in our bloom filter, when our set contains {x, y, z}. Our bloom filter will return ‘not in set’ as one of the bits is not set._

If the response is ‘possibly in the set’, then RocksDB can query the raw data from our SSTables to determine whether the item actually exists within the set. But in most cases, we can avoid querying any SSTables whatsoever, since the filter will return a ‘definitely not in the set’ response. 

When we query RocksDB, we issue a **MultiGet** for all of the relevant `messageIds` we’d like to query. We issue these as part of a batch for performance, and to avoid many concurrent locking operations. It also allows us to batch the data coming from Kafka and generally avoid random writes in favor of sequential ones. 

This answers the question of how the read/write workload gets good performance–but there’s still the question of how stale data is aged out. 

## Deletion: size-bound, not time-bound

With our de-dupe process, we had to decide whether to limit our system to a strict ‘de-duplication window’, or by the total database size on disk.

To avoid the system falling over suddenly and de-dupe collection for all customers, we decided to **limit by size** rather than **limit to a set time window**. This allows us to set a max size for each RocksDB instance, and deal with sudden spikes or increases in load. The side-effect is that this can lower the de-duplication window to under 24 hours, at which point it will page our on-call engineer. 

We periodically age out old keys from RocksDB to keep it from growing to an unbounded size. To do this, we keep a **secondary index** of the keys based upon sequence number, so that we can delete the oldest received keys first. 

Rather than using the RocksDB TTL, which would require that we keep a fixed TTL when opening the database–we instead delete objects ourselves using the sequence number for each inserted key.

Because the sequence number is stored as a secondary index, we can query for it quickly, and ‘mark’ it as being deleted. Here’s our deletion function, when passed a sequence number. 

Go

Copy code
    
    
    func (d *DB) delete(n int) error {
            // open a connection to RocksDB
            ro := rocksdb.NewDefaultReadOptions()
            defer ro.Destroy()
    
            // find our offset to seek through for writing deletes
            hint, err := d.GetBytes(ro, []byte("seek_hint"))
            if err != nil {
                    return err
            }
    
            it := d.NewIteratorCF(ro, d.seq)
            defer it.Close()
    
            // seek to the first key, this is a small
            // optimization to ensure we don't use `.SeekToFirst()`
            // since it has to skip through a lot of tombstones.
            if len(hint) > 0 {
                    it.Seek(hint)
            } else {
                    it.SeekToFirst()
            }
    
            seqs := make([][]byte, 0, n)
            keys := make([][]byte, 0, n)
    
            // look through our sequence numbers, counting up
            // append any data keys that we find to our set to be
            // deleted
            for it.Valid() && len(seqs) < n {
                    k, v := it.Key(), it.Value()
                    key := make([]byte, len(k.Data()))
                    val := make([]byte, len(v.Data()))
    
                    copy(key, k.Data())
                    copy(val, v.Data())
                    seqs = append(seqs, key)
                    keys = append(keys, val)
    
                    it.Next()
                    k.Free()
                    v.Free()
            }
    
            wb := rocksdb.NewWriteBatch()
            wo := rocksdb.NewDefaultWriteOptions()
            defer wb.Destroy()
            defer wo.Destroy()
    
            // preserve next sequence to be deleted.
            // this is an optimization so we can use `.Seek()`
            // instead of letting `.SeekToFirst()` skip through lots of tombstones.
            if len(seqs) > 0 {
                    hint, err := strconv.ParseUint(string(seqs[len(seqs)-1]), 10, 64)
                    if err != nil {
                            return err
                    }
    
                    buf := []byte(strconv.FormatUint(hint+1, 10))
                    wb.Put([]byte("seek_hint"), buf)
            }
    
            // we not only purge the keys, but the sequence numbers as well
            for i := range seqs {
                    wb.DeleteCF(d.seq, seqs[i])
                    wb.Delete(keys[i])
            }
    
            // finally, we persist the deletions to our database
            err = d.Write(wo, wb)
            if err != nil {
                    return err
            }
    
            return it.Err()
    }

To continue ensuring write speed, RocksDB doesn’t immediately go back and delete a key (remember these SSTables are immutable!). Instead, RocksDB will append a ‘tombstone’ which then gets removed as part of the compaction process. Thus, we can age out quickly with sequential writes, and avoid thrashing our memory by removing old items.

## Ensuring Correctness

We’ve now discussed how we ensure speed, scale, and low-cost searching across billions of messages. The last remaining piece is how we ensure correctness of the data in various failure modes. 

## EBS-snapshots and attachments

To ensure that our RocksDB instances are not corrupted by a bad code push or underlying EBS outage, we take periodic snapshots of each of our hard drives. While EBS is already replicated under the hood, this step guards against the database becoming corrupted from some underlying mechanism. 

If we need to cycle an instance–the consumer can be paused, and the associated EBS drive detached and then re-attached to the new instance. So long as we keep the partition ID the same, re-assigning the disk is a fairly painless process that still guarantees correctness. 

In the case of a worker crash, we rely on RocksDB’s built-in [write-ahead-log](https://en.wikipedia.org/wiki/Write-ahead_logging) to ensure that we don’t lose messages. Messages are not committed from the input topic unless we have a guarantee that RocksDB has persisted the message in the log. 

## Reading the output topic

You may notice that up until this point, that there is no ‘atomic’ step here which allows us to ensure that we’ve delivered messages just once. It’s possible that our worker could crash at any point: writing to RocksDB, publishing to the output topic, or acknowledging the input messages. 

We need a ‘commit’ point that is atomic–and ensures that it covers the transaction for all of these separate systems. We need some “source of truth” for our data. 

That’s where reading from the output topic comes in. 

If the dedupe worker crashes for any reason or encounters an error from Kafka, when it re-starts it will first consult the “source of truth” for whether an event was published: **the output topic**. 

If a message was found in the output topic, but _not_ RocksDB (or vice-versa) the dedupe worker will make the necessary repairs to keep the database and RocksDB in-sync. In essence, we’re using the output topic as both our write-ahead-log, and our end source of truth, with RocksDB checkpointing and verifying it. 

## In Production

We’ve now been running our de-dupe system in production for 3 months, and are incredibly pleased with the results. By the numbers, we have:

  * **1.5 TB worth of keys** stored on disk in RocksDB

  * a **4-week** window of de-duplication before aging out old keys

  * approximately **60B** keys stored inside our RocksDB instances

  * **200B** messages passed through the dedupe system




The system has generally been fast, efficient, and fault tolerant–as well as extremely easy to reason about. 

In particular, the our v2 system has a number of advantages over our old de-duplication system. 

Previously we stored all of our keys in Memcached and used Memcached’s atomic CAS (check-and-set) operator to set keys if they didn’t exist. Memcached served as the commit point and ‘atomicity’ for publishing keys. 

While this worked well enough, it required a large amount of memory to fit all of our keys. Furthermore, we had to decide between accepting the occasional Memcached failures, or doubling our spend with high-memory failover replicas. 

The Kafka/RocksDB approach allows us to get almost all of the benefits of the old system, with increased reliability. To sum up the biggest wins:

**Data stored on disk:** keeping a full set of keys or full indexing in-memory was prohibitively expensive. By moving more of the data to disk, and leveraging various level of files and indexes, we were able to cut the cost of our bookkeeping by a wide margin. We are able to push the failover to cold storage (EBS) rather than running additional hot failover instances. 

**Partitioning** : of course, in order to narrow our search space and avoid loading too many indexes in memory, we need a guarantee that certain messages are routed to the right workers. Partitioning upstream in Kafka allows us to consistently route these messages so we can cache and query much more efficiently. 

**Explicit age-out:** with Memcached, we would set a TTL on each key to age them out, and then rely on the Memcached process to handle evictions. This caused us exhaust our memory in the face of large batches of data, and spike the Memcached CPU in the face of a large number of evictions. By having the client handle key deletion, we’re able to fail gracefully by shortening our ‘window of deduplication’. 

**Kafka as the source of truth:** to truly avoid de-duplication in the face of multiple commit points, we have to use a source of truth that’s common to all of our downstream consumers. Using Kafka as that ‘source of truth’ has worked amazingly well. In the case of most failures (aside from Kafka failures), messages will either be written to Kafka, or they wont. And using Kafka ensures that published messages are delivered in-order, and replicated on-disk across multiple machines, without needing to keep much data in memory. 

**Batching reads and writes:** by making batched I/O calls to Kafka and RocksDB, we’re able to get much better performance by leveraging sequential reads and writes. Instead of the random access we had before with Memcached, we’re able to achieve much better throughput by leaning into our disk performance, and keeping only the indexes in memory. 

Overall, we’ve been quite happy with the guarantees provided by the de-duplication system we’ve built. Using Kafka and RocksDB as the primitives for streaming applications has started to become [more and more the norm](https://www.confluent.io/blog/introducing-kafka-streams-stream-processing-made-simple/). And we’re excited to continue building atop these primitives to build new distributed applications. 

* * *

Thanks to [Rick Branson](https://twitter.com/rbranson), [Calvin French-Owen](https://twitter.com/calvinfo), [Fouad Matin](https://twitter.com/fouadmatin), [Peter Reinhardt](https://twitter.com/reinpk), [Albert Strasheim](https://twitter.com/fullung), [Josh Ma](https://twitter.com/munchybunch) and [Alan Braithwaite](https://github.com/abraithwaite) for providing feedback around this post.

###  Ready to see what Twilio Segment can do for you? 

[ Get a demo  ](https://segment.com/demo/?utm_referrer=https%3A%2F%2Fwww.twilio.com%2Fen-us%2Fblog%2Finsights%2Fexactly-once-delivery)

![](/content/dam/segment/cdp-report/CDP-cover-2025.png/_jcr_content/renditions/compressed-original.webp)

![](/content/dam/segment/cdp-report/CDP-cover-2025.png/_jcr_content/renditions/compressed-original.webp)

##  The Customer Data Platform Report 2025 

Drawing on anonymized insights from thousands of Twilio customers, the Customer Data Platform report explores how companies are using CDPs to unlock the power of their data.

[ Get the report  ](https://segment.com/the-cdp-report/?utm_referrer=https%3A%2F%2Fwww.twilio.com%2Fen-us%2Fblog%2Finsights%2Fexactly-once-delivery)

##  Related Posts 

  * [ ![Woman with glasses and green shirt smiling while using a laptop in a café](/content/dam/twilio-com/global/en/blog/segment-blog-migration/segment-generic---happy-dreamy-woman.jpg/_jcr_content/renditions/compressed-original.webp) Data you can depend on: why your data architecture should be built around your customer  Steven Schuler  ](https://www.twilio.com/en-us/blog/insights/data/data-you-can-depend-on)
  * [ ![Man in glasses standing by the window, smiling; colleagues discussing at a table in the background.](/content/dam/twilio-com/global/en/blog/segment-blog-migration/segment-generic---team-leader.jpg/_jcr_content/renditions/compressed-original.webp) Twilio Engage: Real-Time Signals, Richer Personalization, Remarkable Experiences Megan DeGruttola  ](https://www.twilio.com/en-us/blog/products/launches/twilio-engage-real-time-signals-richer-personalization-remarkable-experiences)
  * [ ![Woman in business attire shaking hands with a man in an office setting, with colleagues working in the background.](/content/dam/twilio-com/global/en/blog/segment-blog-migration/segment-generic---two-colleagues-handshake.jpg/_jcr_content/renditions/compressed-original.webp) Meet the New Data Graph Visual Builder: Model Your Data, Your Way Sean Spediacci  ](https://www.twilio.com/en-us/blog/products/launches/meet-the-new-data-graph-visual-builder-model)



##  Related Resources 

[ A newspaper article Twilio Docs From APIs to SDKs to sample apps API reference documentation, SDKs, helper libraries, quickstarts, and tutorials for your language and platform. ](https://www.twilio.com/docs) [ An Open book Resource Center The latest ebooks, industry reports, and webinars Learn from customer engagement experts to improve your own communication. ](/en-us/resource-center) [ User group reactions Ahoy Twilio's developer community hub Best practices, code samples, and inspiration to build communications and digital engagement experiences. ](/en-us/ahoy)

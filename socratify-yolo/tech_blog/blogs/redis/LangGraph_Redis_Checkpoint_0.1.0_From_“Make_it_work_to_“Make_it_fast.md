---
title: "LangGraph Redis Checkpoint 0.1.0: From “Make it work\" to “Make it fast\""
author: "Unknown"
url: "https://redis.io/blog/langgraph-redis-checkpoint-010/"
date: "2025-09-15"
---

# LangGraph Redis Checkpoint 0.1.0: From “Make it work" to “Make it fast"
August 29, 2025
[![Image](https://cdn.sanity.io/images/sy1jschh/production/b566b185b46861c427fcba7c47672a5882774185-100x100.jpg?w=256&q=80&fit=clip&auto=format)Jim Allen Wallace](/blog/author/jim-allenwallaceredis-com/)[![Brian Sam-Bodden](https://cdn.sanity.io/images/sy1jschh/production/1cc6f1d3c877a44e44d64a2974a1c93f90871704-361x349.png?w=750&q=80&fit=clip&auto=format)Brian Sam-Bodden](/blog/author/brian-sam-bodden/)
## A performance-driven redesign for production AI agents
When we [first announced LangGraph Redis integration](https://redis.io/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/) earlier this year, we were focused on bringing Redis' reliability and simplicity to the world of stateful AI agents. The initial releases (pre-0.1.0) were firmly in the "make it work" phase—we adapted the PostgreSQL reference implementation's patterns to Redis, ensuring functional parity across the LangGraph ecosystem.
After months of real-world usage and valuable feedback from early adopters, we recognized an opportunity to leverage Redis' performance story. Version 0.1.0 represents a fundamental redesign—not just optimizations, but a complete rethinking of how to structure checkpoint data for a high-performance in-memory data store.
## From SQL patterns to NoSQL performance
The original implementation followed the normalized, relational patterns of the PostgreSQL reference checkpointer. While this ensured compatibility and correctness, it didn't take advantage of Redis' unique strengths. We embarked on a comprehensive refactoring that embraces denormalization and Redis-native data structures.
### The key architectural changes
#### 1\. Denormalized storage: Inline channel values
The most impactful change was moving from a normalized storage model to an inline, document-oriented approach:
**Before (Normalized):**
**After (Denormalized):**
This single change eliminated O(m) FT.SEARCH queries per checkpoint retrieval (where m = number of channels), replacing them with a single JSON.GET operation.
#### 2\. Sorted Sets for write tracking
Instead of relying on FT.SEARCH queries to find pending writes, we introduced a Redis sorted set-based registry system:
This allows us to:
* Check write existence with ZCARD (O(1))
* Retrieve all write keys with ZRANGE (O(log(n) + m))
* Batch fetch writes with pipelined JSON.GET operations
#### 3\. Aggressive pipelining
We transformed sequential operations into batched pipeline executions. For example, the list_checkpoints operation now uses a three-phase pipeline approach:
This reduces network round trips from O(n) to O(3), regardless of the number of checkpoints.
## The numbers: Benchmarking methodology
To measure the impact of these changes, we developed a comprehensive benchmarking suite that tests all LangGraph checkpointer implementations (that we could get to work) using TestContainers for consistent, reproducible environments. The benchmarks:
* Run 5 iterations of each operation, taking the median
* Use Redis 8.0 with default configuration (no connection pooling optimization, 8 Query Engine worker threads)
* Test realistic agent workflows, including the LangGraph fanout pattern
* Measure operations per second for direct comparisons
All database containers run on the same machine with identical resource constraints, ensuring fair comparisons.
## Performance gains by operation
### Get Checkpoint
***Before**: 238 ops/sec (4.21ms)
***After**: 2,950 ops/sec (0.34ms)
***Improvement**:**12.4x faster**
The inline storage model transforms checkpoint retrieval from multiple search operations to a single JSON.GET.
### List Checkpoints
***Before**: 22 ops/sec (45.03ms)
***After**: 696 ops/sec (1.44ms)
***Improvement**:**31.6x faster**
Batch loading of pending writes via sorted sets eliminates the O(n) FT.SEARCH queries.
### Put Checkpoint
***Before**: 2,596 ops/sec (0.39ms)
***After**: 1,647 ops/sec (0.61ms)
***Trade-off**: 37% slower but includes inline storage setup
The slight regression in put operations is intentional—we're doing more work upfront (storing channel values inline, maintaining the key registry) to dramatically accelerate read operations.
### Fanout pattern: The scalability test
The fanout benchmark tests a critical LangGraph pattern where work is distributed to multiple parallel subgraphs—a common pattern for agent swarms and parallel task execution.
**Fanout-100 (100 parallel branches):**
***Redis**: 846ms (ranked 5th overall)
* Faster than PostgreSQL (1,959ms) and MySQL (7,183ms)
**Fanout-500 (500 parallel branches):**
***Redis**: 4,578ms (ranked 5th overall)
* Scales better than PostgreSQL (9,997ms) and MySQL (34,637ms)
The fanout pattern stresses checkpoint creation, write tracking, and state merging—areas where our optimizations shine at scale.
## Comparative performance
With these optimizations, Redis checkpoint operations now consistently outperform several alternatives:
**Get checkpoint performance**(operations/second):
1. Memory: 8,392 ops/sec
2. SQLite: 7,083 ops/sec
3.**Redis: 2,950 ops/sec**✨
4. MySQL: 1,152 ops/sec
5. PostgreSQL: 1,038 ops/sec
6. MongoDB: 659 ops/sec
**List checkpoints performance**(operations/second):
1. Memory: 21,642 ops/sec
2. SQLite: 5,766 ops/sec
3.**Redis: 696 ops/sec**✨
4. PostgreSQL: 695 ops/sec
5. MySQL: 664 ops/sec
6. MongoDB: 126 ops/sec
## Additional Optimizations
Beyond the Redis-specific changes, we implemented several Python-level optimizations:
***orjson**: Replaced standard json library with orjson for 2-3x faster serialization
***Cached key generation**: Reduced string formatting overhead
***asyncio.gather()**: Parallelized independent async operations
***Eliminated redundant fetches**: Fixed a bug in shallow async that caused duplicate checkpoint retrievals
## Room for further optimization
These benchmarks use default Redis configurations. Production deployments can achieve even better performance by tuning. It is also fair to note that we did not do any fine-tuning of the other systems benchmarked, as this was not an effort to beat any of them but to make our implementation the best possible for our customers:
***FT.SEARCH worker threads**: Increase from default for parallel search operations
***Connection pooling**: Configure pool size based on concurrent load
***Redis cluster mode**: Distribute load across multiple nodes
## Breaking changes and migration
Version 0.1.0 introduces breaking changes in the storage format. New checkpoints use inline channel values, while the system cannot read pre-0.1.0 checkpoints without migration. This was a deliberate decision—we prioritized performance for new deployments over maintaining backward compatibility (at this early stage in the library's life), which would compromise the optimizations.
## Looking forward
The journey from 0.0.x to 0.1.0 demonstrates our commitment to making Redis not just a functional choice for LangGraph checkpointing, but a performance-optimized one. By embracing Redis' strengths—in-memory operations, efficient data structures, and pipelining—we've significantly changed the performance signature of the project.
Whether you're building agent swarms that spawn hundreds of parallel tasks or need sub-millisecond checkpoint retrieval for real-time applications, LangGraph Redis 0.1.0 delivers the performance that production AI systems demand.
## Getting Started
For async applications, use AsyncRedisSaver for even better performance in high-concurrency scenarios.
## Acknowledgments
This performance journey wouldn't have been possible without the feedback from early adopters who pushed the library by building some impressive stateful AI agent systems. Your real-world usage patterns and performance requirements shaped every optimization in this release.
## Ready to build?
_Ready to build high-performance AI agents with Redis?_
_Check out the[docs](https://github.com/redis-developer/langgraph-redis) and join our community to share your experiences with LangGraph Redis 0.1.0._
[Redis Docs](https://github.com/redis-developer/langgraph-redis)

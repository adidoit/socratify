---
title: "Guardians of consistency"
author: "https://medium.com/@onno.vos.dev"
url: "https://engineering.klarna.com/guardians-of-consistency-caf10252313e?source=rss----86090d14ab52---4"
date: "2025-09-15"
---

# Guardians of consistency
[![Onno Vos Dev](https://miro.medium.com/v2/resize:fill:64:64/1*FUfkRZu2ecHPJRESfeJP5w.png)](https://medium.com/@onno.vos.dev?source=post_page---byline--caf10252313e---------------------------------------)
[Onno Vos Dev](https://medium.com/@onno.vos.dev?source=post_page---byline--caf10252313e---------------------------------------)
11 min read
·
Mar 12, 2025
[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fklarna-engineering%2Fcaf10252313e&operation=register&redirect=https%3A%2F%2Fengineering.klarna.com%2Fguardians-of-consistency-caf10252313e&user=Onno+Vos+Dev&userId=11e5d7d195d4&source=---header_actions--caf10252313e---------------------clap_footer------------------)
\--
[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fcaf10252313e&operation=register&redirect=https%3A%2F%2Fengineering.klarna.com%2Fguardians-of-consistency-caf10252313e&source=---header_actions--caf10252313e---------------------bookmark_footer------------------)
Listen
Share
## The Quest for Mnesia-Like Compatibility
Press enter or click to view image in full size
In [part 1](/the-fellowship-of-the-forgotten-d341045a6123), you’ve read about the journey of moving from Mnesia to Postgres with zero downtime. In this blog post we will focus on database isolation levels and how we managed to make Postgres behave like Mnesia and how we ensured our implementation of serializable on top of Postgres met the requirements for serializable isolation level.
### A brief look into database isolation levels
The SQL standard defines four isolation levels, in increasing order: _“READ UNCOMMITTED”, “READ COMMITTED”, “REPEATABLE READ”_ and “ _SERIALIZABLE_ ” with Postgres essentially only providing the latter three since read uncommitted maps to read committed in Postgres. Let’s take a brief look at each without essentially turning this into a separate blog post dedicated to discussing this topic in detail. If you want to learn more, [the Postgres documentation](https://www.postgresql.org/docs/current/transaction-iso.html#TRANSACTION-ISO) is a great starting point.
**Read committed
**Transactions with read committed can read only committed data from before the query began. It will never see uncommitted data or changes committed by a concurrent transaction. In essence, it sees a snapshot of the database as of the moment each query in a transaction begins to run. So, two _SELECT_ statements within a transaction can see different data if a concurrent transaction is committed in between the first and second _SELECT_ statement.
**Repeatable read
**Just like read committed, repeatable read only sees the data committed before the transaction began. Where it differs however is that it doesn’t see committed changes from concurrent transactions. Whereas read committed could see different data between two _SELECT_ statements, repeatable read does not.
**Serializable
**Serializable is the strictest isolation level. With serializable, it is as if all transactions had been executed serially rather than concurrently. It behaves exactly like repeatable read, except it also ensures that any possible serial execution of a set of transactions has the same consistent outcome as their concurrent execution.
### Introduction to Mnesia
Before we deep dive into how we managed to make Postgres behave exactly like [Mnesia](https://www.erlang.org/doc/apps/mnesia/mnesia.html), we need a little bit of an understanding of the previous database technology that was used by KRED. Mnesia is a distributed key-value database and is written in Erlang, and distributed as part of Erlang [OTP](https://github.com/erlang/otp). Data can be stored in memory or on disk. Furthermore, Mnesia can be extended with various storage backends such as [mnesia_eleveldb](https://github.com/klarna/mnesia_eleveldb) or [mnesia_rocksdb](https://github.com/aeternity/mnesia_rocksdb).
A key thing is that Mnesia provides transactional properties such as atomicity, consistency, isolation and durability just as any other SQL database. With the exception of so called “[dirty operations](https://www.erlang.org/doc/apps/mnesia/mnesia_chap4.html#dirty-operations)”, Mnesia uses a serializable isolation level.
### Smoking gun on why serializable isolation level did not work
Since KRED was developed with a serializable isolation level in mind, one of our biggest challenges turned out to be running KRED on Postgres with the same isolation level.
Postgres provides a serializable isolation level and naturally we attempted to use this isolation level. However, when running one of our batch jobs, we constantly failed transactions with serialization failures. Strangely enough, these happened whenever we tried writing keys which were exclusively processed by one single process. This made us think that the excess of serialization errors may be due to internal false positives in the way it handles transactions with serializable isolation level. It was time to check out Postgres master branch, patching and start debugging our way in Postgres as to why we were experiencing so many restarts.
The first question to answer was: Are we having serialization errors due to potential conflicts between this batch job and other processes?
One way to figure this out was by adding more logs in Postgres so that we can log the other transaction_id which conflicts with the currently executing transaction. After adding this log, we discovered that conflicts were occurring between concurrent transactions.
Finally, we applied a change in Postgres that would log all the lock types at the time of detecting the serialization error. At this point we noticed that we were getting tuple locks on the relationship and page lock on the primary key relationship. This would explain why we were experiencing serialization errors even though transactions were operating on disjoint keys.
After a lot of iterations and deeper debugging in Postgres we managed to come up with a SQL snippet that proves our initial theory: Postgres throws a lot of false positives for KRED’s workload.
The following snippet proves that:
-- Setup
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (user_id numeric primary key, balance numeric);
-- transaction 1:
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT balance FROM accounts WHERE user_id = 1;
-- transaction 2:
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT balance FROM accounts WHERE user_id = 2;
INSERT INTO accounts (user_id, balance) VALUES (2, 300);
-- transaction 1:
INSERT INTO accounts (user_id, balance) VALUES (1, 200);
COMMIT;
-- transaction 2:
COMMIT;
We believe that most of our serialization errors come from concurrent updates of key rows for which the keys are stored in the same page in the primary key relation. More information on this topic can be found in [this article](http://www.interdb.jp/pg/pgsql05.html#:~:text=to%20concurrent%20update-,5.9,-.%20Serializable%20Snapshot%20Isolation).
Seeing as KRED is heavily parallelized, these kinds of restarts happen all the time leading to low throughput and high latency.
Given this, we decided to try another solution, lower the isolation level and somehow still maintain the same guarantees as we would get with serializable.
### How we replicated Mnesia’s serializable implementation in Postgres
To achieve serializable-like guarantees, we started looking into the Mnesia implementation of achieving serializable transactions. Mnesia uses a combination of read/write locks plus table table locks whenever needed. While going through the Postgres documentation, we noticed two locking mechanisms that could help us: [select_for_share](https://www.postgresql.org/docs/14/explicit-locking.html#LOCKING-ROWS) and [advisory locks](https://www.postgresql.org/docs/14/explicit-locking.html#ADVISORY-LOCKS).
To quote official Postgres docs:
_SELECT…FOR SHARE_ behaves similarly to _FOR NO KEY UPDATE_ , except that it acquires a shared lock rather than exclusive lock on each retrieved row. A shared lock blocks other transactions from performing _UPDATE_ , _DELETE, SELECT FOR UPDATE_ or _SELECT FOR NO KEY UPDATE_ on these rows, but it does not prevent them from performing _SELECT FOR SHARE_ or _SELECT FOR KEY SHARE_.
This starts to feel very close to Mnesia’s implementation of read locks. Once a transaction acquires a read lock, other transactions can acquire read locks for the same row but no other transaction can acquire a write lock.
_SELECT FOR SHARE_ is a good fit for concurrency control whenever the _SELECT_ returns rows. However there are two issues with _SELECT FOR SHARE_. Postgres doesn’t lock records that do not exist when a _SELECT_ is run while another transaction has created it.
Secondly, Postgres does not lock records that do not match a _SELECT_ while another transaction modified a record so that it would become matching. This is in contrast with Mnesia which does take a lock on a read even though the record does not exist in the database.
The following scenario illustrates the first issue:
DROP TABLE IF EXISTS test;
CREATE TABLE test (id int PRIMARY KEY, value int);
INSERT INTO test (id, value) VALUES (1, 10), (2, 20);
BEGIN; -- T1
BEGIN; -- T2
INSERT INTO test (id, value) VALUES (3, 30); -- T1
SELECT * FROM test WHERE id = 4 FOR SHARE; -- T1
INSERT INTO test (id, value) values(4, 42); -- T2
SELECT * FROM test WHERE id=3 FOR SHARE; -- T2 (0 rows)
COMMIT; -- T1
COMMIT; -- T2
The outcome of T2 will be 0 rows! Had these transactions been executed in serializable isolation level the possible outcomes, due to serializable failures which would abort one of the transactions, would have been:
T1 -> T2 [(3, 30)]
T2 -> T1 [(4, 42)]
This problem can be fixed by manual locking through advisory locks. Inserts, updates and deletes by key will get a non-blocking exclusive advisory lock on the key(s) they operate on. Furthermore, whenever we select a record by key for set/ordered_set tables but don’t find a record, we take a non-blocking shared advisory lock on it in order to avoid concurrent transactions from creating it. For bag tables, tables which can have many objects but only one instance of each object per key, we acquire a shared advisory lock on its key to prevent more records from being added under the same key and then read the actual key. Whenever selecting, inserting, updating or deleting records with some filter instead of by key, we place a shared read lock on the full table to prevent previously non-matching records to be changed to matching ones. The latter is rarely done in KRED so such full table locks are an extremely rare occurrence.
The non-blocking behavior was chosen so that we can get back a fast reply from Postgres if the resource is already locked. In cases when the resource is locked we will get back false from Postgres which in turn could be used as a mechanism to simulate transaction restarts.
So to summarize, we can achieve serializable like guarantees by:
* Every _INSERT/DELETE/UPDATE_ that operates on a single key first acquires an exclusive non-blocking advisory lock and executes the statement if there was not already a lock acquired by reading the key.
* Every _SELECT_ operating on a single key is using _FOR SHARE_.
* For set/ordered_set tables, if a _SELECT FOR SHARE_ on a key does not return a record, we acquire a shared non-blocking advisory lock. After placing the lock, we re-run the select again and check if we get back a non-empty result. If so, a race condition has occurred, and we restart the transaction.
* For bag tables, every _SELECT_ starts by acquiring a shared non-blocking advisory lock on the key and executes the select.
* Every query that _SELECT/DELETE/UPDATE_ by some filter instead of by primary key, should acquire a table lock in shared mode.
* Every transaction runs under read committed isolation level.
* Dirty reads should be implemented as regular _SELECT_ under read committed isolation level but won’t acquire any advisory lock nor use _FOR SHARE_.
So how can we be sure that this methodology worked? There are two ways we can prove this: [hermitage](https://github.com/ept/hermitage/blob/master/postgres.md) as well as [property based testing](https://www.propertesting.com/)! Let’s look at these one by one.
### Hermitage to the rescue!
First off, we can look at the [hermitage](https://github.com/ept/hermitage/blob/master/postgres.md) examples and inject our for share and advisory locking strategies into each of these examples and ensure that they pass.
For example, repeatable read (one higher isolation level than read committed) does not prevent Write Skew as per the below example:
DROP TABLE IF EXISTS test;
CREATE TABLE test (id int PRIMARY KEY, value int);
INSERT INTO test (id, value) VALUES (1, 10), (2, 20);
BEGIN; SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; -- T1
BEGIN; SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; -- T2
SELECT * FROM test WHERE id IN (1,2); -- T1
SELECT * FROM test WHERE id IN (1,2); -- T2
UPDATE test SET value = 11 WHERE id = 1; -- T1
UPDATE test SET value = 21 WHERE id = 2; -- T2
COMMIT; -- T1
COMMIT; -- T2
Whereas in our scenario the same would be executed as per the following example:
DROP TABLE IF EXISTS test;
CREATE TABLE test (id int PRIMARY KEY, value int);
INSERT INTO test (id, value) VALUES (1, 10), (2, 20);
BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED; -- T1
BEGIN; SET TRANSACTION ISOLATION LEVEL READ COMMITTED; -- T2
SELECT * FROM test WHERE id IN (1,2) FOR SHARE; -- T1 => [(1, 10), (2, 20)]
SELECT * FROM test WHERE id IN (1,2) FOR SHARE; -- T2 => [(1, 10), (2, 20)]
SELECT pg_try_advisory_xact_lock(1); -- T1
UPDATE test SET value = 11 WHERE id = 1; -- T1, hangs due to locking via FOR SHARE in T2
SELECT pg_try_advisory_xact_lock(2); -- T2
UPDATE test SET value = 21 WHERE id = 2; -- T2, ERROR: deadlock detected => T2 will restart
COMMIT; -- T1, 1 => 11
ABORT; -- T2
In case of serializable isolation level T2 would have failed at commit with serialization error. In both cases, we end up with a serializable chain of events, we just abort slightly earlier.
Writing down all the scenarios and our modified versions of it would be too much for the sake of this blog post but every scenario in the hermitage library passes with our approach. Recently, I wrote a library for automated testing of hermitage scenarios (see [issue #17](https://github.com/ept/hermitage/issues/17)) which I hope to open source in the short term and allow others to use and deep-dive further into our implementation as well as other database technologies and test them in an automated fashion.
### Property based testing our approach
Even so, the question was raised if there’s a better way that we can test this. Obviously we cannot run through a couple dozen examples manually every time we make a change to our library. We need something more solid than that. [Property based testing](https://www.propertesting.com/) proved to be the answer here. Given that Mnesia provides a serializable isolation level, we can write property based tests that generate a random sequence of database operations inside a transaction and run them both against Mnesia and Postgres. If there’s a difference, then we know that one of the two is not serializable.
Given two Mnesia transactions, each reading a particular balance where one adds interest and the other adds a payment. We can reverse the operations and first add a payment followed by interest and still end up with the same result. Both versions are recorded as serializable outcomes.
We then go one step further and attempt all possible interleavings of the database operations using two processes and verifies that the transactions won’t deadlock or lead to a third result.
Since this suite is part of the CI, we run this all the time and on an average month run the same suite 500 times. With a relatively large number of iterations and all kinds of combinations of table types, secondary indexes, writes, deletes, reads, etc. we can be confident that as long as the serializability suite passes, we have achieved serializability with our approach.
By running these tests, we actually managed to discover two bugs in Mnesia’s implementation of serializable isolation level while our solution was passing. The mentioned bugs were the following:
* [Fix for delete_object at read on a set table](https://github.com/erlang/otp/pull/2663)
* [Do not unconditionally delete index keys](https://github.com/erlang/otp/pull/5131)
### Final notes
So should everyone use our approach now? No, probably not. If your application is using Mnesia or a Mnesia-like setup, then maybe. This approach, just as out-of-the-box serializable, comes with a small performance impact. We have a slightly higher CPU and RAM consumption with our approach but at a negligible cost. To reduce this further, we keep track of locks already acquired on the client side to avoid attempting to grab locks that we already hold. Since updates in KRED are typically done in a “read current value -> update it -> write new value” type of pattern, this optimization eliminates advisory locks on the great majority of _INSERT/UPDATE/DELETE_ queries. From the client’s side, KRED is already built with Mnesia in mind and all business code expects the same kind of locking behavior. So any performance penalty that is paid by this approach, was already paid for by Mnesia as well.
This was certainly not an easy journey but a fun one it was! Thinking out of the box and comparing two database technologies with each other allowed us to make one behave exactly like the other and allowed us a smoooth migration where we could be confident that the very foundation of KRED, serializable transactions, could be upheld!

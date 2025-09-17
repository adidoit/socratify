---
title: "What Powers Instagram: Hundreds of Instances, Dozens of Technologies"
company: "instagram"
url: "https://instagram-engineering.com/what-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad"
type: "final_harvest"
date: "2025-09-15"
---

# What Powers Instagram: Hundreds of Instances, Dozens of Technologies

[![Instagram Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*8x_1IP3b75o5u9M4LgFBig.jpeg)](https://medium.com/@InstagramEng?source=post_page---byline--adf2e22da2ad---------------------------------------)

[Instagram Engineering](https://medium.com/@InstagramEng?source=post_page---byline--adf2e22da2ad---------------------------------------)

6 min read

·

Dec 2, 2011

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Finstagram-engineering%2Fadf2e22da2ad&operation=register&redirect=https%3A%2F%2Finstagram-engineering.com%2Fwhat-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad&user=Instagram+Engineering&userId=a4c6efa67fe0&source=---header_actions--adf2e22da2ad---------------------clap_footer------------------)

\--

20

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fadf2e22da2ad&operation=register&redirect=https%3A%2F%2Finstagram-engineering.com%2Fwhat-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad&source=---header_actions--adf2e22da2ad---------------------bookmark_footer------------------)

Listen

Share

One of the questions we always get asked at meet-ups and conversations with other engineers is, “what’s your stack?” We thought it would be fun to give a sense of all the systems that power Instagram, at a high-level; you can look forward to more in-depth descriptions of some of these systems in the future. This is how our system has evolved in the just-over-1-year that we’ve been live, and while there are parts we’re always re-working, this is a glimpse of how a startup with a small engineering team can scale to our 14 million+ users in a little over a year. Our core principles when choosing a system are:

  * Keep it very simple
  * Don’t re-invent the wheel
  * Go with proven and solid technologies when you can



We’ll go from top to bottom:

## OS / Hosting

We run Ubuntu Linux 11.04 (“Natty Narwhal”) on Amazon EC2. We’ve found previous versions of Ubuntu had all sorts of unpredictable freezing episodes on EC2 under high traffic, but Natty has been solid. We’ve only got 3 engineers, and our needs are still evolving, so self-hosting isn’t an option we’ve explored too deeply yet, though is something we may revisit in the future given the unparalleled growth in usage.

## Load Balancing

Every request to Instagram servers goes through load balancing machines; we used to run 2 [nginx](http://t.umblr.com/redirect?z=http%3A%2F%2Fnginx.org&t=OTJjODk2YzBhOGE4ZjczNjEyZWUzNzY0MDFlZDc4ODE3ZjhiNGVjMixDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) machines and DNS Round-Robin between them. The downside of this approach is the time it takes for DNS to update in case one of the machines needs to get decomissioned. Recently, we moved to using Amazon’s Elastic Load Balancer, with 3 NGINX instances behind it that can be swapped in and out (and are automatically taken out of rotation if they fail a health check). We also terminate our SSL at the ELB level, which lessens the CPU load on nginx. We use Amazon’s Route53 for DNS, which they’ve recently added a pretty good GUI tool for in the AWS console.

## Application Servers

Next up comes the application servers that handle our requests. We run [Django](http://t.umblr.com/redirect?z=https%3A%2F%2Fwww.djangoproject.com%2F&t=YmYzYmUzOWI0NGIyZDU5NTk3NmNhZjFhZWI5ZTBkYzJjZTEzYjVkYyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1)on Amazon High-CPU Extra-Large machines, and as our usage grows we’ve gone from just a few of these machines to over 25 of them (luckily, this is one area that’s easy to horizontally scale as they are stateless). We’ve found that our particular work-load is very CPU-bound rather than memory-bound, so the High-CPU Extra-Large instance type provides the right balance of memory and CPU.

We use [http://gunicorn.org/](http://t.umblr.com/redirect?z=http%3A%2F%2FGunicorn&t=YTJlMjA5NGRhNDQxODI0NGY5MDQzOGM4OTVjMTE0NTVlN2MyYWFjZixDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) as our WSGI server; we used to use mod_wsgi and Apache, but found Gunicorn was much easier to configure, and less CPU-intensive. To run commands on many instances at once (like deploying code), we use [Fabric](http://t.umblr.com/redirect?z=http%3A%2F%2Ffabric.readthedocs.org%2Fen%2F1.3.3%2Findex.html&t=NWI5YWQzMmRlOWE5NDAwYTMxMjMzMzMzMjAwMDRmMTNlYTI4NDNmOSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), which recently added a useful parallel mode so that deploys take a matter of seconds.

## Data storage

Most of our data (users, photo metadata, tags, etc) lives in PostgreSQL; we’ve [previously written](http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram) about how we shard across our different Postgres instances. Our main shard cluster involves 12 Quadruple Extra-Large memory instances (and twelve replicas in a different zone.)

We’ve found that Amazon’s network disk system (EBS) doesn’t support enough disk seeks per second, so having all of our working set in memory is extremely important. To get reasonable IO performance, we set up our EBS drives in a software RAID using mdadm.

As a quick tip, we’ve found that [vmtouch](http://t.umblr.com/redirect?z=http%3A%2F%2Fhoytech.com%2Fvmtouch%2Fvmtouch.c&t=Y2Q1ODE5OWRjOWI1NGE5ZDczMmQ1MzU0Nzk0NjkxNDdmNzI2YzJiMSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) is a fantastic tool for managing what data is in memory, especially when failing over from one machine to another where there is no active memory profile already. [Here is the script](http://t.umblr.com/redirect?z=https%3A%2F%2Fgist.github.com%2F1424540&t=MmFkZTcxNDExYzE4ZDE2NGRlMmU2NDljMGQzZDk0NWY4ZDI0ZTYxYyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) we use to parse the output of a vmtouch run on one machine and print out the corresponding vmtouch command to run on another system to match its current memory status.

All of our PostgreSQL instances run in a master-replica setup using Streaming Replication, and we use EBS snapshotting to take frequent backups of our systems. We use XFS as our file system, which lets us freeze & unfreeze the RAID arrays when snapshotting, in order to guarantee a consistent snapshot (our original inspiration came from [ec2-consistent-snapshot](http://t.umblr.com/redirect?z=http%3A%2F%2Falestic.com%2F2009%2F09%2Fec2-consistent-snapshot&t=OWE1YTJjZGQ4YWYyMDYxMWNiMTJmOGM3YmQ5ZTI2NGYxOWZmNGU1OCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1). To get streaming replication started, our favorite tool is [repmgr](http://t.umblr.com/redirect?z=https%3A%2F%2Fgithub.com%2Fgreg2ndQuadrant%2Frepmgr&t=YmFlYmVjOTZiYzE1MTNmZmExYzQzOGMyYmFhMjY1ZmZlMjcwMmE1YSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) by the folks at 2ndQuadrant.

To connect to our databases from our app servers, we made early on that had a huge impact on performance was using [Pgbouncer](http://t.umblr.com/redirect?z=http%3A%2F%2Fpgfoundry.org%2Fprojects%2Fpgbouncer%2F&t=ZWUxMDc5ZDMyMDJiZGZmYzZkMmY1NGY4NjBkYWM1MTE0YmY1MDkyMCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) to pool our connections to PostgreSQL. We found [Christophe Pettus’s blog](http://t.umblr.com/redirect?z=http%3A%2F%2Fthebuild.com%2Fblog%2F&t=ZDEyODliODkzNWFkYzk4YzQwODk1NjA1ZTZjOTAyYmEyMmE5OTQ2MCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) to be a great resource for Django, PostgreSQL and Pgbouncer tips.

The photos themselves go straight to Amazon S3, which currently stores several terabytes of photo data for us. We use Amazon CloudFront as our CDN, which helps with image load times from users around the world (like in Japan, our second most-popular country).

We also use [Redis](http://t.umblr.com/redirect?z=http%3A%2F%2Fredis.io%2F&t=ODRkNDRjY2NhNDQ2YzhjMzk0MGMyNWY4MTcxNGQ0OTNhOTAzZjU5YixDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) extensively; it powers our main feed, our activity feed, our sessions system ([here’s our Django session backend](http://t.umblr.com/redirect?z=https%3A%2F%2Fgist.github.com%2F910392&t=NDQ4NjZjMDhhYjgyMGU0ZGJkN2E5Yjg3NWMxOTFiNmVkODIxMzBiYSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1)), and other [related systems](http://instagram-engineering.tumblr.com/post/12202313862/storing-hundreds-of-millions-of-simple-key-value-pairs). All of Redis’ data needs to fit in memory, so we end up running several Quadruple Extra-Large Memory instances for Redis, too, and occasionally shard across a few Redis instances for any given subsystem. We run Redis in a master-replica setup, and have the replicas constantly saving the DB out to disk, and finally use EBS snapshots to backup those DB dumps (we found that dumping the DB on the master was too taxing). Since Redis allows writes to its replicas, it makes for very easy online failover to a new Redis machine, without requiring any downtime.

For our [geo-search API](http://t.umblr.com/redirect?z=http%3A%2F%2Finstagram.com%2Fdeveloper%2Fendpoints%2Fmedia%2F%23get_media_search&t=NjI3OTQxOTQ1NjYwMGI4OGY5ZjEwZjNiZmIwNTA3ZGFlYzUyMTZiNixDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), we used PostgreSQL for many months, but once our Media entries were sharded, moved over to using [Apache Solr](http://t.umblr.com/redirect?z=http%3A%2F%2Flucene.apache.org%2Fsolr%2F&t=ZjY2OGU3NTFkMGY3NTFmN2NlMzc3ZmU0OTRkNDgzNzNkMTZjODAwMyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1). It has a simple JSON interface, so as far as our application is concerned, it’s just another API to consume.

Finally, like any modern Web service, we use Memcached for caching, and currently have 6 Memcached instances, which we connect to using pylibmc & libmemcached. Amazon has an Elastic Cache service they’ve recently launched, but it’s not any cheaper than running our instances, so we haven’t pushed ourselves to switch quite yet.

## Task Queue & Push Notifications

When a user decides to share out an Instagram photo to Twitter or Facebook, or when we need to notify one of our [Real-time subscribers](http://t.umblr.com/redirect?z=http%3A%2F%2Finstagram.com%2Fdeveloper%2Frealtime%2F&t=YWNlMGQ5NDI2NDJiZWVmZTg4MjQ4ODYxNWVlYTVmNDU2NmFjZjFmMCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) of a new photo posted, we push that task into [Gearman](http://t.umblr.com/redirect?z=http%3A%2F%2Fgearman.org%2F&t=NjlhZjk2ODU4ZWIxMmI0M2YzMzcyNjc0ZTQ2NzM5ZWVkOTVmMmVjOSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), a task queue system originally written at Danga. Doing it asynchronously through the task queue means that media uploads can finish quickly, while the ‘heavy lifting’ can run in the background. We have about 200 workers (all written in Python) consuming the task queue at any given time, split between the services we share to. We also do our feed fan-out in Gearman, so posting is as responsive for a new user as it is for a user with many followers.

For doing push notifications, the most cost-effective solution we found was [https://github.com/samuraisam/pyapns](http://t.umblr.com/redirect?z=http%3A%2F%2FPyAPNS&t=MzkzZTY0ZTcyYWE1NzFiNDFmMGExOTFlNjQ4YjJkZWZjNTk5MzE1MyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), an open-source Twisted service that has handled over a billion push notifications for us, and has been rock-solid.

## Monitoring

With 100+ instances, it’s important to keep on top of what’s going on across the board. We use [Munin](http://t.umblr.com/redirect?z=http%3A%2F%2Fmunin-monitoring.org%2F&t=NzhjNjdkOTNiNTA5ZjQ5ZjY0NDA1Mzc0M2I4OTlkYzEyZjJjNTg4OSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) to graph metrics across all of our system, and also alert us if anything is outside of its normal range. We write a lot of custom Munin plugins, building on top of [Python-Munin](http://t.umblr.com/redirect?z=http%3A%2F%2Fsamuelks.com%2Fpython-munin%2F&t=MjZmNzViNjNmZThjNjc2MmZlZTQ4OWEwODc0MjdlYzk5OTliZTljNCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), to graph metrics that aren’t system-level (for example, signups per minute, photos posted per second, etc). We use [Pingdom](http://t.umblr.com/redirect?z=http%3A%2F%2Fpingdom.com&t=YmJjNmNkMDJjYjZiNzkyYWI3OTk2NzU1YjU5MjFhYTRlODUwMmEyMyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) for external monitoring of the service, and [PagerDuty](http://t.umblr.com/redirect?z=http%3A%2F%2Fpagerduty.com&t=ZWRiZDkyYzM4ZGRhMTY4MDFjYjJiYjhiNjAzYTkyMWZjOWUyN2M4OCxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1) for handling notifications and incidents.

For Python error reporting, we use [Sentry](http://t.umblr.com/redirect?z=http%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjango-sentry&t=NjBkNTdjMmM5ZjM3MzAyZDVkNmNhNTA4ZGZkMGUxNTAzNGU5YjIyZSxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1), an awesome open-source Django app written by the folks at Disqus. At any given time, we can sign-on and see what errors are happening across our system, in real time.

## You?

If this description of our systems interests you, or if you’re hopping up and down ready to tell us all the things you’d change in the system, we’d love to hear from you. [We’re looking for a DevOps person to join us and help us tame our EC2 instance herd](http://t.umblr.com/redirect?z=http%3A%2F%2Finstagr.am%2Fabout%2Fjobs%2F&t=NzFiZWVmZWZjOGMzMWQ4M2NkMjEzOTRiMDY3Yjk5NWZjNDZjNDUzYyxDTkhKTHlScA%3D%3D&b=t%3A3lU1XNmZZGkFDk-fPGXVAA&m=1).

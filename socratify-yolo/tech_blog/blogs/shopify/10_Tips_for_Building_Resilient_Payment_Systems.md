---
title: "10 Tips for Building Resilient Payment Systems"
company: "shopify"
url: "https://shopify.engineering/building-resilient-payment-systems"
type: "system_architecture"
date: "2025-09-15"
---

[blog](/)|[Development](/topics/development)

# 10 Tips for Building Resilient Payment Systems

The top 10 tips and tricks for building resilient payment systems from a Staff Developer working on Shopify’s payment infrastructure.

Published on Jul 28, 2022

![10 Tips for Building Resilient Payment Systems](https://cdn.shopify.com/s/files/1/0779/4361/articles/ShopifyEng_BlogIllustrations_210719_72ppi_06_HowWeRestartThousandsOfProxySQLs.jpg?v=1659022840&originalWidth=1848&originalHeight=782)

Engineering at Shopify

We’re hiring

[See open roles](https://www.shopify.com/careers#Engineering)

During the past five years I’ve worked on a lot of different parts of Shopify’s payment infrastructure and helped onboard dozens of developers in one way or another. Some people came from different programming languages, others used Ruby before but were new to the payments space. What was mostly consistent among new team members was little experience in building systems at Shopify’s scale—it was new for me too when I joined.

> ⏪ Rewinding for a moment — preparing for an event of this scale doesn't happen overnight. In anticipation of BFCM 2021 we began load testing back in July! To better simulate real global traffic we spread out our load generation across [@GoogleCloud](https://twitter.com/googlecloud?ref_src=twsrc%5Etfw)'s global network. [pic.twitter.com/5oXqFOadae](https://t.co/5oXqFOadae)
> 
> — Shopify Engineering (@ShopifyEng) [November 30, 2021](https://twitter.com/ShopifyEng/status/1465806698954772489?ref_src=twsrc%5Etfw)

It’s hard to learn something when you don’t know what you don’t know. As I learned things over the years—sometimes the hard way—I eventually found myself passing on these lessons to others. I distilled these topics into a presentation I gave to my team and boiled that down into this blog post. So, without further ado, here are my top 10 tips and tricks for building resilient payment systems.

# 1\. Lower Your Timeouts

Ruby’s built-in `Net::HTTP` client has a default timeout of 60 seconds to open a connection to a server, 60 seconds to write data, and another 60 seconds to read a response. For online applications where a human being is waiting for something to happen, this is too long. At least there’s a default timeout in place. HTTP clients in other programming languages, like `http.Client` in Go and `http.request` in Node.JS don’t have a default timeout at all! This means an unresponsive server could tie up your resources indefinitely and increase your infrastructure bill unnecessarily.

Timeouts can also be set in data stores. For example MySQL has the [MAX_EXECUTION_TIME](https://dev.mysql.com/doc/refman/5.7/en/optimizer-hints.html#optimizer-hints-execution-time "Optimizer Hints") optimizer hint for setting a per-SELECT query timeout in milliseconds. Combined with other tools like [pt-kill](https://www.percona.com/doc/percona-toolkit/LATEST/pt-kill.html "pt-kill"), we try to prevent bad queries from overwhelming the database.

If there’s only a single thing you take away from this post, dear reader, it should be to investigate and set low timeouts everywhere you can. _But what is the right timeout to set?_ you may wonder. That ultimately depends on your application’s unique situation and can be deduced with monitoring (more on that later), but I found that an open timeout of one second with a write and read or query timeout of five seconds is a decent starting point. Consider this waiting time from the perspective of the end user: would you like to wait for more than five seconds for a page to load successfully or show an error?

# 2\. Install Circuit Breakers

Timeouts put an upper bound on how long we wait before giving up. But services that go down tend to stay down for a while, so if we see multiple timeouts in a short period of time, we can improve on this by not trying at all. Much like the circuit breaker you will find in your house or apartment, once the circuit is opened or **tripped** , nothing is let through.

Shopify developed [Semian](https://github.com/Shopify/semian "Semian - Shopify Open Source") to protect `Net::HTTP`, MySQL, Redis, and gRPC services with a circuit breaker in Ruby. By raising an exception instantly once we detect a service being down, we save resources by not waiting for another timeout we expect to happen. In some cases rescuing these exceptions allows you to provide a fallback. [Building and Testing Resilient Ruby on Rails Applications](https://shopify.engineering/building-and-testing-resilient-ruby-on-rails-applications "Building and Testing Resilient Ruby on Rails Applications") describes how we design and unit tests such fallbacks using [Toxiproxy](https://github.com/Shopify/toxiproxy "Toxiproxy - Shopify Open Source").

The Semian readme recommends to concatenate the host and port of an HTTP endpoint to create the identifier for the resource being protected. Worldwide payment processing typically uses a single endpoint, but often payment gateways use local acquirers behind the scenes to optimize authorization rates and lower costs. For Shopify Payments credit card transactions, we add the merchant's country code to the endpoint host and port to create a more fine-grained Semian identifier, so an open circuit due to an local outage in one country doesn’t affect transactions for merchants in other countries.

Semian and other circuit breaker implementations aren’t a silver bullet that will solve all your resiliency problems by adding it to your application. It requires understanding the ways your application can fail and what falling back could look like. At scale a circuit breaker can still waste a lot of resources (and money) as well. The article [Your Circuit Breaker is Misconfigured](https://shopify.engineering/circuit-breaker-misconfigured "Your Circuit Breaker is Misconfigured") explains how to fine tune this pattern for maximum performance.

# 3\. Understand Capacity

Understanding a bit of queueing theory goes a long way in being able to reason about how a system will behave under load. Slightly summarized, [Little’s Law](https://en.wikipedia.org/wiki/Little%27s_law "Little’s Law") states that “ _the average number of customers in a system (over an interval) is equal to their average arrival rate, multiplied by their average time in the system._ ” The **arrival rate** is the amount of customers entering and leaving the system.

Some might not realize it at first, but queues are _everywhere_ : in grocery stores, traffic, factories, and as I recently rediscovered, at a festival in front of the toilets. Jokes aside, you find queues in online applications as well. A background job, a Kafka event, and a web request all are examples of units of work processed on queues. Put in a formula, Little’s Law is expressed as capacity = throughput * latency. This also means that throughput = capacity / latency. Or in more practical terms: if we have 50 requests arrive in our queue and it takes an average of 100 milliseconds to process a request, our throughput is 500 requests per second.

With the relationship between queue size, throughput, and latency clarified, we can reason about what changing any of the variables implies. An N+1 query increases the latency of a request and lowers our throughput. If the amount of requests coming in exceeds our capacity, the requests queue grows and at some point a client is waiting so long for their request to be served that they time out. At some point you need to put a limit on the amount of work coming in—your application can’t out scale the world. Rate limiting and load shedding are two techniques for this.

# 4\. Add Monitoring and Alerting

With our newfound understanding of queues, we now have a better idea of what kind of metrics we need to monitor to know our system is at risk of going down due to overload. Google’s site reliability engineering (SRE) book lists [four golden signals](https://sre.google/sre-book/monitoring-distributed-systems/ "Monitoring Distributed Systems") a user-facing system should be monitored for:

  * **Latency** : the amount of time it takes to process a unit of work, broken down between success and failures. With circuit breakers failures can happen very fast and lead to misleading graphs.
  * **Traffic** : the rate in which new work comes into the system, typically expressed in requests per minute.
  * **Errors** : the rate of unexpected things happening. In payments, we distinguish between payment failures and errors. An example of a failure is a charge being declined due to insufficient funds, which isn’t unexpected at all. HTTP 500 response codes from our financial partners on the other hand are. However a sudden increase in failures might need further investigation.
  * **Saturation** : how much load the system is under, relative to its total capacity. This could be the amount of memory used versus available or a thread pool’s active threads versus total number of threads available, in any layer of the system.



# 5\. Implement Structured Logging

Where metrics provide a high-level overview of how our system is behaving, logging allows us to understand what happened inside a single web request or background job. Out of the box Ruby on Rails logs are human-friendly but hard to parse for machines. This can work okay if you have only a single application server, but beyond that you’ll quickly want to store logs in a centralized place and make them easily searchable. This is done by using structured logging in a machine readable format, like `key=value` pairs or JSON, allows log aggregation systems to parse and index the data. 

In distributed systems, it’s useful to pass along some sort of correlation identifier. A hypothetical example is when a buyer initiates a payment at checkout, a `correlation_id` is generated by our Rails controller. This identifier is passed along to a background job that makes the API call to the payment service that handles sensitive credit card data, which contains the correlation identifier in the API parameters and SQL query comments. Because these components of our checkout process all log the `correlation_id`, we can easily find all related logs when we need to debug this payment attempt.

# 6\. Use Idempotency Keys

Distributed systems use unreliable networks, even if the networks look reliable most of the time. At Shopify’s scale, a **once in a million** chance of something unreliable occurring during payment processing means it’s happening many times a day. If this is a payments API call that timed out, we want to retry the request, but do so safely. Double charging a customer's card isn’t just annoying for the card holder, it also opens up the merchant for a potential chargeback if they don’t notice the double charge and refund it. A double refund isn’t good for the merchant's business either.

In short, we want a payment or refund to happen exactly once despite the occasional hiccups that could lead to sending an API request more than once. Our centralized payment service can track attempts, which consists of at least one or more (retried) identical API requests, by sending an idempotency key that’s unique for each one. The idempotency key looks up the steps the attempt completed (such as creating a local database record of the transaction) and makes sure we send only a single request to our financial partners. If any of these steps fail and a retried request with the same idempotency key is received, recovery steps are run to recreate the same state before continuing. [Building Resilient GraphQL APIs Using Idempotency](https://shopify.engineering/building-resilient-graphql-apis-using-idempotency "Building Resilient GraphQL APIs Using Idempotency") describes how our idempotency mechanism works in more detail.

An idempotency key needs to be unique for the time we want the request to be retryable, typically 24 hours or less. We prefer using an Universally Unique Lexicographically Sortable Identifier ([ULID](https://github.com/ulid/spec "Universally Unique Lexicographically Sortable Identifier")) for these idempotency keys instead of a random version 4 UUID. ULIDs contain a 48-bit timestamp followed by 80 bits of random data. The timestamp allows ULIDs to be sorted, which works much better with the b-tree data structure databases use for indexing. In one high-throughput system at Shopify we’ve seen a 50 percent decrease in INSERT statement duration by switching from UUIDv4 to ULID for idempotency keys.

# 7\. Be Consistent With Reconciliation

With reconciliation we make sure that our records are consistent with those of our financial partners. We reconcile individual records such as charges or refunds, and aggregates such as the current balance not yet paid out to a merchant. Having accurate records isn’t just for display purposes, they’re also used as input for tax forms were required to generate for merchants in some jurisdictions.

In case of a mismatch, we record the anomaly in our database. An example is the `MismatchCaptureStatusAnomaly`, expressing the status of a captured local charge wasn’t the same as the status as returned by our financial partners. Often we can automatically attempt to remediate the discrepancy and mark the anomaly as resolved. In cases where this isn’t possible, the developer team investigates anomalies and ships fixes as necessary.

Even though we attempt automatic fixes where possible, we want to keep track of the mismatch so we know what our system did and how often. We should rely on anomalies to fix things as a last resort, preferring solutions that prevent anomalies from being created in the first place.

# 8\. Incorporate Load testing

While Little’s Law is a useful theorem, practice is messier: the processing time for work isn’t uniformly distributed, making it impossible to achieve 100% saturation. In practice, queue size starts growing somewhere around the 70 to 80 percent mark, and if the time spent waiting in the queue exceeds the client timeout, from the client’s perspective our service is down. If the volume of incoming work is large enough, our servers can even run out of memory to store work on the queue and crash.

There are various ways we can keep queue size under control. For example, we use scriptable load balancers to throttle the amount of checkouts happening at any given time. In order to provide a good user experience for buyers, if the amount of buyers wanting to check out exceeds our capacity, we place these buyers on a waiting queue (I told you they are everywhere!) before allowing them to pay for their order. [Surviving Flashes of High-Write Traffic Using Scriptable Load Balancers](https://shopify.engineering/surviving-flashes-of-high-write-traffic-using-scriptable-load-balancers-part-i "Surviving Flashes of High-Write Traffic Using Scriptable Load Balancers") describes this system in more detail.

We regularly test the limits and protection mechanisms of our systems by simulating large volume flash sales on specifically set up benchmark stores. [Pummelling the Platform–Performance Testing Shopify](https://shopify.engineering/performance-testing-shopify "Pummelling the Platform–Performance Testing Shopify") describes our load testing tooling and philosophy. Specifically for load testing payments end-to-end, we have a bit of a problem: the test and staging environments of our financial partners don’t have the same capacity or latency distribution as production. To solve this, our benchmark stores are configured with a special benchmark gateway whose responses mimic these properties.

# 9\. Get on Top of Incident Management

As mentioned at the start of this article, we know that failure can’t be completely avoided and is a situation that we need to prepare for. An incident usually starts when the oncall service owners get paged, either by an automatic alert based on monitoring or by hand if someone notices a problem. Once the problem is confirmed, we start the incident process with a command sent to our Slack bot **spy**. 

The conversation moves to the assigned incident channel where we have three roles involved:

  * Incident Manager on Call (IMOC): responsible for coordinating the incident
  * Support Response Manager (SRM): responsible for public communication 
  * the service owner(s): who are working on restoring stability.



The article [I](https://shopify.engineering/implementing-chatops-into-our-incident-management-procedure)[mplementing ChatOps into our Incident Management Procedure](https://shopify.engineering/implementing-chatops-into-our-incident-management-procedure "mplementing ChatOps into our Incident Management Procedure") goes into more detail about the process. Once the problem has been mitigated, the incident is stopped, and the Slack bot generates a Service Disruption in our services database application. The disruption contains an initial timeline of events, Slack messages marked as important, and a list of people involved.

# 10\. Organize Incident Retrospectives

We aim to have an incident retrospective meeting within a week after the incident occurred. During this meeting:

  * we dig deep into what exactly happened
  * what incorrect assumptions we held about our systems
  * what we can do to prevent the same thing from happening again. 



Once these things are understood, typically a few action items are assigned to implement safeguards to prevent the same thing from happening again.

Retrospectives aren’t just good for trying to prevent problems, they’re also a valuable learning tool for new members of the team. At Shopify, the details of every incident are internally public for all employees to learn from. A well-documented incident can also be a training tool for newer members joining the team on call rotation, either as an archived document to refer to or by creating a [disaster role playing scenario](https://landing.google.com/sre/book/chapters/accelerating-sre-on-call.html#xref_training_disaster-rpg "Disaster Role Playing") from it.

# Scratching the Surface

I moved from my native Netherlands to Canada for this job in 2016, before Shopify became a Digital by Design company. During my work, I’m often reminded of this Dutch saying “ _trust arrives on foot, but leaves on horseback_.” Merchants’ livelihoods are dependent on us if they pick Shopify Payments for accepting payments online or in-person, and we take that responsibility seriously. While failure isn’t completely avoidable, there are many concepts and techniques that we apply to minimize downtime, limit the scope of impact, and build applications that are resilient to failure.

This top ten only scratches the tip of the iceberg, it was meant as an introduction to the kind of challenges the Shopify Payments team deals with after all. I usually recommend [Release It!](https://pragprog.com/titles/mnee2/release-it-second-edition/ "Release It! Second Edition Design and Deploy Production-Ready Software") by Michael Nygard as a good resource for team members who want to learn more.

**Bart** is a staff developer on the Shopify Payments team and has been working on the scalability, reliability, and security of Shopify’s payment processing infrastructure since 2016.

* * *

Wherever you are, your next journey starts here! If building systems from the ground up to solve real-world problems interests you, our Engineering blog has stories about other challenges we have encountered. Intrigued? Visit our [Engineering career page](http://www.shopify.com/careers/specialties/engineering?itcat=EngBlog&itterm=Post) to find out about our open positions and learn about [Digital by Design](https://www.shopify.com/careers/work-anywhere?itcat=EngBlog&itterm=CCTA-DD).

BdW

by [Bart de Water](/authors/bart-de-water)

Published on Jul 28, 2022

Share article

  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fshopify.engineering%2Fbuilding-resilient-payment-systems)
  * [Twitter](https://twitter.com/intent/tweet?text=10+Tips+for+Building+Resilient+Payment+Systems&url=https%3A%2F%2Fshopify.engineering%2Fbuilding-resilient-payment-systems&via=Shopify)
  * [LinkedIn](https://www.linkedin.com/shareArticle?mini=true&source=Shopify&title=10+Tips+for+Building+Resilient+Payment+Systems&url=https%3A%2F%2Fshopify.engineering%2Fbuilding-resilient-payment-systems)



by [Bart de Water](/authors/bart-de-water)

Published on Jul 28, 2022

• 12 minute read

[Development](/topics/development)[Introducing Ruvy](/introducing-ruvy)[Developer Tooling](/topics/developer-tooling)[Building a ShopifyQL Code Editor](/building-a-shopifyql-code-editor)

[Apps](/topics/apps)[Shopify’s platform is the Web platform](/shopifys-platform-is-the-web-platform)[Development](/topics/development)[The Engineering Story Behind Flex Comp](/building-flex-comp)

---
title: "Dynein: Building an Open-source Distributed Delayed Job Queueing System"
company: "airbnb"
url: "https://medium.com/airbnb-engineering/dynein-building-a-distributed-delayed-job-queueing-system-93ab10f05f99"
type: "system_architecture"
date: "2025-09-15"
---

# Dynein: Building an Open-source Distributed Delayed Job Queueing System

[![Andy Fang](https://miro.medium.com/v2/resize:fill:64:64/1*iKEJuZCIGikOb8X8buXr-A@2x.jpeg)](/@andyfang_dz?source=post_page---byline--93ab10f05f99---------------------------------------)

[Andy Fang](/@andyfang_dz?source=post_page---byline--93ab10f05f99---------------------------------------)

13 min read

·

Dec 10, 2019

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F93ab10f05f99&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdynein-building-a-distributed-delayed-job-queueing-system-93ab10f05f99&user=Andy+Fang&userId=278e4e619639&source=---header_actions--93ab10f05f99---------------------clap_footer------------------)

\--

18

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F93ab10f05f99&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdynein-building-a-distributed-delayed-job-queueing-system-93ab10f05f99&source=---header_actions--93ab10f05f99---------------------bookmark_footer------------------)

Listen

Share

 _Learn about the background, challenges, and future of Airbnb’s distributed scheduling and queueing system._

An Airbnb Plus listing in Argyll, Scotland

## Introduction

Asynchronous background jobs can often dramatically improve the scalability of web applications by moving time-consuming, resource-intensive tasks to the background. These tasks are often prone to failures, and retrying mechanisms often make it even more expensive to operate applications with such jobs. Having a background queue helps the web servers handle incoming web requests promptly, and reduces the likelihood of performance issues that occur when requests become backlogged.

At Airbnb, we built a job scheduling system called [Dynein](https://github.com/airbnb/dynein) for very critical use cases. Since its introduction, the system has become a very important component of our architecture, powering use cases from [delivering in-app messaging](/airbnb-engineering/discovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c) to [dynamic pricing](/airbnb-engineering/learning-market-dynamics-for-optimal-pricing-97cffbcc53e3), all with very high number of transactions per second. In this article, we will walk through the history of job queuing systems at Airbnb, explain why we built Dynein, describe how we were able to achieve its high scalability, and finally, open-source the highly scalable scheduler we built for Dynein.

## Job Queuing at Airbnb

Many systems at Airbnb take advantage of a job queue. For example, when Airbnb’s community of generous hosts join our [Open Homes](https://www.airbnb.com/openhomes) program, Airbnb will match them with non-profits or evacuees in need. The matching process is quite complicated and takes intensive compute resources, so we put the matching jobs on a job queue to ensure Airbnb’s reliability and responsiveness to those in need. In another example, before the scheduled check-in time for a reservation, we send guests a reminder that it’s time to get ready for their trip. These jobs can often be scheduled months or even years into the future, and they must be delivered reliably to ensure a good experience for the Airbnb community.

In those cases, a reliable and easy-to-use jobs scheduling system would be extremely useful and also necessary. After talking to teams at Airbnb, we decided that the scheduling system has to provide the following abilities:

  * _Reliability_. The system should not lose data if the system fails or restarts. It should guarantee at-least-once delivery of every single job.
  * _Scalability_. Airbnb believes in long-term investments, and our queuing system should be able to scale and support our needs in the future without significant scaling efforts. The scheduling system should be horizontally scalable, to allow for capacity planning as the Airbnb community grows.
  * _Isolation_. The system should be able to isolate jobs for each application. A single application’s queue being overwhelmed should not affect job processing in other services.
  * _Timing accuracy_. In lots of our use cases, applications require jobs to run within seconds of their scheduled time. The scheduler should have a p95 scheduling deviation lower than 10 seconds.
  * _Efficient queuing_. Besides scheduling the jobs reliably, the system should also offer an efficient queuing interface. For example, the job queue should support individual message success/fail acknowledgment (failing to process a single message should not affect the others), dead letter queues (messages that have failed to be processed for a number of times should be moved to a separate queue), and separate worker pools for each individual consumer (each service should run its own worker pool, rather than a shared worker pool).
  * _Useability_. The fact that the job is scheduled with a specific job scheduler and transported in a message queue should be transparent to developers. The client library should be designed to promote best practices such as exponential backoffs and rate limit handling, rather than to expose the internal of the scheduling service.
  * _Unscheduling_. A job should be able to be un-scheduled at any time, based on a unique identifier issued by the queuing system.



### Running Resque at Scale

Historically, Airbnb runs a centralized cluster of Resque workers on top of Resque Scheduler, as well as a customized scheduler for longer delays. While easy to use, the Resque cluster built years ago to support our [monolithic application](https://www.slideshare.net/AmazonWebServices/a-chronicle-of-airbnb-architecture-evolution-arc407-aws-reinvent-2018/8) is no longer sufficient for our move towards SOA (service-oriented architecture). We discovered the following issues when operating Resque at scale:

  * Resque is an at-most-once system, which means that messages aren’t guaranteed to be delivered.
  * Resque has significant scaling bottlenecks. Resque depends on a single Redis instance, and there’s [no way to use Redis cluster mode with Resque](https://github.com/resque/resque/issues/1301). We’re then limited by the memory size and network capacity of a single Redis instance.
  * We run most of our jobs in the worker cluster of our [monolithic application](https://www.slideshare.net/AmazonWebServices/a-chronicle-of-airbnb-architecture-evolution-arc407-aws-reinvent-2018/8). While Resque offers the ability to use different queues in a single application, these queues still share the same code base and Redis instance. A single bad job can often halt a large portion of the job processing workers.
  * Resque Scheduler is an extension on top of Resque that provides limited scheduling abilities. Resque Scheduler is similar to Resque in its simplicity, but its scheduling abilities are limited. For example, Resque Scheduler stores every job it’s going to run inside Redis, which means the queue size is inherently limited by the RAM size of the machine hosting Redis. It’s also difficult to dequeue a job in Resque Scheduler. While Resque Scheduler offers such API, internally, [it needs to search through the entire backlog of jobs](https://github.com/resque/resque-scheduler/blob/6c36c945a1510392a129f9d28ee0e5ee11c527df/lib/resque/scheduler/delaying_extensions.rb#L274-L288). Due to these limitations, we set tight limits on the data size and delay time for jobs using Resque Scheduler, and restrict the usage of dequeue APIs.
  * To address the limits of Resque Scheduler, we built an internal, MySQL-based system that provides long-duration delays as well as a stronger delivery guarantee and auditability. However, this system is built to be highly consistent, rather than highly scalable.



## Building the Right Queuing and Scheduling Service

With the historical context and challenges in mind, we built Dynein, a distributed delayed job queueing service. Below is a high-level overview of how we orchestrate different components in the Dynein service, and how we integrate it into different services at Airbnb. We will go through why and how we designed each component, and explain how they work together.

Press enter or click to view image in full size

 _Dynein Overview_

### Service Queues

For the queuing system of Dynein, we decided to use AWS Simple Queuing System (SQS). SQS is an interesting product in the field of queuing systems, and we find its set of tradeoffs to be an excellent choice for a job queue. SQS is true to its name: it’s a simple system to reason about and to operate in production. SQS does not have a strong ordering guarantee, nor is it intended to be used as a storage system like [Apache Kafka](https://kafka.apache.org/). However, with those constraints removed, SQS offers many properties that make it an ideal choice for most of the use cases of a job queue:

  * SQS is simple to scale up. The cost and time to provision a new queue is negligible with SQS, and at Airbnb, this step is a simple PR to our [terraform](https://www.terraform.io/) repository. This property makes SQS an ideal choice for a world of SOA, as each service can easily set up its own queue to avoid interference with other services. Historically, all of Airbnb’s job queuing is done in a centralized cluster, which comes with much scaling and operational burdens.
  * SQS is high throughput and low enough latency. On AWS’ documentation site, it documents that SQS offers infinite transactions per second. In practice, we’ve never observed rate limits from SQS, and it provides latencies low enough for Airbnb’s job queuing system.
  * SQS offers at-least-once delivery. Because Dynein is designed to be at-least-once as well, SQS guaranteeing this property means that we do not need to take additional steps to ensure message delivery.
  * SQS comes with many additional features for free, such as dead letter queues, individual message acknowledgment, access control, and encryption at rest.



### Dynein Service

We can divide Dynein jobs into two categories: immediate jobs and delayed jobs.

**Immediate Jobs**

For immediate jobs, or jobs that are scheduled to run within 15 minutes, Dynein simply works as a wrapper of the SQS API — Jobs submitted to Dynein will be relayed to an SQS queue immediately, and the job will then be consumed by consumers with the SQS dequeue API. We opted to wrap the SQS API rather than have services directly enqueue to SQS because this approach offers us expansive metrics coverage, as well as tight integration with Airbnb’s internal rate-limiting and backpressure systems. Additionally, our users can use the same API they use for delayed jobs.

**Delayed Jobs**

Dynein takes a more elaborate approach to delayed jobs. Delayed jobs, to Dynein, means deliver the right message to the right service queue at the right time. When a delayed job is submitted to Dynein, it is immediately put into an SQS queue — we call it inbound queue. This queue works as a write buffer for our scheduler, designed so that we can sustain small spikes in jobs submitted. Not only does the inbound queue protect our system from write spikes, but it also gives us clear indicating metrics that such issues are happening. SQS gives us enough time to figure out what the issue is, fix it, and then process the backlog.

Press enter or click to view image in full size

 _Dynein’s behavior in a real production incident. In this incident, the Dynein service briefly lost its connection with the job scheduler (Quartz). We see a backlog of jobs in the inbound queue as soon as the incident starts, and then the backlog being processed quickly when the incident is resolved. During the process, no user intervention was required, and no jobs were lost._

Dynein service then picks up the job from the inbound queue with a consistent ingestion rate, and stores a trigger for the job into the scheduler. At the scheduled time, Dynein service selects the jobs from the scheduler, and then enqueues the jobs into SQS. The Dynein service is completely stateless, and runs as a simple Deployment on our internal Kubernetes platform.

### Delayed Job Scheduler

As described above, a job queue is only part of the story for Dynein. There are plenty of job queues available on the market, but almost none that offer a solid scheduling story. Therefore, we decided to build the scheduler as a separate component of Dynein.

**Quartz**

With the goal in mind, we looked into Quartz. Quartz is a popular open-source job scheduling library for Java applications, and we have been using Quartz for scheduling critical jobs in production for a few years. In general, Quartz does a good job of running jobs at their scheduled time, but it was clear that there was room for improvement:

  * _Scalability_ : Quartz doesn’t have an excellent way to distribute the load among many schedulers and databases. Internally, we use Quartz with most of its locking mechanism disabled, and run many scheduler instances on a single schedules table. However, the complexity of Quartz introduces unnecessary performance overhead (more on this later).
  * _Usability_ : Quartz has a large API surface, and a high number of options to tweak. While different services have different needs, much of the configuration is repetitive. Best practices are hard to enforce across multiple services, and engineers have to learn about the architecture of Quartz to reason about their job processing system.
  * _Queuing_ : Scheduling is only a part of the story in async job processing, and another important piece is queuing. To quote the [official Quartz manual](http://www.quartz-scheduler.org/documentation/2.4.0-SNAPSHOT/faq.html), “ _Quartz is not a job queue — though it is often used as one, and can do a reasonable job of such at a small scale._ ” A queuing system is often designed with a different set of tradeoffs than that of a scheduler, and coupling the two together has significant downsides, for example, with long-running jobs. We’re also faced with two bad organizational choices if we use the quartz workers directly: either the queuing team will have to maintain the Quartz cluster running application logic for every service (similar to the monolithic Resque cluster), or each service will have to run its own Quartz cluster.



In our first iteration of Dynein, we used Quartz as the job scheduler with great success. Out of the box, Quartz provided most of the features that we need, and had a great delivery guarantee. However, as the number of services that adopt Dynein grows, we realized that we needed a system that could scale to our needs.

**Building a DynamoDB Based Scheduler**

Despite our scaling efforts, we were only able to achieve 1000 QPS (500 jobs enqueuing, 500 jobs dequeuing, not including immediate jobs) per r4.8xlarge RDS instance. We run multiple instances in order to work around this limit, but running multiple MySQL instances for a scheduling service is both operationally and financially expensive. We did extensive deep dives into Quartz, and found that query amplification is the bottleneck: a single enqueue is translated into 4 SELECT and 3 INSERT queries in Quartz. While each of the query serves an essential purpose, we’re simply not utilizing the features that they are built for. Features such as repeated schedules are simply never used, as we only care about dispatching a specific payload to SQS at a given time.

From there, we decided that adapting Quartz to suit our specific use case would take a significant amount of time as our tradeoffs are fundamentally different. We then decided to build our own scheduler, which would only support a limited set of features but would be highly scalable. We summarized the job of the scheduler into the following steps:

  * At each scheduler tick, query the database to see if there are jobs that are overdue;
  * For each of the jobs that are overdue, dispatch them into their specific SQS queue.



This query model is very simple, and can be efficiently implemented with a single index on the scheduled time column, in any database. Moreover, it can be trivially sharded — we can simply assign each job with a random ID, and then use that random ID as the sharding key.

If the above sounds familiar, that’s because it’s exactly the best-case scenario for DynamoDB! DynamoDB supports a [Partition Key and a Sort Key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html), which exactly maps to the random ID and the scheduled time for each job. DynamoDB is implemented [using b-trees internally](https://www.slideshare.net/AmazonWebServices/amazon-dynamodb-under-the-hood-how-we-built-a-hyperscale-database-dat321-aws-reinvent-2018), and therefore range queries on the Sort Key are highly efficient. Because we use a random ID as the Partition Key, our read/write load is evenly distributed across all partitions, and we can avoid one of the common pitfalls of DynamoDB: [hot partitions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html). Each partition has exactly the same load, thus making the RCU and WCU spendings on DynamoDB effective.

Press enter or click to view image in full size

 _Dynein’s simple data model._

Every time a job is added, we simply store it as a row in the DynamoDB table. The Partition Key is set to a random ID, and the Sort Key is set to the job’s schedule time concatenated with a UUID to ensure uniqueness. Besides the Partition Key, Sort Key, and the job payload, we also set the status of this job to “Scheduled”. These steps are the only feature that the service-facing Dynein instances will handle, and the actual schedulers are run on different Kubernetes Pods. These scheduler pods will each be assigned a list of partitions. At each scheduler tick, they will query DynamoDB for a list of jobs that are overdue. In order to prevent duplicate deliveries, before dispatching them to their final destination, we first use Conditional Update in DynamoDB to update the status column on the job to “Acquired” and only proceed with the dispatch if the Compare-And-Set is successful. Effectively, we are using optimistic locking. From there, the scheduler pods will simply dispatch the job to its destination SQS, and delete the job from the table.

Dynein was designed with capacity planning as a first-class citizen. A scheduler’s workload often fluctuates as traffic changes, and we need to dynamically adjust the number of scheduler instances for capacity planning. Quartz was designed to work within a statically defined set of schedulers: when you start up Quartz, you have to store the list of schedulers in its properties. As a result, adding or removing scheduler instances in Quartz is a complicated operation and capacity planning becomes difficult. As Airbnb moves its services to Kubernetes, this limitation becomes much more challenging as Pods are much more frequently rotated compared to EC2 hosts. One of the solutions is to run the set of schedulers in a [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) in Kubernetes. However, running StatefulSets is [difficult](https://elastisys.com/2018/09/18/sad-state-stateful-pods-kubernetes/), and it still doesn’t allow us to dynamically change the cluster size. Dynein was designed to work with orchestrators such as Kubernetes natively, and can be used with a standard Kubernetes deployment ([ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)), or even with an [auto-scaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/). Each of the scheduler pod maintains a watch on the ReplicaSet it’s a part of. Given the list of pods and their names, each pod is able to deterministically calculate a list of partitions that it should work on. When we add or remove pods from the ReplicaSet, the pods will simply pick up the change, and work on the new set of partitions instead. Instead of having to statically define the list of partitions for each worker in Quartz, we’re now able to dynamically adjust the number of scheduler instances based on load.

Press enter or click to view image in full size

 _Total monthly cost of infrastructure per 1,000 QPS in each scheduling system. Lower is better. While Quartz achieved our goals for scalability and reliability, it also massively increased our costs. Switching to the DynamoDB-based scheduler yielded significant cost savings, while providing an even better scalability, reliability, and operational story. The hypothetical numbers in this chart do not in any way reflect Airbnb’s production usage of these systems._

The process described above, while simple, proved to be highly effective. Each enqueue is simply a PUT operation on the table (consumes 1 WCU), and a dequeue is simply a GET, a SET, and a DELETE (consumes 2 WCUs and 1 RCU). Compared to the price of running an r4.8xlarge RDS instance, using AWS’ publicly published cost [data](https://calculator.s3.amazonaws.com/index.html), we’re able to achieve 1,000 QPS with less than ⅓ of the cost. At the same time, we offer virtually unlimited, linear scalability without the need to manually shard the data into different tables or database instances. Because of the dynamic scaling feature of DynamoDB, instead of commiting to a large instance type for our peak load, we’re able to dynamically adjust the provisioned throughput according to the seasonal load on our system. While it is possible to switch instance type of an RDS cluster, we find the operation to be too complicated and error-prone for something we want to dynamically adjust.

The architecture of Dynein allows us to swap its components freely as they are sufficiently decoupled. In our migration to the DynamoDB-based scheduler, we were able to keep the interface to the users unchanged, while providing scaling improvements behind the scenes. Our internal customers were able to get the advantages automatically while enjoying the same delivery guarantees as Quartz. Furthermore, the scheduler itself is not limited to DynamoDB. Any KV store that offers a prefix scan, such as Rocks DB or even MySQL, can be integrated with very little work.

## Conclusion and Acknowledgements

We built Dynein to reliably and effectively schedule and process the most critical tasks at Airbnb. It has been widely embraced by many product teams since its release. We’re incredibly happy with the performance and ease-of-use of the scheduler, and welcome you to see our work at: <https://github.com/airbnb/dynein>. If you enjoyed reading the post and are interested in working on distributed systems and helping travelers around the world belong anywhere, [Airbnb is hiring](https://careers.airbnb.com/)!

One of Dynein’s main contributors was [Krishna Patel](https://www.linkedin.com/in/krishnakpatel/), an intern who worked with us in Summer 2019. Thank you Krishna for your amazing impact during the summer! Also many thanks to [Xu Zhang](https://www.linkedin.com/in/zhangxu325/), [Ren Yu](https://www.linkedin.com/in/ren-yu-77385b8b/), [Michel Weksler](https://www.linkedin.com/in/michelweksler/), [Claudio Wilson](https://www.linkedin.com/in/claudio-wilson-7a983630/), [Divyahans Gupta](https://www.linkedin.com/in/divyahansg/), [Alice Liang](https://www.linkedin.com/in/alice-l-594a7128/), [Amre Shakimov](https://www.linkedin.com/in/amreshakim/), [Bruce Jin](https://www.linkedin.com/in/brucexingjin/), and the rest of Airbnb Engineering who helped with this project.

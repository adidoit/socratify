---
title: "How I stopped worrying and learned to love Cloud Inventory"
author: "https://medium.com/@maxim.savin"
url: "https://engineering.klarna.com/how-i-stopped-worrying-and-learned-to-love-cloud-inventory-723cd3c49d46?source=rss----86090d14ab52---4"
date: "2025-09-15"
---

# How I stopped worrying and learned to love Cloud Inventory
[![Maxim Savin](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*hciM-9qNwnB214Zr)](https://medium.com/@maxim.savin?source=post_page---byline--723cd3c49d46---------------------------------------)
[Maxim Savin](https://medium.com/@maxim.savin?source=post_page---byline--723cd3c49d46---------------------------------------)
9 min read
·
Jun 6, 2025
[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fklarna-engineering%2F723cd3c49d46&operation=register&redirect=https%3A%2F%2Fengineering.klarna.com%2Fhow-i-stopped-worrying-and-learned-to-love-cloud-inventory-723cd3c49d46&user=Maxim+Savin&userId=ea173cae8136&source=---header_actions--723cd3c49d46---------------------clap_footer------------------)
\--
[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F723cd3c49d46&operation=register&redirect=https%3A%2F%2Fengineering.klarna.com%2Fhow-i-stopped-worrying-and-learned-to-love-cloud-inventory-723cd3c49d46&source=---header_actions--723cd3c49d46---------------------bookmark_footer------------------)
Listen
Share
Press enter or click to view image in full size
A long time ago, as a punishment for his crimes, Hades, the king of the underworld, made Sisyphus roll a huge enchanted boulder endlessly up a steep hill. Since then, many tech companies have learned to do that at scale by the hardships of cloud configuration management.
Consider an Engineer who wants to ensure that the data that moves through their system is encrypted along the way. This is a noble goal, and to achieve it they must identify every classic load balancer in their AWS environment to replace it with an application load balancer that enforces encryption in transit. Now imagine doing that at the scale of a company like Klarna, where teams collectively own more than a thousand AWS accounts? Add to this a multitude of other configuration challenges — databases that have not been deployed in a multi-availability zone set-up, missing Cloudwatch logs, expired digital certificates, systems running on unsupported framework versions — the list is endless. Identifying and rectifying violating cloud assets often feels like an endless game of whack-a-mole played blindfolded. This is the steep price tech companies pay to operate their systems securely and confidently, day by day.
**_Klarna Engineering Platform (KEP)_**has been on a mission to facilitate configuration management for Klarna Engineers. After a few iterations we have built an ecosystem of Klarna services designed to collect, normalize, map, and serve data on ICT assets within Klarna’s cloud infrastructure. We call this system**_Cloud Inventory_**.
Over the last few months Klarna has:
* Rolled out over 100 automated controls enhancing every aspect of our configuration management (security, governance, and operational excellence), each control aimed to help system owners to identify and fix violations quickly.
* Reduced the lead time of rolling out a control from several weeks to a matter of minutes
* And as a result, successfully completed several large-scale cloud infrastructure optimization projects, such as a company-wide clean-up of RDS and EBS snapshots, without any incidents.
In what follows, I will walk you through the foundation and the building blocks of**_Cloud Inventory_**as well as share some of the use cases it enables.
**In the beginning there was a SystemID**
It is often simple statements that are most important. Let’s begin with a fundamental statement about configuration management that the whole Klarna technology rests on:**_every system at Klarna must have a SystemID_**. A SystemID is a unique identifier of a system. It is hard to give a “scientific” definition of what the scope for a given SystemID should be, but we are following some guiding principles:
* A SystemID should not cover multiple things that are naturally handled by different teams
* A SystemID should cover things that are logically developed as a unit which interact through non-published APIs, loosely defined as “code base”
SystemID is required in several key processes of the software development lifecycle. For example, without it, one cannot create an access group or set up an AWS account. This simple yet powerful concept helps to define the boundaries of a system. Klarna maintains a dedicated systems registry in order to store and manage the lifecycle of SystemIDs. In the context of Cloud Inventory, System Owners are required to tag their cloud assets with SystemID tags (preferably by configuration), and it enables**_everything_**— ownership, accountability, governance.
**Cloud Inventory**
Now, onto the main secret, which is quite simple! As the whole Universe is based on a concept of graph theory where love is an edge, no wonder graphs are so helpful in configuration management. We employ a graph database solution to build a model of our cloud inventory featuring teams, systems and related ICT assets. For example, the graph example below represents a system “Klarna App” along with its assets and dependencies.
Press enter or click to view image in full size
Pic 1. A system and its assets represented in a graph
This representation includes both cloud resources owned by the system — such as instances, databases, security groups, load balancers, VPC endpoints — as well as ICT assets external to our cloud providers, such as artifact repositories, threat models, user access groups, experimentation platform features, Kafka topics, and more. The most valuable aspect is that all these assets, residing in various siloed sources of truth across the company, are unified into**_a single graph with established relationships_**— all thanks to the little thing called SystemID. This also explains why we do not tend to rely on AWS-specific solutions like AWS Config — they are severely limited since they can only involve AWS data but also lack context when it comes to change management (more on that below).
How do we achieve this? There are two main components to Cloud Inventory:
* A graph database. We currently use a [third-party platform _JupiterOne_](https://www.jupiterone.com/) __ which provides us a database that has direct integrations with our cloud providers. The database acts like a “giant cache” of Klarna’s cloud inventory, fully refreshed every few hours.
* A set of ETL jobs. We have built synchronization jobs that run at specified polling intervals to set up custom integrations with our internal sources of truth — such as organizational data and the systems registry. These integrations are established through dedicated S3 buckets with distributed ownership, where different teams own various parts of the inventory.
The central question that the Cloud Inventory solution enables us to answer is:**_“What is the current state of what we own as a company in the cloud?”._**With the support of the graph query language, we can break down this question into specific queries, obtaining granular-level answers.
Below, I will present a use case illustrating how we assist Klarna system owners in optimizing their inventory — leading to operational cost savings and fewer incidents.
**So what is a target spec?**
Every engineer’s goal is to make sure their systems run reliably, securely and efficiently. Suppose a Klarna team runs a system with an RDS instance. This team has a dashboard displaying reports, such as one suggesting that**_“All production databases must be enabled for multiple availability zones”_**. Teams are expected to act on these reports within a specified SLA.
We call these reports “**_target specifications_**” because they define the target state which we expect an asset to achieve. Every target specification has several qualities:
* It has context — every target specification will have a short, concise and relatively human friendly description of what is expected of the team and why it is important to address it.
* Evidence collection is automated — scoring whether an asset meets the expectation or deviates from it is expressed as a simple query
* Evidence is precise and verifiable — evidence of an asset meeting or deviating from the expectation is on the exact configuration item (e.g. the exact database instance)
* It is actionable — it explains how to achieve the target in a user-friendly way. The goal is that an Engineer should have everything they need to act on a target spec just by having a glance at it.
* It is configured as code. Every target specification is essentially an _.md file_ in a repository, meaning that anyone with basic Git knowledge can contribute and propose changes to both asset identification methods and the instructions provided to asset owners.
Press enter or click to view image in full size
As you’ve probably noticed, target specifications are just organized and scheduled queries to the graph database, identifying deviations from the target state and exposing them to system owners.
Press enter or click to view image in full size
Pic 3. How a target spec looks like in the repo
And what about impact? In the past few months, Klarna has released more than 100 target specifications covering nearly every aspect of configuration management — from database operations and tagging to logs and encryption. Target specifications have scaled well and are on track to fully replace manual surveys and reviews previously used for governance. They have proven highly effective. For instance, in enabling Multi-AZ for RDS instances, the number of identified violations has halved and continues to decline steadily.
Another straightforward example is a target spec for untagged database snapshots older than 90 days. At the time of its introduction, Klarna had roughly 1,500 such snapshots in its cloud inventory. One month later, this number dropped to about 500 as system owners proactively reduced waste, resulting in €10k — €20k monthly savings on the AWS bill from a single target spec.
Target specifications powered by Cloud Inventory have significantly enhanced Klarna’s security, reliability, and performance.
Press enter or click to view image in full size
Pic 4. A steady decline in the number of violating assets after activation
**Lessons Learned**
We’ve been working on Cloud Inventory out for a bit more than a year and here are some of the learnings so far:
***Ownership matters.**Since Cloud Inventory touches nearly every source of truth within the company, it was crucial to define the owners of the running integrations and data in the graph. Clear ownership is key to successful scaling and incident resolution and without it, things are doomed to deteriorate over time.
* Change management starts with being**clear on expectations**. The set format of target specifications forced us to formulate expectations in a concise and clear manner, increasing the likelihood of teams acting on violations. We also learned that even small changes with a limited scope are best conducted via target specs, as they can be scaled very gracefully and teams benefit from having every kind of change request on a single dashboard.
***Focus on the data model**when dealing with graphs. We quickly learned that the complexity of AWS integration alone is substantial. Scaling Cloud Inventory to 20+ different integrations was an opportunity to introduce chaos. Therefore we dedicated considerable time to aligning data standards (e.g., entity classes and types) and naming conventions to ensure Cloud Inventory scaled gracefully.
***Simplification is key.**Overall, in the case of target specifications, we chose to opt for a very straightforward, almost “one-size-fits-all” model targeting every type of asset and it suited us very well.
***Show value early.**Demonstrating immediate direct value was essential to convince our customers within Klarna to integrate their data sources with Cloud Inventory. Initially, the central team drove the integration process by selecting and implementing sync jobs with the most relevant data sources. However, after a few successful cases that proved the value of established integrations (such as the ability to set up relevant target specs), we began to see data source owners proactively proposing integrations. We’ve transitioned from a “supplier push” to a “customer pull” in our rollout.
**Next steps**
Although Cloud Inventory is now an integral part of the Klarna Engineering Platform, our journey is far from over. Our current goals to advance it further include:
***Expanding data sources**. We still have some data sources not yet covered, which we are eager to bring in to enable more transparency and control. Our current focus includes ingesting an inventory of Jenkins instances, team on-call schedules, and code repositories.
***Leveraging AI**. We are actively using Klarna’s internal AI Assistant to help teams to validate any manual inputs to the graph’s entities. For example, AI is already helping to reason about and cross-check information on system attributes (such as availability, integrity, confidentiality classifications) and system dependencies. In the future, we aim to empower our users with AI-driven support for managing the data model and constructing queries to the graph.
***Making better use of positive evidence**. We aim to expand the perspective of target specifications as automated controls, integrating “good evidence” in addition to violations. This will not only act as positive motivation for system owners but also align with risk control frameworks and facilitate regulatory compliance.
By continuously improving Cloud Inventory, we strive to set new benchmarks in cloud configuration management, driving operational excellence, and assisting Klarna system owners in making smart choices about their cloud assets. I am excited to see what comes next!

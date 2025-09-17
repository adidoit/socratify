---
title: "Achieving High Availability with distributed database on Kubernetes at Airbnb"
author: "https://medium.com/@tema.danilov"
url: "https://medium.com/airbnb-engineering/achieving-high-availability-with-distributed-database-on-kubernetes-at-airbnb-58cc2e9856f4?source=rss----53c7c27702d5---4"
published_date: "2025-07-28T18:00:59.220Z"
downloaded_date: "2025-09-15T10:24:39.231937"
company: "airbnb"
blog_type: "mainstream"
technical_score: 41
quality_rating: "⭐⭐⭐"
---

# **Achieving High Availability with distributed database on Kubernetes at Airbnb**
[![Artem Danilov](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](/@tema.danilov?source=post_page---byline--58cc2e9856f4---------------------------------------)
[Artem Danilov](/@tema.danilov?source=post_page---byline--58cc2e9856f4---------------------------------------)
6 min read
·
Jul 28, 2025
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F58cc2e9856f4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fachieving-high-availability-with-distributed-database-on-kubernetes-at-airbnb-58cc2e9856f4&user=Artem+Danilov&userId=418607e82e3e&source=---header_actions--58cc2e9856f4---------------------clap_footer------------------)
\--
1
[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F58cc2e9856f4&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fachieving-high-availability-with-distributed-database-on-kubernetes-at-airbnb-58cc2e9856f4&source=---header_actions--58cc2e9856f4---------------------bookmark_footer------------------)
Listen
Share
Press enter or click to view image in full size
## Introduction
Traditionally, organizations have deployed databases on costly, high-end standalone servers using sharding for scaling as a strategy. As data demands grew, the limitations of this strategy became increasingly evident with increasingly longer and more complex maintenance projects.
Increasingly distributed horizontally scalable databases are not uncommon and many of them are open source. However, running these databases reliably in the cloud with high availability, low latency and scalability, all at a reasonable cost is a problem many companies are trying to solve.
We chose an innovative strategy of deploying**a distributed database cluster across multiple Kubernetes clusters in a cloud environment**. Although currently an uncommon design pattern due to its complexity, this strategy allowed us to achieve target system reliability and operability.
In this post, we’ll share how we overcame challenges and the best practices we’ve developed for this strategy and we believe these best practices should be applicable to any other strongly consistent, distributed storage systems.
## Managing Databases on Kubernetes
Earlier this year, we integrated an open source horizontally scalable, distributed SQL database into our infrastructure.
While Kubernetes is a great tool for running stateless services, the use of Kubernetes for stateful services — like databases — is challenging, particularly around node replacement and upgrades.
Since Kubernetes lacks knowledge of data distribution across nodes, each node replacement requires careful data handling to prevent data quorum loss and service disruption, this includes copying the data before replacing a node.
At Airbnb, we opted to attach storage volumes to nodes using AWS EBS, this allows quick volume reattachment to new virtual machines upon node replacement. Thanks to Kubernetes’ Persistent Volume Claims ([PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#binding)), this reattachment happens automatically. In addition we need to allow time for a new storage node to catch up with the cluster’s current state before moving to the next node replacement. For this, we rely on the custom [k8s operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)[,](https://github.com/pingcap/tidb-operator) which allows us to customize various Kubernetes operations according to specifics of the application.
## Coordinating Node Replacement
Node replacements occur for various reasons, from [AWS instance retirement](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-retirement.html) to Kubernetes upgrades or configuration changes. To address these cases, we categorize node replacement events into three groups:
1. **Database-initiated events:** Such as config changes or version upgrades.
2. **Proactive infrastructure events:** Like instance retirements or node upgrades.
3. **Unplanned infrastructure failures:** Such as a node becoming unresponsive.
To safely manage node replacements for database-initiated events, we implemented a a custom check in the k8s-operator that verifies that all nodes are up and running before deleting any pod.
In order to serialize it with the second group initiated by infrastructure, we implemented [an admission hook](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) in k8s to intercept pod eviction. This admission hook rejects any attempt to evict the pod, but assigns a custom annotation on the pod which our customer database k8s-operator watches and acts on to safely delete the pod serializing it with any database-initiated node replacements described above.
Node replacements due to unplanned infrastructure failure events like hardware failure, can’t be coordinated. But we can still improve availability by ensuring that any node replacement event from the first two groups will be blocked until the failed hardware is replaced.
In our infrastructure the k8s operator handles both proactive and infrastructure-triggered node replacements, maintaining data consistency in the presence of node replacements and ensuring that unplanned events don’t impact ongoing maintenance.
## Kubernetes Upgrades
Regular Kubernetes upgrades are essential but can be high-risk operations, especially for databases. Cloud managed Kubernetes might not offer rollbacks once the control plane is upgraded, posing a potential disaster recovery challenge if something goes wrong. While our approach involves using self-managed Kubernetes clusters, which does allow rolling back the control plane, a bad Kubernetes upgrade could still cause service disruption till rollback is completed.
## Ensuring Fault Tolerance with Multiple Kubernetes clusters
At Airbnb, we think the best way to achieve high regional availability is to deploy each database across three independent Kubernetes clusters, each within a different AWS availability zone ([AZ](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/availability-zones.htm)). AWS uses availability zones not just for independent power, networking, and connectivity, but they also do rollouts zone by zone. Our Kubernetes cluster alignment with AWS AZ also means that any underlying infrastructure issues or bad deployments have a limited blast radius as they are restricted to a single AZ. Internally, we also deploy a new configuration or a new database version to a part of the logical cluster running in a single Kubernetes cluster in one AZ first.
While this setup adds complexity, it significantly boosts availability by limiting the blast radius of any issues stemming from faulty deployments at every layer — whether database, Kubernetes, or AWS infrastructure.
For instance, recently, a faulty config deployment in our infrastructure abruptly terminated all VMs of a specific type in our staging Kubernetes cluster, deleting most of the query layer pods. However, since the disruption was isolated to a single Kubernetes cluster, two-thirds of our query layer nodes remained operational, preventing any impact.
We also overprovision our database clusters to ensure that, even if an entire AZ, Kubernetes cluster, or all storage nodes within a zone goes down, we still have sufficient capacity to handle traffic.
Press enter or click to view image in full size
## Leveraging AWS EBS for Reliability and Latency Handling
EBS offers two key benefits for our deployment: rapid reattachment during node replacements and superior durability compared to local disks. With EBS, we confidently run a highly available cluster using only three replicas, maintaining reliability without needing additional redundancy.
However, EBS can occasionally experience tail latency spikes, with p99 latency reaching up to 1 second. To mitigate this, we implemented a storage read timeout session variable, allowing queries to transparently retry against other storage nodes during EBS latency spikes. By default the database we use sends all requests and retries to the leader. To enable retries on storage nodes with healthy EBS, we have to allow reads from both leader and replica reads, but prefer the closest one for the original request. This brings the added benefit of reduced latency and no cross-AZ network costs, as we have a replica in each AZ. Finally, for use cases that permit it, we leverage stale reads feature, enabling reads to be served independently by the replica without requiring synchronous calls to the leader, which may be experiencing an EBS latency spike at the time of the read.
## Conclusion: Exploring Open Source Databases on Kubernetes
Our journey running a distributed database on Kubernetes has empowered us to achieve high availability, low latency, scalability, and lower maintenance costs. By leveraging the operator pattern, multi-cluster deployments, AWS EBS, and stale reads, we’ve demonstrated that even open source distributed storage systems can thrive in cloud environments.
We already operate several database clusters in production in the described setup, with the largest one handling 3M QPS across 150 storage nodes, storing over 300+ TB of data spread across 4M internal shards. All this with 99.95% availability thanks to techniques described in this post.
For other companies considering to run open-source databases on Kubernetes, the opportunities are immense. Embrace the challenge, run open-source databases to shape these tools for enterprise use. The future of scalable, reliable data management in the cloud lies in collaboration and open-source innovation — now is the time to lead and participate.
## Acknowledgments
Thanks to Abhishek Parmar, Brian Wolfe, Chen Ding, Daniel Low, Hao Luo, Xiaomou Wang for collaboration and Shylaja Ramachandra for editing.